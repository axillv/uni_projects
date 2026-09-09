"""
Database connector for PostgreSQL operations.

This module handles database connections and operations for the bike analytics system.
"""

import logging
from typing import Any, Dict, List, Optional

import pandas as pd
import psycopg2
from pyspark.sql import DataFrame
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)


class DatabaseConnector:
    """Database connector for PostgreSQL operations."""

    def __init__(self, config):
        """
        Initialize database connector.

        Args:
            config: Configuration object containing database settings
        """
        self.config = config
        self.connection_string = (
            f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
            f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
        )
        self.engine = None
        self._initialize_connection()

    def _initialize_connection(self):
        """Initialize database connection."""
        try:
            self.engine = create_engine(self.connection_string)
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database connection: {e}")
            raise

    def write_hourly_summaries(self, df: DataFrame):
        """
        Write hourly summaries DataFrame to PostgreSQL.

        Args:
            df: Spark DataFrame with hourly summaries
        """
        try:
            logger.info("Writing hourly summaries to database...")

            # Convert Spark DataFrame to Pandas for easier database writing
            pandas_df = df.toPandas()

            if pandas_df.empty:
                logger.info("No data to write")
                return

            # Write to PostgreSQL
            pandas_df.to_sql(
                "hourly_summaries",
                self.engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=1000,
            )

            logger.info(
                f"Successfully wrote {len(pandas_df)} records to hourly_summaries"
            )

        except Exception as e:
            logger.error(f"Error writing hourly summaries: {e}")
            raise

    def read_historical_data(self, days: int = 7) -> Optional[pd.DataFrame]:
        """
        Read historical data for ML model training.

        Args:
            days: Number of days of historical data to retrieve

        Returns:
            Pandas DataFrame with historical data or None if no data
        """
        try:
            query = """
            SELECT 
                timestamp,
                temperature,
                wind_speed,
                precipitation,
                cloudiness,
                average_docking_station_utilisation,
                max_docking_station_utilisation,
                min_docking_station_utilisation,
                std_dev_docking_station_utilisation,
                total_stations,
                total_bikes_available,
                total_docks_available
            FROM hourly_summaries
            WHERE timestamp >= NOW() - INTERVAL %s DAY
            ORDER BY timestamp DESC
            """

            df = pd.read_sql(query, self.engine, params=(days,))
            logger.info(f"Retrieved {len(df)} historical records")
            return df if not df.empty else None

        except Exception as e:
            logger.error(f"Error reading historical data: {e}")
            return None

    def read_recent_data(self, hours: int = 24) -> Optional[pd.DataFrame]:
        """
        Read recent data for ML predictions.

        Args:
            hours: Number of hours of recent data to retrieve

        Returns:
            Pandas DataFrame with recent data or None if no data
        """
        try:
            query = """
            SELECT 
                id,
                timestamp,
                temperature,
                wind_speed,
                precipitation,
                cloudiness,
                average_docking_station_utilisation,
                max_docking_station_utilisation,
                min_docking_station_utilisation,
                std_dev_docking_station_utilisation,
                total_stations,
                total_bikes_available,
                total_docks_available
            FROM hourly_summaries
            WHERE timestamp >= NOW() - INTERVAL %s HOUR
              AND predicted_utilization_next_hour IS NULL
            ORDER BY timestamp DESC
            """

            df = pd.read_sql(query, self.engine, params=(hours,))
            logger.info(f"Retrieved {len(df)} recent records for prediction")
            return df if not df.empty else None

        except Exception as e:
            logger.error(f"Error reading recent data: {e}")
            return None

    def update_predictions(self, df: pd.DataFrame):
        """
        Update ML predictions in the database.

        Args:
            df: Pandas DataFrame with predictions
        """
        try:
            if df.empty or "id" not in df.columns:
                logger.warning("No valid data for prediction updates")
                return

            # Prepare update statements
            with self.engine.connect() as conn:
                for _, row in df.iterrows():
                    if pd.notna(row.get("predicted_utilization_next_hour")):
                        query = text("""
                            UPDATE hourly_summaries 
                            SET 
                                predicted_utilization_next_hour = :prediction,
                                prediction_confidence = :confidence,
                                updated_at = CURRENT_TIMESTAMP
                            WHERE id = :record_id
                        """)

                        conn.execute(
                            query,
                            {
                                "prediction": float(
                                    row["predicted_utilization_next_hour"]
                                ),
                                "confidence": float(
                                    row.get("prediction_confidence", 0.0)
                                ),
                                "record_id": row["id"],
                            },
                        )

                conn.commit()

            logger.info(f"Updated predictions for {len(df)} records")

        except Exception as e:
            logger.error(f"Error updating predictions: {e}")
            raise

    def write_station_information(self, df: DataFrame):
        """
        Write station information to database.

        Args:
            df: Spark DataFrame with station information
        """
        try:
            pandas_df = df.toPandas()

            if pandas_df.empty:
                return

            # Upsert station information
            pandas_df.to_sql(
                "station_information",
                self.engine,
                if_exists="replace",
                index=False,
                method="multi",
            )

            logger.info(f"Updated station information for {len(pandas_df)} stations")

        except Exception as e:
            logger.error(f"Error writing station information: {e}")
            raise

    def write_station_status_history(self, df: DataFrame):
        """
        Write station status history to database.

        Args:
            df: Spark DataFrame with station status data
        """
        try:
            pandas_df = df.toPandas()

            if pandas_df.empty:
                return

            pandas_df.to_sql(
                "station_status_history",
                self.engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=1000,
            )

            logger.info(f"Wrote {len(pandas_df)} station status records")

        except Exception as e:
            logger.error(f"Error writing station status history: {e}")
            raise

    def write_weather_history(self, df: DataFrame):
        """
        Write weather history to database.

        Args:
            df: Spark DataFrame with weather data
        """
        try:
            pandas_df = df.toPandas()

            if pandas_df.empty:
                return

            pandas_df.to_sql(
                "weather_history",
                self.engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=1000,
            )

            logger.info(f"Wrote {len(pandas_df)} weather records")

        except Exception as e:
            logger.error(f"Error writing weather history: {e}")
            raise

    def close(self):
        """Close database connection."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")
