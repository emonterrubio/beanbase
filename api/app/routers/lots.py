from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.session import get_db
from app.models.auction_event import AuctionEvent
from app.models.farm import Farm
from app.models.lot import Lot
from app.schemas.lot import LotDetail, LotRow
from app.schemas.pagination import Page

router = APIRouter()


def _lot_to_row(lot: Lot) -> LotRow:
    d = LotRow.model_validate(lot)
    if lot.farm:
        d.farm_name = lot.farm.canonical_name
    if lot.auction_event:
        d.country = lot.auction_event.country
        d.year = lot.auction_event.year
    return d


def _lot_to_detail(lot: Lot) -> LotDetail:
    d = LotDetail.model_validate(lot)
    if lot.farm:
        d.farm_name = lot.farm.canonical_name
    if lot.auction_event:
        d.country = lot.auction_event.country
        d.year = lot.auction_event.year
    return d


@router.get("", response_model=Page[LotRow])
async def list_lots(
    origin: Optional[str] = Query(None, description="Filter by country"),
    year: Optional[int] = Query(None, description="Filter by auction year"),
    min_score: Optional[float] = Query(None, description="Minimum CoE score"),
    max_score: Optional[float] = Query(None, description="Maximum CoE score"),
    process: Optional[str] = Query(None, description="Filter by process method"),
    min_price: Optional[float] = Query(None, description="Min price USD/kg"),
    max_price: Optional[float] = Query(None, description="Max price USD/kg"),
    farm_id: Optional[int] = Query(None, description="Filter by farm ID"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Lot)
        .options(joinedload(Lot.farm), joinedload(Lot.auction_event))
        .join(AuctionEvent, Lot.auction_event_id == AuctionEvent.id)
    )

    if origin:
        stmt = stmt.where(AuctionEvent.country.ilike(origin))
    if year:
        stmt = stmt.where(AuctionEvent.year == year)
    if min_score is not None:
        stmt = stmt.where(Lot.score >= min_score)
    if max_score is not None:
        stmt = stmt.where(Lot.score <= max_score)
    if process:
        stmt = stmt.where(Lot.process_method.ilike(f"%{process}%"))
    if min_price is not None:
        stmt = stmt.where(Lot.winning_price_usd_per_kg >= min_price)
    if max_price is not None:
        stmt = stmt.where(Lot.winning_price_usd_per_kg <= max_price)
    if farm_id:
        stmt = stmt.where(Lot.farm_id == farm_id)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar_one()

    stmt = (
        stmt.order_by(Lot.score.desc().nulls_last())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    lots = (await db.execute(stmt)).unique().scalars().all()

    return Page(
        items=[_lot_to_row(lot) for lot in lots],
        total=total,
        page=page,
        page_size=page_size,
        pages=-(-total // page_size),
    )


@router.get("/{lot_id}", response_model=LotDetail)
async def get_lot(lot_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Lot)
        .options(joinedload(Lot.farm), joinedload(Lot.auction_event))
        .where(Lot.id == lot_id)
    )
    lot = result.unique().scalars().first()
    if not lot:
        raise HTTPException(status_code=404, detail=f"Lot {lot_id} not found")
    return _lot_to_detail(lot)
