from sqlalchemy.orm import Session

from app.repositories.transcript_repository import TranscriptRepository


class TranscriptAggregator:

    """
    Combines transcript segments into final answer.
    """


    def __init__(self):

        self.repository = TranscriptRepository()



    def get_answer(
        self,
        db: Session,
        interview_id: int,
        question_id: int,
    ) -> str:


        transcripts = (
            self.repository.get_by_question(
                db=db,
                question_id=question_id,
            )
        )


        if not transcripts:
            return ""



        # filter interview

        transcripts = [
            item
            for item in transcripts
            if item.interview_id == interview_id
        ]



        # remove duplicates

        unique_segments = []


        seen = set()


        for item in transcripts:

            key = (
                item.start_time,
                item.end_time,
                item.transcript.strip()
            )


            if key not in seen:

                seen.add(key)

                unique_segments.append(item)



        # sort timeline

        unique_segments.sort(
            key=lambda x:
                x.start_time
                if x.start_time
                else 0
        )



        return " ".join(

            item.transcript.strip()

            for item in unique_segments

            if item.transcript

        )



    def get_word_count(
        self,
        db: Session,
        interview_id: int,
        question_id: int,
    ):

        answer = self.get_answer(
            db,
            interview_id,
            question_id
        )


        return len(answer.split())
