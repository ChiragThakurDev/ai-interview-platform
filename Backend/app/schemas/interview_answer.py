from datetime import datetime

from pydantic import BaseModel


class SubmitAnswerRequest(BaseModel):
    answer: str


class InterviewAnswerResponse(BaseModel):
    id: int
    question_id: int
    answer: str
    score: int
    feedback: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
