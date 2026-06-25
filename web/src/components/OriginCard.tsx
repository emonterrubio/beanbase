import Link from "next/link";
import type { OriginCard as OriginCardData } from "@/lib/api";

const MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

function harvestWindow(start: number | null, end: number | null): string {
  if (!start || !end) return "";
  return `${MONTHS[start - 1]}–${MONTHS[end - 1]}`;
}

export function OriginCard({ origin }: { origin: OriginCardData }) {
  const harvest = harvestWindow(origin.harvest_start_month, origin.harvest_end_month);

  return (
    <Link
      href={`/origins/${encodeURIComponent(origin.country)}`}
      className="group flex flex-col gap-3 rounded-card border border-border bg-white p-5 transition-shadow hover:shadow-md"
    >
      <h3 className="text-base font-semibold text-text group-hover:text-brand">
        {origin.country}
      </h3>

      <dl className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs text-muted">
        {origin.altitude_min_m != null && (
          <>
            <dt>Altitude</dt>
            <dd className="text-right tabular-nums">
              {origin.altitude_min_m}–{origin.altitude_max_m ?? "?"}m
            </dd>
          </>
        )}
        {harvest && (
          <>
            <dt>Harvest</dt>
            <dd className="text-right">{harvest}</dd>
          </>
        )}
      </dl>

      {origin.flavor_tags && origin.flavor_tags.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {origin.flavor_tags.slice(0, 4).map((tag) => (
            <span
              key={tag}
              className="rounded-badge bg-honey-50 px-2 py-0.5 text-xs text-honey-700"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
    </Link>
  );
}
