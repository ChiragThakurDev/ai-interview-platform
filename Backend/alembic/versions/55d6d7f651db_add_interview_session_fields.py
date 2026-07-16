"""add interview session fields

Revision ID: 55d6d7f651db
Revises: f70e321ec907
Create Date: 2026-07-16 05:41:08.283639

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "55d6d7f651db"
down_revision: Union[str, Sequence[str], None] = "f70e321ec907"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "interviews",
        sa.Column(
            "current_question",
            sa.Integer(),
            nullable=False,
            server_default="1",
        ),
    )

    op.add_column(
        "interviews",
        sa.Column(
            "score",
            sa.Integer(),
            nullable=True,
        ),
    )

    # Remove the temporary default after existing rows are updated
    op.alter_column(
        "interviews",
        "current_question",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("interviews", "score")
    op.drop_column("interviews", "current_question")
