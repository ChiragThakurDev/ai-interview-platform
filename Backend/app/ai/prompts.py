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
