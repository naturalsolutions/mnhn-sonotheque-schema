from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from src.database import Base, DefaultColsMixin


class Organization(DefaultColsMixin, Base):
    __tablename__ = "organizations"

    parent_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=True,
        comment="FK to represent hierarchy in organization, e.g., main organizations and units",
    )
    name = Column(String, nullable=False, comment="Name of the organizations")
    type = Column(String, nullable=False, comment="Category of the organization")
    contact = Column(
        String, nullable=True, comment="Free text form for contact information"
    )
    contact_id = Column(
        UUID(as_uuid=True),
        ForeignKey("people.id"),
        nullable=True,
        comment="Foreign Key to the orgzanization contact; just one contact for a given organization in this version of the schema",
    )
    location_id = Column(
        UUID(as_uuid=True),
        ForeignKey("locations.id"),
        nullable=True,
        comment="FK to location",
    )
    description = Column(
        String, nullable=True, comment="Description of the organization"
    )
    dynamic_properties = Column(
        JSONB,
        nullable=False,
        comment="Flexible JSON schema to store additional properties",
    )

    # children = relationship("Organization", backref="parent")
    parent = relationship(
        "Organization",
        foreign_keys=[parent_id],
        remote_side=[id],
        backref="children",
    )

    contact_person = relationship(
        "Person", foreign_keys=[contact_id], backref="organizations"
    )
    location = relationship("Location", back_populates="organizations")

    def to_dict(self, include_relationships=False):
        """Converts the Organization object into a dictionary, optionally including relationships."""
        org_dict = {
            "id": str(self.id),
            "parent_id": str(self.parent_id) if self.parent_id else None,
            "name": self.name,
            "type": self.type,
            "contact": self.contact,
            "contact_id": str(self.contact_id) if self.contact_id else None,
            "description": self.description,
            "dynamic_properties": self.dynamic_properties,
        }

        if include_relationships:
            org_dict["children"] = (
                [child.to_dict() for child in self.children] if self.children else []
            )
            org_dict["parent"] = self.parent.to_dict() if self.parent else None
            org_dict["contact_person"] = (
                self.contact_person.to_dict() if self.contact_person else None
            )

        return org_dict
