"""upgrade prompt management

Revision ID: 46d1cff24103
Revises: a6a5ccd70267
Create Date: 2026-08-03 03:38:28.800419

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "46d1cff24103"
down_revision: Union[str, Sequence[str], None] = "a6a5ccd70267"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Upgrade prompt management.

    prompts table already exists from previous migration.
    Only add missing columns.
    """

    conn = op.get_bind()

    inspector = sa.inspect(conn)

    existing_columns = {
        col["name"]
        for col in inspector.get_columns("prompts")
    }


    # Add only missing columns

    if "provider" not in existing_columns:
        op.add_column(
            "prompts",
            sa.Column(
                "provider",
                sa.String(length=50),
                nullable=True
            )
        )


    if "model" not in existing_columns:
        op.add_column(
            "prompts",
            sa.Column(
                "model",
                sa.String(length=100),
                nullable=True
            )
        )


    if "temperature" not in existing_columns:
        op.add_column(
            "prompts",
            sa.Column(
                "temperature",
                sa.Float(),
                nullable=True
            )
        )


    if "is_active" not in existing_columns:
        op.add_column(
            "prompts",
            sa.Column(
                "is_active",
                sa.Boolean(),
                nullable=True,
                server_default=sa.text("true")
            )
        )


    if "created_at" not in existing_columns:
        op.add_column(
            "prompts",
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                nullable=True
            )
        )


    if "updated_at" not in existing_columns:
        op.add_column(
            "prompts",
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                nullable=True
            )
        )


    # indexes

    indexes = {
        idx["name"]
        for idx in inspector.get_indexes("prompts")
    }


    if "idx_prompt_active" not in indexes:
        op.create_index(
            "idx_prompt_active",
            "prompts",
            ["name", "is_active"],
            unique=False
        )


def downgrade() -> None:
    """
    Reverse changes.
    """

    op.drop_index(
        "idx_prompt_active",
        table_name="prompts"
    )


    conn = op.get_bind()

    inspector = sa.inspect(conn)

    columns = {
        col["name"]
        for col in inspector.get_columns("prompts")
    }


    for column in [
        "updated_at",
        "created_at",
        "is_active",
        "temperature",
        "model",
        "provider",
    ]:
        if column in columns:
            op.drop_column(
                "prompts",
                column
            )
