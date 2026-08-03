from datetime import UTC, datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from app.db.base import Base


class PromptExecution(Base):

    __tablename__ = "prompt_executions"


    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )


    prompt_id = Column(
        Integer,
        ForeignKey(
            "prompts.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )


    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )


    prompt_name = Column(
        String(100),
        nullable=False,
        index=True,
    )


    prompt_version = Column(
        String(50),
        nullable=False,
    )


    provider = Column(
        String(50),
        nullable=True,
    )


    model = Column(
        String(100),
        nullable=True,
    )


    variables = Column(
        Text,
        nullable=True,
    )


    rendered_prompt = Column(
        Text,
        nullable=False,
    )


    response = Column(
        Text,
        nullable=True,
    )


    error = Column(
        Text,
        nullable=True,
    )


    success = Column(
        Boolean,
        default=True,
        nullable=False,
    )


    latency = Column(
        Float,
        nullable=True,
    )


    tokens_used = Column(
        Integer,
        nullable=True,
    )


    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
