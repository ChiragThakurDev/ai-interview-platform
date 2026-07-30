import logging

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from app.ai.factory import AIFactory
from app.ai.prompts import CHAT_SYSTEM_PROMPT


logger = logging.getLogger(__name__)


def chat_chain(
    messages: list[dict],
) -> str:
    """
    AI Chat conversation chain.

    Routed through AIFactory.chat() to ensure:
    - Correct model: llama3.2:3b (fast, conversational)
    - Singleton instance (no cold-start per request)
    - Consistent temperature and context settings

    Flow:
    User Message
        ↓
    Chat History
        ↓
    LangChain Messages
        ↓
    System Prompt
        ↓
    AIFactory.chat() → llama3.2:3b
        ↓
    AI Response
    """

    try:

        # Use AIFactory to get the shared singleton chat provider.
        # This avoids creating a new ChatOllama instance on every request.
        provider = AIFactory.chat()
        llm = provider.llm

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

        response = llm.invoke(langchain_messages)

        return response.content

    except Exception as e:

        logger.error(f"Chat AI generation failed: {str(e)}")

        return (
            "I am currently unable to generate a response. "
            "Please try again later."
        )
