"""add comment reply parent column

Revision ID: b3e7020cc23c
Revises: a1b2c3d4e5f6
Create Date: 2025-12-09 18:22:20.907809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3e7020cc23c'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # parent_comment_id is already included in the initial schema migration.
    pass


def downgrade() -> None:
    pass
