from sqlalchemy import Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CodingTestCase(Base):
    __tablename__ = "coding_test_cases"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    question_id: Mapped[int] = mapped_column(
        ForeignKey("coding_questions.id", ondelete="CASCADE"),
        nullable=False,
    )

    input_data: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    expected_output: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_hidden: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    question = relationship(
        "CodingQuestion",
        back_populates="test_cases",
    )
