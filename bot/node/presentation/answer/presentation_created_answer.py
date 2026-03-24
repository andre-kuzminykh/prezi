"""Answer: inform user that input was received.

## Traceability
Component: Node / Presentation / Answer / PresentationCreatedAnswer
Feature: F001
Scenarios: SC001, SC002
"""
from __future__ import annotations

from typing import Any

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback.presentation_callback import PresentationCallback
from core import vocab


class PresentationCreatedAnswer:
    """Send confirmation that material was accepted."""

    @staticmethod
    async def run(
        event: types.Message | types.CallbackQuery,
        data: dict[str, Any],
    ) -> None:
        """Render the 'input received' response with a Structure button."""
        presentation_id = data["presentation_id"]

        kb = InlineKeyboardBuilder()
        kb.button(
            text=vocab.BTN_STRUCTURE,
            callback_data=PresentationCallback(
                action="structure",
                presentation_id=presentation_id,
            ),
        )

        text = vocab.INPUT_RECEIVED

        if isinstance(event, types.CallbackQuery):
            await event.message.edit_text(text, reply_markup=kb.as_markup())
        else:
            await event.answer(text, reply_markup=kb.as_markup())
