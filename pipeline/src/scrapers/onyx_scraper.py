"""
Onyx Coffee Lab wholesale catalog scraper.
Reads the Shopify products.json endpoint and flattens products × variants
into one row per variant, with tag-derived metadata normalized.

Usage:
    python pipeline/src/scrapers/onyx_scraper.py
    python pipeline/src/scrapers/onyx_scraper.py --out custom.csv
    python pipeline/src/scrapers/onyx_scraper.py --json
    python pipeline/src/scrapers/onyx_scraper.py --all-pages

Outputs default to pipeline/data/onyx_YYYY-MM.csv (and optional .json sidecar).
"""

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import requests

BASE_URL = "https://onyxcoffeelab.com/collections/wholesale-coffee/products.json"
PAGE_LIMIT = 250  # Shopify max per page

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent.parent / "data"

# Tag prefixes to extract into dedicated columns
TAG_FIELDS = ("origin", "process", "method", "type", "profile", "caffeine")

# Canonical process names (lowercase key → display value)
PROCESS_NORM = {
    "washed":         "Washed",
    "natural":        "Natural",
    "honey":          "Honey",
    "dry washed":     "Dry Washed",
    "anaerobic":      "Anaerobic",
    "pulped natural": "Pulped Natural",
}


def _norm_process(raw: str) -> str:
    return PROCESS_NORM.get(raw.lower().strip(), raw.strip().title())


def _parse_tags(tags: list[str]) -> dict[str, str]:
    """Extract prefix:value pairs from a Shopify tags list."""
    result: dict[str, list[str]] = {f: [] for f in TAG_FIELDS}
    for tag in tags:
        for field in TAG_FIELDS:
            prefix = f"{field}:"
            if tag.lower().startswith(prefix):
                value = tag[len(prefix):].strip()
                result[field].append(value)
    out = {}
    for field, values in result.items():
        if field == "process":
            out[field] = " / ".join(_norm_process(v) for v in values)
        else:
            out[field] = " / ".join(values)
    return out


def fetch_page(url: str, page: int) -> list[dict]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }
    params = {"limit": PAGE_LIMIT, "page": page}
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("products", [])


def flatten_to_rows(products: list[dict], month_stamp: str) -> list[dict]:
    rows = []
    for product in products:
        tags = _parse_tags(product.get("tags", []))
        base = {
            "ProductID":   str(product["id"]),
            "Title":       product.get("title", ""),
            "Handle":      product.get("handle", ""),
            "ProductType": product.get("product_type", ""),
            "Origin":      tags["origin"],
            "Process":     tags["process"],
            "Method":      tags["method"],
            "Type":        tags["type"],
            "Profile":     tags["profile"],
            "Caffeine":    tags["caffeine"],
            "PublishedAt": (product.get("published_at") or "")[:10],
            "UpdatedAt":   (product.get("updated_at") or "")[:10],
        }
        for variant in product.get("variants", []):
            row = {
                **base,
                "VariantID":      str(variant["id"]),
                "VariantTitle":   variant.get("title", ""),
                "SKU":            variant.get("sku", ""),
                "Price":          variant.get("price", ""),
                "CompareAtPrice": variant.get("compare_at_price") or "",
                "Available":      str(variant.get("available", "")).lower(),
                "Grams":          str(variant.get("grams", "")),
                "ScrapedMonth":   month_stamp,
            }
            rows.append(row)
    return rows


OUTPUT_FIELDS = [
    "ProductID", "VariantID", "Title", "Handle", "ProductType",
    "VariantTitle", "SKU", "Price", "CompareAtPrice", "Available", "Grams",
    "Origin", "Process", "Method", "Type", "Profile", "Caffeine",
    "PublishedAt", "UpdatedAt", "ScrapedMonth",
]


def write_csv(rows: list[dict], path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"CSV  → {path}  ({len(rows)} rows)")


def write_json(rows: list[dict], path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"JSON → {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Onyx Coffee Lab wholesale catalog")
    parser.add_argument("--out", help="Output CSV path (default: pipeline/data/onyx_YYYY-MM.csv)")
    parser.add_argument("--json", action="store_true", help="Also write a JSON sidecar")
    parser.add_argument("--url", default=BASE_URL, help="Override the products.json URL")
    parser.add_argument("--all-pages", action="store_true",
                        help="Paginate until empty page (default: single request with limit=250)")
    args = parser.parse_args()

    month_stamp = date.today().strftime("%Y-%m")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = Path(args.out) if args.out else DATA_DIR / f"onyx_{month_stamp}.csv"
    json_path = csv_path.with_suffix(".json")

    all_products: list[dict] = []

    if args.all_pages:
        page = 1
        while True:
            print(f"Fetching page {page} …")
            batch = fetch_page(args.url, page)
            if not batch:
                break
            all_products.extend(batch)
            if len(batch) < PAGE_LIMIT:
                break
            page += 1
    else:
        print(f"Fetching {args.url} (limit={PAGE_LIMIT}) …")
        all_products = fetch_page(args.url, page=1)

    if not all_products:
        sys.exit("ERROR: No products returned — check the URL or collection slug.")

    print(f"Flattening {len(all_products)} products into variant rows …")
    rows = flatten_to_rows(all_products, month_stamp)

    write_csv(rows, csv_path)
    if args.json:
        write_json(rows, json_path)

    process_counts = Counter(r["Process"] for r in rows if r["Process"])
    origin_counts  = Counter(
        o for r in rows for o in r["Origin"].split(" / ") if o
    )
    available = sum(1 for r in rows if r["Available"] == "true")

    print(f"\nSummary — {len(all_products)} products → {len(rows)} variant rows:")
    print(f"  Available:  {available}/{len(rows)}")
    print(f"  By Process: {dict(process_counts.most_common(8))}")
    print(f"  By Origin:  {dict(origin_counts.most_common(8))}")


if __name__ == "__main__":
    main()
