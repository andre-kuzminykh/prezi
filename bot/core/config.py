"""Application configuration via pydantic-settings.

## Traceability
Component: Core / Config
"""
from pathlib import Path
from pydantic_settings import BaseSettings

# Look for .env in bot/ dir first, then project root
_bot_dir = Path(__file__).resolve().parent.parent
_root_dir = _bot_dir.parent
_env_file = _bot_dir / ".env" if (_bot_dir / ".env").exists() else _root_dir / ".env"


class Settings(BaseSettings):
    """Bot settings loaded from environment variables."""

    BOT_TOKEN: str
    BACKEND_URL: str = "http://localhost:8000"

    model_config = {"env_file": str(_env_file), "env_file_encoding": "utf-8"}


settings = Settings()
