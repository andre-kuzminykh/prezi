"""Code: fetch slides and compute navigation position.

## Traceability
Component: Node / Presentation / Code / NavigateSlideCode
Feature: F003
Scenarios: SC006, SC007
"""
from __future__ import annotations

import logging
from typing import Any

from aiogram.fsm.context import FSMContext

from service.api.presentation_api import PresentationAPI

logger = logging.getLogger(__name__)


class NavigateSlideCode:
    """Resolve the current slide for display."""

    @staticmethod
    async def run(
        trigger_data: dict[str, Any],
        state: FSMContext,
        api: PresentationAPI,
    ) -> dict[str, Any]:
        """Fetch slides and return the one at *slide_index*."""
        try:
            presentation_id = trigger_data["presentation_id"]
            slide_index = trigger_data["slide_index"]

            slides = await api.get_slides(presentation_id)
            total = len(slides)

            if total == 0:
                return {
                    "answer_name": "error",
                    "data": {"error": "Слайды не найдены"},
                }

            # Clamp index
            idx = max(0, min(slide_index, total - 1))
            slide = slides[idx]

            await state.update_data(
                presentation_id=presentation_id,
                current_slide_index=idx,
                current_slide_id=slide.get("id"),
            )

            return {
                "answer_name": "slide_view",
                "data": {
                    "slide": slide,
                    "index": idx,
                    "total": total,
                    "presentation_id": presentation_id,
                },
            }

        except Exception as exc:
            logger.exception("NavigateSlideCode error")
            return {
                "answer_name": "error",
                "data": {"error": str(exc)},
            }
