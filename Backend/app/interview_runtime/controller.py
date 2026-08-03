"""
Interview Controller.

High-level API over InterviewRuntime.

Controllers should be used by services.
"""

from app.interview_runtime.manager import runtime_manager


class InterviewController:

    def __init__(self):
        pass

    def start(
        self,
        interview_id: int,
    ):

        runtime = runtime_manager.get(interview_id)

        runtime.start()

        return runtime

    def submit_answer(
        self,
        interview_id: int,
        score: float,
    ):

        runtime = runtime_manager.get(interview_id)

        runtime.submit_answer(score)

        return runtime

    def skip_question(
        self,
        interview_id: int,
    ):

        runtime = runtime_manager.get(interview_id)

        runtime.skip_question()

        return runtime

    def finish(
        self,
        interview_id: int,
    ):

        runtime = runtime_manager.get(interview_id)

        runtime.finish()

        return runtime

    def get_runtime(
        self,
        interview_id: int,
    ):

        return runtime_manager.get(interview_id)

    def remove_runtime(
        self,
        interview_id: int,
    ):

        runtime_manager.delete(interview_id)
