"""Widget: Export presentation.

## Traceability
Feature: F007, F008
Scenarios: SC012, SC013
"""
from __future__ import annotations

import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from callback.presentation_callback import PresentationCallback
from node.presentation.answer.error_answer import ErrorAnswer
from node.presentation.answer.export_ready_answer import ExportReadyAnswer
from service.api.presentation_api import PresentationAPI

logger = logging.getLogger(__name__)

router = Router(name="export_widget")

api = PresentationAPI()


@router.callback_query(PresentationCallback.filter(F.action == "export_html"))
async def on_export_html(
    callback: types.CallbackQuery,
    callback_data: PresentationCallback,
    state: FSMContext,
) -> None:
    """Export presentation as HTML."""
    try:
        result = await api.export_html(callback_data.presentation_id)

        await ExportReadyAnswer.run(
            callback,
            {
                "html_url": result.get("html_url", ""),
                "content": result.get("content", ""),
            },
        )
    except Exception as exc:
        logger.exception("HTML export failed")
        await ErrorAnswer.run(callback, {"error": str(exc)})

    await callback.answer()


@router.callback_query(PresentationCallback.filter(F.action == "export_pdf"))
async def on_export_pdf(
    callback: types.CallbackQuery,
    callback_data: PresentationCallback,
    state: FSMContext,
) -> None:
    """Export presentation as PDF."""
    try:
        pdf_bytes = await api.export_pdf(callback_data.presentation_id)

        await ExportReadyAnswer.run(callback, {"pdf_bytes": pdf_bytes})
    except Exception as exc:
        logger.exception("PDF export failed")
        await ErrorAnswer.run(callback, {"error": str(exc)})

    await callback.answer()
