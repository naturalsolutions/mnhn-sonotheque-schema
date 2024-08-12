from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date, datetime


class IdentificationBase(BaseModel):
    verification_status: Optional[str] = None
    qualifier: Optional[str] = None
    identification_date: Optional[date] = None
    identified_by: Optional[UUID4] = None
    review_by: Optional[UUID4] = None
    taxon_id: Optional[UUID4] = None
    notes: Optional[str] = None


class IdentificationCreate(IdentificationBase):
    pass


class IdentificationUpdate(IdentificationBase):
    pass


class Identification(IdentificationBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
