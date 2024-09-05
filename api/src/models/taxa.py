from sqlalchemy import Column, DateTime, Integer, String, Boolean, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from src.database import Base


class Taxon(Base):
    __tablename__ = "taxa"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Taxon internal identifier See: http://purl.org/dc/terms/identifier",
    )
    legacy_id = Column(
        Integer,
        comment="Legacy Taxon identifier from previous database; See: http://purl.org/dc/terms/identifier",
    )
    original_scientific_name = Column(
        String,
        comment="Taxon scientific name as recorded in the previousSonotheque database",
    )
    gbif_key = Column(Integer, comment="GBIF taxon identifier")
    gbif_name_key = Column(Integer, comment="GBIF taxon name identifier")
    gbif_parent_key = Column(Integer, comment="GBIF parent taxon identifier")
    gbif_dataset_key = Column(Integer, comment="GBIF dataset identifier")
    vernacular_name = Column(String, comment="Taxon vernacular name")
    kingdom = Column(String, comment="Taxon kingdom")
    phylum = Column(String, comment="Taxon phylum")
    class_ = Column(String, comment="Taxon class")
    order = Column(String, comment="Taxon order")
    family = Column(String, comment="Taxon family")
    genus = Column(String, comment="Taxon genus")
    species = Column(String, comment="Taxon species epithet")
    scientific_name = Column(String, comment="Taxon scientific name")
    canonical_name = Column(String, comment="Taxon canonical name")
    original_vernacular_names = Column(
        JSONB,
        comment="Taxon vernacular names with language as recorded in the previous Sonotheque database",
    )
    vernacular_name_english = Column(String)
    vernacular_name_french = Column(String)
    rank = Column(String)
    status = Column(String)
    synonym = Column(Boolean)
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship

    occurrences = relationship("Occurrence", back_populates="taxon")
    identifications = relationship("Identification", back_populates="taxon")
