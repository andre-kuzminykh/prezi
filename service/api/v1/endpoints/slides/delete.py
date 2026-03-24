"""
DELETE endpoints for slides.

## Traceability
- Feature: F003 (Slide Editing)
- Scenario: SC008
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.endpoints.slides import router
from core.database import get_session
from service.slides.slide_service import SlideService

slide_service = SlideService()


@router.delete("/{slide_id}", status_code=204)
async def delete_slide(
    presentation_id: int,
    slide_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Delete a slide and reorder remaining slides."""
    await slide_service.delete_slide(slide_id, session)
    return None
