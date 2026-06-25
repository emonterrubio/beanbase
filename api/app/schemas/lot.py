from typing import List, Optional
from pydantic import BaseModel


class LotRow(BaseModel):
    id: int
    auction_event_id: Optional[int] = None
    farm_id: Optional[int] = None
    farm_name: Optional[str] = None         # joined from farm
    country: Optional[str] = None           # joined from auction_event
    year: Optional[int] = None              # joined from auction_event
    lot_rank: Optional[str] = None
    lot_number: Optional[int] = None
    score: Optional[float] = None
    process_method: Optional[str] = None
    varietal: Optional[List[str]] = None
    weight_kg: Optional[float] = None
    winning_price_usd_per_kg: Optional[float] = None
    buyer_name: Optional[str] = None

    model_config = {"from_attributes": True}


class LotDetail(LotRow):
    tasting_notes: Optional[str] = None
    flavor_tags: Optional[List[str]] = None
