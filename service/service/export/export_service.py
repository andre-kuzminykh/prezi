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
        """Convert LLM-generated HTML into a landscape PDF with one slide per page."""
        from weasyprint import HTML

        # Inject print-specific CSS so each .slide becomes a separate
        # landscape page and horizontal scroll layout is removed.
        print_css = """
<style>
@page { size: landscape; margin: 0; }
html, body {
    display: block !important;
    overflow: visible !important;
    width: auto !important;
    height: auto !important;
    scroll-snap-type: none !important;
}
.slide {
    width: 100vw !important;
    height: 100vh !important;
    page-break-after: always;
    break-after: page;
    flex: none !important;
    scroll-snap-align: unset !important;
}
.slide:last-child { page-break-after: auto; break-after: auto; }
.aurora-blob { animation: none !important; }
</style>
"""
        # Insert before closing </head>
        if "</head>" in html_content:
            html_content = html_content.replace("</head>", print_css + "</head>")
        else:
            html_content = print_css + html_content

        pdf_bytes = HTML(string=html_content).write_pdf()
        return pdf_bytes
