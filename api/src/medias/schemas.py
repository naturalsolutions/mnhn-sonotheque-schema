from pydantic import BaseModel, Field
import uuid


class MediaModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    parent_id: uuid.UUID
    code: str
    title: str
    type: str
    subtype: str
    description: str
    tags: list[str]
    comment: str
    resource_creation_technique: str
    available: list[str]  # Assuming a simple representation for the range of timestamps
    created_at: str
    updated_at: str
    recorded_at: str
    recording_range: list[
        str
    ]  # Assuming a simple representation for the range of timestamps
    temporal: str
    time_of_day: str
    rating: int
    naturality_rating: int
    musicality_rating: int
    media_propagation: str
    ecological_tags: list[str]
