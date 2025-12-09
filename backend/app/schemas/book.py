"""Book schemas for request/response validation."""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class BookBase(BaseModel):
    """Base book schema."""
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=255)


class BookCreate(BookBase):
    """Schema for creating a new book."""
    isbn: Optional[str] = Field(None, max_length=20)
    open_library_id: Optional[str] = Field(None, max_length=50)
    cover_url: Optional[str] = None


class BookResponse(BookBase):
    """Schema for book response."""
    id: UUID
    isbn: Optional[str] = None
    open_library_id: Optional[str] = None
    cover_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class BookSearchResult(BaseModel):
    """Schema for book search results from Open Library."""
    title: str
    author: str
    isbn: Optional[str] = None
    open_library_id: Optional[str] = None
    cover_url: Optional[str] = None
    publish_year: Optional[int] = None


class GroupBookCreate(BaseModel):
    """Schema for adding a book to a group."""
    book_id: Optional[UUID] = None  # If book already exists
    # If book doesn't exist, create from these fields:
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, max_length=20)
    open_library_id: Optional[str] = Field(None, max_length=50)
    cover_url: Optional[str] = None


class GroupBookResponse(BaseModel):
    """Schema for group book response."""
    id: UUID
    group_id: UUID
    book_id: UUID
    added_by: Optional[UUID] = None
    added_at: datetime
    book: BookResponse

    class Config:
        from_attributes = True
