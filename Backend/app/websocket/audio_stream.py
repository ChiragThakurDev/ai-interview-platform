import os
import tempfile


from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)


from app.speech.factory import SpeechFactory

from app.db.session import SessionLocal

from app.services.transcript_service import TranscriptService

from app.interview_runtime import session_manager



router = APIRouter()



speech_provider = SpeechFactory.get_provider()


transcript_service = TranscriptService()



@router.websocket(
    "/ws/interview/{interview_id}/audio"
)
async def audio_stream(
    websocket: WebSocket,
    interview_id: int,
):


    await websocket.accept()


    print(
        f"🎤 Audio stream started {interview_id}"
    )



    db = SessionLocal()


    buffer = bytearray()



    try:


        while True:


            audio_chunk = await websocket.receive_bytes()


            buffer.extend(
                audio_chunk
            )



            print(
                f"Received {len(audio_chunk)} bytes"
            )



            #
            # Transcribe after enough audio
            #

            if len(buffer) > 200000:



                with tempfile.NamedTemporaryFile(
                    suffix=".mp3",
                    delete=False,
                ) as temp:


                    temp.write(
                        buffer
                    )


                    audio_path = temp.name




                try:


                    result = speech_provider.transcribe(
                        audio_path
                    )



                    question_id = (
                        session_manager
                        .get_current_question(
                            interview_id
                        )
                    )



                    if question_id is None:


                        question_id = 1




                    #
                    # Save transcript segments
                    #

                    transcripts = (
                        transcript_service
                        .save_transcript_segments(
                            db=db,
                            interview_id=interview_id,
                            question_id=question_id,
                            result=result,
                            speaker="candidate",
                        )
                    )



                    await websocket.send_json(

                        {

                            "type":"transcript",

                            "interview_id":
                                interview_id,

                            "question_id":
                                question_id,

                            "language":
                                result["language"],

                            "text":
                                result["transcript"],

                            "segments":
                                result["segments"],

                            "saved":
                                len(transcripts),

                        }

                    )



                finally:


                    if os.path.exists(
                        audio_path
                    ):


                        os.remove(
                            audio_path
                        )



                buffer.clear()



    except WebSocketDisconnect:


        print(
            f"❌ Audio disconnected {interview_id}"
        )


    finally:


        db.close()
