"""
Pydantic schemas for edit command operations.

## Traceability
- Feature: F003 (Slide Editing)
- Scenario: SC006, SC007
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from model.enums import EditScope


class EditCommandCreateSchema(BaseModel):
    """Schema for creating a new edit command."""

    scope: EditScope
    target_slide_id: Optional[int] = None
    command_text: str


class EditCommandResponseSchema(BaseModel):
    """Schema for edit command API responses."""

    model_config = {"from_attributes": True}

    id: int
    presentation_id: int
    scope: EditScope
    target_slide_id: Optional[int] = None
    command_text: str
    result_summary: Optional[str] = None
    applied: bool
    created_at: datetime


class ExportResponseSchema(BaseModel):
    """Schema for export operation responses."""

    url: str
