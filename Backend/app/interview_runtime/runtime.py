"""
Interview Runtime.

Coordinates interview execution.
"""

from app.interview_engine.engine import InterviewEngine
from app.interview_runtime.progress import InterviewProgress
from app.interview_runtime.timer import InterviewTimer


class InterviewRuntime:

    def __init__(
        self,
        total_questions: int = 10,
        duration_minutes: int = 30,
    ):

        self.engine = InterviewEngine()

        self.timer = InterviewTimer(duration_minutes)

        self.progress = InterviewProgress(total_questions)

        self.started = False

        self.finished = False

    # =====================================================
    # Lifecycle
    # =====================================================

    def start(self):

        self.started = True
        self.finished = False

        self.timer.start()

    def finish(self):

        self.finished = True

        self.engine.flow.finish()

    def reset(self):

        self.engine.flow.state.reset()

        self.progress.reset()

        self.timer.reset()

        self.started = False

        self.finished = False

    # =====================================================
    # Interview Actions
    # =====================================================

    def submit_answer(
        self,
        score: float,
    ):

        self.progress.answer(score)

        self.engine.flow.next()

    def skip(self):

        self.progress.skip()

        self.engine.flow.next()

    # Alias expected by InterviewController
    def skip_question(self):

        self.skip()

    # =====================================================
    # Runtime Properties
    # =====================================================

    @property
    def completed(self):

        return self.engine.flow.completed()

    @property
    def current_question(self):

        return self.engine.flow.state.current_question
