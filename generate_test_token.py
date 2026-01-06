from datetime import datetime, timedelta
from jose import jwt
from backend.config import settings

# Create a test token that will work with the backend
payload = {
    "sub": "test-user-123",  # This is the user ID that will be used in API calls
    "name": "Test User",
    "email": "test@example.com",
    "exp": datetime.utcnow() + timedelta(days=30)  # Token expires in 30 days
}

# Generate the token using the same secret and algorithm as the backend
token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

print("Generated test JWT token:")
print(token)
print("\nCopy this token and save it to localStorage in your browser console:")
print(f"localStorage.setItem('auth_token', '{token}');")
print("localStorage.setItem('user_email', 'test@example.com');")