from pydantic import BaseModel, Field, UUID4
from typing import List
from datetime import datetime


class SamplingEventsSchema(BaseModel):
    id: UUID4 = Field(
        ...,
        description="An identifier for the set of information associated with a dwc:Event (something that occurs at a place and time). May be a global unique identifier or an identifier specific to the data set.",
    )
    parent_id: UUID4 = Field(
        ...,
        description="An identifier for the broader dwc:Event that groups this and potentially other dwc:Events.",
    )
    basis_of_record: List[str] = Field(
        ...,
        description="Type of record collected in the sampling event: whether Human Observation or Machine Observation",
    )
    type: str = Field(
        ...,
        description="The nature of the dwc:Event. Recommended best practice is to use a controlled vocabulary.",
    )
    sampling_protocol: str = Field(
        ...,
        description="The names of, references to, or descriptions of the methods or protocols used during a dwc:Event.",
    )
    started_at: datetime = Field(
        ..., description="The date-time or interval during which a dwc:Event occurred"
    )
    ended_at: datetime = Field(
        ..., description="The date-time or interval during which a dwc:Event occurred"
    )
    date_range: List[datetime] = Field(
        ..., description="The date-time or interval during which a dwc:Event occurred"
    )
    habitat: str = Field(
        ...,
        description="A category or description of the habitat in which the dwc:Event occurred.",
    )
    notes: str = Field(..., description="Comments or notes about the dwc:Event.")
    measurements_or_facts: dict = Field(
        ...,
        description="A list (concatenated and separated) of additional measurements or characteristics of the Event.",
    )
    created_at: datetime = Field(
        ..., description="Timestamp of resource creation in database"
    )
    updated_at: datetime = Field(
        ..., description="Timestamp of resource update in database"
    )
