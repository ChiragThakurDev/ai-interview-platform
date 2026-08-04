"""
Prompt Template Registry.

Keeps metadata about available prompts.
"""


PROMPT_TEMPLATE_REGISTRY = {

    # ============================
    # Resume
    # ============================

    "resume_analysis": {
        "variables": [
            "resume"
        ]
    },


    # ============================
    # Interview
    # ============================

    "interview_generation": {
        "variables": [
            "resume",
            "role",
            "difficulty",
            "number_of_questions",
        ]
    },


    "answer_evaluation": {
        "variables": [
            "question",
            "answer",
        ]
    },


    "interview_report": {
        "variables": [
            "results"
        ]
    },


    "skill_analysis": {
        "variables": [
            "results"
        ]
    },


    # ============================
    # Coding Interview
    # ============================

    "coding_interview_generation": {
        "variables": [
            "role",
            "company",
            "language",
            "difficulty",
            "number_of_questions",
            "seed",
            "previous_topics",
        ]
    },


    "coding_evaluation": {
        "variables": [
            "question",
            "language",
            "code",
            "execution_output",
            "execution_error",
        ]
    },


    "coding_interview_report": {
        "variables": [
            "results"
        ]
    },


    # ============================
    # Roadmap
    # ============================

    "roadmap": {
        "variables": [
            "skill_report"
        ]
    },


    # ============================
    # Chat
    # ============================

    "chat": {
        "variables": [
            "name",
            "question",
        ]
    },


    "chat_system": {
        "variables": []
    },

}
