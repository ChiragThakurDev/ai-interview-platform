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


class APILog(Base):

    __tablename__ = "api_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    method = Column(
        String(10),
        nullable=False,
    )

    endpoint = Column(
        String(255),
        nullable=False,
    )

    status_code = Column(
        Integer,
        nullable=False,
    )

    response_time = Column(
        Integer,
        nullable=False,
    )

    ip_address = Column(
        String(50),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user = relationship(
        "User",
    )
