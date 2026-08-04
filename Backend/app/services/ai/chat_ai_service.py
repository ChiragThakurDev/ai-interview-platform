from sqlalchemy.orm import Session

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from app.ai.factory import AIFactory
from app.ai.prompt_manager import PromptManager
from app.services.prompt_service import PromptService


class ChatAIService:
    """
    AI Chat service for conversational interview assistance.

    Loads the active system prompt from the database.
    Falls back to the default prompt if PromptService is configured to do so.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.provider = AIFactory.chat()
        self.llm = self.provider.llm

        self.prompt_service = PromptService(
            db
        )

    def chat(
        self,
        messages: list[dict],
    ) -> str:
        """
        Generate an AI response given a conversation history.

        Args:
            messages: List of
                {
                    "role": "user" | "assistant",
                    "content": str
                }

        Returns:
            AI response string.
        """

        latest_user_message = next(
            (
                message.get("content", "")
                for message in reversed(messages)
                if message.get("role") == "user"
            ),
            "",
        )

        variables = {
            "name": "Candidate",
            "question": latest_user_message,
        }

        try:
            system_prompt = self.prompt_service.build_prompt(
                name="chat_system",
                variables=variables,
            )
        except ValueError:
            system_prompt = PromptManager.build(
                "chat_system",
                **variables,
            )

        langchain_messages = [
            SystemMessage(
                content=system_prompt
            )
        ]

        for message in messages:

            role = message.get("role")
            content = message.get("content", "")

            if role == "user":

                langchain_messages.append(
                    HumanMessage(
                        content=content
                    )
                )

            elif role == "assistant":

                langchain_messages.append(
                    AIMessage(
                        content=content
                    )
                )

        response = self.llm.invoke(
            langchain_messages
        )

        return response.content
