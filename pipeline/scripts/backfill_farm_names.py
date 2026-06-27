#!/usr/bin/env python3
"""
Backfill parsed lot-title fields for existing farms.

- cafe_imports: re-parse source_lot_title + Region from sample JSON
- cup_of_excellence: re-read CoE JSON files for FarmName / ProducerName / Region

Usage:
  cd pipeline && python scripts/backfill_farm_names.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from normalizers import slugify
from normalizers.farm_name import parse_importer_lot_name

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "coe"
CAFE_SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples"

_LOT_TITLE_FIELDS = """
    canonical_name = :name,
    owner_name = :owner,
    municipality = :municipality,
    department = :department,
    lot_varietal = :lot_varietal,
    lot_process = :lot_process,
    packaging_type = :packaging_type,
    source_lot_title = COALESCE(:source_lot_title, source_lot_title)
"""


def _parsed_params(parsed, source_lot_title: str | None, region: str | None = None) -> dict:
    department = parsed.department or (region.strip() if region else None) or None
    return {
        "name": parsed.farm_name,
        "owner": parsed.owner_name,
        "municipality": parsed.municipality,
        "department": department,
        "lot_varietal": parsed.varietal,
        "lot_process": parsed.process_hint,
        "packaging_type": parsed.packaging_type,
        "source_lot_title": source_lot_title,
    }


def _load_cafe_imports_map() -> dict[str, dict]:
    """Map farm slug → parsed fields + Region from sample JSON files."""
    mapping: dict[str, dict] = {}
    for path in sorted(CAFE_SAMPLES.glob("cafe_imports_*.json")):
        with open(path, encoding="utf-8") as f:
            rows = json.load(f)
        for row in rows:
            origin = str(row.get("Origin", "") or "").strip()
            name = str(row.get("Name", "") or "").strip()
            if not origin or not name:
                continue
            slug = f"{slugify(origin)}--{slugify(name)}"
            region = str(row.get("Region", "") or "").strip()
            parsed = parse_importer_lot_name(name)
            mapping[slug] = _parsed_params(parsed, name, region)
    return mapping


def backfill_cafe_imports(conn, dry_run: bool) -> int:
    cafe_map = _load_cafe_imports_map()
    rows = conn.execute(
        text("""
            SELECT id, slug, canonical_name, source_lot_title
            FROM farms WHERE source = 'cafe_imports'
        """)
    ).fetchall()
    updated = 0
    for row in rows:
        if row.slug in cafe_map:
            params = cafe_map[row.slug]
        else:
            raw = row.source_lot_title or row.canonical_name
            parsed = parse_importer_lot_name(raw)
            if not parsed.farm_name:
                continue
            params = _parsed_params(parsed, raw)
        if dry_run:
            print(f"[cafe_imports] {row.id}: {row.slug!r}")
            print(f"  → dept={params['department']!r}, muni={params['municipality']!r}")
        else:
            conn.execute(
                text(f"UPDATE farms SET {_LOT_TITLE_FIELDS} WHERE id = :id"),
                {**params, "id": row.id},
            )
        updated += 1
    return updated


def _load_coe_farm_map() -> dict[str, dict]:
    """Map slug → farm fields from all CoE JSON files."""
    mapping: dict[str, dict] = {}
    if not DATA_DIR.exists():
        return mapping

    for path in sorted(DATA_DIR.glob("*.json")):
        parts = path.stem.split("-")
        year_idx = next(
            (i for i, p in enumerate(parts) if p.isdigit() and len(p) == 4),
            None,
        )
        country_slug = "-".join(parts[:year_idx]) if year_idx is not None else path.stem

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        lots = data if isinstance(data, list) else data.get("lots", data.get("Lots", []))
        for lot in lots:
            producer = str(lot.get("ProducerName", "") or "").strip()
            farm_name = str(lot.get("FarmName", "") or "").strip()
            region = str(lot.get("Region", "") or "").strip()
            if not producer and not farm_name:
                continue
            canonical = farm_name or producer
            owner = producer if farm_name else None
            slug_key = producer or farm_name
            slug = f"{country_slug}--{slugify(slug_key)}"
            mapping[slug] = {
                "name": canonical,
                "owner": owner,
                "municipality": None,
                "department": region or None,
                "lot_varietal": None,
                "lot_process": None,
                "packaging_type": None,
                "source_lot_title": None,
            }
    return mapping


def backfill_coe(conn, dry_run: bool) -> int:
    farm_map = _load_coe_farm_map()
    rows = conn.execute(
        text("SELECT id, slug FROM farms WHERE source = 'cup_of_excellence'")
    ).fetchall()
    updated = 0
    for row in rows:
        if row.slug not in farm_map:
            continue
        params = farm_map[row.slug]
        if dry_run and updated < 5:
            print(f"[coe] {row.slug}: dept={params['department']!r}")
        elif not dry_run:
            conn.execute(
                text(f"""
                    UPDATE farms SET
                        canonical_name = :name,
                        owner_name = :owner,
                        municipality = :municipality,
                        department = :department
                    WHERE id = :id
                """),
                {**params, "id": row.id},
            )
        updated += 1
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill farm lot-title fields")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without writing")
    args = parser.parse_args()

    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL is required", file=sys.stderr)
        sys.exit(1)

    engine = create_engine(db_url)
    with engine.begin() as conn:
        ci = backfill_cafe_imports(conn, args.dry_run)
        coe = backfill_coe(conn, args.dry_run)

    action = "Would update" if args.dry_run else "Updated"
    print(f"{action} {ci} cafe_imports farms, {coe} cup_of_excellence farms")


if __name__ == "__main__":
    main()
