from app.ai.factory import AIFactory
from app.ai.prompts import CHAT_SYSTEM_PROMPT

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)


class ChatAIService:
    """
    AI Chat service for conversational interview assistance.

    Model: llama3.2:3b (via AIFactory.chat())
    Reason: Chat is conversational — fast response time matters more than
            maximum accuracy. llama3.2:3b fits 100% in 4GB VRAM, delivering
            sub-second first token latency. No JSON mode needed.

    Settings: temperature=0.7, num_ctx=2048, num_predict=512, keep_alive=30m

    Note: This service wraps the same logic as chains.chat_chain but as a
    class-based service for consistency with the rest of the service layer.
    Use chat_service.py → chains.chat_chain for the main chat API.
    This class is available for future extensions (e.g., streaming, context injection).
    """

    def __init__(self):
        # llama3.2:3b — fast, fits in VRAM, great for conversation
        self.provider = AIFactory.chat()
        self.llm = self.provider.llm

    def chat(
        self,
        messages: list[dict],
    ) -> str:
        """
        Generate an AI response given a conversation history.

        Args:
            messages: List of {"role": "user"|"assistant", "content": str}

        Returns:
            AI response string
        """

        langchain_messages = [
            SystemMessage(content=CHAT_SYSTEM_PROMPT)
        ]

        for message in messages:
            role = message.get("role")
            content = message.get("content", "")

            if role == "user":
                langchain_messages.append(
                    HumanMessage(content=content)
                )
            elif role == "assistant":
                langchain_messages.append(
                    AIMessage(content=content)
                )

        response = self.llm.invoke(langchain_messages)
        return response.content
