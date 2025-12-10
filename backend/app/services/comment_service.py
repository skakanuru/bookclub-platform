"""Comment service for managing comments with visibility filtering."""
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from fastapi import HTTPException, status
from ..config import get_settings
from ..models.comment import Comment, CommentLike
from ..models.group import GroupMember
from ..models.progress import UserReadingProgress
from ..schemas.comment import CommentCreate, CommentUpdate

settings = get_settings()


class CommentService:
    """Service for handling comment operations with visibility logic."""

    @staticmethod
    def create_comment(
        db: Session,
        group_id: UUID,
        user_id: UUID,
        comment_data: CommentCreate
    ) -> Comment:
        """
        Create a new comment.

        Args:
            db: Database session
            group_id: Group UUID
            user_id: User UUID
            comment_data: Comment creation data

        Returns:
            Created Comment instance

        Raises:
            HTTPException: If validation fails
        """
        # Validate parent comment if provided
        if comment_data.parent_comment_id:
            parent = db.query(Comment).filter(Comment.id == comment_data.parent_comment_id).first()
            if not parent:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent comment not found")
            if parent.group_id != group_id or parent.book_id != comment_data.book_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parent comment must be in same group and book")

        # Verify user is member of group
        membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        ).first()
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be a member of this group to comment"
            )

        # Validate progress
        if comment_data.progress_page > comment_data.progress_total_pages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Progress page cannot exceed total pages"
            )

        # Calculate progress percentage
        progress_percentage = (
            Decimal(comment_data.progress_page) / Decimal(comment_data.progress_total_pages) * 100
        )

        # Create comment
        comment = Comment(
            group_id=group_id,
            book_id=comment_data.book_id,
            user_id=user_id,
            content=comment_data.content,
            progress_page=comment_data.progress_page,
            progress_total_pages=comment_data.progress_total_pages,
            progress_percentage=progress_percentage,
            parent_comment_id=comment_data.parent_comment_id
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def get_visible_comments(
        db: Session,
        group_id: UUID,
        book_id: UUID,
        user_id: UUID
    ) -> List[Comment]:
        """
        Get comments visible to user based on their reading progress.
        User can only see comments where comment.progress_percentage <= user.progress_percentage - 3.0

        Args:
            db: Database session
            group_id: Group UUID
            book_id: Book UUID
            user_id: User UUID

        Returns:
            List of visible Comment instances
        """
        # Get user's current progress for this book in this group
        user_progress = db.query(UserReadingProgress).filter(
            UserReadingProgress.user_id == user_id,
            UserReadingProgress.book_id == book_id,
            UserReadingProgress.group_id == group_id
        ).first()

        if not user_progress:
            # If user has no progress, they can only see comments at 0% progress
            max_visible_percentage = Decimal("0.00")
        else:
            # User can see comments up to their current progress (no buffer)
            max_visible_percentage = user_progress.progress_percentage

        # Query comments with visibility filter
        comments = db.query(Comment).filter(
            and_(
                Comment.group_id == group_id,
                Comment.book_id == book_id,
                Comment.progress_percentage <= max_visible_percentage
            )
        ).order_by(Comment.progress_percentage, Comment.created_at).all()

        return comments

    @staticmethod
    def get_comments_ahead(
        db: Session,
        group_id: UUID,
        book_id: UUID,
        user_id: UUID
    ) -> List[Comment]:
        """
        Get comments ahead of the user's current visibility (used for notifications).

        Args:
            db: Database session
            group_id: Group UUID
            book_id: Book UUID
            user_id: User UUID

        Returns:
            List of Comment instances that are ahead of the user's visible progress
        """
        # Get user's current progress for this book in this group
        user_progress = db.query(UserReadingProgress).filter(
            UserReadingProgress.user_id == user_id,
            UserReadingProgress.book_id == book_id,
            UserReadingProgress.group_id == group_id
        ).first()

        if not user_progress:
            max_visible_percentage = Decimal("0.00")
        else:
            max_visible_percentage = user_progress.progress_percentage

        comments = db.query(Comment).filter(
            and_(
                Comment.group_id == group_id,
                Comment.book_id == book_id,
                Comment.progress_percentage > max_visible_percentage
            )
        ).order_by(Comment.progress_percentage, Comment.created_at).all()

        return comments

    @staticmethod
    def get_comment_by_id(
        db: Session,
        comment_id: UUID,
        user_id: UUID
    ) -> Comment:
        """
        Get a comment by ID, checking visibility.

        Args:
            db: Database session
            comment_id: Comment UUID
            user_id: User UUID

        Returns:
            Comment instance

        Raises:
            HTTPException: If comment not found or not visible
        """
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )

        # Check if user can see this comment
        user_progress = db.query(UserReadingProgress).filter(
            UserReadingProgress.user_id == user_id,
            UserReadingProgress.book_id == comment.book_id,
            UserReadingProgress.group_id == comment.group_id
        ).first()

        if user_progress:
            max_visible = user_progress.progress_percentage
        else:
            max_visible = Decimal("0.00")

        if comment.progress_percentage > max_visible:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have sufficient reading progress to view this comment"
            )

        return comment

    @staticmethod
    def update_comment(
        db: Session,
        comment_id: UUID,
        user_id: UUID,
        comment_data: CommentUpdate
    ) -> Comment:
        """
        Update a comment (user can only update their own comments).

        Args:
            db: Database session
            comment_id: Comment UUID
            user_id: User UUID
            comment_data: Comment update data

        Returns:
            Updated Comment instance

        Raises:
            HTTPException: If not found or not authorized
        """
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )

        if comment.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own comments"
            )

        comment.content = comment_data.content
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def delete_comment(
        db: Session,
        comment_id: UUID,
        user_id: UUID
    ) -> None:
        """
        Delete a comment (user can only delete their own comments).

        Args:
            db: Database session
            comment_id: Comment UUID
            user_id: User UUID

        Raises:
            HTTPException: If not found or not authorized
        """
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )

        if comment.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own comments"
            )

        db.delete(comment)
        db.commit()

    @staticmethod
    def like_comment(
        db: Session,
        comment_id: UUID,
        user_id: UUID
    ) -> CommentLike:
        """
        Like a comment (user must be able to see it first).

        Args:
            db: Database session
            comment_id: Comment UUID
            user_id: User UUID

        Returns:
            Created CommentLike instance

        Raises:
            HTTPException: If comment not visible or already liked
        """
        # Verify comment is visible to user
        comment = CommentService.get_comment_by_id(db, comment_id, user_id)

        # Check if already liked
        existing = db.query(CommentLike).filter(
            CommentLike.comment_id == comment_id,
            CommentLike.user_id == user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already liked this comment"
            )

        like = CommentLike(
            comment_id=comment_id,
            user_id=user_id
        )
        db.add(like)
        db.commit()
        db.refresh(like)
        return like

    @staticmethod
    def unlike_comment(
        db: Session,
        comment_id: UUID,
        user_id: UUID
    ) -> None:
        """
        Remove like from a comment.

        Args:
            db: Database session
            comment_id: Comment UUID
            user_id: User UUID

        Raises:
            HTTPException: If like not found
        """
        like = db.query(CommentLike).filter(
            CommentLike.comment_id == comment_id,
            CommentLike.user_id == user_id
        ).first()
        if not like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Like not found"
            )

        db.delete(like)
        db.commit()

    @staticmethod
    def get_comment_like_count(db: Session, comment_id: UUID) -> int:
        """Get the number of likes for a comment."""
        return db.query(func.count(CommentLike.id)).filter(
            CommentLike.comment_id == comment_id
        ).scalar()

    @staticmethod
    def user_has_liked_comment(db: Session, comment_id: UUID, user_id: UUID) -> bool:
        """Check if user has liked a comment."""
        return db.query(CommentLike).filter(
            CommentLike.comment_id == comment_id,
            CommentLike.user_id == user_id
        ).first() is not None
