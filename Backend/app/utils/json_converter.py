import json
from typing import Any


def serialize_test_data(
    data: Any
) -> str:

    """
    Convert AI generated test data
    into database safe string format.

    Handles:
    - list
    - dict
    - string
    - integer
    - boolean
    """

    if isinstance(
        data,
        (list, dict)
    ):
        return json.dumps(
            data
        )


    return str(data)
