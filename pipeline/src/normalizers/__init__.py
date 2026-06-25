import re


def slugify(text: str) -> str:
    """Convert arbitrary text to a URL-safe slug."""
    s = re.sub(r"[^\w\s-]", "", (text or "").lower().strip())
    s = re.sub(r"[-\s]+", "-", s)
    return s.strip("-")[:250]
