from typing import Any


class AIMemory:

    def __init__(self):

        self.memory = {}

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.memory[key] = value

    def get(
        self,
        key: str,
        default=None,
    ):

        return self.memory.get(
            key,
            default,
        )

    def delete(
        self,
        key: str,
    ) -> None:

        self.memory.pop(
            key,
            None,
        )

    def clear(
        self,
    ) -> None:

        self.memory.clear()

    def all(
        self,
    ):

        return self.memory
