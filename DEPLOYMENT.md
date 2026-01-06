# Todo Application - Deployment Guide

This is a full-stack todo application with a Next.js frontend and FastAPI backend. The application is designed to be deployed with the frontend on Vercel and the backend on Railway.

## Architecture

- **Frontend**: Next.js 16+ application with TypeScript, Tailwind CSS, and Better Auth
- **Backend**: FastAPI application with PostgreSQL database
- **Authentication**: JWT-based authentication with Better Auth

## Deployment

### Backend Deployment (Railway)

1. Create a Railway account at [railway.app](https://railway.app)
2. Create a new project and connect to this repository
3. Set the following environment variables:
   - `DATABASE_URL`: Your PostgreSQL database connection string
   - `JWT_SECRET`: A secure secret for JWT tokens
   - `BETTER_AUTH_SECRET`: A secure secret for Better Auth
   - `PORT`: Will be set by Railway automatically (typically 8000+)
4. The application will be deployed using the Dockerfile in the backend directory
5. Take note of your backend deployment URL (e.g., `https://your-app-name.up.railway.app`)

### Frontend Deployment (Vercel)

1. Create a Vercel account at [vercel.com](https://vercel.com)
2. Import your repository
3. Set the following environment variable:
   - `NEXT_PUBLIC_API_BASE_URL`: The URL of your deployed backend (from Railway deployment, without `/api` part)
4. The application will be deployed automatically
5. Your frontend will be available at a URL like `https://your-app-name.vercel.app`

## Environment Variables

### Backend (Railway)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL database connection string | `postgresql://user:pass@host:port/dbname` |
| `JWT_SECRET` | Secret for JWT token signing | `your-super-secret-jwt-key-change-in-production` |
| `BETTER_AUTH_SECRET` | Secret for Better Auth | `your-better-auth-secret-key` |
| `PORT` | Port to run the application on | `8000` (set by Railway) |

### Frontend (Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | Base URL for the backend API | `https://your-railway-app.up.railway.app` |

## Development

To run the application locally:

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Features

- User authentication with Better Auth
- Full CRUD operations for todo tasks
- Task categorization and prioritization
- Responsive UI that works on all device sizes
- JWT-based authentication and authorization
- PostgreSQL database with SQLModel ORM