from datetime import datetime, UTC

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Float,
    DateTime,
    UniqueConstraint,
    Index,
)

from app.db.base import Base


class Prompt(Base):

    __tablename__ = "prompts"

    __table_args__ = (

        # Same prompt cannot have duplicate versions
        UniqueConstraint(
            "name",
            "version",
            name="uq_prompt_name_version",
        ),

        Index(
            "idx_prompt_active",
            "name",
            "is_active",
        ),
    )


    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )


    # Example:
    # chat
    # resume_analysis
    # coding_evaluation
    name = Column(
        String(100),
        nullable=False,
        index=True,
    )


    # Example:
    # v1
    # v2
    version = Column(
        String(50),
        nullable=False,
    )


    template = Column(
        Text,
        nullable=False,
    )


    # Ollama / OpenAI / Claude etc.
    provider = Column(
        String(50),
        default="ollama",
    )


    model = Column(
        String(100),
        default="llama3.1:8b",
    )


    temperature = Column(
        Float,
        default=0.3,
    )


    is_active = Column(
        Boolean,
        default=False,
        index=True,
    )


    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )


    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
