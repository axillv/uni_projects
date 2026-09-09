#!/usr/bin/env python3
"""
Main entry point for the DDE project.

This script provides a command-line interface for various operations
including starting producers, running analytics, ML training, and database inspection.
"""

import argparse
import logging
import subprocess
import sys
from datetime import datetime

from config import get_config

# Try to import database connector, will be available when needed
try:
    from spark.database_connector import DatabaseConnector
except ImportError:
    DatabaseConnector = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_producers():
    """Start all producers using Docker Compose."""
    logger.info("Starting data producers...")
    subprocess.run(["docker-compose", "up", "-d", "gbfs_producer", "weather_producer"])


def run_analytics():
    """Start Spark analytics processing."""
    logger.info("Starting Spark analytics...")
    subprocess.run(["docker-compose", "up", "-d", "spark-driver"])


def run_ml_training():
    """Run ML model training in the Spark container."""
    logger.info("Running ML model training...")

    # First, check if the spark-driver container is running
    result = subprocess.run(
        ["docker", "ps", "--filter", "name=spark-driver", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
    )

    if "spark-driver" not in result.stdout:
        logger.error(
            "Spark driver container is not running. Please start it first with 'python main.py analytics'"
        )
        return False

    # Run ML training in the container
    cmd = [
        "docker",
        "exec",
        "spark-driver",
        "python3",
        "-c",
        """
from bike_analytics_processor import BikeAnalyticsProcessor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    logger.info('Initializing processor for ML training...')
    processor = BikeAnalyticsProcessor()
    logger.info('Running ML training...')
    processor.run_ml_training()
    logger.info('ML training completed successfully!')
except Exception as e:
    logger.error(f'ML training failed: {e}')
    raise
        """,
    ]

    result = subprocess.run(cmd)
    return result.returncode == 0


def stop_all():
    """Stop all services."""
    logger.info("Stopping all services...")
    subprocess.run(["docker-compose", "down"])


def get_database_connector():
    """Get a database connector instance."""
    try:
        if DatabaseConnector is None:
            from spark.database_connector import DatabaseConnector as DBConnector
        else:
            DBConnector = DatabaseConnector

        config = get_config()
        return DBConnector(config)
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return None


def db_status():
    """Show database status and table overview."""
    logger.info("Checking database status...")

    db = get_database_connector()
    if not db:
        return False

    try:
        # Get table counts
        tables = [
            "hourly_summaries",
            "station_information",
            "station_status_history",
            "weather_history",
        ]

        print("\n" + "=" * 60)
        print("DATABASE STATUS")
        print("=" * 60)

        for table in tables:
            try:
                query = f"SELECT COUNT(*) FROM {table}"
                with db.engine.connect() as conn:
                    result = conn.execute(db.engine.text(query))
                    count = result.scalar()
                    print(f"{table:25}: {count:,} records")
            except Exception as e:
                print(f"{table:25}: Error - {str(e)[:30]}...")

        # Get latest activity
        try:
            query = """
                SELECT MAX(timestamp) as latest_activity 
                FROM hourly_summaries
            """
            with db.engine.connect() as conn:
                result = conn.execute(db.engine.text(query))
                latest = result.scalar()
                if latest:
                    print(f"\nLatest Activity: {latest}")
                else:
                    print(f"\nLatest Activity: No data yet")
        except Exception:
            print(f"\nLatest Activity: Unable to retrieve")

        print("=" * 60)
        return True

    except Exception as e:
        logger.error(f"Error checking database status: {e}")
        return False
    finally:
        if db:
            db.close()


def db_tables():
    """List all tables with detailed information."""
    logger.info("Retrieving table information...")

    db = get_database_connector()
    if not db:
        return False

    try:
        query = """
            SELECT 
                table_name,
                (SELECT COUNT(*) 
                 FROM information_schema.columns 
                 WHERE table_name = t.table_name) as column_count
            FROM information_schema.tables t
            WHERE table_schema = 'public'
            ORDER BY table_name
        """

        with db.engine.connect() as conn:
            result = conn.execute(db.engine.text(query))
            tables = result.fetchall()

        print("\n" + "=" * 60)
        print("ALL TABLES")
        print("=" * 60)

        for table_name, column_count in tables:
            # Get record count
            try:
                count_query = f"SELECT COUNT(*) FROM {table_name}"
                with db.engine.connect() as conn:
                    count_result = conn.execute(db.engine.text(count_query))
                    record_count = count_result.scalar()

                print(
                    f"{table_name:25}: {record_count:,} records, {column_count} columns"
                )
            except Exception:
                print(f"{table_name:25}: Error accessing table")

        print("=" * 60)
        return True

    except Exception as e:
        logger.error(f"Error retrieving table information: {e}")
        return False
    finally:
        if db:
            db.close()


def db_latest(table_name="hourly_summaries", limit=10):
    """Show latest records from specified table."""
    logger.info(f"Retrieving latest {limit} records from {table_name}...")

    db = get_database_connector()
    if not db:
        return False

    try:
        # Check if table exists
        check_query = """
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_name = %s AND table_schema = 'public'
        """

        with db.engine.connect() as conn:
            result = conn.execute(db.engine.text(check_query), (table_name,))
            if result.scalar() == 0:
                print(f"Table '{table_name}' does not exist")
                return False

        # Get latest records
        if table_name == "hourly_summaries":
            query = f"""
                SELECT 
                    timestamp,
                    city_name,
                    temperature,
                    average_docking_station_utilisation,
                    total_stations
                FROM {table_name}
                ORDER BY timestamp DESC
                LIMIT %s
            """
        else:
            query = f"""
                SELECT * FROM {table_name}
                ORDER BY 
                    CASE 
                        WHEN EXISTS (SELECT 1 FROM information_schema.columns 
                                   WHERE table_name = '{table_name}' 
                                   AND column_name = 'timestamp') 
                        THEN timestamp 
                        ELSE NULL 
                    END DESC
                LIMIT %s
            """

        with db.engine.connect() as conn:
            result = conn.execute(db.engine.text(query), (limit,))
            records = result.fetchall()
            columns = result.keys()

        print(f"\n" + "=" * 80)
        print(f"LATEST {limit} RECORDS FROM {table_name.upper()}")
        print("=" * 80)

        if not records:
            print("No records found")
        else:
            # Print header
            header = " | ".join(f"{col:15}" for col in columns)
            print(header)
            print("-" * len(header))

            # Print records
            for record in records:
                row = " | ".join(f"{val!s:15}" for val in record)
                print(row)

        print("=" * 80)
        return True

    except Exception as e:
        logger.error(f"Error retrieving latest records: {e}")
        return False
    finally:
        if db:
            db.close()


def ml_results():
    """Show ML training results and prediction statistics."""
    logger.info("Retrieving ML results...")

    db = get_database_connector()
    if not db:
        return False

    try:
        print("\n" + "=" * 60)
        print("ML TRAINING RESULTS")
        print("=" * 60)

        # Check for predictions
        pred_query = """
            SELECT 
                COUNT(*) as total_predictions,
                COUNT(CASE WHEN predicted_utilization_next_hour IS NOT NULL 
                           THEN 1 END) as with_predictions,
                AVG(prediction_confidence) as avg_confidence,
                MAX(updated_at) as last_prediction_time
            FROM hourly_summaries
        """

        with db.engine.connect() as conn:
            result = conn.execute(db.engine.text(pred_query))
            stats = result.fetchone()

        total, with_pred, avg_conf, last_pred = stats

        print(f"Total Records: {total:,}")
        print(f"Records with Predictions: {with_pred:,}")
        print(
            f"Prediction Coverage: {(with_pred / total * 100):.1f}%"
            if total > 0
            else "Prediction Coverage: 0%"
        )
        print(
            f"Average Confidence: {avg_conf:.3f}"
            if avg_conf
            else "Average Confidence: N/A"
        )
        print(
            f"Last Prediction: {last_pred}" if last_pred else "Last Prediction: Never"
        )

        # Recent predictions
        recent_query = """
            SELECT 
                timestamp,
                average_docking_station_utilisation as actual,
                predicted_utilization_next_hour as predicted,
                prediction_confidence as confidence
            FROM hourly_summaries
            WHERE predicted_utilization_next_hour IS NOT NULL
            ORDER BY timestamp DESC
            LIMIT 5
        """

        with db.engine.connect() as conn:
            result = conn.execute(db.engine.text(recent_query))
            recent = result.fetchall()

        if recent:
            print(f"\nRECENT PREDICTIONS:")
            print(f"{'Timestamp':20} {'Actual':8} {'Predicted':8} {'Confidence':10}")
            print("-" * 55)
            for timestamp, actual, predicted, confidence in recent:
                print(
                    f"{str(timestamp)[:19]:20} "
                    f"{actual:8.3f} {predicted:8.3f} {confidence:10.3f}"
                )
        else:
            print(f"\nNo predictions found yet")

        print("=" * 60)
        return True

    except Exception as e:
        logger.error(f"Error retrieving ML results: {e}")
        return False
    finally:
        if db:
            db.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="DDE Project Management Script")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Service management commands
    subparsers.add_parser("producers", help="Start data producers")
    subparsers.add_parser("analytics", help="Start Spark analytics")
    subparsers.add_parser("ml-train", help="Run ML model training")
    subparsers.add_parser("stop", help="Stop all services")
    subparsers.add_parser("all", help="Start all services")

    # Database inspection commands
    subparsers.add_parser("db-status", help="Show database status and overview")
    subparsers.add_parser("db-tables", help="List all tables with information")

    latest_parser = subparsers.add_parser(
        "db-latest", help="Show latest records from table"
    )
    latest_parser.add_argument(
        "--table",
        default="hourly_summaries",
        help="Table name (default: hourly_summaries)",
    )
    latest_parser.add_argument(
        "--limit", type=int, default=10, help="Number of records to show (default: 10)"
    )

    subparsers.add_parser("ml-results", help="Show ML training results")

    args = parser.parse_args()

    if args.command == "producers":
        run_producers()
    elif args.command == "analytics":
        run_analytics()
    elif args.command == "ml-train":
        success = run_ml_training()
        if not success:
            sys.exit(1)
    elif args.command == "stop":
        stop_all()
    elif args.command == "all":
        logger.info("Starting all services...")
        subprocess.run(["docker-compose", "up", "-d"])
    elif args.command == "db-status":
        success = db_status()
        if not success:
            sys.exit(1)
    elif args.command == "db-tables":
        success = db_tables()
        if not success:
            sys.exit(1)
    elif args.command == "db-latest":
        success = db_latest(args.table, args.limit)
        if not success:
            sys.exit(1)
    elif args.command == "ml-results":
        success = ml_results()
        if not success:
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
