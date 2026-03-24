"""Widget: Export presentation (handled by confirm_widget).

## Traceability
Feature: F007, F008
Scenarios: SC012, SC013
"""
from aiogram import Router

router = Router(name="export_widget")
# Export is handled in confirm_widget via the "done" action
