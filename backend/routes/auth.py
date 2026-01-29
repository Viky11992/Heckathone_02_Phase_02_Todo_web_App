from fastapi import APIRouter, HTTPException, status, Depends, Request
from schemas import task as task_schemas
from middleware.auth import JWTBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from config import settings
from sqlmodel import Session
from database import get_session
import models
from pydantic import BaseModel


router = APIRouter()


@router.get("/auth/me", response_model=task_schemas.TaskResponseWrapper)
async def get_current_user(
    current_user_id: str = Depends(JWTBearer())
):
    """
    Get current authenticated user info
    """
    # In a real implementation, this would return user details from the database
    # For now, we'll return a minimal response to show the endpoint exists
    return task_schemas.TaskResponseWrapper(
        success=True,
        data=task_schemas.TaskResponse(
            id=0,
            user_id=current_user_id,
            title="",
            description="",
            completed=False,
            created_at="2026-01-01T00:00:00Z",
            updated_at="2026-01-01T00:00:00Z"
        )
    )


class UserLogin(BaseModel):
    email: str
    password: str


class UserRegister(BaseModel):
    id: str
    email: str
    name: str
    password: str


@router.post("/auth/register")
async def register_user(user_data: UserRegister, session: Session = Depends(get_session)):
    """
    Register a new user with email and password
    """
    try:
        # Check if user already exists
        existing_user = session.query(models.User).filter(models.User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        # Hash the password
        hashed_password = models.User.hash_password(user_data.password)

        # Create new user
        new_user = models.User(
            id=user_data.id,
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        # Create JWT payload
        payload = {
            "sub": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "exp": datetime.utcnow() + timedelta(days=30)  # Token expires in 30 days
        }

        # Generate the token using the same secret and algorithm as the backend
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

        return {
            "success": True,
            "token": token,
            "user_id": new_user.id,
            "expires_in": 30 * 24 * 60 * 60  # 30 days in seconds
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error registering user: {str(e)}"
        )


@router.post("/auth/login")
async def login_user(login_data: UserLogin, session: Session = Depends(get_session)):
    """
    Login a user with email and password
    """
    try:
        # Find user by email
        user = session.query(models.User).filter(models.User.email == login_data.email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Verify password
        if not user.verify_password(login_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Create JWT payload
        payload = {
            "sub": user.id,
            "name": user.name,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(days=30)  # Token expires in 30 days
        }

        # Generate the token using the same secret and algorithm as the backend
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

        return {
            "success": True,
            "token": token,
            "user_id": user.id,
            "expires_in": 30 * 24 * 60 * 60  # 30 days in seconds
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error logging in: {str(e)}"
        )


@router.post("/auth/generate-token")
async def generate_token(request: Request, session: Session = Depends(get_session)):
    """
    Generate a JWT token for a user (for frontend authentication)
    This endpoint allows the frontend to get a proper JWT token
    NOTE: This endpoint is now for backward compatibility only.
    For security, use /auth/register or /auth/login instead.
    """
    try:
        # Get user data from request body
        body = await request.json()
        user_id = body.get('user_id', 'default-user')
        email = body.get('email', f'{user_id}@example.com')
        name = body.get('name', f'User {user_id}')
        password = body.get('password')  # Optional password for enhanced security

        # Check if user exists
        existing_user = session.get(models.User, user_id)
        if not existing_user:
            # Create new user with a default password if none provided
            hashed_password = models.User.hash_password(password if password else "default_temp_password")

            new_user = models.User(
                id=user_id,
                email=email,
                name=name,
                hashed_password=hashed_password,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        else:
            # Update user info if it has changed
            existing_user.email = email
            existing_user.name = name
            existing_user.updated_at = datetime.utcnow()
            session.add(existing_user)
            session.commit()

        # Create JWT payload
        payload = {
            "sub": user_id,
            "name": name,
            "email": email,
            "exp": datetime.utcnow() + timedelta(days=30)  # Token expires in 30 days
        }

        # Generate the token using the same secret and algorithm as the backend
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

        return {
            "success": True,
            "token": token,
            "user_id": user_id,
            "expires_in": 30 * 24 * 60 * 60  # 30 days in seconds
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error generating token: {str(e)}"
        )


@router.post("/auth/validate-token")
async def validate_token(request: Request):
    """
    Validate a JWT token and return user info
    This helps frontend verify if token is valid
    """
    try:
        body = await request.json()
        token = body.get('token')

        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token is required"
            )

        # Decode and validate the token
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])

        return {
            "success": True,
            "user_id": payload.get("sub"),
            "name": payload.get("name"),
            "email": payload.get("email"),
            "exp": payload.get("exp")
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error validating token: {str(e)}"
        )