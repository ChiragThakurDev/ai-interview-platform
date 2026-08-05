import asyncio
import websockets

AUDIO_FILE =("/home/chirag/Downloads/LearningEnglishConversations-20260804-TheEnglishWeSpeakKeepYourselfToYourself.mp3")


async def test():

    uri = (
        "ws://127.0.0.1:8000"
        "/ws/interview/2/audio"
    )

    async with websockets.connect(uri) as ws:

        print("✅ Connected")

        with open(AUDIO_FILE, "rb") as audio:

            while True:

                chunk = audio.read(4096)

                if not chunk:
                    break


                await ws.send(chunk)

                print(
                    f"sent {len(chunk)} bytes"
                )


                await asyncio.sleep(0.1)


        print("🎤 Audio upload finished")


        try:

            while True:

                response = await ws.recv()

                print(
                    "SERVER:",
                    response
                )


        except Exception:

            pass



asyncio.run(test())
