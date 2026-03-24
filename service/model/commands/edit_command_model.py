"""
SQLAlchemy model for edit commands.

## Traceability
- Feature: F003 (Slide Editing)
- Scenario: SC006, SC007
"""

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, Text, func
from sqlalchemy.orm import relationship

from model.base_model import Base
from model.enums import EditScope


class EditCommandModel(Base):
    __tablename__ = "edit_commands"

    id = Column(Integer, primary_key=True, autoincrement=True)
    presentation_id = Column(
        Integer, ForeignKey("presentations.id", ondelete="CASCADE"), nullable=False
    )
    scope = Column(Enum(EditScope), nullable=False)
    target_slide_id = Column(Integer, nullable=True)
    command_text = Column(Text, nullable=False)
    result_summary = Column(Text, nullable=True)
    applied = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    presentation = relationship("PresentationModel", back_populates="commands")
