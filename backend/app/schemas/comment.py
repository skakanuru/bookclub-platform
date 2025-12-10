"""Comment schemas for request/response validation."""
from datetime import datetime
from typing import Optional
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    """Base comment schema."""
    content: str = Field(..., min_length=1, max_length=1000)


class CommentCreate(CommentBase):
    """Schema for creating a new comment."""
    book_id: UUID
    progress_page: int = Field(..., ge=0)
    progress_total_pages: int = Field(..., gt=0)
    parent_comment_id: Optional[UUID] = None


class CommentUpdate(BaseModel):
    """Schema for updating a comment."""
    content: str = Field(..., min_length=1, max_length=1000)


class CommentLikeResponse(BaseModel):
    """Schema for comment like response."""
    id: UUID
    comment_id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class CommentResponse(CommentBase):
    """Schema for comment response."""
    id: UUID
    group_id: UUID
    book_id: UUID
    user_id: UUID
    progress_page: int
    progress_total_pages: int
    progress_percentage: Decimal
    parent_comment_id: Optional[UUID] = None
    created_at: datetime
    like_count: Optional[int] = None
    user_has_liked: Optional[bool] = None

    class Config:
        from_attributes = True


class CommentWithUser(CommentResponse):
    """Schema for comment with user information."""
    user_name: str
    user_avatar_url: Optional[str] = None

    class Config:
        from_attributes = True
