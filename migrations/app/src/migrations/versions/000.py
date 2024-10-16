"""Create tables

Revision ID: 000
Revises:
Create Date: 2023-12-09 10:00:00

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table('users',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('referrer_id', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('referrer_codes',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('code', sa.String(), nullable=False),
                    sa.Column('end_date', sa.Date(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id']),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('referral_codes')
    op.drop_table('users')
