import logging

from app.ai.llm import get_ai_provider
from app.ai.parser import parse_json_response

from app.ai.prompts import (
        RESUME_ANALYSIS_PROMPT,
        INTERVIEW_GENERATION_PROMPT,
        ANSWER_EVALUATION_PROMPT,
        INTERVIEW_REPORT_PROMPT,
        SKILL_ANALYSIS_PROMPT,
        ROADMAP_PROMPT,
        )

from app.schemas.ai import (
        ResumeAnalysisResponse,
        AIInterviewResponse,
        AIAnswerEvaluationResponse,
        AISkillReportResponse,
        )

from app.schemas.interview_report import (
        AIInterviewReportResponse,
        )

from app.schemas.roadmap import (
        LearningRoadmapResponse,
        )
from app.ai.prompts import (
        CODING_INTERVIEW_GENERATION_PROMPT,
        CODING_EVALUATION_PROMPT,
        CODING_INTERVIEW_REPORT_PROMPT,
        )

logger = logging.getLogger(__name__)


class AIService:

    def __init__(self):
        self.ai = get_ai_provider()

    # =====================================================
    # Resume Analysis
    # =====================================================

    def analyze_resume(
            self,
            resume_text: str,
            ):

        prompt = RESUME_ANALYSIS_PROMPT.format(
                resume=resume_text
                )

        response = self.ai.generate(
                prompt
                )

        data = parse_json_response(
                response
                )

        return ResumeAnalysisResponse.model_validate(
                data
                )

    # =====================================================
    # Generate Interview Questions
    # =====================================================

    def generate_interview_questions(
            self,
            resume_text: str,
            role: str,
            difficulty: str,
            number_of_questions: int,
            ):

        prompt = INTERVIEW_GENERATION_PROMPT.format(
                resume=resume_text,
                role=role,
                difficulty=difficulty,
                number_of_questions=number_of_questions,
                )

        response = self.ai.generate(
                prompt
                )

        data = parse_json_response(
                response
                )

        return AIInterviewResponse.model_validate(
                data
                )

    # =====================================================
    # Evaluate Interview Answer
    # =====================================================

    def evaluate_answer(
            self,
            question: str,
            answer: str,
            ):

        prompt = ANSWER_EVALUATION_PROMPT.format(
                question=question,
                answer=answer,
                )

        response = self.ai.generate(
                prompt
                )

        data = parse_json_response(
                response
                )

        return AIAnswerEvaluationResponse.model_validate(
                data
                )

    # =====================================================
    # Generate Interview Report
    # =====================================================

    def generate_interview_report(
            self,
            results: str,
            ):

        prompt = INTERVIEW_REPORT_PROMPT.format(
                results=results
                )

        response = self.ai.generate(
                prompt
                )

        data = parse_json_response(
                response
                )

        return AIInterviewReportResponse.model_validate(
                data
                )

    # =====================================================
    # Generate Skill Report
    # =====================================================

    def generate_skill_report(
            self,
            results: str,
            ):

        prompt = SKILL_ANALYSIS_PROMPT.format(
                results=results
                )

        response = self.ai.generate(
                prompt
                )

        data = parse_json_response(
                response
                )

        return AISkillReportResponse.model_validate(
                data
                )

    # =====================================================
    # Generate Learning Roadmap
    # =====================================================

    def generate_learning_roadmap(
            self,
            skill_report: str,
            ):

        prompt = ROADMAP_PROMPT.format(
                skill_report=skill_report
                )

        response = self.ai.generate(
                prompt
                )

        data = parse_json_response(
                response
                )

        return LearningRoadmapResponse.model_validate(
                data
                )


        # =====================================================
    # Generate Coding Interview Questions
    # =====================================================

    def generate_coding_questions(
            self,
            role: str,
            company: str | None,
            language: str,
            difficulty: str,
            number_of_questions: int,
            ):

        prompt = CODING_INTERVIEW_GENERATION_PROMPT.format(
                role=role,
                company=company or "Any",
                language=language,
                difficulty=difficulty,
                number_of_questions=number_of_questions,
                )


        response = self.ai.generate(
                prompt
                )


        data = parse_json_response(
                response
                )


        return data



    # =====================================================
    # Evaluate Coding Submission
    # =====================================================

    def evaluate_code(
            self,
            question: str,
            language: str,
            code: str,
            execution_output: str,
            execution_error: str,
            ):

        prompt = CODING_EVALUATION_PROMPT.format(
                question=question,
                language=language,
                code=code,
                execution_output=execution_output,
                execution_error=execution_error,
                )


        response = self.ai.generate(
                prompt
                )


        data = parse_json_response(
                response
                )


        return data


     # =====================================================
    # Generate Coding Interview Report
    # =====================================================

    def generate_coding_report(
            self,
            results: str,
            ):

        prompt = CODING_INTERVIEW_REPORT_PROMPT.format(
                results=results
                )

        response = self.ai.generate(
                prompt
                )

        data = parse_json_response(
                response
                )

        return data
