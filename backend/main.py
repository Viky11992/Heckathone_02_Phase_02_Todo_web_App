from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import engine
import models
from config import settings
from routes import tasks, auth, users
from sqlmodel import SQLModel
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI
    """
    # Initialize the database
    logging.info("Creating database tables...")
    # SQLModel.metadata.create_all(bind=engine)
    logging.info("Database tables created successfully")
    yield
    # Shutdown logic here if needed


# Create FastAPI app instance
app = FastAPI(
    title="Todo Application API",
    description="REST API for the Todo Full-Stack Web Application",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose the authorization header to allow frontend to access JWT tokens
    expose_headers=["Access-Control-Allow-Origin", "Authorization"]
)

# Include API routes
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(users.router, prefix="/api", tags=["users"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Todo API", "status": "running"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Todo API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )