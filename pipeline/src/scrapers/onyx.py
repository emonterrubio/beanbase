"""
Onyx Coffee Lab wholesale catalog scraper (Shopify JSON API).
Exposes run(month_stamp) -> list[dict] for the monthly orchestrator.
Also runnable standalone: python3 -m scrapers.onyx
"""

import sys

import requests

URL = "https://onyxcoffeelab.com/collections/wholesale-coffee/products.json"
PAGE_LIMIT = 250

TAG_FIELDS = ("origin", "process", "method", "type", "profile", "caffeine")

PROCESS_NORM = {
    "washed":           "Washed",
    "natural":          "Natural",
    "honey":            "Honey",
    "dry washed":       "Dry Washed",
    "anaerobic":        "Anaerobic",
    "pulped natural":   "Pulped Natural",
    "anaerobic natural": "Anaerobic Natural",
    "anaerobic washed": "Anaerobic Washed",
    "white honey":      "White Honey",
    "yellow honey":     "Yellow Honey",
    "innoculated":      "Inoculated",
}

FIELDS = [
    "ProductID", "VariantID", "Title", "Handle", "ProductType",
    "VariantTitle", "SKU", "Price", "CompareAtPrice", "Available", "Grams",
    "Origin", "Process", "Method", "Type", "Profile", "Caffeine",
    "PublishedAt", "UpdatedAt", "ScrapedMonth",
]


def _norm_process(raw: str) -> str:
    return PROCESS_NORM.get(raw.lower().strip(), raw.strip().title())


def _parse_tags(tags: list[str]) -> dict[str, str]:
    result: dict[str, list[str]] = {f: [] for f in TAG_FIELDS}
    for tag in tags:
        for field in TAG_FIELDS:
            if tag.lower().startswith(f"{field}:"):
                result[field].append(tag[len(field) + 1:].strip())
    out = {}
    for field, values in result.items():
        if field == "process":
            out[field] = " / ".join(_norm_process(v) for v in values)
        else:
            out[field] = " / ".join(values)
    return out


def _fetch_all(url: str) -> list[dict]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }
    products: list[dict] = []
    page = 1
    while True:
        resp = requests.get(url, headers=headers,
                            params={"limit": PAGE_LIMIT, "page": page}, timeout=30)
        resp.raise_for_status()
        batch = resp.json().get("products", [])
        if not batch:
            break
        products.extend(batch)
        if len(batch) < PAGE_LIMIT:
            break
        page += 1
    return products


def _flatten(products: list[dict], month_stamp: str) -> list[dict]:
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
            rows.append({
                **base,
                "VariantID":      str(variant["id"]),
                "VariantTitle":   variant.get("title", ""),
                "SKU":            variant.get("sku", ""),
                "Price":          variant.get("price", ""),
                "CompareAtPrice": variant.get("compare_at_price") or "",
                "Available":      str(variant.get("available", "")).lower(),
                "Grams":          str(variant.get("grams", "")),
                "ScrapedMonth":   month_stamp,
            })
    return rows


def run(month_stamp: str, url: str = URL) -> list[dict]:
    products = _fetch_all(url)
    return _flatten(products, month_stamp)


if __name__ == "__main__":
    import csv
    from datetime import date

    month = date.today().strftime("%Y-%m")
    rows = run(month)
    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    print(f"# {len(rows)} rows", file=sys.stderr)
