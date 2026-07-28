from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

from app.core.config import settings


class AIProvider:

    def __init__(self):

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

    return ChatOllama(

        model=settings.ollama_model,

        base_url=settings.ollama_url,

        temperature=0.1,

        format="json"

    )



def get_ai_provider():

    return AIProvider()
