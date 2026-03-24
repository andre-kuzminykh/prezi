"""Widget: Confirm presentation.

## Traceability
Feature: F006
Scenarios: SC011
"""
from __future__ import annotations

import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback.presentation_callback import PresentationCallback
from core import vocab
from node.presentation.answer.error_answer import ErrorAnswer
from service.api.presentation_api import PresentationAPI
from state.presentation_state import PresentationState

logger = logging.getLogger(__name__)

router = Router(name="confirm_widget")

api = PresentationAPI()


@router.callback_query(PresentationCallback.filter(F.action == "confirm"))
async def on_confirm(
    callback: types.CallbackQuery,
    callback_data: PresentationCallback,
    state: FSMContext,
) -> None:
    """Mark the presentation as ready."""
    try:
        await api.update_presentation(
            callback_data.presentation_id,
            {"status": "ready"},
        )

        await state.set_state(PresentationState.confirming)

        kb = InlineKeyboardBuilder()
        kb.button(
            text=vocab.BTN_EXPORT_HTML,
            callback_data=PresentationCallback(
                action="export_html",
                presentation_id=callback_data.presentation_id,
            ),
        )
        kb.button(
            text=vocab.BTN_EXPORT_PDF,
            callback_data=PresentationCallback(
                action="export_pdf",
                presentation_id=callback_data.presentation_id,
            ),
        )
        kb.button(
            text=vocab.BTN_BACK,
            callback_data=PresentationCallback(
                action="back",
                presentation_id=callback_data.presentation_id,
            ),
        )
        kb.adjust(2, 1)

        await callback.message.edit_text(
            vocab.CONFIRM_PROMPT + "\n\n" + vocab.EXPORT_READY,
            reply_markup=kb.as_markup(),
        )
    except Exception as exc:
        logger.exception("Confirm failed")
        await ErrorAnswer.run(callback, {"error": str(exc)})

    await callback.answer()


@router.callback_query(PresentationCallback.filter(F.action == "back"))
async def on_back(
    callback: types.CallbackQuery,
    callback_data: PresentationCallback,
    state: FSMContext,
) -> None:
    """Go back to slide view."""
    from node.presentation.answer.slide_view_answer import SlideViewAnswer

    await state.set_state(PresentationState.viewing_slides)

    try:
        slides = await api.get_slides(callback_data.presentation_id)
        if not slides:
            await callback.message.edit_text(vocab.NO_PRESENTATIONS)
            await callback.answer()
            return

        state_data = await state.get_data()
        idx = state_data.get("current_slide_index", 0)
        idx = max(0, min(idx, len(slides) - 1))

        await SlideViewAnswer.run(
            callback,
            {
                "slide": slides[idx],
                "index": idx,
                "total": len(slides),
                "presentation_id": callback_data.presentation_id,
            },
        )
    except Exception as exc:
        logger.exception("Back navigation failed")
        await ErrorAnswer.run(callback, {"error": str(exc)})

    await callback.answer()
