"""
Router registration for the FastAPI application.

## Traceability
- Feature: F000 (Application Bootstrap)
"""

from fastapi import FastAPI

from api.v1.endpoints.presentations import router as presentations_router
from api.v1.endpoints.slides import router as slides_router
from api.v1.endpoints.export import router as export_router


def include_routers(app: FastAPI) -> None:
    """Include all v1 API routers with the /api/v1 prefix."""
    app.include_router(presentations_router, prefix="/api/v1")
    app.include_router(slides_router, prefix="/api/v1")
    app.include_router(export_router, prefix="/api/v1")
