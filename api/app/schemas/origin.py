from typing import List, Optional
from pydantic import BaseModel


class OriginCard(BaseModel):
    id: int
    country: str
    region: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude_min_m: Optional[int] = None
    altitude_max_m: Optional[int] = None
    harvest_start_month: Optional[int] = None
    harvest_end_month: Optional[int] = None
    dominant_varietals: Optional[List[str]] = None
    flavor_tags: Optional[List[str]] = None
    notes: Optional[str] = None

    model_config = {"from_attributes": True}
