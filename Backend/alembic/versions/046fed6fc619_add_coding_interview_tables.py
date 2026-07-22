"""add coding interview tables

Revision ID: 046fed6fc619
Revises: 11428530178f
Create Date: 2026-07-22
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "046fed6fc619"
down_revision: Union[str, Sequence[str], None] = "11428530178f"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "coding_interviews",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            index=True,
        ),
    )

    op.create_table(
        "coding_questions",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            index=True,
        ),
    )

    op.create_table(
        "coding_submissions",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            index=True,
        ),
    )


def downgrade() -> None:

    op.drop_table("coding_submissions")
    op.drop_table("coding_questions")
    op.drop_table("coding_interviews")
