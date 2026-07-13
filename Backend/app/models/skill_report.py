from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    JSON,
    Text,
    DateTime,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base



class SkillReport(Base):

    __tablename__ = "skill_reports"


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
        unique=True,
    )


    strong_skills = Column(
        JSON,
        nullable=False,
    )


    weak_skills = Column(
        JSON,
        nullable=False,
    )


    recommended_topics = Column(
        JSON,
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


    user = relationship(
        "User",
        back_populates="skill_report",
    )
