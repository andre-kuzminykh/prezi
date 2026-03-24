"""
Test SC004: LLM structuring creates slides from text input.

## Traceability
- Feature: F002 (Auto Structuring)
- Scenario: SC004 (Structure Slides)
"""

import json
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient


MOCK_LLM_RESPONSE = {
    "slides": [
        {
            "title": "Introduction to AI",
            "text": "Artificial Intelligence is transforming industries worldwide.",
            "visual_description": "A futuristic robot shaking hands with a human.",
        },
        {
            "title": "Key Trends",
            "text": "Major trends include generative AI, autonomous systems, and AI ethics.",
            "visual_description": "A chart showing AI adoption growth over the years.",
        },
        {
            "title": "Future Outlook",
            "text": "AI will continue to evolve and integrate into daily life.",
            "visual_description": "A crystal ball with circuit patterns glowing inside.",
        },
    ]
}


@pytest.mark.asyncio
async def test_structure_presentation_creates_slides(client: AsyncClient):
    """SC004: Structuring a presentation via LLM creates ordered slides."""
    # Create a presentation
    create_resp = await client.post(
        "/api/v1/presentations",
        json={"user_id": 100, "title": "AI Overview"},
    )
    presentation_id = create_resp.json()["id"]

    # Add input text
    await client.post(
        f"/api/v1/presentations/{presentation_id}/input",
        json={
            "type": "text",
            "raw_content": (
                "AI is transforming industries. Key trends include generative AI, "
                "autonomous systems, and ethics. The future looks promising."
            ),
        },
    )

    # Mock the OpenAI call
    mock_message = AsyncMock()
    mock_message.content = json.dumps(MOCK_LLM_RESPONSE)
    mock_choice = AsyncMock()
    mock_choice.message = mock_message
    mock_response = AsyncMock()
    mock_response.choices = [mock_choice]

    with patch(
        "service.llm.llm_service.AsyncOpenAI"
    ) as mock_openai_cls:
        mock_client_instance = AsyncMock()
        mock_client_instance.chat.completions.create = AsyncMock(
            return_value=mock_response
        )
        mock_openai_cls.return_value = mock_client_instance

        # Re-instantiate LLM service with mocked client
        from service.llm.llm_service import LLMService

        patched_service = LLMService()
        patched_service.client = mock_client_instance

        with patch(
            "api.v1.endpoints.presentations.post.llm_service",
            patched_service,
        ):
            response = await client.post(
                f"/api/v1/presentations/{presentation_id}/structure"
            )

    assert response.status_code == 200
    slides = response.json()
    assert len(slides) == 3
    assert slides[0]["order"] == 1
    assert slides[0]["slide_title"] == "Introduction to AI"
    assert slides[1]["order"] == 2
    assert slides[2]["order"] == 3


@pytest.mark.asyncio
async def test_structure_updates_presentation_status(client: AsyncClient):
    """SC004: After structuring, the presentation status becomes 'ready'."""
    create_resp = await client.post(
        "/api/v1/presentations",
        json={"user_id": 200, "title": "Status Test"},
    )
    presentation_id = create_resp.json()["id"]

    await client.post(
        f"/api/v1/presentations/{presentation_id}/input",
        json={"type": "text", "raw_content": "Some content to structure."},
    )

    mock_message = AsyncMock()
    mock_message.content = json.dumps(MOCK_LLM_RESPONSE)
    mock_choice = AsyncMock()
    mock_choice.message = mock_message
    mock_response = AsyncMock()
    mock_response.choices = [mock_choice]

    with patch(
        "service.llm.llm_service.AsyncOpenAI"
    ) as mock_openai_cls:
        mock_client_instance = AsyncMock()
        mock_client_instance.chat.completions.create = AsyncMock(
            return_value=mock_response
        )
        mock_openai_cls.return_value = mock_client_instance

        from service.llm.llm_service import LLMService

        patched_service = LLMService()
        patched_service.client = mock_client_instance

        with patch(
            "api.v1.endpoints.presentations.post.llm_service",
            patched_service,
        ):
            await client.post(
                f"/api/v1/presentations/{presentation_id}/structure"
            )

    get_resp = await client.get(f"/api/v1/presentations/{presentation_id}")
    assert get_resp.json()["status"] == "ready"
