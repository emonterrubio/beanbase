"""
Monthly pipeline orchestrator.
Runs all scrapers, writes dated snapshots, and appends to rolling history CSVs.

Usage:
    python3 run_monthly.py              # run for current month
    python3 run_monthly.py --month 2026-05  # backfill a specific month
    python3 run_monthly.py --dry-run    # fetch + parse but don't write files
"""

import argparse
import csv
import logging
import os
import sys
from collections import Counter
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Paths (all relative to pipeline/)
# ---------------------------------------------------------------------------
PIPELINE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR     = PIPELINE_DIR / "data"
SNAP_DIR     = DATA_DIR / "snapshots"
HIST_DIR     = DATA_DIR / "history"
LOG_DIR      = PIPELINE_DIR / "logs"

# Add src/ to path so scrapers and loaders are importable when called directly
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Load pipeline .env (DATABASE_URL for loaders), then fall back to api/.env
_PIPELINE_ENV = Path(__file__).resolve().parents[1] / ".env"
_API_ENV      = Path(__file__).resolve().parents[2] / "api" / ".env"
load_dotenv(_PIPELINE_ENV if _PIPELINE_ENV.exists() else _API_ENV)

from scrapers import cafe_imports, coe_scraper, onyx  # noqa: E402

# ---------------------------------------------------------------------------
# Scraper registry
# Each entry: (key, module, fields_list)
# ---------------------------------------------------------------------------
SCRAPERS = [
    ("cafe_imports", cafe_imports, cafe_imports.FIELDS),
    ("onyx",         onyx,         onyx.FIELDS),
    ("coe",          coe_scraper,  coe_scraper.FIELDS),
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("pipeline")


# ---------------------------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------------------------

def _write_snapshot(rows: list[dict], fields: list[str], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=fields).writeheader()
        csv.DictWriter(f, fieldnames=fields).writerows(rows)


def _append_history(rows: list[dict], fields: list[str],
                    path: Path, month_stamp: str) -> tuple[int, bool]:
    """
    Append rows to the rolling history CSV.
    Returns (rows_written, already_existed) and skips the month if already present.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    already_exists = path.exists()

    if already_exists:
        # Check whether this month is already in the file to avoid duplicate appends
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for existing_row in reader:
                if existing_row.get("ScrapedMonth") == month_stamp:
                    log.warning(
                        "%s already contains %s — skipping history append",
                        path.name, month_stamp,
                    )
                    return 0, True

    mode = "a" if already_exists else "w"
    with open(path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if not already_exists:
            writer.writeheader()
        writer.writerows(rows)

    return len(rows), already_exists


# ---------------------------------------------------------------------------
# Per-scraper summary
# ---------------------------------------------------------------------------

def _summarize(key: str, rows: list[dict]) -> None:
    if not rows:
        log.warning("%s: 0 rows — check scraper", key)
        return

    log.info("%s: %d rows", key, len(rows))

    if key == "cafe_imports":
        status_counts = Counter(r.get("Status", "") for r in rows)
        log.info("  Status  → %s", dict(status_counts.most_common()))
    elif key == "onyx":
        avail = sum(1 for r in rows if r.get("Available") == "true")
        log.info("  Available → %d/%d", avail, len(rows))
    elif key == "coe":
        country_counts = Counter(r.get("Country", "") for r in rows)
        log.info("  Countries → %s", dict(country_counts.most_common(10)))
        lot_type_counts = Counter(r.get("LotType", "") for r in rows)
        log.info("  LotType   → %s", dict(lot_type_counts.most_common()))

    process_field = "Process" if key != "onyx" else "Process"
    process_counts = Counter(r.get(process_field, "") for r in rows if r.get(process_field))
    if process_counts:
        log.info("  Process → %s", dict(process_counts.most_common(6)))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _run_loaders(scraped: dict, month_stamp: str) -> None:
    """Phase 2: write scraped rows to PostgreSQL. Skipped if DATABASE_URL not set."""
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        log.info("DATABASE_URL not set — skipping DB loaders")
        return

    from loaders import cafe_imports_loader, coe_loader, onyx_loader

    LOADERS = [
        ("coe",          coe_loader,          scraped.get("coe", [])),
        ("cafe_imports", cafe_imports_loader,  scraped.get("cafe_imports", [])),
        ("onyx",         onyx_loader,          scraped.get("onyx", [])),
    ]

    log.info("--- DB loaders ---")
    for key, loader, rows in LOADERS:
        if not rows:
            log.info("%s loader: 0 rows — skipping", key)
            continue
        try:
            result = loader.load(rows)
            log.info("%s loader: %s", key, result)
        except Exception as exc:
            log.error("%s loader failed: %s", key, exc)


def main() -> None:
    parser = argparse.ArgumentParser(description="beanBase monthly pipeline")
    parser.add_argument("--month", default=date.today().strftime("%Y-%m"),
                        help="Month to scrape, format YYYY-MM (default: current month)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Fetch and parse but do not write any files or load DB")
    args = parser.parse_args()

    month_stamp = args.month
    log.info("=== beanBase pipeline — %s%s ===",
             month_stamp, "  [DRY RUN]" if args.dry_run else "")

    failed: list[str] = []
    scraped: dict = {}

    # Phase 1: scrape
    for key, module, fields in SCRAPERS:
        log.info("--- %s ---", key)
        try:
            rows = module.run(month_stamp)
        except Exception as exc:
            log.error("%s: scrape failed — %s", key, exc)
            failed.append(key)
            continue

        scraped[key] = rows
        _summarize(key, rows)

        if args.dry_run:
            log.info("%s: dry-run — no files written", key)
            continue

        # Snapshot
        snap_path = SNAP_DIR / month_stamp / f"{key}.csv"
        _write_snapshot(rows, fields, snap_path)
        log.info("%s: snapshot → %s", key, snap_path.relative_to(PIPELINE_DIR))

        # History
        hist_path = HIST_DIR / f"{key}_history.csv"
        written, existed = _append_history(rows, fields, hist_path, month_stamp)
        if written:
            action = "appended" if existed else "created"
            log.info("%s: history %s → %s  (+%d rows)",
                     key, action, hist_path.relative_to(PIPELINE_DIR), written)

    # Phase 2: load into DB
    if not args.dry_run:
        _run_loaders(scraped, month_stamp)

    if failed:
        log.error("Pipeline finished with errors: %s", failed)
        sys.exit(1)

    log.info("=== done ===")


if __name__ == "__main__":
    main()
