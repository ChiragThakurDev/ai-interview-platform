"""add prompt execution logs

Revision ID: 381148e6e1da
Revises: 46d1cff24103
Create Date: 2026-08-03

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "381148e6e1da"
down_revision: Union[str, Sequence[str], None] = "46d1cff24103"

branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Add prompt execution logs.

    prompts table already exists.
    Do NOT recreate it.
    """


    op.create_table(
        "prompt_execution_logs",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "prompt_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "input_data",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "output_data",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "model",
            sa.String(length=100),
            nullable=True
        ),

        sa.Column(
            "provider",
            sa.String(length=50),
            nullable=True
        ),

        sa.Column(
            "tokens_used",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "execution_time",
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ["prompt_id"],
            ["prompts.id"],
            ondelete="CASCADE"
        ),

        sa.PrimaryKeyConstraint("id")
    )


    op.create_index(
        "ix_prompt_execution_logs_id",
        "prompt_execution_logs",
        ["id"],
        unique=False
    )



def downgrade() -> None:

    op.drop_index(
        "ix_prompt_execution_logs_id",
        table_name="prompt_execution_logs"
    )

    op.drop_table(
        "prompt_execution_logs"
    )
