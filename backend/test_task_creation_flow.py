"""
Test script to verify the complete task creation flow including
frontend-style data submission and backend validation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schemas.task import TaskCreate, TaskUpdate
from datetime import datetime

def test_task_creation_flow():
    """Test the task creation flow with realistic frontend data."""

    print("Testing task creation flow with frontend-style data...")

    # Simulate data that would come from the frontend form
    print("\n1. Testing TaskCreate with frontend-style data (date string)...")
    try:
        # This simulates what comes from the frontend date picker: "YYYY-MM-DD"
        task_data = {
            "title": "Test task from frontend",
            "description": "Task created from the frontend form",
            "priority": "medium",
            "category": "work",
            "due_date": "2026-01-29"  # Date string from HTML date input
        }

        task = TaskCreate(**task_data)
        print(f"   Success: Created task with due_date={task.due_date}")
        print(f"   Type: {type(task.due_date)}")
        print(f"   Value: {repr(task.due_date)}")
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

    # Test with datetime string (what might come from API)
    print("\n2. Testing TaskCreate with datetime string...")
    try:
        task_data = {
            "title": "Test task with datetime",
            "description": "Task with full datetime",
            "priority": "high",
            "category": "personal",
            "due_date": "2026-01-29T14:30:00"  # Full datetime
        }

        task = TaskCreate(**task_data)
        print(f"   Success: Created task with due_date={task.due_date}")
        print(f"   Type: {type(task.due_date)}")
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

    # Test with null due_date
    print("\n3. Testing TaskCreate with null due_date...")
    try:
        task_data = {
            "title": "Test task without due date",
            "description": "Task without due date",
            "priority": "low",
            "category": "other",
            "due_date": None
        }

        task = TaskCreate(**task_data)
        print(f"   Success: Created task with due_date={task.due_date}")
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

    # Test with empty string (common from forms)
    print("\n4. Testing TaskCreate with empty due_date string...")
    try:
        task_data = {
            "title": "Test task with empty due date",
            "description": "Task with empty due date string",
            "priority": "medium",
            "category": "health",
            "due_date": ""  # Empty string from form
        }

        task = TaskCreate(**task_data)
        print(f"   Success: Created task with due_date={task.due_date}")
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

    # Test TaskUpdate with date string
    print("\n5. Testing TaskUpdate with date string...")
    try:
        update_data = {
            "due_date": "2026-02-15",  # Date string for update
            "priority": "high"
        }

        task_update = TaskUpdate(**update_data)
        print(f"   Success: Updated task with due_date={task_update.due_date}")
        print(f"   Type: {type(task_update.due_date)}")
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

    # Test the exact scenario from the error: date-only string
    print("\n6. Testing the exact error scenario: '2026-01-29'...")
    try:
        # This is exactly the format that was causing the 422 error
        task_data = {
            "title": "Critical test task",
            "description": "Testing the exact scenario that was failing",
            "priority": "urgent",
            "category": "work",
            "due_date": "2026-01-29"  # The problematic date-only string
        }

        task = TaskCreate(**task_data)
        print(f"   SUCCESS: The exact scenario that was failing now works!")
        print(f"   Created task with due_date={task.due_date}")
        print(f"   Type: {type(task.due_date)}")
        print(f"   This confirms the 422 error is FIXED!")
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

    print("\n[SUCCESS] All task creation flow tests passed!")
    print("The frontend-to-backend data flow is working correctly for:")
    print("- Date-only strings from HTML date inputs")
    print("- Full datetime strings")
    print("- Null/empty values")
    print("- Task creation and update operations")
    print("\nThe 422 error should now be completely resolved!")

    return True

if __name__ == "__main__":
    print("="*60)
    print("Task Creation Flow Verification")
    print("="*60)

    success = test_task_creation_flow()

    if success:
        print("\n[SUCCESS] Task creation flow verification passed!")
        sys.exit(0)
    else:
        print("\n[FAILURE] Task creation flow verification failed!")
        sys.exit(1)