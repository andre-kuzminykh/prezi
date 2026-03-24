"""
Generic base repository with common CRUD operations.

## Traceability
- Feature: F000 (Application Bootstrap)
"""

from typing import Generic, Optional, Sequence, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Generic async repository providing standard CRUD operations."""

    def __init__(self, model: type[T]):
        self.model = model

    async def get_by_id(self, id: int, session: AsyncSession) -> Optional[T]:
        """Fetch a single record by primary key."""
        result = await session.get(self.model, id)
        return result

    async def get_all(
        self,
        session: AsyncSession,
        filters: Optional[dict] = None,
    ) -> Sequence[T]:
        """Fetch all records, optionally filtered by column values."""
        stmt = select(self.model)
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    stmt = stmt.where(getattr(self.model, key) == value)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def create(self, session: AsyncSession, **kwargs) -> T:
        """Insert a new record."""
        instance = self.model(**kwargs)
        session.add(instance)
        await session.flush()
        await session.refresh(instance)
        return instance

    async def update(self, session: AsyncSession, id: int, **kwargs) -> Optional[T]:
        """Update an existing record by primary key."""
        instance = await self.get_by_id(id, session)
        if instance is None:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(instance, key):
                setattr(instance, key, value)
        await session.flush()
        await session.refresh(instance)
        return instance

    async def delete(self, session: AsyncSession, id: int) -> bool:
        """Delete a record by primary key. Returns True if deleted."""
        instance = await self.get_by_id(id, session)
        if instance is None:
            return False
        await session.delete(instance)
        await session.flush()
        return True
