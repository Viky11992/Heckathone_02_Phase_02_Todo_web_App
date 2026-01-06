from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
from config import settings
import models
import logging


class JWTBearer(HTTPBearer):
    """
    JWT Bearer token authentication class
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme."
                )
            token = credentials.credentials
            user_id = self.verify_jwt(token)
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token or expired token."
                )
            # Add user_id to request state for use in route handlers
            request.state.user_id = user_id
            return user_id
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authentication credentials were not provided."
            )

    def verify_jwt(self, jwt_token: str) -> Optional[str]:
        """
        Verify the JWT token and return the user ID if valid
        """
        try:
            payload = jwt.decode(
                jwt_token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )
            user_id: str = payload.get("sub")
            if user_id:
                return user_id
        except JWTError as e:
            logging.error(f"JWT verification error: {e}")
        return None


# Dependency for requiring authentication
def get_current_user_id(token: str = Depends(JWTBearer())) -> str:
    """
    Get the current user ID from the JWT token
    """
    return token


def verify_user_access(user_id_in_token: str, user_id_in_url: str) -> bool:
    """
    Verify that the user ID in the token matches the user ID in the URL
    This ensures users can only access their own data
    """
    if user_id_in_token != user_id_in_url:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own data"
        )
    return True