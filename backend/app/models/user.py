"""User model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..database import Base


class User(Base):
    """User model for storing user account information."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    google_id = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    avatar_url = Column(String, nullable=True)  # Google avatar initially, then custom upload
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    group_memberships = relationship("GroupMember", back_populates="user", cascade="all, delete-orphan")
    created_groups = relationship("Group", back_populates="creator", foreign_keys="Group.created_by")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    reading_progress = relationship("UserReadingProgress", back_populates="user", cascade="all, delete-orphan")
    comment_likes = relationship("CommentLike", back_populates="user", cascade="all, delete-orphan")
    spoiler_reports = relationship("SpoilerReport", back_populates="reporter", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"
