"""Answer: display an error message.

## Traceability
Component: Node / Presentation / Answer / ErrorAnswer
"""
from __future__ import annotations

from typing import Any

from aiogram import types

from core import vocab


class ErrorAnswer:
    """Show a user-friendly error message."""

    @staticmethod
    async def run(
        event: types.Message | types.CallbackQuery,
        data: dict[str, Any],
    ) -> None:
        """Send the error text."""
        error_text = vocab.ERROR.format(error=data.get("error", "unknown"))

        if isinstance(event, types.CallbackQuery):
            await event.message.answer(error_text)
            await event.answer()
        else:
            await event.answer(error_text)
