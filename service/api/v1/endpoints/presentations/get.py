"""
GET endpoints for presentations.

## Traceability
- Feature: F001 (Create Presentation)
- Scenario: SC003
"""

from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.endpoints.presentations import router
from core.database import get_session
from schema.presentations.presentation_schema import PresentationResponseSchema
from service.presentations.presentation_service import PresentationService

presentation_service = PresentationService()


@router.get("", response_model=list[PresentationResponseSchema])
async def list_presentations(
    user_id: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
):
    """List presentations, optionally filtered by user_id."""
    if user_id is not None:
        presentations = await presentation_service.get_user_presentations(
            user_id, session
        )
    else:
        presentations = await presentation_service.presentation_repo.get_all(session)
    return presentations


@router.get("/{presentation_id}", response_model=PresentationResponseSchema)
async def get_presentation(
    presentation_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Get a single presentation by ID."""
    return await presentation_service.get_presentation(presentation_id, session)
