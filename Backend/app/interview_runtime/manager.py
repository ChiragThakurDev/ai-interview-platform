"""
Interview Runtime Manager.

Maintains active InterviewRuntime instances.

Current:
    - In-memory storage

Future:
    - Redis
    - PostgreSQL
    - Distributed workers
"""

from typing import Dict

from app.interview_runtime.runtime import InterviewRuntime


class RuntimeManager:

    def __init__(self):
        self._runtimes: Dict[int, InterviewRuntime] = {}

    def create(
        self,
        interview_id: int,
    ) -> InterviewRuntime:

        runtime = InterviewRuntime()

        self._runtimes[interview_id] = runtime

        return runtime

    def get(
        self,
        interview_id: int,
    ) -> InterviewRuntime:

        if interview_id not in self._runtimes:
            return self.create(interview_id)

        return self._runtimes[interview_id]

    def exists(
        self,
        interview_id: int,
    ) -> bool:

        return interview_id in self._runtimes

    def delete(
        self,
        interview_id: int,
    ) -> None:

        self._runtimes.pop(interview_id, None)

    def clear(
        self,
    ) -> None:

        self._runtimes.clear()

    def count(
        self,
    ) -> int:

        return len(self._runtimes)


runtime_manager = RuntimeManager()
