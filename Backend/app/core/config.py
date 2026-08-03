import os

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


ENV_FILE = os.getenv(
    "ENV_FILE",
    ".env",
)


class Settings(BaseSettings):

    # ==============================
    # Application
    # ==============================

    app_name: str = "AI Interview Platform"

    app_version: str = "1.0.0"

    debug: bool = False

    # ==============================
    # Frontend
    # ==============================

    frontend_url: str = (
        "http://localhost:3000"
    )

    # ==============================
    # JWT Security
    # ==============================

    secret_key: str

    algorithm: str = "HS256"

    # ==============================
    # Database
    # ==============================

    database_url: str

    # ==============================
    # Token Expiry
    # ==============================

    access_token_expire_minutes: int = 30

    refresh_token_expire_days: int = 7

    email_verification_expire_hours: int = 24

    password_reset_expire_minutes: int = 15

    # ==============================
    # Redis
    # ==============================

    redis_url: str = (
        "redis://localhost:6379/0"
    )

    # ==============================
    # SMTP Email
    # ==============================

    smtp_host: str = (
        "smtp.gmail.com"
    )

    smtp_port: int = 587

    smtp_email: str

    smtp_password: str

    # ==================================================
    # AI Configuration
    # ==================================================

    # Provider
    ai_provider: str = "ollama"

    # Ollama Server
    ollama_url: str = (
        "http://host.docker.internal:11434"
    )

    # Chat Model
    chat_model: str = (
        "phi4-mini:latest"
    )

    # Coding Model
    coding_model: str = (
        "qwen2.5-coder:3b"
    )

    # Structured JSON Model
    json_model: str = (
        "qwen2.5-coder:3b"
    )

    # Fast / Cheap Model
    fast_model: str = (
        "llama3.2:3b"
    )

    # Embedding Model (Future)
    embedding_model: str = (
        "nomic-embed-text"
    )

    # Vision Model (Future)
    vision_model: str = (
        "llava:7b"
    )

    # ==================================================
    # AI Generation Settings
    # ==================================================

    chat_temperature: float = 0.7

    coding_temperature: float = 0.2

    json_temperature: float = 0.1

    fast_temperature: float = 0.3

    max_tokens: int = 4096

    request_timeout: int = 300

    # ==============================
    # Pydantic Configuration
    # ==============================

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
