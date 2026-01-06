"""Initial task table

Revision ID: 001
Revises:
Create Date: 2026-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create the tasks table
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.CheckConstraint('length(title) >= 1 AND length(title) <= 200', name='chk_tasks_title_length'),
        sa.CheckConstraint('length(description) <= 1000', name='chk_tasks_description_length'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('idx_tasks_user_id', 'task', ['user_id'])
    op.create_index('idx_tasks_completed', 'task', ['completed'])
    op.create_index('idx_tasks_created_at', 'task', ['created_at'])


def downgrade():
    # Drop indexes
    op.drop_index('idx_tasks_user_id', table_name='task')
    op.drop_index('idx_tasks_completed', table_name='task')
    op.drop_index('idx_tasks_created_at', table_name='task')

    # Drop the tasks table
    op.drop_table('task')