"""Group management routes."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from ..schemas.group import (
    GroupCreate,
    GroupResponse,
    GroupUpdate,
    GroupJoinRequest,
    GroupMemberResponse
)
from ..services.group_service import GroupService
from ..middleware.auth_middleware import get_current_user
from ..models.user import User
from ..models.group import GroupMember

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post("", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    group_data: GroupCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new group.

    Args:
        group_data: Group creation data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created group information
    """
    group = GroupService.create_group(db, current_user.id, group_data)

    # Add member count
    response = GroupResponse.from_orm(group)
    response.member_count = len(group.members)
    return response


@router.get("", response_model=List[GroupResponse])
async def get_my_groups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all groups the current user is a member of.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of groups
    """
    groups = GroupService.get_user_groups(db, current_user.id)

    # Add member counts
    result = []
    for group in groups:
        response = GroupResponse.from_orm(group)
        response.member_count = len(group.members)
        result.append(response)

    return result


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific group by ID.

    Args:
        group_id: Group UUID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Group information
    """
    group = GroupService.get_group_by_id(db, group_id, current_user.id)

    # Add member count and members list
    response = GroupResponse.from_orm(group)
    response.member_count = len(group.members)

    # Add member details
    members = []
    for member in group.members:
        member_response = GroupMemberResponse(
            id=member.id,
            user_id=member.user_id,
            group_id=member.group_id,
            role=member.role,
            joined_at=member.joined_at,
            user_name=member.user.name,
            user_avatar_url=member.user.avatar_url
        )
        members.append(member_response)
    response.members = members

    return response


@router.put("/{group_id}", response_model=GroupResponse)
async def update_group(
    group_id: UUID,
    group_data: GroupUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a group (admin only).

    Args:
        group_id: Group UUID
        group_data: Group update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated group information
    """
    group = GroupService.update_group(db, group_id, current_user.id, group_data)

    response = GroupResponse.from_orm(group)
    response.member_count = len(group.members)
    return response


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a group (admin only).

    Args:
        group_id: Group UUID
        current_user: Current authenticated user
        db: Database session
    """
    GroupService.delete_group(db, group_id, current_user.id)


@router.post("/join", response_model=GroupResponse)
async def join_group(
    join_request: GroupJoinRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Join a group using an invite code.

    Args:
        join_request: Join request with invite code
        current_user: Current authenticated user
        db: Database session

    Returns:
        Joined group information
    """
    group = GroupService.join_group(db, current_user.id, join_request.invite_code)

    response = GroupResponse.from_orm(group)
    response.member_count = len(group.members)
    return response


@router.post("/{group_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
async def leave_group(
    group_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Leave a group.

    Args:
        group_id: Group UUID
        current_user: Current authenticated user
        db: Database session
    """
    GroupService.leave_group(db, group_id, current_user.id)


@router.get("/{group_id}/members", response_model=List[GroupMemberResponse])
async def get_group_members(
    group_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all members of a group.

    Args:
        group_id: Group UUID
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of group members
    """
    members = GroupService.get_group_members(db, group_id, current_user.id)

    result = []
    for member in members:
        member_response = GroupMemberResponse(
            id=member.id,
            user_id=member.user_id,
            group_id=member.group_id,
            role=member.role,
            joined_at=member.joined_at,
            user_name=member.user.name,
            user_avatar_url=member.user.avatar_url
        )
        result.append(member_response)

    return result


@router.delete("/{group_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    group_id: UUID,
    member_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a member from a group (admin only).

    Args:
        group_id: Group UUID
        member_id: Member user UUID to remove
        current_user: Current authenticated user
        db: Database session
    """
    GroupService.remove_member(db, group_id, current_user.id, member_id)


@router.post("/{group_id}/members/{member_id}/promote", response_model=GroupMemberResponse)
async def promote_member(
    group_id: UUID,
    member_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Promote a member to admin (admin only).

    Args:
        group_id: Group UUID
        member_id: Member user UUID to promote
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated member information
    """
    member = GroupService.promote_to_admin(db, group_id, current_user.id, member_id)

    return GroupMemberResponse(
        id=member.id,
        user_id=member.user_id,
        group_id=member.group_id,
        role=member.role,
        joined_at=member.joined_at,
        user_name=member.user.name,
        user_avatar_url=member.user.avatar_url
    )
