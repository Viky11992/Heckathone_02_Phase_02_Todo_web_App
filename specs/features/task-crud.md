# Feature: Task CRUD Operations

## Overview
Enable users to create, read, update, and delete todo tasks in the application. This feature forms the core functionality of the todo application.

## User Stories
- As a user, I can create a new task with a title and optional description
- As a user, I can view all my tasks with their current status
- As a user, I can update an existing task's details
- As a user, I can delete a task I no longer need
- As a user, I can mark a task as complete or pending
- As a user, I can filter tasks by status (all, pending, completed)

## Acceptance Criteria

### Create Task
- Title is required (1-200 characters)
- Description is optional (max 1000 characters)
- Task is associated with the authenticated user
- Task is created with "pending" status by default
- Created timestamp is automatically set
- Returns 201 Created with the new task object

### View Tasks
- Only show tasks for the authenticated user
- Display title, status (pending/completed), and creation date
- Support filtering by status (all, pending, completed)
- Support sorting by creation date or title
- Return paginated results if more than 50 tasks

### Update Task
- Allow updating title and description
- Preserve the original creation timestamp
- Update the modification timestamp
- Return 200 OK with updated task object

### Delete Task
- Remove the task from the user's list
- Return 204 No Content on successful deletion
- Prevent deletion of non-existent tasks (return 404)

### Toggle Completion
- Change task status between pending and completed
- Update the modification timestamp
- Return 200 OK with updated task object

## Business Rules
- Users can only access/modify their own tasks
- Tasks must have a non-empty title
- Task titles must be between 1 and 200 characters
- Task descriptions can be up to 1000 characters
- Tasks are automatically assigned to the creating user
- Tasks cannot be shared between users

## Error Conditions
- Unauthorized access: Return 401 Unauthorized
- Access to another user's tasks: Return 403 Forbidden
- Non-existent task: Return 404 Not Found
- Invalid input data: Return 400 Bad Request with validation errors
- Server error: Return 500 Internal Server Error

## Performance Requirements
- Task creation: < 200ms
- Task listing: < 300ms for up to 100 tasks
- Task updates: < 200ms
- Task deletion: < 200ms

## Security Considerations
- All operations require valid JWT authentication
- User ID in URL must match authenticated user
- Input validation to prevent injection attacks
- Rate limiting to prevent abuse