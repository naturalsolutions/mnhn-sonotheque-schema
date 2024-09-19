from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from src.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        comment="An identifier for the set of resources",
        server_default=func.gen_random_uuid(),
    )
    name = Column(
        String,
        nullable=False,
        comment="The name identifying the data set from which the record was derived.",
    )
    description = Column(String, nullable=False, comment="Description of the dataset")
    doi = Column(
        String,
        comment="Publication unique identifier for a reference associated to this datasets",
    )
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=False,
        comment="Foreign Key to the dataset creator",
    )
    maintained_by = Column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=False,
        comment="Foreign Key to the dataset maintainers; just one maintainer for a given dataset in this version of the schema",
    )
    contact = Column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=False,
        comment="Foreign Key to the contact person for this dataset",
    )
    published_by = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        comment="Foreign Key to the organization",
    )
    created_at = Column(
        DateTime, nullable=False, comment="Creation datetime for this resource"
    )
    updated_at = Column(
        DateTime, nullable=False, comment="Modification datetime for this resource"
    )
    dynamic_properties = Column(
        JSONB,
        nullable=False,
        comment="Flexible JSON schema to store additional properties",
    )
    creator = relationship(
        "Person", foreign_keys=[created_by], backref="created_datasets"
    )
    maintainer = relationship(
        "Person", foreign_keys=[maintained_by], backref="maintained_datasets"
    )
