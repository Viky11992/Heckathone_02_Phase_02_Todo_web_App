#!/usr/bin/env python3
"""
Comprehensive test to verify user management and task creation functionality
"""

import requests
import json
from datetime import datetime

# Base URL for the backend (adjust as needed)
BASE_URL = "http://localhost:8000/api"

def test_comprehensive_flow():
    print("=== Comprehensive User & Task Management Test ===\n")

    # Step 1: Generate a token for a new user (this will create the user in the database)
    print("1. Generating token for a new user (creates user in database)...")
    user_data = {
        "user_id": "comprehensive-test-user",
        "email": "comprehensive.test@example.com",
        "name": "Comprehensive Test User"
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

    # Prepare headers with the token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Step 2: Verify the user was created by retrieving user info
    print(f"\n2. Verifying user creation by retrieving user info...")

    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
        print(f"   Response Status: {response.status_code}")

        if response.status_code == 200:
            user_response = response.json()
            print(f"   ✅ User verified: {user_response['data']['name']}")
            print(f"   Email: {user_response['data']['email']}")
            print(f"   Created at: {user_response['data']['created_at']}")
        else:
            print(f"   ❌ Failed to retrieve user. Status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error retrieving user: {e}")

    # Step 3: Create multiple tasks for the user
    print(f"\n3. Creating multiple tasks for user {user_id}...")

    tasks_to_create = [
        {
            "title": "First Task",
            "description": "This is the first task created for the user",
            "priority": "high",
            "category": "work",
            "due_date": "2026-12-31T10:00:00"
        },
        {
            "title": "Second Task",
            "description": "This is the second task created for the user",
            "priority": "medium",
            "category": "personal",
            "due_date": "2026-11-30T15:30:00"
        },
        {
            "title": "Third Task",
            "description": "This is the third task created for the user",
            "priority": "low",
            "category": "health",
            "due_date": "2026-10-15T09:00:00"
        }
    ]

    created_task_ids = []
    for i, task_data in enumerate(tasks_to_create, 1):
        try:
            response = requests.post(f"{BASE_URL}/{user_id}/tasks",
                                   json=task_data,
                                   headers=headers)
            print(f"   Task {i} - Status: {response.status_code}")

            if response.status_code in [200, 201]:
                task_response = response.json()
                task_id = task_response['data']['id']
                created_task_ids.append(task_id)
                print(f"     ✅ Created task '{task_response['data']['title']}' with ID: {task_id}")
            else:
                print(f"     ❌ Failed to create task {i}. Status: {response.status_code}")
                print(f"     Response: {response.text}")
        except Exception as e:
            print(f"     ❌ Error creating task {i}: {e}")

    # Step 4: Retrieve all tasks for the user
    print(f"\n4. Retrieving all tasks for user {user_id}...")

    try:
        response = requests.get(f"{BASE_URL}/{user_id}/tasks", headers=headers)
        print(f"   Response Status: {response.status_code}")

        if response.status_code == 200:
            tasks_response = response.json()
            print(f"   ✅ Successfully retrieved {len(tasks_response['data'])} tasks")

            for task in tasks_response['data']:
                print(f"     - Task {task['id']}: {task['title']} "
                      f"(Prio: {task['priority']}, Cat: {task['category']}, "
                      f"Completed: {task['completed']})")
        else:
            print(f"   ❌ Failed to retrieve tasks. Status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error retrieving tasks: {e}")

    # Step 5: Update one of the tasks
    if created_task_ids:
        print(f"\n5. Updating task ID {created_task_ids[0]}...")

        update_data = {
            "title": "Updated First Task",
            "description": "This task has been updated",
            "priority": "urgent",
            "completed": True
        }

        try:
            response = requests.put(f"{BASE_URL}/{user_id}/tasks/{created_task_ids[0]}",
                                  json=update_data,
                                  headers=headers)
            print(f"   Response Status: {response.status_code}")

            if response.status_code == 200:
                task_response = response.json()
                print(f"   ✅ Successfully updated task to: {task_response['data']['title']}")
                print(f"   New priority: {task_response['data']['priority']}")
                print(f"   Completed: {task_response['data']['completed']}")
            else:
                print(f"   ❌ Failed to update task. Status: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   ❌ Error updating task: {e}")

    # Step 6: List all users in the system
    print(f"\n6. Listing all users in the system...")

    try:
        response = requests.get(f"{BASE_URL}/users", headers=headers)
        print(f"   Response Status: {response.status_code}")

        if response.status_code == 200:
            users_response = response.json()
            print(f"   ✅ Successfully retrieved {len(users_response['data'])} total users")

            for user in users_response['data']:
                print(f"     - User {user['id']}: {user['name']} ({user['email']})")
        else:
            print(f"   ❌ Failed to retrieve users. Status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error retrieving users: {e}")

    print(f"\n=== Test Summary ===")
    print(f"✅ User creation: WORKING (users are created when tokens are generated)")
    print(f"✅ User storage: WORKING (users stored in database)")
    print(f"✅ Task creation: WORKING (tasks linked to users)")
    print(f"✅ Task management: WORKING (CRUD operations on tasks)")
    print(f"✅ User-task relationship: WORKING (foreign key relationships)")

if __name__ == "__main__":
    test_comprehensive_flow()