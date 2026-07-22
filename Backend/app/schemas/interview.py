from datetime import datetime

from pydantic import BaseModel, ConfigDict


# =====================================================
# Generate Interview
# =====================================================

class GenerateInterviewRequest(BaseModel):
    role: str
    company: str | None = None
    difficulty: str = "medium"
    number_of_questions: int = 10


class InterviewQuestionResponse(BaseModel):
    question: str


class InterviewResponse(BaseModel):
    id: int
    user_id: int
    resume_id: int
    title: str
    role: str
    company: str | None = None
    difficulty: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class InterviewListResponse(BaseModel):
    id: int
    user_id: int
    resume_id: int
    title: str
    role: str
    company: str | None = None
    difficulty: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class GenerateInterviewResponse(BaseModel):
    interview: InterviewResponse
    questions: list[InterviewQuestionResponse]


# =====================================================
# Interview Session
# =====================================================

class StartInterviewResponse(BaseModel):
    interview_id: int
    status: str
    current_question: int
    question: str


class CurrentQuestionResponse(BaseModel):
    interview_id: int
    current_question: int
    total_questions: int
    question: str


class SubmitAnswerRequest(BaseModel):
    answer: str


class SubmitAnswerResponse(BaseModel):
    interview_completed: bool
    current_question: int | None = None
    next_question: str | None = None
    score: int | None = None
    feedback: str | None = None
    message: str


class FinishInterviewResponse(BaseModel):
    interview_id: int
    status: str
    score: int | None = None
    duration: int | None = None
    message: str
