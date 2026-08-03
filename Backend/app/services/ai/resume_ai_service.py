from app.ai.factory import AIFactory
from app.ai.parser import parse_json_response
from app.ai.prompt_manager import PromptManager


class ResumeAIService:
    """
    Resume analysis AI service.

    Uses database-backed prompt versioning.
    """

    def __init__(self):

        self.ai = AIFactory.general()

        self.prompt_manager = PromptManager()


    def analyze_resume(
        self,
        resume_text: str,
    ):


        prompt = self.prompt_manager.build(
            "resume_analysis",
            resume=resume_text,
        )


        response = self.ai.generate(
            prompt
        )


        data = parse_json_response(
            response
        )


        return data
