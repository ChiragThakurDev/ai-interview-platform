"""
Simple retry helper for AI providers.
"""

import time


def retry(
    func,
    retries: int = 2,
    delay: float = 1.0,
):

    last_exception = None

    for _ in range(retries):

        try:
            return func()

        except Exception as e:

            last_exception = e

            time.sleep(delay)

    raise last_exception
