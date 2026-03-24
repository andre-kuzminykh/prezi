"""Shared test fixtures.

## Traceability
Component: Tests / Conftest
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from service.api.presentation_api import PresentationAPI


@pytest.fixture()
def api_client() -> PresentationAPI:
    """Return a PresentationAPI with all methods mocked."""
    client = PresentationAPI(base_url="http://test:8000")
    # Replace every public async method with an AsyncMock
    for name in dir(client):
        if name.startswith("_"):
            continue
        attr = getattr(client, name)
        if callable(attr):
            setattr(client, name, AsyncMock())
    return client


@pytest.fixture()
def fake_message() -> MagicMock:
    """Return a mocked aiogram Message."""
    msg = MagicMock()
    msg.from_user = MagicMock()
    msg.from_user.id = 123456
    msg.text = "Тестовый текст для презентации"
    msg.voice = None
    msg.answer = AsyncMock()
    return msg


@pytest.fixture()
def fake_callback() -> MagicMock:
    """Return a mocked aiogram CallbackQuery."""
    cb = MagicMock()
    cb.from_user = MagicMock()
    cb.from_user.id = 123456
    cb.message = MagicMock()
    cb.message.edit_text = AsyncMock()
    cb.message.answer = AsyncMock()
    cb.message.answer_document = AsyncMock()
    cb.answer = AsyncMock()
    cb.data = ""
    return cb


@pytest.fixture()
def fake_state() -> MagicMock:
    """Return a mocked FSMContext."""
    state = MagicMock()
    state.get_data = AsyncMock(return_value={})
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()
    state.clear = AsyncMock()
    return state
