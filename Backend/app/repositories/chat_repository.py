from sqlalchemy.orm import Session

from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage



class ChatRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db


    # =====================================================
    # Chat Sessions
    # =====================================================


    def create_session(
        self,
        user_id: int,
        title: str,
    ):

        session = ChatSession(
            user_id=user_id,
            title=title,
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session



    def get_user_sessions(
        self,
        user_id: int,
    ):

        return (
            self.db.query(ChatSession)
            .filter(
                ChatSession.user_id == user_id
            )
            .order_by(
                ChatSession.created_at.desc()
            )
            .all()
        )



    def get_session(
        self,
        session_id: int,
        user_id: int,
    ):

        return (
            self.db.query(ChatSession)
            .filter(
                ChatSession.id == session_id,
                ChatSession.user_id == user_id,
            )
            .first()
        )



    def delete_session(
        self,
        session: ChatSession,
    ):

        self.db.delete(session)
        self.db.commit()



    # =====================================================
    # Chat Messages
    # =====================================================


    def create_message(
        self,
        session_id: int,
        role: str,
        content: str,
    ):

        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message



    def get_messages(
        self,
        session_id: int,
    ):

        return (
            self.db.query(ChatMessage)
            .filter(
                ChatMessage.session_id == session_id
            )
            .order_by(
                ChatMessage.created_at.asc()
            )
            .all()
        )
