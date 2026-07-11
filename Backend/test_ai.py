from app.services.ai_service import AIService

service = AIService()

resume = """
Chirag Thakur

MCA Student

Skills:
Python
FastAPI
Docker
React
MongoDB
Redis
PostgreSQL

Projects:
AI Interview Platform
"""

result = service.analyze_resume(resume)

print(result.model_dump_json(indent=4))
