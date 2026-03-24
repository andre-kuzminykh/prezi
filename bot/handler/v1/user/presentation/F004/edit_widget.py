"""Widget: Edit slide via natural language.

## Traceability
Feature: F004
Scenarios: SC008, SC009, SC010
"""
from __future__ import annotations

import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from callback.presentation_callback import SlideActionCallback
from core import vocab
from node.presentation.answer.error_answer import ErrorAnswer
from node.presentation.answer.slide_view_answer import SlideViewAnswer
from node.presentation.code.edit_slide_code import EditSlideCode
from node.presentation.trigger.edit_slide_trigger import EditSlideTrigger
from service.api.presentation_api import PresentationAPI
from state.presentation_state import PresentationState

logger = logging.getLogger(__name__)

router = Router(name="edit_widget")

api = PresentationAPI()


@router.callback_query(SlideActionCallback.filter(F.action == "edit"))
async def on_edit_start(
    callback: types.CallbackQuery,
    callback_data: SlideActionCallback,
    state: FSMContext,
) -> None:
    """Prompt user for an edit instruction."""
    await state.set_state(PresentationState.editing_slide)
    await state.update_data(
        current_slide_id=callback_data.slide_id,
        presentation_id=callback_data.presentation_id,
        slide_widget_message_id=callback.message.message_id,
    )

    await callback.message.answer(vocab.EDIT_PROMPT)
    await callback.answer()


@router.message(PresentationState.editing_slide, F.text)
async def on_edit_text(message: types.Message, state: FSMContext) -> None:
    """Apply text edit command to the current slide."""
    trigger_data = await EditSlideTrigger.run(message, state)
    result = await EditSlideCode.run(trigger_data, state, api)

    await state.set_state(PresentationState.viewing_slides)

    if result["answer_name"] == "error":
        await ErrorAnswer.run(message, result["data"])
        return

    state_data = await state.get_data()
    presentation_id = state_data.get("presentation_id")

    # Delete old slide widget message
    old_msg_id = state_data.get("slide_widget_message_id")
    if old_msg_id:
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=old_msg_id,
            )
        except Exception:
            pass

    # Fetch updated slides and find current index
    slides = await api.get_slides(presentation_id)
    current_slide_id = state_data.get("current_slide_id")
    idx = next(
        (i for i, s in enumerate(slides) if s.get("id") == current_slide_id),
        state_data.get("current_slide_index", 0),
    )
    idx = max(0, min(idx, len(slides) - 1))

    # Send new slide widget message
    await SlideViewAnswer.run(
        message,
        {
            "slide": slides[idx],
            "index": idx,
            "total": len(slides),
            "presentation_id": presentation_id,
        },
    )

    await state.update_data(
        current_slide_index=idx,
        current_slide_id=slides[idx].get("id"),
    )


@router.message(PresentationState.editing_slide, F.voice)
async def on_edit_voice(message: types.Message, state: FSMContext) -> None:
    """Apply voice edit command to the current slide."""
    trigger_data = await EditSlideTrigger.run(message, state)
    result = await EditSlideCode.run(trigger_data, state, api)

    await state.set_state(PresentationState.viewing_slides)

    if result["answer_name"] == "error":
        await ErrorAnswer.run(message, result["data"])
        return

    state_data = await state.get_data()
    presentation_id = state_data.get("presentation_id")

    old_msg_id = state_data.get("slide_widget_message_id")
    if old_msg_id:
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=old_msg_id,
            )
        except Exception:
            pass

    slides = await api.get_slides(presentation_id)
    current_slide_id = state_data.get("current_slide_id")
    idx = next(
        (i for i, s in enumerate(slides) if s.get("id") == current_slide_id),
        state_data.get("current_slide_index", 0),
    )
    idx = max(0, min(idx, len(slides) - 1))

    await SlideViewAnswer.run(
        message,
        {
            "slide": slides[idx],
            "index": idx,
            "total": len(slides),
            "presentation_id": presentation_id,
        },
    )

    await state.update_data(
        current_slide_index=idx,
        current_slide_id=slides[idx].get("id"),
    )
