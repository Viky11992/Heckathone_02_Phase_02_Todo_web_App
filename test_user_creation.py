#!/usr/bin/env python3
"""
Test script to demonstrate user management and task creation
"""

import requests
import json
from datetime import datetime

# Base URL for the backend (adjust as needed)
BASE_URL = "http://localhost:8000/api"

def test_user_and_task_flow():
    print("=== Testing User Management and Task Creation ===\n")

    # Step 1: Generate a token for a user (this will create the user in the database)
    print("1. Generating token for user (this will create the user in the database)...")
    user_data = {
        "user_id": "test-user-123",
        "email": "test@example.com",
        "name": "Test User"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/generate-token", json=user_data)
        print(f"   Response Status: {response.status_code}")

        if response.status_code == 200:
            token_response = response.json()
            token = token_response.get("token")
            user_id = token_response.get("user_id")

            if token:
                print(f"   ✅ Successfully generated token for user: {user_id}")
                print(f"   Token: {token[:20]}...")  # Show first 20 chars only
            else:
                print("   ❌ Failed to generate token")
                print(f"   Response: {token_response}")
                return
        else:
            print(f"   ❌ Failed to generate token. Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error generating token: {e}")
        return

    # Step 2: Use the token to get user information
    print(f"\n2. Retrieving user information...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
        print(f"   Response Status: {response.status_code}")

        if response.status_code == 200:
            user_response = response.json()
            print(f"   ✅ Successfully retrieved user: {user_response['data']['name']}")
            print(f"   Email: {user_response['data']['email']}")
        else:
            print(f"   ❌ Failed to retrieve user. Status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error retrieving user: {e}")

    # Step 3: Use the token to create a task
    print(f"\n3. Creating task for user {user_id}...")

    task_data = {
        "title": "Test Task",
        "description": "This is a test task created for the test user",
        "priority": "medium",
        "category": "personal",
        "due_date": "2026-12-31T10:00:00"
    }

    try:
        response = requests.post(f"{BASE_URL}/{user_id}/tasks",
                               json=task_data,
                               headers=headers)
        print(f"   Response Status: {response.status_code}")

        if response.status_code in [200, 201]:
            task_response = response.json()
            print(f"   ✅ Successfully created task: {task_response['data']['title']}")
            task_id = task_response['data']['id']
            print(f"   Task ID: {task_id}")
        else:
            print(f"   ❌ Failed to create task. Status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error creating task: {e}")
        return

    # Step 4: Get the user's tasks
    print(f"\n4. Retrieving tasks for user {user_id}...")

    try:
        response = requests.get(f"{BASE_URL}/{user_id}/tasks", headers=headers)
        print(f"   Response Status: {response.status_code}")

        if response.status_code == 200:
            tasks_response = response.json()
            print(f"   ✅ Successfully retrieved {len(tasks_response['data'])} tasks")
            for task in tasks_response['data']:
                print(f"     - Task {task['id']}: {task['title']} (Completed: {task['completed']})")
        else:
            print(f"   ❌ Failed to retrieve tasks. Status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error retrieving tasks: {e}")

    # Step 5: List all users (admin functionality)
    print(f"\n5. Listing all users...")

    try:
        response = requests.get(f"{BASE_URL}/users", headers=headers)
        print(f"   Response Status: {response.status_code}")

        if response.status_code == 200:
            users_response = response.json()
            print(f"   ✅ Successfully retrieved {len(users_response['data'])} users")
            for user in users_response['data']:
                print(f"     - User {user['id']}: {user['name']} ({user['email']})")
        else:
            print(f"   ❌ Failed to retrieve users. Status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error retrieving users: {e}")

if __name__ == "__main__":
    test_user_and_task_flow()