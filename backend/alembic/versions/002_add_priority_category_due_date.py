"""Add priority, category, and due_date fields to task table

Revision ID: 002
Revises: 001
Create Date: 2026-01-05 06:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Add priority column with default value 'medium'
    op.add_column('task', sa.Column('priority', sa.String(), nullable=False, server_default='medium'))
    op.create_index('idx_tasks_priority', 'task', ['priority'])

    # Add category column with default value 'other'
    op.add_column('task', sa.Column('category', sa.String(), nullable=False, server_default='other'))
    op.create_index('idx_tasks_category', 'task', ['category'])

    # Add due_date column (nullable)
    op.add_column('task', sa.Column('due_date', sa.DateTime(), nullable=True))
    op.create_index('idx_tasks_due_date', 'task', ['due_date'])


def downgrade():
    # Drop indexes
    op.drop_index('idx_tasks_due_date', table_name='task')
    op.drop_index('idx_tasks_category', table_name='task')
    op.drop_index('idx_tasks_priority', table_name='task')

    # Drop columns
    op.drop_column('task', 'due_date')
    op.drop_column('task', 'category')
    op.drop_column('task', 'priority')