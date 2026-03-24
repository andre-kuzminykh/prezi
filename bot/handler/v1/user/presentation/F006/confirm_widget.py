"""Widget: Generate and export presentation as HTML.

## Traceability
Feature: F006, F007, F008
Scenarios: SC011, SC012, SC013
"""
from __future__ import annotations

import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile

from callback.presentation_callback import PresentationCallback
from core import vocab
from node.presentation.answer.error_answer import ErrorAnswer
from service.api.presentation_api import PresentationAPI

logger = logging.getLogger(__name__)

router = Router(name="confirm_widget")

api = PresentationAPI()


@router.callback_query(PresentationCallback.filter(F.action == "done"))
async def on_done(
    callback: types.CallbackQuery,
    callback_data: PresentationCallback,
    state: FSMContext,
) -> None:
    """Generate HTML presentation via LLM and send as file."""
    presentation_id = callback_data.presentation_id

    await callback.answer()
    await callback.message.edit_text(vocab.GENERATING_HTML)

    try:
        html_content = await api.export_html(presentation_id)

        doc = BufferedInputFile(
            file=html_content.encode("utf-8"),
            filename=f"presentation_{presentation_id}.html",
        )
        await callback.message.answer_document(
            document=doc,
            caption=vocab.EXPORT_READY,
        )

        try:
            await callback.message.delete()
        except Exception:
            pass

    except Exception as exc:
        logger.exception("Export failed")
        await callback.message.edit_text(
            vocab.ERROR.format(error=str(exc))
        )
