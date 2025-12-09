"""Group models."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..database import Base


class Group(Base):
    """Group model for book clubs."""

    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    invite_code = Column(String(12), unique=True, nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    creator = relationship("User", back_populates="created_groups", foreign_keys=[created_by])
    members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")
    books = relationship("GroupBook", back_populates="group", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="group", cascade="all, delete-orphan")
    reading_progress = relationship("UserReadingProgress", back_populates="group", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Group {self.name} ({self.invite_code})>"


class GroupMember(Base):
    """Group membership model."""

    __tablename__ = "group_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), default="member", nullable=False)  # 'admin' or 'member'
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    group = relationship("Group", back_populates="members")
    user = relationship("User", back_populates="group_memberships")

    __table_args__ = (
        CheckConstraint("role IN ('admin', 'member')", name="check_role"),
    )

    def __repr__(self):
        return f"<GroupMember user_id={self.user_id} group_id={self.group_id} role={self.role}>"
