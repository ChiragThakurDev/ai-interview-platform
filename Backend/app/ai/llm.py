from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

from app.core.config import settings


class AIProvider:

    def __init__(self):

        # format="json" forces structured JSON output — used for all AI analysis
        self.llm = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_url,
            temperature=0.1,
            format="json"
        )


    def generate(
        self,
        prompt: str
    ) -> str:

        response = self.llm.invoke(
            [
                HumanMessage(
                    content=prompt
                )
            ]
        )

        return response.content



def get_llm():
    """LLM for structured JSON output (analysis, reports, evaluations)."""
    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_url,
        temperature=0.1,
        format="json"
    )


def get_chat_llm():
    """LLM for free-form conversational responses — NO json format constraint."""
    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_url,
        temperature=0.7,
        # No format="json" — returns natural language
    )


def get_ai_provider():

    return AIProvider()
