"""Answer: presentation created confirmation.

## Traceability
Component: Node / Presentation / Answer / PresentationCreatedAnswer
Feature: F001
Scenarios: SC001, SC002
"""
from __future__ import annotations
from typing import Any
from aiogram import types
from core import vocab


class PresentationCreatedAnswer:
    """Show presentation created message."""

    @staticmethod
    async def run(
        event: types.Message | types.CallbackQuery,
        data: dict[str, Any],
    ) -> None:
        target = event.message if isinstance(event, types.CallbackQuery) else event
        await target.answer(vocab.PRESENTATION_CREATED)
