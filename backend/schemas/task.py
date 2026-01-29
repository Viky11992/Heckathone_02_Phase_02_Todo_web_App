from pydantic import BaseModel, field_validator
from typing import Optional, List, Union
from datetime import datetime, date
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class TaskBase(BaseModel):
    """
    Base schema for task data
    """
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"  # Using string for compatibility
    category: Optional[str] = "other"   # Using string for compatibility
    due_date: Optional[datetime] = None

    @field_validator('due_date', mode='before')
    @classmethod
    def validate_due_date(cls, value):
        if value == "" or value is None:
            return None
        if isinstance(value, str):
            # Handle string datetime formats
            if value.strip() == "":
                return None
            # If it's a date-only string like "2023-12-31", convert to datetime
            if len(value) == 10 and '-' in value:  # YYYY-MM-DD format
                try:
                    # Convert date-only string to datetime (at midnight)
                    parsed_date = datetime.strptime(value, '%Y-%m-%d')
                    return parsed_date
                except ValueError:
                    pass  # Fall through to try datetime parsing
            # Try to parse as datetime
            try:
                # Handle various datetime formats including with/without timezone
                value_cleaned = value.replace('Z', '+00:00')
                if value_cleaned.count(':') == 1:  # HH:MM format without seconds
                    value_cleaned += ':00'

                # Handle timezone formats properly
                if '+' in value_cleaned and value_cleaned.count('+') == 1:
                    parts = value_cleaned.split('+')
                    dt_part = parts[0]
                    tz_part = parts[1]
                    if len(tz_part) == 2:
                        value_cleaned = f"{dt_part}+{tz_part}:00"

                return datetime.fromisoformat(value_cleaned.replace('Z', '+00:00'))
            except ValueError:
                pass
        elif isinstance(value, date) and type(value) is date:
            # If it's a date but not datetime, convert to datetime at midnight
            return datetime.combine(value, datetime.min.time())
        return value


class TaskCreate(TaskBase):
    """
    Schema for creating a new task
    """
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"  # Using string for compatibility
    category: Optional[str] = "other"   # Using string for compatibility
    # due_date inherited from TaskBase

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Need to buy milk, bread, and eggs",
                "priority": "medium",
                "category": "personal",
                "due_date": "2023-12-31T10:00:00Z"
            }
        }


class TaskUpdate(TaskBase):
    """
    Schema for updating an existing task
    """
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    # due_date inherited from TaskBase with its validator

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated task title",
                "description": "Updated task description",
                "priority": "high",
                "category": "work",
                "due_date": "2023-12-31"
            }
        }


class TaskToggleComplete(BaseModel):
    """
    Schema for toggling task completion status
    """
    completed: bool

    class Config:
        json_schema_extra = {
            "example": {
                "completed": True
            }
        }


class TaskResponse(TaskBase):
    """
    Schema for task response
    """
    id: int
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """
    Schema for task list response
    """
    success: bool
    data: List[TaskResponse]


class TaskResponseWrapper(BaseModel):
    """
    Wrapper for single task response
    """
    success: bool
    data: TaskResponse


class ErrorResponse(BaseModel):
    """
    Schema for error responses
    """
    success: bool
    error: dict


class TaskFilterParams(BaseModel):
    """
    Schema for task filtering parameters
    """
    status: Optional[TaskStatus] = "all"
    sort: Optional[str] = "created"
    page: Optional[int] = 1
    limit: Optional[int] = 20