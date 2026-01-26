# User Management System Documentation

## Overview
This document explains the user management system in the Todo Application, detailing who is responsible for user management and where user data is stored and accessed.

## Who is Responsible for User Management?

### Backend System (Primary Responsibility)
- **Custom JWT-based Authentication System**: The backend implements its own JWT authentication system rather than relying on a third-party service like Better Auth for user storage
- **JWT Token Generation**: The `/api/auth/generate-token` endpoint creates JWT tokens with user identity
- **Token Validation**: The `/api/auth/validate-token` endpoint validates JWT tokens
- **User ID Management**: The system uses user IDs embedded in JWT tokens for identification

### Frontend System (Secondary Role)
- **LocalStorage Management**: Stores authentication tokens, user IDs, and emails in browser's localStorage
- **Token Lifecycle**: Handles token generation, storage, and cleanup
- **User Session Management**: Manages user authentication state in the browser

## How User Data is Stored and Accessed

### User Identity Storage

#### In Database
- **File**: `backend/models.py` - Contains the `Task` model with `user_id` field
- **Database Table**: Each task record has a `user_id` column linking it to a user
- **Field Location**: Line 18 in `models.py` shows `user_id: str = Field(nullable=False, index=True)` with comment "Foreign key to Better Auth user"

#### In JWT Tokens
- **Storage**: User ID is stored in the `sub` (subject) field of JWT tokens
- **Format**: The JWT payload contains `{"sub": user_id, "name": name, "email": email, "exp": expiration_time}`

#### In Frontend LocalStorage
- **File**: `frontend/lib/auth-service.ts` - Manages user authentication state
- **LocalStorage Keys**:
  - `'auth_token'` - Stores the JWT token
  - `'user_id'` - Stores the user ID
  - `'user_email'` - Stores the user email

### API Endpoints for User Data
- `/api/{user_id}/tasks` - Get all tasks for a specific user
- `/api/{user_id}/tasks/{id}` - Get a specific task for a specific user
- `/api/{user_id}/tasks/{id}/complete` - Toggle completion status for a specific user's task
- `/api/{user_id}/tasks` (POST) - Create a new task for a specific user
- `/api/{user_id}/tasks/{id}` (PUT) - Update a specific task for a specific user
- `/api/{user_id}/tasks/{id}` (DELETE) - Delete a specific task for a specific user
- `/api/auth/me` - Get current user info (currently returns minimal data)
- `/api/auth/generate-token` - Generate JWT token for a user
- `/api/auth/validate-token` - Validate JWT token

### Authentication Flow
1. User registers/login via frontend
2. Frontend calls `/api/auth/generate-token` to generate token
3. Token contains user ID in the `sub` field
4. All subsequent requests include this token in Authorization header
5. Backend middleware extracts user ID from token and validates against URL parameters
6. Each user can only access their own data based on user ID matching

## Security Features
- **User Isolation**: Users can only access their own tasks (validated by comparing token user ID with URL user ID)
- **JWT Validation**: All requests require valid JWT tokens
- **Request State**: User ID is stored in request state for use by route handlers
- **Path Validation**: Middleware ensures user ID in token matches user ID in URL path
- **Authorization Checks**: Each route handler verifies user access rights

## Key Files
- `backend/middleware/auth.py` - JWT token validation and user identification
- `backend/models.py` - Task model with user_id foreign key
- `backend/routes/auth.py` - Authentication endpoints
- `backend/routes/tasks.py` - Task endpoints with user validation
- `frontend/lib/auth-service.ts` - Frontend authentication management
- `frontend/lib/api.ts` - API client that uses user authentication

## User Data Access Pattern
1. User authenticates and receives a JWT token
2. Token is stored in frontend localStorage
3. When making API requests, token is included in Authorization header
4. Backend middleware validates token and extracts user_id
5. Route handlers verify that the user_id in token matches the user_id in the URL
6. Database queries filter results by the user_id to ensure proper isolation