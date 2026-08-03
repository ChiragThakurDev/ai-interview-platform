from sqlalchemy.orm import Session

from app.models.prompt import Prompt
from app.db.session import SessionLocal

from app.ai.prompts import (
    RESUME_ANALYSIS_PROMPT,
    INTERVIEW_GENERATION_PROMPT,
    ANSWER_EVALUATION_PROMPT,
    INTERVIEW_REPORT_PROMPT,
    CHAT_SYSTEM_PROMPT,
)


PROMPTS = [

    {
        "name": "resume_analysis",
        "version": "v1",
        "template": RESUME_ANALYSIS_PROMPT,
        "model": "llama3.1:8b",
        "temperature": 0.3,
    },

    {
        "name": "interview_generation",
        "version": "v1",
        "template": INTERVIEW_GENERATION_PROMPT,
        "model": "llama3.1:8b",
        "temperature": 0.3,
    },

    {
        "name": "answer_evaluation",
        "version": "v1",
        "template": ANSWER_EVALUATION_PROMPT,
        "model": "llama3.1:8b",
        "temperature": 0.2,
    },

    {
        "name": "interview_report",
        "version": "v1",
        "template": INTERVIEW_REPORT_PROMPT,
        "model": "llama3.1:8b",
        "temperature": 0.3,
    },

    {
        "name": "chat_system",
        "version": "v1",
        "template": CHAT_SYSTEM_PROMPT,
        "model": "llama3.1:8b",
        "temperature": 0.4,
    },
]


def seed_prompts():

    db: Session = SessionLocal()

    try:

        for item in PROMPTS:

            exists = (
                db.query(Prompt)
                .filter(
                    Prompt.name == item["name"],
                    Prompt.version == item["version"],
                )
                .first()
            )

            if not exists:

                prompt = Prompt(
                    **item,
                    is_active=True,
                )

                db.add(prompt)

        db.commit()

        print("Prompts seeded successfully")


    finally:

        db.close()


if __name__ == "__main__":
    seed_prompts()
