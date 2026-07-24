from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(
        self,
        interview_id: int,
        websocket: WebSocket,
    ):
        await websocket.accept()
        self.active_connections[interview_id] = websocket

    def disconnect(
        self,
        interview_id: int,
    ):
        self.active_connections.pop(interview_id, None)

    async def send_message(
        self,
        interview_id: int,
        message: dict,
    ):
        websocket = self.active_connections.get(interview_id)

        if websocket:
            await websocket.send_json(message)


manager = ConnectionManager()
