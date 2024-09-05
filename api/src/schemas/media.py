from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
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


class MediaBase(BaseModel):
    parent_id: Optional[uuid.UUID] = None
    code: Optional[str] = None
    title: Optional[str] = None
    type: Optional[MediaTypeEnum] = MediaTypeEnum.Sound
    subtype: Optional[MediaSubTypeEnum] = MediaSubTypeEnum.ESPECE
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    comment: Optional[str] = None
    resource_creation_technique: Optional[str] = None
    available: Optional[list[str]] = (
        None  # Assuming a simple representation for the range of timestamps
    )
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    recorded_at: Optional[str] = None
    recording_range: Optional[list[str]] = (
        None  # Assuming a simple representation for the range of timestamps
    )
    temporal: Optional[str] = None
    time_of_day: Optional[str] = None
    rating: Optional[int] = None
    naturality_rating: Optional[int] = None
    musicality_rating: Optional[int] = None
    media_propagation: Optional[str] = None
    ecological_tags: Optional[list[str]] = None


class MediaCreate(MediaBase):
    pass


class Media(MediaBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    class Config:
        orm_mode = True
