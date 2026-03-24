"""SC007: SlideViewAnswer renders slide with navigation and escapes HTML.

## Traceability
Feature: F003
Scenario: SC007
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from aiogram import types

from node.presentation.answer.slide_view_answer import SlideViewAnswer


def _make_callback() -> MagicMock:
    cb = MagicMock(spec=types.CallbackQuery)
    cb.message = MagicMock()
    cb.message.edit_text = AsyncMock()
    cb.message.answer = AsyncMock()
    return cb


def _make_message() -> MagicMock:
    msg = MagicMock(spec=types.Message)
    msg.answer = AsyncMock()
    return msg


def _slide(title="Title", text="Body", visual="Img", slide_id=1):
    return {
        "id": slide_id,
        "slide_title": title,
        "slide_text": text,
        "visual_description": visual,
    }


@pytest.mark.asyncio
async def test_slide_view_escapes_html():
    """HTML special characters in slide content must be escaped."""
    cb = _make_callback()
    slide = _slide(title="A <b>bold</b> & 'quoted'", text="x < y > z", visual="<img>")

    await SlideViewAnswer.run(
        cb,
        {"slide": slide, "index": 0, "total": 1, "presentation_id": 1},
    )

    sent_text = cb.message.edit_text.call_args[0][0]
    assert "&lt;b&gt;" in sent_text
    assert "&amp;" in sent_text
    assert "&lt;img&gt;" in sent_text
    assert "x &lt; y &gt; z" in sent_text


@pytest.mark.asyncio
async def test_slide_view_callback_edit_text():
    """For CallbackQuery, edit_text should be called with markup."""
    cb = _make_callback()

    await SlideViewAnswer.run(
        cb,
        {"slide": _slide(), "index": 0, "total": 3, "presentation_id": 5},
    )

    cb.message.edit_text.assert_awaited_once()
    args, kwargs = cb.message.edit_text.call_args
    assert "reply_markup" in kwargs or len(args) > 1


@pytest.mark.asyncio
async def test_slide_view_message_answer():
    """For Message, answer should be called."""
    msg = _make_message()

    await SlideViewAnswer.run(
        msg,
        {"slide": _slide(), "index": 0, "total": 3, "presentation_id": 5},
    )

    msg.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_slide_view_first_slide_prev_inactive():
    """On first slide, prev button should be inactive (noop)."""
    cb = _make_callback()

    await SlideViewAnswer.run(
        cb,
        {"slide": _slide(), "index": 0, "total": 3, "presentation_id": 5},
    )

    markup = cb.message.edit_text.call_args[1]["reply_markup"]
    nav_row = markup.inline_keyboard[0]
    # First button (prev) should be noop
    assert nav_row[0].callback_data == "noop"
    # Last button (next) should NOT be noop
    assert nav_row[2].callback_data != "noop"


@pytest.mark.asyncio
async def test_slide_view_last_slide_next_inactive():
    """On last slide, next button should be inactive (noop)."""
    cb = _make_callback()

    await SlideViewAnswer.run(
        cb,
        {"slide": _slide(), "index": 2, "total": 3, "presentation_id": 5},
    )

    markup = cb.message.edit_text.call_args[1]["reply_markup"]
    nav_row = markup.inline_keyboard[0]
    # Last button (next) should be noop
    assert nav_row[2].callback_data == "noop"
    # First button (prev) should NOT be noop
    assert nav_row[0].callback_data != "noop"


@pytest.mark.asyncio
async def test_slide_view_counter_text():
    """Counter button should show current/total."""
    cb = _make_callback()

    await SlideViewAnswer.run(
        cb,
        {"slide": _slide(), "index": 1, "total": 5, "presentation_id": 5},
    )

    markup = cb.message.edit_text.call_args[1]["reply_markup"]
    counter_btn = markup.inline_keyboard[0][1]
    assert counter_btn.text == "2/5"


@pytest.mark.asyncio
async def test_slide_view_has_edit_and_done_rows():
    """Markup should have 3 rows: navigation, edit, done."""
    cb = _make_callback()

    await SlideViewAnswer.run(
        cb,
        {"slide": _slide(), "index": 0, "total": 1, "presentation_id": 5},
    )

    markup = cb.message.edit_text.call_args[1]["reply_markup"]
    assert len(markup.inline_keyboard) == 3


@pytest.mark.asyncio
async def test_slide_view_fallback_on_edit_failure():
    """If edit_text fails, should send a new message as fallback."""
    cb = _make_callback()
    cb.message.edit_text = AsyncMock(side_effect=Exception("Bad Request"))

    await SlideViewAnswer.run(
        cb,
        {"slide": _slide(), "index": 0, "total": 1, "presentation_id": 5},
    )

    cb.message.answer.assert_awaited_once()
