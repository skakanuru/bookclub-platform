"""Authentication schemas for request/response validation."""
from pydantic import BaseModel, Field, EmailStr
from .user import UserResponse


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class EmailPasswordRegister(BaseModel):
    """Schema for email/password registration."""
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")
    name: str = Field(..., min_length=1, description="Full name")


class EmailPasswordLogin(BaseModel):
    """Schema for email/password login."""
    email: EmailStr
    password: str


class GoogleAuthRequest(BaseModel):
    """Schema for Google OAuth authentication request."""
    token: str = Field(..., min_length=1, description="Google ID token")


class GoogleUserInfo(BaseModel):
    """Schema for Google user information."""
    google_id: str
    email: str
    name: str
    avatar_url: str
