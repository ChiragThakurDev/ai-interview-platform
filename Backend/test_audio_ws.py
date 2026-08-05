import asyncio
import websockets


URI = "ws://127.0.0.1:8000/ws/interview/2/audio"

AUDIO_FILE = "/home/chirag/Downloads/LearningEnglishConversations-20260804-TheEnglishWeSpeakKeepYourselfToYourself.mp3"


async def test():

    async with websockets.connect(
        URI
    ) as ws:

        print("✅ Connected")


        with open(
            AUDIO_FILE,
            "rb"
        ) as audio:

            data = audio.read()


            await ws.send(data)


            print(
                f"Sent {len(data)} bytes"
            )


        response = await ws.recv()

        print(
            response
        )


asyncio.run(test())
