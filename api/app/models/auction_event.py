from __future__ import annotations

import datetime
from typing import List, Optional

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class AuctionEvent(Base):
    __tablename__ = "auction_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    event_name: Mapped[Optional[str]] = mapped_column(String(200))
    event_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    origin_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("origins.id"))

    origin: Mapped[Optional["Origin"]] = relationship("Origin", back_populates="auction_events")
    lots: Mapped[List["Lot"]] = relationship("Lot", back_populates="auction_event")
