from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    DateTime,
    func,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class Roadmap(Base):
    __tablename__ = "roadmaps"

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
    )

    skill_report_id = Column(
        Integer,
        ForeignKey(
            "skill_reports.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    title = Column(
        Text,
        nullable=False,
    )

    duration = Column(
        Text,
        nullable=False,
    )

    weekly_plan = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship("User")

    skill_report = relationship("SkillReport")
