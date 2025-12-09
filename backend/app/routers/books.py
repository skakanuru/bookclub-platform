"""Book management routes."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from ..schemas.book import (
    BookSearchResult,
    BookResponse,
    GroupBookCreate,
    GroupBookResponse
)
from ..services.book_service import BookService
from ..middleware.auth_middleware import get_current_user
from ..models.user import User

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/search", response_model=List[BookSearchResult])
async def search_books(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    current_user: User = Depends(get_current_user)
):
    """
    Search for books using Open Library API.

    Args:
        q: Search query string
        limit: Maximum number of results (1-50)
        current_user: Current authenticated user

    Returns:
        List of book search results
    """
    return await BookService.search_books(q, limit)


@router.post("/groups/{group_id}/books", response_model=GroupBookResponse, status_code=status.HTTP_201_CREATED)
async def add_book_to_group(
    group_id: UUID,
    book_data: GroupBookCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a book to a group.

    Args:
        group_id: Group UUID
        book_data: Book data (either existing book_id or new book info)
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created group book association
    """
    group_book = BookService.add_book_to_group(
        db,
        group_id,
        current_user.id,
        book_data
    )

    # Create response with book details
    response = GroupBookResponse(
        id=group_book.id,
        group_id=group_book.group_id,
        book_id=group_book.book_id,
        added_by=group_book.added_by,
        added_at=group_book.added_at,
        book=BookResponse.from_orm(group_book.book)
    )
    return response


@router.get("/groups/{group_id}/books", response_model=List[GroupBookResponse])
async def get_group_books(
    group_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all books for a group.

    Args:
        group_id: Group UUID
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of books in the group
    """
    group_books = BookService.get_group_books(db, group_id, current_user.id)

    result = []
    for group_book in group_books:
        response = GroupBookResponse(
            id=group_book.id,
            group_id=group_book.group_id,
            book_id=group_book.book_id,
            added_by=group_book.added_by,
            added_at=group_book.added_at,
            book=BookResponse.from_orm(group_book.book)
        )
        result.append(response)

    return result
