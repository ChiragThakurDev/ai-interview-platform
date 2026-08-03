"""
Interview session.
"""

import uuid

from app.interview_engine.state import InterviewState


class InterviewSession:

    def __init__(self):

        self.id = str(uuid.uuid4())

        self.state = InterviewState()

    def reset(self):

        self.state.reset()
