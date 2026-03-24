"""
SQLAlchemy model for presentations.

## Traceability
- Feature: F001 (Create Presentation)
- Scenario: SC001, SC002, SC003
"""

from sqlalchemy import BigInteger, Column, Enum, String
from sqlalchemy.orm import relationship

from model.base_model import Base, BaseModel
from model.enums import PresentationStatus, SourceInputType


class PresentationModel(BaseModel, Base):
    __tablename__ = "presentations"

    user_id = Column(BigInteger, nullable=False, index=True)
    title = Column(String, nullable=True)
    status = Column(
        Enum(PresentationStatus),
        default=PresentationStatus.draft,
        nullable=False,
    )
    source_input_type = Column(Enum(SourceInputType), nullable=True)
    html_output_url = Column(String, nullable=True)
    pdf_output_url = Column(String, nullable=True)

    slides = relationship(
        "SlideModel",
        back_populates="presentation",
        cascade="all, delete-orphan",
        order_by="SlideModel.order",
    )
    inputs = relationship(
        "InputMessageModel",
        back_populates="presentation",
        cascade="all, delete-orphan",
    )
    commands = relationship(
        "EditCommandModel",
        back_populates="presentation",
        cascade="all, delete-orphan",
    )
