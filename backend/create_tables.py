#!/usr/bin/env python3
"""
Script to manually create database tables in NeonDB
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import SQLModel
from database import engine
import models
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """Create all database tables."""
    logger.info("Starting database table creation...")

    try:
        # Import all models to ensure they're registered
        logger.info("Importing models...")

        # Create all tables
        logger.info("Creating tables in database...")
        SQLModel.metadata.create_all(bind=engine)

        logger.info("Tables created successfully!")

        # Verify tables were created by checking if we can access them
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        logger.info(f"Existing tables: {tables}")

        if 'task' in tables:
            logger.info("✅ Task table exists!")
        else:
            logger.warning("⚠️  Task table does not exist!")

        return True

    except Exception as e:
        logger.error(f"❌ Error creating tables: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_tables()
    if success:
        print("\nSUCCESS: Database tables created successfully!")
        sys.exit(0)
    else:
        print("\nFAILED: Failed to create database tables!")
        sys.exit(1)