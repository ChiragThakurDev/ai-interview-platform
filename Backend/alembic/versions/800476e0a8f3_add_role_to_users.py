"""Add role to users

Revision ID: 800476e0a8f3
Revises: 4ed6252fb6bf
Create Date: 2026-07-01 03:54:23.141878

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "800476e0a8f3"
down_revision: Union[str, Sequence[str], None] = "4ed6252fb6bf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(length=20),
            nullable=False,
            server_default="user",
        ),
    )

    # Remove the server default after existing rows are updated
    op.alter_column(
        "users",
        "role",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "role")
