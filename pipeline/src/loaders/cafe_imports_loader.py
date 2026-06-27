"""
Cafe Imports DB loader.

Reads lot rows produced by cafe_imports scraper and upserts into:
  farms (one record per unique producer Name + Origin, keyed by slug)

importer_ids JSONB is updated to include {"cafe_imports": <OfferingID>} for
the most recent offering seen for that producer. Multiple offerings from the
same producer accumulate on a single farm record.

Interface:
    load(rows: list[dict]) -> dict   # {"inserted": n, "updated": n, "skipped": n}
"""

import json
import logging
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from normalizers import slugify
from normalizers.farm_name import parse_importer_lot_name
from normalizers.process_method import normalize as norm_process

load_dotenv(Path(__file__).resolve().parents[3] / "api" / ".env")
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/beanbase")

log = logging.getLogger(__name__)


def _get_engine():
    return create_engine(DATABASE_URL, connect_args={"connect_timeout": 15})


def _origin_id_cache(conn) -> Dict[str, int]:
    rows = conn.execute(
        text("SELECT id, country FROM origins WHERE region IS NULL")
    ).fetchall()
    return {row.country.lower(): row.id for row in rows}


def _group_by_producer(rows: list) -> Dict[str, dict]:
    """
    Collapse multiple offerings from the same producer into one record.
    Key: (origin, name) slug. Merges process_methods and offering IDs.
    """
    groups: Dict[str, dict] = {}

    for row in rows:
        origin = str(row.get("Origin", "") or "").strip()
        name = str(row.get("Name", "") or "").strip()
        if not origin or not name:
            continue

        key = f"{slugify(origin)}--{slugify(name)}"
        parsed = parse_importer_lot_name(name)

        if key not in groups:
            groups[key] = {
                "slug": key,
                "source_lot_title": name,
                "canonical_name": parsed.farm_name,
                "owner_name": parsed.owner_name,
                "municipality": parsed.municipality,
                "department": parsed.department,
                "lot_varietal": parsed.varietal,
                "lot_process": parsed.process_hint,
                "packaging_type": parsed.packaging_type,
                "origin": origin,
                "processes": [],
                "offering_ids": [],
                "tasting_notes": [],
                "certifications": set(),
                "region": str(row.get("Region", "") or "").strip(),
            }

        g = groups[key]
        proc = norm_process(str(row.get("Process", "") or ""))
        if proc and proc not in g["processes"]:
            g["processes"].append(proc)

        oid = str(row.get("OfferingID", "") or "").strip()
        if oid and oid not in g["offering_ids"]:
            g["offering_ids"].append(oid)

        notes = str(row.get("TastingNotes", "") or "").strip()
        if notes and notes not in g["tasting_notes"]:
            g["tasting_notes"].append(notes)

        certs_raw = str(row.get("Certifications", "") or "")
        for c in certs_raw.split(","):
            c = c.strip()
            if c:
                g["certifications"].add(c)

    return groups


def load(rows: list) -> dict:
    if not rows:
        return {"inserted": 0, "updated": 0, "skipped": 0}

    engine = _get_engine()
    counts = {"inserted": 0, "updated": 0, "skipped": 0}
    groups = _group_by_producer(rows)

    with engine.begin() as conn:
        origin_cache = _origin_id_cache(conn)

        for slug, g in groups.items():
            origin_id = origin_cache.get(g["origin"].lower())
            processes = g["processes"]
            importer_ids = {"cafe_imports": g["offering_ids"]} if g["offering_ids"] else {}

            existing = conn.execute(
                text("SELECT id, process_methods, importer_ids FROM farms WHERE slug = :slug"),
                {"slug": slug},
            ).fetchone()

            if existing:
                # Merge process_methods; overwrite importer_ids cafe_imports key
                existing_procs = existing.process_methods or []
                merged_procs = list(dict.fromkeys(existing_procs + processes))
                existing_imp = existing.importer_ids or {}
                existing_imp.update(importer_ids)

                conn.execute(
                    text("""
                        UPDATE farms SET
                            canonical_name = :name,
                            owner_name = COALESCE(:owner, owner_name),
                            municipality = COALESCE(:municipality, municipality),
                            department = COALESCE(:department, department),
                            lot_varietal = COALESCE(:lot_varietal, lot_varietal),
                            lot_process = COALESCE(:lot_process, lot_process),
                            packaging_type = COALESCE(:packaging_type, packaging_type),
                            source_lot_title = COALESCE(:source_lot_title, source_lot_title),
                            process_methods = :pm,
                            importer_ids = :imp
                        WHERE id = :id
                    """),
                    {
                        "name": g["canonical_name"],
                        "owner": g.get("owner_name"),
                        "municipality": g.get("municipality"),
                        "department": g.get("department"),
                        "lot_varietal": g.get("lot_varietal"),
                        "lot_process": g.get("lot_process"),
                        "packaging_type": g.get("packaging_type"),
                        "source_lot_title": g.get("source_lot_title"),
                        "pm": merged_procs,
                        "imp": json.dumps(existing_imp),
                        "id": existing.id,
                    },
                )
                counts["updated"] += 1
            else:
                conn.execute(
                    text("""
                        INSERT INTO farms (
                            slug, canonical_name, owner_name, municipality, department,
                            lot_varietal, lot_process, packaging_type, source_lot_title,
                            origin_id, process_methods, importer_ids, source
                        )
                        VALUES (
                            :slug, :name, :owner, :municipality, :department,
                            :lot_varietal, :lot_process, :packaging_type, :source_lot_title,
                            :origin_id, :pm, :imp, 'cafe_imports'
                        )
                    """),
                    {
                        "slug": slug,
                        "name": g["canonical_name"],
                        "owner": g.get("owner_name"),
                        "municipality": g.get("municipality"),
                        "department": g.get("department"),
                        "lot_varietal": g.get("lot_varietal"),
                        "lot_process": g.get("lot_process"),
                        "packaging_type": g.get("packaging_type"),
                        "source_lot_title": g.get("source_lot_title"),
                        "origin_id": origin_id,
                        "pm": processes,
                        "imp": json.dumps(importer_ids),
                    },
                )
                counts["inserted"] += 1

    log.info(
        "cafe_imports loader: inserted=%d updated=%d skipped=%d",
        counts["inserted"], counts["updated"], counts["skipped"],
    )
    return counts
