import type { FarmSummary } from "@/lib/api";

export function farmCell(value: string | null | undefined): string {
  return value?.trim() ? value : "—";
}

export function displayVarietal(farm: FarmSummary): string {
  if (farm.lot_varietal) return farm.lot_varietal;
  if (farm.varietals?.length) return farm.varietals.join(", ");
  return "—";
}

export function displayProcess(farm: FarmSummary): string {
  if (farm.lot_process) return farm.lot_process;
  if (farm.process_methods?.length) return farm.process_methods.join(", ");
  return "—";
}

export const LOT_TITLE_FIELDS = [
  { key: "owner_name", label: "Producer / Micro-Region" },
  { key: "municipality", label: "Municipality" },
  { key: "department", label: "Department" },
  { key: "lot_varietal", label: "Varietal" },
  { key: "lot_process", label: "Process" },
  { key: "packaging_type", label: "Packaging" },
] as const;

export function lotTitleValue(
  farm: FarmSummary,
  key: (typeof LOT_TITLE_FIELDS)[number]["key"]
): string {
  switch (key) {
    case "owner_name":
      return farmCell(farm.owner_name);
    case "municipality":
      return farmCell(farm.municipality);
    case "department":
      return farmCell(farm.department);
    case "lot_varietal":
      return displayVarietal(farm);
    case "lot_process":
      return displayProcess(farm);
    case "packaging_type":
      return farmCell(farm.packaging_type);
  }
}

export function hasLotTitleData(farm: FarmSummary): boolean {
  return (
    Boolean(farm.owner_name?.trim()) ||
    Boolean(farm.municipality?.trim()) ||
    Boolean(farm.department?.trim()) ||
    Boolean(farm.lot_varietal?.trim()) ||
    Boolean(farm.lot_process?.trim()) ||
    Boolean(farm.packaging_type?.trim())
  );
}
