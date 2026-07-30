"""ensure all model columns exist (schema reconciliation)

Revision ID: a1b2c3d4e5f6
Revises: ec8436767dbd
Create Date: 2026-07-30

This migration reconciles the database schema with the SQLAlchemy models by
adding any columns that exist in the models but were never added via Alembic
migrations. It is idempotent: columns are only added if they don't already exist.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "ec8436767dbd"
branch_labels = None
depends_on = None


def _column_exists(conn, table: str, column: str) -> bool:
    result = conn.execute(sa.text(
        """
        SELECT 1 FROM information_schema.columns
        WHERE table_name = :table AND column_name = :column
        """
    ), {"table": table, "column": column})
    return result.fetchone() is not None


def upgrade() -> None:
    conn = op.get_bind()

    # ── interviews table ────────────────────────────────────────────────────
    # status (core field — was never added by any migration)
    if not _column_exists(conn, "interviews", "status"):
        op.add_column("interviews", sa.Column(
            "status", sa.String(20), nullable=False, server_default="pending"
        ))

    # started_at
    if not _column_exists(conn, "interviews", "started_at"):
        op.add_column("interviews", sa.Column(
            "started_at", sa.DateTime(timezone=True), nullable=True
        ))

    # completed_at
    if not _column_exists(conn, "interviews", "completed_at"):
        op.add_column("interviews", sa.Column(
            "completed_at", sa.DateTime(timezone=True), nullable=True
        ))

    # duration
    if not _column_exists(conn, "interviews", "duration"):
        op.add_column("interviews", sa.Column(
            "duration", sa.Integer(), nullable=True, server_default="0"
        ))

    # current_question — 55d6d7f651db added it but with server_default=1, model wants 0
    if not _column_exists(conn, "interviews", "current_question"):
        op.add_column("interviews", sa.Column(
            "current_question", sa.Integer(), nullable=False, server_default="0"
        ))

    # score — 55d6d7f651db adds this but let's be safe
    if not _column_exists(conn, "interviews", "score"):
        op.add_column("interviews", sa.Column(
            "score", sa.Integer(), nullable=True, server_default="0"
        ))

    # role — 67c96ab13061 adds this but on a fresh DB it may fail due to NOT NULL
    if not _column_exists(conn, "interviews", "role"):
        op.add_column("interviews", sa.Column(
            "role", sa.String(), nullable=True
        ))

    # difficulty — same as role
    if not _column_exists(conn, "interviews", "difficulty"):
        op.add_column("interviews", sa.Column(
            "difficulty", sa.String(), nullable=True
        ))

    # company — 11428530178f adds this
    if not _column_exists(conn, "interviews", "company"):
        op.add_column("interviews", sa.Column(
            "company", sa.String(), nullable=True
        ))

    # ── coding_interviews table ─────────────────────────────────────────────
    # Verify key coding_interviews columns exist (added by various migrations)
    coding_interview_columns = {
        "user_id": sa.Column("user_id", sa.Integer(), nullable=True),
        "status": sa.Column("status", sa.String(), nullable=True, server_default="pending"),
        "score": sa.Column("score", sa.Integer(), nullable=True),
        "created_at": sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        "completed_at": sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        "language": sa.Column("language", sa.String(), nullable=True, server_default="python"),
        "role": sa.Column("role", sa.String(), nullable=True),
        "difficulty": sa.Column("difficulty", sa.String(), nullable=True),
        "company": sa.Column("company", sa.String(), nullable=True),
        "current_question": sa.Column("current_question", sa.Integer(), nullable=False, server_default="0"),
        "answered_questions": sa.Column("answered_questions", sa.Integer(), nullable=False, server_default="0"),
        "started_at": sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
    }
    for col_name, col_def in coding_interview_columns.items():
        if not _column_exists(conn, "coding_interviews", col_name):
            op.add_column("coding_interviews", col_def)

    # ── coding_questions table ──────────────────────────────────────────────
    coding_question_columns = {
        "coding_interview_id": sa.Column("coding_interview_id", sa.Integer(), nullable=True),
        "title": sa.Column("title", sa.String(), nullable=True),
        "description": sa.Column("description", sa.Text(), nullable=True),
        "difficulty": sa.Column("difficulty", sa.String(), nullable=True),
        "starter_code": sa.Column("starter_code", sa.Text(), nullable=True),
        "solution_code": sa.Column("solution_code", sa.Text(), nullable=True),
        "function_name": sa.Column("function_name", sa.String(), nullable=True),
        "created_at": sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
    }
    for col_name, col_def in coding_question_columns.items():
        if not _column_exists(conn, "coding_questions", col_name):
            op.add_column("coding_questions", col_def)

    # ── coding_submissions table ────────────────────────────────────────────
    coding_submission_columns = {
        "question_id": sa.Column("question_id", sa.Integer(), nullable=True),
        "language": sa.Column("language", sa.String(), nullable=True),
        "code": sa.Column("code", sa.Text(), nullable=True),
        "passed": sa.Column("passed", sa.Boolean(), nullable=False, server_default="false"),
        "score": sa.Column("score", sa.Integer(), nullable=True),
        "feedback": sa.Column("feedback", sa.Text(), nullable=True),
        "submitted_at": sa.Column("submitted_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
    }
    for col_name, col_def in coding_submission_columns.items():
        if not _column_exists(conn, "coding_submissions", col_name):
            op.add_column("coding_submissions", col_def)

    # output column: add as JSON if missing
    if not _column_exists(conn, "coding_submissions", "output"):
        op.add_column("coding_submissions", sa.Column("output", sa.JSON(), nullable=True))


def downgrade() -> None:
    # This migration only adds columns; downgrade is a no-op to avoid data loss.
    pass
