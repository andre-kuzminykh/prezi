"""Code: apply natural-language edit to a slide.

## Traceability
Component: Node / Presentation / Code / EditSlideCode
Feature: F004
Scenarios: SC008, SC009, SC010
"""
from __future__ import annotations

import logging
from typing import Any

from aiogram.fsm.context import FSMContext

from service.api.presentation_api import PresentationAPI

logger = logging.getLogger(__name__)


class EditSlideCode:
    """Send the NL edit command to the backend and return the updated slide."""

    @staticmethod
    async def run(
        trigger_data: dict[str, Any],
        state: FSMContext,
        api: PresentationAPI,
    ) -> dict[str, Any]:
        """Execute the edit and return answer descriptor."""
        try:
            updated_slide = await api.edit_slide_nl(
                presentation_id=trigger_data["presentation_id"],
                slide_id=trigger_data["slide_id"],
                command_text=trigger_data["command_text"],
            )

            return {
                "answer_name": "slide_edited",
                "data": {"slide": updated_slide},
            }

        except Exception as exc:
            logger.exception("EditSlideCode error")
            return {
                "answer_name": "error",
                "data": {"error": str(exc)},
            }
