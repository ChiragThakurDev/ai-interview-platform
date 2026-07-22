from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.chat_repository import ChatRepository
from app.ai.chains import chat_chain


class ChatService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = ChatRepository(db)


    # =====================================================
    # Create Chat Session
    # =====================================================

    def create_session(
        self,
        user_id: int,
        title: str,
    ):

        return self.repository.create_session(
            user_id=user_id,
            title=title,
        )


    # =====================================================
    # Get User Sessions
    # =====================================================

    def get_sessions(
        self,
        user_id: int,
    ):

        return self.repository.get_user_sessions(
            user_id
        )


    # =====================================================
    # Get Chat History
    # =====================================================

    def get_messages(
        self,
        session_id: int,
        user_id: int,
    ):

        session = self.repository.get_session(
            session_id=session_id,
            user_id=user_id,
        )


        if session is None:

            raise HTTPException(
                status_code=404,
                detail="Chat session not found",
            )


        return self.repository.get_messages(
            session_id
        )


    # =====================================================
    # Send Message
    # =====================================================

    def send_message(
        self,
        session_id: int,
        user_id: int,
        message: str,
    ):


        session = self.repository.get_session(
            session_id=session_id,
            user_id=user_id,
        )


        if session is None:

            raise HTTPException(
                status_code=404,
                detail="Chat session not found",
            )


        # Save user message

        self.repository.create_message(
            session_id=session_id,
            role="user",
            content=message,
        )


        # Get conversation history

        history = self.repository.get_messages(
            session_id
        )


        ai_messages = [
            {
                "role": msg.role,
                "content": msg.content,
            }
            for msg in history
        ]


        # Generate AI response

        response = chat_chain(
            ai_messages
        )


        # Save AI response

        ai_message = self.repository.create_message(
            session_id=session_id,
            role="assistant",
            content=response,
        )


        return ai_message


    # =====================================================
    # Delete Session
    # =====================================================

    def delete_session(
        self,
        session_id: int,
        user_id: int,
    ):


        session = self.repository.get_session(
            session_id=session_id,
            user_id=user_id,
        )


        if session is None:

            raise HTTPException(
                status_code=404,
                detail="Chat session not found",
            )


        self.repository.delete_session(
            session
        )


        return {
            "message": "Chat session deleted successfully"
        }
