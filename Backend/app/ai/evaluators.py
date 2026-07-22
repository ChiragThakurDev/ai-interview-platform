import time

from app.ai.chains import chat_chain
from app.ai.parsers import parse_json_response



def evaluate_ai_response(
    messages: list[dict],
):

    start_time = time.time()


    response = chat_chain(
        messages
    )


    parsed_response = parse_json_response(
        response
    )


    response_time = (
        time.time() - start_time
    )


    return {

        "data": parsed_response,

        "metadata": {

            "response_time":
                round(
                    response_time,
                    3
                ),

            "model":
                "llama3.1:8b"

        }

    }
