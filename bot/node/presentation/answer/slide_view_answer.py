"""Answer: render a slide card with navigation and action buttons.

## Traceability
Component: Node / Presentation / Answer / SlideViewAnswer
Feature: F003
Scenarios: SC006, SC007
"""
from __future__ import annotations

from typing import Any

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback.presentation_callback import (
    PresentationCallback,
    SlideActionCallback,
    SlideNavigationCallback,
)
from core import vocab


class SlideViewAnswer:
    """Display a single slide with navigation controls."""

    @staticmethod
    async def run(
        event: types.Message | types.CallbackQuery,
        data: dict[str, Any],
    ) -> None:
        """Render slide card."""
        slide = data["slide"]
        idx = data["index"]
        total = data["total"]
        presentation_id = data["presentation_id"]

        text = vocab.SLIDE_TEMPLATE.format(
            index=idx + 1,
            total=total,
            title=slide.get("title", ""),
            text=slide.get("text", ""),
            visual_description=slide.get("visual_description", ""),
        )

        kb = InlineKeyboardBuilder()

        # Navigation row
        if idx > 0:
            kb.button(
                text=vocab.BTN_PREV,
                callback_data=SlideNavigationCallback(
                    action="prev",
                    presentation_id=presentation_id,
                    slide_index=idx - 1,
                ),
            )
        if idx < total - 1:
            kb.button(
                text=vocab.BTN_NEXT,
                callback_data=SlideNavigationCallback(
                    action="next",
                    presentation_id=presentation_id,
                    slide_index=idx + 1,
                ),
            )

        kb.adjust(2)

        # Action row
        slide_id = slide.get("id", 0)
        action_row = InlineKeyboardBuilder()
        action_row.button(
            text=vocab.BTN_EDIT,
            callback_data=SlideActionCallback(
                action="edit",
                presentation_id=presentation_id,
                slide_id=slide_id,
            ),
        )
        action_row.button(
            text=vocab.BTN_DELETE,
            callback_data=SlideActionCallback(
                action="delete",
                presentation_id=presentation_id,
                slide_id=slide_id,
            ),
        )
        action_row.button(
            text=vocab.BTN_ADD_SLIDE,
            callback_data=SlideActionCallback(
                action="add_after",
                presentation_id=presentation_id,
                slide_id=slide_id,
            ),
        )
        action_row.adjust(3)

        # Presentation-level row
        pres_row = InlineKeyboardBuilder()
        pres_row.button(
            text=vocab.BTN_CONFIRM,
            callback_data=PresentationCallback(
                action="confirm",
                presentation_id=presentation_id,
            ),
        )
        pres_row.button(
            text=vocab.BTN_EXPORT_HTML,
            callback_data=PresentationCallback(
                action="export_html",
                presentation_id=presentation_id,
            ),
        )
        pres_row.button(
            text=vocab.BTN_EXPORT_PDF,
            callback_data=PresentationCallback(
                action="export_pdf",
                presentation_id=presentation_id,
            ),
        )
        pres_row.adjust(3)

        kb.attach(action_row)
        kb.attach(pres_row)

        markup = kb.as_markup()

        if isinstance(event, types.CallbackQuery):
            await event.message.edit_text(text, reply_markup=markup)
        else:
            await event.answer(text, reply_markup=markup)
