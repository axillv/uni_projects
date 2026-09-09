# Decentralized Data Engineering Project

## Project Overview

This project is a decentralized data engineering system designed to process and analyze bike-sharing data using a **standard Spark architecture** with a driver-only client approach. The system integrates PostgreSQL, Kafka, Spark Master/Workers, and custom producers to handle real-time data ingestion, processing, and analytics.

## Architecture

The system follows the **standard Spark approach** where:

- **Spark Master**: Manages the cluster and distributes tasks
- **Spark Workers**: Execute tasks assigned by the master
- **Spark Driver**: The main application that acts as the client, communicating directly with the Spark Master to schedule and coordinate analytics tasks

This simplified architecture eliminates the need for separate task orchestrators and workers, making the system more maintainable and following Spark best practices.

### Components

- **PostgreSQL**: Data storage with pgAdmin for management
- **Kafka**: Message streaming with Kafka UI for monitoring
- **Spark Cluster**: Master + Workers for distributed processing
- **Spark Driver**: Main analytics application with integrated orchestration
- **Data Producers**: GBFS and Weather data producers

## Prerequisites

- Docker and Docker Compose installed on your system
- Basic understanding of Docker and data engineering concepts
- UV package manager for creating the specific requirements.txt file for all containers (else they need to be created manually)

## Setup Instructions

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Build and start the services using Docker Compose:

   ```bash
   docker-compose up --build
   ```

4. Wait for all services to initialize. Ensure no errors are reported in the logs.

## Usage

### Starting the System

The system can be started in different modes using the main script:

```bash
# Start all services
python main.py all

# Start only data producers
python main.py producers

# Start only analytics processing
python main.py analytics

# Stop all services
python main.py stop
```

### Manual ML Training

ML model training and inference is **manual only** and does not run on any automatic schedule. This gives you full control over when ML operations occur.

To run ML training:

1. **Ensure the analytics service is running**:

   ```bash
   python main.py analytics
   ```

2. **Run ML training manually**:

   ```bash
   python main.py ml-train
   ```

The ML training will:

- Use historical data from the database (last 7 days)
- Train a RandomForest regression model
- Generate predictions for recent data (last 24 hours)
- Update the database with predictions and confidence scores

#### ML Model Architecture

The system implements a **RandomForest regression model** for predicting bike station utilization. Here's how it's structured:

**Model Class**: `BikeUsagePredictionModel` (in `spark/ml_model.py`)

**Algorithm**: RandomForest Regressor with the following hyperparameters:

- `n_estimators=100` (number of trees)
- `max_depth=10` (maximum tree depth)
- `min_samples_split=5` (minimum samples to split)
- `min_samples_leaf=2` (minimum samples per leaf)
- `random_state=42` (for reproducibility)

**Target Variable**: `average_docking_station_utilisation` (station utilization rate)

#### Feature Engineering

The model uses **10 engineered features** derived from weather and station data:

1. **Weather Features**:
   - `temperature` (°C)
   - `wind_speed` (m/s)
   - `cloudiness` (%)
   - `precipitation_numeric` (0/1 boolean converted to numeric)

2. **Time-based Features**:
   - `hour_of_day` (0-23)
   - `day_of_week` (0-6, Monday=0)

3. **Station Features**:
   - `total_stations` (number of stations in the system)

4. **Temporal Lag Features** (for capturing patterns):
   - `avg_utilization_lag1` (utilization 1 hour ago)
   - `avg_utilization_lag2` (utilization 2 hours ago)
   - `avg_utilization_lag3` (utilization 3 hours ago)

#### Data Preprocessing

**Feature Scaling**: StandardScaler normalizes all features to zero mean and unit variance

**Missing Value Handling**:

- Numeric features: Filled with median values
- Categorical features: Filled with default values
- Lag features: Filled with 0.5 (neutral utilization)

**Data Validation**:

- Minimum 100 records required for training
- At least 50 valid records after cleaning
- Target variable must be present and non-null

#### Training Process

1. **Data Retrieval**: Fetches last 7 days of historical data from `hourly_summaries` table
2. **Feature Preparation**: Applies all preprocessing and feature engineering
3. **Train/Test Split**: 80/20 split with `random_state=42`
4. **Model Training**: Fits RandomForest on scaled training data
5. **Model Persistence**: Saves trained model and scaler to `/tmp/bike_utilization_model/`
6. **Batch Prediction**: Generates predictions for last 24 hours of data
7. **Database Update**: Stores predictions with confidence scores

#### Model Evaluation

**Metrics Calculated**:

- **RMSE** (Root Mean Square Error)
- **MAE** (Mean Absolute Error)
- **R² Score** (coefficient of determination)

**Prediction Confidence**: Calculated using ensemble variance:

- Higher tree prediction variance = lower confidence
- Confidence = exp(-prediction_std) (exponential decay)

#### Prediction Output

The model adds two columns to the database:

- `predicted_utilization_next_hour`: Predicted utilization rate (0.0-1.0)
- `prediction_confidence`: Confidence score (0.0-1.0)

#### Model Persistence

**Storage Location**: `/tmp/bike_utilization_model/`

- `model.pkl`: Trained RandomForest model
- `scaler.pkl`: Feature scaler

**Automatic Loading**: Model loads from disk on prediction requests if not in memory

#### Usage in Production

```python
# In BikeAnalyticsProcessor
processor = BikeAnalyticsProcessor()
processor.run_ml_training()  # Manual trigger only
```

The model integrates with Spark DataFrames for distributed prediction on large datasets.

### Database Inspection

The system provides several commands to inspect the database and view processing results:

```bash
# Show database status and table overview
python main.py db-status

# List all tables with record counts and column information
python main.py db-tables

# Show latest 10 records from hourly_summaries table (default)
python main.py db-latest

# Show latest 5 records from a specific table
python main.py db-latest --table station_information --limit 5

# Show ML training results and prediction statistics
python main.py ml-results
```

**Database Inspection Features:**

- **`db-status`**: Shows record counts for all main tables, latest data activity timestamp
- **`db-tables`**: Lists all database tables with record counts and column information  
- **`db-latest`**: Displays recent records from any table with customizable limits
- **`ml-results`**: Shows ML model performance metrics, prediction coverage, and recent predictions with confidence scores

### Data Processing Schedule

The system automatically:

- **Every 5 minutes**: Processes latest Kafka messages
- **Every hour (at :05)**: Generates hourly summaries with all required analytics fields:
  - `timestamp`, `city_name`, `temperature`, `wind_speed`, `precipitation`, `cloudiness`
  - `average_docking_station_utilisation`, `max_docking_station_utilisation`
  - `min_docking_station_utilisation`, `std_dev_docking_station_utilisation`

### Configuration

The system behavior can be controlled via environment variables:

- `HOURLY_SUMMARIES_ENABLED=true` (default): Enable/disable hourly summary generation
- `ML_TRAINING_ENABLED=false` (default): This is always false - ML training is manual only
- `SPARK_PROCESSING_MODE=streaming`: Set to "streaming", "batch", or "hourly"

### Database Schema

The system creates the following main tables:

- `hourly_summaries`: Contains all hourly analytics data
- `station_information`: GBFS station details
- `station_status_history`: Historical station status data
- `weather_history`: Weather data history

## Service URLs

- **PostgreSQL (pgAdmin)**: [http://localhost:5050](http://localhost:5050)
  - Default credentials: `admin@admin.com` / `admin`
- **Kafka UI**: [http://localhost:8080](http://localhost:8080)
- **Spark Master UI**: [http://localhost:8081](http://localhost:8081)
