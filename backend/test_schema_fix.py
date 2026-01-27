from schemas.task import TaskCreate
from datetime import datetime

print("Testing the fixed schema...")

# Test 1: Empty string should become None
try:
    task1 = TaskCreate(
        title="Test task",
        description="Test with empty due_date",
        priority="medium",
        category="personal",
        due_date=""
    )
    print(f"PASS Test 1 - Empty string: due_date = {task1.due_date} (type: {type(task1.due_date)})")
except Exception as e:
    print(f"FAIL Test 1 failed: {e}")

# Test 2: None should remain None
try:
    task2 = TaskCreate(
        title="Test task",
        description="Test with None due_date",
        priority="medium",
        category="personal",
        due_date=None
    )
    print(f"PASS Test 2 - None: due_date = {task2.due_date} (type: {type(task2.due_date)})")
except Exception as e:
    print(f"FAIL Test 2 failed: {e}")

# Test 3: Valid datetime string should work
try:
    task3 = TaskCreate(
        title="Test task",
        description="Test with valid datetime",
        priority="medium",
        category="personal",
        due_date="2026-12-31T23:59:59"
    )
    print(f"PASS Test 3 - Valid datetime: due_date = {task3.due_date} (type: {type(task3.due_date)})")
except Exception as e:
    print(f"FAIL Test 3 failed: {e}")

# Test 4: Date-only string should work
try:
    task4 = TaskCreate(
        title="Test task",
        description="Test with date-only",
        priority="medium",
        category="personal",
        due_date="2026-12-31"
    )
    print(f"PASS Test 4 - Date-only: due_date = {task4.due_date} (type: {type(task4.due_date)})")
except Exception as e:
    print(f"FAIL Test 4 failed: {e}")

print("Schema validation tests completed!")