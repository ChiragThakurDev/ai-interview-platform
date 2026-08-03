from app.ai.middleware import AIMiddleware


class FakeProvider:

    model_name = "fake-model"

    def generate(self, prompt):

        return "hello"


def test_middleware():

    middleware = AIMiddleware(FakeProvider())

    result = middleware.generate("hi")

    assert result["response"] == "hello"

    assert result["telemetry"]["model"] == "fake-model"

    assert result["telemetry"]["success"] is True
