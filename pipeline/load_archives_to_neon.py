"""
One-shot: load all CoE archive JSON files into the target DATABASE_URL.
Processes one archive file at a time (one transaction per auction page) to
avoid remote connection timeouts on large backfills. Connection errors on
individual files are caught and retried once; persistent failures are logged
and skipped so the overall run completes.

Run from the pipeline/ directory:
    DATABASE_URL="postgresql://..." python3 load_archives_to_neon.py
"""
import json
import logging
import sys
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s %(message)s")
log = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from loaders.coe_loader import load

ARCHIVE_DIR = Path(__file__).resolve().parent / "data" / "coe"


def _load_with_retry(lots, filename, attempt=1):
    try:
        return load(lots)
    except Exception as exc:
        if attempt < 3:
            wait = attempt * 5
            log.warning("%s: error on attempt %d — %s. Retrying in %ds...", filename, attempt, exc, wait)
            time.sleep(wait)
            return _load_with_retry(lots, filename, attempt + 1)
        raise


def main():
    files = sorted(ARCHIVE_DIR.glob("*.json"))
    log.info("Found %d archive files in %s", len(files), ARCHIVE_DIR)

    total = {"inserted": 0, "updated": 0, "skipped": 0}
    failed = []

    for i, f in enumerate(files, 1):
        with open(f) as fp:
            data = json.load(fp)
        lots = data.get("lots", data) if isinstance(data, dict) else data

        if not lots:
            log.warning("[%d/%d] %s — no lots, skipping", i, len(files), f.name)
            continue

        try:
            result = _load_with_retry(lots, f.name)
        except Exception as exc:
            log.error("[%d/%d] %s — FAILED after retries: %s", i, len(files), f.name, exc)
            failed.append(f.name)
            continue

        total["inserted"] += result["inserted"]
        total["updated"]  += result["updated"]
        total["skipped"]  += result["skipped"]

        log.info(
            "[%d/%d] %s — inserted=%d updated=%d skipped=%d  (total: +%d ~%d)",
            i, len(files), f.name,
            result["inserted"], result["updated"], result["skipped"],
            total["inserted"], total["updated"],
        )

    log.info(
        "Done: inserted=%d updated=%d skipped=%d",
        total["inserted"], total["updated"], total["skipped"],
    )
    if failed:
        log.error("Failed files (%d): %s", len(failed), ", ".join(failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
