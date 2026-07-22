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



    # ==============================
    # AI / Ollama
    # ==============================

    ollama_url: str = (
        "http://host.docker.internal:11434"
    )


    ollama_model: str = (
        "llama3.1:8b"
    )



    # ==============================
    # Pydantic Configuration
    # ==============================

    model_config = SettingsConfigDict(

        env_file=ENV_FILE,

        case_sensitive=False,

        extra="ignore",

    )



settings = Settings()
