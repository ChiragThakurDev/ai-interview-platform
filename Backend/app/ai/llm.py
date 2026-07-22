from langchain_ollama import ChatOllama

from app.core.config import settings



def get_llm():

    return ChatOllama(

        model=settings.ollama_model,

        base_url=settings.ollama_url,

        temperature=0.3,

    )



# Backward compatibility
# Used by AIService and older modules

def get_ai_provider():

    return get_llm()
