"""
FastAPI application factory and startup configuration.

## Traceability
- Feature: F000 (Application Bootstrap)
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1.include_router import include_routers
from api.v1.exception_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Create database tables on startup if they don't exist."""
    from core.database import engine
    from model.base_model import Base
    # Import all models so their tables are registered with Base.metadata
    from model.presentations.presentation_model import PresentationModel  # noqa: F401
    from model.slides.slide_model import SlideModel  # noqa: F401
    from model.inputs.input_message_model import InputMessageModel  # noqa: F401
    from model.commands.edit_command_model import EditCommandModel  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="AI Presentation Builder",
    description="Backend service for managing presentations, slides, and LLM-powered structuring/editing.",
    version="1.0.0",
    lifespan=lifespan,
)

include_routers(app)
register_exception_handlers(app)
