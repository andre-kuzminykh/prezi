"""
Global exception handlers for the FastAPI application.

## Traceability
- Feature: F000 (Application Bootstrap)
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.exceptions import AppException, NotFoundError, ValidationError


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers on the app."""

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(
        request: Request, exc: ValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request, exc: AppException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )
