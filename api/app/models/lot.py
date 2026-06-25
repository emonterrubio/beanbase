from __future__ import annotations

from typing import Dict, List, Optional

from sqlalchemy import ARRAY, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Lot(Base):
    __tablename__ = "lots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    auction_event_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("auction_events.id"), index=True)
    farm_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("farms.id"), index=True)
    lot_number: Mapped[Optional[int]] = mapped_column(Integer)
    lot_rank: Mapped[Optional[str]] = mapped_column(String(20), index=True)
    score: Mapped[Optional[float]] = mapped_column(Numeric(4, 2), index=True)
    process_method: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    varietal: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    weight_kg: Mapped[Optional[float]] = mapped_column(Numeric(8, 2))
    winning_price_usd_per_kg: Mapped[Optional[float]] = mapped_column(Numeric(8, 2))
    buyer_name: Mapped[Optional[str]] = mapped_column(String(300), index=True)
    flavor_tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    tasting_notes: Mapped[Optional[str]] = mapped_column(Text)
    raw_source_data: Mapped[Optional[Dict]] = mapped_column(JSONB)

    auction_event: Mapped[Optional["AuctionEvent"]] = relationship("AuctionEvent", back_populates="lots")
    farm: Mapped[Optional["Farm"]] = relationship("Farm", back_populates="lots")
