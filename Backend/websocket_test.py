import asyncio
import json
import websockets


async def main():
    uri = "ws://127.0.0.1:5000/ws/coding-interview/4"

    async with websockets.connect(uri) as websocket:

        await websocket.send(json.dumps({
            "message": "Hello Backend"
        }))

        response = await websocket.recv()

        print(response)


asyncio.run(main())
