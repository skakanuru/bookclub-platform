"""Authentication schemas for request/response validation."""
from pydantic import BaseModel, Field
from .user import UserResponse


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class GoogleAuthRequest(BaseModel):
    """Schema for Google OAuth authentication request."""
    token: str = Field(..., min_length=1, description="Google ID token")


class GoogleUserInfo(BaseModel):
    """Schema for Google user information."""
    google_id: str
    email: str
    name: str
    avatar_url: str
