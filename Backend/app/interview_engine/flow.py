"""
Interview flow.
"""

from app.interview_engine.state import InterviewState


class InterviewFlow:

    def __init__(self):

        self.state = InterviewState()

    def next(self):

        self.state.next_question()

    def finish(self):

        self.state.finish()

    def completed(self):

        return self.state.completed
