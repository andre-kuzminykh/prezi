"""Answer: render a slide card with navigation and action buttons.

## Traceability
Component: Node / Presentation / Answer / SlideViewAnswer
Feature: F003
Scenarios: SC006, SC007
"""
from __future__ import annotations

import html
import logging
from typing import Any

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from callback.presentation_callback import (
    PresentationCallback,
    SlideActionCallback,
    SlideNavigationCallback,
)
from core import vocab

logger = logging.getLogger(__name__)


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
            title=html.escape(slide.get("slide_title", slide.get("title", ""))),
            text=html.escape(slide.get("slide_text", slide.get("text", ""))),
            visual_description=html.escape(slide.get("visual_description", "—")),
        )

        # Row 1: Navigation [◀️] [1/5] [▶️]
        if idx > 0:
            btn_prev = InlineKeyboardButton(
                text=vocab.BTN_PREV,
                callback_data=SlideNavigationCallback(
                    action="prev",
                    presentation_id=presentation_id,
                    slide_index=idx - 1,
                ).pack(),
            )
        else:
            btn_prev = InlineKeyboardButton(text=vocab.BTN_INACTIVE, callback_data="noop")

        btn_counter = InlineKeyboardButton(
            text=f"{idx + 1}/{total}",
            callback_data="noop",
        )

        if idx < total - 1:
            btn_next = InlineKeyboardButton(
                text=vocab.BTN_NEXT,
                callback_data=SlideNavigationCallback(
                    action="next",
                    presentation_id=presentation_id,
                    slide_index=idx + 1,
                ).pack(),
            )
        else:
            btn_next = InlineKeyboardButton(text=vocab.BTN_INACTIVE, callback_data="noop")

        # Row 2: Edit
        slide_id = slide.get("id", 0)
        btn_edit = InlineKeyboardButton(
            text=vocab.BTN_EDIT,
            callback_data=SlideActionCallback(
                action="edit",
                presentation_id=presentation_id,
                slide_id=slide_id,
            ).pack(),
        )

        # Row 3: Done
        btn_done = InlineKeyboardButton(
            text=vocab.BTN_DONE,
            callback_data=PresentationCallback(
                action="done",
                presentation_id=presentation_id,
            ).pack(),
        )

        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [btn_prev, btn_counter, btn_next],
                [btn_edit],
                [btn_done],
            ]
        )

        if isinstance(event, types.CallbackQuery):
            try:
                await event.message.edit_text(text, reply_markup=markup)
            except Exception:
                logger.exception("SlideViewAnswer: edit_text failed, sending new message")
                await event.message.answer(text, reply_markup=markup)
        else:
            await event.answer(text, reply_markup=markup)
