"""Add is_verified to users

Revision ID: a869b94ad100
Revises: 800476e0a8f3
Create Date: 2026-07-03 00:01:08.860744

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a869b94ad100"
down_revision: Union[str, Sequence[str], None] = "800476e0a8f3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "users",
        sa.Column(
            "is_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.alter_column(
        "users",
        "is_verified",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "is_verified")
