"""
SQLAlchemy model for slides.

## Traceability
- Feature: F002 (Auto Structuring)
- Scenario: SC004, SC005
"""

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from model.base_model import Base, BaseModel
from model.enums import SlideStatus


class SlideModel(BaseModel, Base):
    __tablename__ = "slides"

    presentation_id = Column(
        Integer, ForeignKey("presentations.id", ondelete="CASCADE"), nullable=False
    )
    order = Column(Integer, nullable=False)
    slide_title = Column(String, nullable=False)
    slide_text = Column(Text, nullable=False)
    visual_description = Column(Text, nullable=True)
    speaker_notes = Column(Text, nullable=True)
    status = Column(
        Enum(SlideStatus),
        default=SlideStatus.draft,
        nullable=False,
    )

    presentation = relationship("PresentationModel", back_populates="slides")
