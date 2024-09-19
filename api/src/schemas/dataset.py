from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class DatasetSchema(BaseModel):
    id: UUID = Field(..., description="An identifier for the set of resources")
    name: str = Field(
        ...,
        description="The name identifying the data set from which the record was derived.",
    )
    description: str = Field(..., description="Description of the dataset")
    doi: Optional[str] = Field(
        None,
        description="Publication unique identifier for a reference associated to this datasets",
    )
    created_by: Optional[UUID] = Field(None, description="Foreign Key to the dataset creator")
    maintained_by: Optional[UUID] = Field(
        None,
        description="Foreign Key to the dataset maintainers; just one maintainer for a given dataset in this version of the schema",
    )
    contact: UUID = Field(
        ..., description="Foreign Key to the contact person for this dataset"
    )
    published_by: Optional[UUID] = Field(..., description="Foreign Key to the organization")
    created_at: datetime = Field(..., description="Creation datetime for this resource")
    updated_at: datetime = Field(
        ..., description="Modification datetime for this resource"
    )
    dynamic_properties: dict = Field(
        ..., description="Flexible JSON schema to store additional properties"
    )
