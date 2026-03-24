"""Answer nodes for presentations.

## Traceability
Component: Node / Presentation / Answer
"""
from node.presentation.answer.presentation_created_answer import (
    PresentationCreatedAnswer,
)
from node.presentation.answer.slide_view_answer import SlideViewAnswer
from node.presentation.answer.slide_edited_answer import SlideEditedAnswer
from node.presentation.answer.export_ready_answer import ExportReadyAnswer
from node.presentation.answer.error_answer import ErrorAnswer

__all__ = [
    "PresentationCreatedAnswer",
    "SlideViewAnswer",
    "SlideEditedAnswer",
    "ExportReadyAnswer",
    "ErrorAnswer",
]
