from patito import Model, Field
from typing import Optional
from datetime import date, datetime
from uuid import UUID


class IdentificationBase(Model):
    verification_status: Optional[str] = Field()
    qualifier: Optional[str] = Field()
    identification_date: Optional[date] = Field()
    identified_by: Optional[UUID] = Field()
    review_by: Optional[UUID] = Field()
    taxon_id: Optional[UUID] = Field()
    notes: Optional[str] = Field()


class IdentificationCreate(IdentificationBase):
    pass


class IdentificationUpdate(IdentificationBase):
    pass


class Identification(IdentificationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
