import os
import tempfile
import logging

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from app.speech.factory import SpeechFactory
from app.db.session import SessionLocal

from app.services.transcript_service import (
    TranscriptService,
)

from app.services.silence_detector import (
    SilenceDetector,
)

from app.services.interview_evaluation_runtime import (
    InterviewEvaluationRuntime,
)

from app.services.interview_question_service import (
    InterviewQuestionService,
)

from app.interview_runtime import session_manager

from app.services.interview_report_runtime import (
    InterviewReportRuntime,
)

from app.services.interview_runtime_service import (
    InterviewRuntimeService,
)

logger = logging.getLogger(__name__)

router = APIRouter()

speech_provider = SpeechFactory.get_provider()

transcript_service = TranscriptService()

evaluation_runtime = InterviewEvaluationRuntime()

report_runtime = InterviewReportRuntime()


@router.websocket("/ws/interview/{interview_id}/audio")
async def audio_stream(
    websocket: WebSocket,
    interview_id: int,
):
    await websocket.accept()

    logger.info(
        "🎤 Audio stream started: %s",
        interview_id,
    )

    db = SessionLocal()

    question_service = InterviewQuestionService(db)

    runtime_service = InterviewRuntimeService(
        db=db,
    )

    buffer = bytearray()

    silence_detector = SilenceDetector(
        silence_seconds=3.0,
    )

    evaluated = False
    audio_path = None

    try:
        while True:
            audio_chunk = await websocket.receive_bytes()

            buffer.extend(audio_chunk)

            silence_detector.update()

            if len(buffer) < 200000:
                continue

            try:
                with tempfile.NamedTemporaryFile(
                    suffix=".mp3",
                    delete=False,
                ) as temp:
                    temp.write(buffer)
                    audio_path = temp.name

                result = speech_provider.transcribe(audio_path)

                question_id = session_manager.get_current_question(
                    interview_id
                )

                if question_id is None:
                    question_id = 1

                saved = transcript_service.save_transcript_segments(
                    db=db,
                    interview_id=interview_id,
                    question_id=question_id,
                    result=result,
                    speaker="candidate",
                )

                await websocket.send_json(
                    {
                        "type": "transcript",
                        "interview_id": interview_id,
                        "question_id": question_id,
                        "text": result.get(
                            "transcript",
                            "",
                        ),
                        "segments": result.get(
                            "segments",
                            [],
                        ),
                        "saved": len(saved),
                    }
                )

                if silence_detector.is_silent() and not evaluated:

                    logger.info(
                        "Candidate stopped speaking. Starting evaluation..."
                    )

                    evaluation = (
                        evaluation_runtime.evaluate_question(
                            db=db,
                            interview_id=interview_id,
                            question_id=question_id,
                            question="Current Interview Question",
                        )
                    )

                    await websocket.send_json(
                        {
                            "type": "evaluation",
                            "question_id": question_id,
                            "result": evaluation,
                        }
                    )

                    evaluated = True

                    next_question = (
                        question_service.get_next_question(
                            interview_id=interview_id,
                            current_question_id=question_id,
                        )
                    )

                    if next_question:

                        session_manager.update_question(
                            interview_id,
                            next_question.id,
                        )

                        await websocket.send_json(
                            {
                                "type": "next_question",
                                "question_id": next_question.id,
                                "question": next_question.question,
                                "difficulty": next_question.difficulty,
                                "category": next_question.category,
                            }
                        )

                        # Prepare for next question
                        evaluated = False
                        silence_detector.reset()
                        buffer.clear()

                    else:

                        logger.info("Interview completed.")

                        try:

                            report = report_runtime.generate(
                                db=db,
                                interview_id=interview_id,
                            )

                            runtime_service.finish_runtime(
                                interview_id
                            )

                            await websocket.send_json(
                                {
                                    "type": "interview_completed",
                                    "interview_id": interview_id,
                                    "report": report,
                                }
                            )

                            logger.info(
                                "Interview report generated successfully."
                            )

                        except Exception:

                            logger.exception(
                                "Failed to generate interview report."
                            )

                            await websocket.send_json(
                                {
                                    "type": "interview_completed",
                                    "interview_id": interview_id,
                                    "report": None,
                                }
                            )

                        break

            finally:
                if audio_path and os.path.exists(audio_path):
                    os.remove(audio_path)
                    audio_path = None

    except WebSocketDisconnect:

        logger.info(
            "❌ Audio disconnected: %s",
            interview_id,
        )

    except Exception as e:

        logger.exception(
            "Audio processing failed"
        )

        await websocket.send_json(
            {
                "type": "error",
                "message": str(e),
            }
        )

    finally:
        buffer.clear()
        db.close()