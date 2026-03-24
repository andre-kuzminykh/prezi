"""
POST endpoints for presentations.

## Traceability
- Feature: F001 (Create Presentation)
- Feature: F002 (Auto Structuring)
- Scenario: SC001, SC002, SC004
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.endpoints.presentations import router
from core.database import get_session
from model.enums import PresentationStatus
from schema.inputs.input_message_schema import (
    InputMessageCreateSchema,
    InputMessageResponseSchema,
)
from schema.presentations.presentation_schema import (
    PresentationCreateSchema,
    PresentationResponseSchema,
)
from schema.slides.slide_schema import SlideResponseSchema
from service.llm.llm_service import LLMService
from service.presentations.presentation_service import PresentationService
from service.slides.slide_service import SlideService

presentation_service = PresentationService()
slide_service = SlideService()
llm_service = LLMService()


@router.post("", response_model=PresentationResponseSchema, status_code=201)
async def create_presentation(
    data: PresentationCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    """Create a new presentation."""
    return await presentation_service.create_presentation(data, session)


@router.post(
    "/{presentation_id}/input",
    response_model=InputMessageResponseSchema,
    status_code=201,
)
async def add_input(
    presentation_id: int,
    data: InputMessageCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    """Add an input message to a presentation."""
    return await presentation_service.add_input(presentation_id, data, session)


@router.post(
    "/{presentation_id}/structure",
    response_model=list[SlideResponseSchema],
)
async def structure_presentation(
    presentation_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Trigger LLM structuring: analyze inputs and create slides."""
    presentation = await presentation_service.get_presentation(
        presentation_id, session
    )

    await presentation_service.update_status(
        presentation_id, PresentationStatus.structuring, session
    )

    inputs = await presentation_service.input_repo.get_by_presentation_id(
        presentation_id, session
    )
    combined_text = "\n\n".join(
        inp.transcript or inp.raw_content for inp in inputs
    )

    slide_data_list = await llm_service.structure_text(combined_text)

    created_slides = []
    for idx, slide_data in enumerate(slide_data_list, start=1):
        from schema.slides.slide_schema import SlideCreateSchema

        slide_schema = SlideCreateSchema(
            order=idx,
            slide_title=slide_data.get("title", f"Slide {idx}"),
            slide_text=slide_data.get("text", ""),
            visual_description=slide_data.get("visual_description"),
        )
        slide = await slide_service.create_slide(
            presentation_id, slide_schema, session
        )
        created_slides.append(slide)

    await presentation_service.update_status(
        presentation_id, PresentationStatus.ready, session
    )

    return created_slides
