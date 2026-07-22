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


    # Remove markdown formatting

    cleaned_response = (
        response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )


    # Try direct JSON parsing

    try:

        return json.loads(
            cleaned_response
        )


    except json.JSONDecodeError:

        logger.warning(
            "Direct JSON parsing failed. Trying extraction..."
        )


    # Extract JSON object from text

    try:

        start = cleaned_response.index("{")

        end = (
            cleaned_response.rindex("}")
            + 1
        )

        json_text = cleaned_response[start:end]


        return json.loads(
            json_text
        )


    except Exception as error:

        logger.error(
            "Failed to parse AI JSON response: %s",
            error,
        )


        return {
            "error": "Invalid AI response",
            "raw_response": response,
        }
