"""v1 create table Deal

Revision ID: 695b1089fd34
Revises: 
Create Date: 2025-05-25 16:24:53.692094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '695b1089fd34'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'deals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('money', sa.Integer(), nullable=True),
        sa.Column('profit', sa.Boolean(), server_default='false', nullable=True),
        sa.Column('date', sa.Date(), server_default=text('CURRENT_DATE'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('deals')
