from pydantic import BaseModel, Field 

class ResumeAnalysisResponse(BaseModel):
    overall_score: int =Field(...,ge=0,le=100)

    strengths: list[str]

    weaknesses: list[str]

    suggestions:list[str]

    recommended_roles: list[str]

    summary: str

class AIInterviewQuestion(BaseModel):
    question: str


class AIInterviewResponse(BaseModel):
    questions: list[AIInterviewQuestion]
