"""Widget: Create presentation from text/voice.

## Traceability
Feature: F001
Scenarios: SC001, SC002, SC003
"""
from __future__ import annotations

import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback.presentation_callback import PresentationCallback
from core import vocab
from node.presentation.answer.error_answer import ErrorAnswer
from node.presentation.answer.slide_view_answer import SlideViewAnswer
from node.presentation.code.create_presentation_code import CreatePresentationCode
from node.presentation.trigger.create_presentation_trigger import (
    CreatePresentationTrigger,
)
from service.api.presentation_api import PresentationAPI
from state.presentation_state import PresentationState

logger = logging.getLogger(__name__)

router = Router(name="create_widget")

api = PresentationAPI()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    """Handle /start - show welcome message with Create button."""
    await state.clear()

    kb = InlineKeyboardBuilder()
    kb.button(text=vocab.BTN_CREATE, callback_data="new_presentation")

    await message.answer(vocab.WELCOME, reply_markup=kb.as_markup())


@router.callback_query(F.data == "new_presentation")
async def on_new_presentation(
    callback: types.CallbackQuery, state: FSMContext
) -> None:
    """Handle Create button press."""
    await state.clear()

    try:
        result = await api.create_presentation(callback.from_user.id)
        presentation_id = result["id"]
        await state.update_data(presentation_id=presentation_id)
        await state.set_state(PresentationState.collecting_input)

        await callback.message.edit_text(vocab.CREATE_PROMPT)
    except Exception as exc:
        logger.exception("Create presentation failed")
        await ErrorAnswer.run(callback, {"error": str(exc)})

    await callback.answer()


@router.callback_query(F.data == "noop")
async def on_noop(callback: types.CallbackQuery) -> None:
    """Handle noop callback (inactive buttons)."""
    await callback.answer()


@router.message(PresentationState.collecting_input, F.text)
async def on_text_input(message: types.Message, state: FSMContext) -> None:
    """Handle text input while collecting material."""
    trigger_data = await CreatePresentationTrigger.run(message, state)
    result = await CreatePresentationCode.run(trigger_data, state, api)

    if result["answer_name"] == "error":
        await ErrorAnswer.run(message, result["data"])
    else:
        presentation_id = result["data"]["presentation_id"]
        kb = InlineKeyboardBuilder()
        kb.button(
            text=vocab.BTN_STRUCTURE,
            callback_data=PresentationCallback(
                action="structure",
                presentation_id=presentation_id,
            ),
        )
        await message.answer(vocab.INPUT_RECEIVED, reply_markup=kb.as_markup())


@router.message(PresentationState.collecting_input, F.voice)
async def on_voice_input(message: types.Message, state: FSMContext) -> None:
    """Handle voice input while collecting material."""
    trigger_data = await CreatePresentationTrigger.run(message, state)
    result = await CreatePresentationCode.run(trigger_data, state, api)

    if result["answer_name"] == "error":
        await ErrorAnswer.run(message, result["data"])
    else:
        presentation_id = result["data"]["presentation_id"]
        kb = InlineKeyboardBuilder()
        kb.button(
            text=vocab.BTN_STRUCTURE,
            callback_data=PresentationCallback(
                action="structure",
                presentation_id=presentation_id,
            ),
        )
        await message.answer(vocab.INPUT_RECEIVED, reply_markup=kb.as_markup())


@router.callback_query(
    PresentationCallback.filter(F.action == "structure"),
)
async def on_structure(
    callback: types.CallbackQuery,
    callback_data: PresentationCallback,
    state: FSMContext,
) -> None:
    """Trigger AI structuring and show the first slide."""
    presentation_id = callback_data.presentation_id

    await callback.message.edit_text(vocab.STRUCTURING)

    try:
        slides = await api.structure_presentation(presentation_id)

        if not slides:
            await callback.message.edit_text(vocab.NO_SLIDES)
            await callback.answer()
            return

        await state.set_state(PresentationState.viewing_slides)
        await state.update_data(
            presentation_id=presentation_id,
            current_slide_index=0,
            current_slide_id=slides[0].get("id"),
        )

        await SlideViewAnswer.run(
            callback,
            {
                "slide": slides[0],
                "index": 0,
                "total": len(slides),
                "presentation_id": presentation_id,
            },
        )
    except Exception as exc:
        logger.exception("Structure failed")
        await ErrorAnswer.run(callback, {"error": str(exc)})

    await callback.answer()
