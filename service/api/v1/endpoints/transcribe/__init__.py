"""
Transcription endpoints package.

## Traceability
- Feature: F001, F004 (Voice input support)
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/transcribe",
    tags=["transcribe"],
)

from api.v1.endpoints.transcribe import post as _post  # noqa: E402, F401
