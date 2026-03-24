"""
Test SC012: HTML generation from presentation and slides.

## Traceability
- Feature: F007 (HTML Generation)
- Scenario: SC012 (Generate HTML)
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_generate_html_for_presentation(client: AsyncClient):
    """SC012: Generating HTML returns a valid HTML document with slide content."""
    # Create presentation
    create_resp = await client.post(
        "/api/v1/presentations",
        json={"user_id": 300, "title": "HTML Export Test"},
    )
    presentation_id = create_resp.json()["id"]

    # Create slides directly
    await client.post(
        f"/api/v1/presentations/{presentation_id}/slides",
        json={
            "order": 1,
            "slide_title": "First Slide",
            "slide_text": "This is the first slide content.",
            "visual_description": "A bright opening image.",
        },
    )
    await client.post(
        f"/api/v1/presentations/{presentation_id}/slides",
        json={
            "order": 2,
            "slide_title": "Second Slide",
            "slide_text": "This is the second slide content.",
        },
    )

    # Generate HTML
    response = await client.post(
        f"/api/v1/presentations/{presentation_id}/export/html"
    )
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    html = response.text
    assert "HTML Export Test" in html
    assert "First Slide" in html
    assert "Second Slide" in html
    assert "first slide content" in html
    assert "bright opening image" in html


@pytest.mark.asyncio
async def test_generate_html_empty_presentation(client: AsyncClient):
    """SC012: Generating HTML for a presentation with no slides still returns valid HTML."""
    create_resp = await client.post(
        "/api/v1/presentations",
        json={"user_id": 301, "title": "Empty Pres"},
    )
    presentation_id = create_resp.json()["id"]

    response = await client.post(
        f"/api/v1/presentations/{presentation_id}/export/html"
    )
    assert response.status_code == 200
    html = response.text
    assert "Empty Pres" in html
    assert "<!DOCTYPE html>" in html


@pytest.mark.asyncio
async def test_generate_html_not_found(client: AsyncClient):
    """SC012: Generating HTML for a non-existent presentation returns 404."""
    response = await client.post(
        "/api/v1/presentations/99999/export/html"
    )
    assert response.status_code == 404
