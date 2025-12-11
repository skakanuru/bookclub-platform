"""Authentication service for email/password and Google OAuth."""
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from google.oauth2 import id_token
from google.auth.transport import requests
from ..config import get_settings
from ..models.user import User
from ..schemas.auth import GoogleUserInfo, TokenResponse
from ..schemas.user import UserResponse
from ..utils.security import create_access_token

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for handling authentication operations."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password. Truncates to 72 bytes for bcrypt compatibility."""
        # Bcrypt has a 72-byte limit, so truncate if necessary
        password_bytes = password.encode('utf-8')[:72]
        truncated_password = password_bytes.decode('utf-8', errors='ignore')
        return pwd_context.hash(truncated_password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash. Truncates to 72 bytes for bcrypt compatibility."""
        # Bcrypt has a 72-byte limit, so truncate if necessary
        password_bytes = plain_password.encode('utf-8')[:72]
        return pwd_context.verify(password_bytes, hashed_password)

    @staticmethod
    def register_user(db: Session, email: str, password: str, name: str) -> User:
        """
        Register a new user with email and password.

        Args:
            db: Database session
            email: User email
            password: Plain text password
            name: User full name

        Returns:
            Created user

        Raises:
            HTTPException: If email already exists
        """
        # Check if user exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        user = User(
            email=email,
            name=name,
            password_hash=AuthService.hash_password(password),
            last_login=datetime.utcnow()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        """
        Authenticate user with email and password.

        Args:
            db: Database session
            email: User email
            password: Plain text password

        Returns:
            Authenticated user

        Raises:
            HTTPException: If credentials are invalid
        """
        user = db.query(User).filter(User.email == email).first()
        if not user or not user.password_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not AuthService.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def verify_google_token(token: str) -> GoogleUserInfo:
        """
        Verify Google ID token and extract user information.

        Args:
            token: Google ID token from frontend

        Returns:
            GoogleUserInfo with user data

        Raises:
            HTTPException: If token is invalid
        """
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.google_client_id
            )

            # Verify token is for our app
            if idinfo['aud'] != settings.google_client_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token audience"
                )

            # Extract user information
            return GoogleUserInfo(
                google_id=idinfo['sub'],
                email=idinfo['email'],
                name=idinfo.get('name', idinfo['email']),
                avatar_url=idinfo.get('picture', '')
            )

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid Google token: {str(e)}"
            )

    @staticmethod
    def get_or_create_user(db: Session, google_user: GoogleUserInfo) -> User:
        """
        Get existing user or create new one from Google user info.

        Args:
            db: Database session
            google_user: Verified Google user information

        Returns:
            User instance
        """
        # Try to find existing user by google_id
        user = db.query(User).filter(User.google_id == google_user.google_id).first()

        if user:
            # Update last login
            user.last_login = datetime.utcnow()
            db.commit()
            db.refresh(user)
            return user

        # Create new user
        user = User(
            google_id=google_user.google_id,
            email=google_user.email,
            name=google_user.name,
            avatar_url=google_user.avatar_url,
            last_login=datetime.utcnow()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def create_token_response(user: User) -> TokenResponse:
        """
        Create JWT token response for authenticated user.

        Args:
            user: Authenticated user

        Returns:
            TokenResponse with access token and user info
        """
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.from_orm(user)
        )

    @staticmethod
    def authenticate_google_user(db: Session, token: str) -> TokenResponse:
        """
        Authenticate user with Google token and return JWT.

        Args:
            db: Database session
            token: Google ID token

        Returns:
            TokenResponse with JWT and user info
        """
        # Verify Google token
        google_user = AuthService.verify_google_token(token)

        # Get or create user
        user = AuthService.get_or_create_user(db, google_user)

        # Create and return JWT token
        return AuthService.create_token_response(user)

    @staticmethod
    def get_current_user(db: Session, user_id: str) -> User:
        """
        Get current user from user ID.

        Args:
            db: Database session
            user_id: User UUID as string

        Returns:
            User instance

        Raises:
            HTTPException: If user not found
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
