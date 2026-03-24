"""
SQLAlchemy declarative base and shared BaseModel mixin.

## Traceability
- Feature: F000 (Application Bootstrap)
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel:
    """Mixin providing common fields for all models."""

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
