"""change coding submission output to json

Revision ID: 0a26cfbb9286
Revises: 7afe56747231
Create Date: 2026-07-28 13:12:08.028254

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0a26cfbb9286"

down_revision: Union[str, Sequence[str], None] = "7afe56747231"

branch_labels = None

depends_on = None



def upgrade() -> None:


    # Convert old text values into valid JSON
    op.execute(
        """
        UPDATE coding_submissions
        SET output = json_build_object(
            'message',
            output
        )::text
        WHERE output IS NOT NULL
        AND output NOT LIKE '{%';
        """
    )


    # Change TEXT -> JSON
    op.alter_column(
        "coding_submissions",
        "output",
        existing_type=sa.TEXT(),
        type_=sa.JSON(),
        postgresql_using="output::json",
        existing_nullable=True,
    )




def downgrade() -> None:


    # JSON -> TEXT

    op.alter_column(
        "coding_submissions",
        "output",
        existing_type=sa.JSON(),
        type_=sa.TEXT(),
        postgresql_using="output::text",
        existing_nullable=True,
    )
