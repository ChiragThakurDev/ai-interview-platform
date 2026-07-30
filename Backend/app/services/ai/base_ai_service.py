from app.ai.factory import AIFactory


class BaseAIService:
    """
    Base AI Service.

    Provides shared AI providers.
    All AI services inherit this.
    """


    def __init__(
        self,
        provider_type="json"
    ):

        if provider_type == "chat":
            self.ai = AIFactory.chat()

        elif provider_type == "coding":
            self.ai = AIFactory.coding()

        elif provider_type == "fast":
            self.ai = AIFactory.fast()

        else:
            self.ai = AIFactory.json()
