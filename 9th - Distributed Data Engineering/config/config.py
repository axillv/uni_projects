import os
from typing import ClassVar

from dotenv import load_dotenv

env_path = ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    # HTTP
    HTTP_REQUEST_TIMEOUT = int(os.getenv("HTTP_REQUEST_TIMEOUT", "30"))  # 30 seconds
    HTTP_MAX_RETRIES = int(os.getenv("HTTP_MAX_RETRIES", "3"))

    # Weather API
    CITY_NAME = os.getenv("CITY_NAME", "New York")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    WEATHER_BASE_URL = os.getenv(
        "WEATHER_BASE_URL", "https://api.openweathermap.org/data/2.5/weather"
    )
    WEATHER_LAT = float(os.getenv("WEATHER_LAT", "40.7128"))  # NYC latitude
    WEATHER_LON = float(os.getenv("WEATHER_LON", "-74.0060"))  # NYC longitude
    WEATHER_API_ENDPOINT = (
        f"?lat={WEATHER_LAT}&lon={WEATHER_LON}&appid={OPENWEATHER_API_KEY}"
    )

    # GBFS API
    GBFS_BASE_URL = os.getenv("GBFS_BASE_URL", "https://gbfs.lyft.com/gbfs/2.3/bkn/en")
    GBFS_STATION_INFO_ENDPOINT = os.getenv(
        "GBFS_STATION_INFO_ENDPOINT", "station_information.json"
    )
    GBFS_STATION_STATUS_ENDPOINT = os.getenv(
        "GBFS_STATION_STATUS_ENDPOINT", "station_status.json"
    )

    # Producers
    PRODUCER_INTERVAL = int(os.getenv("PRODUCER_INTERVAL", "300"))  # 5 minutes

    # Kafka
    KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER", "kafka:9092")
    KAFKA_ACKS = os.getenv("KAFKA_ACKS", "1")  # Leader acknowledgment
    KAFKA_RETRIES = int(os.getenv("KAFKA_RETRIES", "5"))
    TOPIC_STATION_INFO = os.getenv("KAFKA_TOPIC_STATION_INFO", "station_information")
    TOPIC_STATION_STATUS = os.getenv("KAFKA_TOPIC_STATION_STATUS", "station_status")
    TOPIC_WEATHER_DATA = os.getenv("KAFKA_TOPIC_WEATHER_DATA", "weather_data")

    # PostgreSQL Database
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB = os.getenv("POSTGRES_DB", "bike_analytics")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")

    # Spark Configuration
    SPARK_MASTER_URL = os.getenv("SPARK_MASTER_URL", "local[*]")
    SPARK_APP_NAME = os.getenv("SPARK_APP_NAME", "BikeAnalyticsProcessor")
    SPARK_PROCESSING_MODE = os.getenv(
        "SPARK_PROCESSING_MODE", "batch"
    )  # batch or hourly

    # Data Processing Configuration
    HOURLY_SUMMARIES_ENABLED = (
        os.getenv("HOURLY_SUMMARIES_ENABLED", "true").lower() == "true"
    )

    # ML Training Configuration (manual only - no automatic scheduling)
    ML_TRAINING_ENABLED = os.getenv("ML_TRAINING_ENABLED", "false").lower() == "true"


config = Config()


def get_config():
    return config
