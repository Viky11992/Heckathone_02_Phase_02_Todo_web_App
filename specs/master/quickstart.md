# Quickstart Guide for Todo Full-Stack Web Application

## Overview
This guide provides step-by-step instructions to set up and run the Todo Full-Stack Web Application locally. The application consists of a Next.js frontend and a FastAPI backend with Neon PostgreSQL database.

## Prerequisites
- Node.js 18+ (for frontend development)
- Python 3.9+ (for backend development)
- PostgreSQL client tools
- Git version control system
- A Neon account for PostgreSQL database
- A Better Auth account for authentication

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo-fullstack-app
```

### 2. Backend Setup (FastAPI)

#### Navigate to Backend Directory
```bash
cd backend
```

#### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Set Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=your_neon_database_url
BETTER_AUTH_SECRET=your_jwt_secret_key
```

#### Run Database Migrations
```bash
alembic upgrade head
```

#### Start the Backend Server
```bash
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup (Next.js)

#### Navigate to Frontend Directory
```bash
cd frontend
```

#### Install Dependencies
```bash
npm install
```

#### Set Environment Variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
NEXT_PUBLIC_BETTER_AUTH_SECRET=your_jwt_secret_key
```

#### Start the Frontend Development Server
```bash
npm run dev
```

## Configuration Details

### Better Auth Configuration
The application uses Better Auth for authentication. The configuration is set up in `frontend/src/lib/auth.ts`:

```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET!,
    }),
  ],
});
```

### Database Configuration
The backend uses SQLModel with Neon PostgreSQL. The database connection is configured in `backend/database.py`:

```python
from sqlmodel import create_engine
from .config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,
    pool_pre_ping=True,
)
```

### API Endpoints
The backend provides the following API endpoints:
- `GET /api/{user_id}/tasks` - List all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get task details
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status

## Running the Application

### Development Mode
1. Start the backend server: `cd backend && uvicorn main:app --reload --port 8000`
2. Start the frontend server: `cd frontend && npm run dev`
3. Access the application at `http://localhost:3000`

### Production Mode
1. Build the frontend: `cd frontend && npm run build`
2. Start the backend server in production mode
3. Configure your web server to serve the frontend and proxy API requests to the backend

## Testing

### Backend Tests
Run backend tests with pytest:
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests
Run frontend tests:
```bash
cd frontend
npm test
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Verify your Neon database URL is correct
   - Ensure your database credentials are properly set
   - Run `alembic upgrade head` to ensure migrations are applied

2. **Authentication Issues**:
   - Ensure the `BETTER_AUTH_SECRET` is the same in both frontend and backend
   - Verify JWT configuration is correct
   - Check that authentication middleware is properly set up

3. **API Connection Issues**:
   - Verify backend server is running on the correct port
   - Check that frontend API client is configured with the correct base URL
   - Ensure CORS settings allow frontend-backend communication

### Development Tips
- Use the FastAPI automatic documentation at `http://localhost:8000/docs`
- Check the Next.js development server for compilation errors
- Monitor database logs if experiencing connection issues
- Use browser developer tools to debug API requests

## Next Steps

1. Implement the remaining features as per the specification
2. Add comprehensive tests for all functionality
3. Set up CI/CD pipeline for automated testing and deployment
4. Configure monitoring and logging for production
5. Implement performance optimizations