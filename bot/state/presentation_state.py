"""FSM states for the presentation flow.

## Traceability
Component: State / PresentationState
"""
from aiogram.fsm.state import State, StatesGroup


class PresentationState(StatesGroup):
    """States for the presentation creation / editing workflow."""

    collecting_input = State()
    viewing_slides = State()
    editing_slide = State()
    confirming = State()
