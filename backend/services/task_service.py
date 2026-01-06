from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import models
from schemas import task as task_schemas


class TaskService:
    """
    Service class for handling task-related business logic
    """

    @staticmethod
    def create_task(session: Session, user_id: str, task_data: task_schemas.TaskCreate) -> models.Task:
        """
        Create a new task for a user
        """
        # Validate input data
        TaskService.validate_task_data(task_data)

        # Create task instance
        task = models.Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            category=task_data.category,
            due_date=task_data.due_date,
            completed=False,  # New tasks are created as pending by default
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Add to database
        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def get_task_by_id(session: Session, task_id: int, user_id: str) -> Optional[models.Task]:
        """
        Get a specific task by ID for a specific user
        """
        task = session.get(models.Task, task_id)

        # Verify that the task belongs to the user
        if task and task.user_id == user_id:
            return task
        return None

    @staticmethod
    def get_tasks_for_user(
        session: Session,
        user_id: str,
        status_filter: str = "all",
        priority_filter: str = "all",
        category_filter: str = "all",
        sort_by: str = "created",
        page: int = 1,
        limit: int = 20
    ) -> List[models.Task]:
        """
        Get all tasks for a specific user with optional filtering and sorting
        """
        # Build query
        query = select(models.Task).where(models.Task.user_id == user_id)

        # Apply status filter
        if status_filter and status_filter != "all":
            query = query.where(models.Task.completed == (status_filter == "completed"))

        # Apply priority filter
        if priority_filter and priority_filter != "all":
            query = query.where(models.Task.priority == priority_filter)

        # Apply category filter
        if category_filter and category_filter != "all":
            query = query.where(models.Task.category == category_filter)

        # Apply sorting
        if sort_by == "title":
            query = query.order_by(models.Task.title)
        elif sort_by == "created":
            query = query.order_by(models.Task.created_at.desc())
        elif sort_by == "due_date":
            query = query.order_by(models.Task.due_date.asc())
        elif sort_by == "priority":
            query = query.order_by(models.Task.priority)
        else:  # default
            query = query.order_by(models.Task.created_at.desc())

        # Apply pagination
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        return session.exec(query).all()

    @staticmethod
    def update_task(
        session: Session,
        task_id: int,
        user_id: str,
        task_data: task_schemas.TaskUpdate
    ) -> Optional[models.Task]:
        """
        Update an existing task
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)

        if not task:
            return None

        # Update task fields if provided
        if task_data.title is not None:
            TaskService.validate_title(task_data.title)
            task.title = task_data.title
        if task_data.description is not None:
            TaskService.validate_description(task_data.description)
            task.description = task_data.description
        if task_data.priority is not None:
            task.priority = task_data.priority
        if task_data.category is not None:
            task.category = task_data.category
        if task_data.due_date is not None:
            task.due_date = task_data.due_date

        # Update the timestamp
        task.updated_at = datetime.utcnow()

        # Commit changes to database
        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: str) -> bool:
        """
        Delete a specific task
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)

        if not task:
            return False

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(
        session: Session,
        task_id: int,
        user_id: str,
        completion_data: task_schemas.TaskToggleComplete
    ) -> Optional[models.Task]:
        """
        Toggle the completion status of a task
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)

        if not task:
            return None

        # Update completion status
        task.completed = completion_data.completed
        task.updated_at = datetime.utcnow()

        # Commit changes to database
        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def validate_task_data(task_data: task_schemas.TaskCreate) -> None:
        """
        Validate task data
        """
        TaskService.validate_title(task_data.title)
        if task_data.description:
            TaskService.validate_description(task_data.description)
        if task_data.priority and task_data.priority not in ["low", "medium", "high", "urgent"]:
            raise ValueError("Priority must be one of: low, medium, high, urgent")
        if task_data.category and task_data.category not in ["work", "personal", "health", "finance", "education", "other"]:
            raise ValueError("Category must be one of: work, personal, health, finance, education, other")

    @staticmethod
    def validate_title(title: str) -> None:
        """
        Validate task title
        """
        if not title or len(title.strip()) == 0:
            raise ValueError("Title is required")

        if len(title) < 1 or len(title) > 200:
            raise ValueError("Title must be between 1 and 200 characters")

    @staticmethod
    def validate_description(description: Optional[str]) -> None:
        """
        Validate task description
        """
        if description and len(description) > 1000:
            raise ValueError("Description must be less than 1000 characters")