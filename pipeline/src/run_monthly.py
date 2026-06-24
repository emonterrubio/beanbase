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
import sys
from collections import Counter
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (all relative to pipeline/)
# ---------------------------------------------------------------------------
PIPELINE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR     = PIPELINE_DIR / "data"
SNAP_DIR     = DATA_DIR / "snapshots"
HIST_DIR     = DATA_DIR / "history"
LOG_DIR      = PIPELINE_DIR / "logs"

# Add src/ to path so scrapers are importable when called directly
sys.path.insert(0, str(Path(__file__).resolve().parent))

from scrapers import cafe_imports, onyx  # noqa: E402

# ---------------------------------------------------------------------------
# Scraper registry
# Each entry: (key, module, fields_list)
# ---------------------------------------------------------------------------
SCRAPERS = [
    ("cafe_imports", cafe_imports, cafe_imports.FIELDS),
    ("onyx",         onyx,         onyx.FIELDS),
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

    status_field  = "Status"    if key == "cafe_imports" else "Available"
    process_field = "Process"

    log.info("%s: %d rows", key, len(rows))

    if key == "cafe_imports":
        status_counts = Counter(r.get(status_field, "") for r in rows)
        log.info("  Status  → %s", dict(status_counts.most_common()))
    else:
        avail = sum(1 for r in rows if r.get("Available") == "true")
        log.info("  Available → %d/%d", avail, len(rows))

    process_counts = Counter(r.get(process_field, "") for r in rows if r.get(process_field))
    log.info("  Process → %s", dict(process_counts.most_common(6)))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="beanBase monthly pipeline")
    parser.add_argument("--month", default=date.today().strftime("%Y-%m"),
                        help="Month to scrape, format YYYY-MM (default: current month)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Fetch and parse but do not write any files")
    args = parser.parse_args()

    month_stamp = args.month
    log.info("=== beanBase pipeline — %s%s ===",
             month_stamp, "  [DRY RUN]" if args.dry_run else "")

    failed: list[str] = []

    for key, module, fields in SCRAPERS:
        log.info("--- %s ---", key)
        try:
            rows = module.run(month_stamp)
        except Exception as exc:
            log.error("%s: scrape failed — %s", key, exc)
            failed.append(key)
            continue

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

    if failed:
        log.error("Pipeline finished with errors: %s", failed)
        sys.exit(1)

    log.info("=== done ===")


if __name__ == "__main__":
    main()
