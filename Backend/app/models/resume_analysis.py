from sqlalchemy import (
        Column,
        Integer,
        ForeignKey,
        Text,
        DateTime,
)

from sqlalchemy.sql import func 
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base import Base

class ResumeAnalysis(Base):
    __tablename__="resume_analysis"

    id=Column(Integer, primary_key=True, index=True)

    resume_id=Column(
            Integer,
            ForeignKey("resumes.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
            )
    overall_score=Column(Integer, nullable=False)

    strengths=Column(JSONB, nullable=False)

    weaknesses=Column(JSONB, nullable=False)

    suggestions=Column(JSONB, nullable=False)

    recommended_roles=Column(JSONB,nullable=False)

    summary=Column(Text, nullable=False)

    created_at=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            )

