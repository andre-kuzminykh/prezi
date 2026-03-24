"""SC011: User confirms presentation and receives PDF.

## Traceability
Feature: F006
Scenario: SC011
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from node.presentation.code.navigate_slide_code import NavigateSlideCode


@pytest.mark.asyncio
async def test_navigate_returns_slide_data(fake_state, api_client):
    """NavigateSlideCode should return slide data for SlideViewAnswer."""
    slides = [
        {"id": 1, "slide_title": "S1", "slide_text": "T1", "visual_description": "V1"},
        {"id": 2, "slide_title": "S2", "slide_text": "T2", "visual_description": "V2"},
    ]
    api_client.get_slides = AsyncMock(return_value=slides)

    trigger_data = {"presentation_id": 10, "slide_index": 1, "action": "next"}
    result = await NavigateSlideCode.run(trigger_data, fake_state, api_client)

    assert result["answer_name"] == "slide_view"
    assert result["data"]["slide"]["id"] == 2
    assert result["data"]["total"] == 2


@pytest.mark.asyncio
async def test_confirm_widget_calls_export_pdf():
    """on_done handler should call export_pdf and send document."""
    from handler.v1.user.presentation.F006.confirm_widget import on_done

    cb = MagicMock()
    cb.message = MagicMock()
    cb.message.edit_text = AsyncMock()
    cb.message.answer_document = AsyncMock()
    cb.message.delete = AsyncMock()
    cb.answer = AsyncMock()

    cb_data = MagicMock()
    cb_data.presentation_id = 42

    state = MagicMock()

    with patch(
        "handler.v1.user.presentation.F006.confirm_widget.api"
    ) as mock_api:
        mock_api.export_pdf = AsyncMock(return_value=b"%PDF-fake-content")

        await on_done(cb, cb_data, state)

    # callback.answer() is called first (immediately), then edit_text
    cb.answer.assert_awaited_once()
    cb.message.edit_text.assert_awaited_once()
    mock_api.export_pdf.assert_awaited_once_with(42)
    cb.message.answer_document.assert_awaited_once()


@pytest.mark.asyncio
async def test_confirm_widget_handles_export_error():
    """on_done should show error if export fails."""
    from handler.v1.user.presentation.F006.confirm_widget import on_done

    cb = MagicMock()
    cb.message = MagicMock()
    cb.message.edit_text = AsyncMock()
    cb.message.answer_document = AsyncMock()
    cb.answer = AsyncMock()

    cb_data = MagicMock()
    cb_data.presentation_id = 42

    state = MagicMock()

    with patch(
        "handler.v1.user.presentation.F006.confirm_widget.api"
    ) as mock_api:
        mock_api.export_pdf = AsyncMock(side_effect=Exception("PDF generation failed"))

        await on_done(cb, cb_data, state)

    # callback.answer() first, then edit_text twice (generating + error)
    cb.answer.assert_awaited_once()
    assert cb.message.edit_text.await_count == 2
    error_text = cb.message.edit_text.call_args_list[1][0][0]
    assert "PDF generation failed" in error_text
