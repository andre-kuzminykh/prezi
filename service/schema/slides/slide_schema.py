"""
Pydantic schemas for slide CRUD and edit operations.

## Traceability
- Feature: F002 (Auto Structuring)
- Feature: F003 (Slide Editing)
- Scenario: SC004, SC005, SC006, SC007
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from model.enums import SlideStatus


class SlideCreateSchema(BaseModel):
    """Schema for creating a new slide."""

    order: int
    slide_title: str
    slide_text: str
    visual_description: Optional[str] = None
    speaker_notes: Optional[str] = None


class SlideUpdateSchema(BaseModel):
    """Schema for updating an existing slide."""

    order: Optional[int] = None
    slide_title: Optional[str] = None
    slide_text: Optional[str] = None
    visual_description: Optional[str] = None
    speaker_notes: Optional[str] = None
    status: Optional[SlideStatus] = None


class SlideResponseSchema(BaseModel):
    """Schema for slide API responses."""

    model_config = {"from_attributes": True}

    id: int
    presentation_id: int
    order: int
    slide_title: str
    slide_text: str
    visual_description: Optional[str] = None
    speaker_notes: Optional[str] = None
    status: SlideStatus
    created_at: datetime
    updated_at: datetime


class SlideEditRequestSchema(BaseModel):
    """Schema for natural-language slide edit via LLM."""

    command_text: str
