"""Book models."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..database import Base


class Book(Base):
    """Book model."""

    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(20), nullable=True, index=True)
    open_library_id = Column(String(50), nullable=True, index=True)
    cover_url = Column(String, nullable=True)  # Hotlinked from Open Library
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    group_books = relationship("GroupBook", back_populates="book", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="book", cascade="all, delete-orphan")
    reading_progress = relationship("UserReadingProgress", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"


class GroupBook(Base):
    """Association between groups and books."""

    __tablename__ = "group_books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    added_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    added_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    group = relationship("Group", back_populates="books")
    book = relationship("Book", back_populates="group_books")
    added_by_user = relationship("User", foreign_keys=[added_by])

    def __repr__(self):
        return f"<GroupBook group_id={self.group_id} book_id={self.book_id}>"
