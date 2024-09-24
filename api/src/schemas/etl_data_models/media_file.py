from patito import Model, Field
from typing import List, Optional
from uuid import UUID


class MediaFiles(Model):
    id: Optional[UUID] = Field(None, description="Media file identifier")
    storage_url: Optional[str] = Field(
        None, description="URL access point to the media"
    )
    mime_type_format: Optional[str] = Field(
        None, description="Mimetype format of the file"
    )
    freq_low: Optional[float] = Field(
        None,
        description="The lowest frequency of the phenomena reflected in the multimedia item. Numeric value in hertz (Hz)",
    )
    freq_high: Optional[float] = Field(
        None,
        description="The highest frequency of the phenomena reflected in the multimedia item. Numeric value in hertz (Hz)",
    )
    sample_rate: Optional[float] = Field(
        None,
        description="Associates a digital signal to its sample rate. Numeric value in hertz (Hz)",
    )
    duration: Optional[int] = Field(
        None, description="Duration of the media in seconds"
    )
    size: Optional[int] = Field(None, description="Size of the media in bytes")
    pixel_x_dimension: Optional[int] = Field(None, description="Pixel X dimension")
    pixel_y_dimension: Optional[int] = Field(None, description="Pixel Y dimension")
    creation_technique: Optional[str] = Field(
        None,
        description="Information about technical aspects of the creation and digitization process of the resource",
    )
    rights: Optional[str] = Field(
        None, description="Information about rights held in and over the resource"
    )
    attribution_url: Optional[str] = Field(
        None,
        description="The URL where information about ownership, attribution, etc. of the resource may be found",
    )
    usage_terms: Optional[str] = Field(
        None,
        description="A collection of text instructions on how a resource can be legally used",
    )
    cv_terms: Optional[List[str]] = Field(
        None,
        description="A term to describe the content of the image by a value from a Controlled Vocabulary",
    )
    dynamic_metadata: Optional[dict] = Field(
        None,
        description="Any information that could be gathered from original file (XMP, IPTC, WAV header)",
    )
    associated_media: Optional[UUID] = Field(None, description="Associated media UUID")
    owned_by: Optional[UUID] = Field(None, description="Owner's UUID")
    owner_litteral: Optional[str] = Field(
        None, description="Legal owner of the resource"
    )
    created_at: Optional[str] = Field(
        None, description="Timestamp of resource creation"
    )
    updated_at: Optional[str] = Field(None, description="Timestamp of resource update")
