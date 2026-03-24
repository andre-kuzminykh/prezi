"""
Test SC001: Creating a presentation from text input via API.

## Traceability
- Feature: F001 (Create Presentation)
- Scenario: SC001 (Text Input)
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_presentation_from_text(client: AsyncClient):
    """SC001: User creates a presentation with text input."""
    response = await client.post(
        "/api/v1/presentations",
        json={
            "user_id": 123456789,
            "title": "My Test Presentation",
            "source_input_type": "text",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 123456789
    assert data["title"] == "My Test Presentation"
    assert data["status"] == "draft"
    assert data["source_input_type"] == "text"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_add_text_input_to_presentation(client: AsyncClient):
    """SC001: User adds text input to an existing presentation."""
    create_resp = await client.post(
        "/api/v1/presentations",
        json={"user_id": 123456789, "title": "Input Test"},
    )
    presentation_id = create_resp.json()["id"]

    response = await client.post(
        f"/api/v1/presentations/{presentation_id}/input",
        json={
            "type": "text",
            "raw_content": "This is a sample presentation about AI trends in 2026.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["presentation_id"] == presentation_id
    assert data["type"] == "text"
    assert "AI trends" in data["raw_content"]


@pytest.mark.asyncio
async def test_get_presentation_by_id(client: AsyncClient):
    """SC001: User retrieves a presentation by its ID."""
    create_resp = await client.post(
        "/api/v1/presentations",
        json={"user_id": 999, "title": "Fetch Test"},
    )
    presentation_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/presentations/{presentation_id}")
    assert response.status_code == 200
    assert response.json()["id"] == presentation_id


@pytest.mark.asyncio
async def test_get_presentation_not_found(client: AsyncClient):
    """SC001: Requesting a non-existent presentation returns 404."""
    response = await client.get("/api/v1/presentations/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_presentations_by_user(client: AsyncClient):
    """SC001: User lists their presentations."""
    await client.post(
        "/api/v1/presentations",
        json={"user_id": 42, "title": "Pres 1"},
    )
    await client.post(
        "/api/v1/presentations",
        json={"user_id": 42, "title": "Pres 2"},
    )
    await client.post(
        "/api/v1/presentations",
        json={"user_id": 99, "title": "Other user"},
    )

    response = await client.get("/api/v1/presentations", params={"user_id": 42})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(p["user_id"] == 42 for p in data)
