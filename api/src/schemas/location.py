from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping


class LocationBase(BaseModel):
    parent_id: Optional[UUID]
    higher_geography_path: Optional[str]
    geom: Optional[str] = Field(
        None,
        description="Spatial geometry representing a given location as Well-Known Text (WKT) format",
    )
    geometry_precision: Optional[float]
    identifier: Optional[str]
    country: Optional[str]
    state_province: Optional[str]
    municipality: Optional[str]
    locality: Optional[str]
    depth_min: Optional[float]
    elevation_max: Optional[float]
    sampling_remarks: Optional[dict]
    remarks: Optional[str]
    provided_id: Optional[str]
    provider_source: Optional[str]

    class Config:
        from_attributes = True


class LocationCreate(LocationBase):
    pass


class LocationUpdate(LocationBase):
    pass


class Location(LocationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_orm(obj):
        data = obj
        if obj.geom:
            data["geom"] = mapping(to_shape(obj.geom))
        return data
