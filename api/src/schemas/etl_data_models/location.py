from datetime import datetime
from patito import Model, Field
from typing import Optional
from uuid import UUID
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping


class LocationBase(Model):
    parent_id: Optional[UUID] = Field(
        None, description="Identifier for the parent location"
    )
    higher_geography_path: Optional[str] = Field(
        None, description="Path representing the higher geography"
    )
    geom: Optional[str] = Field(
        None,
        description="Spatial geometry representing a given location as Well-Known Text (WKT) format",
    )
    geometry_precision: Optional[float] = Field(
        None, description="Precision of the geometry"
    )
    identifier: Optional[str] = Field(None, description="Identifier for the location")
    country: Optional[str] = Field(None, description="Country of the location")
    state_province: Optional[str] = Field(
        None, description="State or province of the location"
    )
    municipality: Optional[str] = Field(
        None, description="Municipality of the location"
    )
    locality: Optional[str] = Field(None, description="Locality of the location")
    depth_min: Optional[float] = Field(
        None, description="Minimum depth of the location"
    )
    elevation_max: Optional[float] = Field(
        None, description="Maximum elevation of the location"
    )
    sampling_remarks: Optional[dict] = Field(
        None, description="Remarks about the sampling"
    )
    remarks: Optional[str] = Field(
        None, description="Additional remarks about the location"
    )
    provided_id: Optional[str] = Field(
        None, description="Provided identifier for the location"
    )
    provider_source: Optional[str] = Field(None, description="Source of the provider")

    class Config:
        from_attributes = True


class LocationCreate(LocationBase):
    pass


class LocationUpdate(LocationBase):
    pass


class Location(LocationBase):
    id: UUID = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    @staticmethod
    def from_orm(obj):
        data = obj
        if obj.geom:
            data["geom"] = mapping(to_shape(obj.geom))
        return data
