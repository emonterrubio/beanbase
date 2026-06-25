import Link from "next/link";
import type { FarmSummary } from "@/lib/api";

export function FarmCard({ farm }: { farm: FarmSummary }) {
  return (
    <Link
      href={`/farms/${farm.slug}`}
      className="group flex flex-col gap-3 rounded-card border border-border bg-white p-4 transition-shadow hover:shadow-md"
    >
      <div className="flex items-start justify-between gap-2">
        <h3 className="text-sm font-semibold leading-snug text-text group-hover:text-brand line-clamp-2">
          {farm.canonical_name}
        </h3>
        {farm.source && (
          <span className="shrink-0 rounded-badge bg-cream-100 px-2 py-0.5 text-xs text-muted">
            {farm.source}
          </span>
        )}
      </div>

      {farm.country && (
        <p className="text-xs text-muted">{farm.country}</p>
      )}

      {farm.process_methods && farm.process_methods.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {farm.process_methods.slice(0, 3).map((p) => (
            <span
              key={p}
              className="rounded-badge bg-honey-50 px-2 py-0.5 text-xs text-honey-700"
            >
              {p}
            </span>
          ))}
        </div>
      )}
    </Link>
  );
}
