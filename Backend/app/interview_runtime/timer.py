"""
Interview Timer.

Tracks interview duration.
Supports start, pause, resume and expiry checks.
"""

from datetime import datetime, timedelta


class InterviewTimer:

    def __init__(self, duration_minutes: int = 30):
        self.duration = timedelta(minutes=duration_minutes)

        self.started_at = None
        self.paused_at = None

        self.total_paused = timedelta()

        self.running = False

    def start(self):

        self.started_at = datetime.utcnow()

        self.running = True

    def pause(self):

        if self.running:
            self.paused_at = datetime.utcnow()
            self.running = False

    def resume(self):

        if self.paused_at:

            self.total_paused += (
                datetime.utcnow() - self.paused_at
            )

            self.paused_at = None

            self.running = True

    def elapsed(self):

        if not self.started_at:
            return timedelta()

        now = datetime.utcnow()

        if not self.running and self.paused_at:
            now = self.paused_at

        return (
            now
            - self.started_at
            - self.total_paused
        )

    def remaining(self):

        remaining = self.duration - self.elapsed()

        if remaining.total_seconds() < 0:
            return timedelta()

        return remaining

    def expired(self):

        return self.remaining().total_seconds() <= 0

    def reset(self):

        self.started_at = None
        self.paused_at = None

        self.total_paused = timedelta()

        self.running = False
