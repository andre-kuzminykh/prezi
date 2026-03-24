"""
Export endpoints package.

## Traceability
- Feature: F007 (HTML Generation)
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/presentations/{presentation_id}/export",
    tags=["export"],
)

from api.v1.endpoints.export import post as _post  # noqa: E402, F401
