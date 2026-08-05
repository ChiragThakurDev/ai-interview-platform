from sqlalchemy import (
    Column,
    Integer,
    Float,
    Text,
    JSON,
    DateTime,
    ForeignKey,
)

from sqlalchemy.sql import func

from app.db.base import Base


class InterviewEvaluation(Base):

    __tablename__ = "interview_evaluations"


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
    )


    question_id = Column(
        Integer,
        ForeignKey(
            "interview_questions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )


    technical_score = Column(
        Float,
        nullable=True,
    )


    communication_score = Column(
        Float,
        nullable=True,
    )


    confidence_score = Column(
        Float,
        nullable=True,
    )


    overall_score = Column(
        Float,
        nullable=True,
    )


    feedback = Column(
        Text,
        nullable=True,
    )


    strengths = Column(
        JSON,
        nullable=True,
    )


    weaknesses = Column(
        JSON,
        nullable=True,
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
