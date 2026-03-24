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

from api.v1.endpoints.slides import get as _get  # noqa: E402, F401
from api.v1.endpoints.slides import post as _post  # noqa: E402, F401
from api.v1.endpoints.slides import patch as _patch  # noqa: E402, F401
from api.v1.endpoints.slides import delete as _delete  # noqa: E402, F401
