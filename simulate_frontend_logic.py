"""
Simulate the frontend date formatting logic to verify it produces the right format
"""

def simulate_format_date_to_datetime(date_string):
    """Simulate the frontend formatDateToDateTime function logic"""
    if not date_string:  # Handles None, empty string, undefined
        return None

    # If dateString is already in ISO datetime format, return as is
    if 'T' in str(date_string):
        return date_string

    # Convert date string (YYYY-MM-DD) to datetime (YYYY-MM-DDT00:00:00)
    return f"{date_string}T00:00:00"

def simulate_create_task_payload(task_data):
    """Simulate how the frontend prepares the payload"""
    # This mimics the logic in api.ts createTask method
    prepared_data = {
        **task_data,
        "due_date": simulate_format_date_to_datetime(task_data.get("due_date")) or None
    }

    # Remove due_date if it's None to not send it in the request
    if prepared_data["due_date"] is None:
        del prepared_data["due_date"]

    return prepared_data

def test_frontend_logic():
    print("Testing frontend date formatting logic...\n")

    # Test cases
    test_cases = [
        {"input": "2026-01-29", "expected": "2026-01-29T00:00:00"},
        {"input": "2026-01-29T10:30:00", "expected": "2026-01-29T10:30:00"},  # Already datetime
        {"input": "", "expected": None},
        {"input": None, "expected": None}
    ]

    print("Test cases for formatDateToDateTime:")
    for i, test_case in enumerate(test_cases, 1):
        result = simulate_format_date_to_datetime(test_case["input"])
        passed = result == test_case["expected"]

        print(f"{i}. Input: {repr(test_case['input'])}")
        print(f"   Expected: {repr(test_case['expected'])}")
        print(f"   Got: {repr(result)}")
        print(f"   Status: {'PASS' if passed else 'FAIL'}\n")

    # Test the exact scenario from the error
    print("Testing the exact failing scenario:")
    print("Original payload from frontend:")
    original_task_data = {
        "title": "jhgjhgjhgjhg",
        "description": "hgjghjhg",
        "priority": "medium",
        "category": "other",
        "due_date": "2026-01-29"  # This is what comes from the date picker
    }

    print(f"  {original_task_data}")

    print("\nAfter frontend processing (what gets sent to backend):")
    processed_payload = simulate_create_task_payload(original_task_data)
    print(f"  {processed_payload}")

    print(f"\nNotice: The due_date became '{processed_payload['due_date']}'")
    print("This format SHOULD be accepted by the updated backend!")
    print("\nThe issue is likely that your deployed backend (Hugging Face Space) doesn't have the recent fixes.")

if __name__ == "__main__":
    test_frontend_logic()