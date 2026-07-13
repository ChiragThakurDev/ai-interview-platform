import json

from app.ai.llm import get_llm
from app.ai.prompts import (RESUME_ANALYSIS_PROMPT, INTERVIEW_GENERATION_PROMPT, ANSWER_EVALUATION_PROMPT,INTERVIEW_REPORT_PROMPT,)
from app.schemas.ai import (ResumeAnalysisResponse, AIInterviewResponse, AIAnswerEvaluationResponse,)

from app.schemas.interview_report import (
    InterviewReportResponse,
)


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

    def generate_interview_report(
    self,
    results: str,
    ):
        prompt = INTERVIEW_REPORT_PROMPT.format(
        results=results
        )

        response = self.llm.invoke(prompt)

        data = json.loads(response.content)

        return InterviewReportResponse.model_validate(data)

    def evaluate_answer(
            self,
            question:str,
            answer:str,
    ):
        prompt=ANSWER_EVALUATION_PROMPT.format(
                question=question,
                answer=answer,
        )

        response =self.llm.invoke(prompt)

        data=json.loads(response.content)

        return AIAnswerEvaluationResponse.model_validate(data)




