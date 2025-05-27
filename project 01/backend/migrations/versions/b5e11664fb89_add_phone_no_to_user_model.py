"""add phone no to user model

Revision ID: b5e11664fb89
Revises: 7b891f2bf045
Create Date: 2025-05-22 11:07:52.915507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5e11664fb89'
down_revision: Union[str, None] = '7b891f2bf045'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
