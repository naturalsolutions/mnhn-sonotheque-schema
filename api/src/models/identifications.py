from sqlalchemy import Column, String, UUID, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

from src.database import Base


class Identification(Base):
    __tablename__ = "identifications"

    id = Column(UUID, primary_key=True)
    verification_status = Column(String)
    qualifier = Column(String)
    identification_date = Column(Date)
    notes = Column(String)
    dynamic_properties = Column(JSON)
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    # Foreign keys
    identified_by = Column(UUID, ForeignKey("people.id"))
    review_by = Column(UUID, ForeignKey("people.id"))
    taxon_id = Column(UUID, ForeignKey("taxa.id"))
    occurrence_id = Column(UUID, ForeignKey("occurrences.id"))

    # Relationships with backpopulates
    occurrence = relationship("Occurrence", back_populates="identifications")
    taxon = relationship("Taxon", back_populates="identifications")
    reviewer = relationship(
        "Person", foreign_keys=[review_by], back_populates="reviewed_identifications"
    )
    identifier = relationship(
        "Person",
        foreign_keys=[identified_by],
        back_populates="submitted_identifications",
    )
