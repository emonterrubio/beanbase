"""
Cup of Excellence historical scraper.
Interface: run(month_stamp) -> list[dict]

First run (empty pipeline/data/coe/ archive): scrapes all historical auction pages.
Subsequent monthly runs: re-fetches only current-year pages to pick up new auctions.
Raw JSON archived per auction to pipeline/data/coe/{slug}-{year_str}.json.

Standalone usage:
    python3 -m scrapers.coe_scraper                      # incremental (current year only if archive exists)
    python3 -m scrapers.coe_scraper --backfill           # force full backfill regardless of archive
    python3 -m scrapers.coe_scraper --country ethiopia   # single country only
    python3 -m scrapers.coe_scraper --dry-run            # fetch + parse, no archive writes
"""

import json
import logging
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://allianceforcoffeeexcellence.org"
COE_DIR = Path(__file__).resolve().parents[2] / "data" / "coe"

log = logging.getLogger(__name__)

_HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# ---------------------------------------------------------------------------
# Auction page registry
# (country, slug, year_str) — year_str is the URL suffix after the slug.
# URL = f"{BASE_URL}/{slug}-{year_str}/"
# year_str is usually "YYYY" but can be "YYYY-suffix" (e.g. "2015-january").
# ---------------------------------------------------------------------------
AUCTION_PAGES: List[tuple] = [
    # Bolivia
    ("Bolivia", "bolivia", "2004"),
    ("Bolivia", "bolivia", "2005"),
    ("Bolivia", "bolivia", "2007"),
    ("Bolivia", "bolivia", "2008"),
    ("Bolivia", "bolivia", "2009"),
    # Brazil — unified format (2019+)
    ("Brazil", "brazil", "2019"),
    ("Brazil", "brazil", "2020"),
    ("Brazil", "brazil", "2021"),
    ("Brazil", "brazil", "2022"),
    ("Brazil", "brazil", "2023"),
    ("Brazil", "brazil", "2024"),
    ("Brazil", "brazil", "2025"),
    ("Brazil", "brazil", "2026"),
    # Brazil Naturals (2012–2018)
    ("Brazil", "brazil-naturals", "2012"),
    ("Brazil", "brazil-naturals", "2013"),
    ("Brazil", "brazil-naturals", "2014"),
    ("Brazil", "brazil-naturals", "2015"),
    ("Brazil", "brazil-naturals", "2015-january"),
    ("Brazil", "brazil-naturals", "2016"),
    ("Brazil", "brazil-naturals", "2017"),
    ("Brazil", "brazil-naturals", "2018"),
    # Brazil Pulped Naturals (1999–2018)
    ("Brazil", "brazil-pulped-naturals", "1999"),
    ("Brazil", "brazil-pulped-naturals", "2000"),
    ("Brazil", "brazil-pulped-naturals", "2001"),
    ("Brazil", "brazil-pulped-naturals", "2002"),
    ("Brazil", "brazil-pulped-naturals", "2003"),
    ("Brazil", "brazil-pulped-naturals", "2004"),
    ("Brazil", "brazil-pulped-naturals", "2005"),
    ("Brazil", "brazil-pulped-naturals", "2006"),
    ("Brazil", "brazil-pulped-naturals", "2008"),
    ("Brazil", "brazil-pulped-naturals", "2009"),
    ("Brazil", "brazil-pulped-naturals", "2011"),
    ("Brazil", "brazil-pulped-naturals", "2012"),
    ("Brazil", "brazil-pulped-naturals", "2013"),
    ("Brazil", "brazil-pulped-naturals", "2014"),
    ("Brazil", "brazil-pulped-naturals", "2015"),
    ("Brazil", "brazil-pulped-naturals", "2016"),
    ("Brazil", "brazil-pulped-naturals", "2017"),
    ("Brazil", "brazil-pulped-naturals", "2018"),
    # Burundi
    ("Burundi", "burundi", "2012"),
    ("Burundi", "burundi", "2013"),
    ("Burundi", "burundi", "2014"),
    ("Burundi", "burundi", "2015"),
    ("Burundi", "burundi", "2017"),
    ("Burundi", "burundi", "2018"),
    ("Burundi", "burundi", "2019"),
    # Colombia — unified
    ("Colombia", "colombia", "2017"),
    ("Colombia", "colombia", "2018"),
    ("Colombia", "colombia", "2020"),
    ("Colombia", "colombia", "2021"),
    ("Colombia", "colombia", "2022"),
    ("Colombia", "colombia", "2023"),
    # Colombia North
    ("Colombia", "colombia-north", "2005"),
    ("Colombia", "colombia-north", "2006"),
    ("Colombia", "colombia-north", "2007"),
    ("Colombia", "colombia-north", "2009"),
    ("Colombia", "colombia-north", "2011"),
    ("Colombia", "colombia-north", "2013"),
    ("Colombia", "colombia-north", "2015"),
    ("Colombia", "colombia-north", "2019"),
    # Colombia South
    ("Colombia", "colombia-south", "2005"),
    ("Colombia", "colombia-south", "2006"),
    ("Colombia", "colombia-south", "2008"),
    ("Colombia", "colombia-south", "2010"),
    ("Colombia", "colombia-south", "2012"),
    ("Colombia", "colombia-south", "2014"),
    # Costa Rica
    ("Costa Rica", "costa-rica", "2007"),
    ("Costa Rica", "costa-rica", "2008"),
    ("Costa Rica", "costa-rica", "2009"),
    ("Costa Rica", "costa-rica", "2011"),
    ("Costa Rica", "costa-rica", "2012"),
    ("Costa Rica", "costa-rica", "2013"),
    ("Costa Rica", "costa-rica", "2014"),
    ("Costa Rica", "costa-rica", "2015"),
    ("Costa Rica", "costa-rica", "2016"),
    ("Costa Rica", "costa-rica-coe", "2017"),
    ("Costa Rica", "costa-rica", "2018"),
    ("Costa Rica", "costa-rica", "2019"),
    ("Costa Rica", "costa-rica", "2020"),
    ("Costa Rica", "costa-rica", "2021"),
    ("Costa Rica", "costa-rica", "2022"),
    ("Costa Rica", "costa-rica", "2023"),
    ("Costa Rica", "costa-rica", "2024"),
    ("Costa Rica", "costa-rica", "2025"),
    ("Costa Rica", "costa-rica", "2026"),
    # Ecuador
    ("Ecuador", "ecuador", "2021"),
    ("Ecuador", "ecuador", "2022"),
    ("Ecuador", "ecuador", "2023"),
    # El Salvador
    ("El Salvador", "el-salvador", "2003"),
    ("El Salvador", "el-salvador", "2004"),
    ("El Salvador", "el-salvador", "2005"),
    ("El Salvador", "el-salvador", "2006"),
    ("El Salvador", "el-salvador", "2007"),
    ("El Salvador", "el-salvador", "2008"),
    ("El Salvador", "el-salvador", "2009"),
    ("El Salvador", "el-salvador", "2010"),
    ("El Salvador", "el-salvador", "2011"),
    ("El Salvador", "el-salvador", "2012"),
    ("El Salvador", "el-salvador", "2013"),
    ("El Salvador", "el-salvador", "2014"),
    ("El Salvador", "el-salvador", "2015"),
    ("El Salvador", "el-salvador", "2017"),
    ("El Salvador", "el-salvador", "2018"),
    ("El Salvador", "el-salvador", "2019"),
    ("El Salvador", "el-salvador", "2020"),
    ("El Salvador", "el-salvador", "2021"),
    ("El Salvador", "el-salvador", "2022"),
    ("El Salvador", "el-salvador", "2023"),
    ("El Salvador", "el-salvador", "2024"),
    ("El Salvador", "el-salvador", "2025"),
    ("El Salvador", "el-salvador", "2026"),
    # Ethiopia
    ("Ethiopia", "ethiopia", "2020"),
    ("Ethiopia", "ethiopia", "2021"),
    ("Ethiopia", "ethiopia", "2022"),
    ("Ethiopia", "ethiopia", "2024"),
    # Guatemala
    ("Guatemala", "guatemala", "2001"),
    ("Guatemala", "guatemala", "2002"),
    ("Guatemala", "guatemala", "2006"),
    ("Guatemala", "guatemala", "2007"),
    ("Guatemala", "guatemala", "2008"),
    ("Guatemala", "guatemala", "2009"),
    ("Guatemala", "guatemala", "2010"),
    ("Guatemala", "guatemala", "2011"),
    ("Guatemala", "guatemala", "2012"),
    ("Guatemala", "guatemala", "2013"),
    ("Guatemala", "guatemala", "2014"),
    ("Guatemala", "guatemala", "2015"),
    ("Guatemala", "guatemala", "2016"),
    ("Guatemala", "guatemala", "2017"),
    ("Guatemala", "guatemala", "2018"),
    ("Guatemala", "guatemala", "2019"),
    ("Guatemala", "guatemala", "2020"),
    ("Guatemala", "guatemala", "2021"),
    ("Guatemala", "guatemala", "2022"),
    ("Guatemala", "guatemala", "2023"),
    ("Guatemala", "guatemala", "2024"),
    ("Guatemala", "guatemala", "2025"),
    ("Guatemala", "guatemala", "2026"),
    # Honduras
    ("Honduras", "honduras", "2004"),
    ("Honduras", "honduras", "2005"),
    ("Honduras", "honduras", "2006"),
    ("Honduras", "honduras", "2007"),
    ("Honduras", "honduras", "2008"),
    ("Honduras", "honduras", "2009"),
    ("Honduras", "honduras", "2010"),
    ("Honduras", "honduras", "2011"),
    ("Honduras", "honduras", "2012"),
    ("Honduras", "honduras", "2013"),
    ("Honduras", "honduras", "2014"),
    ("Honduras", "honduras", "2015"),
    ("Honduras", "honduras", "2016"),
    ("Honduras", "honduras", "2017"),
    ("Honduras", "honduras", "2018"),
    ("Honduras", "honduras", "2019"),
    ("Honduras", "honduras", "2021"),
    ("Honduras", "honduras", "2022"),
    ("Honduras", "honduras", "2023"),
    ("Honduras", "honduras", "2024"),
    ("Honduras", "honduras", "2025"),
    ("Honduras", "honduras", "2026"),
    # Indonesia
    ("Indonesia", "indonesia", "2021"),
    ("Indonesia", "indonesia", "2022"),
    ("Indonesia", "indonesia", "2023"),
    ("Indonesia", "indonesia", "2026"),
    # Mexico
    ("Mexico", "mexico", "2012"),
    ("Mexico", "mexico", "2013"),
    ("Mexico", "mexico", "2014"),
    ("Mexico", "mexico", "2015"),
    ("Mexico", "mexico", "2017"),
    ("Mexico", "mexico", "2018"),
    ("Mexico", "mexico", "2019"),
    ("Mexico", "mexico", "2021"),
    ("Mexico", "mexico", "2022"),
    ("Mexico", "mexico", "2023"),
    ("Mexico", "mexico", "2024"),
    ("Mexico", "mexico", "2025"),
    ("Mexico", "mexico", "2026"),
    # Nicaragua
    ("Nicaragua", "nicaragua", "2002"),
    ("Nicaragua", "nicaragua", "2003"),
    ("Nicaragua", "nicaragua", "2004"),
    ("Nicaragua", "nicaragua", "2005"),
    ("Nicaragua", "nicaragua", "2006"),
    ("Nicaragua", "nicaragua", "2007"),
    ("Nicaragua", "nicaragua", "2008"),
    ("Nicaragua", "nicaragua", "2009"),
    ("Nicaragua", "nicaragua", "2010"),
    ("Nicaragua", "nicaragua", "2011"),
    ("Nicaragua", "nicaragua", "2012"),
    ("Nicaragua", "nicaragua", "2014"),
    ("Nicaragua", "nicaragua", "2015"),
    ("Nicaragua", "nicaragua", "2017"),
    ("Nicaragua", "nicaragua", "2018"),
    ("Nicaragua", "nicaragua", "2020"),
    ("Nicaragua", "nicaragua", "2021"),
    ("Nicaragua", "nicaragua", "2022"),
    ("Nicaragua", "nicaragua", "2023"),
    ("Nicaragua", "nicaragua", "2024"),
    ("Nicaragua", "nicaragua", "2025"),
    ("Nicaragua", "nicaragua", "2026"),
    # Peru
    ("Peru", "peru", "2017"),
    ("Peru", "peru", "2018"),
    ("Peru", "peru", "2019"),
    ("Peru", "peru", "2020"),
    ("Peru", "peru", "2021"),
    ("Peru", "peru", "2022"),
    ("Peru", "peru", "2023"),
    ("Peru", "peru", "2024"),
    ("Peru", "peru", "2025"),
    ("Peru", "peru", "2026"),
    # Rwanda
    ("Rwanda", "rwanda", "2008"),
    ("Rwanda", "rwanda", "2010"),
    ("Rwanda", "rwanda", "2011"),
    ("Rwanda", "rwanda", "2012"),
    ("Rwanda", "rwanda", "2013"),
    ("Rwanda", "rwanda", "2014"),
    ("Rwanda", "rwanda", "2015"),
    ("Rwanda", "rwanda", "2018"),
    # Taiwan
    ("Taiwan", "taiwan", "2024"),
    ("Taiwan", "taiwan", "2025"),
    # Thailand
    ("Thailand", "thailand", "2023"),
    ("Thailand", "thailand", "2024"),
    ("Thailand", "thailand", "2025"),
    ("Thailand", "thailand", "2026"),
]

FIELDS = [
    "AuctionSlug", "AuctionYear", "Country", "LotRank", "LotType",
    "FarmName", "ProducerName", "Region", "Process", "Varietal",
    "WeightKg", "ScoreCoE", "PriceUSDPerLb", "TotalValueUSD", "BuyerName",
    "ScrapedMonth",
]

# Process inferred from slug when no PROCESS column exists (old pages)
_SLUG_PROCESS: Dict[str, str] = {
    "pulped-naturals": "Pulped Natural",
    "naturals":        "Natural",
}


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def _parse_float(text: str) -> Optional[float]:
    if not text:
        return None
    # Strip currency, units, commas — take numeric part before any "/"
    s = re.sub(r"[,$€£\s]", "", text.split("/")[0])
    try:
        return float(s)
    except ValueError:
        return None


def _process_hint(slug: str) -> str:
    for pattern, process in _SLUG_PROCESS.items():
        if pattern in slug:
            return process
    return ""


def _fetch(url: str) -> Optional[BeautifulSoup]:
    try:
        resp = requests.get(url, headers=_HTTP_HEADERS, timeout=30)
        if resp.status_code == 404:
            log.debug("404: %s", url)
            return None
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "lxml")
    except requests.RequestException as exc:
        log.warning("fetch error %s: %s", url, exc)
        return None


# ---------------------------------------------------------------------------
# Table classification
# ---------------------------------------------------------------------------

def _header_map(table) -> Dict[str, int]:
    """Return {UPPERCASE_HEADER: col_index} from the first non-empty row."""
    for row in table.find_all("tr"):
        cells = row.find_all(["th", "td"])
        texts = [_clean(c.get_text()).upper() for c in cells]
        if any(t for t in texts if len(t) > 1):
            return {t: i for i, t in enumerate(texts) if t}
    return {}


def _is_results_table(hmap: Dict[str, int]) -> bool:
    has_score = "SCORE" in hmap
    has_farm = any(k for k in hmap if "FARM" in k and "WINNING" not in k)
    has_region = "REGION" in hmap
    return has_score and has_farm and has_region


def _is_auction_table(hmap: Dict[str, int]) -> bool:
    has_bid = any(k for k in hmap if "BID" in k or "FINAL BID" in k)
    has_buyer = any(k for k in hmap if "BIDDER" in k or "COMPANY" in k)
    return has_bid and has_buyer


def _is_jury_or_commission_table(hmap: Dict[str, int]) -> bool:
    return (
        ("NAME" in hmap and "COMPANY" in hmap and "COUNTRY" in hmap)
        or "AUCTION COMMISSION" in hmap
        or "COMMISSION" in hmap
    )


# ---------------------------------------------------------------------------
# Table parsers
# ---------------------------------------------------------------------------

def _get_cell(hmap: Dict[str, int], cells: list, *keys: str) -> str:
    for k in keys:
        if k in hmap:
            idx = hmap[k]
            if idx < len(cells):
                return _clean(cells[idx].get_text())
    return ""


def _parse_results_table(
    table, hmap: Dict[str, int], lot_type: str, process_hint: str
) -> Dict[str, dict]:
    """Return {rank_str: {lot fields}} — no auction data yet."""
    lots: Dict[str, dict] = {}
    rows = table.find_all("tr")

    for row in rows[1:]:
        cells = row.find_all(["td", "th"])
        if not cells:
            continue

        rank = _get_cell(hmap, cells, "RANK")
        if not rank or rank.upper() == "RANK":
            continue

        farm = _get_cell(
            hmap, cells,
            "FARM/CWS", "FARM / CWS", "FARM", "WINNING FARM/CWS", "WINNING FARM / CWS",
        )
        producer = _get_cell(
            hmap, cells,
            "FARMER/REPRESENTATIVE", "FARMER / REPRESENTATIVE", "FARMER",
        )
        region  = _get_cell(hmap, cells, "REGION")
        process = _get_cell(hmap, cells, "PROCESS") or process_hint
        varietal = _get_cell(hmap, cells, "VARIETY", "VARIETAL", "VARIETIES")
        score_raw = _get_cell(hmap, cells, "SCORE")

        # Weight: modern pages have "WEIGHT (KG)"; old pages have "SIZE" (bag count)
        weight_kg = None
        if "WEIGHT (KG)" in hmap:
            weight_kg = _parse_float(_get_cell(hmap, cells, "WEIGHT (KG)"))
        # Old "SIZE" column is bag count — can't convert without known bag size; leave None

        lots[rank] = {
            "LotRank":     rank,
            "LotType":     lot_type,
            "FarmName":    farm,
            "ProducerName": producer,
            "Region":      region,
            "Process":     process,
            "Varietal":    varietal,
            "WeightKg":    weight_kg,
            "ScoreCoE":    _parse_float(score_raw),
            "PriceUSDPerLb": None,
            "TotalValueUSD": None,
            "BuyerName":   "",
        }

    return lots


def _parse_auction_table(table, hmap: Dict[str, int]) -> Dict[str, dict]:
    """Return {rank_str: {price, total, buyer}}."""
    results: Dict[str, dict] = {}
    rows = table.find_all("tr")

    for row in rows[1:]:
        cells = row.find_all(["td", "th"])
        if not cells:
            continue

        rank = _get_cell(hmap, cells, "RANK", "LOT #", "LOT#", "LOT")
        if not rank or rank.upper() in ("RANK", "LOT #", "LOT", "LOT#"):
            continue

        price_raw = _get_cell(
            hmap, cells,
            "FINAL BID ($/LB)", "FINAL BID", "HIGH BID",
        )
        total_raw  = _get_cell(hmap, cells, "TOTAL VALUE")
        buyer      = _get_cell(hmap, cells, "COMPANY NAME", "HIGH BIDDER(S)", "HIGH BIDDER")

        results[rank] = {
            "PriceUSDPerLb": _parse_float(price_raw),
            "TotalValueUSD": _parse_float(total_raw),
            "BuyerName":    buyer,
        }

    return results


# ---------------------------------------------------------------------------
# Page parser
# ---------------------------------------------------------------------------

def _parse_page(
    soup: BeautifulSoup,
    country: str,
    slug: str,
    year_str: str,
    year: int,
    month_stamp: str,
) -> List[dict]:
    process_hint = _process_hint(slug)
    auction_slug = f"{slug}-{year_str}"

    results_tables: List[tuple] = []   # (table, hmap)
    auction_tables: List[tuple] = []

    for table in soup.find_all("table"):
        hmap = _header_map(table)
        if not hmap or _is_jury_or_commission_table(hmap):
            continue
        if _is_results_table(hmap):
            results_tables.append((table, hmap))
        elif _is_auction_table(hmap):
            auction_tables.append((table, hmap))

    if not results_tables:
        log.warning("%s: no results tables found", auction_slug)
        return []

    all_lots: List[dict] = []
    # Tables arrive in order: COE Results, COE Auction, NW Results, NW Auction
    lot_type_labels = ["COE", "NW"]

    for i, (rt, rt_hmap) in enumerate(results_tables):
        lot_type = lot_type_labels[i] if i < len(lot_type_labels) else f"T{i}"

        results = _parse_results_table(rt, rt_hmap, lot_type, process_hint)
        auction_data: Dict[str, dict] = {}
        if i < len(auction_tables):
            at, at_hmap = auction_tables[i]
            auction_data = _parse_auction_table(at, at_hmap)

        for rank, lot in results.items():
            if rank in auction_data:
                lot.update(auction_data[rank])
            lot.update({
                "AuctionSlug": auction_slug,
                "AuctionYear": year,
                "Country":     country,
                "ScrapedMonth": month_stamp,
            })
            all_lots.append({f: lot.get(f, "") for f in FIELDS})

    return all_lots


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def run(
    month_stamp: str,
    backfill: bool = False,
    country_filter: Optional[str] = None,
    dry_run: bool = False,
) -> List[dict]:
    """
    Scrape CoE auction pages and return lots as list[dict].

    backfill=True   — ignore archive, re-fetch everything
    country_filter  — restrict to a single country (case-insensitive)
    dry_run         — fetch + parse but do not write archive files
    """
    if not dry_run:
        COE_DIR.mkdir(parents=True, exist_ok=True)

    current_year = int(month_stamp[:4])
    cf = country_filter.lower().strip() if country_filter else None

    pages = [
        (country, slug, year_str)
        for country, slug, year_str in AUCTION_PAGES
        if cf is None or country.lower() == cf
    ]

    # First run detection: if the archive is empty, this is a full backfill
    is_first_run = not dry_run and not any(COE_DIR.iterdir()) if COE_DIR.exists() else True
    if is_first_run:
        log.info("coe: archive is empty — running full historical backfill (%d pages)", len(pages))

    to_scrape = []
    for country, slug, year_str in pages:
        year = int(year_str[:4])
        archive_path = COE_DIR / f"{slug}-{year_str}.json"

        # Skip if already archived AND it's a past year AND not forcing backfill
        if not backfill and archive_path.exists() and year < current_year:
            continue

        to_scrape.append((country, slug, year_str, year, archive_path))

    if not to_scrape:
        log.info("coe: all pages up to date — nothing to scrape")
        return []

    log.info(
        "coe: scraping %d/%d pages (%s)",
        len(to_scrape), len(pages),
        "backfill" if (backfill or is_first_run) else "incremental",
    )

    all_lots: List[dict] = []
    skipped = 0
    errors = 0

    for idx, (country, slug, year_str, year, archive_path) in enumerate(to_scrape):
        url = f"{BASE_URL}/{slug}-{year_str}/"
        log.info("coe [%d/%d]: %s", idx + 1, len(to_scrape), url)

        soup = _fetch(url)
        if soup is None:
            skipped += 1
            continue

        lots = _parse_page(soup, country, slug, year_str, year, month_stamp)

        if not lots:
            log.warning("coe: no lots parsed from %s", url)
            errors += 1
        else:
            if not dry_run:
                archive_path.write_text(
                    json.dumps(
                        {"url": url, "scraped_month": month_stamp, "lots": lots},
                        indent=2,
                        default=str,
                    ),
                    encoding="utf-8",
                )
            all_lots.extend(lots)

        time.sleep(0.5)

    log.info(
        "coe: done — %d lots, %d pages skipped (404/error), %d parse failures",
        len(all_lots), skipped, errors,
    )
    return all_lots


# ---------------------------------------------------------------------------
# Standalone CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import csv
    from datetime import date

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-7s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    parser = argparse.ArgumentParser(description="CoE historical scraper")
    parser.add_argument(
        "--month", default=date.today().strftime("%Y-%m"),
        help="Month stamp YYYY-MM (default: current month)",
    )
    parser.add_argument("--backfill", action="store_true", help="Re-fetch all pages")
    parser.add_argument("--country", default=None, help="Scrape one country only")
    parser.add_argument("--dry-run", action="store_true", help="No archive writes")
    args = parser.parse_args()

    rows = run(
        month_stamp=args.month,
        backfill=args.backfill,
        country_filter=args.country,
        dry_run=args.dry_run,
    )

    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    print(f"# {len(rows)} lots", file=sys.stderr)
