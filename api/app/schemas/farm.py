from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class FarmSummary(BaseModel):
    id: int
    slug: str
    canonical_name: str
    owner_name: Optional[str] = None
    municipality: Optional[str] = None
    department: Optional[str] = None
    lot_varietal: Optional[str] = None
    lot_process: Optional[str] = None
    packaging_type: Optional[str] = None
    origin_id: Optional[int] = None
    country: Optional[str] = None       # joined from origin
    process_methods: Optional[List[str]] = None
    varietals: Optional[List[str]] = None
    source: Optional[str] = None

    model_config = {"from_attributes": True}


class FarmDetail(FarmSummary):
    altitude_m: Optional[int] = None
    cooperative_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    flavor_tags: Optional[List[str]] = None
    importer_ids: Optional[Dict[str, Any]] = None
    source_lot_title: Optional[str] = None


class FarmFacets(BaseModel):
    """Available filter values given the other active filters."""
    origins: List[str]
    sources: List[str]
    processes: List[str]
