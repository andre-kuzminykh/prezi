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
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.request(method, self._url(path), **kwargs)
            response.raise_for_status()
            return response

    # Presentations

    async def create_presentation(self, user_id: int) -> dict:
        resp = await self._request("POST", "/presentations", json={"user_id": user_id})
        return resp.json()

    async def get_presentation(self, presentation_id: int) -> dict:
        resp = await self._request("GET", f"/presentations/{presentation_id}")
        return resp.json()

    async def get_user_presentations(self, user_id: int) -> list:
        resp = await self._request("GET", "/presentations", params={"user_id": user_id})
        return resp.json()

    async def update_presentation(self, presentation_id: int, data: dict) -> dict:
        resp = await self._request("PATCH", f"/presentations/{presentation_id}", json=data)
        return resp.json()

    # Input

    async def add_input(
        self,
        presentation_id: int,
        content: str,
        input_type: str = "text",
    ) -> dict:
        resp = await self._request(
            "POST",
            f"/presentations/{presentation_id}/input",
            json={"type": input_type, "raw_content": content},
        )
        return resp.json()

    # Structure

    async def structure_presentation(self, presentation_id: int) -> list[dict]:
        resp = await self._request(
            "POST",
            f"/presentations/{presentation_id}/structure",
            timeout=httpx.Timeout(120.0),
        )
        return resp.json()

    # Slides

    async def get_slides(self, presentation_id: int) -> list[dict]:
        resp = await self._request("GET", f"/presentations/{presentation_id}/slides")
        return resp.json()

    async def get_slide(self, presentation_id: int, slide_id: int) -> dict:
        resp = await self._request(
            "GET", f"/presentations/{presentation_id}/slides/{slide_id}"
        )
        return resp.json()

    async def update_slide(self, presentation_id: int, slide_id: int, data: dict) -> dict:
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
        resp = await self._request(
            "POST",
            f"/presentations/{presentation_id}/slides/{slide_id}/edit",
            json={"command_text": command_text},
            timeout=httpx.Timeout(60.0),
        )
        return resp.json()

    async def delete_slide(self, presentation_id: int, slide_id: int) -> None:
        await self._request(
            "DELETE", f"/presentations/{presentation_id}/slides/{slide_id}"
        )

    async def create_slide(self, presentation_id: int, data: dict) -> dict:
        resp = await self._request(
            "POST", f"/presentations/{presentation_id}/slides", json=data
        )
        return resp.json()

    # Export

    async def export_html(self, presentation_id: int) -> dict:
        resp = await self._request(
            "POST",
            f"/presentations/{presentation_id}/export/html",
            timeout=httpx.Timeout(60.0),
        )
        return {"content": resp.text}

    # Transcription

    async def transcribe(self, audio_base64: str) -> str:
        """Transcribe base64-encoded audio via the backend."""
        resp = await self._request(
            "POST",
            "/transcribe",
            json={"audio_base64": audio_base64},
            timeout=httpx.Timeout(60.0),
        )
        return resp.json()["text"]

    async def export_pdf(self, presentation_id: int) -> bytes:
        resp = await self._request(
            "POST",
            f"/presentations/{presentation_id}/export/pdf",
            timeout=httpx.Timeout(120.0),
        )
        return resp.content
