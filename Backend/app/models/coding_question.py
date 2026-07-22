from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class CodingQuestion(Base):
    __tablename__ = "coding_questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    coding_interview_id = Column(
        Integer,
        ForeignKey(
            "coding_interviews.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    title = Column(
        String,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    starter_code = Column(
        Text,
        nullable=True,
    )

    solution = Column(
        Text,
        nullable=True,
    )

    difficulty = Column(
        String,
        nullable=False,
    )

    # ======================================
    # Relationships
    # ======================================

    coding_interview = relationship(
        "CodingInterview",
        back_populates="questions",
    )

    submissions = relationship(
        "CodingSubmission",
        back_populates="question",
        cascade="all, delete-orphan",
    )
