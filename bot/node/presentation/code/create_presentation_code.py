"""Code: create presentation and add input via API.

## Traceability
Component: Node / Presentation / Code / CreatePresentationCode
Feature: F001
Scenarios: SC001, SC002, SC003
"""
from __future__ import annotations

import logging
from typing import Any

from aiogram.fsm.context import FSMContext

from service.api.presentation_api import PresentationAPI

logger = logging.getLogger(__name__)


class CreatePresentationCode:
    """Business logic for creating a presentation and adding input."""

    @staticmethod
    async def run(
        trigger_data: dict[str, Any],
        state: FSMContext,
        api: PresentationAPI,
    ) -> dict[str, Any]:
        """Execute creation flow. Returns answer descriptor dict."""
        try:
            state_data = await state.get_data()
            presentation_id = state_data.get("presentation_id")

            # Create presentation if not yet started
            if not presentation_id:
                result = await api.create_presentation(trigger_data["user_id"])
                presentation_id = result["id"]
                await state.update_data(presentation_id=presentation_id)

            # Add input material
            input_result = await api.add_input(
                presentation_id=presentation_id,
                content=trigger_data["content"],
                input_type=trigger_data["input_type"],
            )

            return {
                "answer_name": "input_received",
                "data": {
                    "presentation_id": presentation_id,
                    "input": input_result,
                },
            }

        except Exception as exc:
            logger.exception("CreatePresentationCode error")
            return {
                "answer_name": "error",
                "data": {"error": str(exc)},
            }
