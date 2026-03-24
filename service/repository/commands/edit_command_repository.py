"""
Repository for edit command database queries.

## Traceability
- Feature: F003 (Slide Editing)
- Scenario: SC006, SC007
"""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from model.commands.edit_command_model import EditCommandModel
from repository.base_repository import BaseRepository


class EditCommandRepository(BaseRepository[EditCommandModel]):
    def __init__(self):
        super().__init__(EditCommandModel)

    async def get_by_presentation_id(
        self, presentation_id: int, session: AsyncSession
    ) -> Sequence[EditCommandModel]:
        """Fetch all edit commands for a presentation."""
        stmt = (
            select(EditCommandModel)
            .where(EditCommandModel.presentation_id == presentation_id)
            .order_by(EditCommandModel.created_at)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
