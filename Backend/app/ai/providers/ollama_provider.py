from langchain_ollama import ChatOllama


class OllamaProvider:

    def __init__(self):

        self.llm = ChatOllama(
            model="llama3.1:8b",
            base_url="http://host.docker.internal:11434",
            #base_url="http://127.0.0.1:11434",
            temperature=0.3,
        )


    def generate(
        self,
        prompt: str,
    ):

        response = self.llm.invoke(
            prompt
        )

        return response.content


    def chat(
        self,
        messages,
    ):

        response = self.llm.invoke(
            messages
        )

        return response.content
