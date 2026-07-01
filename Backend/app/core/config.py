from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name:str
    app_version:str
    debug:bool

    secret_key:str
    algorithm:str

    database_url:str

    access_token_expire_minutes:int
    refresh_token_expire_days: int

    redis_url:str

    model_config=SettingsConfigDict(
            env_file=".env",
            case_sensitive=False,
)
settings=Settings()
