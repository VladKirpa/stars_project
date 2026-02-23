"""create orders tasks tasks_comletion tables

Revision ID: 1891f9f150a9
Revises: 6b0496b89421
Create Date: 2026-02-20 17:33:07.135496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1891f9f150a9'
down_revision: Union[str, Sequence[str], None] = '6b0496b89421'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
