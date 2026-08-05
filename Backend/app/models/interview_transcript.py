from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class InterviewTranscript(Base):

    __tablename__ = "interview_transcripts"

    # ==========================================
    # Primary Key
    # ==========================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ==========================================
    # Foreign Keys
    # ==========================================

    interview_id = Column(
        Integer,
        ForeignKey(
            "interviews.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    question_id = Column(
        Integer,
        ForeignKey(
            "interview_questions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # ==========================================
    # Transcript
    # ==========================================

    speaker = Column(
        String(20),
        nullable=False,
    )

    transcript = Column(
        Text,
        nullable=False,
    )

    confidence = Column(
        Float,
        nullable=True,
    )

    language = Column(
        String(20),
        nullable=True,
    )

    # ==========================================
    # Timing
    # ==========================================

    start_time = Column(
        Float,
        nullable=True,
    )

    end_time = Column(
        Float,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # ==========================================
    # Relationships
    # ==========================================

    interview = relationship(
        "Interview",
        back_populates="transcripts",
    )

    question = relationship(
        "InterviewQuestion",
        back_populates="transcripts",
    )
