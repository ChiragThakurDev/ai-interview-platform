from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
    DateTime,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    question_id = Column(
        Integer,
        ForeignKey(
            "interview_questions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    answer = Column(
        Text,
        nullable=False,
    )

    score = Column(
        Integer,
        nullable=False,
    )

    feedback = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    question = relationship(
        "InterviewQuestion",
        back_populates="answer",
    )
