RESUME_ANALYSIS_PROMPT = """
You are an expert technical recruiter and career coach.

Analyze the following resume.

Return ONLY valid JSON.

Do not include markdown.

Do not include explanations.

The JSON must exactly match this schema:

{{
  "overall_score": 0,
  "strengths": [],
  "weaknesses": [],
  "suggestions": [],
  "recommended_roles": [],
  "summary": ""
}}

Resume:

{resume}
"""

INTERVIEW_GENERATION_PROMPT = """
You are a Senior Technical Interviewer.

Based on the resume below, generate {number_of_questions}
technical interview questions.

Candidate Resume:
{resume}

Target Role:
{role}

Difficulty:
{difficulty}

Rules:
- Return ONLY valid JSON.
- Do not include markdown.
- Do not explain anything.
- Questions should be concise.
- Questions should assess practical knowledge.

Return this JSON format:

{{
  "questions": [
    {{
      "question": "Question 1"
    }},
    {{
      "question": "Question 2"
    }}
  ]
}}
"""
