"""Comment management routes with visibility filtering."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from ..schemas.comment import (
    CommentCreate,
    CommentResponse,
    CommentWithUser,
    CommentUpdate,
    CommentLikeResponse
)
from ..services.comment_service import CommentService
from ..middleware.auth_middleware import get_current_user
from ..models.user import User

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/groups/{group_id}/comments", response_model=CommentWithUser, status_code=status.HTTP_201_CREATED)
async def create_comment(
    group_id: UUID,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new comment in a group.

    Args:
        group_id: Group UUID
        comment_data: Comment creation data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created comment with user information
    """
    comment = CommentService.create_comment(
        db,
        group_id,
        current_user.id,
        comment_data
    )

    # Get like count and user liked status
    like_count = CommentService.get_comment_like_count(db, comment.id)
    user_has_liked = CommentService.user_has_liked_comment(db, comment.id, current_user.id)

    # Create response with user info
    response = CommentWithUser(
        id=comment.id,
        group_id=comment.group_id,
        book_id=comment.book_id,
        user_id=comment.user_id,
        content=comment.content,
        progress_page=comment.progress_page,
        progress_total_pages=comment.progress_total_pages,
        progress_percentage=comment.progress_percentage,
        created_at=comment.created_at,
        like_count=like_count,
        user_has_liked=user_has_liked,
        user_name=current_user.name,
        user_avatar_url=current_user.avatar_url
    )
    return response


@router.get("/groups/{group_id}/books/{book_id}/comments", response_model=List[CommentWithUser])
async def get_book_comments(
    group_id: UUID,
    book_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all visible comments for a book in a group.
    Visibility is based on user's reading progress with 3% buffer.

    Args:
        group_id: Group UUID
        book_id: Book UUID
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of visible comments with user information
    """
    comments = CommentService.get_visible_comments(
        db,
        group_id,
        book_id,
        current_user.id
    )

    result = []
    for comment in comments:
        like_count = CommentService.get_comment_like_count(db, comment.id)
        user_has_liked = CommentService.user_has_liked_comment(db, comment.id, current_user.id)

        response = CommentWithUser(
            id=comment.id,
            group_id=comment.group_id,
            book_id=comment.book_id,
            user_id=comment.user_id,
            content=comment.content,
            progress_page=comment.progress_page,
            progress_total_pages=comment.progress_total_pages,
            progress_percentage=comment.progress_percentage,
            created_at=comment.created_at,
            like_count=like_count,
            user_has_liked=user_has_liked,
            user_name=comment.user.name,
            user_avatar_url=comment.user.avatar_url
        )
        result.append(response)

    return result


@router.get("/comments/{comment_id}", response_model=CommentWithUser)
async def get_comment(
    comment_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific comment by ID (with visibility check).

    Args:
        comment_id: Comment UUID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Comment with user information
    """
    comment = CommentService.get_comment_by_id(db, comment_id, current_user.id)

    like_count = CommentService.get_comment_like_count(db, comment.id)
    user_has_liked = CommentService.user_has_liked_comment(db, comment.id, current_user.id)

    response = CommentWithUser(
        id=comment.id,
        group_id=comment.group_id,
        book_id=comment.book_id,
        user_id=comment.user_id,
        content=comment.content,
        progress_page=comment.progress_page,
        progress_total_pages=comment.progress_total_pages,
        progress_percentage=comment.progress_percentage,
        created_at=comment.created_at,
        like_count=like_count,
        user_has_liked=user_has_liked,
        user_name=comment.user.name,
        user_avatar_url=comment.user.avatar_url
    )
    return response


@router.put("/comments/{comment_id}", response_model=CommentWithUser)
async def update_comment(
    comment_id: UUID,
    comment_data: CommentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a comment (user can only update their own comments).

    Args:
        comment_id: Comment UUID
        comment_data: Comment update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated comment with user information
    """
    comment = CommentService.update_comment(
        db,
        comment_id,
        current_user.id,
        comment_data
    )

    like_count = CommentService.get_comment_like_count(db, comment.id)
    user_has_liked = CommentService.user_has_liked_comment(db, comment.id, current_user.id)

    response = CommentWithUser(
        id=comment.id,
        group_id=comment.group_id,
        book_id=comment.book_id,
        user_id=comment.user_id,
        content=comment.content,
        progress_page=comment.progress_page,
        progress_total_pages=comment.progress_total_pages,
        progress_percentage=comment.progress_percentage,
        created_at=comment.created_at,
        like_count=like_count,
        user_has_liked=user_has_liked,
        user_name=current_user.name,
        user_avatar_url=current_user.avatar_url
    )
    return response


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a comment (user can only delete their own comments).

    Args:
        comment_id: Comment UUID
        current_user: Current authenticated user
        db: Database session
    """
    CommentService.delete_comment(db, comment_id, current_user.id)


@router.post("/comments/{comment_id}/like", response_model=CommentLikeResponse, status_code=status.HTTP_201_CREATED)
async def like_comment(
    comment_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Like a comment.

    Args:
        comment_id: Comment UUID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created comment like
    """
    like = CommentService.like_comment(db, comment_id, current_user.id)
    return CommentLikeResponse.from_orm(like)


@router.delete("/comments/{comment_id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_comment(
    comment_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove like from a comment.

    Args:
        comment_id: Comment UUID
        current_user: Current authenticated user
        db: Database session
    """
    CommentService.unlike_comment(db, comment_id, current_user.id)
