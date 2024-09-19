from sqlalchemy import Column, DateTime, String, UUID, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship

from src.database import Base


class Occurrence(Base):
    __tablename__ = "occurrences"

    id = Column(UUID, primary_key=True)
    behavior = Column(String)
    life_stage = Column(String)
    sex = Column(String)
    degree_of_establishment = Column(String)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Foreign keys
    media_id = Column(UUID, ForeignKey("media.id"))
    # just a memory aid
    # media_id = Column(UUID(as_uuid=True), ForeignKey("media.id"))
    taxa_id = Column(UUID, ForeignKey("taxa.id"))
    location_id = Column(UUID, ForeignKey("locations.id"))
    acoustic_event_id = Column(UUID, ForeignKey("acoustic_events.id"))

    # Relationships with backpopulates
    media = relationship("Media", back_populates="occurrences")
    taxon = relationship("Taxon", back_populates="occurrences")
    location = relationship("Location", back_populates="occurrences")
    acoustic_event = relationship("AcousticEvent", back_populates="occurrences")

    identifications = relationship("Identification", back_populates="occurrence")
