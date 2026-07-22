from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.chat import (
    ChatSessionCreate,
    ChatMessageCreate,
)

from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


# =====================================================
# Create Chat Session
# =====================================================

@router.post("/sessions")
def create_session(
    data: ChatSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = ChatService(db)

    return service.create_session(
        user_id=current_user.id,
        title=data.title,
    )


# =====================================================
# Get User Chat Sessions
# =====================================================

@router.get("/sessions")
def get_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = ChatService(db)

    return service.get_sessions(
        current_user.id
    )


# =====================================================
# Get Messages
# =====================================================

@router.get("/sessions/{session_id}/messages")
def get_messages(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = ChatService(db)

    return service.get_messages(
        session_id=session_id,
        user_id=current_user.id,
    )


# =====================================================
# Send Message
# =====================================================

@router.post("/sessions/{session_id}/message")
def send_message(
    session_id: int,
    data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = ChatService(db)

    return service.send_message(
        session_id=session_id,
        user_id=current_user.id,
        message=data.message,
    )


# =====================================================
# Delete Session
# =====================================================

@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = ChatService(db)

    return service.delete_session(
        session_id=session_id,
        user_id=current_user.id,
    )
