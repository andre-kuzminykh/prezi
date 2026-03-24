"""Widget: Generate and export presentation.

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
    """Generate HTML + PDF and send PDF to user."""
    presentation_id = callback_data.presentation_id

    # Answer callback immediately to avoid Telegram timeout
    await callback.answer()
    await callback.message.edit_text(vocab.GENERATING_PDF)

    try:
        # Generate PDF via backend
        pdf_bytes = await api.export_pdf(presentation_id)

        # Send PDF file
        doc = BufferedInputFile(
            file=pdf_bytes,
            filename=f"presentation_{presentation_id}.pdf",
        )
        await callback.message.answer_document(
            document=doc,
            caption=vocab.EXPORT_READY,
        )

        # Delete the "generating" message
        try:
            await callback.message.delete()
        except Exception:
            pass

    except Exception as exc:
        logger.exception("Export failed")
        await callback.message.edit_text(
            vocab.ERROR.format(error=str(exc))
        )
