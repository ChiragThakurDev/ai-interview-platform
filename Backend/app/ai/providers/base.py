from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def generate(self, prompt: str):
        pass

    @abstractmethod
    def chat(self, messages):
        pass

    @abstractmethod
    def stream(self, prompt: str):
        pass

    @abstractmethod
    def stream_chat(self, messages):
        pass
