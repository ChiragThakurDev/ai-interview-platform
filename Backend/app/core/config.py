import os

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from pydantic import field_validator


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


    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value):

        if isinstance(value, str):

            normalized = value.strip().lower()

            if normalized in {
                "release",
                "prod",
                "production",
            }:
                return False


            if normalized in {
                "dev",
                "development",
            }:
                return True


        return value



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

    ai_provider: str = "ollama"


    ollama_url: str = (
    "http://localhost:11434"
    )


    # Default general model
    default_model: str = (
     "llama3.1:8b"
    )


    # Models

    chat_model: str = (
     "phi4-mini:latest"
    )


    coding_model: str = (
     "qwen2.5-coder:3b"
    )


    json_model: str = (
      "qwen2.5-coder:3b"
    )


    evaluation_model: str = (
     "qwen2.5-coder:3b"
    )


    fast_model: str = (
     "llama3.2:3b"
    )


    embedding_model: str = (
     "nomic-embed-text"
    )


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



    # ==================================================
    # LiveKit Video Interview
    # ==================================================

    livekit_url: str

    livekit_api_key: str

    livekit_api_secret: str



    # ==============================
    # Pydantic Configuration
    # ==============================

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        case_sensitive=False,
        extra="ignore",
    )

    # ==============================
    # Speech AI
    # ==============================

    speech_provider: str = "faster-whisper"

    whisper_model: str = "base"

    whisper_device: str = "auto"

    whisper_compute_type: str = "int8"

    transcript_language: str = "en"

    enable_auto_language_detection: bool = True



settings = Settings()
