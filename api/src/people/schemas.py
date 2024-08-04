from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date


class Person(BaseModel):
    id: UUID4
    full_name: str
    birth_date: Optional[date] = None
    death_date: Optional[date] = None
    has_gender: Optional[str] = None
    email: Optional[str] = None
    identity_provider: Optional[str] = None
    identity_token: Optional[str] = None

    class Config:
        from_attributes = True
