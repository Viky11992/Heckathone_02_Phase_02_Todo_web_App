from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings using Pydantic Settings
    """
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app_local.db")
    db_echo: bool = os.getenv("DB_ECHO", "False").lower() == "true"

    # API settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    reload: bool = os.getenv("RELOAD", "True").lower() == "true"

    # JWT settings
    jwt_secret: str = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-change-in-production")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # CORS settings
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",

        # Add Vercel deployment URLs
        "https://heckathone-02-phase-02-todo-web-app.vercel.app",
        "https://*.vercel.app",
        # Add Hugging Face Space URL pattern
        "https://*.hf.space",
        "https://*.huggingface.app"
    ]

    # Better Auth settings
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "your-better-auth-secret-key")

    # Application settings
    app_name: str = "Todo API"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"


# Create settings instance
settings = Settings()