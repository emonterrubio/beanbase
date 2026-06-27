"""
Parse importer lot titles (Cafe Imports) into farm name + owner.

Importer lot strings follow a loose convention (specific → general):

  [Producer / micro-region] - [Farm] - [Municipality] - [Department] -
  [Varietal] - [Process] (Packaging)

Examples:
  "Area 18 - Finca Santa Barbara - Timbio - Cauca - Pink Bourbon - Oxidation Washed (GrainPro)"
    → farm="Finca Santa Barbara", owner="Area 18"

  "Daniel Mauricio Bolanos Zuniga - Finca El Placer - San Agustin - Huila - Caturra ..."
    → farm="Finca El Placer", owner="Daniel Mauricio Bolanos Zuniga"

  "Natural - Fazenda Sertão - Yellow Bourbon (SC Bags)"
    → farm="Fazenda Sertão", owner=None
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

# Trailing packaging / contract markers
_PACKAGING_RE = re.compile(
    r"\s*[\(\{](?:GrainPro|SC\s*Bags|Bags|ORG|Vac\s*Pack|Ecotact|Jute\s*Bag\s*Only)[\)\}]\s*",
    re.IGNORECASE,
)

# Explicit estate markers — prefer these over loose geographic prefixes
_EXPLICIT_FARM_RE = re.compile(
    r"^(?:finca|fazenda|hacienda|rancho|estate|granja)\b",
    re.IGNORECASE,
)

_PROCESS_PREFIXES = (
    "natural",
    "washed",
    "honey",
    "anaerobic",
    "pulped",
    "semi",
    "double",
    "fully",
    "experimental",
    "oxidation",
    "thermal",
    "carbonic",
    "mwp",
)

_PROCESS_KEYWORDS_RE = re.compile(
    r"\b(?:natural|washed|honey|anaerobic|oxidation|fermentation|maceration|"
    r"pulped|semi[- ]washed|double|experimental|thermal|carbonic|"
    r"perla\s+negra|alma\s+negra|yellow\s+diamond|black\s+diamond|"
    r"double\s+diamond|white\s+honey|red\s+honey|yellow\s+honey)\b",
    re.IGNORECASE,
)

# Known botanical varieties (lowercase keys)
_VARIETAL_TERMS = frozenset(
    {
        "gesha",
        "geisha",
        "caturra",
        "catuai",
        "catuaí",
        "bourbon",
        "pink bourbon",
        "yellow bourbon",
        "red bourbon",
        "striped red bourbon",
        "castillo",
        "colombia",
        "pacamara",
        "typica",
        "sl-28",
        "sl-34",
        "maragogype",
        "peaberry",
        "obata",
        "villa sarchí",
        "villa sarchi",
        "sarchimor",
        "yellow catuai",
        "red catuai",
        "red diabolo",
        "yellow obata",
        "mundo novo",
        "parainema",
        "java",
        "ruiru 11",
        "batian",
    }
)

# Colombian departments commonly appearing in lot titles
_CO_DEPARTMENTS = frozenset(
    {
        "cauca",
        "huila",
        "nariño",
        "narino",
        "tolima",
        "antioquia",
        "caldas",
        "risaralda",
        "quindio",
        "quindío",
        "valle del cauca",
        "santander",
        "magdalena",
        "boyaca",
        "boyacá",
        "caquetá",
        "caqueta",
    }
)

# Costa Rica / Central America regions that appear as state-like segments
_OTHER_REGIONS = frozenset(
    {
        "minas gerais",
        "la paz",
        "pitalito",
        "palestina",
        "acevedo",
        "caldono",
        "sotara",
        "sotará",
    }
)

_PRODUCER_HINTS = (
    "micromill",
    "mill",
    "brothers",
    "area ",
    "sector ",
    "asociacion",
    "asociación",
    "cooperativa",
    "cooperative",
    "program",
    "argcafee",
)

_ORG_KEYWORDS = (
    "asociacion",
    "asociación",
    "cooperativa",
    "cooperative",
    "program",
    "argcafee",
    "apca",
    "asocafe",
    "s.a.",
    "s.a",
    " ltd",
    " inc",
)


@dataclass(frozen=True)
class ParsedFarmName:
    farm_name: str
    owner_name: Optional[str] = None
    municipality: Optional[str] = None
    department: Optional[str] = None
    varietal: Optional[str] = None
    process_hint: Optional[str] = None
    packaging_type: Optional[str] = None


def _extract_packaging(raw: str) -> Optional[str]:
    m = _PACKAGING_RE.search(raw)
    if not m:
        return None
    inner = m.group(0).strip().strip("({})").strip()
    return f"({inner})"


def _clean(raw: str) -> str:
    return _PACKAGING_RE.sub("", raw).strip()


def _expand_merged_segments(parts: List[str]) -> List[str]:
    """Re-split segments where dashes were omitted between fields."""
    expanded: List[str] = []
    for part in parts:
        if "-" in part and not _is_varietal_segment(part):
            head = part.split("-", 1)[0].strip()
            if _is_explicit_farm(head) or _looks_like_cooperative(head):
                sub = [s.strip() for s in re.split(r"\s*-\s*", part) if s.strip()]
                expanded.extend(sub)
                continue
        expanded.append(part)
    return expanded


def _split_parts(raw: str) -> List[str]:
    parts = [p.strip() for p in _clean(raw).split(" - ") if p.strip()]
    return _expand_merged_segments(parts)


def _is_explicit_farm(part: str) -> bool:
    return bool(_EXPLICIT_FARM_RE.match(part.strip()))


def _is_process_segment(part: str) -> bool:
    lower = part.lower()
    if any(lower.startswith(p) for p in _PROCESS_PREFIXES):
        return True
    return bool(_PROCESS_KEYWORDS_RE.search(part))


def _is_varietal_segment(part: str) -> bool:
    lower = part.lower().strip()
    if lower in _VARIETAL_TERMS:
        return True
    if "&" in lower:
        tokens = [t.strip() for t in re.split(r"\s*&\s*", lower)]
        if tokens and all(t in _VARIETAL_TERMS or "bourbon" in t or "catuai" in t for t in tokens):
            return True
    if re.search(r"\bbourbon\b", lower):
        return True
    if re.match(r"^[hf]\d+$", lower):  # H1, F5 lot codes used as varietal slot
        return True
    if re.match(r"^(?:sl|pk)-?\d+$", lower, re.I):
        return True
    return False


def _is_department_segment(part: str) -> bool:
    lower = part.lower().strip()
    return lower in _CO_DEPARTMENTS or lower in _OTHER_REGIONS


def _is_municipality_segment(part: str) -> bool:
    """Town name between farm and department — short, not a varietal/process/farm."""
    if _is_explicit_farm(part) or _is_process_segment(part) or _is_varietal_segment(part):
        return False
    if _is_department_segment(part):
        return False
    if any(kw in part.lower() for kw in _ORG_KEYWORDS):
        return False
    words = part.split()
    return 1 <= len(words) <= 3


def _strip_trailing_metadata(parts: List[str]) -> Tuple[List[str], dict]:
    """
    Peel varietal, process, department, and municipality off the end.

    Returns the leading segments plus any metadata recovered from the tail.
    """
    remaining = list(parts)
    meta: dict = {
        "municipality": None,
        "department": None,
        "varietal": None,
        "process_hint": None,
    }

    while len(remaining) > 1:
        tail = remaining[-1]

        if _is_process_segment(tail):
            meta["process_hint"] = tail
            remaining.pop()
            continue

        if _is_varietal_segment(tail):
            meta["varietal"] = tail
            remaining.pop()
            continue

        if _is_department_segment(tail):
            meta["department"] = tail
            remaining.pop()
            continue

        if meta["department"] and _is_municipality_segment(tail):
            meta["municipality"] = tail
            remaining.pop()
            continue

        break

    return remaining, meta


def _geo_from_core_after_farm(
    core: List[str], farm_idx: int
) -> Tuple[Optional[str], Optional[str]]:
    """Geo segments between farm name and varietal/process in the lot title."""
    geo = [
        p
        for p in core[farm_idx + 1 :]
        if not _is_varietal_segment(p) and not _is_process_segment(p)
    ]
    if len(geo) >= 2:
        return geo[0], geo[-1]
    if len(geo) == 1:
        if _is_department_segment(geo[0]):
            return None, geo[0]
        return geo[0], None
    return None, None


def _merge_geo(
    meta: dict, core: List[str], farm_idx: Optional[int]
) -> Tuple[Optional[str], Optional[str]]:
    municipality = meta.get("municipality")
    department = meta.get("department")
    if farm_idx is not None:
        core_muni, core_dept = _geo_from_core_after_farm(core, farm_idx)
        municipality = municipality or core_muni
        department = department or core_dept
    return municipality, department


def _looks_like_cooperative(part: str) -> bool:
    lower = part.lower()
    return any(kw in lower for kw in _ORG_KEYWORDS)


def _is_producer_prefix(part: str) -> bool:
    """Leading segment before a Finca/Fazenda — person, mill, or micro-region."""
    if _is_process_segment(part):
        return False
    lower = part.lower()
    if any(h in lower for h in _PRODUCER_HINTS):
        return True
    if _looks_like_cooperative(part):
        return False
    if re.match(r"^area\s+\d+", lower):
        return True
    # Person names: 2+ words; allow & for couples; digits ok in "Area 18" handled above
    words = part.replace("&", " ").split()
    if len(words) >= 2 and not _is_varietal_segment(part):
        return True
    return False


def parse_importer_lot_name(raw: str) -> ParsedFarmName:
    """Split a Cafe Imports offering title into farm, owner, and optional tail metadata."""
    text = (raw or "").strip()
    if not text:
        return ParsedFarmName(farm_name="")

    packaging = _extract_packaging(text)
    parts = _split_parts(text)
    if not parts:
        return ParsedFarmName(farm_name=text, packaging_type=packaging)

    if len(parts) == 1:
        return ParsedFarmName(farm_name=parts[0], packaging_type=packaging)

    core, meta = _strip_trailing_metadata(parts)

    # Locate explicit Finca / Fazenda segment
    farm_idx = next((i for i, p in enumerate(core) if _is_explicit_farm(p)), None)

    if farm_idx is not None:
        farm_name = core[farm_idx]
        owner_name: Optional[str] = None
        if farm_idx > 0 and _is_producer_prefix(core[0]):
            owner_name = core[0]
        municipality, department = _merge_geo(meta, core, farm_idx)
        return ParsedFarmName(
            farm_name=farm_name,
            owner_name=owner_name,
            municipality=municipality,
            department=department,
            varietal=meta.get("varietal"),
            process_hint=meta.get("process_hint"),
            packaging_type=packaging,
        )

    # Process-first: "Natural - Fazenda ..."
    if _is_process_segment(core[0]) and len(core) > 1:
        farm_candidate = core[1]
        if _is_explicit_farm(farm_candidate) or not _is_varietal_segment(farm_candidate):
            return ParsedFarmName(
                farm_name=farm_candidate,
                varietal=meta.get("varietal"),
                process_hint=core[0],
                packaging_type=packaging,
            )

    # Cooperative / program titles (no finca marker)
    if _looks_like_cooperative(core[0]):
        farm_parts = [core[0]]
        if len(core) > 1 and (
            _looks_like_cooperative(core[1]) or "program" in core[1].lower()
        ):
            farm_parts.append(core[1])
        elif len(core) > 1 and not _is_department_segment(core[1]):
            farm_parts.append(core[1])
        return ParsedFarmName(farm_name=" - ".join(farm_parts), packaging_type=packaging)

    # Fallback: first segment is the best label
    return ParsedFarmName(
        farm_name=core[0],
        owner_name=core[1] if len(core) > 1 and _is_producer_prefix(core[0]) else None,
        municipality=meta.get("municipality"),
        department=meta.get("department"),
        varietal=meta.get("varietal"),
        process_hint=meta.get("process_hint"),
        packaging_type=packaging,
    )
