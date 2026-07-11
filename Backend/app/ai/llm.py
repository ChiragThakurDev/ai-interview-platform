from langchain_ollama import ChatOllama

llm=ChatOllama(
        model="llama3.1:8b",
        temperature=0.3,
)

def get_llm():
    return llm
