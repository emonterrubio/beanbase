"""
Onyx Coffee Lab DB loader.

Reads product rows produced by onyx scraper and upserts into importer_products.
Unique key: (source='onyx', variant_id, scraped_month).

Onyx products are retail SKUs (blends + single-origins + subscriptions) that
don't map cleanly to canonical farms, so they live in importer_products rather
than farms/lots.

Interface:
    load(rows: list[dict]) -> dict   # {"inserted": n, "updated": n, "skipped": n}
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from normalizers.process_method import normalize as norm_process

load_dotenv(Path(__file__).resolve().parents[3] / "api" / ".env")
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/beanbase")

log = logging.getLogger(__name__)


def _get_engine():
    return create_engine(DATABASE_URL, connect_args={"connect_timeout": 15})


def _price(raw) -> Optional[float]:
    try:
        return float(raw) if raw not in (None, "", "0.0", "0") else None
    except (ValueError, TypeError):
        return None


def _bool(raw) -> bool:
    return str(raw).lower() in ("true", "1", "yes")


def load(rows: list) -> dict:
    if not rows:
        return {"inserted": 0, "updated": 0, "skipped": 0}

    engine = _get_engine()
    counts = {"inserted": 0, "updated": 0, "skipped": 0}

    with engine.begin() as conn:
        for row in rows:
            variant_id = str(row.get("VariantID", "") or "").strip()
            scraped_month = str(row.get("ScrapedMonth", "") or "").strip()

            if not variant_id or not scraped_month:
                counts["skipped"] += 1
                continue

            params = {
                "source": "onyx",
                "variant_id": variant_id,
                "title": str(row.get("Title", "") or "").strip() or None,
                "product_type": str(row.get("ProductType", "") or "").strip() or None,
                "sku": str(row.get("SKU", "") or "").strip() or None,
                "price_usd": _price(row.get("Price")),
                "available": _bool(row.get("Available")),
                "origin": str(row.get("Origin", "") or "").strip() or None,
                "process": norm_process(str(row.get("Process", "") or "")) or None,
                "profile": str(row.get("Profile", "") or "").strip() or None,
                "scraped_month": scraped_month,
                "raw": json.dumps(dict(row)),
            }

            existing = conn.execute(
                text("""
                    SELECT id FROM importer_products
                    WHERE source = 'onyx'
                      AND variant_id = :variant_id
                      AND scraped_month = :scraped_month
                """),
                {"variant_id": variant_id, "scraped_month": scraped_month},
            ).fetchone()

            if existing:
                conn.execute(
                    text("""
                        UPDATE importer_products SET
                            title = :title, product_type = :product_type, sku = :sku,
                            price_usd = :price_usd, available = :available,
                            origin = :origin, process = :process, profile = :profile,
                            raw_data = :raw
                        WHERE id = :id
                    """),
                    {**params, "id": existing.id},
                )
                counts["updated"] += 1
            else:
                conn.execute(
                    text("""
                        INSERT INTO importer_products
                            (source, variant_id, title, product_type, sku, price_usd,
                             available, origin, process, profile, scraped_month, raw_data)
                        VALUES
                            (:source, :variant_id, :title, :product_type, :sku, :price_usd,
                             :available, :origin, :process, :profile, :scraped_month, :raw)
                    """),
                    params,
                )
                counts["inserted"] += 1

    log.info(
        "onyx loader: inserted=%d updated=%d skipped=%d",
        counts["inserted"], counts["updated"], counts["skipped"],
    )
    return counts
