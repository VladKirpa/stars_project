"""sync --autogenerate

Revision ID: f9e09b90e837
Revises: ee7f40dc8b20
Create Date: 2026-02-21 23:40:56.699302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9e09b90e837'
down_revision: Union[str, Sequence[str], None] = 'ee7f40dc8b20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('orders', column_name='created_at', server_default=(sa.text('now()')))

def downgrade() -> None:
    """Downgrade schema."""
    pass
