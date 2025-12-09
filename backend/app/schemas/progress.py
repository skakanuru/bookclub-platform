"""Reading progress schemas for request/response validation."""
from datetime import datetime
from typing import Optional
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field


class ProgressBase(BaseModel):
    """Base progress schema."""
    current_page: int = Field(..., ge=0)
    total_pages: int = Field(..., gt=0)


class ProgressCreate(ProgressBase):
    """Schema for creating reading progress."""
    book_id: UUID
    group_id: UUID


class ProgressUpdate(ProgressBase):
    """Schema for updating reading progress."""
    pass


class ProgressResponse(ProgressBase):
    """Schema for progress response."""
    id: UUID
    user_id: UUID
    book_id: UUID
    group_id: UUID
    progress_percentage: Decimal
    updated_at: datetime

    class Config:
        from_attributes = True


class ProgressWithBook(ProgressResponse):
    """Schema for progress with book information."""
    book_title: str
    book_author: str
    book_cover_url: Optional[str] = None

    class Config:
        from_attributes = True
