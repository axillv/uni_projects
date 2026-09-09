"""
Bike Analytics Processor using Apache Spark and trains ML models for bike usage prediction.
"""

import logging
import os
import time
from datetime import datetime, timedelta
from typing import Optional

import schedule
from database_connector import DatabaseConnector
from ml_model import BikeUsagePredictionModel
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import (
    avg,
    broadcast,
    col,
    count,
    from_json,
    lit,
    stddev,
    to_timestamp,
    when,
    window,
)
from pyspark.sql.functions import max as spark_max
from pyspark.sql.functions import min as spark_min
from pyspark.sql.functions import round as spark_round
from pyspark.sql.functions import sum as spark_sum
from pyspark.sql.types import (
    ArrayType,
    BooleanType,
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

from config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Reduce Spark and Kafka logging verbosity
logging.getLogger("org.apache.spark").setLevel(logging.WARN)
logging.getLogger("org.apache.hadoop").setLevel(logging.WARN)
logging.getLogger("kafka").setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)


class BikeAnalyticsProcessor:
    """
    Main processor for bike sharing analytics using Apache Spark.

    This class handles:
    - Streaming data from Kafka topics
    - Data processing and analytics
    - Machine learning model training and inference
    - Data storage to PostgreSQL
    """

    def __init__(self):
        """Initialize the Bike Analytics Processor."""
        self.config = get_config()
        self.spark: Optional[SparkSession] = None
        self.db_connector: Optional[DatabaseConnector] = None
        self.ml_model: Optional[BikeUsagePredictionModel] = None
        self._initialize_spark()
        self._initialize_components()

    def _initialize_spark(self):
        """Initialize Spark session with proper configuration."""
        logger.info("Initializing Spark session...")

        self.spark = (
            SparkSession.builder.appName(self.config.SPARK_APP_NAME)
            .master(self.config.SPARK_MASTER_URL)
            .config("spark.sql.adaptive.enabled", "true")
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
            .config("spark.sql.streaming.checkpointLocation", "/tmp/spark-checkpoint")
            .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")
            .config("spark.driver.memory", "2g")
            .config("spark.executor.memory", "2g")
            .config("spark.sql.execution.arrow.pyspark.enabled", "true")
            .getOrCreate()
        )

        self.spark.sparkContext.setLogLevel("WARN")
        logger.info(
            f"Spark session initialized successfully. "
            f"Master: {self.config.SPARK_MASTER_URL}"
        )

    def _initialize_components(self):
        """Initialize database connector and ML model."""
        logger.info("Initializing components...")
        if self.spark is None:
            raise RuntimeError("Spark session not initialized")
        self.db_connector = DatabaseConnector(self.config)
        self.ml_model = BikeUsagePredictionModel(self.spark, self.config)
        logger.info("Components initialized successfully")

    def get_kafka_stream_df(self, topic: str) -> DataFrame:
        """
        Create a Kafka streaming DataFrame for the specified topic.

        Args:
            topic: Kafka topic name

        Returns:
            Streaming DataFrame from Kafka
        """
        if self.spark is None:
            raise RuntimeError("Spark session not initialized")

        logger.info(f"Creating Kafka stream for topic: {topic}")

        return (
            self.spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", self.config.KAFKA_BOOTSTRAP_SERVER)
            .option("subscribe", topic)
            .option("startingOffsets", "latest")
            .option("maxOffsetsPerTrigger", 1000)
            .option("kafka.consumer.group.id", f"spark-{topic}-consumer")
            .load()
        )

    def get_kafka_batch_df(
        self, topic: str, start_time: Optional[str] = None
    ) -> DataFrame:
        """
        Create a Kafka batch DataFrame for the specified topic.

        Args:
            topic: Kafka topic name
            start_time: Start time for batch processing (ISO format)

        Returns:
            Batch DataFrame from Kafka
        """
        if self.spark is None:
            raise RuntimeError("Spark session not initialized")

        logger.info(f"Creating Kafka batch reader for topic: {topic}")

        reader = (
            self.spark.read.format("kafka")
            .option("kafka.bootstrap.servers", self.config.KAFKA_BOOTSTRAP_SERVER)
            .option("subscribe", topic)
        )

        if start_time:
            reader = reader.option(
                "startingOffsets", f'{{"topic":{{"0":{start_time}}}}}'
            )
        else:
            reader = reader.option("startingOffsets", "earliest")

        return reader.load()

    def parse_station_information(self, df: DataFrame) -> DataFrame:
        """
        Parse station information data from Kafka.

        Args:
            df: Raw Kafka DataFrame

        Returns:
            Parsed station information DataFrame
        """
        station_info_schema = StructType(
            [
                StructField("station_id", StringType(), True),
                StructField("name", StringType(), True),
                StructField("short_name", StringType(), True),
                StructField("lat", DoubleType(), True),
                StructField("lon", DoubleType(), True),
                StructField("capacity", IntegerType(), True),
                StructField("region_id", IntegerType(), True),
                StructField("timestamp", StringType(), True),
            ]
        )

        return (
            df.select(
                from_json(col("value").cast("string"), station_info_schema).alias(
                    "data"
                )
            )
            .select("data.*")
            .withColumn(
                "timestamp",
                to_timestamp(col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"),
            )
            .filter(col("station_id").isNotNull())
        )

    def parse_station_status(self, df: DataFrame) -> DataFrame:
        """
        Parse station status data from Kafka.

        Args:
            df: Raw Kafka DataFrame

        Returns:
            Parsed station status DataFrame
        """
        station_status_schema = StructType(
            [
                StructField("station_id", StringType(), True),
                StructField("num_bikes_available", IntegerType(), True),
                StructField("num_docks_available", IntegerType(), True),
                StructField("is_installed", BooleanType(), True),
                StructField("is_renting", BooleanType(), True),
                StructField("is_returning", BooleanType(), True),
                StructField("last_reported", StringType(), True),
                StructField("timestamp", StringType(), True),
            ]
        )

        return (
            df.select(
                from_json(col("value").cast("string"), station_status_schema).alias(
                    "data"
                )
            )
            .select("data.*")
            .withColumn(
                "timestamp",
                to_timestamp(col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"),
            )
            .withColumn("last_reported", to_timestamp(col("last_reported")))
            .withColumn(
                "total_capacity",
                col("num_bikes_available") + col("num_docks_available"),
            )
            .withColumn(
                "utilization",
                when(
                    col("total_capacity") > 0,
                    col("num_bikes_available") / col("total_capacity"),
                ).otherwise(0.0),
            )
            .filter(col("station_id").isNotNull())
        )

    def parse_weather_data(self, df: DataFrame) -> DataFrame:
        """
        Parse weather data from Kafka.

        Args:
            df: Raw Kafka DataFrame

        Returns:
            Parsed weather DataFrame
        """
        weather_schema = StructType(
            [
                StructField(
                    "main",
                    StructType(
                        [
                            StructField("temp", DoubleType(), True),
                            StructField("feels_like", DoubleType(), True),
                            StructField("humidity", IntegerType(), True),
                            StructField("pressure", IntegerType(), True),
                        ]
                    ),
                    True,
                ),
                StructField(
                    "weather",
                    ArrayType(
                        StructType(
                            [
                                StructField("id", IntegerType(), True),
                                StructField("main", StringType(), True),
                                StructField("description", StringType(), True),
                            ]
                        )
                    ),
                    True,
                ),
                StructField(
                    "wind",
                    StructType(
                        [
                            StructField("speed", DoubleType(), True),
                            StructField("deg", IntegerType(), True),
                        ]
                    ),
                    True,
                ),
                StructField(
                    "clouds",
                    StructType([StructField("all", IntegerType(), True)]),
                    True,
                ),
                StructField(
                    "rain", StructType([StructField("1h", DoubleType(), True)]), True
                ),
                StructField(
                    "snow", StructType([StructField("1h", DoubleType(), True)]), True
                ),
                StructField("visibility", IntegerType(), True),
                StructField("name", StringType(), True),
                StructField("timestamp", StringType(), True),
            ]
        )

        return (
            df.select(
                from_json(col("value").cast("string"), weather_schema).alias("data")
            )
            .select("data.*")
            .withColumn(
                "timestamp",
                to_timestamp(col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"),
            )
            .withColumn("temperature", col("main.temp") - 273.15)
            .withColumn("wind_speed", col("wind.speed"))
            .withColumn("cloudiness", col("clouds.all"))
            .withColumn(
                "precipitation",
                (col("rain.1h").isNotNull() & (col("rain.1h") > 0))
                | (col("snow.1h").isNotNull() & (col("snow.1h") > 0)),
            )
            .withColumn("city_name", lit(self.config.CITY_NAME))
            .select(
                "timestamp",
                "city_name",
                "temperature",
                "wind_speed",
                "cloudiness",
                "precipitation",
                "main.humidity",
                "main.pressure",
            )
            .filter(col("temperature").isNotNull())
        )

    def calculate_hourly_analytics(
        self, station_status_df: DataFrame, weather_df: DataFrame
    ) -> DataFrame:
        """
        Calculate hourly analytics by joining station status with weather data.

        Args:
            station_status_df: Station status DataFrame
            weather_df: Weather DataFrame

        Returns:
            Hourly analytics DataFrame
        """
        logger.info("Calculating hourly analytics...")

        # Aggregate station status by hour
        hourly_station_stats = (
            station_status_df.withWatermark("timestamp", "10 minutes")
            .groupBy(window(col("timestamp"), "1 hour", "1 hour").alias("window"))
            .agg(
                avg("utilization").alias("average_docking_station_utilisation"),
                spark_max("utilization").alias("max_docking_station_utilisation"),
                spark_min("utilization").alias("min_docking_station_utilisation"),
                stddev("utilization").alias("std_dev_docking_station_utilisation"),
                count("station_id").alias("total_stations"),
                spark_sum("num_bikes_available").alias("total_bikes_available"),
                spark_sum("num_docks_available").alias("total_docks_available"),
            )
            .select(
                col("window.start").alias("timestamp"),
                col("average_docking_station_utilisation"),
                col("max_docking_station_utilisation"),
                col("min_docking_station_utilisation"),
                col("std_dev_docking_station_utilisation"),
                col("total_stations"),
                col("total_bikes_available"),
                col("total_docks_available"),
            )
        )

        # Get weather data for the same time windows
        hourly_weather = (
            weather_df.withWatermark("timestamp", "10 minutes")
            .groupBy(
                window(col("timestamp"), "1 hour", "1 hour").alias("window"),
                col("city_name"),
            )
            .agg(
                avg("temperature").alias("temperature"),
                avg("wind_speed").alias("wind_speed"),
                spark_max("precipitation").cast("boolean").alias("precipitation"),
                avg("cloudiness").alias("cloudiness"),
            )
            .select(
                col("window.start").alias("timestamp"),
                col("city_name"),
                col("temperature"),
                col("wind_speed"),
                col("precipitation"),
                col("cloudiness"),
            )
        )

        # Join station stats with weather data
        hourly_analytics = hourly_station_stats.join(
            broadcast(hourly_weather), on="timestamp", how="inner"
        ).select(
            col("timestamp"),
            col("city_name"),
            spark_round(col("temperature"), 2).alias("temperature"),
            spark_round(col("wind_speed"), 2).alias("wind_speed"),
            col("precipitation"),
            spark_round(col("cloudiness"), 0).cast("int").alias("cloudiness"),
            spark_round(col("average_docking_station_utilisation"), 4).alias(
                "average_docking_station_utilisation"
            ),
            spark_round(col("max_docking_station_utilisation"), 4).alias(
                "max_docking_station_utilisation"
            ),
            spark_round(col("min_docking_station_utilisation"), 4).alias(
                "min_docking_station_utilisation"
            ),
            spark_round(col("std_dev_docking_station_utilisation"), 4).alias(
                "std_dev_docking_station_utilisation"
            ),
            col("total_stations"),
            col("total_bikes_available"),
            col("total_docks_available"),
        )

        logger.info("Hourly analytics calculated successfully")
        return hourly_analytics

    def process_streaming_data(self):
        """Process streaming data from Kafka topics."""
        logger.info("Starting streaming data processing...")

        try:
            # Create streaming DataFrames
            station_info_stream = self.get_kafka_stream_df(
                self.config.TOPIC_STATION_INFO
            )
            station_status_stream = self.get_kafka_stream_df(
                self.config.TOPIC_STATION_STATUS
            )
            weather_stream = self.get_kafka_stream_df(self.config.TOPIC_WEATHER_DATA)

            # Parse the data
            parsed_station_info = self.parse_station_information(station_info_stream)
            parsed_station_status = self.parse_station_status(station_status_stream)
            parsed_weather = self.parse_weather_data(weather_stream)

            # Calculate analytics
            analytics = self.calculate_hourly_analytics(
                parsed_station_status, parsed_weather
            )

            # Write to database
            query = (
                analytics.writeStream.outputMode("append")
                .foreachBatch(self._write_analytics_to_db)
                .option("checkpointLocation", "/tmp/spark-checkpoint/analytics")
                .trigger(processingTime="5 minutes")
                .start()
            )

            logger.info("Streaming query started successfully")

            # Process hourly summaries (ML training is manual only)
            hourly_summaries_enabled = (
                os.getenv("HOURLY_SUMMARIES_ENABLED", "true").lower() == "true"
            )

            if hourly_summaries_enabled:
                schedule.every().hour.at(":05").do(self._process_hourly_summaries)

                while query.isActive:
                    schedule.run_pending()
                    time.sleep(60)
            else:
                query.awaitTermination()

        except Exception as e:
            logger.error(f"Error in streaming processing: {e}")
            raise

    def process_batch_data(self, target_hour: Optional[str] = None):
        """
        Process batch data for a specific time period.

        Args:
            target_hour: Target hour for processing (ISO format)
        """
        logger.info(f"Starting batch data processing for hour: {target_hour}")

        try:
            # Determine time range
            if target_hour:
                start_time = datetime.fromisoformat(target_hour.replace("Z", "+00:00"))
            else:
                start_time = datetime.now().replace(
                    minute=0, second=0, microsecond=0
                ) - timedelta(hours=1)

            end_time = start_time + timedelta(hours=1)
            logger.info(f"Processing data from {start_time} to {end_time}")

            # Read batch data
            station_info_df = self.get_kafka_batch_df(self.config.TOPIC_STATION_INFO)
            station_status_df = self.get_kafka_batch_df(
                self.config.TOPIC_STATION_STATUS
            )
            weather_df = self.get_kafka_batch_df(self.config.TOPIC_WEATHER_DATA)

            # Parse the data
            parsed_station_info = self.parse_station_information(station_info_df)
            parsed_station_status = self.parse_station_status(station_status_df)
            parsed_weather = self.parse_weather_data(weather_df)

            # Filter by time range
            time_filter = (col("timestamp") >= start_time) & (
                col("timestamp") < end_time
            )
            parsed_station_status = parsed_station_status.filter(time_filter)
            parsed_weather = parsed_weather.filter(time_filter)

            # Calculate analytics
            analytics = self.calculate_hourly_analytics(
                parsed_station_status, parsed_weather
            )

            # Cache for multiple operations
            analytics.cache()

            # Write to database
            self._write_analytics_to_db(analytics, None)

            logger.info(f"Batch processing completed for hour: {target_hour}")

        except Exception as e:
            logger.error(f"Error in batch processing: {e}")
            raise

    def _write_analytics_to_db(self, df: DataFrame, batch_id):
        """
        Write analytics DataFrame to PostgreSQL database.

        Args:
            df: Analytics DataFrame
            batch_id: Batch ID (for streaming)
        """
        try:
            if df.count() == 0:
                logger.info("No data to write to database")
                return

            logger.info(f"Writing {df.count()} records to database")

            # Write to PostgreSQL (no ML predictions - those are manual only)
            if self.db_connector:
                self.db_connector.write_hourly_summaries(df)

            logger.info("Data written to database successfully")

        except Exception as e:
            logger.error(f"Error writing to database: {e}")
            raise

    def _process_hourly_summaries(self):
        """
        Process hourly summaries by reading recent Kafka data and generating analytics.
        This runs every hour to create summaries for the past hour.
        """
        try:
            logger.info("Processing hourly summaries...")

            # Calculate the previous hour's time range
            now = datetime.now()
            end_time = now.replace(minute=0, second=0, microsecond=0)
            start_time = end_time - timedelta(hours=1)

            logger.info(f"Processing summaries for {start_time} to {end_time}")

            # Read batch data for the past hour
            station_status_df = self.get_kafka_batch_df(
                self.config.TOPIC_STATION_STATUS
            )
            weather_df = self.get_kafka_batch_df(self.config.TOPIC_WEATHER_DATA)

            # Parse the data
            parsed_station_status = self.parse_station_status(station_status_df)
            parsed_weather = self.parse_weather_data(weather_df)

            # Filter by time range
            time_filter = (col("timestamp") >= start_time) & (
                col("timestamp") < end_time
            )
            parsed_station_status = parsed_station_status.filter(time_filter)
            parsed_weather = parsed_weather.filter(time_filter)

            # Calculate analytics
            analytics = self.calculate_hourly_analytics(
                parsed_station_status, parsed_weather
            )

            # Write to database
            if analytics.count() > 0:
                self._write_analytics_to_db(analytics, None)
                logger.info("Hourly summaries processed successfully")
            else:
                logger.warning("No data found for hourly summary processing")

        except Exception as e:
            logger.error(f"Error processing hourly summaries: {e}")

    def run_ml_training(self):
        """
        Manual ML model training and predictions.
        This method should be called explicitly when ML training is desired.
        """
        logger.info("Manual ML training requested...")
        self._run_ml_predictions()

    def _run_ml_predictions(self):
        """Run ML model training and predictions."""
        try:
            logger.info("Running ML model training and predictions...")

            if not self.db_connector or not self.ml_model:
                logger.warning("Database connector or ML model not initialized")
                return

            # Get historical data for training
            historical_data = self.db_connector.read_historical_data(days=7)

            if historical_data is not None and len(historical_data) > 100:
                # Train the model
                self.ml_model.train_model(historical_data)

                # Update predictions for recent data
                recent_data = self.db_connector.read_recent_data(hours=24)
                if recent_data is not None and len(recent_data) > 0:
                    # Convert to Spark DataFrame for ML model
                    if self.spark:
                        spark_df = self.spark.createDataFrame(recent_data)
                        updated_data = self.ml_model.add_predictions(spark_df)
                        # Convert back to Pandas for database update
                        pandas_df = updated_data.toPandas()
                        self.db_connector.update_predictions(pandas_df)

                logger.info("ML predictions completed successfully")
            else:
                logger.warning("Insufficient data for ML model training")

        except Exception as e:
            logger.error(f"Error in ML predictions: {e}")

    def run(self):
        """Main execution method."""
        logger.info(
            f"Starting Bike Analytics Processor in {self.config.SPARK_PROCESSING_MODE} mode"
        )

        try:
            processing_mode = self.config.SPARK_PROCESSING_MODE.lower()

            if processing_mode == "streaming":
                self.process_streaming_data()
            elif processing_mode == "batch":
                self.process_batch_data()
            elif processing_mode == "hourly":
                target_hour = os.getenv("TARGET_HOUR")
                self.process_batch_data(target_hour)
            else:
                raise ValueError(f"Unknown processing mode: {processing_mode}")

        except KeyboardInterrupt:
            logger.info("Processing interrupted by user")
        except Exception as e:
            logger.error(f"Error in main processing: {e}")
            raise
        finally:
            if self.spark:
                self.spark.stop()
            logger.info("Bike Analytics Processor stopped")


def main():
    """Main function."""
    processor = BikeAnalyticsProcessor()
    processor.run()


if __name__ == "__main__":
    main()
