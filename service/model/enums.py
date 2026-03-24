"""
Enum types used across the application models.

## Traceability
- Feature: F001 (Create Presentation)
- Feature: F002 (Auto Structuring)
- Feature: F003 (Slide Editing)
"""

import enum


class PresentationStatus(str, enum.Enum):
    draft = "draft"
    structuring = "structuring"
    ready = "ready"
    generated = "generated"
    exported = "exported"


class SlideStatus(str, enum.Enum):
    draft = "draft"
    edited = "edited"
    approved = "approved"


class InputType(str, enum.Enum):
    voice = "voice"
    text = "text"
    command = "command"


class SourceInputType(str, enum.Enum):
    voice = "voice"
    text = "text"
    mixed = "mixed"


class EditScope(str, enum.Enum):
    presentation = "presentation"
    slide = "slide"
