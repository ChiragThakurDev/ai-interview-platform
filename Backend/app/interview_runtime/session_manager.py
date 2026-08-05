class InterviewSessionManager:


    def __init__(self):

        self.sessions = {}



    def start_session(
        self,
        interview_id:int,
        question_id:int
    ):

        self.sessions[interview_id] = {

            "current_question_id": question_id

        }



    def get_current_question(
        self,
        interview_id:int
    ):

        session = self.sessions.get(
            interview_id
        )

        if not session:
            return None


        return session[
            "current_question_id"
        ]



    def update_question(
        self,
        interview_id:int,
        question_id:int
    ):

        if interview_id in self.sessions:

            self.sessions[interview_id][
                "current_question_id"
            ] = question_id
