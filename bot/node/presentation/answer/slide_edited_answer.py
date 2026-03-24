"""Answer: show the updated slide after editing.

## Traceability
Component: Node / Presentation / Answer / SlideEditedAnswer
Feature: F004
Scenarios: SC008, SC009, SC010
"""
from __future__ import annotations

from typing import Any

from aiogram import types

from node.presentation.answer.slide_view_answer import SlideViewAnswer


class SlideEditedAnswer:
    """Re-render the slide after a successful edit."""

    @staticmethod
    async def run(
        event: types.Message | types.CallbackQuery,
        data: dict[str, Any],
    ) -> None:
        """Delegate to SlideViewAnswer with updated slide data."""
        slide = data["slide"]

        view_data = {
            "slide": slide,
            "index": data.get("index", 0),
            "total": data.get("total", 1),
            "presentation_id": data.get(
                "presentation_id", slide.get("presentation_id", 0)
            ),
        }

        await SlideViewAnswer.run(event, view_data)
