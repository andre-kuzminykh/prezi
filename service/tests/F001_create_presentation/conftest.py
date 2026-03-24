"""
Fixtures specific to F001 Create Presentation tests.

## Traceability
- Feature: F001 (Create Presentation)
"""

import pytest_asyncio


@pytest_asyncio.fixture
async def sample_presentation_data():
    """Provide sample data for creating a presentation."""
    return {
        "user_id": 123456789,
        "title": "Test Presentation",
        "source_input_type": "text",
    }
