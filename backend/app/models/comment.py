"""Comment models."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Numeric, CheckConstraint, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import text
from ..database import Base


class Comment(Base):
    """Comment model for book discussions."""

    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    progress_page = Column(Integer, nullable=False)
    progress_total_pages = Column(Integer, nullable=False)
    # Computed column: progress_percentage = (progress_page / progress_total_pages) * 100
    progress_percentage = Column(
        Numeric(5, 2),
        nullable=False,
        server_default=text("0.00")
    )
    parent_comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    group = relationship("Group", back_populates="comments")
    book = relationship("Book", back_populates="comments")
    user = relationship("User", back_populates="comments")
    likes = relationship("CommentLike", back_populates="comment", cascade="all, delete-orphan")
    reports = relationship("SpoilerReport", back_populates="comment", cascade="all, delete-orphan")
    parent = relationship("Comment", remote_side=[id], back_populates="replies")
    replies = relationship(
        "Comment",
        back_populates="parent",
        cascade="all, delete-orphan",
        single_parent=True
    )

    __table_args__ = (
        CheckConstraint("LENGTH(content) >= 1 AND LENGTH(content) <= 1000", name="check_content_length"),
        CheckConstraint("progress_page >= 0", name="check_progress_page_positive"),
        CheckConstraint("progress_total_pages > 0", name="check_progress_total_pages_positive"),
        CheckConstraint("progress_page <= progress_total_pages", name="check_progress_page_not_exceeds_total"),
        Index("idx_comments_progress", "book_id", "group_id", "progress_percentage"),
    )

    def __repr__(self):
        return f"<Comment id={self.id} progress={self.progress_percentage}%>"


class CommentLike(Base):
    """Comment like/reaction model."""

    __tablename__ = "comment_likes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    comment = relationship("Comment", back_populates="likes")
    user = relationship("User", back_populates="comment_likes")

    __table_args__ = (
        UniqueConstraint("comment_id", "user_id", name="unique_comment_user_like"),
    )

    def __repr__(self):
        return f"<CommentLike comment_id={self.comment_id} user_id={self.user_id}>"
