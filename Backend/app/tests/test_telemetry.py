from app.ai.telemetry import Telemetry


def test_telemetry():

    t = Telemetry()

    assert t.success is True

    assert t.retry_count == 0

    assert isinstance(t.request_id, str)

    assert "elapsed" in t.to_dict()
