from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional
from datetime import datetime
import os
from enum import Enum
from passlib.context import CryptContext


class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b", bcrypt__rounds=12)


class User(SQLModel, table=True):
    """
    User model for local user management
    """
    id: Optional[str] = Field(default=None, primary_key=True)  # Using string ID to match Better Auth pattern
    email: str = Field(unique=True, nullable=False, index=True)
    name: Optional[str] = Field(default=None, max_length=100)
    hashed_password: str = Field(nullable=False)  # Add hashed password field
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    def verify_password(self, plain_password: str) -> bool:
        """Verify a plain password against the hashed password."""
        return pwd_context.verify(plain_password, self.hashed_password)

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Hash a plain password."""
        # Truncate password to 72 bytes to comply with bcrypt limitations
        truncated_password = plain_password[:72] if len(plain_password) > 72 else plain_password
        return pwd_context.hash(truncated_password)


class Task(SQLModel, table=True):
    """
    Task model representing a user's todo task
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(nullable=False, foreign_key="user.id", index=True)  # Foreign key to User table
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    priority: Optional[str] = Field(default="medium", index=True)  # Using string for SQLite compatibility
    category: Optional[str] = Field(default="other", index=True)   # Using string for SQLite compatibility
    due_date: Optional[datetime] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }