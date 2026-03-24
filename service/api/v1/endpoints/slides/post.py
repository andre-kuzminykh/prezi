"""
POST endpoints for slides.

## Traceability
- Feature: F002 (Auto Structuring)
- Feature: F003 (Slide Editing)
- Scenario: SC004, SC006, SC007
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.endpoints.slides import router
from core.database import get_session
from model.enums import EditScope
from repository.commands.edit_command_repository import EditCommandRepository
from schema.slides.slide_schema import (
    SlideCreateSchema,
    SlideEditRequestSchema,
    SlideResponseSchema,
)
from service.llm.llm_service import LLMService
from service.slides.slide_service import SlideService

slide_service = SlideService()
llm_service = LLMService()
command_repo = EditCommandRepository()


@router.post("", response_model=SlideResponseSchema, status_code=201)
async def create_slide(
    presentation_id: int,
    data: SlideCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    """Create a new slide for a presentation."""
    return await slide_service.create_slide(presentation_id, data, session)


@router.post("/{slide_id}/edit", response_model=SlideResponseSchema)
async def edit_slide_with_llm(
    presentation_id: int,
    slide_id: int,
    data: SlideEditRequestSchema,
    session: AsyncSession = Depends(get_session),
):
    """Edit a slide using natural-language instruction via LLM."""
    slide = await slide_service.get_slide(slide_id, session)

    updated = await llm_service.edit_slide(
        current_title=slide.slide_title,
        current_text=slide.slide_text,
        current_visual=slide.visual_description or "",
        instruction=data.command_text,
    )

    from schema.slides.slide_schema import SlideUpdateSchema

    update_schema = SlideUpdateSchema(
        slide_title=updated.get("title", slide.slide_title),
        slide_text=updated.get("text", slide.slide_text),
        visual_description=updated.get("visual_description", slide.visual_description),
    )
    updated_slide = await slide_service.update_slide(slide_id, update_schema, session)

    await command_repo.create(
        session,
        presentation_id=presentation_id,
        scope=EditScope.slide,
        target_slide_id=slide_id,
        command_text=data.command_text,
        result_summary=f"Updated slide '{updated_slide.slide_title}'",
        applied=True,
    )

    return updated_slide
