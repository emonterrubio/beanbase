"""
Cafe Imports North America offerings scraper.
Fetches the offerings table, normalizes key fields, and writes a dated CSV dump.

Usage:
    python pipeline/src/scrapers/cafe_imports_scraper.py
    python pipeline/src/scrapers/cafe_imports_scraper.py --out custom.csv
    python pipeline/src/scrapers/cafe_imports_scraper.py --json

Outputs default to pipeline/data/cafe_imports_YYYY-MM.csv (and optional .json sidecar).
"""

import argparse
import csv
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://www.cafeimports.com/north-america/offerings"

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent.parent / "data"

# ---------------------------------------------------------------------------
# Column layout (positional, 0-based) as observed from live page HTML
# ---------------------------------------------------------------------------
COL = {
    "ORIGIN":      0,
    "GRADE":       1,
    "NAME":        2,
    "ID":          3,
    "BAG_SIZE":    4,
    "BAG_COUNT":   5,
    "LOCATION":    6,   # "StatusEst Arrival/Ship: Date" — split below
    "EST_ARRIVAL": 7,   # populated for Afloat rows only (same concat format)
    "EST_SHIP":    8,   # populated for At Origin rows only
    "DESTINATION": 9,
    # 10 = More Info (skip)
    # 11 = Location Dictionary (skip — we parse col 6 instead)
    "NOTES":      12,
    "CERT":       13,
    "REGION":     14,
    "PROCESS":    15,
    "STRATIFIED": 16,
    "PROGRAM":    17,
    "FEATURED":   18,
    "NEW":        19,
}

# Canonical process names
PROCESS_NORM = {
    "washed":          "Washed",
    "natural":         "Natural",
    "honey":           "Honey",
    "pulped natural":  "Pulped Natural",
    "wet hulled":      "Wet Hulled",
    "wet-hulled":      "Wet Hulled",
    "anaerobic":       "Anaerobic",
    "decaf":           "Decaf",
    "co2 decaf":       "Decaf (CO2)",
    "swiss water":     "Decaf (Swiss Water)",
    "semi-washed":     "Semi-Washed",
}

# Canonical status names
STATUS_NORM = {
    "spot":      "Spot",
    "afloat":    "Afloat",
    "at origin": "At Origin",
    "origin":    "At Origin",
    "pre-ship":  "Pre-Ship",
    "pre ship":  "Pre-Ship",
}

# Regex to split e.g. "AfloatEst Arrival: Early Jul 2026"
#                  or "At originEst Ship: Aug 2026"
_LOC_RE = re.compile(
    r'^(Spot|Afloat|At\s+origin|Pre[- ]?ship)\s*(Est\s+(?:Arrival|Ship)\s*:\s*(.+))?$',
    re.IGNORECASE,
)


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _dedup_text(text: str) -> str:
    """Fix DOM duplication: 'Carmo de Minas Carmo de Minas' → 'Carmo de Minas'."""
    words = text.split()
    n = len(words)
    if n >= 2 and n % 2 == 0:
        half1 = " ".join(words[: n // 2])
        half2 = " ".join(words[n // 2 :])
        if half1 == half2:
            return half1
    return text


def _norm_process(raw: str) -> str:
    key = raw.lower().strip()
    return PROCESS_NORM.get(key, raw.strip().title() if raw.strip() else "")


def _norm_status(raw: str) -> str:
    key = raw.lower().strip()
    return STATUS_NORM.get(key, raw.strip().title() if raw.strip() else "")


def _parse_location(raw: str) -> tuple[str, str]:
    """
    Split a concatenated location cell into (status, date_string).
    Examples:
      "Spot"                          → ("Spot", "")
      "AfloatEst Arrival: Jul 2026"   → ("Afloat", "Jul 2026")
      "At originEst Ship: Aug 2026"   → ("At Origin", "Aug 2026")
    """
    raw = _clean(raw)
    m = _LOC_RE.match(raw)
    if m:
        status = _norm_status(m.group(1))
        date_str = _clean(m.group(3)) if m.group(3) else ""
        return status, date_str
    # Fallback: whole string is the status
    return _norm_status(raw), ""


# CSS class tokens and internal labels that appear in the certs cell — not real certs
_CERT_SKIP = re.compile(r'^(nft|norg|ci-usa|ci-eu|featured|new)$', re.IGNORECASE)

def _clean_certs(raw_tab_preserved: str) -> str:
    """
    Extract real certification names from the certs cell.
    The cell uses commas AND tabs as token separators; tabs must be split
    BEFORE whitespace normalization to avoid fusing adjacent tokens.
    """
    parts = re.split(r"[\t,]+", raw_tab_preserved)
    seen: set[str] = set()
    out = []
    for p in parts:
        p = _clean(p)
        if not p or _CERT_SKIP.match(p):
            continue
        key = p.lower()
        if key not in seen:
            seen.add(key)
            out.append(p)
    return ", ".join(out)


def _cell_text(cells: list, idx: int) -> str:
    if idx >= len(cells):
        return ""
    return _clean(cells[idx].get_text())


def _cell_raw(cells: list, idx: int) -> str:
    """Return cell text with original whitespace intact (tabs/newlines preserved)."""
    if idx >= len(cells):
        return ""
    return cells[idx].get_text()


# ---------------------------------------------------------------------------
# Fetch + parse
# ---------------------------------------------------------------------------

def fetch_page(url: str) -> BeautifulSoup:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")


def parse_offerings(soup: BeautifulSoup) -> list[dict]:
    table = soup.find("table")
    if not table:
        sys.exit("ERROR: No <table> found on the page — layout may have changed.")

    rows = table.find_all("tr")
    if len(rows) < 2:
        sys.exit("ERROR: Table has fewer than 2 rows.")

    today = date.today().strftime("%Y-%m")
    offerings = []

    for row in rows[1:]:  # skip header row
        cells = row.find_all(["td", "th"])
        if len(cells) < 16:
            continue

        raw_id = re.sub(r"\D", "", _cell_text(cells, COL["ID"]))
        if not raw_id:
            continue  # repeated header or spacer row

        loc_raw = _cell_text(cells, COL["LOCATION"])
        status, loc_date = _parse_location(loc_raw)

        est_arrival_raw = _cell_text(cells, COL["EST_ARRIVAL"])
        _, est_arrival = _parse_location(est_arrival_raw)
        if not est_arrival and loc_date and status == "Afloat":
            est_arrival = loc_date

        est_ship_raw = _cell_text(cells, COL["EST_SHIP"])
        _, est_ship = _parse_location(est_ship_raw)
        if not est_ship and loc_date and status == "At Origin":
            est_ship = loc_date

        record = {
            "OfferingID":        raw_id,
            "Origin":            _cell_text(cells, COL["ORIGIN"]),
            "Grade":             _dedup_text(_cell_text(cells, COL["GRADE"])),
            "Name":              _cell_text(cells, COL["NAME"]),
            "Region":            _cell_text(cells, COL["REGION"]),
            "Process":           _norm_process(_cell_text(cells, COL["PROCESS"])),
            "Status":            status,
            "BagSize_kg":        _cell_text(cells, COL["BAG_SIZE"]),
            "BagCount":          _cell_text(cells, COL["BAG_COUNT"]),
            "EstArrival":        est_arrival,
            "EstShip":           est_ship,
            "Destination":       _cell_text(cells, COL["DESTINATION"]),
            "Certifications":    _clean_certs(_cell_raw(cells, COL["CERT"])),
            "StratifiedCategory": _cell_text(cells, COL["STRATIFIED"]),
            "Program":           _cell_text(cells, COL["PROGRAM"]),
            "TastingNotes":      _cell_text(cells, COL["NOTES"]),
            "Featured":          _cell_text(cells, COL["FEATURED"]),
            "New":               _cell_text(cells, COL["NEW"]),
            "ScrapedMonth":      today,
        }
        offerings.append(record)

    return offerings


OUTPUT_FIELDS = [
    "OfferingID", "Origin", "Grade", "Name", "Region", "Process", "Status",
    "BagSize_kg", "BagCount", "EstArrival", "EstShip", "Destination",
    "Certifications", "StratifiedCategory", "Program", "TastingNotes",
    "Featured", "New", "ScrapedMonth",
]


def write_csv(offerings: list[dict], path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(offerings)
    print(f"CSV  → {path}  ({len(offerings)} rows)")


def write_json(offerings: list[dict], path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(offerings, f, indent=2, ensure_ascii=False)
    print(f"JSON → {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Cafe Imports North America offerings")
    parser.add_argument("--out", help="Output CSV path (default: pipeline/data/cafe_imports_YYYY-MM.csv)")
    parser.add_argument("--json", action="store_true", help="Also write a JSON sidecar")
    parser.add_argument("--url", default=BASE_URL, help="Override the offerings URL")
    args = parser.parse_args()

    month_stamp = date.today().strftime("%Y-%m")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = Path(args.out) if args.out else DATA_DIR / f"cafe_imports_{month_stamp}.csv"
    json_path = csv_path.with_suffix(".json")

    print(f"Fetching {args.url} …")
    soup = fetch_page(args.url)

    print("Parsing table …")
    offerings = parse_offerings(soup)

    if not offerings:
        sys.exit("ERROR: Parsed 0 offerings — verify the page structure hasn't changed.")

    write_csv(offerings, csv_path)
    if args.json:
        write_json(offerings, json_path)

    status_counts = Counter(o["Status"] for o in offerings)
    process_counts = Counter(o["Process"] for o in offerings)
    print(f"\nSummary — {len(offerings)} offerings total:")
    print("  Status :", dict(status_counts.most_common()))
    print("  Process:", dict(process_counts.most_common(8)))


if __name__ == "__main__":
    main()
