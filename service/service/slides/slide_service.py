"""
Business logic for slide management.

## Traceability
- Feature: F002 (Auto Structuring)
- Feature: F003 (Slide Editing)
- Scenario: SC004, SC005, SC006, SC007
"""

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundError
from model.slides.slide_model import SlideModel
from repository.slides.slide_repository import SlideRepository
from schema.slides.slide_schema import SlideCreateSchema, SlideUpdateSchema


class SlideService:
    def __init__(self):
        self.slide_repo = SlideRepository()

    async def get_slides(
        self, presentation_id: int, session: AsyncSession
    ) -> Sequence[SlideModel]:
        """Get all slides for a presentation, ordered."""
        return await self.slide_repo.get_by_presentation_id(presentation_id, session)

    async def get_slide(
        self, slide_id: int, session: AsyncSession
    ) -> SlideModel:
        """Get a single slide by ID."""
        slide = await self.slide_repo.get_by_id(slide_id, session)
        if slide is None:
            raise NotFoundError(f"Slide with id {slide_id} not found")
        return slide

    async def create_slide(
        self,
        presentation_id: int,
        data: SlideCreateSchema,
        session: AsyncSession,
    ) -> SlideModel:
        """Create a new slide for a presentation."""
        return await self.slide_repo.create(
            session,
            presentation_id=presentation_id,
            order=data.order,
            slide_title=data.slide_title,
            slide_text=data.slide_text,
            visual_description=data.visual_description,
            speaker_notes=data.speaker_notes,
        )

    async def update_slide(
        self,
        slide_id: int,
        data: SlideUpdateSchema,
        session: AsyncSession,
    ) -> SlideModel:
        """Update an existing slide."""
        update_data = data.model_dump(exclude_unset=True)
        slide = await self.slide_repo.update(session, slide_id, **update_data)
        if slide is None:
            raise NotFoundError(f"Slide with id {slide_id} not found")
        return slide

    async def delete_slide(
        self,
        slide_id: int,
        session: AsyncSession,
    ) -> bool:
        """Delete a slide by ID."""
        slide = await self.slide_repo.get_by_id(slide_id, session)
        if slide is None:
            raise NotFoundError(f"Slide with id {slide_id} not found")
        presentation_id = slide.presentation_id
        deleted = await self.slide_repo.delete(session, slide_id)
        if deleted:
            await self.reorder_after_delete(presentation_id, session)
        return deleted

    async def reorder_after_delete(
        self, presentation_id: int, session: AsyncSession
    ) -> Sequence[SlideModel]:
        """Reorder slides after a deletion to maintain sequential order."""
        return await self.slide_repo.reorder_slides(presentation_id, session)
