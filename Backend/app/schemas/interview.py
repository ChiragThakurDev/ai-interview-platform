from pydantic import BaseModel


class GenerateInterviewRequest(BaseModel):
    role: str
    difficulty: str = "medium"
    number_of_questions: int = 10


class InterviewQuestionResponse(BaseModel):
    question: str


class GenerateInterviewResponse(BaseModel):
    questions: list[InterviewQuestionResponse]
