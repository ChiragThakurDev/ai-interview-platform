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

    conn = op.get_bind()

    # Get existing columns in coding_submissions
    result = conn.execute(sa.text(
        """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'coding_submissions'
        """
    ))
    existing_columns = {row[0]: row[1] for row in result}

    # Add missing columns that were never added by earlier migrations
    if 'question_id' not in existing_columns:
        op.add_column('coding_submissions', sa.Column('question_id', sa.Integer(), nullable=True))
        op.create_foreign_key(None, 'coding_submissions', 'coding_questions', ['question_id'], ['id'], ondelete='CASCADE')

    if 'language' not in existing_columns:
        op.add_column('coding_submissions', sa.Column('language', sa.String(), nullable=True))

    if 'code' not in existing_columns:
        op.add_column('coding_submissions', sa.Column('code', sa.Text(), nullable=True))

    if 'passed' not in existing_columns:
        op.add_column('coding_submissions', sa.Column('passed', sa.Boolean(), nullable=False, server_default='false'))

    if 'score' not in existing_columns:
        op.add_column('coding_submissions', sa.Column('score', sa.Integer(), nullable=True))

    if 'feedback' not in existing_columns:
        op.add_column('coding_submissions', sa.Column('feedback', sa.Text(), nullable=True))

    if 'submitted_at' not in existing_columns:
        op.add_column('coding_submissions', sa.Column('submitted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))

    # Handle output column: add as JSON if missing, or convert TEXT -> JSON if it exists as text
    if 'output' not in existing_columns:
        op.add_column('coding_submissions', sa.Column('output', sa.JSON(), nullable=True))
    elif existing_columns.get('output') in ('text', 'character varying'):
        # Convert old text values into valid JSON first
        conn.execute(sa.text(
            """
            UPDATE coding_submissions
            SET output = json_build_object('message', output)::text
            WHERE output IS NOT NULL
            AND output NOT LIKE '{%'
            """
        ))
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
