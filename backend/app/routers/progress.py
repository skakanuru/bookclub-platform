"""Reading progress management routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from ..schemas.progress import (
    ProgressCreate,
    ProgressResponse,
    ProgressUpdate,
    ProgressWithBook
)
from ..services.progress_service import ProgressService
from ..middleware.auth_middleware import get_current_user
from ..models.user import User

router = APIRouter(prefix="/progress", tags=["Reading Progress"])


@router.post("", response_model=ProgressResponse, status_code=status.HTTP_201_CREATED)
async def create_or_update_progress(
    progress_data: ProgressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create or update reading progress for a book in a group.

    Args:
        progress_data: Progress data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created or updated progress
    """
    progress = ProgressService.create_or_update_progress(
        db,
        current_user.id,
        progress_data
    )
    return ProgressResponse.from_orm(progress)


@router.get("", response_model=List[ProgressWithBook])
async def get_my_progress(
    group_id: Optional[UUID] = Query(None, description="Filter by group ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all reading progress for current user, optionally filtered by group.

    Args:
        group_id: Optional group UUID to filter by
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of user's reading progress
    """
    progress_list = ProgressService.get_user_all_progress(
        db,
        current_user.id,
        group_id
    )

    result = []
    for progress in progress_list:
        response = ProgressWithBook(
            id=progress.id,
            user_id=progress.user_id,
            book_id=progress.book_id,
            group_id=progress.group_id,
            current_page=progress.current_page,
            total_pages=progress.total_pages,
            progress_percentage=progress.progress_percentage,
            updated_at=progress.updated_at,
            book_title=progress.book.title,
            book_author=progress.book.author,
            book_cover_url=progress.book.cover_url
        )
        result.append(response)

    return result


@router.get("/groups/{group_id}/books/{book_id}", response_model=ProgressResponse)
async def get_user_book_progress(
    group_id: UUID,
    book_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's progress for a specific book in a group.

    Args:
        group_id: Group UUID
        book_id: Book UUID
        current_user: Current authenticated user
        db: Database session

    Returns:
        User's progress for the book
    """
    progress = ProgressService.get_user_progress(
        db,
        current_user.id,
        book_id,
        group_id
    )

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found for this book"
        )

    return ProgressResponse.from_orm(progress)


@router.get("/groups/{group_id}/books/{book_id}/all", response_model=List[ProgressResponse])
async def get_group_book_progress(
    group_id: UUID,
    book_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all members' progress for a book in a group.

    Args:
        group_id: Group UUID
        book_id: Book UUID
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of all members' progress
    """
    progress_list = ProgressService.get_group_progress(
        db,
        group_id,
        book_id,
        current_user.id
    )

    return [ProgressResponse.from_orm(p) for p in progress_list]


@router.put("/{progress_id}", response_model=ProgressResponse)
async def update_progress(
    progress_id: UUID,
    progress_data: ProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update existing reading progress.

    Args:
        progress_id: Progress UUID
        progress_data: Progress update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated progress
    """
    progress = ProgressService.update_progress(
        db,
        progress_id,
        current_user.id,
        progress_data
    )
    return ProgressResponse.from_orm(progress)


@router.delete("/{progress_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_progress(
    progress_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete reading progress.

    Args:
        progress_id: Progress UUID
        current_user: Current authenticated user
        db: Database session
    """
    ProgressService.delete_progress(db, progress_id, current_user.id)
