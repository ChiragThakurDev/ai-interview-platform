# 🤖 AI Interview Preparation Platform

An AI-powered Interview Preparation Platform built with **FastAPI**, **PostgreSQL**, **Docker**, **Redis**, and **Ollama**. The platform enables users to upload resumes, receive AI-powered resume analysis, generate personalized interview questions, and prepares the foundation for AI-based interview evaluation.

---

## 🚀 Features

### 👤 Authentication & Authorization

* JWT Authentication
* Role-Based Authorization
* Secure Password Hashing (bcrypt)
* Protected API Endpoints

### 📄 Resume Management

* Upload PDF resumes
* Store resume metadata
* Extract text from PDF files
* Resume management APIs

### 🧠 AI Resume Analysis

* AI-powered resume analysis using Ollama
* Resume summary
* Strengths & weaknesses
* Improvement suggestions
* Recommended job roles
* Resume scoring

### 💼 AI Interview Generation

* Generate interview questions based on resume content
* Role-specific interview generation
* Difficulty levels (Easy / Medium / Hard)
* Configurable number of questions
* Store interviews in PostgreSQL
* Store interview questions for future practice

### 🐳 Infrastructure

* Docker & Docker Compose
* PostgreSQL
* Redis
* Ollama Integration
* Logging Middleware
* Alembic Database Migrations

---

# 🛠 Tech Stack

### Backend

* FastAPI
* Python 3.12+
* SQLAlchemy
* Alembic
* Pydantic

### Database

* PostgreSQL

### AI

* Ollama
* Local LLM

### Cache

* Redis

### DevOps

* Docker
* Docker Compose

---

# 📁 Project Structure

```text
app/
├── ai/
├── api/
├── core/
├── db/
├── dependencies/
├── middleware/
├── models/
├── repositories/
├── schemas/
├── services/
├── utils/
├── main.py
│
alembic/
docker-compose.yml
Dockerfile
requirements.txt
README.md
```

---

# ⚙️ Setup

## Clone Repository

```bash
git clone <your-repository-url>
cd ai-interview-platform
```

## Create Environment File

```env
DATABASE_URL=postgresql://ai_user:password123@postgres:5432/ai_interview_platform

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

REDIS_URL=redis://redis:6379

OLLAMA_BASE_URL=http://host.docker.internal:11434
```

---

## Start Services

```bash
docker compose up --build
```

---

## Run Database Migrations

```bash
docker compose exec backend alembic upgrade head
```

---

# 📚 API Modules

## Authentication

* Register User
* Login
* Protected Routes
* JWT Authentication

## Resume

* Upload Resume
* Get Resume
* Resume Analysis

## Interview

* Generate Interview Questions
* Store Interview
* Store Questions

---

# 🤖 AI Workflow

```text
User Uploads Resume
        │
        ▼
Extract PDF Text
        │
        ▼
Ollama AI
        │
        ├───────────────┐
        ▼               ▼
Resume Analysis   Interview Questions
        │               │
        ▼               ▼
 Store in Database
        │
        ▼
 Return API Response
```

---

# 📦 Database Tables

* users
* api_keys
* resumes
* resume_analysis
* interviews
* interview_questions

---

# 🔜 Upcoming Features

* AI Interview Answer Evaluation
* Voice-Based Interview
* Speech-to-Text
* AI Feedback & Scoring
* Interview History
* Performance Dashboard
* Interview Reports
* Authentication Refresh Tokens
* Admin Dashboard

---

# 📖 API Documentation

After starting the project:

Swagger UI:

```
http://localhost:5000/docs
```

OpenAPI JSON:

```
http://localhost:5000/openapi.json
```

---

# 👨‍💻 Author

**Chirag Thakur**

MCA (Artificial Intelligence & Machine Learning)

Full Stack Developer

## Connect with me

* GitHub: https://github.com/ChiragThakurDev
* LinkedIn: https://www.linkedin.com/in/chirag-thakur-404b00229/

---

# ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub.

