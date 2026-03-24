"""
Presentation endpoints package.

## Traceability
- Feature: F001 (Create Presentation)
"""

from fastapi import APIRouter

router = APIRouter(prefix="/presentations", tags=["presentations"])

from api.v1.endpoints.presentations import get as _get  # noqa: E402, F401
from api.v1.endpoints.presentations import post as _post  # noqa: E402, F401
from api.v1.endpoints.presentations import patch as _patch  # noqa: E402, F401
