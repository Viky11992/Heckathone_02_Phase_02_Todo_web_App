# REST API Endpoints Specification

## Overview
This document defines the REST API endpoints for the Todo Full-Stack Web Application. All endpoints require JWT authentication and follow RESTful design principles.

## Base Configuration
- Base URL (Development): http://localhost:8000/api
- Base URL (Production): https://api.todoapp.com/api
- Content-Type: application/json
- Authentication: JWT token in Authorization header

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description",
    "details": { ... }
  }
}
```

## Endpoints

### Tasks Management

#### GET /{user_id}/tasks
List all tasks for the authenticated user.

**Parameters:**
- user_id (path): The ID of the authenticated user
- status (query, optional): Filter by status ("all", "pending", "completed") - default: "all"
- sort (query, optional): Sort by ("created", "title", "due_date") - default: "created"
- page (query, optional): Page number for pagination - default: 1
- limit (query, optional): Number of items per page - default: 20, max: 100

**Response:**
- 200: OK - Array of Task objects
- 401: Unauthorized - Invalid or missing token
- 403: Forbidden - User trying to access another user's tasks
- 500: Internal Server Error

#### POST /{user_id}/tasks
Create a new task for the authenticated user.

**Parameters:**
- user_id (path): The ID of the authenticated user

**Request Body:**
```json
{
  "title": "Task title (1-200 characters)",
  "description": "Optional task description (max 1000 characters)",
  "due_date": "Optional due date (ISO 8601 format)"
}
```

**Response:**
- 201: Created - The created Task object
- 400: Bad Request - Invalid input data
- 401: Unauthorized - Invalid or missing token
- 403: Forbidden - User trying to create task for another user
- 500: Internal Server Error

#### GET /{user_id}/tasks/{id}
Get details of a specific task.

**Parameters:**
- user_id (path): The ID of the authenticated user
- id (path): The ID of the task

**Response:**
- 200: OK - The Task object
- 401: Unauthorized - Invalid or missing token
- 403: Forbidden - User trying to access another user's task
- 404: Not Found - Task does not exist
- 500: Internal Server Error

#### PUT /{user_id}/tasks/{id}
Update an existing task.

**Parameters:**
- user_id (path): The ID of the authenticated user
- id (path): The ID of the task

**Request Body:**
```json
{
  "title": "Updated task title (1-200 characters)",
  "description": "Updated task description (max 1000 characters)",
  "due_date": "Optional due date (ISO 8601 format)"
}
```

**Response:**
- 200: OK - The updated Task object
- 400: Bad Request - Invalid input data
- 401: Unauthorized - Invalid or missing token
- 403: Forbidden - User trying to update another user's task
- 404: Not Found - Task does not exist
- 500: Internal Server Error

#### DELETE /{user_id}/tasks/{id}
Delete a specific task.

**Parameters:**
- user_id (path): The ID of the authenticated user
- id (path): The ID of the task

**Response:**
- 204: No Content - Task successfully deleted
- 401: Unauthorized - Invalid or missing token
- 403: Forbidden - User trying to delete another user's task
- 404: Not Found - Task does not exist
- 500: Internal Server Error

#### PATCH /{user_id}/tasks/{id}/complete
Toggle the completion status of a task.

**Parameters:**
- user_id (path): The ID of the authenticated user
- id (path): The ID of the task

**Request Body:**
```json
{
  "completed": true
}
```

**Response:**
- 200: OK - The updated Task object
- 401: Unauthorized - Invalid or missing token
- 403: Forbidden - User trying to update another user's task
- 404: Not Found - Task does not exist
- 500: Internal Server Error

## Data Models

### Task Object
```json
{
  "id": 123,
  "user_id": "user-uuid",
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "created_at": "2026-01-01T10:00:00Z",
  "updated_at": "2026-01-01T10:00:00Z",
  "due_date": "2026-01-15T00:00:00Z"
}
```

## Error Codes
- `VALIDATION_ERROR`: Input validation failed
- `UNAUTHORIZED_ACCESS`: Invalid or missing authentication token
- `FORBIDDEN_ACCESS`: User trying to access unauthorized resource
- `RESOURCE_NOT_FOUND`: Requested resource does not exist
- `INTERNAL_ERROR`: Server-side error occurred
- `RATE_LIMIT_EXCEEDED`: Too many requests from the same IP

## Rate Limiting
- General API requests: 1000 requests per hour per IP
- Authentication requests: 50 requests per hour per IP
- Exceeding limits results in 429 Too Many Requests response

## Security Headers
All responses include:
- Strict-Transport-Security: max-age=31536000; includeSubDomains
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block