"""
PATCH endpoints for slides.

## Traceability
- Feature: F003 (Slide Editing)
- Scenario: SC006
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.endpoints.slides import router
from core.database import get_session
from schema.slides.slide_schema import SlideResponseSchema, SlideUpdateSchema
from service.slides.slide_service import SlideService

slide_service = SlideService()


@router.patch("/{slide_id}", response_model=SlideResponseSchema)
async def update_slide(
    presentation_id: int,
    slide_id: int,
    data: SlideUpdateSchema,
    session: AsyncSession = Depends(get_session),
):
    """Directly update a slide's fields."""
    return await slide_service.update_slide(slide_id, data, session)
