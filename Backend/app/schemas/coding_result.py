from pydantic import BaseModel
from typing import List


class CodingInterviewResultResponse(BaseModel):

    interview_id: int

    role: str

    company: str | None

    score: int

    performance: str

    total_questions: int

    attempted_questions: int

    passed_questions: int

    failed_questions: int

    average_score: float

    strengths: List[str]

    weaknesses: List[str]

    ai_summary: str
