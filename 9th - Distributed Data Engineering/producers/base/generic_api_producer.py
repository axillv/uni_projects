"""A generic API producer that fetches data from an API and sends it to Kafka."""

import json
import logging
import queue
import threading
import time
import traceback
from threading import Thread
from typing import Any

import requests
from confluent_kafka import Producer

from config import get_config

logger = logging.getLogger(__name__)


class GenericAPIProducer:
    """
    This class handles HTTP requests, retries, and Kafka message production with
    automatic queuing and retry mechanisms. It is designed to be extended for
    specific API integrations.

    Attributes:
        url (str): Base URL of the API.
        client_id (str): Identifier for the Kafka producer client.
        timeout (int): HTTP request timeout in seconds.
        max_retries (int): Maximum number of HTTP request retries.
        message_queue (queue.Queue): Queue for storing messages to be sent to Kafka.
        kafka_producer (Producer | None): Confluent Kafka producer instance.
    """

    def __init__(self, url: str, client_id: str):
        """
        Initialize the GenericAPIProducer.

        Args:
            url (str): Base URL of the API.
            client_id (str): Identifier for the Kafka producer client.
        """
        self.config = get_config()
        self.url = url
        self.timeout = self.config.HTTP_REQUEST_TIMEOUT
        self.max_retries = self.config.HTTP_MAX_RETRIES
        self.client_id = client_id

        # Configure reduced Kafka logging verbosity
        logging.getLogger("confluent_kafka").setLevel(logging.WARNING)

        self.message_queue = queue.Queue(maxsize=0)  # Unlimited size

        self.kafka_producer: None | Producer = None
        self.kafka_producer_lock = threading.Lock()
        self.retry_active = True
        self._last_queue_size_log = time.time()
        self._init_kafka_producer()

        self.retry_thread = Thread(target=self._retry_loop, daemon=True)
        self.retry_thread.start()

    def _init_kafka_producer(self):
        """
        Initialize the Kafka producer instance.

        Ensures thread safety during initialization. Logs a warning if the
        initialization fails.

        Returns:
            bool: True if initialization succeeds, False otherwise.
        """
        with self.kafka_producer_lock:
            try:
                producer_config = {
                    "bootstrap.servers": self.config.KAFKA_BOOTSTRAP_SERVER,
                    "client.id": self.client_id,
                    "acks": self.config.KAFKA_ACKS,
                    "retries": self.config.KAFKA_RETRIES,
                    "compression.type": "gzip",
                    "linger.ms": 5,  # Batch messages for up to 5ms
                    "batch.size": 16384,  # 16KB batch size
                    "queue.buffering.max.messages": 100000,
                    "queue.buffering.max.ms": 500,  # Max wait time before sending
                    "message.timeout.ms": 30000,  # 30 second timeout
                }

                self.kafka_producer = Producer(producer_config)
                logger.info("Confluent Kafka producer initialized successfully")
                return True
            except Exception as e:
                logger.warning(f"Producer initialization failed: {e}")
                self.kafka_producer = None
                return False

    def _delivery_callback(self, err, msg):
        """
        Callback function for message delivery reports.

        Args:
            err: Error object if delivery failed
            msg: Message object that was delivered
        """
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.debug(
                f"Message delivered to {msg.topic()} [{msg.partition()}] "
                f"at offset {msg.offset()}"
            )

    def _retry_loop(self):
        """
        Background thread for processing queued messages with exponential backoff.

        Retries sending messages in the queue and reinitializes the Kafka producer
        if necessary. Logs the queue size periodically.
        """
        retry_delay = 1
        kafka_init_delay = 2  # Start with 2 seconds for Kafka initialization
        last_kafka_init_attempt = 0

        while self.retry_active:
            try:
                current_time = time.time()

                if self.kafka_producer and not self.message_queue.empty():
                    success = self._process_queue()
                    retry_delay = 1 if success else min(retry_delay * 2, 60)
                    kafka_init_delay = 2  # Reset Kafka init delay on success
                else:
                    if not self.kafka_producer:
                        # Only attempt Kafka initialization if enough time has passed
                        if current_time - last_kafka_init_attempt >= kafka_init_delay:
                            last_kafka_init_attempt = current_time
                            init_success = self._init_kafka_producer()
                            if not init_success:
                                # Exponential backoff for Kafka initialization
                                kafka_init_delay = min(kafka_init_delay * 2, 60)
                                logger.info(
                                    f"Kafka unavailable, retry in {kafka_init_delay}s"
                                )
                            else:
                                kafka_init_delay = 2  # Reset on successful init

                # Poll for delivery reports and handle callbacks
                if self.kafka_producer:
                    self.kafka_producer.poll(0.1)

                # Log queue size periodically
                if current_time - self._last_queue_size_log > 60:
                    if not self.message_queue.empty():
                        logger.info(f"Message queue size: {self.message_queue.qsize()}")
                    self._last_queue_size_log = current_time

                time.sleep(retry_delay)

            except Exception as e:
                logger.error(f"Error in retry loop: {e}")
                time.sleep(min(retry_delay * 2, 60))

    def _process_queue(self):
        """
        Process all messages in the queue and send them to Kafka.

        Returns:
            bool: True if all messages are processed successfully, False otherwise.
        """
        failed_messages = []
        topic, value, kwargs = None, None, None

        while not self.message_queue.empty() and self.kafka_producer:
            try:
                topic, value, kwargs = self.message_queue.get_nowait()
                logger.debug(
                    f"Processing message for topic: {topic}, value type: {type(value)}"
                )

                # Serialize the value to JSON
                json_value = json.dumps(value).encode("utf-8")

                # Produce the message
                self.kafka_producer.produce(
                    topic=topic,
                    value=json_value,
                    callback=self._delivery_callback,
                    **kwargs,
                )

            except Exception as e:
                failed_messages.append((topic, value, kwargs))
                logger.error(f"Error processing message for topic '{topic}': {e}")
                logger.error(
                    f"Value type: {type(value)}, Value content: {str(value)[:200]}"
                )
                logger.error(f"Full traceback: {traceback.format_exc()}")

            finally:
                self.message_queue.task_done()

        # Re-queue failed messages
        for msg in failed_messages:
            self.message_queue.put_nowait(msg)

        return len(failed_messages) == 0

    def send_to_kafka(self, topic, value, **kwargs):
        """
        Send a message to Kafka or queue it for retry if unavailable.

        Args:
            topic (str): Kafka topic to send the message to.
            value (Any): Message value.

        Returns:
            bool: True if the message is sent or queued successfully.
        """
        if self.kafka_producer:
            try:
                # Serialize the value to JSON
                json_value = json.dumps(value).encode("utf-8")

                # Produce the message
                self.kafka_producer.produce(
                    topic=topic,
                    value=json_value,
                    callback=self._delivery_callback,
                    **kwargs,
                )

                # Poll for delivery reports
                self.kafka_producer.poll(0)
                return True

            except Exception as e:
                logger.debug(f"Kafka send failed: {e}, queuing message for retry")
                pass

        self.message_queue.put_nowait((topic, value, kwargs))
        return True

    def safe_http_request(self, endpoint) -> dict[str, Any] | None:
        """
        Perform an HTTP GET request with retries and exponential backoff.

        Args:
            endpoint (str): API endpoint to fetch data from.

        Returns:
            dict | None: JSON response data if successful, None otherwise.
        """
        url = f"{self.url}/{endpoint}"

        for attempt in range(self.max_retries + 1):
            try:
                logger.debug(f"Making HTTP request to: {url} (attempt {attempt + 1})")
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response.json()

            except requests.exceptions.RequestException as e:
                logger.warning(f"Request error for {url}: {e} (attempt {attempt + 1})")

            if attempt < self.max_retries:
                time.sleep(2**attempt)

        logger.error(f"All retry attempts failed for {url}")
        return None

    def add_timestamp(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Add a timestamp to the given data.

        Args:
            data (dict): Data to enhance.

        Returns:
            dict: Data with added timestamp fields.
        """
        data_copy = data.copy()
        data_copy["collection_timestamp"] = time.time()
        data_copy["collection_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S UTC")
        return data_copy

    def flush(self, timeout=None):
        """
        Flush the Kafka producer and process remaining messages in the queue.

        Args:
            timeout (int | None): Maximum time to wait for flushing.
        """
        if self.kafka_producer:
            # Confluent-kafka flush method takes timeout in seconds
            timeout_seconds = timeout if timeout else 10
            self.kafka_producer.flush(timeout_seconds)

        start_time = time.time()
        while not self.message_queue.empty() and (
            timeout is None or time.time() - start_time < timeout
        ):
            self._process_queue()
            time.sleep(0.1)

    def close(self):
        """
        Shut down the producer and stop the retry thread.
        """
        self.retry_active = False
        if self.kafka_producer:
            self.flush(timeout=10)
            # Confluent-kafka doesn't need explicit close, but we can flush and poll
            self.kafka_producer.poll(1)  # Final poll for any remaining callbacks
        logger.info("Producer shut down complete")
