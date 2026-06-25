import type { Metadata } from "next";
import { api } from "@/lib/api";
import { FarmGrid } from "@/components/FarmGrid";
import { SearchBar } from "@/components/SearchBar";
import { FilterChip } from "@/components/FilterChip";
import { Pagination } from "@/components/Pagination";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Farm Explorer" };

const ORIGINS = [
  "Ethiopia", "Colombia", "Guatemala", "Honduras",
  "El Salvador", "Costa Rica", "Brazil", "Peru",
];

type SearchParams = Promise<{ [k: string]: string | string[] | undefined }>;

function str(v: string | string[] | undefined): string {
  return Array.isArray(v) ? (v[0] ?? "") : (v ?? "");
}

export default async function FarmsPage({ searchParams }: { searchParams: SearchParams }) {
  const sp = await searchParams;
  const q      = str(sp.q);
  const origin = str(sp.origin);
  const page   = Math.max(1, Number(sp.page ?? 1));

  const data = await api.farms.list({ q, origin, page, page_size: 24 });

  // params passed down to client components so they can preserve other filters on change
  const currentParams: Record<string, string> = {};
  if (q)      currentParams.q      = q;
  if (origin) currentParams.origin = origin;

  // build hrefBase for pagination (everything except page=)
  const qs = new URLSearchParams(currentParams).toString();
  const hrefBase = `/farms${qs ? `?${qs}&` : "?"}`;

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-text">Farm Explorer</h1>
        <p className="mt-1 text-sm text-muted">
          {data.total.toLocaleString()} farms across 18+ origins
        </p>
      </div>

      {/* Filters */}
      <div className="mb-6 flex flex-col gap-4">
        <SearchBar
          placeholder="Search farm names…"
          defaultValue={q}
          currentParams={currentParams}
        />
        <div className="flex flex-wrap gap-2">
          <span className="self-center text-xs text-muted">Origin:</span>
          {ORIGINS.map((o) => (
            <FilterChip
              key={o}
              label={o}
              param="origin"
              value={o}
              isActive={origin === o}
              currentParams={{ ...currentParams, origin: "" }}
            />
          ))}
        </div>
      </div>

      <FarmGrid farms={data.items} />

      <Pagination page={data.page} pages={data.pages} hrefBase={hrefBase} />
    </div>
  );
}
