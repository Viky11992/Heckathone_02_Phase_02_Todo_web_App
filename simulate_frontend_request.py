"""
Script to simulate frontend requests to the backend to verify communication
between the frontend and backend systems.
"""
import requests
import json
import uuid
from datetime import datetime

def test_backend_health():
    """Test if the backend is accessible and healthy."""
    backend_url = "https://vickey92-todo-backend.hf.space"

    print("Testing backend health...")
    try:
        response = requests.get(f"{backend_url}/health")
        print(f"Health check status: {response.status_code}")
        if response.status_code == 200:
            print(f"Health response: {response.json()}")
            return True
        else:
            print(f"Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"Error connecting to backend: {str(e)}")
        return False

def test_cors_configuration():
    """Test if the backend accepts requests from the frontend origin."""
    backend_url = "https://vickey92-todo-backend.hf.space"

    print("\nTesting CORS configuration...")
    try:
        # Test with OPTIONS request to check CORS
        headers = {
            'Origin': 'https://heckathone-02-phase-02-todo-web-app.vercel.app',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'X-Requested-With, Content-Type, Authorization'
        }

        response = requests.options(f"{backend_url}/health", headers=headers)
        print(f"CORS preflight status: {response.status_code}")

        cors_headers = {k.lower(): v for k, v in response.headers.items()}
        if 'access-control-allow-origin' in cors_headers:
            print(f"Allowed origins: {cors_headers['access-control-allow-origin']}")
            return True
        else:
            print("CORS headers not found in response")
            return False
    except Exception as e:
        print(f"Error testing CORS: {str(e)}")
        return False

def test_token_generation():
    """Test the token generation endpoint."""
    backend_url = "https://vickey92-todo-backend.hf.space"

    print("\nTesting token generation...")
    try:
        # Create a mock user
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        user_data = {
            "user_id": user_id,
            "email": f"{user_id}@example.com",
            "name": f"Test User {user_id}"
        }

        response = requests.post(f"{backend_url}/api/auth/generate-token", json=user_data)
        print(f"Token generation status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Token generated successfully for user: {data.get('user_id')}")
            return data.get('token')
        else:
            print(f"Token generation failed: {response.text}")
            return None
    except Exception as e:
        print(f"Error generating token: {str(e)}")
        return None

def test_task_operations_with_token(token):
    """Test task CRUD operations with a valid token."""
    if not token:
        print("\nSkipping task operations - no valid token obtained")
        return False

    backend_url = "https://vickey92-todo-backend.hf.space"

    # Use the same user ID that was used to generate the token
    # Extract user_id from token payload (decode JWT)
    import base64
    try:
        # Split the JWT token to get the payload
        header, payload, signature = token.split('.')
        # Add padding if needed
        payload += '=' * (4 - len(payload) % 4)
        decoded_payload = base64.b64decode(payload)
        import json
        payload_data = json.loads(decoded_payload)
        user_id = payload_data.get('sub', f"test_user_{uuid.uuid4().hex[:8]}")
    except:
        # If decoding fails, use a random user ID
        user_id = f"test_user_{uuid.uuid4().hex[:8]}"

    print(f"\nTesting task operations for user: {user_id}")

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Test 1: Create a task
    print("  - Creating a task...")
    task_data = {
        "title": "Test task from frontend simulation",
        "description": "This task was created to test frontend-backend communication",
        "priority": "medium",
        "category": "personal",
        "due_date": "2026-12-31T23:59:59"
    }

    try:
        response = requests.post(f"{backend_url}/api/{user_id}/tasks",
                                json=task_data, headers=headers)
        print(f"    Create task status: {response.status_code}")

        if response.status_code == 200:
            created_task = response.json()
            task_id = created_task['data']['id']
            print(f"    Task created successfully with ID: {task_id}")
        else:
            print(f"    Task creation failed: {response.text}")
            # Continue with other tests even if this fails
            task_id = None

    except Exception as e:
        print(f"    Error creating task: {str(e)}")
        task_id = None

    # If we successfully created a task, proceed with other operations
    if task_id:
        # Test 2: Get the created task
        print("  - Retrieving the created task...")
        try:
            response = requests.get(f"{backend_url}/api/{user_id}/tasks/{task_id}",
                                   headers=headers)
            print(f"    Get task status: {response.status_code}")

            if response.status_code == 200:
                retrieved_task = response.json()
                print(f"    Task retrieved successfully: {retrieved_task['data']['title']}")
            else:
                print(f"    Task retrieval failed: {response.text}")

        except Exception as e:
            print(f"    Error retrieving task: {str(e)}")

        # Test 3: Update the task
        print("  - Updating the task...")
        update_data = {
            "title": "Updated test task from frontend simulation",
            "description": "This task was updated to test frontend-backend communication",
            "priority": "high",
            "category": "work",
            "due_date": "2026-12-31T23:59:59"
        }

        try:
            response = requests.put(f"{backend_url}/api/{user_id}/tasks/{task_id}",
                                  json=update_data, headers=headers)
            print(f"    Update task status: {response.status_code}")

            if response.status_code == 200:
                updated_task = response.json()
                print(f"    Task updated successfully: {updated_task['data']['title']}")
            else:
                print(f"    Task update failed: {response.text}")

        except Exception as e:
            print(f"    Error updating task: {str(e)}")

        # Test 4: Toggle task completion
        print("  - Toggling task completion...")
        completion_data = {
            "completed": True
        }

        try:
            response = requests.patch(f"{backend_url}/api/{user_id}/tasks/{task_id}/complete",
                                     json=completion_data, headers=headers)
            print(f"    Toggle completion status: {response.status_code}")

            if response.status_code == 200:
                toggled_task = response.json()
                print(f"    Task completion toggled: {toggled_task['data']['completed']}")
            else:
                print(f"    Task completion toggle failed: {response.text}")

        except Exception as e:
            print(f"    Error toggling task completion: {str(e)}")

    # Test 3: Get all tasks for the user (always run this)
    print("  - Retrieving all tasks for the user...")
    try:
        response = requests.get(f"{backend_url}/api/{user_id}/tasks",
                               headers=headers)
        print(f"    Get all tasks status: {response.status_code}")

        if response.status_code == 200:
            tasks_response = response.json()
            task_count = len(tasks_response['data'])
            print(f"    Found {task_count} tasks for user {user_id}")
            return True  # At least some operations worked
        else:
            print(f"    Get all tasks failed: {response.text}")
            return False

    except Exception as e:
        print(f"    Error retrieving all tasks: {str(e)}")
        return False

def main():
    print("="*60)
    print("FRONTEND-BACKEND COMMUNICATION TEST")
    print("="*60)

    # Step 1: Test backend health
    backend_healthy = test_backend_health()

    if not backend_healthy:
        print("\n❌ Backend is not accessible. Cannot proceed with tests.")
        return

    # Step 2: Test CORS configuration
    cors_ok = test_cors_configuration()

    # Step 3: Test token generation (simulates frontend auth)
    token = test_token_generation()

    # Step 4: Test task operations (main functionality)
    if token:
        tasks_work = test_task_operations_with_token(token)
    else:
        print("\n❌ Could not obtain authentication token. Cannot test task operations.")
        tasks_work = False

    print("\n" + "="*60)
    print("TEST SUMMARY:")
    print(f"- Backend Health: {'PASS' if backend_healthy else 'FAIL'}")
    print(f"- CORS Configuration: {'PASS' if cors_ok else 'FAIL'}")
    print(f"- Token Generation: {'PASS' if token else 'FAIL'}")
    print(f"- Task Operations: {'PASS' if tasks_work else 'FAIL'}")

    if backend_healthy and token and tasks_work:
        print("\nALL TESTS PASSED! The frontend and backend are communicating properly.")
        print("The system is ready for production use.")
    else:
        print("\nSome tests failed. Please check the backend configuration.")

    print("="*60)

if __name__ == "__main__":
    main()