import logging
import time

from sqlalchemy.orm import Session

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)

from app.ai.factory import AIFactory
from app.ai.prompt_loader import PromptLoader

from app.repositories.prompt_repository import (
    PromptRepository,
)
from app.repositories.prompt_execution_repository import (
    PromptExecutionRepository,
)

from app.services.prompt_service import (
    PromptService,
)
from app.services.prompt_execution_service import (
    PromptExecutionService,
)


logger = logging.getLogger(__name__)


def chat_chain(
    messages: list[dict],
    db: Session,
) -> str:
    """
    AI Chat conversation chain.
    """

    prompt = None
    system_prompt = ""

    prompt_repository = PromptRepository(db)
    prompt_service = PromptService(prompt_repository)

    execution_repository = PromptExecutionRepository(db)
    execution_service = PromptExecutionService(
        execution_repository
    )

    try:

        # -----------------------------
        # Get chat model
        # -----------------------------

        provider = AIFactory.chat()
        llm = provider.llm

        # -----------------------------
        # Load active prompt
        # -----------------------------

        prompt = prompt_service.get_active_prompt(
            "chat"
        )

        if prompt is None:
            raise ValueError(
                "No active chat prompt found."
            )

        prompt_loader = PromptLoader(
            prompt_service
        )

        variables = {}

        system_prompt = prompt_loader.load(
            name="chat",
            variables=variables,
        )

        # -----------------------------
        # Build LangChain messages
        # -----------------------------

        langchain_messages = [
            SystemMessage(
                content=system_prompt
            )
        ]

        for message in messages:

            role = message.get("role")
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

        # -----------------------------
        # Invoke LLM
        # -----------------------------

        start = time.perf_counter()

        response = llm.invoke(
            langchain_messages
        )

        latency = (
            time.perf_counter() - start
        )

        # -----------------------------
        # Log execution
        # -----------------------------

        execution_service.log_execution(
            prompt=prompt,
            variables=variables,
            rendered_prompt=system_prompt,
            response=response.content,
            success=True,
            latency=latency,
        )

        return response.content

    except Exception as e:

        logger.exception(
            "Chat AI generation failed"
        )

        if prompt is not None:

            try:

                execution_service.log_execution(
                    prompt=prompt,
                    variables={},
                    rendered_prompt=system_prompt,
                    response=str(e),
                    success=False,
                    latency=None,
                )

            except Exception:

                logger.exception(
                    "Failed to save prompt execution log"
                )

        return (
            "I am currently unable to generate a response. "
            "Please try again later."
        )
