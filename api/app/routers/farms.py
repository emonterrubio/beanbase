from typing import FrozenSet, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.session import get_db
from app.models.farm import Farm
from app.models.origin import Origin
from app.schemas.farm import FarmDetail, FarmFacets, FarmSummary
from app.schemas.pagination import Page

router = APIRouter()


def _country_from_slug(slug: str) -> Optional[str]:
    """Derive country from slug prefix when origin_id is missing (e.g. nicaragua--farm-name)."""
    prefix = slug.split("--", 1)[0]
    if not prefix:
        return None
    return " ".join(word.capitalize() for word in prefix.split("-"))


def _resolve_country(farm: Farm) -> Optional[str]:
    if farm.origin:
        return farm.origin.country
    return _country_from_slug(farm.slug)


def _farm_to_summary(farm: Farm) -> FarmSummary:
    d = FarmSummary.model_validate(farm)
    d.country = _resolve_country(farm)
    return d


def _farm_to_detail(farm: Farm) -> FarmDetail:
    d = FarmDetail.model_validate(farm)
    d.country = _resolve_country(farm)
    return d


def _apply_farm_filters(
    stmt,
    *,
    q: Optional[str] = None,
    origin: Optional[str] = None,
    source: Optional[str] = None,
    process: Optional[str] = None,
    exclude: FrozenSet[str] = frozenset(),
):
    """Apply list filters; use exclude to omit one dimension when computing facets."""
    if q and "q" not in exclude:
        stmt = stmt.where(Farm.canonical_name.ilike(f"%{q}%"))
    if origin and "origin" not in exclude:
        slug_prefix = origin.lower().replace(" ", "-")
        stmt = stmt.outerjoin(Origin).where(
            or_(
                Origin.country.ilike(origin),
                Farm.slug.like(f"{slug_prefix}--%"),
            )
        )
    if process and "process" not in exclude:
        stmt = stmt.where(Farm.process_methods.any(process))
    if source and "source" not in exclude:
        stmt = stmt.where(Farm.source == source)
    return stmt


@router.get("/facets", response_model=FarmFacets)
async def farm_facets(
    q: Optional[str] = Query(None, description="Search by name"),
    origin: Optional[str] = Query(None, description="Filter by country"),
    process: Optional[str] = Query(None, description="Filter by process method"),
    source: Optional[str] = Query(None, description="Filter by data source"),
    db: AsyncSession = Depends(get_db),
):
    # Origins available given source, process, and search (exclude origin filter)
    origin_stmt = _apply_farm_filters(
        select(Farm).options(joinedload(Farm.origin)),
        q=q,
        source=source,
        process=process,
        exclude=frozenset({"origin"}),
    )
    origin_rows = (await db.execute(origin_stmt)).unique().scalars().all()
    origins = sorted({c for f in origin_rows if (c := _resolve_country(f))})

    # Sources available given origin, process, and search
    source_stmt = _apply_farm_filters(
        select(Farm.source),
        q=q,
        origin=origin,
        process=process,
        exclude=frozenset({"source"}),
    ).where(Farm.source.isnot(None)).distinct()
    source_rows = (await db.execute(source_stmt)).scalars().all()
    sources = sorted({s for s in source_rows if s})

    # Process methods available given origin, source, and search
    process_stmt = _apply_farm_filters(
        select(func.unnest(Farm.process_methods).label("method")),
        q=q,
        origin=origin,
        source=source,
        exclude=frozenset({"process"}),
    ).where(Farm.process_methods.isnot(None)).distinct()
    process_rows = (await db.execute(process_stmt)).scalars().all()
    processes = sorted({p for p in process_rows if p})

    return FarmFacets(origins=origins, sources=sources, processes=processes)


@router.get("", response_model=Page[FarmSummary])
async def list_farms(
    q: Optional[str] = Query(None, description="Search by name"),
    origin: Optional[str] = Query(None, description="Filter by country"),
    process: Optional[str] = Query(None, description="Filter by process method"),
    source: Optional[str] = Query(None, description="Filter by data source"),
    sort: Literal["asc", "desc"] = Query("asc", description="Sort by farm name"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    stmt = _apply_farm_filters(
        select(Farm).options(joinedload(Farm.origin)),
        q=q,
        origin=origin,
        source=source,
        process=process,
    )

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar_one()

    order = Farm.canonical_name.asc() if sort == "asc" else Farm.canonical_name.desc()
    stmt = stmt.order_by(order).offset((page - 1) * page_size).limit(page_size)
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
