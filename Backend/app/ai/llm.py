from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.1:8b",
    base_url="http://host.docker.internal:11434",
    temperature=0.3,
)

def get_llm():
    return llm
