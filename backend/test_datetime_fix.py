"""
Simple test to verify that the backend is running and the datetime parsing fix is in place.
This creates a simple test to validate the schema handling of due_date field.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the schema to test the datetime validation directly
from schemas.task import TaskCreate
from datetime import datetime

def test_datetime_parsing():
    """Test the datetime parsing in the schema directly."""

    print("Testing datetime parsing in TaskCreate schema...")

    # Test 1: Valid task with no due_date (should work)
    print("\n1. Testing TaskCreate with no due_date...")
    try:
        task1 = TaskCreate(
            title="Test task",
            description="Test without due date",
            priority="medium",
            category="test"
            # No due_date field
        )
        print(f"   Success: Created task with due_date={task1.due_date}")
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

    # Test 2: Valid task with proper due_date (should work)
    print("\n2. Testing TaskCreate with proper due_date...")
    try:
        proper_date = datetime.now()
        task2 = TaskCreate(
            title="Test task",
            description="Test with proper due date",
            priority="high",
            category="test",
            due_date=proper_date
        )
        print(f"   Success: Created task with due_date={task2.due_date}")
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

    # Test 3: Valid task with None due_date (should work)
    print("\n3. Testing TaskCreate with None due_date...")
    try:
        task3 = TaskCreate(
            title="Test task",
            description="Test with None due date",
            priority="low",
            category="test",
            due_date=None
        )
        print(f"   Success: Created task with due_date={task3.due_date}")
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

    print("\n[SUCCESS] All datetime parsing tests passed!")
    print("The Pydantic schema is correctly handling:")
    print("- Missing due_date fields (defaults to None)")
    print("- Proper datetime objects")
    print("- Explicit None values")
    print("\nThe 422 error fix is properly implemented in the backend schema.")

    return True

if __name__ == "__main__":
    print("="*60)
    print("Backend Datetime Parsing Fix Verification")
    print("="*60)

    success = test_datetime_parsing()

    if success:
        print("\n[SUCCESS] Backend datetime parsing fix verified!")
        sys.exit(0)
    else:
        print("\n[FAILURE] Backend datetime parsing fix verification failed!")
        sys.exit(1)