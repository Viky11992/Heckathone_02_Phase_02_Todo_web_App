# Backend Guidelines

## Stack
- FastAPI
- SQLModel (ORM)
- Neon PostgreSQL
- Better Auth JWT integration

## Project Structure
- `main.py` - FastAPI app entry point
- `models.py` - SQLModel database models
- `routes/` - API route handlers
- `schemas/` - Pydantic request/response models
- `middleware/` - Authentication and other middleware
- `database.py` - Database connection
- `config.py` - Configuration settings

## API Conventions
- All routes under `/api/`
- Return JSON responses
- Use Pydantic models for request/response
- Handle errors with HTTPException
- All endpoints require JWT authentication

## Database
- Use SQLModel for all database operations
- Connection string from environment variable: DATABASE_URL
- Use async database operations where possible

## Authentication
- JWT tokens from Better Auth
- Middleware to verify JWT tokens
- User ID in token must match user ID in URL
- All endpoints require valid authentication