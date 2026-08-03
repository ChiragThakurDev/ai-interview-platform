"""
Prompt cache.
"""

import hashlib


def prompt_hash(
    prompt: str,
) -> str:

    return hashlib.sha256(
        prompt.encode()
    ).hexdigest()
