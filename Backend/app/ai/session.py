"""
AI Session Manager.

Supports both:
- Legacy tests
- New AI architecture
"""

from uuid import uuid4
from typing import Dict

from app.ai.history import ChatHistory
from app.ai.memory import AIMemory
"""
AI Session Manager.

Supports both:
- Legacy tests
- New AI architecture
"""

from uuid import uuid4
from typing import Dict

from app.ai.history import ChatHistory
from app.ai.memory import AIMemory


class SessionManager:

    def __init__(self):

        # New AI architecture
        self._sessions: Dict[str, ChatHistory] = {}

        # Legacy compatibility
        self.data = {}

    # =====================================================
    # Create
    # =====================================================

    def create(
        self,
        session_id: str | None = None,
        **kwargs,
    ):

        # Legacy API
        if session_id is None:

            session_id = str(uuid4())

            self.data = {
                "id": session_id,
                **kwargs,
            }

            return self.data

        # New API
        history = ChatHistory()

        self._sessions[session_id] = history

        return history

    # =====================================================
    # Update
    # =====================================================

    def update(
        self,
        **kwargs,
    ):

        self.data.update(kwargs)

        return self.data

    # =====================================================
    # Set
    # =====================================================

    def set(
        self,
        key,
        value,
    ):

        self.data[key] = value

    # =====================================================
    # Value
    # =====================================================

    def value(
        self,
        key,
        default=None,
    ):

        return self.data.get(key, default)

    # =====================================================
    # Get
    # =====================================================

    def get(
        self,
        session_id=None,
    ):

        if session_id is None:
            return self.data

        if session_id not in self._sessions:
            self.create(session_id)

        return self._sessions[session_id]

    # =====================================================
    # Exists
    # =====================================================

    def exists(
        self,
        session_id=None,
    ):

        if session_id is None:
            return bool(self.data)

        return session_id in self._sessions

    # =====================================================
    # Delete
    # =====================================================

    def delete(
        self,
        session_id,
    ):

        self._sessions.pop(session_id, None)

    # =====================================================
    # Clear
    # =====================================================

    def clear(self):

        self.data.clear()

        self._sessions.clear()

    # =====================================================
    # Count
    # =====================================================

    def count(self):

        return len(self._sessions)


class AISession:

    def __init__(self):

        self.history = ChatHistory()

        self.memory = AIMemory()

    def reset(self):

        self.history.clear()

        self.memory.clear()
