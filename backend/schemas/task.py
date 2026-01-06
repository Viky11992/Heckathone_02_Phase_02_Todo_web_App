from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
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


class TaskCreate(TaskBase):
    """
    Schema for creating a new task
    """
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"  # Using string for compatibility
    category: Optional[str] = "other"   # Using string for compatibility
    due_date: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Need to buy milk, bread, and eggs",
                "priority": "medium",
                "category": "personal",
                "due_date": "2023-12-31T10:00:00Z"
            }
        }


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task
    """
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Updated task title",
                "description": "Updated task description",
                "priority": "high",
                "category": "work",
                "due_date": "2023-12-31T10:00:00Z"
            }
        }


class TaskToggleComplete(BaseModel):
    """
    Schema for toggling task completion status
    """
    completed: bool

    class Config:
        schema_extra = {
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