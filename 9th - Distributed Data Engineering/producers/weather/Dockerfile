# Use the official Python image as the base image
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY producers/weather/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file
COPY .env ./

# Copy the config directory to maintain local structure
COPY config/ ./config/

# Copy the base producer
COPY producers/base/ ./producers/base/

# Copy the specific producer directory
COPY producers/weather/ ./producers/weather/

# Create a custom __init__.py for this container
RUN echo "from .base.generic_api_producer import GenericAPIProducer" > ./producers/__init__.py && \
    echo "from .weather.weather_producer import WeatherProducer" >> ./producers/__init__.py && \
    echo "__all__ = ['GenericAPIProducer', 'WeatherProducer']" >> ./producers/__init__.py

# Set Python path to include the app directory
ENV PYTHONPATH=/app

# Define the entry point
CMD ["python", "producers/weather/weather_producer.py"]