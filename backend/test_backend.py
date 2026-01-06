from main import app
from fastapi.testclient import TestClient

def test_api_routes():
    """Test that API routes are registered"""
    client = TestClient(app)

    # Test that we get a proper response (even if unauthorized) rather than 404
    response = client.get("/api/user123/tasks")
    # Should return 401 (Unauthorized) or 403 (Forbidden) rather than 404 (Not Found)
    # This confirms the route exists
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.text}")
    # Just check that the route exists (doesn't return 404)
    assert response.status_code != 404

if __name__ == "__main__":
    test_api_routes()
    print("Backend route test passed!")