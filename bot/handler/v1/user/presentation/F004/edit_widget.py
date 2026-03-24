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
from node.presentation.answer.slide_edited_answer import SlideEditedAnswer
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
    )

    await callback.message.answer(vocab.EDIT_PROMPT)
    await callback.answer()


@router.callback_query(SlideActionCallback.filter(F.action == "delete"))
async def on_delete_slide(
    callback: types.CallbackQuery,
    callback_data: SlideActionCallback,
    state: FSMContext,
) -> None:
    """Delete a slide and show the previous one."""
    try:
        await api.delete_slide(
            callback_data.presentation_id, callback_data.slide_id
        )

        slides = await api.get_slides(callback_data.presentation_id)
        if not slides:
            await callback.message.edit_text(vocab.NO_PRESENTATIONS)
            await callback.answer()
            return

        idx = 0
        await state.update_data(
            current_slide_index=idx,
            current_slide_id=slides[idx].get("id"),
        )

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
        logger.exception("Delete slide failed")
        await ErrorAnswer.run(callback, {"error": str(exc)})

    await callback.answer()


@router.callback_query(SlideActionCallback.filter(F.action == "add_after"))
async def on_add_slide(
    callback: types.CallbackQuery,
    callback_data: SlideActionCallback,
    state: FSMContext,
) -> None:
    """Add a new blank slide after the current one."""
    try:
        new_slide = await api.create_slide(
            callback_data.presentation_id,
            {"title": "Новый слайд", "text": "", "after_slide_id": callback_data.slide_id},
        )

        slides = await api.get_slides(callback_data.presentation_id)
        total = len(slides)
        # Find index of the new slide
        idx = next(
            (i for i, s in enumerate(slides) if s.get("id") == new_slide.get("id")),
            total - 1,
        )

        await state.update_data(
            current_slide_index=idx,
            current_slide_id=new_slide.get("id"),
        )

        await SlideViewAnswer.run(
            callback,
            {
                "slide": new_slide,
                "index": idx,
                "total": total,
                "presentation_id": callback_data.presentation_id,
            },
        )
    except Exception as exc:
        logger.exception("Add slide failed")
        await ErrorAnswer.run(callback, {"error": str(exc)})

    await callback.answer()


@router.message(PresentationState.editing_slide, F.text)
async def on_edit_text(message: types.Message, state: FSMContext) -> None:
    """Apply text edit command to the current slide."""
    trigger_data = await EditSlideTrigger.run(message, state)
    result = await EditSlideCode.run(trigger_data, state, api)

    await state.set_state(PresentationState.viewing_slides)

    if result["answer_name"] == "error":
        await ErrorAnswer.run(message, result["data"])
    else:
        # Fetch context for rendering
        state_data = await state.get_data()
        result["data"]["index"] = state_data.get("current_slide_index", 0)
        result["data"]["presentation_id"] = state_data.get("presentation_id")

        slides = await api.get_slides(state_data["presentation_id"])
        result["data"]["total"] = len(slides)

        await SlideEditedAnswer.run(message, result["data"])


@router.message(PresentationState.editing_slide, F.voice)
async def on_edit_voice(message: types.Message, state: FSMContext) -> None:
    """Apply voice edit command to the current slide."""
    trigger_data = await EditSlideTrigger.run(message, state)
    result = await EditSlideCode.run(trigger_data, state, api)

    await state.set_state(PresentationState.viewing_slides)

    if result["answer_name"] == "error":
        await ErrorAnswer.run(message, result["data"])
    else:
        state_data = await state.get_data()
        result["data"]["index"] = state_data.get("current_slide_index", 0)
        result["data"]["presentation_id"] = state_data.get("presentation_id")

        slides = await api.get_slides(state_data["presentation_id"])
        result["data"]["total"] = len(slides)

        await SlideEditedAnswer.run(message, result["data"])
