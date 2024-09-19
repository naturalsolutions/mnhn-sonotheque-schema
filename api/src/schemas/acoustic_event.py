from datetime import datetime
from pydantic import BaseModel, Field, UUID4
from uuid import UUID as PyUUID
from typing import Optional


class AcousticEventBase(BaseModel):
    id: UUID4
    type: str = Field(
        ...,
        description="Coverage of the acoustic event; constrains to 'set' if event occurs during the entire duration of the media duration or 'subset' if the event occurs in a given region (temporal, spatial or inside frequency bounds)",
    )
    region_of_interest: dict = Field(
        ...,
        description="A designated region of a media item bounded in dimensions appropriate for the media type. Dimensions may include spatial, temporal, or frequency bounds.",
    )
    time_end: Optional[float] = Field(
        None,
        description="The end of a temporal region, specified as an absolute offset relative to the beginning of the media item, in seconds.",
    )
    time_start: Optional[float] = Field(
        None,
        description="The beginning of a temporal region, specified as an absolute offset relative to the beginning of the media item, in seconds.",
    )
    x_frac: Optional[float] = Field(
        None,
        description="The horizontal position of a reference point, measured from the left side of the media item and expressed as a decimal fraction of the width of the media item.",
    )
    y_frac: Optional[float] = Field(
        None,
        description="The vertical position of a reference point, measured from the top of the media item and expressed as a decimal fraction of the height of the media item.",
    )
    width_frac: Optional[float] = Field(
        None,
        description="The width of the bounding rectangle, expressed as a decimal fraction of the width of the media item.",
    )
    is_roi_of: Optional[UUID4] = None
    identification_id: Optional[UUID4] = None
    occurrence_id: Optional[PyUUID] = None


class AcousticEventCreate(AcousticEventBase):
    pass


class AcousticEventUpdate(AcousticEventBase):
    pass


class AcousticEvent(AcousticEventBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
