from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session
from typing import List
from datetime import datetime
from database import get_session
import models
from middleware.auth import JWTBearer, get_current_user_id, verify_user_access
from pydantic import BaseModel


router = APIRouter()


class UserCreate(BaseModel):
    id: str
    email: str
    name: str = None
    password: str  # Password is required for user creation


class UserUpdate(BaseModel):
    email: str = None
    name: str = None
    password: str = None  # Optional password update


class UserResponse(BaseModel):
    id: str
    email: str
    name: str = None
    created_at: str
    updated_at: str


class UserResponseWrapper(BaseModel):
    success: bool
    data: UserResponse


class UserListResponse(BaseModel):
    success: bool
    data: List[UserResponse]


@router.get("/users/{user_id}", response_model=UserResponseWrapper)
async def get_user(
    user_id: str,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get a specific user by ID
    """
    # Verify that the user can only access their own user info (or admin access)
    verify_user_access(current_user_id, user_id)

    user = session.get(models.User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponseWrapper(
        success=True,
        data=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat()
        )
    )


@router.get("/users", response_model=UserListResponse)
async def list_users(
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    List all users (admin functionality)
    """
    # For now, we'll allow listing all users
    # In a real application, this would require admin privileges

    users = session.query(models.User).all()

    return UserListResponse(
        success=True,
        data=[
            UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                created_at=user.created_at.isoformat(),
                updated_at=user.updated_at.isoformat()
            )
            for user in users
        ]
    )


@router.post("/users", response_model=UserResponseWrapper)
async def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Create a new user
    """
    # Verify that the user creating the account matches the user ID (or admin)
    verify_user_access(current_user_id, user_data.id)

    # Check if user already exists
    existing_user = session.get(models.User, user_data.id)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    # Check if email already exists
    existing_email_user = session.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Hash the password
    hashed_password = models.User.hash_password(user_data.password)

    # Create new user
    user = models.User(
        id=user_data.id,
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return UserResponseWrapper(
        success=True,
        data=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat()
        )
    )


@router.put("/users/{user_id}", response_model=UserResponseWrapper)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Update an existing user
    """
    # Verify that the user can only update their own info
    verify_user_access(current_user_id, user_id)

    user = session.get(models.User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update user fields if provided
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.password is not None:
        # Hash the new password
        user.hashed_password = models.User.hash_password(user_data.password)

    user.updated_at = datetime.utcnow()

    session.add(user)
    session.commit()
    session.refresh(user)

    return UserResponseWrapper(
        success=True,
        data=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat()
        )
    )


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Delete a user
    """
    # Verify that the user can only delete their own account
    verify_user_access(current_user_id, user_id)

    user = session.get(models.User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    session.delete(user)
    session.commit()

    return {"success": True, "message": "User deleted successfully"}