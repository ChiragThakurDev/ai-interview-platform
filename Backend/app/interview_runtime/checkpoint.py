"""
Interview Checkpoint Manager.

Stores runtime state so an interview
can be resumed later.
"""


class CheckpointManager:

    def __init__(self):

        self._checkpoint = {}

    def save(self, runtime):

        self._checkpoint = {
            "started": runtime.started,
            "question": runtime.current_question,
            "answered": runtime.progress.answered_questions,
            "skipped": runtime.progress.skipped_questions,
            "score": runtime.progress.total_score,
        }

    def load(self):

        return self._checkpoint

    def exists(self):

        return bool(self._checkpoint)

    def clear(self):

        self._checkpoint = {}
