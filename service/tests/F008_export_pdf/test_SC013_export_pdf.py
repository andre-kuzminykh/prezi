"""SC013: PDF export generates a valid PDF document.

## Traceability
Feature: F008
Scenario: SC013
"""
from unittest.mock import patch, MagicMock

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_export_pdf_returns_pdf_bytes(client: AsyncClient):
    """SC013: Exporting PDF returns valid response with PDF content-type."""
    # Create presentation with slides
    create_resp = await client.post(
        "/api/v1/presentations",
        json={"user_id": 400, "title": "PDF Export Test"},
    )
    presentation_id = create_resp.json()["id"]

    await client.post(
        f"/api/v1/presentations/{presentation_id}/slides",
        json={
            "order": 1,
            "slide_title": "PDF Slide",
            "slide_text": "Content for PDF.",
            "visual_description": "A diagram.",
        },
    )

    # Mock WeasyPrint to avoid needing system dependencies
    fake_pdf = b"%PDF-1.4 fake pdf content"
    with patch(
        "service.export.export_service.ExportService.generate_pdf",
        return_value=fake_pdf,
    ):
        response = await client.post(
            f"/api/v1/presentations/{presentation_id}/export/pdf"
        )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content == fake_pdf


@pytest.mark.asyncio
async def test_export_pdf_not_found(client: AsyncClient):
    """SC013: Exporting PDF for non-existent presentation returns 404."""
    response = await client.post(
        "/api/v1/presentations/99999/export/pdf"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_export_html_then_pdf_consistency(client: AsyncClient):
    """SC013: HTML and PDF export use the same template rendering."""
    create_resp = await client.post(
        "/api/v1/presentations",
        json={"user_id": 401, "title": "Consistency Test"},
    )
    presentation_id = create_resp.json()["id"]

    await client.post(
        f"/api/v1/presentations/{presentation_id}/slides",
        json={
            "order": 1,
            "slide_title": "Consistent Slide",
            "slide_text": "Same content.",
        },
    )

    # Get HTML
    html_resp = await client.post(
        f"/api/v1/presentations/{presentation_id}/export/html"
    )
    assert html_resp.status_code == 200
    html_content = html_resp.text
    assert "Consistent Slide" in html_content
    assert "Same content." in html_content

    # Mock PDF generation but verify HTML is passed through
    captured_html = {}

    def mock_generate_pdf(html_str):
        captured_html["value"] = html_str
        return b"%PDF-1.4"

    with patch(
        "service.export.export_service.ExportService.generate_pdf",
        side_effect=mock_generate_pdf,
    ):
        pdf_resp = await client.post(
            f"/api/v1/presentations/{presentation_id}/export/pdf"
        )

    assert pdf_resp.status_code == 200
    assert "Consistent Slide" in captured_html["value"]


@pytest.mark.asyncio
async def test_export_service_generate_html_directly():
    """Unit test: ExportService.generate_html renders the template."""
    from service.export.export_service import ExportService

    svc = ExportService()

    presentation = MagicMock()
    presentation.title = "Unit Test Pres"

    slide = MagicMock()
    slide.slide_title = "Slide Title"
    slide.slide_text = "Slide body text"
    slide.visual_description = "An illustration"

    html = svc.generate_html(presentation, [slide])

    assert "<!DOCTYPE html>" in html
    assert "Unit Test Pres" in html
    assert "Slide Title" in html
    assert "Slide body text" in html
    assert "An illustration" in html
