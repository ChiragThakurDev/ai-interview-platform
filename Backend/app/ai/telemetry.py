import time
import uuid


class Telemetry:

    def __init__(self):
        self.request_id = str(uuid.uuid4())
        self.start = time.time()

        self.model = None
        self.cached = False
        self.retry_count = 0
        self.success = True

    def elapsed(self):

        return round(time.time() - self.start, 3)

    def to_dict(self):

        return {
            "request_id": self.request_id,
            "elapsed": self.elapsed(),
            "model": self.model,
            "cached": self.cached,
            "retry_count": self.retry_count,
            "success": self.success,
        }
