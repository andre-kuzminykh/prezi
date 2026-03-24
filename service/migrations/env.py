"""
Alembic async migration environment.

## Traceability
- Feature: F000 (Application Bootstrap)
"""

import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

# Add service/ directory to Python path so imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from core.config import config as app_config
from model.base_model import Base

# Import all models so their metadata is registered
from model.presentations.presentation_model import PresentationModel  # noqa: F401
from model.slides.slide_model import SlideModel  # noqa: F401
from model.inputs.input_message_model import InputMessageModel  # noqa: F401
from model.commands.edit_command_model import EditCommandModel  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url() -> str:
    return app_config.database_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode using async engine."""
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
