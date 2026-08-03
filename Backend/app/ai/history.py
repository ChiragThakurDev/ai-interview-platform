"""
Conversation History Manager.

Stores conversation history for a single session.
Future versions can store this in Redis or PostgreSQL.
"""

from collections import deque
from typing import Dict, List


class HistoryManager:

    def __init__(self):

        self._messages = []

    # =====================================================
    # Add
    # =====================================================

    def add(
        self,
        role: str,
        content: str,
    ):

        self._messages.append(
            {
                "role": role,
                "content": content,
            }
        )

    # =====================================================
    # Backward Compatibility
    # =====================================================

    def append(
        self,
        role: str,
        content: str,
    ):

        self.add(role, content)

    # =====================================================
    # Get
    # =====================================================

    def get(self):

        return self._messages

    # =====================================================
    # Last Message
    # =====================================================

    def last(self):

        if not self._messages:
            return None

        return self._messages[-1]

    # =====================================================
    # Count
    # =====================================================

    def count(self):

        return len(self._messages)

    # =====================================================
    # Size
    # =====================================================

    def size(self):

        return len(self._messages)

    # =====================================================
    # Clear
    # =====================================================

    def clear(self):

        self._messages.clear()


# ==========================================================
# New AI Chat History
# ==========================================================


class ChatHistory:

    def __init__(
        self,
        max_messages: int = 20,
    ):

        self.messages = deque(maxlen=max_messages)

    def add(
        self,
        role: str,
        content: str,
    ):

        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

    def append(
        self,
        role: str,
        content: str,
    ):

        self.add(role, content)

    def extend(
        self,
        messages: List[Dict],
    ):

        for message in messages:
            self.messages.append(message)

    def get(self):

        return list(self.messages)

    def last(
        self,
        count: int = 5,
    ):

        return list(self.messages)[-count:]

    def clear(self):

        self.messages.clear()

    def size(self):

        return len(self.messages)
