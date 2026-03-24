"""
FastAPI application factory and startup configuration.

## Traceability
- Feature: F000 (Application Bootstrap)
"""

from fastapi import FastAPI

from api.v1.include_router import include_routers
from api.v1.exception_handlers import register_exception_handlers

app = FastAPI(
    title="AI Presentation Builder",
    description="Backend service for managing presentations, slides, and LLM-powered structuring/editing.",
    version="1.0.0",
)

include_routers(app)
register_exception_handlers(app)
