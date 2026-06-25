from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.origin import Origin
from app.schemas.origin import OriginCard

router = APIRouter()


@router.get("", response_model=List[OriginCard])
async def list_origins(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Origin).order_by(Origin.country))
    return result.scalars().all()


@router.get("/{country}", response_model=OriginCard)
async def get_origin(country: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Origin)
        .where(Origin.country.ilike(country))
        .where(Origin.region.is_(None))
    )
    origin = result.scalars().first()
    if not origin:
        raise HTTPException(status_code=404, detail=f"Origin '{country}' not found")
    return origin
