"""
Canonical process method taxonomy for BeanBase.

All scrapers feed raw process strings here before DB writes.
"""

import re
from typing import Optional

# Maps lowercase raw strings → canonical display value
_CANONICAL: dict = {
    # Washed / Wet
    "washed":                   "Washed",
    "fully washed":              "Washed",
    "wet process":               "Washed",
    "wet processed":             "Washed",
    "wet":                       "Washed",
    # Natural / Dry
    "natural":                   "Natural",
    "dry process":               "Natural",
    "dry processed":             "Natural",
    "sun-dried":                 "Natural",
    "sun dried":                 "Natural",
    # Honey
    "honey":                     "Honey",
    "honey process":             "Honey",
    "yellow honey":              "Yellow Honey",
    "red honey":                 "Red Honey",
    "black honey":               "Black Honey",
    "white honey":               "White Honey",
    # Pulped Natural
    "pulped natural":            "Pulped Natural",
    "pulped naturals":           "Pulped Natural",
    # Semi-Washed
    "semi-washed":               "Semi-Washed",
    "semi washed":               "Semi-Washed",
    # Wet Hulled (Giling Basah)
    "wet hulled":                "Wet Hulled",
    "wet-hulled":                "Wet Hulled",
    "giling basah":              "Wet Hulled",
    # Anaerobic
    "anaerobic":                 "Anaerobic",
    "anaerobic natural":         "Anaerobic Natural",
    "anaerobic washed":          "Anaerobic Washed",
    "anaerobic fermentation":    "Anaerobic",
    "double anaerobic":          "Double Anaerobic",
    # Carbonic Maceration
    "carbonic maceration":       "Carbonic Maceration",
    "co2 maceration":            "Carbonic Maceration",
    # Thermal Shock
    "thermal shock":             "Thermal Shock",
    # Decaf
    "decaf":                     "Decaf",
    "decaffeinated":             "Decaf",
    "co2 decaf":                 "Decaf (CO2)",
    "swiss water":               "Decaf (Swiss Water)",
    "swiss water process":       "Decaf (Swiss Water)",
    "swiss water decaf":         "Decaf (Swiss Water)",
    "mountain water":            "Decaf (Mountain Water)",
    # Misc
    "experimental":              "Experimental",
}


def normalize(raw: Optional[str]) -> str:
    """Return canonical process method string, or title-cased original if unknown."""
    if not raw:
        return ""
    key = re.sub(r"\s+", " ", raw.lower().strip())
    return _CANONICAL.get(key, raw.strip().title())


def normalize_list(raw: Optional[str]) -> list:
    """Split a comma-separated process string and normalize each part."""
    if not raw:
        return []
    return [normalize(p.strip()) for p in raw.split(",") if p.strip()]
