"""
Cafe Imports North America offerings scraper.
Exposes run(month_stamp) -> list[dict] for the monthly orchestrator.
Also runnable standalone: python3 -m scrapers.cafe_imports
"""

import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URL = "http://www.cafeimports.com/north-america/offerings"

# Positional column layout (0-based) as observed from live page HTML
COL = {
    "ORIGIN":      0,
    "GRADE":       1,
    "NAME":        2,
    "ID":          3,
    "BAG_SIZE":    4,
    "BAG_COUNT":   5,
    "LOCATION":    6,   # "StatusEst Arrival/Ship: Date" — split below
    "EST_ARRIVAL": 7,   # Afloat rows only
    "EST_SHIP":    8,   # At Origin rows only
    "DESTINATION": 9,
    # 10 = More Info (skip)
    # 11 = Location Dictionary (skip — col 6 parsed instead)
    "NOTES":      12,
    "CERT":       13,
    "REGION":     14,
    "PROCESS":    15,
    "STRATIFIED": 16,
    "PROGRAM":    17,
    "FEATURED":   18,
    "NEW":        19,
}

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

STATUS_NORM = {
    "spot":      "Spot",
    "afloat":    "Afloat",
    "at origin": "At Origin",
    "origin":    "At Origin",
    "pre-ship":  "Pre-Ship",
    "pre ship":  "Pre-Ship",
}

_LOC_RE = re.compile(
    r"^(Spot|Afloat|At\s+origin|Pre[- ]?ship)\s*(Est\s+(?:Arrival|Ship)\s*:\s*(.+))?$",
    re.IGNORECASE,
)

_CERT_SKIP = re.compile(r"^(nft|norg|ci-usa|ci-eu|featured|new)$", re.IGNORECASE)

FIELDS = [
    "OfferingID", "Origin", "Grade", "Name", "Region", "Process", "Status",
    "BagSize_kg", "BagCount", "EstArrival", "EstShip", "Destination",
    "Certifications", "StratifiedCategory", "Program", "TastingNotes",
    "Featured", "New", "ScrapedMonth",
]


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _dedup_text(text: str) -> str:
    words = text.split()
    n = len(words)
    if n >= 2 and n % 2 == 0:
        half1 = " ".join(words[: n // 2])
        half2 = " ".join(words[n // 2 :])
        if half1 == half2:
            return half1
    return text


def _norm_process(raw: str) -> str:
    return PROCESS_NORM.get(raw.lower().strip(), raw.strip().title() if raw.strip() else "")


def _norm_status(raw: str) -> str:
    return STATUS_NORM.get(raw.lower().strip(), raw.strip().title() if raw.strip() else "")


def _parse_location(raw: str) -> tuple[str, str]:
    raw = _clean(raw)
    m = _LOC_RE.match(raw)
    if m:
        return _norm_status(m.group(1)), _clean(m.group(3)) if m.group(3) else ""
    return _norm_status(raw), ""


def _clean_certs(raw_tab_preserved: str) -> str:
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


def _cell(cells: list, idx: int) -> str:
    if idx >= len(cells):
        return ""
    return _clean(cells[idx].get_text())


def _cell_raw(cells: list, idx: int) -> str:
    if idx >= len(cells):
        return ""
    return cells[idx].get_text()


def fetch(url: str = URL) -> BeautifulSoup:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")


def parse(soup: BeautifulSoup, month_stamp: str) -> list[dict]:
    table = soup.find("table")
    if not table:
        raise RuntimeError("No <table> found — page layout may have changed.")

    rows = table.find_all("tr")
    if len(rows) < 2:
        raise RuntimeError("Table has fewer than 2 rows.")

    offerings = []
    for row in rows[1:]:
        cells = row.find_all(["td", "th"])
        if len(cells) < 16:
            continue

        raw_id = re.sub(r"\D", "", _cell(cells, COL["ID"]))
        if not raw_id:
            continue

        loc_raw = _cell(cells, COL["LOCATION"])
        status, loc_date = _parse_location(loc_raw)

        _, est_arrival = _parse_location(_cell(cells, COL["EST_ARRIVAL"]))
        if not est_arrival and loc_date and status == "Afloat":
            est_arrival = loc_date

        _, est_ship = _parse_location(_cell(cells, COL["EST_SHIP"]))
        if not est_ship and loc_date and status == "At Origin":
            est_ship = loc_date

        offerings.append({
            "OfferingID":        raw_id,
            "Origin":            _cell(cells, COL["ORIGIN"]),
            "Grade":             _dedup_text(_cell(cells, COL["GRADE"])),
            "Name":              _cell(cells, COL["NAME"]),
            "Region":            _cell(cells, COL["REGION"]),
            "Process":           _norm_process(_cell(cells, COL["PROCESS"])),
            "Status":            status,
            "BagSize_kg":        _cell(cells, COL["BAG_SIZE"]),
            "BagCount":          _cell(cells, COL["BAG_COUNT"]),
            "EstArrival":        est_arrival,
            "EstShip":           est_ship,
            "Destination":       _cell(cells, COL["DESTINATION"]),
            "Certifications":    _clean_certs(_cell_raw(cells, COL["CERT"])),
            "StratifiedCategory": _cell(cells, COL["STRATIFIED"]),
            "Program":           _cell(cells, COL["PROGRAM"]),
            "TastingNotes":      _cell(cells, COL["NOTES"]),
            "Featured":          _cell(cells, COL["FEATURED"]),
            "New":               _cell(cells, COL["NEW"]),
            "ScrapedMonth":      month_stamp,
        })

    return offerings


def run(month_stamp: str, url: str = URL) -> list[dict]:
    soup = fetch(url)
    return parse(soup, month_stamp)


if __name__ == "__main__":
    import csv
    from datetime import date

    month = date.today().strftime("%Y-%m")
    rows = run(month)
    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    print(f"# {len(rows)} rows", file=sys.stderr)
