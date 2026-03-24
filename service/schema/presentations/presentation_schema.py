"""
Pydantic schemas for presentation CRUD operations.

## Traceability
- Feature: F001 (Create Presentation)
- Scenario: SC001, SC002, SC003
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from model.enums import PresentationStatus, SourceInputType


class PresentationCreateSchema(BaseModel):
    """Schema for creating a new presentation."""

    user_id: int
    title: Optional[str] = None
    source_input_type: Optional[SourceInputType] = None


class PresentationUpdateSchema(BaseModel):
    """Schema for updating an existing presentation."""

    title: Optional[str] = None
    status: Optional[PresentationStatus] = None
    source_input_type: Optional[SourceInputType] = None
    html_output_url: Optional[str] = None
    pdf_output_url: Optional[str] = None


class PresentationResponseSchema(BaseModel):
    """Schema for presentation API responses."""

    model_config = {"from_attributes": True}

    id: int
    user_id: int
    title: Optional[str] = None
    status: PresentationStatus
    source_input_type: Optional[SourceInputType] = None
    html_output_url: Optional[str] = None
    pdf_output_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class StructureRequestSchema(BaseModel):
    """Schema for triggering LLM structuring on a presentation."""

    presentation_id: int
