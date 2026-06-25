import type { FarmSummary } from "@/lib/api";
import { FarmCard } from "./FarmCard";

export function FarmGrid({ farms }: { farms: FarmSummary[] }) {
  if (farms.length === 0) {
    return (
      <p className="py-12 text-center text-sm text-muted">
        No farms found. Try adjusting your filters.
      </p>
    );
  }
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {farms.map((farm) => (
        <FarmCard key={farm.id} farm={farm} />
      ))}
    </div>
  );
}
