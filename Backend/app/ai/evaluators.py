import time
import logging

from app.ai.chains import chat_chain
from app.ai.parser import parse_json_response
from app.ai.models import CHAT_MODEL


logger = logging.getLogger(__name__)


def evaluate_ai_response(
    messages: list[dict],
):
    """
    Evaluate an AI chat response with timing metadata.

    Uses the chat_chain which routes through AIFactory.chat()
    → llama3.2:3b with the configured chat settings.
    """

    start_time = time.time()

    response = chat_chain(messages)

    parsed_response = parse_json_response(response)

    response_time = time.time() - start_time

    return {

        "data": parsed_response,

        "metadata": {

            "response_time": round(response_time, 3),

            # Read model name from central registry, not hardcoded
            "model": CHAT_MODEL,

        }

    }
