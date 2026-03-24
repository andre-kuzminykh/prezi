"""Application configuration via pydantic-settings.

## Traceability
Component: Core / Config
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Bot settings loaded from environment variables."""

    BOT_TOKEN: str
    BACKEND_URL: str = "http://localhost:8000"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
