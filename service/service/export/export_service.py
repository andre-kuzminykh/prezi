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

    async def generate_pdf(self, html_content: str) -> bytes:
        """Render HTML in headless Chromium and print to landscape PDF.

        Each slide (100vw x 100vh) becomes a separate PDF page that looks
        exactly like it does in the browser.
        """
        from playwright.async_api import async_playwright

        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            page = await browser.new_page(viewport={"width": 1280, "height": 720})
            await page.set_content(html_content, wait_until="networkidle")

            # Count slides to set the correct page dimensions
            slide_count = await page.locator(".slide").count()
            if slide_count == 0:
                slide_count = 1

            # Scroll through all slides so fonts / animations settle
            for i in range(slide_count):
                await page.evaluate(f"window.scrollTo({i * 1280}, 0)")
                await page.wait_for_timeout(100)
            await page.evaluate("window.scrollTo(0, 0)")

            pdf_bytes = await page.pdf(
                width="1280px",
                height="720px",
                landscape=True,
                print_background=True,
                prefer_css_page_size=False,
            )

            await browser.close()

        return pdf_bytes
