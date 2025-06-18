"""rooms migration

Revision ID: 3c8435762e7d
Revises: 1bd84586932e
Create Date: 2025-06-18 16:39:10.791303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3c8435762e7d'
down_revision: Union[str, None] = '1bd84586932e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hotel_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('rooms')
