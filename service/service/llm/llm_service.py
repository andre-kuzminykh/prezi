"""
LLM service for AI-powered text structuring and slide editing.

## Traceability
- Feature: F002 (Auto Structuring)
- Feature: F003 (Slide Editing)
- Scenario: SC004, SC005, SC006, SC007
"""

import json

from openai import AsyncOpenAI

from core.config import config

STRUCTURE_SYSTEM_PROMPT = """You are a presentation structuring assistant.
Analyze the provided text and break it into logical presentation slides.
Return a JSON array of slide objects. Each object must have:
- "title": a concise slide title
- "text": the main content for the slide
- "visual_description": a brief description of a suitable visual or illustration

Return ONLY the JSON array, no other text."""

EDIT_SLIDE_SYSTEM_PROMPT = """You are a presentation slide editor.
You will receive the current slide content and an edit instruction.
Apply the instruction and return a JSON object with the updated fields:
- "title": updated slide title
- "text": updated slide text
- "visual_description": updated visual description

Return ONLY the JSON object, no other text."""

EDIT_PRESENTATION_SYSTEM_PROMPT = """You are a presentation editor.
You will receive all slides of a presentation and a global edit instruction.
Apply the instruction across all slides and return a JSON array of updated slide objects.
Each object must have:
- "title": the slide title
- "text": the slide text
- "visual_description": the visual description

Return ONLY the JSON array, no other text."""


class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_MODEL

    async def structure_text(self, text: str) -> list[dict]:
        """Analyze text and return a structured list of slides."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": STRUCTURE_SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        content = response.choices[0].message.content
        parsed = json.loads(content)
        if isinstance(parsed, dict) and "slides" in parsed:
            return parsed["slides"]
        if isinstance(parsed, list):
            return parsed
        return parsed.get("slides", [])

    async def edit_slide(
        self,
        current_title: str,
        current_text: str,
        current_visual: str,
        instruction: str,
    ) -> dict:
        """Edit a single slide based on a natural-language instruction."""
        user_content = (
            f"Current slide:\n"
            f"Title: {current_title}\n"
            f"Text: {current_text}\n"
            f"Visual: {current_visual}\n\n"
            f"Instruction: {instruction}"
        )
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": EDIT_SLIDE_SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        content = response.choices[0].message.content
        return json.loads(content)

    async def edit_presentation(
        self, slides: list[dict], instruction: str
    ) -> list[dict]:
        """Apply a global edit instruction across all slides."""
        slides_text = json.dumps(slides, indent=2)
        user_content = (
            f"Current slides:\n{slides_text}\n\n"
            f"Instruction: {instruction}"
        )
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": EDIT_PRESENTATION_SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        content = response.choices[0].message.content
        parsed = json.loads(content)
        if isinstance(parsed, dict) and "slides" in parsed:
            return parsed["slides"]
        if isinstance(parsed, list):
            return parsed
        return parsed.get("slides", [])
