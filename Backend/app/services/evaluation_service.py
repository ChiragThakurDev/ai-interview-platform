import json

from app.repositories.evaluation_repository import (
    EvaluationRepository,
)

from app.ai.llm import get_llm



class EvaluationService:


    def __init__(self):

        self.repository = EvaluationRepository()

        self.llm = get_llm()



    def evaluate_answer(
        self,
        db,
        interview_id: int,
        question_id: int,
        question: str,
        answer: str,
    ):


        prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate answer.

Question:
{question}


Candidate Answer:
{answer}


Return ONLY valid JSON.

Format:

{{
    "technical_score": number,
    "communication_score": number,
    "confidence_score": number,
    "overall_score": number,

    "feedback": "text",

    "strengths": [
        "item"
    ],

    "weaknesses": [
        "item"
    ]
}}

Rules:

- Scores must be between 0 and 100.
- Be strict like a real interviewer.
- Evaluate correctness, clarity and confidence.
"""


        response = self.llm.invoke(
            prompt
        )


        content = response.content


        try:

            evaluation = json.loads(
                content
            )


        except Exception:


            evaluation = {

                "technical_score": 0,

                "communication_score": 0,

                "confidence_score": 0,

                "overall_score": 0,

                "feedback": content,

                "strengths": [],

                "weaknesses": [
                    "AI response parsing failed"
                ],

            }



        saved = self.repository.create(

            db=db,

            interview_id=interview_id,

            question_id=question_id,

            technical_score=evaluation.get(
                "technical_score"
            ),

            communication_score=evaluation.get(
                "communication_score"
            ),

            confidence_score=evaluation.get(
                "confidence_score"
            ),

            overall_score=evaluation.get(
                "overall_score"
            ),

            feedback=evaluation.get(
                "feedback"
            ),

            strengths=evaluation.get(
                "strengths"
            ),

            weaknesses=evaluation.get(
                "weaknesses"
            ),

        )


        return saved
