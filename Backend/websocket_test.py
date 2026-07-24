import asyncio
import json
import requests
import websockets


BASE_URL = "http://127.0.0.1:5000"


EMAIL = "chirag212003@gmail.com"
PASSWORD = "123@chiku"



def get_token():

    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "grant_type": "password",
            "username": EMAIL,
            "password": PASSWORD,
            "scope": "",
            "client_id": "string",
            "client_secret": "",
        },
    )

    response.raise_for_status()

    return response.json()["access_token"]





async def main():


    token = get_token()


    uri = (
        "ws://127.0.0.1:5000/"
        "ws/coding-interview/4"
        f"?token={token}"
    )


    async with websockets.connect(uri) as websocket:


        print("CONNECTED")



        # ==================================
        # START INTERVIEW
        # ==================================

        await websocket.send(
            json.dumps(
                {
                    "type": "start_interview"
                }
            )
        )


        response = await websocket.recv()


        print("\nSTART INTERVIEW RESPONSE:")

        print(response)



        question = json.loads(response)



        question_id = (
            question["question"]["id"]
        )



        # ==================================
        # AUTO SAVE
        # ==================================

        await websocket.send(
            json.dumps(
                {
                    "type": "autosave",

                    "question_id": question_id,

                    "language": "python",

                    "code":
                    "def hello():\n    print('Draft saved')",
                }
            )
        )


        response = await websocket.recv()


        print("\nAUTOSAVE RESPONSE:")

        print(response)



        # ==================================
        # SUBMIT CODE
        # ==================================

        await websocket.send(
            json.dumps(
                {
                    "type": "submit_code",

                    "question_id": question_id,

                    "language": "python",

                    "code":
                    "print('Hello WebSocket')",
                }
            )
        )


        response = await websocket.recv()


        print("\nSUBMISSION RESPONSE:")

        print(response)




asyncio.run(main())
