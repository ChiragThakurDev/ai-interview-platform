import json
import logging
from typing import Any


logger = logging.getLogger(__name__)


def parse_json_response(
    response: str | None,
) -> dict[str, Any]:

    """
    Safely convert LLM response into JSON.

    Handles:
    - Normal JSON responses
    - Markdown JSON blocks
    - Extra text around JSON
    - Invalid AI responses
    """

    if not response:

        logger.warning(
            "Empty response received from LLM"
        )

        return {
            "error": "Empty AI response",
            "raw_response": response,
        }


    cleaned_response = (
        response
        .replace("```json", "")
        .replace("```JSON", "")
        .replace("```", "")
        .strip()
    )


    # Direct JSON parsing

    try:

        return json.loads(
            cleaned_response
        )


    except json.JSONDecodeError:

        logger.warning(
            "Direct JSON parsing failed. Extracting JSON..."
        )


    # Safer JSON extraction

    try:

        decoder = json.JSONDecoder()

        start = cleaned_response.index("{")

        json_object, _ = decoder.raw_decode(
            cleaned_response[start:]
        )

        return json_object


    except Exception as error:

        logger.error(
            "Failed parsing LLM JSON: %s",
            error,
        )

        return {
            "error": "Invalid AI response",
            "raw_response": response,
        }
