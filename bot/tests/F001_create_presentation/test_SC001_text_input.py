"""SC001: User sends text to create a presentation.

## Traceability
Feature: F001
Scenario: SC001
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from node.presentation.code.create_presentation_code import CreatePresentationCode
from node.presentation.trigger.create_presentation_trigger import (
    CreatePresentationTrigger,
)


@pytest.mark.asyncio
async def test_text_trigger_extracts_content(fake_message, fake_state):
    """CreatePresentationTrigger should extract text content."""
    fake_message.text = "Мой доклад о машинном обучении"
    fake_message.voice = None

    result = await CreatePresentationTrigger.run(fake_message, fake_state)

    assert result["user_id"] == fake_message.from_user.id
    assert result["content"] == "Мой доклад о машинном обучении"
    assert result["input_type"] == "text"


@pytest.mark.asyncio
async def test_create_presentation_code_creates_and_adds_input(
    fake_state, api_client
):
    """CreatePresentationCode should create presentation then add input."""
    fake_state.get_data = AsyncMock(return_value={})
    api_client.create_presentation = AsyncMock(return_value={"id": 42})
    api_client.add_input = AsyncMock(return_value={"id": 1, "content": "text"})

    trigger_data = {
        "user_id": 123456,
        "content": "Текст презентации",
        "input_type": "text",
    }

    result = await CreatePresentationCode.run(trigger_data, fake_state, api_client)

    assert result["answer_name"] == "input_received"
    assert result["data"]["presentation_id"] == 42
    api_client.create_presentation.assert_awaited_once_with(123456)
    api_client.add_input.assert_awaited_once_with(
        presentation_id=42,
        content="Текст презентации",
        input_type="text",
    )


@pytest.mark.asyncio
async def test_create_presentation_code_reuses_existing(fake_state, api_client):
    """If presentation_id is already in state, do not create a new one."""
    fake_state.get_data = AsyncMock(return_value={"presentation_id": 99})
    api_client.add_input = AsyncMock(return_value={"id": 2, "content": "more"})

    trigger_data = {
        "user_id": 123456,
        "content": "Ещё текст",
        "input_type": "text",
    }

    result = await CreatePresentationCode.run(trigger_data, fake_state, api_client)

    assert result["answer_name"] == "input_received"
    assert result["data"]["presentation_id"] == 99
    api_client.create_presentation.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_presentation_code_handles_error(fake_state, api_client):
    """On API error, answer_name should be 'error'."""
    fake_state.get_data = AsyncMock(return_value={})
    api_client.create_presentation = AsyncMock(
        side_effect=Exception("Connection refused")
    )

    trigger_data = {
        "user_id": 123456,
        "content": "fail",
        "input_type": "text",
    }

    result = await CreatePresentationCode.run(trigger_data, fake_state, api_client)

    assert result["answer_name"] == "error"
    assert "Connection refused" in result["data"]["error"]
