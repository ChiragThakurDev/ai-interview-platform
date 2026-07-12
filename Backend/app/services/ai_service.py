import json

from app.ai.llm import get_llm
from app.ai.prompts import (RESUME_ANALYSIS_PROMPT, INTERVIEW_GENERATION_PROMPT,)
from app.schemas.ai import (ResumeAnalysisResponse, AIInterviewResponse,)


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


    def generate_interview_questions(
            self,
            resume_text:str,
            role:str,
            difficulty:str,
            number_of_questions:int,
    ):
        prompt=INTERVIEW_GENERATION_PROMPT.format(
                resume=resume_text,
                role=role,
                difficulty=difficulty,
                number_of_questions=number_of_questions,
            )

        response =self.llm.invoke(prompt)

        data=json.loads(response.content)

        return AIInterviewResponse.model_validate(data)




