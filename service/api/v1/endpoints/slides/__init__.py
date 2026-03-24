"""
Slide endpoints package.

## Traceability
- Feature: F002 (Auto Structuring)
- Feature: F003 (Slide Editing)
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/presentations/{presentation_id}/slides",
    tags=["slides"],
)

from api.v1.endpoints.slides import get, post, patch, delete  # noqa: E402, F401
