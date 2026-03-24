"""
PATCH endpoints for presentations.

## Traceability
- Feature: F001 (Create Presentation)
- Scenario: SC003
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.endpoints.presentations import router
from core.database import get_session
from schema.presentations.presentation_schema import (
    PresentationResponseSchema,
    PresentationUpdateSchema,
)
from service.presentations.presentation_service import PresentationService

presentation_service = PresentationService()


@router.patch("/{presentation_id}", response_model=PresentationResponseSchema)
async def update_presentation(
    presentation_id: int,
    data: PresentationUpdateSchema,
    session: AsyncSession = Depends(get_session),
):
    """Update a presentation (title, status, etc.)."""
    return await presentation_service.update_presentation(
        presentation_id, data, session
    )
