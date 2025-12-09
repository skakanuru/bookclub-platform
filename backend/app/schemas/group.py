"""Group schemas for request/response validation."""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field


class GroupBase(BaseModel):
    """Base group schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class GroupCreate(GroupBase):
    """Schema for creating a new group."""
    pass


class GroupUpdate(BaseModel):
    """Schema for updating group information."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class GroupMemberResponse(BaseModel):
    """Schema for group member response."""
    id: UUID
    user_id: UUID
    group_id: UUID
    role: str  # 'admin' or 'member'
    joined_at: datetime
    user_name: str
    user_avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


class GroupResponse(GroupBase):
    """Schema for group response."""
    id: UUID
    invite_code: str
    created_by: Optional[UUID] = None
    created_at: datetime
    member_count: Optional[int] = None
    members: Optional[List[GroupMemberResponse]] = None

    class Config:
        from_attributes = True


class GroupJoinRequest(BaseModel):
    """Schema for joining a group via invite code."""
    invite_code: str = Field(..., min_length=1, max_length=12)
