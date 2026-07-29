from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class CodingSubmission(Base):

    __tablename__ = "coding_submissions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ======================================
    # Foreign Keys
    # ======================================

    interview_id = Column(
        Integer,
        ForeignKey(
            "coding_interviews.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    question_id = Column(
        Integer,
        ForeignKey(
            "coding_questions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # ======================================
    # Submission
    # ======================================

    language = Column(
        String,
        nullable=False,
    )

    code = Column(
        Text,
        nullable=False,
    )

    output = Column(
        JSON,
        nullable=True,
    )

    passed = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    score = Column(
        Integer,
        nullable=True,
    )

    feedback = Column(
        Text,
        nullable=True,
    )

    submitted_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # ======================================
    # Relationships
    # ======================================

    interview = relationship(
        "CodingInterview",
        back_populates="submissions",
    )

    question = relationship(
        "CodingQuestion",
        back_populates="submissions",
    )
