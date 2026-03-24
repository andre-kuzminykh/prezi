"""Widget: Slide navigation.

## Traceability
Feature: F003
Scenarios: SC006, SC007
"""
from __future__ import annotations

import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from callback.presentation_callback import SlideNavigationCallback
from node.presentation.answer.error_answer import ErrorAnswer
from node.presentation.answer.slide_view_answer import SlideViewAnswer
from node.presentation.code.navigate_slide_code import NavigateSlideCode
from node.presentation.trigger.navigate_slide_trigger import NavigateSlideTrigger
from service.api.presentation_api import PresentationAPI
from state.presentation_state import PresentationState

logger = logging.getLogger(__name__)

router = Router(name="navigate_widget")

api = PresentationAPI()


@router.callback_query(SlideNavigationCallback.filter())
async def on_slide_navigate(
    callback: types.CallbackQuery,
    callback_data: SlideNavigationCallback,
    state: FSMContext,
) -> None:
    """Handle prev/next/view slide navigation."""
    await state.set_state(PresentationState.viewing_slides)

    trigger_data = await NavigateSlideTrigger.run(callback, state, callback_data)
    result = await NavigateSlideCode.run(trigger_data, state, api)

    if result["answer_name"] == "error":
        await ErrorAnswer.run(callback, result["data"])
    else:
        await SlideViewAnswer.run(callback, result["data"])

    await callback.answer()
