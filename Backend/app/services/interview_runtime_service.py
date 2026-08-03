"""
Interview Runtime Service.

Acts as the application layer between InterviewService
and the Interview Runtime subsystem.
"""

from app.interview_runtime.controller import InterviewController


class InterviewRuntimeService:

    def __init__(self):
        self.controller = InterviewController()

    def start_runtime(
        self,
        interview_id: int,
    ):
        return self.controller.start(interview_id)

    def submit_answer(
        self,
        interview_id: int,
        score: float,
    ):
        return self.controller.submit_answer(
            interview_id,
            score,
        )

    def skip_question(
        self,
        interview_id: int,
    ):
        return self.controller.skip_question(interview_id)

    def finish_runtime(
        self,
        interview_id: int,
    ):
        return self.controller.finish(interview_id)

    def get_runtime(
        self,
        interview_id: int,
    ):
        return self.controller.get_runtime(interview_id)

    def remove_runtime(
        self,
        interview_id: int,
    ):
        self.controller.remove_runtime(interview_id)
