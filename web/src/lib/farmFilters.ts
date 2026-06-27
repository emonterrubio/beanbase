export const FARM_SOURCES = [
  { value: "cup_of_excellence", label: "Cup of Excellence" },
  { value: "cafe_imports", label: "Cafe Imports" },
] as const;

export const FARM_PROCESSES = [
  "Anaerobic",
  "Honey",
  "Natural",
  "Pulped Natural",
  "Semi-Washed",
  "Washed",
  "Wet Hulled",
] as const;

export const FARM_SORT_OPTIONS = [
  { value: "asc", label: "A–Z" },
  { value: "desc", label: "Z–A" },
] as const;

export type FarmSort = (typeof FARM_SORT_OPTIONS)[number]["value"];

export function formatSourceLabel(source: string): string {
  return FARM_SOURCES.find((s) => s.value === source)?.label ?? source;
}

/** Drop an origin filter value if it isn't in the valid list. */
export function sanitizeOriginFilter(
  origin: string,
  validOrigins: string[],
): { origin: string; changed: boolean } {
  if (!origin) return { origin: "", changed: false };
  const match = validOrigins.find((o) => o.toLowerCase() === origin.toLowerCase());
  const resolved = match ?? "";
  return { origin: resolved, changed: resolved !== origin };
}

/** @deprecated Use sanitizeOriginFilter — kept for any legacy callers */
export function sanitizeFarmFilters(
  filters: { origin: string; source: string; process: string },
  facets: { origins: string[]; sources: string[]; processes: string[] },
): { origin: string; source: string; process: string; changed: boolean } {
  const { origin, changed } = sanitizeOriginFilter(filters.origin, facets.origins);
  return {
    origin,
    source: "",
    process: "",
    changed: changed || Boolean(filters.source || filters.process),
  };
}

/** Build visible page numbers with ellipsis for shadcn pagination. */
export function getPaginationRange(
  current: number,
  total: number,
): (number | "ellipsis")[] {
  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1);
  }

  const range: (number | "ellipsis")[] = [1];
  const left = Math.max(2, current - 1);
  const right = Math.min(total - 1, current + 1);

  if (left > 2) range.push("ellipsis");
  for (let i = left; i <= right; i++) range.push(i);
  if (right < total - 1) range.push("ellipsis");
  range.push(total);

  return range;
}
