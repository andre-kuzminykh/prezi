"""
Service for generating HTML and PDF exports of presentations.

## Traceability
- Feature: F007 (HTML Generation)
- Scenario: SC012, SC013
"""

from typing import Sequence

from model.presentations.presentation_model import PresentationModel
from model.slides.slide_model import SlideModel
from service.llm.llm_service import LLMService


class ExportService:
    def __init__(self):
        self.llm_service = LLMService()

    async def generate_html(
        self,
        presentation: PresentationModel,
        slides: Sequence[SlideModel],
    ) -> str:
        """Generate HTML presentation via LLM using design kit + slide content."""
        slides_data = [
            {
                "title": s.slide_title,
                "text": s.slide_text,
                "visual_description": s.visual_description or "",
            }
            for s in slides
        ]
        title = presentation.title or "Презентация"
        return await self.llm_service.generate_html(title, slides_data)

    def generate_pdf(self, html_content: str) -> bytes:
        """Convert an HTML string to PDF bytes using WeasyPrint."""
        from weasyprint import HTML

        pdf_bytes = HTML(string=html_content).write_pdf()
        return pdf_bytes
