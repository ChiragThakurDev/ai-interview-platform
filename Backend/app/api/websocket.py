from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.models.coding_interview import CodingInterview

from app.services.coding_interview_service import (
    CodingInterviewService,
)

from app.websocket.connection_manager import manager

from app.utils.jwt import verify_access_token


router = APIRouter(
    tags=["WebSocket"],
)



@router.websocket("/ws/coding-interview/{interview_id}")
async def coding_interview_socket(
    websocket: WebSocket,
    interview_id: int,
):


    db: Session = SessionLocal()


    connected = False


    try:


        # =====================================================
        # JWT AUTHENTICATION
        # =====================================================

        token = websocket.query_params.get(
            "token"
        )


        if not token:

            await websocket.close(
                code=1008,
                reason="Missing token"
            )

            return



        payload = verify_access_token(
            token
        )


        if not payload:

            await websocket.close(
                code=1008,
                reason="Invalid token"
            )

            return



        user_id = payload.get(
            "user_id"
        )


        if not user_id:

            await websocket.close(
                code=1008,
                reason="Invalid user"
            )

            return



        # =====================================================
        # INTERVIEW VALIDATION
        # =====================================================

        interview = (
            db.query(CodingInterview)
            .filter(
                CodingInterview.id == interview_id
            )
            .first()
        )


        if not interview:


            await websocket.close(
                code=1008,
                reason="Interview not found"
            )

            return



        if interview.user_id != user_id:


            await websocket.close(
                code=1008,
                reason="Not authorized"
            )

            return



        # =====================================================
        # CONNECT
        # =====================================================

        await manager.connect(
            interview_id,
            websocket,
        )


        connected = True


        service = CodingInterviewService(
            db
        )



        # =====================================================
        # EVENT LOOP
        # =====================================================

        while True:


            data = await websocket.receive_json()


            event_type = data.get(
                "type"
            )



            # =====================================================
            # START INTERVIEW
            # =====================================================

            if event_type == "start_interview":


                questions = service.get_questions(
                    interview_id
                )


                if not questions:


                    await manager.send_message(

                        interview_id,

                        {
                            "type": "error",

                            "message":
                            "No questions found",
                        },

                    )

                    continue



                first_question = questions[0]



                interview.current_question = 0

                interview.answered_questions = 0

                interview.status = "running"

                db.commit()



                await manager.send_message(

                    interview_id,

                    {

                        "type":
                        "interview_started",


                        "question":
                        {

                            "id":
                            first_question.id,

                            "title":
                            first_question.title,

                            "description":
                            first_question.description,

                            "difficulty":
                            first_question.difficulty,

                        },


                        "total_questions":
                        len(questions),

                    },

                )



            # =====================================================
            # SUBMIT CODE
            # =====================================================

            elif event_type == "submit_code":



                result = service.submit_code(

                    interview_id=interview_id,

                    question_id=data["question_id"],

                    language=data["language"],

                    code=data["code"],

                )



                await manager.send_message(

                    interview_id,

                    {

                        "type":
                        "submission_result",


                        "execution":
                        result["execution"],


                        "evaluation":
                        result["evaluation"],

                    },

                )



                next_question = result.get(
                    "next_question"
                )



                if next_question:


                    await manager.send_message(

                        interview_id,

                        {

                            "type":
                            "next_question",


                            "question":
                            {

                                "id":
                                next_question.id,


                                "title":
                                next_question.title,


                                "description":
                                next_question.description,


                                "difficulty":
                                next_question.difficulty,

                            },

                        },

                    )


                else:


                    await manager.send_message(

                        interview_id,

                        {

                            "type":
                            "interview_completed",


                            "message":
                            "Interview completed",

                        },

                    )



            # =====================================================
            # AUTO SAVE
            # =====================================================

            elif event_type == "autosave":


                draft = service.save_draft(

                    user_id=user_id,

                    question_id=data["question_id"],

                    language=data["language"],

                    code=data["code"],

                )



                await manager.send_message(

                    interview_id,

                    {

                        "type":
                        "draft_saved",


                        "draft_id":
                        draft.id,


                        "updated_at":
                        str(
                            draft.updated_at
                        ),

                    },

                )



            # =====================================================
            # UNKNOWN EVENT
            # =====================================================

            else:


                await manager.send_message(

                    interview_id,

                    {

                        "type":
                        "error",


                        "message":
                        "Unknown message type",

                    },

                )



    except WebSocketDisconnect:


        print(
            "CLIENT DISCONNECTED"
        )



    except Exception as e:


        print(
            "WEBSOCKET ERROR:",
            e
        )


        try:

            await websocket.close(
                code=1011,
                reason="Internal server error"
            )


        except Exception:

            pass



    finally:


        if connected:

            manager.disconnect(
                interview_id
            )


        db.close()
