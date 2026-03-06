"""merge branches

Revision ID: 35ad4877f882
Revises: 0dac8c41f901
Create Date: 2026-02-25 19:47:55.051328

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35ad4877f882'
down_revision: Union[str, Sequence[str], None] = '0dac8c41f901'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
