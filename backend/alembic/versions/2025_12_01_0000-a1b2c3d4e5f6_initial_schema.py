"""initial schema

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2025-12-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # users
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('google_id', sa.String(255), unique=True, nullable=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=True),
        sa.Column('avatar_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_login', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_users_google_id', 'users', ['google_id'])
    op.create_index('ix_users_email', 'users', ['email'])

    # groups
    op.create_table(
        'groups',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('invite_code', sa.String(12), unique=True, nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_groups_invite_code', 'groups', ['invite_code'])

    # group_members
    op.create_table(
        'group_members',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('group_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(20), nullable=False, server_default='member'),
        sa.Column('joined_at', sa.DateTime(), nullable=False),
        sa.CheckConstraint("role IN ('admin', 'member')", name='check_role'),
    )

    # books
    op.create_table(
        'books',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('author', sa.String(255), nullable=False),
        sa.Column('isbn', sa.String(20), nullable=True),
        sa.Column('open_library_id', sa.String(50), nullable=True),
        sa.Column('cover_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_books_isbn', 'books', ['isbn'])
    op.create_index('ix_books_open_library_id', 'books', ['open_library_id'])

    # group_books
    op.create_table(
        'group_books',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('group_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False),
        sa.Column('book_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('books.id', ondelete='CASCADE'), nullable=False),
        sa.Column('added_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('added_at', sa.DateTime(), nullable=False),
    )

    # comments (includes parent_comment_id from the start)
    op.create_table(
        'comments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('group_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False),
        sa.Column('book_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('books.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('progress_page', sa.Integer(), nullable=False),
        sa.Column('progress_total_pages', sa.Integer(), nullable=False),
        sa.Column('progress_percentage', sa.Numeric(5, 2), nullable=False, server_default='0.00'),
        sa.Column('parent_comment_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('comments.id', ondelete='CASCADE'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.CheckConstraint("LENGTH(content) >= 1 AND LENGTH(content) <= 1000", name='check_content_length'),
        sa.CheckConstraint("progress_page >= 0", name='check_progress_page_positive'),
        sa.CheckConstraint("progress_total_pages > 0", name='check_progress_total_pages_positive'),
        sa.CheckConstraint("progress_page <= progress_total_pages", name='check_progress_page_not_exceeds_total'),
    )
    op.create_index('idx_comments_progress', 'comments', ['book_id', 'group_id', 'progress_percentage'])

    # comment_likes
    op.create_table(
        'comment_likes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('comment_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('comments.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('comment_id', 'user_id', name='unique_comment_user_like'),
    )

    # user_reading_progress
    op.create_table(
        'user_reading_progress',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('book_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('books.id', ondelete='CASCADE'), nullable=False),
        sa.Column('group_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False),
        sa.Column('current_page', sa.Integer(), nullable=False),
        sa.Column('total_pages', sa.Integer(), nullable=False),
        sa.Column('progress_percentage', sa.Numeric(5, 2), nullable=False, server_default='0.00'),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.CheckConstraint("current_page >= 0", name='check_current_page_positive'),
        sa.CheckConstraint("total_pages > 0", name='check_total_pages_positive'),
        sa.CheckConstraint("current_page <= total_pages", name='check_current_page_not_exceeds_total'),
        sa.UniqueConstraint('user_id', 'book_id', 'group_id', name='unique_user_book_group_progress'),
    )

    # spoiler_reports
    op.create_table(
        'spoiler_reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('comment_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('comments.id', ondelete='CASCADE'), nullable=False),
        sa.Column('reported_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('reason', sa.String(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.CheckConstraint("status IN ('pending', 'resolved', 'dismissed')", name='check_status'),
    )


def downgrade() -> None:
    op.drop_table('spoiler_reports')
    op.drop_table('user_reading_progress')
    op.drop_table('comment_likes')
    op.drop_index('idx_comments_progress', 'comments')
    op.drop_table('comments')
    op.drop_table('group_books')
    op.drop_index('ix_books_open_library_id', 'books')
    op.drop_index('ix_books_isbn', 'books')
    op.drop_table('books')
    op.drop_table('group_members')
    op.drop_index('ix_groups_invite_code', 'groups')
    op.drop_table('groups')
    op.drop_index('ix_users_email', 'users')
    op.drop_index('ix_users_google_id', 'users')
    op.drop_table('users')
