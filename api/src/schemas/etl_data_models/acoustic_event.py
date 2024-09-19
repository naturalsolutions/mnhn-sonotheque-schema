from datetime import datetime
from patito import Model, Field
from uuid import UUID
from typing import Optional


class AcousticEventBase(Model):
    id: UUID = Field()
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
    is_roi_of: Optional[UUID] = Field(None)
    identification_id: Optional[UUID] = Field(None)
    occurrence_id: Optional[UUID] = Field(None)


class AcousticEventCreate(AcousticEventBase):
    pass


class AcousticEventUpdate(AcousticEventBase):
    pass


class AcousticEvent(AcousticEventBase):
    id: UUID = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    class Config:
        orm_mode = True
