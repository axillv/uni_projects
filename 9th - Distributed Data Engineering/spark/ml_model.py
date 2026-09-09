"""
Machine Learning Model for Bike Usage Prediction.

This module implements a RandomForest regression model for predicting bike usage.
"""

import logging
import os
from typing import Optional

import joblib
import numpy as np
import pandas as pd
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, lit
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


class BikeUsagePredictionModel:
    """Machine learning model for bike usage prediction."""

    def __init__(self, spark: SparkSession, config):
        """
        Initialize the ML model.

        Args:
            spark: Spark session
            config: Configuration object
        """
        self.spark = spark
        self.config = config
        self.model = None
        self.scaler = None
        self.model_path = "/tmp/bike_utilization_model"
        self.feature_columns = [
            "temperature",
            "wind_speed",
            "cloudiness",
            "precipitation_numeric",
            "hour_of_day",
            "day_of_week",
            "total_stations",
            "avg_utilization_lag1",
            "avg_utilization_lag2",
            "avg_utilization_lag3",
        ]
        self._create_model_directory()

    def _create_model_directory(self):
        """Create model directory if it doesn't exist."""
        os.makedirs(self.model_path, exist_ok=True)

    def _prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for ML model.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with prepared features
        """
        # Create a copy to avoid modifying original
        df_features = df.copy()

        # Convert timestamp to datetime if it's not already
        if "timestamp" in df_features.columns:
            df_features["timestamp"] = pd.to_datetime(df_features["timestamp"])

            # Extract time-based features
            df_features["hour_of_day"] = df_features["timestamp"].dt.hour
            df_features["day_of_week"] = df_features["timestamp"].dt.dayofweek
        else:
            # Default values if timestamp is missing
            df_features["hour_of_day"] = 12
            df_features["day_of_week"] = 1

        # Convert boolean precipitation to numeric
        if "precipitation" in df_features.columns:
            df_features["precipitation_numeric"] = df_features["precipitation"].astype(
                int
            )
        else:
            df_features["precipitation_numeric"] = 0

        # Create lag features for utilization
        df_features = (
            df_features.sort_values("timestamp")
            if "timestamp" in df_features.columns
            else df_features
        )

        if "average_docking_station_utilisation" in df_features.columns:
            df_features["avg_utilization_lag1"] = df_features[
                "average_docking_station_utilisation"
            ].shift(1)
            df_features["avg_utilization_lag2"] = df_features[
                "average_docking_station_utilisation"
            ].shift(2)
            df_features["avg_utilization_lag3"] = df_features[
                "average_docking_station_utilisation"
            ].shift(3)
        else:
            df_features["avg_utilization_lag1"] = 0.5
            df_features["avg_utilization_lag2"] = 0.5
            df_features["avg_utilization_lag3"] = 0.5

        # Fill missing values
        for col_name in self.feature_columns:
            if col_name in df_features.columns:
                if df_features[col_name].dtype in ["float64", "int64"]:
                    df_features[col_name] = df_features[col_name].fillna(
                        df_features[col_name].median()
                    )
                else:
                    df_features[col_name] = df_features[col_name].fillna(0)
            else:
                # Add missing columns with default values
                if "temperature" in col_name:
                    df_features[col_name] = 15.0
                elif "wind_speed" in col_name:
                    df_features[col_name] = 5.0
                elif "cloudiness" in col_name:
                    df_features[col_name] = 50
                elif "total_stations" in col_name:
                    df_features[col_name] = 100
                else:
                    df_features[col_name] = 0.5

        return df_features

    def train_model(self, df: pd.DataFrame) -> bool:
        """
        Train the ML model.

        Args:
            df: Training data DataFrame

        Returns:
            True if training successful, False otherwise
        """
        try:
            logger.info("Starting ML model training...")

            if df.empty or len(df) < 100:
                logger.warning("Insufficient data for model training")
                return False

            # Prepare features
            df_features = self._prepare_features(df)

            # Remove rows with missing target variable
            df_features = df_features.dropna(
                subset=["average_docking_station_utilisation"]
            )

            if len(df_features) < 50:
                logger.warning("Insufficient valid data after cleaning")
                return False

            # Prepare feature matrix and target
            X = df_features[self.feature_columns].values
            y = df_features["average_docking_station_utilisation"].values

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)

            # Train RandomForest model
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1,
            )

            self.model.fit(X_train_scaled, y_train)

            # Evaluate model
            y_pred = self.model.predict(X_test_scaled)

            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            logger.info(
                f"Model training completed - RMSE: {rmse:.4f}, MAE: {mae:.4f}, R2: {r2:.4f}"
            )

            # Save model
            self._save_model()

            return True

        except Exception as e:
            logger.error(f"Error in model training: {e}")
            return False

    def _save_model(self):
        """Save trained model and scaler to disk."""
        try:
            if self.model is not None:
                joblib.dump(self.model, os.path.join(self.model_path, "model.pkl"))
            if self.scaler is not None:
                joblib.dump(self.scaler, os.path.join(self.model_path, "scaler.pkl"))
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Error saving model: {e}")

    def _load_model(self) -> bool:
        """
        Load trained model and scaler from disk.

        Returns:
            True if loading successful, False otherwise
        """
        try:
            model_file = os.path.join(self.model_path, "model.pkl")
            scaler_file = os.path.join(self.model_path, "scaler.pkl")

            if os.path.exists(model_file) and os.path.exists(scaler_file):
                self.model = joblib.load(model_file)
                self.scaler = joblib.load(scaler_file)
                logger.info("Model loaded successfully")
                return True
            else:
                logger.warning("Model files not found")
                return False

        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False

    def is_model_trained(self) -> bool:
        """
        Check if model is trained and ready for predictions.

        Returns:
            True if model is ready, False otherwise
        """
        if self.model is None or self.scaler is None:
            return self._load_model()
        return True

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Make predictions on input data.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with predictions added
        """
        try:
            if not self.is_model_trained():
                logger.warning("Model not trained, cannot make predictions")
                df["predicted_utilization_next_hour"] = None
                df["prediction_confidence"] = None
                return df

            # Prepare features
            df_features = self._prepare_features(df)

            # Make predictions
            X = df_features[self.feature_columns].values
            X_scaled = self.scaler.transform(X)

            predictions = self.model.predict(X_scaled)

            # Calculate confidence (simplified as inverse of prediction variance)
            if hasattr(self.model, "estimators_"):
                tree_predictions = np.array(
                    [tree.predict(X_scaled) for tree in self.model.estimators_]
                )
                prediction_std = np.std(tree_predictions, axis=0)
                confidence = np.exp(-prediction_std)  # Higher std = lower confidence
            else:
                confidence = np.full(len(predictions), 0.5)  # Default confidence

            # Add predictions to original DataFrame
            result_df = df.copy()
            result_df["predicted_utilization_next_hour"] = predictions
            result_df["prediction_confidence"] = confidence

            logger.info(f"Generated predictions for {len(result_df)} records")
            return result_df

        except Exception as e:
            logger.error(f"Error making predictions: {e}")
            df["predicted_utilization_next_hour"] = None
            df["prediction_confidence"] = None
            return df

    def add_predictions(self, df: DataFrame) -> DataFrame:
        """
        Add ML predictions to Spark DataFrame.

        Args:
            df: Input Spark DataFrame

        Returns:
            Spark DataFrame with predictions added
        """
        try:
            if not self.is_model_trained():
                logger.warning("Model not trained, adding null predictions")
                return df.withColumn(
                    "predicted_utilization_next_hour", lit(None)
                ).withColumn("prediction_confidence", lit(None))

            # Convert to Pandas for prediction
            pandas_df = df.toPandas()

            if pandas_df.empty:
                return df.withColumn(
                    "predicted_utilization_next_hour", lit(None)
                ).withColumn("prediction_confidence", lit(None))

            # Make predictions
            predicted_df = self.predict(pandas_df)

            # Convert back to Spark DataFrame
            spark_df = self.spark.createDataFrame(predicted_df)

            return spark_df

        except Exception as e:
            logger.error(f"Error adding predictions to Spark DataFrame: {e}")
            return df.withColumn(
                "predicted_utilization_next_hour", lit(None)
            ).withColumn("prediction_confidence", lit(None))
