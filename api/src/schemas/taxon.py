from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class TaxonBase(BaseModel):
    legacy_id: Optional[int] = Field(
        None, description="Legacy Taxon identifier from previous database"
    )
    original_scientific_name: Optional[str] = Field(
        None,
        description="Taxon scientific name as recorded in the previous Sonotheque database",
    )
    gbif_key: Optional[int] = Field(None, description="GBIF taxon identifier")
    gbif_name_key: Optional[int] = Field(None, description="GBIF taxon name identifier")
    gbif_parent_key: Optional[int] = Field(
        None, description="GBIF parent taxon identifier"
    )
    gbif_dataset_key: Optional[int] = Field(None, description="GBIF dataset identifier")
    vernacular_name: Optional[str] = Field(None, description="Taxon vernacular name")
    kingdom: Optional[str] = Field(None, description="Taxon kingdom")
    phylum: Optional[str] = Field(None, description="Taxon phylum")
    class_: Optional[str] = Field(None, description="Taxon class")
    order: Optional[str] = Field(None, description="Taxon order")
    family: Optional[str] = Field(None, description="Taxon family")
    genus: Optional[str] = Field(None, description="Taxon genus")
    species: Optional[str] = Field(None, description="Taxon species epithet")
    scientific_name: Optional[str] = Field(None, description="Taxon scientific name")
    canonical_name: Optional[str] = Field(None, description="Taxon canonical name")
    original_vernacular_names: Optional[dict] = Field(
        None,
        description="Taxon vernacular names with language as recorded in the previous Sonotheque database",
    )
    vernacular_name_english: Optional[str] = None
    vernacular_name_french: Optional[str] = None
    rank: Optional[str] = None
    status: Optional[str] = None
    synonym: Optional[bool] = None


class TaxonCreate(TaxonBase):
    pass


class TaxonUpdate(TaxonBase):
    pass


class TaxonInDB(TaxonBase):
    id: UUID = Field(..., description="Taxon internal identifier")
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Taxon(TaxonInDB):
    pass
