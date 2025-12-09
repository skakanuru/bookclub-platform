"""Progress service for managing reading progress."""
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.progress import UserReadingProgress
from ..models.group import GroupMember
from ..models.book import Book
from ..schemas.progress import ProgressCreate, ProgressUpdate


class ProgressService:
    """Service for handling reading progress operations."""

    @staticmethod
    def create_or_update_progress(
        db: Session,
        user_id: UUID,
        progress_data: ProgressCreate
    ) -> UserReadingProgress:
        """
        Create or update reading progress for a user.

        Args:
            db: Database session
            user_id: User UUID
            progress_data: Progress data

        Returns:
            UserReadingProgress instance

        Raises:
            HTTPException: If validation fails
        """
        # Verify user is member of group
        membership = db.query(GroupMember).filter(
            GroupMember.group_id == progress_data.group_id,
            GroupMember.user_id == user_id
        ).first()
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be a member of this group"
            )

        # Verify book exists
        book = db.query(Book).filter(Book.id == progress_data.book_id).first()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )

        # Validate progress
        if progress_data.current_page > progress_data.total_pages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current page cannot exceed total pages"
            )

        # Calculate progress percentage
        progress_percentage = (
            Decimal(progress_data.current_page) / Decimal(progress_data.total_pages) * 100
        )

        # Check if progress already exists
        existing = db.query(UserReadingProgress).filter(
            UserReadingProgress.user_id == user_id,
            UserReadingProgress.book_id == progress_data.book_id,
            UserReadingProgress.group_id == progress_data.group_id
        ).first()

        if existing:
            # Update existing progress
            existing.current_page = progress_data.current_page
            existing.total_pages = progress_data.total_pages
            existing.progress_percentage = progress_percentage
            db.commit()
            db.refresh(existing)
            return existing
        else:
            # Create new progress
            progress = UserReadingProgress(
                user_id=user_id,
                book_id=progress_data.book_id,
                group_id=progress_data.group_id,
                current_page=progress_data.current_page,
                total_pages=progress_data.total_pages,
                progress_percentage=progress_percentage
            )
            db.add(progress)
            db.commit()
            db.refresh(progress)
            return progress

    @staticmethod
    def update_progress(
        db: Session,
        progress_id: UUID,
        user_id: UUID,
        progress_data: ProgressUpdate
    ) -> UserReadingProgress:
        """
        Update existing reading progress.

        Args:
            db: Database session
            progress_id: Progress UUID
            user_id: User UUID
            progress_data: Progress update data

        Returns:
            Updated UserReadingProgress instance

        Raises:
            HTTPException: If not found or not authorized
        """
        progress = db.query(UserReadingProgress).filter(
            UserReadingProgress.id == progress_id
        ).first()

        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Progress not found"
            )

        if progress.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own progress"
            )

        # Validate progress
        if progress_data.current_page > progress_data.total_pages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current page cannot exceed total pages"
            )

        # Calculate progress percentage
        progress_percentage = (
            Decimal(progress_data.current_page) / Decimal(progress_data.total_pages) * 100
        )

        progress.current_page = progress_data.current_page
        progress.total_pages = progress_data.total_pages
        progress.progress_percentage = progress_percentage
        db.commit()
        db.refresh(progress)
        return progress

    @staticmethod
    def get_user_progress(
        db: Session,
        user_id: UUID,
        book_id: UUID,
        group_id: UUID
    ) -> Optional[UserReadingProgress]:
        """
        Get user's progress for a specific book in a group.

        Args:
            db: Database session
            user_id: User UUID
            book_id: Book UUID
            group_id: Group UUID

        Returns:
            UserReadingProgress instance or None
        """
        return db.query(UserReadingProgress).filter(
            UserReadingProgress.user_id == user_id,
            UserReadingProgress.book_id == book_id,
            UserReadingProgress.group_id == group_id
        ).first()

    @staticmethod
    def get_user_all_progress(
        db: Session,
        user_id: UUID,
        group_id: Optional[UUID] = None
    ) -> List[UserReadingProgress]:
        """
        Get all reading progress for a user, optionally filtered by group.

        Args:
            db: Database session
            user_id: User UUID
            group_id: Optional group UUID to filter by

        Returns:
            List of UserReadingProgress instances
        """
        query = db.query(UserReadingProgress).filter(
            UserReadingProgress.user_id == user_id
        )

        if group_id:
            query = query.filter(UserReadingProgress.group_id == group_id)

        return query.order_by(UserReadingProgress.updated_at.desc()).all()

    @staticmethod
    def get_group_progress(
        db: Session,
        group_id: UUID,
        book_id: UUID,
        user_id: UUID
    ) -> List[UserReadingProgress]:
        """
        Get all members' progress for a book in a group.

        Args:
            db: Database session
            group_id: Group UUID
            book_id: Book UUID
            user_id: User UUID (to verify membership)

        Returns:
            List of UserReadingProgress instances

        Raises:
            HTTPException: If user not member of group
        """
        # Verify user is member of group
        membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        ).first()
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be a member of this group"
            )

        return db.query(UserReadingProgress).filter(
            UserReadingProgress.group_id == group_id,
            UserReadingProgress.book_id == book_id
        ).order_by(UserReadingProgress.progress_percentage.desc()).all()

    @staticmethod
    def delete_progress(
        db: Session,
        progress_id: UUID,
        user_id: UUID
    ) -> None:
        """
        Delete reading progress.

        Args:
            db: Database session
            progress_id: Progress UUID
            user_id: User UUID

        Raises:
            HTTPException: If not found or not authorized
        """
        progress = db.query(UserReadingProgress).filter(
            UserReadingProgress.id == progress_id
        ).first()

        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Progress not found"
            )

        if progress.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own progress"
            )

        db.delete(progress)
        db.commit()
