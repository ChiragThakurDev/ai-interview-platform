"""add permissions to api_keys

Revision ID: 3e3d3e32b27c
Revises: d8cf25394a92
Create Date: 2026-07-05 10:49:43.209870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3e3d3e32b27c"
down_revision: Union[str, Sequence[str], None] = "d8cf25394a92"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "api_keys",
        sa.Column(
            "permissions",
            sa.String(length=255),
            nullable=False,
            server_default="read",
        ),
    )

    op.alter_column(
        "api_keys",
        "permissions",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("api_keys", "permissions")
