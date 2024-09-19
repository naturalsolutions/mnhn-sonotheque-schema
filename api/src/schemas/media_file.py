from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID


class MediaFiles(BaseModel):
    id: UUID = Field(..., description="Media file identifier")
    storage_url: str = Field(..., description="URL access point to the media")
    mime_type_format: str = Field(..., description="Mimetype format of the file")
    freq_low: float = Field(
        ...,
        description="The lowest frequency of the phenomena reflected in the multimedia item. Numeric value in hertz (Hz)",
    )
    freq_high: float = Field(
        ...,
        description="The highest frequency of the phenomena reflected in the multimedia item. Numeric value in hertz (Hz)",
    )
    sample_rate: float = Field(
        ...,
        description="Associates a digital signal to its sample rate. Numeric value in hertz (Hz)",
    )
    duration: int = Field(..., description="Duration of the media in seconds")
    size: int = Field(..., description="Size of the media in bytes")
    pixel_x_dimension: int = Field(..., description="Pixel X dimension")
    pixel_y_dimension: int = Field(..., description="Pixel Y dimension")
    creation_technique: str = Field(
        ...,
        description="Information about technical aspects of the creation and digitization process of the resource",
    )
    rights: str = Field(
        ..., description="Information about rights held in and over the resource"
    )
    attribution_url: str = Field(
        ...,
        description="The URL where information about ownership, attribution, etc. of the resource may be found",
    )
    usage_terms: str = Field(
        ...,
        description="A collection of text instructions on how a resource can be legally used",
    )
    cv_terms: List[str] = Field(
        ...,
        description="A term to describe the content of the image by a value from a Controlled Vocabulary",
    )
    dynamic_metadata: dict = Field(
        ...,
        description="Any information that could be gathered from original file (XMP, IPTC, WAV header)",
    )
    associated_media: Optional[UUID] = Field(None, description="Associated media UUID")
    owned_by: Optional[UUID] = Field(None, description="Owner's UUID")
    owner_litteral: str = Field(..., description="Legal owner of the resource")
    created_at: str = Field(..., description="Timestamp of resource creation")
    updated_at: str = Field(..., description="Timestamp of resource update")
