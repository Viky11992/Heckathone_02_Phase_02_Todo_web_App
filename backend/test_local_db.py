#!/usr/bin/env python3
"""
Script to test with a local SQLite database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Override the database URL to use local SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./todo_app_local_test.db'

from sqlmodel import SQLModel, create_engine
from database import get_session
from config import settings
import models
from datetime import datetime
from schemas.task import TaskCreate
from services.task_service import TaskService
from sqlmodel import Session

def test_local_database():
    """Test creating and using a local SQLite database."""

    print("Testing with local SQLite database...")

    # Recreate engine with the new database URL
    engine = create_engine(settings.database_url, echo=settings.db_echo)

    # Create all tables
    print("Creating tables in local database...")
    SQLModel.metadata.create_all(bind=engine)

    # Verify tables were created
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in local database: {tables}")

    if 'task' in tables:
        print("✅ Task table exists in local database!")
    else:
        print("❌ Task table does not exist in local database!")
        return False

    # Create a session and test operations
    with Session(engine) as session:
        print("\nTesting task operations with local database...")

        # Create test task data
        task_data = TaskCreate(
            title="Local Test Task",
            description="This is a test task created in local SQLite database",
            priority="medium",
            category="work",
            due_date=datetime(2026, 12, 31)
        )

        try:
            # Create the task using the service
            created_task = TaskService.create_task(
                session=session,
                user_id="local@test.com",
                task_data=task_data
            )

            print(f"✅ Successfully created task with ID: {created_task.id}")
            print(f"   Title: {created_task.title}")
            print(f"   User ID: {created_task.user_id}")
            print(f"   Priority: {created_task.priority}")
            print(f"   Due Date: {created_task.due_date}")

            # Test retrieving the task
            print(f"\nRetrieving task with ID {created_task.id}...")
            retrieved_task = TaskService.get_task_by_id(
                session=session,
                task_id=created_task.id,
                user_id="local@test.com"
            )

            if retrieved_task:
                print(f"✅ Successfully retrieved task: {retrieved_task.title}")
            else:
                print("❌ Failed to retrieve task")

            # Test listing tasks for user
            print(f"\nListing tasks for user 'local@test.com'...")
            user_tasks = TaskService.get_tasks_for_user(
                session=session,
                user_id="local@test.com"
            )

            print(f"✅ Found {len(user_tasks)} tasks for user")
            for task in user_tasks:
                print(f"   - Task ID {task.id}: {task.title}")

            print(f"\n✅ Local database test completed successfully!")
            return True

        except Exception as e:
            print(f"❌ Error during local database operations: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    print("="*60)
    print("Local Database Test")
    print("="*60)

    success = test_local_database()

    if success:
        print("\n🎉 Local database test passed!")
        print("The application can work with a local SQLite database!")
    else:
        print("\n💥 Local database test failed!")

    print("="*60)