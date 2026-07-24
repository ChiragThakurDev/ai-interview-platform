from sqlalchemy.orm import Session

from app.models.coding_draft import CodingDraft


class CodingDraftRepository:


    def __init__(
            self,
            db: Session
            ):
        self.db = db


    # =====================================================
    # SAVE / UPDATE DRAFT
    # =====================================================

    def save_draft(
            self,
            user_id: int,
            question_id: int,
            language: str,
            code: str,
            ):

        draft = (
            self.db.query(CodingDraft)
            .filter(
                CodingDraft.user_id == user_id,
                CodingDraft.question_id == question_id,
            )
            .first()
        )


        if draft:

            draft.language = language
            draft.code = code

        else:

            draft = CodingDraft(
                user_id=user_id,
                question_id=question_id,
                language=language,
                code=code,
            )

            self.db.add(draft)


        self.db.commit()
        self.db.refresh(draft)

        return draft



    # =====================================================
    # GET DRAFT
    # =====================================================

    def get_draft(
            self,
            user_id: int,
            question_id: int,
            ):

        return (
            self.db.query(CodingDraft)
            .filter(
                CodingDraft.user_id == user_id,
                CodingDraft.question_id == question_id,
            )
            .first()
        )
