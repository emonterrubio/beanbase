import Link from "next/link";
import type { FarmSummary } from "@/lib/api";
import { resolveFarmCountry } from "@/lib/farmCountry";
import { CountryBanner } from "./CountryBanner";

export function FarmCard({ farm }: { farm: FarmSummary }) {
  const country = resolveFarmCountry(farm);

  return (
    <Link
      href={`/farms/${farm.slug}`}
      className="group flex flex-col overflow-hidden rounded-card border border-border bg-white transition-shadow hover:shadow-md"
    >
      <CountryBanner country={country} variant="card" />

      <div className="flex flex-col gap-2 p-4">
        <h3 className="line-clamp-2 text-sm font-semibold leading-snug text-text group-hover:text-brand">
          {farm.canonical_name}
        </h3>

        {farm.source && (
          <span className="w-fit rounded-badge bg-cream-100 px-2 py-0.5 text-xs text-muted">
            {farm.source}
          </span>
        )}

        {country && (
          <p className="text-xs text-muted">{country}</p>
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
      </div>
    </Link>
  );
}
