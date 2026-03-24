"""Answer: send the exported file or URL to the user.

## Traceability
Component: Node / Presentation / Answer / ExportReadyAnswer
Feature: F007, F008
Scenarios: SC012, SC013
"""
from __future__ import annotations

import io
from typing import Any

from aiogram import types
from aiogram.types import BufferedInputFile

from core import vocab


class ExportReadyAnswer:
    """Deliver the export result to the user."""

    @staticmethod
    async def run(
        event: types.Message | types.CallbackQuery,
        data: dict[str, Any],
    ) -> None:
        """Send exported file or link."""
        target = event.message if isinstance(event, types.CallbackQuery) else event

        if "pdf_bytes" in data:
            doc = BufferedInputFile(
                file=data["pdf_bytes"],
                filename="presentation.pdf",
            )
            await target.answer_document(document=doc, caption=vocab.EXPORT_READY)
        elif "html_url" in data:
            text = f"{vocab.EXPORT_READY}\n\n<a href=\"{data['html_url']}\">Открыть HTML</a>"
            if "content" in data:
                text += f"\n\n<pre>{data['content'][:3000]}</pre>"
            await target.answer(text, disable_web_page_preview=False)
        else:
            await target.answer(vocab.EXPORT_READY)
