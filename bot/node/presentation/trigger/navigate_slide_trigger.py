"""Trigger: extract navigation data from callback query.

## Traceability
Component: Node / Presentation / Trigger / NavigateSlideTrigger
Feature: F003
Scenarios: SC006, SC007
"""
from __future__ import annotations

from typing import Any

from aiogram import types
from aiogram.fsm.context import FSMContext

from callback.presentation_callback import SlideNavigationCallback


class NavigateSlideTrigger:
    """Extract slide navigation parameters from a callback query."""

    @staticmethod
    async def run(
        callback_query: types.CallbackQuery,
        state: FSMContext,
        callback_data: SlideNavigationCallback,
    ) -> dict[str, Any]:
        """Return presentation_id, slide_index, action."""
        return {
            "presentation_id": callback_data.presentation_id,
            "slide_index": callback_data.slide_index,
            "action": callback_data.action,
        }
