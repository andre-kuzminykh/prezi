"""Trigger: extract edit command from message.

## Traceability
Component: Node / Presentation / Trigger / EditSlideTrigger
Feature: F004
Scenarios: SC008, SC009, SC010
"""
from __future__ import annotations

import io
import logging
from typing import Any

from aiogram import types
from aiogram.fsm.context import FSMContext

from core.loader import bot

logger = logging.getLogger(__name__)


class EditSlideTrigger:
    """Extract the natural-language edit command."""

    @staticmethod
    async def run(
        message: types.Message,
        state: FSMContext,
    ) -> dict[str, Any]:
        """Return slide_id, command_text, presentation_id."""
        state_data = await state.get_data()
        slide_id = state_data.get("current_slide_id")
        presentation_id = state_data.get("presentation_id")

        command_text = ""
        input_type = "text"

        if message.voice:
            input_type = "voice"
            file = await bot.get_file(message.voice.file_id)
            buf = io.BytesIO()
            await bot.download_file(file.file_path, destination=buf)
            import base64

            command_text = base64.b64encode(buf.getvalue()).decode()
        elif message.text:
            command_text = message.text

        return {
            "slide_id": slide_id,
            "presentation_id": presentation_id,
            "command_text": command_text,
            "input_type": input_type,
        }
