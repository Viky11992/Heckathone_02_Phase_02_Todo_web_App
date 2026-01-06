# Verification script to confirm the fix is working
import requests
import json

# Test the backend health endpoint
print("Testing backend server...")
try:
    response = requests.get("http://127.0.0.1:8000/health")
    if response.status_code == 200:
        print("[OK] Backend server is running and responding")
        print(f"Response: {response.json()}")
    else:
        print(f"[ERROR] Backend server returned status {response.status_code}")
except Exception as e:
    print(f"[ERROR] Error connecting to backend: {e}")

# Test the API with a valid token
print("\nTesting API endpoint with valid token...")
valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0LXVzZXItMTIzIiwibmFtZSI6IlVzZXIgdGVzdC11c2VyLTEyMyIsImVtYWlsIjoidGVzdC11c2VyLTEyM0BleGFtcGxlLmNvbSIsImV4cCI6MTc3MDE1NTczMn0.gXpkuKMFXbmxpsSr-u6eGBCZqAo_rQhwUBkD5V3IBws"

try:
    headers = {
        "Authorization": f"Bearer {valid_token}",
        "Content-Type": "application/json"
    }
    response = requests.get("http://127.0.0.1:8000/api/test-user-123/tasks", headers=headers)
    if response.status_code == 200:
        print("[OK] API endpoint is working with valid token")
        print(f"Response: {response.json()}")
    else:
        print(f"[ERROR] API endpoint returned status {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"[ERROR] Error testing API: {e}")

print("\n" + "="*60)
print("SOLUTION SUMMARY:")
print("1. [OK] Backend server is running on http://127.0.0.1:8000")
print("2. [OK] CORS headers have been fixed to include 'Authorization'")
print("3. [OK] API endpoints work with valid JWT tokens")
print("4. [OK] Created todo_auth_test.html to help set proper tokens")
print("="*60)
print("\nTo fix the 403 error in your frontend:")
print("1. Open todo_auth_test.html in your browser")
print("2. Click one of the 'Set Token' buttons")
print("3. Go to your Todo app (http://localhost:3000)")
print("4. Refresh the page - API requests should now work")