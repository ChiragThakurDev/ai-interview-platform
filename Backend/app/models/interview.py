from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Interview(Base):

    __tablename__ = "interviews"


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

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )


    resume_id = Column(
        Integer,
        ForeignKey(
            "resumes.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )


    # ==========================================
    # Interview Information
    # ==========================================

    title = Column(
        String,
        nullable=False,
    )


    role = Column(
        String,
        nullable=False,
    )


    company = Column(
        String,
        nullable=True,
    )


    difficulty = Column(
        String,
        nullable=False,
    )


    # ==========================================
    # Interview Progress State
    # ==========================================

    status = Column(
        String(20),
        nullable=False,
        default="pending",
        server_default="pending",
    )


    current_question = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )


    score = Column(
        Integer,
        nullable=False,
        default="0",
        server_default="0",
    )


    duration = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )


    # ==========================================
    # Timing
    # ==========================================

    started_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )


    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


    # ==========================================
    # Relationships
    # ==========================================


    user = relationship(
        "User",
        back_populates="interviews",
    )


    resume = relationship(
        "Resume",
        back_populates="interviews",
    )


    questions = relationship(
        "InterviewQuestion",
        back_populates="interview",
        cascade="all, delete-orphan",
    )


    answers = relationship(
        "InterviewAnswer",
        back_populates="interview",
        cascade="all, delete-orphan",
    )


    report = relationship(
        "InterviewReport",
        back_populates="interview",
        uselist=False,
        cascade="all, delete-orphan",
    )


    # ==========================================
    # Persistent Runtime Session
    # ==========================================

    session = relationship(
        "InterviewSession",
        back_populates="interview",
        uselist=False,
        cascade="all, delete-orphan",
    )


    # ==========================================
    # LiveKit Video Interview Room
    # ==========================================

    room = relationship(
        "InterviewRoom",
        back_populates="interview",
        uselist=False,
        cascade="all, delete-orphan",
    )
