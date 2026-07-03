from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    app_name: str
    app_version: str
    debug: bool

    # JWT
    secret_key: str
    algorithm: str

    # Database
    database_url: str

    # Token Expiry
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    email_verification_expire_hours: int
    password_reset_expire_minutes: int

    # Redis
    redis_url: str

    # Email (NEW)
    smtp_host: str
    smtp_port: int
    smtp_email: str
    smtp_password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()
