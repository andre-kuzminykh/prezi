"""
Application configuration via pydantic-settings.
All secrets and connection parameters are read from environment variables.

## Traceability
- Feature: F000 (Application Bootstrap)
"""

from pathlib import Path
from pydantic_settings import BaseSettings

# Look for .env in service/ dir first, then project root
_service_dir = Path(__file__).resolve().parent.parent
_root_dir = _service_dir.parent
_env_file = _service_dir / ".env" if (_service_dir / ".env").exists() else _root_dir / ".env"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "prezi_db"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4.1"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = {"env_file": str(_env_file), "env_file_encoding": "utf-8"}


config = Settings()
