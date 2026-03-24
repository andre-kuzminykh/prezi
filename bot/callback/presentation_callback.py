"""CallbackData factories for presentation interactions.

## Traceability
Component: Callback / PresentationCallback
"""
from aiogram.filters.callback_data import CallbackData


class SlideNavigationCallback(CallbackData, prefix="slide"):
    """Navigate between slides."""

    action: str  # prev / next / view
    presentation_id: int
    slide_index: int


class SlideActionCallback(CallbackData, prefix="sact"):
    """Actions on a specific slide."""

    action: str  # edit / delete / add_after / confirm
    presentation_id: int
    slide_id: int


class PresentationCallback(CallbackData, prefix="pres"):
    """Presentation-level actions."""

    action: str  # structure / export_html / export_pdf / confirm / back
    presentation_id: int
