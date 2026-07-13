from datetime import datetime

from pydantic import BaseModel


class QuestionResultResponse(BaseModel):
    id: int
    question: str
    category: str
    difficulty: str

    answer: str | None = None
    score: int | None = None
    feedback: str | None = None

    class Config:
        from_attributes = True


class InterviewInfoResponse(BaseModel):
    id: int
    title: str
    role: str
    difficulty: str
    created_at: datetime

    class Config:
        from_attributes = True


class InterviewResultResponse(BaseModel):
    interview: InterviewInfoResponse

    average_score: float
    total_questions: int

    questions: list[QuestionResultResponse]
