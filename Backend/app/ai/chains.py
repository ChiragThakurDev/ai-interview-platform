import logging

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from app.ai.factory import AIFactory
from app.ai.prompt_manager import PromptManager


logger = logging.getLogger(__name__)


def chat_chain(
    messages: list[dict],
) -> str:
    """
    AI Chat conversation chain.

    Uses database-backed prompt versioning.

    Flow:

    User Message
        ↓
    Chat History
        ↓
    PromptManager
        ↓
    PostgreSQL prompts table
        ↓
    System Prompt
        ↓
    AIFactory.chat()
        ↓
    AI Response
    """

    try:

        # Shared chat model instance
        provider = AIFactory.chat()

        llm = provider.llm


        # Database-backed prompt
        prompt_manager = PromptManager()

        system_prompt = prompt_manager.build(
            "chat_system"
        )


        langchain_messages = [
            SystemMessage(
                content=system_prompt
            )
        ]


        for message in messages:

            role = message.get("role")

            content = message.get(
                "content",
                ""
            )


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


        response = llm.invoke(
            langchain_messages
        )


        return response.content


    except Exception as e:

        logger.error(
            f"Chat AI generation failed: {str(e)}"
        )


        return (
            "I am currently unable to generate a response. "
            "Please try again later."
        )
