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

ANSWER_EVALUATION_PROMPT = """
You are a Senior Technical Interviewer.

Evaluate the candidate's answer to the interview question.

Interview Question:
{question}

Candidate Answer:
{answer}

Instructions:
- Score the answer from 0 to 100.
- Consider:
  - Technical accuracy
  - Completeness
  - Clarity
  - Best practices
- Provide constructive feedback.
- Return ONLY valid JSON.
- Do not include markdown.
- Do not explain anything outside the JSON.

Return this JSON format:

{{
  "score": 0,
  "feedback": ""
}}
"""

INTERVIEW_REPORT_PROMPT = """
You are a Senior Software Engineering Interviewer.

You are given an entire interview consisting of technical questions,
the candidate's answers, and the score for each answer.

Evaluate the candidate as if this were a real technical interview.

Return ONLY valid JSON.

Do not include markdown.

Do not explain anything outside JSON.

The JSON must exactly match this schema:

{{
  "overall_score": 0,
  "technical_level": "",
  "communication": "",
  "strengths": [],
  "weaknesses": [],
  "recommendation": "",
  "summary": ""
}}

Interview Results:

{results}
"""

SKILL_ANALYSIS_PROMPT = """

You are an expert technical interviewer and career mentor.

Analyze the candidate's interview performance.

Based on answers, scores, and feedback:

Identify:
1. Strong technical skills
2. Weak technical areas
3. Recommended learning topics


Return ONLY valid JSON.

Format:
{{
  "strong_skills": [
    "skill1",
    "skill2"
  ],

  "weak_skills": [
    "skill1",
    "skill2"
  ],

  "recommended_topics": [
    "topic1",
    "topic2"
  ],

  "summary": "candidate analysis"
}}

Candidate Interview Data:

{results}

"""

