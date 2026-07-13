from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GenerateInterviewRequest(BaseModel):
    role: str
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
    difficulty: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

class InterviewListResponse(BaseModel):
    id:int
    user_id:int
    resume_id:int
    title:str
    role:str
    difficulty:str
    created_at:datetime

    model_config=ConfigDict(
            from_attributes=True)

class GenerateInterviewResponse(BaseModel):
    interview: InterviewResponse
    questions: list[InterviewQuestionResponse]
