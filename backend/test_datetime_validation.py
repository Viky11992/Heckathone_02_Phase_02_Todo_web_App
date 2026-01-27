"""
Test script to verify that the datetime validation is working properly.
This tests that both date strings like "2026-01-29" and datetime strings are handled correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schemas.task import TaskCreate, TaskUpdate
from datetime import datetime

def test_datetime_validation():
    """Test the datetime validation in the schemas."""

    print("Testing datetime validation in Task schemas...")

    # Test 1: Date string "2026-01-29" should work (the problematic case)
    print("\n1. Testing TaskCreate with date-only string '2026-01-29'...")
    try:
        task1 = TaskCreate(
            title="Test task",
            description="Test with date-only string",
            priority="medium",
            category="test",
            due_date="2026-01-29"  # This was causing the 422 error
        )
        print(f"   Success: Created task with due_date={task1.due_date}")
        print(f"   Type: {type(task1.due_date)}")
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

    # Test 2: Full datetime string should work
    print("\n2. Testing TaskCreate with full datetime string...")
    try:
        task2 = TaskCreate(
            title="Test task",
            description="Test with full datetime",
            priority="high",
            category="test",
            due_date="2026-01-29T10:30:00"
        )
        print(f"   Success: Created task with due_date={task2.due_date}")
        print(f"   Type: {type(task2.due_date)}")
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

    # Test 3: None value should work
    print("\n3. Testing TaskCreate with None due_date...")
    try:
        task3 = TaskCreate(
            title="Test task",
            description="Test with None due_date",
            priority="low",
            category="test",
            due_date=None
        )
        print(f"   Success: Created task with due_date={task3.due_date}")
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

    # Test 4: Empty string should work (convert to None)
    print("\n4. Testing TaskCreate with empty string due_date...")
    try:
        task4 = TaskCreate(
            title="Test task",
            description="Test with empty string due_date",
            priority="low",
            category="test",
            due_date=""
        )
        print(f"   Success: Created task with due_date={task4.due_date}")
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

    # Test 5: Test TaskUpdate with date string (this was the missing piece)
    print("\n5. Testing TaskUpdate with date-only string '2026-01-29'...")
    try:
        task_update = TaskUpdate(
            due_date="2026-01-29",  # This was causing issues before
            title="Updated title"
        )
        print(f"   Success: Updated task with due_date={task_update.due_date}")
        print(f"   Type: {type(task_update.due_date)}")
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

    # Test 6: Test TaskUpdate with full datetime
    print("\n6. Testing TaskUpdate with full datetime string...")
    try:
        task_update2 = TaskUpdate(
            due_date="2026-01-29T15:30:00",
            priority="high"
        )
        print(f"   Success: Updated task with due_date={task_update2.due_date}")
        print(f"   Type: {type(task_update2.due_date)}")
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

    print("\n[SUCCESS] All datetime validation tests passed!")
    print("The Pydantic schemas are correctly handling:")
    print("- Date-only strings (YYYY-MM-DD) like '2026-01-29'")
    print("- Full datetime strings (YYYY-MM-DDTHH:MM:SS)")
    print("- None values")
    print("- Empty string values (converted to None)")
    print("\nThe 422 error should now be fixed!")

    return True

if __name__ == "__main__":
    print("="*60)
    print("Datetime Validation Fix Verification")
    print("="*60)

    success = test_datetime_validation()

    if success:
        print("\n[SUCCESS] Datetime validation fix verified!")
        sys.exit(0)
    else:
        print("\n[FAILURE] Datetime validation fix verification failed!")
        sys.exit(1)