-- Database initialization script for bike-sharing analytics system
-- Creates tables for storing processed analytics data and ML model results

-- Create database if it doesn't exist (handled by Docker environment variables)
-- CREATE DATABASE IF NOT EXISTS bike_analytics;

-- Use the database
-- \c bike_analytics;

-- Create extension for UUID generation if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create hourly_summaries table for aggregated analytics data
CREATE TABLE IF NOT EXISTS hourly_summaries (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    
    -- Weather data
    temperature DECIMAL(5,2),
    wind_speed DECIMAL(5,2),
    precipitation BOOLEAN DEFAULT FALSE,
    cloudiness INTEGER,
    
    -- Station utilization metrics
    average_docking_station_utilisation DECIMAL(5,4),
    max_docking_station_utilisation DECIMAL(5,4),
    min_docking_station_utilisation DECIMAL(5,4),
    std_dev_docking_station_utilisation DECIMAL(5,4),
    
    -- Additional metrics for analysis
    total_stations INTEGER,
    total_bikes_available INTEGER,
    total_docks_available INTEGER,
    
    -- ML prediction fields
    predicted_utilization_next_hour DECIMAL(5,4),
    prediction_confidence DECIMAL(5,4),
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_temperature CHECK (temperature BETWEEN -50 AND 60),
    CONSTRAINT valid_wind_speed CHECK (wind_speed >= 0),
    CONSTRAINT valid_cloudiness CHECK (cloudiness BETWEEN 0 AND 100),
    CONSTRAINT valid_utilization CHECK (
        average_docking_station_utilisation BETWEEN 0 AND 1 AND
        max_docking_station_utilisation BETWEEN 0 AND 1 AND
        min_docking_station_utilisation BETWEEN 0 AND 1 AND
        std_dev_docking_station_utilisation >= 0
    )
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_hourly_summaries_timestamp ON hourly_summaries(timestamp);
CREATE INDEX IF NOT EXISTS idx_hourly_summaries_city_timestamp ON hourly_summaries(city_name, timestamp);
CREATE INDEX IF NOT EXISTS idx_hourly_summaries_created_at ON hourly_summaries(created_at);

-- Create station_information table for static station data
CREATE TABLE IF NOT EXISTS station_information (
    station_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    short_name VARCHAR(100),
    lat DECIMAL(10,8),
    lon DECIMAL(11,8),
    capacity INTEGER,
    region_id INTEGER,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_coordinates CHECK (
        lat BETWEEN -90 AND 90 AND
        lon BETWEEN -180 AND 180
    ),
    CONSTRAINT valid_capacity CHECK (capacity >= 0)
);

-- Create index for spatial queries
CREATE INDEX IF NOT EXISTS idx_station_information_location ON station_information(lat, lon);

-- Create station_status_history table for detailed station status tracking
CREATE TABLE IF NOT EXISTS station_status_history (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    station_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Status data
    num_bikes_available INTEGER NOT NULL,
    num_docks_available INTEGER NOT NULL,
    is_installed BOOLEAN DEFAULT TRUE,
    is_renting BOOLEAN DEFAULT TRUE,
    is_returning BOOLEAN DEFAULT TRUE,
    last_reported TIMESTAMP WITH TIME ZONE,
    
    -- Calculated metrics
    utilization DECIMAL(5,4) GENERATED ALWAYS AS (
        CASE 
            WHEN (num_bikes_available + num_docks_available) > 0 
            THEN num_bikes_available::DECIMAL / (num_bikes_available + num_docks_available)
            ELSE 0
        END
    ) STORED,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_availability CHECK (
        num_bikes_available >= 0 AND
        num_docks_available >= 0
    )
);

-- Create indexes for station status history
CREATE INDEX IF NOT EXISTS idx_station_status_history_station_timestamp 
    ON station_status_history(station_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_station_status_history_timestamp 
    ON station_status_history(timestamp);
CREATE INDEX IF NOT EXISTS idx_station_status_history_utilization 
    ON station_status_history(utilization);

-- Create weather_history table for weather data tracking
CREATE TABLE IF NOT EXISTS weather_history (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Weather metrics
    temperature DECIMAL(5,2),
    feels_like DECIMAL(5,2),
    wind_speed DECIMAL(5,2),
    wind_deg INTEGER,
    humidity INTEGER,
    pressure INTEGER,
    visibility INTEGER,
    uv_index DECIMAL(3,1),
    cloudiness INTEGER,
    
    -- Weather conditions
    weather_main VARCHAR(50),
    weather_description VARCHAR(100),
    weather_id INTEGER,
    
    -- Precipitation
    rain_1h DECIMAL(5,2) DEFAULT 0,
    snow_1h DECIMAL(5,2) DEFAULT 0,
    precipitation BOOLEAN DEFAULT FALSE,
    
    -- Derived features
    is_sunny BOOLEAN DEFAULT FALSE,
    is_cloudy BOOLEAN DEFAULT FALSE,
    is_windy BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_weather_temperature CHECK (temperature BETWEEN -50 AND 60),
    CONSTRAINT valid_weather_humidity CHECK (humidity BETWEEN 0 AND 100),
    CONSTRAINT valid_weather_cloudiness CHECK (cloudiness BETWEEN 0 AND 100),
    CONSTRAINT valid_weather_wind_deg CHECK (wind_deg BETWEEN 0 AND 360)
);

-- Create indexes for weather history
CREATE INDEX IF NOT EXISTS idx_weather_history_city_timestamp 
    ON weather_history(city_name, timestamp);
CREATE INDEX IF NOT EXISTS idx_weather_history_timestamp 
    ON weather_history(timestamp);

-- Create ml_model_metadata table for tracking model versions and performance
CREATE TABLE IF NOT EXISTS ml_model_metadata (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    model_path TEXT,
    
    -- Performance metrics
    training_accuracy DECIMAL(5,4),
    validation_accuracy DECIMAL(5,4),
    test_accuracy DECIMAL(5,4),
    rmse DECIMAL(10,6),
    mae DECIMAL(10,6),
    
    -- Training metadata
    training_data_start TIMESTAMP WITH TIME ZONE,
    training_data_end TIMESTAMP WITH TIME ZONE,
    training_rows INTEGER,
    feature_count INTEGER,
    
    -- Model status
    is_active BOOLEAN DEFAULT FALSE,
    is_deployed BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deployed_at TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT unique_active_model EXCLUDE (model_name WITH =) WHERE (is_active = TRUE)
);

-- Create index for model metadata
CREATE INDEX IF NOT EXISTS idx_ml_model_metadata_name_version 
    ON ml_model_metadata(model_name, model_version);
CREATE INDEX IF NOT EXISTS idx_ml_model_metadata_active 
    ON ml_model_metadata(model_name) WHERE is_active = TRUE;

-- Create view for latest hourly summaries with enriched data
CREATE OR REPLACE VIEW latest_hourly_summaries AS
SELECT 
    hs.*,
    wh.weather_main,
    wh.weather_description,
    wh.humidity,
    wh.pressure,
    wh.uv_index,
    COUNT(si.station_id) as total_stations_in_city
FROM hourly_summaries hs
LEFT JOIN weather_history wh ON (
    hs.city_name = wh.city_name AND
    hs.timestamp >= wh.timestamp - INTERVAL '30 minutes' AND
    hs.timestamp <= wh.timestamp + INTERVAL '30 minutes'
)
LEFT JOIN station_information si ON TRUE
WHERE hs.timestamp >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
GROUP BY hs.id, wh.weather_main, wh.weather_description, wh.humidity, wh.pressure, wh.uv_index
ORDER BY hs.timestamp DESC;

-- Create materialized view for performance analytics
CREATE MATERIALIZED VIEW IF NOT EXISTS daily_performance_summary AS
SELECT 
    DATE(timestamp) as date,
    city_name,
    AVG(average_docking_station_utilisation) as avg_daily_utilization,
    MAX(max_docking_station_utilisation) as peak_utilization,
    MIN(min_docking_station_utilisation) as min_utilization,
    AVG(temperature) as avg_temperature,
    AVG(wind_speed) as avg_wind_speed,
    COUNT(*) as hourly_records,
    STDDEV(average_docking_station_utilisation) as utilization_volatility
FROM hourly_summaries
WHERE timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(timestamp), city_name
ORDER BY date DESC;

-- Create index for the materialized view
CREATE INDEX IF NOT EXISTS idx_daily_performance_summary_date 
    ON daily_performance_summary(date);

-- Grant permissions (adjust as needed for production)
-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO bike_analytics_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO bike_analytics_user;

-- Insert initial data or configuration if needed
INSERT INTO ml_model_metadata (
    model_name, 
    model_version, 
    model_path,
    is_active
) VALUES (
    'bike_utilization_predictor',
    'v1.0.0',
    '/tmp/bike_utilization_model',
    FALSE
) ON CONFLICT DO NOTHING;

-- Create function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_hourly_summaries_updated_at 
    BEFORE UPDATE ON hourly_summaries 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_station_information_updated_at 
    BEFORE UPDATE ON station_information 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add foreign key constraint to station_status_history
ALTER TABLE station_status_history 
ADD CONSTRAINT fk_station_status_station
FOREIGN KEY (station_id) 
REFERENCES station_information(station_id)
ON DELETE CASCADE;

-- Add foreign key constraint to weather_history
ALTER TABLE weather_history 
ADD CONSTRAINT fk_weather_city_name
FOREIGN KEY (city_name) 
REFERENCES cities(name)
ON DELETE CASCADE;
