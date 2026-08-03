class AIException(Exception):
    """Base AI exception."""


class AIProviderError(AIException):
    """Provider failed."""


class AIResponseError(AIException):
    """Invalid AI response."""


class AIJSONParseError(AIException):
    """Failed to parse JSON."""


class AIModelUnavailable(AIException):
    """Model unavailable."""


class AITimeoutError(AIException):
    """LLM request timed out."""
