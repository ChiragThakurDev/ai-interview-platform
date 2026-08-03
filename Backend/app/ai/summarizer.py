from app.ai.history import ChatHistory


class ConversationSummarizer:

    def summarize(
        self,
        history: ChatHistory,
        last_messages: int = 5,
    ) -> str:

        messages = history.last(last_messages)

        if not messages:
            return ""

        summary = []

        for message in messages:

            summary.append(
                f"{message['role']}: {message['content']}"
            )

        return "\n".join(summary)
