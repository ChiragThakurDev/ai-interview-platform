from sqlalchemy.orm import Session

from app.models.coding_test_case import CodingTestCase


class CodingTestCaseRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, test_case: CodingTestCase):
        self.db.add(test_case)
        self.db.commit()
        self.db.refresh(test_case)
        return test_case

    def get_by_question_id(self, question_id: int):
        return (
            self.db.query(CodingTestCase)
            .filter(CodingTestCase.question_id == question_id)
            .all()
        )

    def delete(self, test_case: CodingTestCase):
        self.db.delete(test_case)
        self.db.commit()
