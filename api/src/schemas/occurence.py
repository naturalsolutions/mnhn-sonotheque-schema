from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional


class OccurrenceBase(BaseModel):
    behavior: Optional[str] = None
    life_stage: Optional[str] = None
    sex: Optional[str] = None
    degree_of_establishment: Optional[str] = None
    media_id: Optional[UUID4] = None
    taxa_id: Optional[UUID4] = None
    location_id: Optional[UUID4] = None
    identification_id: Optional[UUID4] = None


class OccurrenceCreate(OccurrenceBase):
    pass


class OccurrenceUpdate(OccurrenceBase):
    pass


class Occurrence(OccurrenceBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
