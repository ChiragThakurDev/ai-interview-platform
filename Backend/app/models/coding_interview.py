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



class CodingInterview(Base):

    __tablename__ = "coding_interviews"



    # =====================================================
    # PRIMARY KEY
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )



    # =====================================================
    # USER
    # =====================================================

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )



    # =====================================================
    # INTERVIEW DETAILS
    # =====================================================

    role = Column(
        String,
        nullable=False,
    )


    company = Column(
        String,
        nullable=True,
    )


    language = Column(
        String,
        nullable=False,
        default="python",
        server_default="python",
    )


    difficulty = Column(
        String,
        nullable=False,
    )



    # =====================================================
    # STATUS
    # =====================================================

    status = Column(
        String,
        nullable=False,
        default="pending",
        server_default="pending",
    )



    # =====================================================
    # SCORE
    # =====================================================

    score = Column(
        Integer,
        nullable=True,
    )



    # =====================================================
    # INTERVIEW PROGRESS
    # =====================================================

    current_question = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )


    answered_questions = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )



    # =====================================================
    # TIMESTAMPS
    # =====================================================

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



    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    user = relationship(
        "User",
        back_populates="coding_interviews",
    )



    questions = relationship(
        "CodingQuestion",

        back_populates="coding_interview",

        cascade="all, delete-orphan",
    )
