"""Trigger nodes for presentations.

## Traceability
Component: Node / Presentation / Trigger
"""
from node.presentation.trigger.create_presentation_trigger import (
    CreatePresentationTrigger,
)
from node.presentation.trigger.navigate_slide_trigger import NavigateSlideTrigger
from node.presentation.trigger.edit_slide_trigger import EditSlideTrigger

__all__ = [
    "CreatePresentationTrigger",
    "NavigateSlideTrigger",
    "EditSlideTrigger",
]
