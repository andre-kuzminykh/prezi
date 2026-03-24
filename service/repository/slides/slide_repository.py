"""
Repository for slide-specific database queries.

## Traceability
- Feature: F002 (Auto Structuring)
- Feature: F003 (Slide Editing)
- Scenario: SC004, SC005, SC006
"""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from model.slides.slide_model import SlideModel
from repository.base_repository import BaseRepository


class SlideRepository(BaseRepository[SlideModel]):
    def __init__(self):
        super().__init__(SlideModel)

    async def get_by_presentation_id(
        self, presentation_id: int, session: AsyncSession
    ) -> Sequence[SlideModel]:
        """Fetch all slides for a presentation, ordered by slide order."""
        stmt = (
            select(SlideModel)
            .where(SlideModel.presentation_id == presentation_id)
            .order_by(SlideModel.order)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def reorder_slides(
        self, presentation_id: int, session: AsyncSession
    ) -> Sequence[SlideModel]:
        """Reassign sequential order values to all slides in a presentation."""
        slides = await self.get_by_presentation_id(presentation_id, session)
        for idx, slide in enumerate(slides, start=1):
            slide.order = idx
        await session.flush()
        return slides
