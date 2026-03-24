"""
GET endpoints for slides.

## Traceability
- Feature: F002 (Auto Structuring)
- Scenario: SC004, SC005
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.endpoints.slides import router
from core.database import get_session
from schema.slides.slide_schema import SlideResponseSchema
from service.slides.slide_service import SlideService

slide_service = SlideService()


@router.get("", response_model=list[SlideResponseSchema])
async def list_slides(
    presentation_id: int,
    session: AsyncSession = Depends(get_session),
):
    """List all slides for a presentation, ordered by slide order."""
    return await slide_service.get_slides(presentation_id, session)


@router.get("/{slide_id}", response_model=SlideResponseSchema)
async def get_slide(
    presentation_id: int,
    slide_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Get a single slide by ID."""
    return await slide_service.get_slide(slide_id, session)
