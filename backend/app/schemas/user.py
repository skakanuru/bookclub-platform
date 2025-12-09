"""User schemas for request/response validation."""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a new user."""
    google_id: str = Field(..., min_length=1, max_length=255)
    avatar_url: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: UUID
    avatar_url: Optional[str] = None
    created_at: datetime
    last_login: datetime

    class Config:
        from_attributes = True


class UserPublic(BaseModel):
    """Public user information (for displaying in comments, groups, etc)."""
    id: UUID
    name: str
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True
