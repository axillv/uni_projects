"""A producer for processing and publishing GBFS (General Bikeshare Feed Specification)
data."""

import logging
import time

from config import get_config
from producers import GenericAPIProducer

logger = logging.getLogger(__name__)


class GBFSProducer(GenericAPIProducer):
    """
    This class fetches station information and status from the GBFS API, processes the
    data, and sends it to Kafka topics.

    Attributes:
        topic_station_info (str): Kafka topic for station information.
        topic_station_status (str): Kafka topic for station status.
        station_information_endpoint (str): API endpoint for station information.
        station_status_endpoint (str): API endpoint for station status.
    """

    def __init__(self):
        """
        Initialize GBFSProducer with GBFS-specific configuration.
        """
        self.config = get_config()
        self.topic_station_info = self.config.TOPIC_STATION_INFO
        self.topic_station_status = self.config.TOPIC_STATION_STATUS
        self.station_information_endpoint = self.config.GBFS_STATION_INFO_ENDPOINT
        self.station_status_endpoint = self.config.GBFS_STATION_STATUS_ENDPOINT

        super().__init__(url=self.config.GBFS_BASE_URL, client_id="gbfs-producer")

    def process_gbfs_data(self, data: dict, topic: str):
        """
        Process GBFS data and send it to the specified Kafka topic.

        Args:
            data (dict): Raw GBFS data fetched from the API.
            topic (str): Kafka topic to send the data to.
        """
        stations = data.get("data", {}).get("stations", [])
        for station in stations:
            enriched_data = self.add_timestamp(station)
            self.send_to_kafka(topic=topic, value=enriched_data)

    def fetch_and_process(self):
        """
        Fetch and process station information and status from the GBFS API.
        """
        station_info = self.fetch_station_information()
        if station_info:
            self.process_gbfs_data(station_info, self.topic_station_info)

        station_status = self.fetch_station_status()
        if station_status:
            self.process_gbfs_data(station_status, self.topic_station_status)

    def fetch_station_information(self) -> dict | None:
        """
        Fetch station information from the GBFS API.

        Returns:
            dict | None: Station information data if successful, None otherwise.
        """
        logger.info(
            f"Fetching station information from: {self.station_information_endpoint}"
        )
        data = self.safe_http_request(self.station_information_endpoint)
        if data and self.validate_gbfs_data(data):
            logger.info(
                f"Fetched {len(data.get('data', {}).get('stations', []))} stations"
            )
            return data
        logger.error("Failed to fetch or validate station information")
        return None

    def fetch_station_status(self) -> dict | None:
        """
        Fetch real-time station status from the GBFS API.

        Returns:
            dict | None: Station status data if successful, None otherwise.
        """
        logger.debug(f"Fetching station status from: {self.station_status_endpoint}")
        data = self.safe_http_request(self.station_status_endpoint)
        if data and self.validate_gbfs_data(data):
            logger.debug(
                f"Fetched status for {len(data.get('data', {}).get('stations', []))} "
                "stations"
            )
            return data
        logger.error("Failed to fetch or validate station status")
        return None

    @staticmethod
    def validate_gbfs_data(data: dict) -> bool:
        """
        Validate the structure of GBFS data.

        Args:
            data (dict): GBFS data to validate.

        Returns:
            bool: True if the data structure is valid, False otherwise.
        """
        return "data" in data and "stations" in data["data"]


def main():
    """
    Main function to run the GBFSProducer in a loop with a configurable interval.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Reduce Kafka logging verbosity
    logging.getLogger("kafka").setLevel(logging.CRITICAL)
    logging.getLogger("kafka.conn").setLevel(logging.CRITICAL)
    logging.getLogger("kafka.client").setLevel(logging.CRITICAL)

    try:
        # Initialize the GBFSProducer
        logger.info("Initializing GBFS Producer...")
        producer = GBFSProducer()
        logger.info("GBFS Producer initialized successfully")

        # Fetch the producer interval from the configuration
        interval = producer.config.PRODUCER_INTERVAL
        logger.info(f"Producer will run every {interval} seconds")

        # Run the producer in a loop
        while True:
            try:
                logger.info("Starting data fetch and process cycle")
                producer.fetch_and_process()
                logger.info("Data fetch and process cycle completed")
            except Exception as e:
                logger.error(f"An error occurred during fetch and process: {e}")

            # Wait for the specified interval before the next iteration
            logger.info(f"Waiting {interval} seconds before next cycle")
            time.sleep(interval)

    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        raise


if __name__ == "__main__":
    main()
