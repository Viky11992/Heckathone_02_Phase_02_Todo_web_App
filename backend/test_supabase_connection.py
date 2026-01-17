#!/usr/bin/env python3
"""
Script to test the Supabase database connection
"""

import asyncio
import urllib.parse
from sqlmodel import create_engine, text
from config import settings

def test_sync_connection():
    """Test synchronous database connection"""
    print("Testing database connection...")
    print(f"Database URL: {settings.database_url}")

    try:
        # Create engine
        engine = create_engine(settings.database_url, echo=True, pool_pre_ping=True)

        # Test the connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"SUCCESS: Connected to database!")
            print(f"Database version: {version}")

            # Additional test - check if we can access the postgres database
            result = connection.execute(text("SELECT current_database();"))
            db_name = result.scalar()
            print(f"Connected to database: {db_name}")

        return True
    except Exception as e:
        print(f"ERROR: Failed to connect to database: {str(e)}")
        return False

async def test_async_connection():
    """Test asynchronous database connection"""
    print("\nTesting async database connection...")

    try:
        from sqlalchemy.ext.asyncio import create_async_engine

        # Create async engine - properly encode URL for asyncpg
        encoded_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

        # If the password contains special characters, we may need to encode it
        if "[15bNZjpIUGeinvps]" in encoded_url:
            # Replace the bracketed password with properly URL-encoded version
            encoded_url = encoded_url.replace("[15bNZjpIUGeinvps]", "15bNZjpIUGeinvps")

        async_engine = create_async_engine(encoded_url)

        async with async_engine.connect() as connection:
            result = await connection.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"SUCCESS: Connected to database asynchronously!")
            print(f"Database version: {version}")

        return True
    except Exception as e:
        print(f"ERROR: Failed to connect to database asynchronously: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Supabase Database Connection Test")
    print("=" * 50)

    # Test sync connection
    sync_success = test_sync_connection()

    # Test async connection if asyncpg is available
    try:
        import asyncpg
        async_success = asyncio.run(test_async_connection())
    except ImportError:
        print("\nNote: asyncpg not installed, skipping async test")
        async_success = True  # Consider this fine since sync worked

    print("\n" + "=" * 50)
    if sync_success:
        print("Database connection test PASSED!")
        print("Supabase integration is configured correctly")
    else:
        print("Database connection test FAILED!")
        print("Check your Supabase credentials and network connectivity")
    print("=" * 50)