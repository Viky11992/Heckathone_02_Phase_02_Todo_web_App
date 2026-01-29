#!/usr/bin/env python3
"""
Migration script to fix potential database schema issues after adding User model
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

def check_database_schema():
    """Check the current database schema."""
    from config import settings

    engine = create_engine(settings.database_url, echo=True)

    # Check existing tables
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    logger.info(f"Existing tables: {tables}")

    # Look for potential duplicate tables
    user_tables = [table for table in tables if 'user' in table.lower()]
    logger.info(f"User-related tables: {user_tables}")

    return tables, engine

def fix_duplicate_user_tables():
    """Fix potential duplicate user tables."""
    from config import settings

    engine = create_engine(settings.database_url, echo=True)

    # Get current tables
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    # Find user-related tables
    user_tables = [table for table in tables if table.lower() in ['user', 'users']]

    if len(user_tables) > 1:
        logger.warning(f"Found multiple user tables: {user_tables}")

        # Check which table has the correct structure
        for table_name in user_tables:
            columns = inspector.get_columns(table_name)
            column_names = [col['name'] for col in columns]

            # Check if this is the correct User table (has expected columns)
            expected_columns = {'id', 'email', 'name', 'created_at', 'updated_at'}
            if expected_columns.issubset(set(column_names)):
                logger.info(f"Table '{table_name}' has correct User structure")

                # If 'user' exists but not 'users', consider renaming or keeping the correct one
                if table_name == 'user':
                    # This is the correct table name based on the model definition
                    logger.info("Keeping 'user' table as correct")
                elif table_name == 'users':
                    # This might be from a different definition
                    logger.info("Found 'users' table")
            else:
                logger.info(f"Table '{table_name}' has columns: {column_names}")
    else:
        logger.info("Single user table found, no conflict detected")

def recreate_user_table():
    """Recreate the user table with correct schema."""
    from config import settings

    engine = create_engine(settings.database_url, echo=True)

    # Drop and recreate only the user table
    with engine.connect() as conn:
        # Check if user table exists
        inspector = inspect(conn)
        tables = inspector.get_table_names()

        if 'user' in tables:
            logger.info("Dropping existing user table...")
            conn.execute(text("DROP TABLE IF EXISTS user CASCADE"))
            conn.commit()

        # Recreate the table
        logger.info("Recreating user table...")
        from models import User
        User.__table__.create(bind=conn)
        conn.commit()

    logger.info("User table recreated successfully")

if __name__ == "__main__":
    logger.info("Checking database schema...")
    tables, engine = check_database_schema()

    logger.info("\nChecking for potential issues...")
    fix_duplicate_user_tables()

    # If needed, recreate the user table
    user_tables = [table for table in tables if 'user' in table.lower()]
    if 'user' not in user_tables:
        logger.info("\nCreating user table...")
        from models import User, Task
        with engine.begin() as conn:
            User.__table__.create(bind=conn)

    logger.info("\nDatabase schema check completed!")