from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.session import get_db
from app.models.farm import Farm
from app.models.origin import Origin
from app.schemas.farm import FarmDetail, FarmSummary
from app.schemas.pagination import Page

router = APIRouter()


def _farm_to_summary(farm: Farm) -> FarmSummary:
    d = FarmSummary.model_validate(farm)
    if farm.origin:
        d.country = farm.origin.country
    return d


def _farm_to_detail(farm: Farm) -> FarmDetail:
    d = FarmDetail.model_validate(farm)
    if farm.origin:
        d.country = farm.origin.country
    return d


@router.get("", response_model=Page[FarmSummary])
async def list_farms(
    q: Optional[str] = Query(None, description="Search by name"),
    origin: Optional[str] = Query(None, description="Filter by country"),
    process: Optional[str] = Query(None, description="Filter by process method"),
    source: Optional[str] = Query(None, description="Filter by data source"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Farm).options(joinedload(Farm.origin))

    if q:
        stmt = stmt.where(Farm.canonical_name.ilike(f"%{q}%"))
    if origin:
        stmt = stmt.join(Origin).where(Origin.country.ilike(origin))
    if process:
        stmt = stmt.where(Farm.process_methods.any(process))
    if source:
        stmt = stmt.where(Farm.source == source)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar_one()

    stmt = stmt.order_by(Farm.canonical_name).offset((page - 1) * page_size).limit(page_size)
    farms = (await db.execute(stmt)).unique().scalars().all()

    return Page(
        items=[_farm_to_summary(f) for f in farms],
        total=total,
        page=page,
        page_size=page_size,
        pages=-(-total // page_size),
    )


@router.get("/{slug}", response_model=FarmDetail)
async def get_farm(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Farm).options(joinedload(Farm.origin)).where(Farm.slug == slug)
    )
    farm = result.unique().scalars().first()
    if not farm:
        raise HTTPException(status_code=404, detail=f"Farm '{slug}' not found")
    return _farm_to_detail(farm)
