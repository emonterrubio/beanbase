"""
One-shot: load all CoE archive JSON files into the target DATABASE_URL.
Run from the pipeline/ directory with the Neon URL set:

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

    all_rows = []
    for f in files:
        with open(f) as fp:
            data = json.load(fp)
            lots = data.get("lots", data) if isinstance(data, dict) else data
            all_rows.extend(lots)

    log.info("Total lots across all archives: %d", len(all_rows))
    result = load(all_rows)
    log.info("Done: inserted=%d updated=%d skipped=%d", result["inserted"], result["updated"], result["skipped"])


if __name__ == "__main__":
    main()
