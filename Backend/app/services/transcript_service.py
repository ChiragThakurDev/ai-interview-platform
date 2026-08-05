from sqlalchemy.orm import Session

from app.repositories.transcript_repository import TranscriptRepository


class TranscriptService:


    def __init__(self):

        self.repository = TranscriptRepository()



    def save_transcript_segments(
        self,
        db: Session,
        interview_id: int,
        question_id: int,
        result: dict,
        speaker: str = "candidate",
    ):

        transcripts = []


        segments = result.get(
            "segments",
            []
        )


        language = result.get(
            "language"
        )


        for segment in segments:


            transcript = self.repository.create(

                db=db,

                interview_id=interview_id,

                question_id=question_id,

                speaker=speaker,

                transcript=segment.get(
                    "text",
                    ""
                ),

                language=language,

                start_time=segment.get(
                    "start"
                ),

                end_time=segment.get(
                    "end"
                ),

            )


            transcripts.append(
                transcript
            )


        return transcripts
