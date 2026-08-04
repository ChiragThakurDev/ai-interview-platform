from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class InterviewRoom(Base):

    __tablename__ = "interview_rooms"


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


    room_name = Column(
        String,
        nullable=False,
        unique=True,
    )


    status = Column(
        String,
        default="waiting",
        nullable=False,
    )


    started_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )


    ended_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )


    duration_seconds = Column(
        Integer,
        nullable=True,
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


    interview = relationship(
        "Interview",
        back_populates="room",
    )
