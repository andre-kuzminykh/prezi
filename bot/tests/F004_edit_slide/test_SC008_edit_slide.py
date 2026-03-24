"""SC008: User edits a slide with natural language commands.

## Traceability
Feature: F004
Scenario: SC008
"""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from node.presentation.code.edit_slide_code import EditSlideCode


@pytest.mark.asyncio
async def test_edit_slide_sends_command(fake_state, api_client):
    """EditSlideCode should call edit_slide_nl with correct params."""
    api_client.edit_slide_nl = AsyncMock(
        return_value={"id": 5, "slide_title": "Updated", "slide_text": "New text"}
    )

    trigger_data = {
        "presentation_id": 10,
        "slide_id": 5,
        "command_text": "Сделай заголовок короче",
        "input_type": "text",
    }

    result = await EditSlideCode.run(trigger_data, fake_state, api_client)

    assert result["answer_name"] == "slide_edited"
    assert result["data"]["slide"]["slide_title"] == "Updated"
    api_client.edit_slide_nl.assert_awaited_once_with(
        presentation_id=10,
        slide_id=5,
        command_text="Сделай заголовок короче",
    )


@pytest.mark.asyncio
async def test_edit_slide_handles_api_error(fake_state, api_client):
    """On API error, should return error answer."""
    api_client.edit_slide_nl = AsyncMock(side_effect=Exception("LLM timeout"))

    trigger_data = {
        "presentation_id": 10,
        "slide_id": 5,
        "command_text": "anything",
        "input_type": "text",
    }

    result = await EditSlideCode.run(trigger_data, fake_state, api_client)

    assert result["answer_name"] == "error"
    assert "LLM timeout" in result["data"]["error"]


@pytest.mark.asyncio
async def test_edit_trigger_extracts_text(fake_state):
    """EditSlideTrigger should extract text command from message."""
    from unittest.mock import MagicMock

    from node.presentation.trigger.edit_slide_trigger import EditSlideTrigger

    fake_state.get_data = AsyncMock(
        return_value={"current_slide_id": 7, "presentation_id": 3}
    )

    msg = MagicMock()
    msg.text = "Добавь больше деталей"
    msg.voice = None

    result = await EditSlideTrigger.run(msg, fake_state)

    assert result["slide_id"] == 7
    assert result["presentation_id"] == 3
    assert result["command_text"] == "Добавь больше деталей"
    assert result["input_type"] == "text"
