"""Trigger: extract user input for presentation creation.

## Traceability
Component: Node / Presentation / Trigger / CreatePresentationTrigger
Feature: F001
Scenarios: SC001, SC002, SC003
"""
from __future__ import annotations

import io
import logging
from typing import Any

from aiogram import types
from aiogram.fsm.context import FSMContext

from core.loader import bot
from state.presentation_state import PresentationState

logger = logging.getLogger(__name__)


class CreatePresentationTrigger:
    """Extract content from a text or voice message."""

    @staticmethod
    async def run(
        message: types.Message,
        state: FSMContext,
    ) -> dict[str, Any]:
        """Parse the incoming message and return normalised trigger data.

        Returns
        -------
        dict with keys: user_id, content, input_type
        """
        user_id = message.from_user.id
        input_type = "text"
        content = ""

        if message.voice:
            input_type = "voice"
            file = await bot.get_file(message.voice.file_id)
            buf = io.BytesIO()
            await bot.download_file(file.file_path, destination=buf)
            # The bot does not perform transcription itself; it sends the
            # base64-encoded audio to the backend which handles STT.
            import base64

            content = base64.b64encode(buf.getvalue()).decode()
        elif message.text:
            content = message.text
        else:
            content = ""

        await state.set_state(PresentationState.collecting_input)

        return {
            "user_id": user_id,
            "content": content,
            "input_type": input_type,
        }
