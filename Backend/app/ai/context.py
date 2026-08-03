from app.ai.session import AISession
from app.ai.summarizer import ConversationSummarizer


class ContextManager:

    def __init__(self):

        self.session = AISession()

        self.summarizer = ConversationSummarizer()

    def add_user_message(
        self,
        message: str,
    ):

        self.session.history.add(
            "user",
            message,
        )

    def add_ai_message(
        self,
        message: str,
    ):

        self.session.history.add(
            "assistant",
            message,
        )

    def remember(
        self,
        key: str,
        value,
    ):

        self.session.memory.set(
            key,
            value,
        )

    def recall(
        self,
        key: str,
        default=None,
    ):

        return self.session.memory.get(
            key,
            default,
        )

    def context(self):

        return {
            "history": self.session.history.get(),
            "summary": self.summarizer.summarize(
                self.session.history
            ),
            "memory": self.session.memory.all(),
        }

    def clear(self):

        self.session.reset()
