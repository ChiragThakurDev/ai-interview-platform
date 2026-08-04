# app/services/livekit_service.py

from livekit import api

from app.core.config import settings


class LiveKitService:


    # =====================================
    # Generate LiveKit Access Token
    # =====================================

    def create_token(
        self,
        room_name: str,
        participant_identity: str,
        participant_name: str,
    ):

        token = (
            api.AccessToken(
                settings.livekit_api_key,
                settings.livekit_api_secret,
            )
            .with_identity(
                participant_identity
            )
            .with_name(
                participant_name
            )
            .with_grants(
                api.VideoGrants(
                    room_join=True,
                    room=room_name,

                    # Camera + microphone
                    can_publish=True,

                    # Receive other participants
                    can_subscribe=True,

                    # Allow data messages
                    can_publish_data=True,
                )
            )
            .to_jwt()
        )

        return token



    # =====================================
    # Create Interview Room Name
    # =====================================

    def create_room_name(
        self,
        interview_id: int,
    ):

        return (
            f"interview-room-{interview_id}"
        )



    # =====================================
    # Generate Complete Interview Token
    # =====================================

    def generate_interview_token(
        self,
        interview_id: int,
        user_id: int,
        user_name: str,
    ):

        room_name = self.create_room_name(
            interview_id
        )


        token = self.create_token(
            room_name=room_name,
            participant_identity=str(
                user_id
            ),
            participant_name=user_name,
        )


        return {
            "room": room_name,
            "token": token,
            "url": settings.livekit_url,
        }
