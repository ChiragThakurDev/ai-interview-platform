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


class InterviewSession(Base):

    __tablename__ = "interview_sessions"


    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )


    interview_id = Column(
        Integer,
        ForeignKey(
            "interviews.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )


    # ==========================================
    # Runtime State
    # ==========================================

    status = Column(
        String(30),
        nullable=False,
        default="active",
        server_default="active",
    )


    current_question = Column(
        Integer,
        nullable=False,
        default=1,
        server_default="1",
    )


    total_questions = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )


    answered_questions = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )


    # ==========================================
    # Evaluation Tracking
    # ==========================================

    total_score = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )


    average_score = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )


    # ==========================================
    # Timing
    # ==========================================

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


    last_activity = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


    # ==========================================
    # Relationship
    # ==========================================

    interview = relationship(
        "Interview",
        back_populates="session",
    )
