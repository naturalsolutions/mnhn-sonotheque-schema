from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class OrganizationSchema(BaseModel):
    id: UUID = Field(..., description="Organization DB unique identifier")
    parent_id: Optional[UUID] = Field(
        None,
        description="FK to represent hierarchy in organization, e.g., main organizations and units",
    )
    name: str = Field(..., description="Name of the organizations")
    type: str = Field(..., description="Category of the organization")
    contact: Optional[str] = Field(
        None, description="Free text form for contact information"
    )
    located_in: Optional[UUID] = Field(None, description="FK to location")
    description: Optional[str] = Field(
        None, description="Description of the organization"
    )
    dynamic_properties: dict = Field(
        ..., description="Flexible JSON schema to store additional properties"
    )
