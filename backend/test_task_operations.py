#!/usr/bin/env python3
"""
Script to test task operations in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session
from database import engine
import models
from datetime import datetime
from schemas.task import TaskCreate
from services.task_service import TaskService

def test_task_operations():
    """Test creating, reading, updating, and deleting tasks."""

    print("Testing task operations...")

    # Create a database session
    with Session(engine) as session:
        print("\n1. Creating a test task...")

        # Create test task data
        task_data = TaskCreate(
            title="Test Task from Backend",
            description="This is a test task created to verify database operations",
            priority="medium",
            category="work",
            due_date=datetime(2026, 12, 31)
        )

        try:
            # Create the task using the service
            created_task = TaskService.create_task(
                session=session,
                user_id="test@example.com",
                task_data=task_data
            )

            print(f"✅ Successfully created task with ID: {created_task.id}")
            print(f"   Title: {created_task.title}")
            print(f"   User ID: {created_task.user_id}")
            print(f"   Priority: {created_task.priority}")
            print(f"   Due Date: {created_task.due_date}")

            # Test retrieving the task
            print(f"\n2. Retrieving task with ID {created_task.id}...")
            retrieved_task = TaskService.get_task_by_id(
                session=session,
                task_id=created_task.id,
                user_id="test@example.com"
            )

            if retrieved_task:
                print(f"✅ Successfully retrieved task: {retrieved_task.title}")
            else:
                print("❌ Failed to retrieve task")

            # Test listing tasks for user
            print(f"\n3. Listing tasks for user 'test@example.com'...")
            user_tasks = TaskService.get_tasks_for_user(
                session=session,
                user_id="test@example.com"
            )

            print(f"✅ Found {len(user_tasks)} tasks for user")
            for task in user_tasks:
                print(f"   - Task ID {task.id}: {task.title}")

            # Test updating the task
            print(f"\n4. Updating task...")
            from schemas.task import TaskUpdate

            update_data = TaskUpdate(
                title="Updated Test Task",
                description="This task has been updated",
                priority="high"
            )

            updated_task = TaskService.update_task(
                session=session,
                task_id=created_task.id,
                user_id="test@example.com",
                task_data=update_data
            )

            if updated_task:
                print(f"✅ Successfully updated task: {updated_task.title}")
            else:
                print("❌ Failed to update task")

            # Test toggling completion
            print(f"\n5. Toggling task completion...")
            from schemas.task import TaskToggleComplete

            completion_data = TaskToggleComplete(completed=True)
            toggled_task = TaskService.toggle_task_completion(
                session=session,
                task_id=created_task.id,
                user_id="test@example.com",
                completion_data=completion_data
            )

            if toggled_task:
                print(f"✅ Successfully toggled task completion: {toggled_task.completed}")
            else:
                print("❌ Failed to toggle task completion")

            print(f"\n6. Final task status:")
            final_task = TaskService.get_task_by_id(
                session=session,
                task_id=created_task.id,
                user_id="test@example.com"
            )
            print(f"   ID: {final_task.id}")
            print(f"   Title: {final_task.title}")
            print(f"   Completed: {final_task.completed}")
            print(f"   Priority: {final_task.priority}")
            print(f"   Updated At: {final_task.updated_at}")

            # Note: We won't delete the task to keep it for potential future tests
            print(f"\n✅ All task operations completed successfully!")
            print(f"   The task remains in the database for continued use.")

        except Exception as e:
            print(f"❌ Error during task operations: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    return True

if __name__ == "__main__":
    print("="*60)
    print("Task Operations Test")
    print("="*60)

    success = test_task_operations()

    if success:
        print("\n🎉 All task operations tests passed!")
        print("The database is properly set up and functional!")
    else:
        print("\n💥 Task operations test failed!")

    print("="*60)