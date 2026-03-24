"""
Pydantic schemas for input message operations.

## Traceability
- Feature: F001 (Create Presentation)
- Scenario: SC001, SC002
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from model.enums import InputType


class InputMessageCreateSchema(BaseModel):
    """Schema for creating a new input message."""

    type: InputType
    raw_content: str
    transcript: Optional[str] = None


class InputMessageResponseSchema(BaseModel):
    """Schema for input message API responses."""

    model_config = {"from_attributes": True}

    id: int
    presentation_id: int
    type: InputType
    raw_content: str
    transcript: Optional[str] = None
    created_at: datetime
