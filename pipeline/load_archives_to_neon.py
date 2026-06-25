"""
One-shot: load all CoE archive JSON files into the target DATABASE_URL.
Processes one archive file at a time (one transaction per auction page) to
avoid remote connection timeouts on large backfills.

Run from the pipeline/ directory:
    DATABASE_URL="postgresql://..." python3 load_archives_to_neon.py
"""
import json
import logging
import os
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s %(message)s")
log = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from loaders.coe_loader import load

ARCHIVE_DIR = Path(__file__).resolve().parent / "data" / "coe"


def main():
    files = sorted(ARCHIVE_DIR.glob("*.json"))
    log.info("Found %d archive files in %s", len(files), ARCHIVE_DIR)

    total = {"inserted": 0, "updated": 0, "skipped": 0}

    for i, f in enumerate(files, 1):
        with open(f) as fp:
            data = json.load(fp)
        lots = data.get("lots", data) if isinstance(data, dict) else data

        if not lots:
            log.warning("[%d/%d] %s — no lots, skipping", i, len(files), f.name)
            continue

        result = load(lots)
        total["inserted"] += result["inserted"]
        total["updated"]  += result["updated"]
        total["skipped"]  += result["skipped"]

        log.info(
            "[%d/%d] %s — inserted=%d updated=%d skipped=%d  (running: +%d ~%d)",
            i, len(files), f.name,
            result["inserted"], result["updated"], result["skipped"],
            total["inserted"], total["updated"],
        )

    log.info(
        "Done: inserted=%d updated=%d skipped=%d",
        total["inserted"], total["updated"], total["skipped"],
    )


if __name__ == "__main__":
    main()
