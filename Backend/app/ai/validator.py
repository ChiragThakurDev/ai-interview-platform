"""
AI response validation.
"""

import json


def validate_json_response(
    text: str,
):

    try:

        json.loads(text)

        return True

    except json.JSONDecodeError:

        return False
