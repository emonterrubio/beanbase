"""
CoE DB loader.

Reads lot rows produced by coe_scraper.run() and upserts into:
  origins (lookup only — pre-seeded)
  farms   (upsert by slug = "{country_slug}--{producer_slug}")
  auction_events (get-or-create by source + country + year)
  lots    (upsert by auction_event_id + lot_rank)

Interface:
    load(rows: list[dict]) -> dict   # {"inserted": n, "updated": n, "skipped": n}
"""

import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from normalizers import slugify
from normalizers.process_method import normalize as norm_process

load_dotenv(Path(__file__).resolve().parents[3] / "api" / ".env")
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/beanbase")

log = logging.getLogger(__name__)

LB_TO_KG = 0.453592


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_engine():
    return create_engine(DATABASE_URL)


def _origin_id_cache(conn) -> Dict[str, int]:
    """Return {country_lower: origin_id} for top-level (no region) origins."""
    rows = conn.execute(
        text("SELECT id, country FROM origins WHERE region IS NULL")
    ).fetchall()
    return {row.country.lower(): row.id for row in rows}


def _lot_number(rank_str: str) -> Optional[int]:
    """Extract leading integer from rank string: '1A' → 1, 'NW' → None."""
    m = re.match(r"^(\d+)", str(rank_str or ""))
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------------------
# Upsert helpers
# ---------------------------------------------------------------------------

def _upsert_farm(conn, canonical_name: str, origin_id: Optional[int],
                 country_slug: str, process: str, varietal: str, source: str) -> Optional[int]:
    if not canonical_name:
        return None

    farm_slug = f"{country_slug}--{slugify(canonical_name)}"
    process_arr = [norm_process(process)] if process else []
    varietal_arr = [varietal] if varietal else []

    existing = conn.execute(
        text("SELECT id, process_methods, varietals FROM farms WHERE slug = :slug"),
        {"slug": farm_slug},
    ).fetchone()

    if existing:
        # Merge process_methods and varietals without duplicates
        existing_processes = existing.process_methods or []
        existing_varietals = existing.varietals or []
        merged_processes = list(dict.fromkeys(existing_processes + process_arr))
        merged_varietals = list(dict.fromkeys(existing_varietals + varietal_arr))

        conn.execute(
            text("""
                UPDATE farms
                SET process_methods = :pm, varietals = :var
                WHERE id = :id
            """),
            {"pm": merged_processes, "var": merged_varietals, "id": existing.id},
        )
        return existing.id

    result = conn.execute(
        text("""
            INSERT INTO farms (slug, canonical_name, origin_id, process_methods, varietals, source)
            VALUES (:slug, :name, :origin_id, :pm, :var, :source)
            RETURNING id
        """),
        {
            "slug": farm_slug,
            "name": canonical_name,
            "origin_id": origin_id,
            "pm": process_arr,
            "var": varietal_arr,
            "source": source,
        },
    )
    return result.fetchone().id


def _get_or_create_auction_event(conn, country: str, year: int,
                                  auction_slug: str, origin_id: Optional[int]) -> int:
    row = conn.execute(
        text("""
            SELECT id FROM auction_events
            WHERE source = 'cup_of_excellence' AND country = :country AND year = :year
        """),
        {"country": country, "year": year},
    ).fetchone()

    if row:
        return row.id

    # Derive a human-readable event name from the auction slug
    # e.g. "ethiopia-2024" → "Cup of Excellence Ethiopia 2024"
    # "brazil-pulped-naturals-2018" → "Cup of Excellence Brazil Pulped Naturals 2018"
    slug_body = auction_slug.rsplit("-", 1)[0]  # strip trailing year
    pretty = slug_body.replace("-", " ").title()
    event_name = f"Cup of Excellence {pretty} {year}"

    result = conn.execute(
        text("""
            INSERT INTO auction_events (source, country, year, event_name, origin_id)
            VALUES ('cup_of_excellence', :country, :year, :event_name, :origin_id)
            RETURNING id
        """),
        {"country": country, "year": year, "event_name": event_name, "origin_id": origin_id},
    )
    return result.fetchone().id


def _upsert_lot(conn, event_id: int, farm_id: Optional[int], row: dict) -> str:
    """Insert or update a lot. Returns 'inserted' | 'updated' | 'skipped'."""
    lot_rank = str(row.get("LotRank", "") or "").strip()
    if not lot_rank:
        return "skipped"

    price_per_lb = row.get("PriceUSDPerLb")
    price_per_kg = round(float(price_per_lb) * (1 / LB_TO_KG), 2) if price_per_lb else None
    varietal_raw = str(row.get("Varietal", "") or "").strip()
    varietal_arr = [varietal_raw] if varietal_raw else None

    params = {
        "event_id": event_id,
        "farm_id": farm_id,
        "lot_rank": lot_rank,
        "lot_number": _lot_number(lot_rank),
        "score": row.get("ScoreCoE") or None,
        "process": norm_process(str(row.get("Process", "") or "")),
        "varietal": varietal_arr,
        "weight_kg": row.get("WeightKg") or None,
        "price_kg": price_per_kg,
        "buyer": ((str(row.get("BuyerName", "") or "")).strip() or None)[:300] if row.get("BuyerName") else None,
        "lot_type": str(row.get("LotType", "") or ""),
        "raw": json.dumps(dict(row), default=str),
    }

    existing = conn.execute(
        text("""
            SELECT id FROM lots
            WHERE auction_event_id = :event_id AND lot_rank = :lot_rank
        """),
        {"event_id": event_id, "lot_rank": lot_rank},
    ).fetchone()

    if existing:
        conn.execute(
            text("""
                UPDATE lots SET
                    farm_id = :farm_id,
                    lot_number = :lot_number,
                    score = :score,
                    process_method = :process,
                    varietal = :varietal,
                    weight_kg = :weight_kg,
                    winning_price_usd_per_kg = :price_kg,
                    buyer_name = :buyer,
                    raw_source_data = :raw
                WHERE id = :id
            """),
            {**params, "id": existing.id},
        )
        return "updated"

    conn.execute(
        text("""
            INSERT INTO lots (
                auction_event_id, farm_id, lot_rank, lot_number,
                score, process_method, varietal, weight_kg,
                winning_price_usd_per_kg, buyer_name, raw_source_data
            ) VALUES (
                :event_id, :farm_id, :lot_rank, :lot_number,
                :score, :process, :varietal, :weight_kg,
                :price_kg, :buyer, :raw
            )
        """),
        params,
    )
    return "inserted"


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def load(rows: list) -> dict:
    if not rows:
        return {"inserted": 0, "updated": 0, "skipped": 0}

    engine = _get_engine()
    counts = {"inserted": 0, "updated": 0, "skipped": 0}

    with engine.begin() as conn:
        origin_cache = _origin_id_cache(conn)

        for row in rows:
            country = str(row.get("Country", "") or "").strip()
            if not country:
                counts["skipped"] += 1
                continue

            origin_id = origin_cache.get(country.lower())
            country_slug = slugify(country)
            year = int(row.get("AuctionYear", 0) or 0)
            auction_slug = str(row.get("AuctionSlug", "") or "")

            if not year or not auction_slug:
                counts["skipped"] += 1
                continue

            # Farm: prefer ProducerName, fall back to FarmName
            producer = str(row.get("ProducerName", "") or "").strip()
            farm_name = str(row.get("FarmName", "") or "").strip()
            canonical_name = producer or farm_name

            farm_id = _upsert_farm(
                conn, canonical_name, origin_id, country_slug,
                str(row.get("Process", "") or ""),
                str(row.get("Varietal", "") or ""),
                "cup_of_excellence",
            )

            event_id = _get_or_create_auction_event(
                conn, country, year, auction_slug, origin_id
            )

            result = _upsert_lot(conn, event_id, farm_id, row)
            counts[result] += 1

    log.info(
        "coe loader: inserted=%d updated=%d skipped=%d",
        counts["inserted"], counts["updated"], counts["skipped"],
    )
    return counts
