from datetime import datetime
from typing import Optional
from patito import Model, Field
import polars as pl
from enum import Enum
from typing import Literal
import uuid


class MediaTypeEnum(str, Enum):
    Sound = "Sound"
    StillImage = "StillImage"
    MovingImage = "MovingImage"
    UNDEFINED = "UNDEFINED"


class MediaSubTypeEnum(str, Enum):
    ESPECE = "ESPECE"
    PAYSAGE_SONORE = "PAYSAGE_SONORE"
    UNDEFINED = "UNDEFINED"


class MediaBase(Model):
    id: str = Field(default=None, description="Media identifier")
    parent_id: Optional[str] = Field(
        default=None, description="Parent media identifier"
    )
    code: Optional[str] = Field(
        default=None, description="A free-form identifier for the resource"
    )
    title: Optional[str] = Field(
        default=None,
        description="Concise title, name, or brief descriptive label of the resource",
    )
    type: Optional[Literal["Sound", "StillImage", "MovingImage", "UNDEFINED"]] = Field(
        default="Sound",
        description="Type of media: Sound, StillImage, MovingImage, UNDEFINED",
    )
    subtype: Optional[Literal["ESPECE", "PAYSAGE_SONORE", "UNDEFINED"]] = Field(
        default="ESPECE",
        description="Subtype of media, e.g., ESPECE, PAYSAGE_SONORE, UNDEFINED",
    )
    description: Optional[str] = Field(
        default=None, description="An account of the resource"
    )
    tags: Optional[list[str]] = Field(
        default=None, description="Media tags, which may be multi-worded phrases"
    )
    comment: Optional[str] = Field(
        default=None, description="Any comment provided on the media resource"
    )
    resource_creation_technique: Optional[str] = Field(
        default=None,
        description="Information about technical aspects of the creation and digitization process of the resource",
    )
    available: Optional[list[str]] = Field(
        default=None,
        description="Date (often a range) that the resource became or will become available",
    )

    recorded_at: Optional[str] = Field(
        default=None, description="Timestamp of resource recording"
    )
    recording_range: Optional[list[str]] = Field(
        default=None, description="Recording timestamp exact temporal coverage"
    )
    temporal: Optional[str] = Field(
        default=None, description="Temporal coverage of the resource"
    )
    time_of_day: Optional[str] = Field(
        default=None, description="Time of day when the resource was recorded"
    )
    rating: Optional[int] = Field(default=None, description="Rating of the media")
    naturality_rating: Optional[int] = Field(
        default=None, description="Naturality rating of the media"
    )
    musicality_rating: Optional[int] = Field(
        default=None, description="Musicality rating of the media"
    )
    media_propagation: Optional[str] = Field(
        default=None, description="Media propagation information"
    )
    ecological_tags: Optional[list[str]] = Field(
        default=None, description="Ecological tags associated with the media"
    )

    created_at: Optional[datetime] = Field(
        default=None, description="Timestamp of resource creation in database"
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="Timestamp of resource update in database"
    )


class MediaCreate(MediaBase):
    pass


class Media(MediaBase):
    class Config:
        orm_mode = True
