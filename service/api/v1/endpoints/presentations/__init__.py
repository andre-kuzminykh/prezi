"""
Presentation endpoints package.

## Traceability
- Feature: F001 (Create Presentation)
"""

from fastapi import APIRouter

router = APIRouter(prefix="/presentations", tags=["presentations"])

from api.v1.endpoints.presentations import get, post, patch  # noqa: E402, F401
