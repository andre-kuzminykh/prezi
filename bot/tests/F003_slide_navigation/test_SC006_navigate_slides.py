"""SC006: User navigates between slides.

## Traceability
Feature: F003
Scenario: SC006
"""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from node.presentation.code.navigate_slide_code import NavigateSlideCode


@pytest.mark.asyncio
async def test_navigate_returns_correct_slide(fake_state, api_client):
    """NavigateSlideCode should return the slide at the requested index."""
    slides = [
        {"id": 1, "title": "Слайд 1", "text": "Текст 1", "visual_description": ""},
        {"id": 2, "title": "Слайд 2", "text": "Текст 2", "visual_description": ""},
        {"id": 3, "title": "Слайд 3", "text": "Текст 3", "visual_description": ""},
    ]
    api_client.get_slides = AsyncMock(return_value=slides)

    trigger_data = {
        "presentation_id": 10,
        "slide_index": 1,
        "action": "next",
    }

    result = await NavigateSlideCode.run(trigger_data, fake_state, api_client)

    assert result["answer_name"] == "slide_view"
    assert result["data"]["slide"]["id"] == 2
    assert result["data"]["index"] == 1
    assert result["data"]["total"] == 3


@pytest.mark.asyncio
async def test_navigate_clamps_index(fake_state, api_client):
    """Index should be clamped to valid range."""
    slides = [
        {"id": 1, "title": "Only", "text": "", "visual_description": ""},
    ]
    api_client.get_slides = AsyncMock(return_value=slides)

    trigger_data = {
        "presentation_id": 10,
        "slide_index": 99,
        "action": "next",
    }

    result = await NavigateSlideCode.run(trigger_data, fake_state, api_client)

    assert result["answer_name"] == "slide_view"
    assert result["data"]["index"] == 0


@pytest.mark.asyncio
async def test_navigate_empty_slides(fake_state, api_client):
    """Should return error when no slides exist."""
    api_client.get_slides = AsyncMock(return_value=[])

    trigger_data = {
        "presentation_id": 10,
        "slide_index": 0,
        "action": "view",
    }

    result = await NavigateSlideCode.run(trigger_data, fake_state, api_client)

    assert result["answer_name"] == "error"


@pytest.mark.asyncio
async def test_navigate_api_error(fake_state, api_client):
    """Should return error on API failure."""
    api_client.get_slides = AsyncMock(side_effect=Exception("timeout"))

    trigger_data = {
        "presentation_id": 10,
        "slide_index": 0,
        "action": "view",
    }

    result = await NavigateSlideCode.run(trigger_data, fake_state, api_client)

    assert result["answer_name"] == "error"
    assert "timeout" in result["data"]["error"]
