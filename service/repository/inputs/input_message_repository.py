"""
Repository for input message database queries.

## Traceability
- Feature: F001 (Create Presentation)
- Scenario: SC001, SC002
"""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from model.inputs.input_message_model import InputMessageModel
from repository.base_repository import BaseRepository


class InputMessageRepository(BaseRepository[InputMessageModel]):
    def __init__(self):
        super().__init__(InputMessageModel)

    async def get_by_presentation_id(
        self, presentation_id: int, session: AsyncSession
    ) -> Sequence[InputMessageModel]:
        """Fetch all input messages for a presentation."""
        stmt = (
            select(InputMessageModel)
            .where(InputMessageModel.presentation_id == presentation_id)
            .order_by(InputMessageModel.created_at)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
