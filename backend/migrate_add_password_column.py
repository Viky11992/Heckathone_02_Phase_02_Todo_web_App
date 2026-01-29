#!/usr/bin/env python3
"""
Migration script to add hashed_password column to user table if it doesn't exist
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import inspect, text
import models
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_and_update_schema():
    """Check the current database schema and add hashed_password column if needed."""
    from config import settings

    engine = create_engine(settings.database_url, echo=True)

    # Check existing columns in the user table
    inspector = inspect(engine)

    # Get all tables
    tables = inspector.get_table_names()
    logger.info(f"Existing tables: {tables}")

    # Check columns in user table
    if 'user' in tables:
        columns = inspector.get_columns('user')
        column_names = [col['name'] for col in columns]
        logger.info(f"Columns in 'user' table: {column_names}")

        # Check if hashed_password column exists
        if 'hashed_password' not in column_names:
            logger.info("Adding hashed_password column to user table...")

            with engine.connect() as conn:
                # Add the hashed_password column
                conn.execute(text("ALTER TABLE \"user\" ADD COLUMN hashed_password VARCHAR NOT NULL DEFAULT '';"))

                # Update existing users with a default password (temporary)
                # In a real scenario, you'd want to handle existing users differently
                conn.execute(text("""
                    UPDATE "user"
                    SET hashed_password = $2$12$12345678901234567890123456789012345678901234567890123
                    WHERE hashed_password = '' OR hashed_password IS NULL
                """))

                conn.commit()

            logger.info("hashed_password column added successfully!")
        else:
            logger.info("hashed_password column already exists.")
    else:
        logger.warning("user table not found!")

    # Also check if users table exists (might have been created previously)
    if 'users' in tables:
        columns = inspector.get_columns('users')
        column_names = [col['name'] for col in columns]
        logger.info(f"Columns in 'users' table: {column_names}")

def recreate_tables():
    """Optionally recreate tables if needed."""
    from config import settings

    engine = create_engine(settings.database_url, echo=True)

    # Create all tables (this will create the new structure)
    SQLModel.metadata.create_all(bind=engine)
    logger.info("Tables recreated with new schema.")

if __name__ == "__main__":
    logger.info("Checking and updating database schema...")
    check_and_update_schema()

    # Also run the standard table creation to ensure all tables are up to date
    recreate_tables()

    logger.info("Database schema update completed!")