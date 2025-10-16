"""Add CZK currency

Revision ID: 78c66a9f91d5
Revises: 143409f9beb3
Create Date: 2025-10-12 21:33:35.200509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '78c66a9f91d5'
down_revision: Union[str, None] = '143409f9beb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add CZK to the currency enum
    op.execute("ALTER TYPE currency ADD VALUE IF NOT EXISTS 'CZK'")


def downgrade() -> None:
    # PostgreSQL doesn't support removing enum values directly
    # You would need to recreate the enum type without CZK
    # For now, we'll leave this as a no-op since removing enum values is complex
    pass
