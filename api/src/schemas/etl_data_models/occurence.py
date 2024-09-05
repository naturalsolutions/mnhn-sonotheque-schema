from datetime import datetime
from typing import Optional
from patito import Model, Field, UUID4



class OccurrenceBase(Model):
    behavior: Optional[str] = Field(None, description="Behavior of the occurrence")
    life_stage: Optional[str] = Field(None, description="Life stage of the occurrence")
    sex: Optional[str] = Field(None, description="Sex of the occurrence")
    degree_of_establishment: Optional[str] = Field(None, description="Degree of establishment of the occurrence")
    media_id: Optional[UUID4] = Field(None, description="Media identifier associated with the occurrence")
    taxa_id: Optional[UUID4] = Field(None, description="Taxa identifier associated with the occurrence")
    location_id: Optional[UUID4] = Field(None, description="Location identifier associated with the occurrence")
    identification_id: Optional[UUID4] = Field(None, description="Identification identifier associated with the occurrence")


class OccurrenceCreate(OccurrenceBase):
    pass


class OccurrenceUpdate(OccurrenceBase):
    pass


class Occurrence(OccurrenceBase):
    id: UUID4 = Field(description="Unique identifier for the occurrence")
    created_at: datetime = Field(description="Timestamp of occurrence creation")
    updated_at: datetime = Field(description="Timestamp of occurrence update")

    class Config:
        orm_mode = True
