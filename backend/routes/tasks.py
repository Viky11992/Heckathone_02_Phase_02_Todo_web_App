from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
import models
from database import get_session
from schemas import task as task_schemas
from middleware.auth import JWTBearer, get_current_user_id, verify_user_access
from services.task_service import TaskService
from datetime import datetime
import logging


router = APIRouter()


@router.get("/{user_id}/tasks", response_model=task_schemas.TaskListResponse)
async def list_tasks(
    user_id: str,
    status_filter: task_schemas.TaskStatus = "all",
    priority_filter: str = "all",
    category_filter: str = "all",
    sort: str = "created",
    page: int = 1,
    limit: int = 20,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    List all tasks for a specific user
    """
    # Verify that the user can only access their own tasks
    verify_user_access(current_user_id, user_id)

    # Use service to get tasks
    tasks = TaskService.get_tasks_for_user(
        session=session,
        user_id=user_id,
        status_filter=status_filter,
        priority_filter=priority_filter,
        category_filter=category_filter,
        sort_by=sort,
        page=page,
        limit=limit
    )

    return task_schemas.TaskListResponse(
        success=True,
        data=[task_schemas.TaskResponse.from_orm(task) for task in tasks]
    )


@router.post("/{user_id}/tasks", response_model=task_schemas.TaskResponseWrapper)
async def create_task(
    user_id: str,
    task_data: task_schemas.TaskCreate,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Create a new task for a specific user
    """
    # Verify that the user can only create tasks for themselves
    verify_user_access(current_user_id, user_id)

    try:
        # Use service to create task
        task = TaskService.create_task(
            session=session,
            user_id=user_id,
            task_data=task_data
        )

        return task_schemas.TaskResponseWrapper(
            success=True,
            data=task_schemas.TaskResponse.from_orm(task)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{user_id}/tasks/{id}", response_model=task_schemas.TaskResponseWrapper)
async def get_task(
    user_id: str,
    id: int,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get a specific task by ID
    """
    # Verify that the user can only access their own tasks
    verify_user_access(current_user_id, user_id)

    # Use service to get task
    task = TaskService.get_task_by_id(session=session, task_id=id, user_id=user_id)

    # Check if task exists
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task_schemas.TaskResponseWrapper(
        success=True,
        data=task_schemas.TaskResponse.from_orm(task)
    )


@router.put("/{user_id}/tasks/{id}", response_model=task_schemas.TaskResponseWrapper)
async def update_task(
    user_id: str,
    id: int,
    task_data: task_schemas.TaskUpdate,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Update a specific task
    """
    # Verify that the user can only update their own tasks
    verify_user_access(current_user_id, user_id)

    try:
        # Use service to update task
        updated_task = TaskService.update_task(
            session=session,
            task_id=id,
            user_id=user_id,
            task_data=task_data
        )

        # Check if task exists
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        return task_schemas.TaskResponseWrapper(
            success=True,
            data=task_schemas.TaskResponse.from_orm(updated_task)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}/tasks/{id}")
async def delete_task(
    user_id: str,
    id: int,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Delete a specific task
    """
    # Verify that the user can only delete their own tasks
    verify_user_access(current_user_id, user_id)

    # Use service to delete task
    success = TaskService.delete_task(session=session, task_id=id, user_id=user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"success": True, "message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{id}/complete", response_model=task_schemas.TaskResponseWrapper)
async def toggle_task_completion(
    user_id: str,
    id: int,
    completion_data: task_schemas.TaskToggleComplete,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Toggle the completion status of a task
    """
    # Verify that the user can only update their own tasks
    verify_user_access(current_user_id, user_id)

    # Use service to toggle task completion
    updated_task = TaskService.toggle_task_completion(
        session=session,
        task_id=id,
        user_id=user_id,
        completion_data=completion_data
    )

    # Check if task exists
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task_schemas.TaskResponseWrapper(
        success=True,
        data=task_schemas.TaskResponse.from_orm(updated_task)
    )