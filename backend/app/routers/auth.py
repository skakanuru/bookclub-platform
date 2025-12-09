"""Authentication routes for Google OAuth and token management."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.auth import GoogleAuthRequest, TokenResponse
from ..schemas.user import UserResponse
from ..services.auth_service import AuthService
from ..middleware.auth_middleware import get_current_user
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/google", response_model=TokenResponse)
async def google_auth(
    auth_request: GoogleAuthRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with Google ID token.

    Args:
        auth_request: Google authentication request with ID token
        db: Database session

    Returns:
        JWT access token and user information
    """
    return AuthService.authenticate_google_user(db, auth_request.token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information.

    Args:
        current_user: Current authenticated user

    Returns:
        User information
    """
    return UserResponse.from_orm(current_user)


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user (client-side should remove token).

    Args:
        current_user: Current authenticated user

    Returns:
        Success message
    """
    # JWT tokens are stateless, so logout is handled client-side
    # This endpoint is mainly for consistent API and future enhancements
    return {"message": "Logged out successfully"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Refresh JWT token for current user.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        New JWT access token and user information
    """
    return AuthService.create_token_response(current_user)
