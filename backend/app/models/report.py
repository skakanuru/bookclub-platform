"""Spoiler report model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..database import Base


class SpoilerReport(Base):
    """Spoiler report model for flagging inappropriate comments."""

    __tablename__ = "spoiler_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id", ondelete="CASCADE"), nullable=False)
    reported_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reason = Column(String, nullable=True)
    status = Column(String(20), default="pending", nullable=False)  # 'pending', 'resolved', 'dismissed'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    comment = relationship("Comment", back_populates="reports")
    reporter = relationship("User", back_populates="spoiler_reports")

    __table_args__ = (
        CheckConstraint("status IN ('pending', 'resolved', 'dismissed')", name="check_status"),
    )

    def __repr__(self):
        return f"<SpoilerReport id={self.id} status={self.status}>"
