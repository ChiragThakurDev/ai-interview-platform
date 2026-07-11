import json

from app.ai.llm import get_llm
from app.ai.prompts import RESUME_ANALYSIS_PROMPT
from app.schemas.ai import ResumeAnalysisResponse


class AIService:
    def __init__(self):
        self.llm=get_llm()


    def analyze_resume(self, resume_text:str):

        prompt=RESUME_ANALYSIS_PROMPT.format(
                resume=resume_text
            )

        response=self.llm.invoke(prompt)

        data=json.loads(response.content)

        return ResumeAnalysisResponse.model_validate(data)


