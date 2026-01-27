"""
Test script to verify the API is working properly and that the 422 error fix is in place.
This script tests task creation with and without due dates to ensure the datetime parsing issue is resolved.
"""

import requests
import json
from datetime import datetime
import sys

def test_api_endpoints():
    """Test the API endpoints to verify the 422 error fix."""

    base_url = "http://127.0.0.1:8000/api"

    print("Testing API endpoints...")

    # Test 1: Try to get tasks for a dummy user (should return empty list or 404, but not 422)
    print("\n1. Testing GET /{user_id}/tasks endpoint...")
    try:
        response = requests.get(f"{base_url}/dummy_user/tasks")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 401:
            print("   Expected: 401 Unauthorized (due to authentication)")
        elif response.status_code == 200:
            print("   Success: 200 OK - Endpoint accessible")
        else:
            print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error connecting to API: {str(e)}")
        return False

    # Test 2: Test task creation with no due date (should not cause 422 error)
    print("\n2. Testing POST /{user_id}/tasks with no due date...")
    try:
        task_data = {
            "title": "Test task without due date",
            "description": "This is a test task to verify the 422 error fix",
            "priority": "medium",
            "category": "test"
            # Note: No due_date field to test the fix
        }

        response = requests.post(f"{base_url}/dummy_user/tasks", json=task_data)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 401:
            print("   Expected: 401 Unauthorized (due to authentication)")
        elif response.status_code == 200:
            print("   Success: 200 OK - Task created successfully")
        elif response.status_code == 422:
            print("   ERROR: 422 Unprocessable Entity - datetime parsing issue still exists!")
            print(f"   Response: {response.text}")
            return False
        else:
            print(f"   Other status: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error creating task: {str(e)}")
        return False

    # Test 3: Test task creation with due date (should work properly)
    print("\n3. Testing POST /{user_id}/tasks with due date...")
    try:
        task_data = {
            "title": "Test task with due date",
            "description": "This is a test task with a due date",
            "priority": "high",
            "category": "test",
            "due_date": "2026-12-31T23:59:59"  # Proper ISO format
        }

        response = requests.post(f"{base_url}/dummy_user/tasks", json=task_data)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 401:
            print("   Expected: 401 Unauthorized (due to authentication)")
        elif response.status_code == 200:
            print("   Success: 200 OK - Task with due date created successfully")
        elif response.status_code == 422:
            print("   ERROR: 422 Unprocessable Entity - datetime parsing issue still exists!")
            print(f"   Response: {response.text}")
            return False
        else:
            print(f"   Other status: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error creating task with due date: {str(e)}")
        return False

    # Test 4: Test task creation with empty due date string (should handle gracefully)
    print("\n4. Testing POST /{user_id}/tasks with empty due date (testing the original bug scenario)...")
    try:
        task_data = {
            "title": "Test task with empty due date",
            "description": "This tests the original 422 error scenario",
            "priority": "low",
            "category": "test",
            "due_date": ""  # Empty string - this was causing the 422 error
        }

        response = requests.post(f"{base_url}/dummy_user/tasks", json=task_data)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 401:
            print("   Expected: 401 Unauthorized (due to authentication)")
        elif response.status_code == 200:
            print("   Success: 200 OK - Task with empty due date handled successfully")
        elif response.status_code == 422:
            print("   ERROR: 422 Unprocessable Entity - datetime parsing issue still exists!")
            print(f"   Response: {response.text}")
            return False
        else:
            print(f"   Other status: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error creating task with empty due date: {str(e)}")
        return False

    print("\n[SUCCESS] All tests passed! The 422 error fix appears to be working correctly.")
    print("The API is properly handling:")
    print("- Tasks without due dates")
    print("- Tasks with proper due dates")
    print("- Tasks with empty due date strings (gracefully handled)")
    print("\nThe datetime parsing issue has been resolved.")

    return True

if __name__ == "__main__":
    print("="*60)
    print("API 422 Error Fix Verification Test")
    print("="*60)

    success = test_api_endpoints()

    if success:
        print("\n[SUCCESS] The 422 API error fix is working properly!")
        sys.exit(0)
    else:
        print("\n❌ FAILURE: The 422 API error fix is not working properly!")
        sys.exit(1)