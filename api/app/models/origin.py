from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ARRAY, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Origin(Base):
    __tablename__ = "origins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    region: Mapped[Optional[str]] = mapped_column(String(200))
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)
    altitude_min_m: Mapped[Optional[int]] = mapped_column(Integer)
    altitude_max_m: Mapped[Optional[int]] = mapped_column(Integer)
    harvest_start_month: Mapped[Optional[int]] = mapped_column(Integer)
    harvest_end_month: Mapped[Optional[int]] = mapped_column(Integer)
    dominant_varietals: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    flavor_tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    notes: Mapped[Optional[str]] = mapped_column(Text)

    farms: Mapped[List["Farm"]] = relationship("Farm", back_populates="origin")
    auction_events: Mapped[List["AuctionEvent"]] = relationship("AuctionEvent", back_populates="origin")
