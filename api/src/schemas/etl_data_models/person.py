from patito import Model, Field, UUID4
from typing import Optional
from datetime import date


class Person(Model):
    id: UUID4 = Field(description="Unique identifier for the person")
    full_name: str = Field(description="Full name of the person")
    birth_date: Optional[date] = Field(None, description="Birth date of the person")
    death_date: Optional[date] = Field(None, description="Death date of the person")
    has_gender: Optional[str] = Field(None, description="Gender of the person")
    email: Optional[str] = Field(None, description="Email address of the person")
    identity_provider: Optional[str] = Field(None, description="Identity provider of the person")
    identity_token: Optional[str] = Field(None, description="Identity token of the person")

    class Config:
        orm_mode = True
