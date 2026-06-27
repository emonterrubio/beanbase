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

export function matchesFacet(value: string, options: string[]): boolean {
  const lower = value.toLowerCase();
  return options.some((o) => o.toLowerCase() === lower);
}

/** Drop filter values that aren't valid given the other active selections. */
export function sanitizeFarmFilters(
  filters: { origin: string; source: string; process: string },
  facets: { origins: string[]; sources: string[]; processes: string[] },
): { origin: string; source: string; process: string; changed: boolean } {
  const origin =
    filters.origin && matchesFacet(filters.origin, facets.origins) ? filters.origin : "";
  const source =
    filters.source && facets.sources.includes(filters.source) ? filters.source : "";
  const process =
    filters.process && facets.processes.includes(filters.process) ? filters.process : "";
  const changed =
    origin !== filters.origin ||
    source !== filters.source ||
    process !== filters.process;
  return { origin, source, process, changed };
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
