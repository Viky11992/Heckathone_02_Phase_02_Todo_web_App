"""
Debug script to replicate the exact issue happening with datetime validation.
This replicates the exact error scenario from the console.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schemas.task import TaskCreate
from datetime import datetime

def debug_datetime_issue():
    """Debug the exact datetime issue with the error scenario."""

    print("Debugging the exact datetime validation issue...")

    # This is the exact data that's failing according to the console
    print("\nReplicating the exact failing scenario:")
    print('Input: {"title": "jhgjhgjhgjhg", "description": "hgjghjhg", "priority": "medium", "category": "other", "due_date": "2026-01-29"}')

    try:
        task_data = {
            "title": "jhgjhgjhgjhg",
            "description": "hgjghjhg",
            "priority": "medium",
            "category": "other",
            "due_date": "2026-01-29"  # This is the problematic value
        }

        print(f"\nAttempting to create TaskCreate with due_date='{task_data['due_date']}'")
        print(f"Type of due_date value: {type(task_data['due_date'])}")

        task = TaskCreate(**task_data)

        print(f"SUCCESS: Task created with due_date = {repr(task.due_date)}")
        print(f"Type of resulting due_date: {type(task.due_date)}")
        print("This means the backend validation is working correctly!")

    except Exception as e:
        print(f"ERROR: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return False

    # Also test what happens when we try to parse the exact string that's causing issues
    print(f"\nTesting direct parsing of '2026-01-29':")
    try:
        # Test if our validator can handle this specific string
        from datetime import datetime

        test_date_str = "2026-01-29"
        print(f"Trying to parse: '{test_date_str}'")

        # This is what our validator should do
        if len(test_date_str) == 10 and '-' in test_date_str:
            parsed = datetime.strptime(test_date_str, '%Y-%m-%d')
            print(f"Parsed successfully to: {parsed} (type: {type(parsed)})")

    except Exception as e:
        print(f"Parsing failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    print("\n[DEBUG RESULT] The backend validation appears to be working correctly.")
    print("If you're still getting 422 errors, the issue might be elsewhere.")
    print("Possible causes:")
    print("1. The deployed backend doesn't have the latest changes")
    print("2. There's a caching issue")
    print("3. The frontend isn't properly formatting the date before sending")

    return True

if __name__ == "__main__":
    print("="*60)
    print("Debugging DateTime Validation Issue")
    print("="*60)

    debug_datetime_issue()