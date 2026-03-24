"""CallbackData factories for presentation interactions.

## Traceability
Component: Callback / PresentationCallback
"""
from aiogram.filters.callback_data import CallbackData


class SlideNavigationCallback(CallbackData, prefix="sn"):
    """Navigate between slides."""
    action: str  # prev / next
    presentation_id: int
    slide_index: int


class SlideActionCallback(CallbackData, prefix="sa"):
    """Actions on a specific slide."""
    action: str  # edit
    presentation_id: int
    slide_id: int


class PresentationCallback(CallbackData, prefix="pc"):
    """Presentation-level actions."""
    action: str  # structure / done
    presentation_id: int
