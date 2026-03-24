"""
Application configuration via pydantic-settings.
All secrets and connection parameters are read from environment variables.

## Traceability
- Feature: F000 (Application Bootstrap)
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "prezi"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4.1"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
