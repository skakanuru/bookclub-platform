"""Group service for managing groups and memberships."""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from ..config import get_settings
from ..models.group import Group, GroupMember
from ..models.user import User
from ..schemas.group import GroupCreate, GroupUpdate
from ..utils.invite_code import generate_invite_code

settings = get_settings()


class GroupService:
    """Service for handling group operations."""

    @staticmethod
    def create_group(
        db: Session,
        user_id: UUID,
        group_data: GroupCreate
    ) -> Group:
        """
        Create a new group with the user as admin.

        Args:
            db: Database session
            user_id: User UUID (will be group creator and admin)
            group_data: Group creation data

        Returns:
            Created Group instance
        """
        # Generate unique invite code
        invite_code = generate_invite_code()
        while db.query(Group).filter(Group.invite_code == invite_code).first():
            invite_code = generate_invite_code()

        # Create group
        group = Group(
            name=group_data.name,
            description=group_data.description,
            invite_code=invite_code,
            created_by=user_id
        )
        db.add(group)
        db.flush()  # Flush to get group ID

        # Add creator as admin member
        membership = GroupMember(
            group_id=group.id,
            user_id=user_id,
            role="admin"
        )
        db.add(membership)
        db.commit()
        db.refresh(group)
        return group

    @staticmethod
    def get_group_by_id(
        db: Session,
        group_id: UUID,
        user_id: UUID
    ) -> Group:
        """
        Get a group by ID (user must be a member).

        Args:
            db: Database session
            group_id: Group UUID
            user_id: User UUID

        Returns:
            Group instance

        Raises:
            HTTPException: If group not found or user not a member
        """
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )

        # Verify user is member
        membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        ).first()
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this group"
            )

        return group

    @staticmethod
    def get_user_groups(db: Session, user_id: UUID) -> List[Group]:
        """
        Get all groups a user is a member of.

        Args:
            db: Database session
            user_id: User UUID

        Returns:
            List of Group instances
        """
        return db.query(Group).join(GroupMember).filter(
            GroupMember.user_id == user_id
        ).all()

    @staticmethod
    def update_group(
        db: Session,
        group_id: UUID,
        user_id: UUID,
        group_data: GroupUpdate
    ) -> Group:
        """
        Update a group (user must be admin).

        Args:
            db: Database session
            group_id: Group UUID
            user_id: User UUID
            group_data: Group update data

        Returns:
            Updated Group instance

        Raises:
            HTTPException: If not found or not authorized
        """
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )

        # Verify user is admin
        membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id,
            GroupMember.role == "admin"
        ).first()
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only group admins can update group information"
            )

        # Update fields
        if group_data.name is not None:
            group.name = group_data.name
        if group_data.description is not None:
            group.description = group_data.description

        db.commit()
        db.refresh(group)
        return group

    @staticmethod
    def delete_group(
        db: Session,
        group_id: UUID,
        user_id: UUID
    ) -> None:
        """
        Delete a group (user must be admin).

        Args:
            db: Database session
            group_id: Group UUID
            user_id: User UUID

        Raises:
            HTTPException: If not found or not authorized
        """
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )

        # Verify user is admin
        membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id,
            GroupMember.role == "admin"
        ).first()
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only group admins can delete the group"
            )

        db.delete(group)
        db.commit()

    @staticmethod
    def join_group(
        db: Session,
        user_id: UUID,
        invite_code: str
    ) -> Group:
        """
        Join a group using an invite code.

        Args:
            db: Database session
            user_id: User UUID
            invite_code: Group invite code

        Returns:
            Group instance

        Raises:
            HTTPException: If invalid code or group full
        """
        # Find group by invite code
        group = db.query(Group).filter(Group.invite_code == invite_code).first()
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid invite code"
            )

        # Check if already a member
        existing = db.query(GroupMember).filter(
            GroupMember.group_id == group.id,
            GroupMember.user_id == user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already a member of this group"
            )

        # Check member limit
        member_count = db.query(func.count(GroupMember.id)).filter(
            GroupMember.group_id == group.id
        ).scalar()
        if member_count >= settings.max_group_members:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Group is full (maximum {settings.max_group_members} members)"
            )

        # Add user as member
        membership = GroupMember(
            group_id=group.id,
            user_id=user_id,
            role="member"
        )
        db.add(membership)
        db.commit()
        db.refresh(group)
        return group

    @staticmethod
    def leave_group(
        db: Session,
        group_id: UUID,
        user_id: UUID
    ) -> None:
        """
        Leave a group.

        Args:
            db: Database session
            group_id: Group UUID
            user_id: User UUID

        Raises:
            HTTPException: If not a member or last admin
        """
        membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        ).first()
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You are not a member of this group"
            )

        # If user is admin, check if they're the last admin
        if membership.role == "admin":
            admin_count = db.query(func.count(GroupMember.id)).filter(
                GroupMember.group_id == group_id,
                GroupMember.role == "admin"
            ).scalar()
            if admin_count <= 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot leave: you are the last admin. Transfer admin rights or delete the group."
                )

        db.delete(membership)
        db.commit()

    @staticmethod
    def get_group_members(
        db: Session,
        group_id: UUID,
        user_id: UUID
    ) -> List[GroupMember]:
        """
        Get all members of a group.

        Args:
            db: Database session
            group_id: Group UUID
            user_id: User UUID (to verify membership)

        Returns:
            List of GroupMember instances

        Raises:
            HTTPException: If user not a member
        """
        # Verify user is member
        membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        ).first()
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be a member of this group"
            )

        return db.query(GroupMember).filter(
            GroupMember.group_id == group_id
        ).all()

    @staticmethod
    def remove_member(
        db: Session,
        group_id: UUID,
        user_id: UUID,
        member_id: UUID
    ) -> None:
        """
        Remove a member from a group (admin only).

        Args:
            db: Database session
            group_id: Group UUID
            user_id: User UUID (must be admin)
            member_id: Member UUID to remove

        Raises:
            HTTPException: If not authorized or member not found
        """
        # Verify user is admin
        admin_membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id,
            GroupMember.role == "admin"
        ).first()
        if not admin_membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only group admins can remove members"
            )

        # Find member to remove
        member = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == member_id
        ).first()
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found in this group"
            )

        # Don't allow removing last admin
        if member.role == "admin":
            admin_count = db.query(func.count(GroupMember.id)).filter(
                GroupMember.group_id == group_id,
                GroupMember.role == "admin"
            ).scalar()
            if admin_count <= 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot remove the last admin"
                )

        db.delete(member)
        db.commit()

    @staticmethod
    def promote_to_admin(
        db: Session,
        group_id: UUID,
        user_id: UUID,
        member_id: UUID
    ) -> GroupMember:
        """
        Promote a member to admin (admin only).

        Args:
            db: Database session
            group_id: Group UUID
            user_id: User UUID (must be admin)
            member_id: Member UUID to promote

        Returns:
            Updated GroupMember instance

        Raises:
            HTTPException: If not authorized or member not found
        """
        # Verify user is admin
        admin_membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id,
            GroupMember.role == "admin"
        ).first()
        if not admin_membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only group admins can promote members"
            )

        # Find member to promote
        member = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == member_id
        ).first()
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found in this group"
            )

        if member.role == "admin":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member is already an admin"
            )

        member.role = "admin"
        db.commit()
        db.refresh(member)
        return member
