"""HTTP client for the FastAPI backend.

## Traceability
Component: Service / API / PresentationAPI
"""
from __future__ import annotations

import logging
from typing import Any

import httpx

from core.config import settings

logger = logging.getLogger(__name__)

API_PREFIX = "/api/v1"


class PresentationAPI:
    """Async HTTP client that communicates with the backend."""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or settings.BACKEND_URL).rstrip("/")

    def _url(self, path: str) -> str:
        return f"{self.base_url}{API_PREFIX}{path}"

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.request(method, self._url(path), **kwargs)
            response.raise_for_status()
            return response

    # ------------------------------------------------------------------
    # Presentations
    # ------------------------------------------------------------------

    async def create_presentation(self, user_id: int) -> dict:
        """Create a new presentation for a user."""
        resp = await self._request("POST", "/presentations", json={"user_id": user_id})
        return resp.json()

    async def get_presentation(self, presentation_id: int) -> dict:
        """Get presentation by id."""
        resp = await self._request("GET", f"/presentations/{presentation_id}")
        return resp.json()

    async def get_user_presentations(self, user_id: int) -> list:
        """List all presentations for a user."""
        resp = await self._request("GET", "/presentations", params={"user_id": user_id})
        return resp.json()

    async def update_presentation(self, presentation_id: int, data: dict) -> dict:
        """Update presentation metadata."""
        resp = await self._request("PATCH", f"/presentations/{presentation_id}", json=data)
        return resp.json()

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    async def add_input(
        self,
        presentation_id: int,
        content: str,
        input_type: str = "text",
    ) -> dict:
        """Add text/voice input to presentation."""
        resp = await self._request(
            "POST",
            f"/presentations/{presentation_id}/inputs",
            json={"content": content, "input_type": input_type},
        )
        return resp.json()

    # ------------------------------------------------------------------
    # Structure
    # ------------------------------------------------------------------

    async def structure_presentation(self, presentation_id: int) -> list[dict]:
        """Trigger AI structuring and return generated slides."""
        resp = await self._request("POST", f"/presentations/{presentation_id}/structure")
        return resp.json()

    # ------------------------------------------------------------------
    # Slides
    # ------------------------------------------------------------------

    async def get_slides(self, presentation_id: int) -> list[dict]:
        """Get all slides for a presentation."""
        resp = await self._request("GET", f"/presentations/{presentation_id}/slides")
        return resp.json()

    async def get_slide(self, presentation_id: int, slide_id: int) -> dict:
        """Get a single slide."""
        resp = await self._request(
            "GET", f"/presentations/{presentation_id}/slides/{slide_id}"
        )
        return resp.json()

    async def update_slide(self, presentation_id: int, slide_id: int, data: dict) -> dict:
        """Update slide fields directly."""
        resp = await self._request(
            "PATCH",
            f"/presentations/{presentation_id}/slides/{slide_id}",
            json=data,
        )
        return resp.json()

    async def edit_slide_nl(
        self,
        presentation_id: int,
        slide_id: int,
        command_text: str,
    ) -> dict:
        """Edit slide via natural-language command."""
        resp = await self._request(
            "POST",
            f"/presentations/{presentation_id}/slides/{slide_id}/edit",
            json={"command": command_text},
        )
        return resp.json()

    async def delete_slide(self, presentation_id: int, slide_id: int) -> None:
        """Delete a slide."""
        await self._request(
            "DELETE", f"/presentations/{presentation_id}/slides/{slide_id}"
        )

    async def create_slide(self, presentation_id: int, data: dict) -> dict:
        """Create a new slide."""
        resp = await self._request(
            "POST", f"/presentations/{presentation_id}/slides", json=data
        )
        return resp.json()

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    async def export_html(self, presentation_id: int) -> dict:
        """Export presentation as HTML. Returns {html_url, content}."""
        resp = await self._request(
            "POST", f"/presentations/{presentation_id}/export/html"
        )
        return resp.json()

    async def export_pdf(self, presentation_id: int) -> bytes:
        """Export presentation as PDF binary."""
        resp = await self._request(
            "POST", f"/presentations/{presentation_id}/export/pdf"
        )
        return resp.content
