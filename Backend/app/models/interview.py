from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    DateTime,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
    )

    title = Column(
        String,
        nullable=False,
    )

    role = Column(
        String,
        nullable=False,
    )

    difficulty = Column(
        String,
        nullable=False,
    )

    status = Column(
        String,
        nullable=False,
        default="pending",
    )

    started_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    duration = Column(
        Integer,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user = relationship(
        "User",
        back_populates="interviews",
    )

    resume = relationship(
        "Resume",
        back_populates="interviews",
    )

    questions = relationship(
        "InterviewQuestion",
        back_populates="interview",
        cascade="all, delete-orphan",
    )

    report = relationship(
        "InterviewReport",
        back_populates="interview",
        uselist=False,
        cascade="all, delete-orphan",
    )
