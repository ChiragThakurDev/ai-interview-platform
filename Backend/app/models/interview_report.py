from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Text,
    DateTime,
    JSON,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class InterviewReport(Base):

    __tablename__ = "interview_reports"

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

    overall_score = Column(
        Integer,
        nullable=False,
    )

    technical_level = Column(
        String,
        nullable=False,
    )

    communication = Column(
        String,
        nullable=False,
    )

    strengths = Column(
        JSON,
        nullable=False,
    )

    weaknesses = Column(
        JSON,
        nullable=False,
    )

    recommendation = Column(
        Text,
        nullable=False,
    )

    summary = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


    interview = relationship(
        "Interview",
        back_populates="report",
    )
