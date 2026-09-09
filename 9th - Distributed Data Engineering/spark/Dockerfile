FROM apache/spark:3.5.0

USER root

# Install Python pip and required packages
RUN apt-get update && \
    apt-get install -y python3-pip curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create symlink for python command to point to python3
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Install Python packages
COPY spark/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Download Kafka connector JAR for Spark
RUN curl -L -o /opt/spark/jars/spark-sql-kafka-0-10_2.12-3.5.0.jar \
    https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.0/spark-sql-kafka-0-10_2.12-3.5.0.jar

# Download Kafka clients JAR (dependency for Kafka connector)
RUN curl -L -o /opt/spark/jars/kafka-clients-3.5.0.jar \
    https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.5.0/kafka-clients-3.5.0.jar

# Download PostgreSQL JDBC driver
RUN curl -L -o /opt/spark/jars/postgresql-42.7.1.jar \
    https://jdbc.postgresql.org/download/postgresql-42.7.1.jar

# Copy source code and configuration
COPY config/ /opt/spark/config/
COPY spark/ /opt/spark/work-dir/

# Set working directory
WORKDIR /opt/spark/work-dir

# Set PYTHONPATH to include config
ENV PYTHONPATH="${PYTHONPATH}:/opt/spark/config:/opt/spark/work-dir"

# Default command
CMD ["python3", "bike_analytics_processor.py"]