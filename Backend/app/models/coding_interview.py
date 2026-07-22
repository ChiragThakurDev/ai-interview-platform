from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class CodingInterview(Base):
    __tablename__ = "coding_interviews"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    role = Column(
        String,
        nullable=False,
    )

    company = Column(
        String,
        nullable=True,
    )

    language = Column(
        String,
        nullable=False,
        default="python",
        server_default="python",
    )

    difficulty = Column(
        String,
        nullable=False,
    )

    status = Column(
        String,
        nullable=False,
        default="pending",
        server_default="pending",
    )

    score = Column(
        Integer,
        nullable=True,
    )

    started_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # ======================================
    # Relationships
    # ======================================

    user = relationship(
        "User",
        back_populates="coding_interviews",
    )

    questions = relationship(
        "CodingQuestion",
        back_populates="coding_interview",
        cascade="all, delete-orphan",
    )
