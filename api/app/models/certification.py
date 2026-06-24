from __future__ import annotations

import datetime
from typing import Optional

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Certification(Base):
    __tablename__ = "certifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    farm_id: Mapped[int] = mapped_column(Integer, ForeignKey("farms.id"), nullable=False, index=True)
    body: Mapped[str] = mapped_column(String(100), nullable=False)
    cert_number: Mapped[Optional[str]] = mapped_column(String(200))
    valid_from: Mapped[Optional[datetime.date]] = mapped_column(Date)
    valid_until: Mapped[Optional[datetime.date]] = mapped_column(Date)

    farm: Mapped["Farm"] = relationship("Farm", back_populates="certifications")
