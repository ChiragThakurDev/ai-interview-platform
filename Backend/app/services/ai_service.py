import logging

from app.services.ai.resume_ai_service import ResumeAIService
from app.services.ai.interview_ai_service import InterviewAIService
from app.services.ai.evaluation_ai_service import EvaluationAIService
from app.services.ai.report_ai_service import ReportAIService
from app.services.ai.coding_ai_service import CodingAIService
from app.services.ai.roadmap_ai_service import RoadmapAIService

logger = logging.getLogger(__name__)


class AIService:

    def __init__(self):

        self.resume = ResumeAIService()

        self.interview = InterviewAIService()

        self.evaluation = EvaluationAIService()

        self.report = ReportAIService()

        self.coding = CodingAIService()

        self.roadmap = RoadmapAIService()

    # =====================================================
    # Resume
    # =====================================================

    def analyze_resume(
        self,
        resume_text: str,
    ):
        return self.resume.analyze_resume(
            resume_text
        )

    # =====================================================
    # Interview Questions
    # =====================================================

    def generate_interview_questions(
        self,
        resume_text: str,
        role: str,
        difficulty: str,
        number_of_questions: int,
    ):
        return self.interview.generate_questions(
            resume_text=resume_text,
            role=role,
            difficulty=difficulty,
            number_of_questions=number_of_questions,
        )

    # =====================================================
    # Interview Answer Evaluation
    # =====================================================

    def evaluate_answer(
        self,
        question: str,
        answer: str,
    ):
        return self.evaluation.evaluate_answer(
            question=question,
            answer=answer,
        )

    # =====================================================
    # Interview Report
    # =====================================================

    def generate_interview_report(
        self,
        results: str,
    ):
        return self.report.generate_interview_report(
            results
        )

    # =====================================================
    # Skill Report
    # =====================================================

    def generate_skill_report(
        self,
        results: str,
    ):
        return self.report.generate_skill_report(
            results
        )

    # =====================================================
    # Learning Roadmap
    # =====================================================

    def generate_learning_roadmap(
        self,
        skill_report: str,
    ):
        return self.roadmap.generate_learning_roadmap(
            skill_report
        )

    # =====================================================
    # Coding Interview
    # =====================================================

    def generate_coding_questions(
        self,
        role: str,
        company: str | None,
        language: str,
        difficulty: str,
        number_of_questions: int,
    ):
        return self.coding.generate_coding_questions(
            role=role,
            company=company,
            language=language,
            difficulty=difficulty,
            number_of_questions=number_of_questions,
        )

    # =====================================================
    # Coding Evaluation
    # =====================================================

    def evaluate_code(
        self,
        question: str,
        language: str,
        code: str,
        execution_output: str,
        execution_error: str,
    ):
        return self.coding.evaluate_code(
            question=question,
            language=language,
            code=code,
            execution_output=execution_output,
            execution_error=execution_error,
        )

    # =====================================================
    # Coding Report
    # =====================================================

    def generate_coding_report(
        self,
        results: str,
    ):
        return self.coding.generate_coding_report(
            results
        )
