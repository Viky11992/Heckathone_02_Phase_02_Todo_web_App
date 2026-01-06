# Database Schema Specification

## Overview
This document defines the database schema for the Todo Full-Stack Web Application using Neon Serverless PostgreSQL. The schema includes tables for tasks and integrates with Better Auth for user management.

## Database Configuration
- Database: Neon Serverless PostgreSQL
- Connection: Connection pooling with max 20 connections
- SSL: Required for all connections
- Character Set: UTF-8
- Collation: C.UTF-8

## Tables

### tasks
Stores user todo tasks with their status and metadata.

**Fields:**
- id (INTEGER, PRIMARY KEY, AUTO_INCREMENT): Unique identifier for the task
- user_id (TEXT, NOT NULL): Foreign key referencing the user who owns the task (references users.id from Better Auth)
- title (VARCHAR(200), NOT NULL): Task title (1-200 characters)
- description (TEXT, NULLABLE): Optional task description (max 1000 characters)
- completed (BOOLEAN, DEFAULT FALSE): Task completion status
- created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP): Timestamp when task was created
- updated_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP): Timestamp when task was last updated
- due_date (TIMESTAMP, NULLABLE): Optional due date for the task

**Indexes:**
- idx_tasks_user_id: Index on user_id for efficient user-based queries
- idx_tasks_completed: Index on completed for status-based queries
- idx_tasks_created_at: Index on created_at for time-based queries
- idx_tasks_due_date: Index on due_date for deadline-based queries

**Constraints:**
- fk_tasks_user_id: Foreign key constraint linking user_id to users.id (from Better Auth)
- chk_tasks_title_length: Check constraint ensuring title is 1-200 characters
- chk_tasks_description_length: Check constraint ensuring description is max 1000 characters

### users (Managed by Better Auth)
User information is managed by Better Auth, but we'll reference the structure for integration.

**Fields (as provided by Better Auth):**
- id (TEXT, PRIMARY KEY): Unique user identifier
- email (TEXT, NOT NULL, UNIQUE): User's email address
- name (TEXT, NULLABLE): User's display name
- image (TEXT, NULLABLE): URL to user's profile image
- email_verified (TIMESTAMP, NULLABLE): When email was verified
- created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP): Account creation timestamp
- updated_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP): Last update timestamp

**Indexes:**
- idx_users_email: Unique index on email for efficient lookups

## Relationships
- tasks.user_id → users.id (Many-to-One relationship)
- One user can have many tasks
- Each task belongs to exactly one user

## Database Operations

### Task Operations
**Create Task:**
- INSERT INTO tasks (user_id, title, description, completed, due_date)
- Automatically sets created_at and updated_at to current timestamp

**Read Tasks:**
- SELECT queries filtered by user_id for user isolation
- Support for filtering by completion status
- Support for sorting by creation date, title, or due date

**Update Task:**
- UPDATE tasks SET ... WHERE id = ? AND user_id = ?
- Automatically updates updated_at to current timestamp
- Prevents users from updating other users' tasks

**Delete Task:**
- DELETE FROM tasks WHERE id = ? AND user_id = ?
- Prevents users from deleting other users' tasks

### User Operations
**User Identification:**
- All task operations must verify user_id matches authenticated user
- Integration with Better Auth JWT token verification

## Performance Considerations

### Indexing Strategy
- Primary indexes on foreign keys (user_id) for fast JOINs and filtering
- Indexes on frequently queried columns (completed, created_at)
- Composite indexes for common query patterns if needed

### Query Optimization
- Always filter by user_id to leverage idx_tasks_user_id
- Use appropriate indexes for sorting operations
- Limit result sets with pagination for large datasets

### Connection Management
- Use connection pooling to manage database connections efficiently
- Implement proper connection cleanup to prevent leaks
- Monitor connection usage and adjust pool size as needed

## Security Considerations

### Data Isolation
- Foreign key constraints ensure referential integrity
- Application-level checks verify user_id matches authenticated user
- Prevent direct access to other users' data

### Input Validation
- Database constraints enforce data integrity
- Check constraints validate field values
- Proper escaping prevents SQL injection

### Access Control
- Database user has minimal required permissions
- No direct database access for application users
- All access through application API endpoints

## Migration Strategy

### Initial Schema Creation
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);

ALTER TABLE tasks
ADD CONSTRAINT chk_tasks_title_length
CHECK (LENGTH(title) >= 1 AND LENGTH(title) <= 200);

ALTER TABLE tasks
ADD CONSTRAINT chk_tasks_description_length
CHECK (LENGTH(description) <= 1000);
```

### Future Migrations
- Use Alembic for Python-based migration management
- Maintain backward compatibility when possible
- Test migrations on staging before production deployment
- Backup database before running migrations

## Backup and Recovery
- Automated daily backups of the database
- Point-in-time recovery capability
- Regular backup verification and restoration testing
- Retention policy: 30 days of daily backups, 12 months of monthly backups