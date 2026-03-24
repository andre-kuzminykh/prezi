"""
POST endpoints for exporting presentations.

## Traceability
- Feature: F007 (HTML Generation)
- Scenario: SC012, SC013
"""

from fastapi import Depends
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.endpoints.export import router
from core.database import get_session
from service.export.export_service import ExportService
from service.presentations.presentation_service import PresentationService
from service.slides.slide_service import SlideService

presentation_service = PresentationService()
slide_service = SlideService()
export_service = ExportService()


@router.post("/html")
async def export_html(
    presentation_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Generate and return HTML for a presentation."""
    presentation = await presentation_service.get_presentation(
        presentation_id, session
    )
    slides = await slide_service.get_slides(presentation_id, session)
    html_content = export_service.generate_html(presentation, slides)
    return HTMLResponse(content=html_content)


@router.post("/pdf")
async def export_pdf(
    presentation_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Generate and return PDF for a presentation."""
    presentation = await presentation_service.get_presentation(
        presentation_id, session
    )
    slides = await slide_service.get_slides(presentation_id, session)
    html_content = export_service.generate_html(presentation, slides)
    pdf_bytes = export_service.generate_pdf(html_content)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="presentation_{presentation_id}.pdf"'
        },
    )
