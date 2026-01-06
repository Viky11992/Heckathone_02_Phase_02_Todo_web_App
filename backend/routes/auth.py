from fastapi import APIRouter, HTTPException, status, Depends, Request
from schemas import task as task_schemas
from middleware.auth import JWTBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from config import settings


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


@router.post("/auth/generate-token")
async def generate_token(request: Request):
    """
    Generate a JWT token for a user (for frontend authentication)
    This endpoint allows the frontend to get a proper JWT token
    """
    try:
        # Get user data from request body
        body = await request.json()
        user_id = body.get('user_id', 'default-user')
        email = body.get('email', f'{user_id}@example.com')
        name = body.get('name', f'User {user_id}')

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