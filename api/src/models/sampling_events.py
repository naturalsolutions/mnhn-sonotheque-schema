from sqlalchemy import Column, ARRAY, TIMESTAMP, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from src.database import Base, DefaultColsMixin


class SamplingEvent(DefaultColsMixin, Base):
    __tablename__ = "sampling_events"

    parent_id = Column(
        UUID(as_uuid=True),
        comment="An identifier for the broader dwc:Event that groups this and potentially other dwc:Events.",
    )
    basis_of_record = Column(
        ARRAY(Text),
        comment="Type of record collected in the sampling event: whether Human Observation or Machine Observation",
    )
    type = Column(
        Text,
        comment="The nature of the dwc:Event. Recommended best practice is to use a controlled vocabulary.",
    )
    sampling_protocol = Column(
        Text,
        comment="The names of, references to, or descriptions of the methods or protocols used during a dwc:Event.",
    )
    started_at = Column(
        TIMESTAMP, comment="The date-time or interval during which a dwc:Event occurred"
    )
    ended_at = Column(
        TIMESTAMP, comment="The date-time or interval during which a dwc:Event occurred"
    )
    date_range = Column(
        ARRAY(TIMESTAMP),
        comment="The date-time or interval during which a dwc:Event occurred",
    )
    habitat = Column(
        Text,
        comment="A category or description of the habitat in which the dwc:Event occurred.",
    )
    notes = Column(Text, comment="Comments or notes about the dwc:Event.")
    measurements_or_facts = Column(
        JSONB,
        comment="A list (concatenated and separated) of additional measurements or characteristics of the Event.",
    )
    location_id = Column(
        UUID(as_uuid=True),
        ForeignKey("locations.id"),
        nullable=True,
        comment="Foreign Key to the location of the sampling event",
    )

    ### # Relationship with backref ###
    parent = relationship("SamplingEvents", backref="children", remote_side=[id])
    medias = relationship("Media", backref="sampling_event")
