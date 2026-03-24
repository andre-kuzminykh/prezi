"""
Repository for presentation-specific database queries.

## Traceability
- Feature: F001 (Create Presentation)
- Scenario: SC001, SC002, SC003
"""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from model.presentations.presentation_model import PresentationModel
from repository.base_repository import BaseRepository


class PresentationRepository(BaseRepository[PresentationModel]):
    def __init__(self):
        super().__init__(PresentationModel)

    async def get_by_user_id(
        self, user_id: int, session: AsyncSession
    ) -> Sequence[PresentationModel]:
        """Fetch all presentations for a given Telegram user."""
        stmt = select(PresentationModel).where(
            PresentationModel.user_id == user_id
        )
        result = await session.execute(stmt)
        return result.scalars().all()
