from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "sprintdesk"
    secret_key: str = "dev-only-change-me"
    access_token_minutes: int = 60 * 12
    database_url: str = "sqlite:///./sprintdesk.db"
    upload_dir: str = "uploads"
    max_upload_bytes: int = 2 * 1024 * 1024
    allowed_mime: set[str] = {
        "text/plain",
        "image/png",
        "image/jpeg",
        "application/pdf",
    }

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
