"""
Business logic for presentation management.

## Traceability
- Feature: F001 (Create Presentation)
- Scenario: SC001, SC002, SC003
"""

from typing import Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundError
from model.enums import PresentationStatus
from model.inputs.input_message_model import InputMessageModel
from model.presentations.presentation_model import PresentationModel
from repository.inputs.input_message_repository import InputMessageRepository
from repository.presentations.presentation_repository import PresentationRepository
from schema.inputs.input_message_schema import InputMessageCreateSchema
from schema.presentations.presentation_schema import (
    PresentationCreateSchema,
    PresentationUpdateSchema,
)


class PresentationService:
    def __init__(self):
        self.presentation_repo = PresentationRepository()
        self.input_repo = InputMessageRepository()

    async def create_presentation(
        self,
        data: PresentationCreateSchema,
        session: AsyncSession,
    ) -> PresentationModel:
        """Create a new presentation."""
        return await self.presentation_repo.create(
            session,
            user_id=data.user_id,
            title=data.title,
            source_input_type=data.source_input_type,
        )

    async def get_presentation(
        self, presentation_id: int, session: AsyncSession
    ) -> PresentationModel:
        """Fetch a presentation by ID or raise NotFoundError."""
        presentation = await self.presentation_repo.get_by_id(presentation_id, session)
        if presentation is None:
            raise NotFoundError(f"Presentation with id {presentation_id} not found")
        return presentation

    async def get_user_presentations(
        self, user_id: int, session: AsyncSession
    ) -> Sequence[PresentationModel]:
        """Fetch all presentations for a user."""
        return await self.presentation_repo.get_by_user_id(user_id, session)

    async def update_status(
        self,
        presentation_id: int,
        status: PresentationStatus,
        session: AsyncSession,
    ) -> PresentationModel:
        """Update the status of a presentation."""
        presentation = await self.presentation_repo.update(
            session, presentation_id, status=status
        )
        if presentation is None:
            raise NotFoundError(f"Presentation with id {presentation_id} not found")
        return presentation

    async def update_presentation(
        self,
        presentation_id: int,
        data: PresentationUpdateSchema,
        session: AsyncSession,
    ) -> PresentationModel:
        """Update presentation fields."""
        update_data = data.model_dump(exclude_unset=True)
        presentation = await self.presentation_repo.update(
            session, presentation_id, **update_data
        )
        if presentation is None:
            raise NotFoundError(f"Presentation with id {presentation_id} not found")
        return presentation

    async def add_input(
        self,
        presentation_id: int,
        data: InputMessageCreateSchema,
        session: AsyncSession,
    ) -> InputMessageModel:
        """Add an input message to a presentation."""
        await self.get_presentation(presentation_id, session)
        return await self.input_repo.create(
            session,
            presentation_id=presentation_id,
            type=data.type,
            raw_content=data.raw_content,
            transcript=data.transcript,
        )
