# Todo Full-Stack Web Application

A modern multi-user todo application built with Next.js, FastAPI, and PostgreSQL.

## Features

- **User Authentication**: Secure JWT-based authentication with Better Auth
- **Task Management**: Create, read, update, and delete tasks
- **Task Completion**: Toggle tasks between pending and completed
- **Responsive UI**: Works on all device sizes
- **Type Safety**: Full TypeScript and Pydantic validation
- **RESTful API**: Well-designed API endpoints

## Tech Stack

- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.9+, SQLModel
- **Database**: PostgreSQL (Neon Serverless)
- **Authentication**: Better Auth with JWT
- **Development**: Claude Code + Spec-Kit Plus

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL (or Neon account)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your configuration
```

4. Run the development server:
```bash
npm run dev
```

## API Endpoints

- `GET /api/{user_id}/tasks` - List all tasks for user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get task details
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status

## Environment Variables

### Backend

- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET` - Secret key for JWT signing
- `BETTER_AUTH_SECRET` - Secret key for Better Auth

### Frontend

- `NEXT_PUBLIC_API_BASE_URL` - Base URL for API calls
- `NEXT_PUBLIC_BETTER_AUTH_URL` - Better Auth URL

## Deployment

### Production Deployment

The application is designed to be deployed with the frontend on Vercel and the backend on Railway:

- **Frontend**: Deployed on [Vercel](https://vercel.com)
- **Backend**: Deployed on [Railway](https://railway.app)

For production deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Local Development with Docker

Build and run the application locally using Docker:

```bash
docker-compose up --build
```

## Project Structure

```
├── backend/                 # FastAPI backend
│   ├── main.py             # Application entry point
│   ├── models.py           # Database models
│   ├── database.py         # Database connection
│   ├── routes/             # API routes
│   ├── schemas/            # Pydantic schemas
│   ├── middleware/         # Middleware
│   └── services/           # Business logic
├── frontend/               # Next.js frontend
│   ├── app/                # App Router pages
│   ├── components/         # Reusable components
│   ├── hooks/              # Custom React hooks
│   ├── lib/                # Utilities and API client
│   └── styles/             # Global styles
└── specs/                  # Project specifications
    ├── master/             # Main feature specifications
    └── plan.md             # Implementation plan
```

## Security

- JWT-based authentication with proper token validation
- User data isolation - users can only access their own tasks
- Input validation and sanitization
- Rate limiting on API endpoints

## Architecture

- Clear separation between frontend and backend
- REST API with consistent endpoint patterns
- Service layer pattern for business logic
- Type safety with TypeScript and Pydantic

## Development

This project follows the Agentic Dev Stack workflow:
1. **Spec**: Document requirements in `/specs/`
2. **Plan**: Generate implementation plan with `/sp.plan`
3. **Tasks**: Break into testable tasks with `/sp.tasks`
4. **Implement**: Execute with Claude Code and Spec-Kit Plus

## Testing

Backend tests:
```bash
cd backend
python -m pytest
```

Frontend tests:
```bash
cd frontend
npm run test
```

## License

This project is licensed under the MIT License.