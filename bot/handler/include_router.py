"""Register all widget routers on the dispatcher.

## Traceability
Component: Handler / Router Setup
"""
from __future__ import annotations

from aiogram import Dispatcher

from handler.v1.user.presentation.F001.create_widget import (
    router as create_router,
)
from handler.v1.user.presentation.F003.navigate_widget import (
    router as navigate_router,
)
from handler.v1.user.presentation.F004.edit_widget import (
    router as edit_router,
)
from handler.v1.user.presentation.F006.confirm_widget import (
    router as confirm_router,
)
from handler.v1.user.presentation.F008.export_widget import (
    router as export_router,
)


def setup_routers(dp: Dispatcher) -> None:
    """Include all feature routers into the dispatcher."""
    dp.include_router(create_router)
    dp.include_router(navigate_router)
    dp.include_router(edit_router)
    dp.include_router(confirm_router)
    dp.include_router(export_router)
