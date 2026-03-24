"""
SQLAlchemy model for input messages (text or voice).

## Traceability
- Feature: F001 (Create Presentation)
- Scenario: SC001, SC002
"""

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Text, func
from sqlalchemy.orm import relationship

from model.base_model import Base
from model.enums import InputType


class InputMessageModel(Base):
    __tablename__ = "input_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    presentation_id = Column(
        Integer, ForeignKey("presentations.id", ondelete="CASCADE"), nullable=False
    )
    type = Column(Enum(InputType), nullable=False)
    raw_content = Column(Text, nullable=False)
    transcript = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    presentation = relationship("PresentationModel", back_populates="inputs")
