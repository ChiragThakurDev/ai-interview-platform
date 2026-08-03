"""add prompt versioning table

Revision ID: a6a5ccd70267
Revises: a1b2c3d4e5f6
Create Date: 2026-08-03 01:18:20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a6a5ccd70267"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f6"

branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "prompts",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            "name",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "version",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "template",
            sa.Text(),
            nullable=False
        ),

        sa.Column(
            "model",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "temperature",
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=True,
            server_default="true"
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True
        )
    )


    op.create_index(
        "ix_prompts_name",
        "prompts",
        ["name"],
        unique=False
    )



def downgrade() -> None:

    op.drop_index(
        "ix_prompts_name",
        table_name="prompts"
    )

    op.drop_table(
        "prompts"
    )
