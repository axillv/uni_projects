"""A producer for processing and publishing weather data from OpenWeatherMap API."""

import logging
import time

from config import get_config
from producers import GenericAPIProducer

logger = logging.getLogger(__name__)


class WeatherProducer(GenericAPIProducer):
    """
    This class fetches weather data from the OpenWeatherMap API, processes the data,
    and sends it to Kafka topics.

    Attributes:
        topic_weather_data (str): Kafka topic for weather data.
        weather_data_endpoint (str): API endpoint for weather data.
    """

    def __init__(self):
        """
        Initialize WeatherProducer with weather-specific configuration.
        """
        self.config = get_config()
        self.topic_weather_data = self.config.TOPIC_WEATHER_DATA
        self.weather_data_endpoint = self.config.WEATHER_API_ENDPOINT

        super().__init__(url=self.config.WEATHER_BASE_URL, client_id="weather-producer")

    def process_weather_data(self, data: dict):
        """
        Process weather data and send it to the Kafka topic.

        Args:
            data (dict): Raw weather data fetched from the API.
        """
        enriched_data = self.add_timestamp(data)
        self.send_to_kafka(topic=self.topic_weather_data, value=enriched_data)

    def fetch_and_process(self):
        """
        Fetch and process weather data from the OpenWeatherMap API.
        """
        weather_data = self.fetch_weather_data()
        if weather_data:
            self.process_weather_data(weather_data)

    def fetch_weather_data(self) -> dict | None:
        """
        Fetch weather data from the OpenWeatherMap API.

        Returns:
            dict | None: Weather data if successful, None otherwise.
        """
        logger.info(f"Fetching weather data from: {self.weather_data_endpoint}")
        data = self.safe_http_request(self.weather_data_endpoint)
        if data and self.validate_weather_data(data):
            logger.info("Successfully fetched and validated weather data")
            return data
        logger.error("Failed to fetch or validate weather data")
        return None

    @staticmethod
    def validate_weather_data(data: dict) -> bool:
        """
        Validate the structure of weather data.

        Args:
            data (dict): Weather data to validate.

        Returns:
            bool: True if the data structure is valid, False otherwise.
        """
        return "main" in data and "weather" in data


def main():
    """
    Main function to run the WeatherProducer in a loop with a configurable interval.
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
        # Initialize the WeatherProducer
        logger.info("Initializing Weather Producer...")
        producer = WeatherProducer()
        logger.info("Weather Producer initialized successfully")

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
