"""Reading progress model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Numeric, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import text
from ..database import Base


class UserReadingProgress(Base):
    """Track user's reading progress for a book in a group."""

    __tablename__ = "user_reading_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    current_page = Column(Integer, nullable=False)
    total_pages = Column(Integer, nullable=False)
    # Computed column: progress_percentage = (current_page / total_pages) * 100
    progress_percentage = Column(
        Numeric(5, 2),
        nullable=False,
        server_default=text("0.00")
    )
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="reading_progress")
    book = relationship("Book", back_populates="reading_progress")
    group = relationship("Group", back_populates="reading_progress")

    __table_args__ = (
        CheckConstraint("current_page >= 0", name="check_current_page_positive"),
        CheckConstraint("total_pages > 0", name="check_total_pages_positive"),
        CheckConstraint("current_page <= total_pages", name="check_current_page_not_exceeds_total"),
        UniqueConstraint("user_id", "book_id", "group_id", name="unique_user_book_group_progress"),
    )

    def __repr__(self):
        return f"<UserReadingProgress user_id={self.user_id} book_id={self.book_id} progress={self.progress_percentage}%>"
