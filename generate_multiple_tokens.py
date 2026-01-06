from datetime import datetime, timedelta
from jose import jwt
from backend.config import settings

def generate_token_for_user(user_id: str):
    """Generate a valid JWT token for a specific user ID"""
    payload = {
        "sub": user_id,  # This is the user ID that will be used in API calls
        "name": f"User {user_id}",
        "email": f"{user_id}@example.com",
        "exp": datetime.utcnow() + timedelta(days=30)  # Token expires in 30 days
    }

    # Generate the token using the same secret and algorithm as the backend
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token

# Example usage
print("Token generation script for Todo App")
print("=" * 50)

# Generate token for the specific user ID from the logs
user_id = "user-1767563258997"
token = generate_token_for_user(user_id)

print(f"Generated token for user: {user_id}")
print(f"Token: {token}")
print()
print("To use this token in the browser console:")
print(f"localStorage.setItem('auth_token', '{token}');")
print(f"localStorage.setItem('user_email', '{user_id}@example.com');")
print()

# Also generate for another user ID seen in the logs
user_id2 = "user-1767563612578"
token2 = generate_token_for_user(user_id2)

print(f"Generated token for user: {user_id2}")
print(f"Token: {token2}")
print()
print("To use this token in the browser console:")
print(f"localStorage.setItem('auth_token', '{token2}');")
print(f"localStorage.setItem('user_email', '{user_id2}@example.com');")
print()

# Also generate for our original test user
test_user_id = "test-user-123"
test_token = generate_token_for_user(test_user_id)

print(f"Generated token for user: {test_user_id}")
print(f"Token: {test_token}")
print()
print("To use this token in the browser console:")
print(f"localStorage.setItem('auth_token', '{test_token}');")
print(f"localStorage.setItem('user_email', 'test@example.com');")