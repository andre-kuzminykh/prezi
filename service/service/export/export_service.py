"""
Service for generating HTML and PDF exports of presentations.

## Traceability
- Feature: F007 (HTML Generation)
- Scenario: SC012, SC013
"""

from pathlib import Path
from typing import Sequence

from jinja2 import Environment, FileSystemLoader

from model.presentations.presentation_model import PresentationModel
from model.slides.slide_model import SlideModel

TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "templates"


class ExportService:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=False,  # We need raw HTML in the template
        )

    def generate_html(
        self,
        presentation: PresentationModel,
        slides: Sequence[SlideModel],
    ) -> str:
        """Render the presentation as an HTML string using the Jinja2 template."""
        template = self.env.get_template("presentation.html")
        return template.render(
            presentation=presentation,
            slides=slides,
        )

    def generate_pdf(self, html_content: str) -> bytes:
        """Convert an HTML string to PDF bytes using WeasyPrint."""
        from weasyprint import HTML

        pdf_bytes = HTML(string=html_content).write_pdf()
        return pdf_bytes
