"""
Runtime Bootstrap.

Converts a database Interview into an InterviewRuntime.

Future:
- Resume checkpoints
- Redis restore
- Adaptive interview state restore
"""

from app.models.interview import Interview
from app.interview_runtime.manager import runtime_manager


class RuntimeBootstrap:

    def build(
        self,
        interview: Interview,
        total_questions: int,
    ):

        runtime = runtime_manager.get(interview.id)

        runtime.progress.total_questions = total_questions

        runtime.engine.flow.state.current_question = (
            interview.current_question
            if interview.current_question > 0
            else 1
        )

        if interview.status == "in_progress":
            runtime.started = True

        if interview.status == "completed":
            runtime.started = True
            runtime.finished = True

        return runtime
