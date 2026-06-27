from __future__ import annotations

from typing import Dict, List, Optional

from sqlalchemy import ARRAY, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Farm(Base):
    __tablename__ = "farms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(300), unique=True, nullable=False, index=True)
    canonical_name: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    origin_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("origins.id"), index=True)
    altitude_m: Mapped[Optional[int]] = mapped_column(Integer)
    varietals: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    process_methods: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    owner_name: Mapped[Optional[str]] = mapped_column(String(300))
    municipality: Mapped[Optional[str]] = mapped_column(String(200))
    department: Mapped[Optional[str]] = mapped_column(String(200))
    lot_varietal: Mapped[Optional[str]] = mapped_column(String(200))
    lot_process: Mapped[Optional[str]] = mapped_column(String(200))
    packaging_type: Mapped[Optional[str]] = mapped_column(String(100))
    source_lot_title: Mapped[Optional[str]] = mapped_column(String(500))
    cooperative_name: Mapped[Optional[str]] = mapped_column(String(300))
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)
    flavor_tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    importer_ids: Mapped[Optional[Dict]] = mapped_column(JSONB)
    source: Mapped[Optional[str]] = mapped_column(String(50))

    origin: Mapped[Optional["Origin"]] = relationship("Origin", back_populates="farms")
    lots: Mapped[List["Lot"]] = relationship("Lot", back_populates="farm")
    certifications: Mapped[List["Certification"]] = relationship("Certification", back_populates="farm")
