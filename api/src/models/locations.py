from sqlalchemy import Column, DateTime, String, ForeignKey, Float, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from src.database import Base, DefaultColsMixin


class Location(DefaultColsMixin, Base):
    __tablename__ = "locations"

    higher_geography_path = Column(
        String,
        nullable=True,
        comment="Hierarchical path of geographic names less specific than locality",
    )
    geom = Column(
        Geometry("GEOMETRY", srid=4326),
        nullable=True,
        comment="Spatial geometry representing a location as WKB",
    )
    geometry_precision = Column(
        Float, nullable=True, comment="Precision of the coordinates"
    )
    identifier = Column(
        String,
        nullable=False,
        unique=True,
        comment="Unique text identifier used in hierarchical path",
    )
    country = Column(
        String,
        nullable=True,
        comment="Country or major administrative unit of the location",
    )
    state_province = Column(
        String, nullable=True, comment="Administrative region smaller than country"
    )
    municipality = Column(
        String, nullable=True, comment="Smaller administrative region than county"
    )
    locality = Column(
        String, nullable=True, comment="Specific description of the place"
    )
    depth_min = Column(
        Float, nullable=True, comment="Minimum depth below local surface in meters"
    )
    elevation_max = Column(
        Float, nullable=True, comment="Maximum elevation above sea level in meters"
    )
    sampling_remarks = Column(
        JSONB,
        nullable=True,
        comment="Notes about the sampling location including meteorological context",
    )
    remarks = Column(
        String, nullable=True, comment="General comments or notes about the location"
    )
    provided_id = Column(String, nullable=True, comment="External ID from a service")
    provider_source = Column(
        String,
        nullable=True,
        comment="Source URL of the external service providing the ID",
    )
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    ### ForeignKeys ###
    parent_id = Column(
        UUID(as_uuid=True),
        ForeignKey("locations.id"),
        nullable=True,
        comment="Identifier for the parent location",
    )

    ### Relationship with back_populates ###
    sampling_events = relationship("SamplingEvent", back_populates="location")
    occurrences = relationship("Occurrence", back_populates="location")
    organizations = relationship("Organization", back_populates="location")
    media = relationship("Media", back_populates="location")
