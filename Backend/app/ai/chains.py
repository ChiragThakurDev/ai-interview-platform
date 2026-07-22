import logging

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from app.ai.llm import get_llm
from app.ai.prompts import CHAT_SYSTEM_PROMPT


logger = logging.getLogger(__name__)



def chat_chain(
    messages: list[dict],
) -> str:
    """
    AI Chat conversation chain.

    Flow:
    User Message
        ↓
    Chat History
        ↓
    LangChain Messages
        ↓
    System Prompt
        ↓
    Ollama LLM
        ↓
    AI Response
    """


    try:

        llm = get_llm()


        langchain_messages = [

            SystemMessage(
                content=CHAT_SYSTEM_PROMPT
            )

        ]


        for message in messages:

            role = message.get(
                "role"
            )

            content = message.get(
                "content",
                "",
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
