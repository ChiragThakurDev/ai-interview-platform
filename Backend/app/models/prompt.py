from datetime import datetime, UTC

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Float,
    DateTime,
)

from app.db.base import Base


class Prompt(Base):

    __tablename__ = "prompts"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String,
        nullable=False,
        index=True
    )

    version = Column(
        String,
        nullable=False
    )

    template = Column(
        Text,
        nullable=False
    )

    model = Column(
        String,
        default="llama3.1:8b"
    )

    temperature = Column(
        Float,
        default=0.3
    )

    is_active = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )
