"""Authentication routes for email/password and Google OAuth."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.auth import EmailPasswordRegister, EmailPasswordLogin, GoogleAuthRequest, TokenResponse
from ..schemas.user import UserResponse
from ..services.auth_service import AuthService
from ..middleware.auth_middleware import get_current_user
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(
    user_data: EmailPasswordRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user with email and password.

    Args:
        user_data: Registration data (email, password, name)
        db: Database session

    Returns:
        JWT access token and user information
    """
    user = AuthService.register_user(
        db,
        email=user_data.email,
        password=user_data.password,
        name=user_data.name
    )
    return AuthService.create_token_response(user)


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: EmailPasswordLogin,
    db: Session = Depends(get_db)
):
    """
    Login with email and password.

    Args:
        credentials: Login credentials (email, password)
        db: Database session

    Returns:
        JWT access token and user information
    """
    user = AuthService.authenticate_user(db, credentials.email, credentials.password)
    return AuthService.create_token_response(user)


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
