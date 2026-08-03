"""
Central AI Middleware.

Every AI request flows through this middleware before reaching
the underlying provider.

Responsibilities:
- Cache lookup
- Telemetry
- Metrics
- Retry
- History
- Memory
"""

from app.ai.telemetry import Telemetry


class AIMiddleware:

    def __init__(self, provider):
        self.provider = provider

    def generate(self, prompt: str):

        telemetry = Telemetry()

        telemetry.model = getattr(
            self.provider,
            "model_name",
            "unknown",
        )

        response = self.provider.generate(prompt)

        return {
            "response": response,
            "telemetry": telemetry.to_dict(),
        }
