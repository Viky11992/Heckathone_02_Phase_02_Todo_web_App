#!/usr/bin/env python3
"""
Script to test the Neon database connection
"""

import asyncio
from sqlmodel import create_engine, text
from config import settings

def test_sync_connection():
    """Test synchronous database connection"""
    print("Testing Neon database connection...")
    print(f"Database URL: {settings.database_url}")

    try:
        # Create engine
        engine = create_engine(settings.database_url, echo=True, pool_pre_ping=True)

        # Test the connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"SUCCESS: Connected to Neon database!")
            print(f"Database version: {version}")

            # Additional test - check if we can access the database
            result = connection.execute(text("SELECT current_database();"))
            db_name = result.scalar()
            print(f"Connected to database: {db_name}")

            # Test user
            result = connection.execute(text("SELECT current_user;"))
            user = result.scalar()
            print(f"Connected as user: {user}")

        return True
    except Exception as e:
        print(f"ERROR: Failed to connect to Neon database: {str(e)}")
        return False

async def test_async_connection():
    """Test asynchronous database connection"""
    print("\nTesting async Neon database connection...")

    try:
        from sqlalchemy.ext.asyncio import create_async_engine

        # Create async engine - properly encode URL for asyncpg
        encoded_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

        async_engine = create_async_engine(encoded_url)

        async with async_engine.connect() as connection:
            result = await connection.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"SUCCESS: Connected to Neon database asynchronously!")
            print(f"Database version: {version}")

        return True
    except Exception as e:
        print(f"ERROR: Failed to connect to Neon database asynchronously: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Neon Database Connection Test")
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
        print("Neon database connection test PASSED!")
        print("Neon integration is configured correctly")
    else:
        print("Neon database connection test FAILED!")
        print("Check your Neon credentials and network connectivity")
    print("=" * 50)