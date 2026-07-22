from app.services.ai_service import AIService


class RoadmapService:

    def __init__(self):
        self.ai_service = AIService()

    def generate_roadmap(
        self,
        skill_report: str,
    ):
        """
        Generate a personalized learning roadmap
        based on the candidate's skill report.
        """

        return self.ai_service.generate_learning_roadmap(
            skill_report
        )
