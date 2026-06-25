import type { Metadata } from "next";
import { api } from "@/lib/api";
import { LotTable } from "@/components/LotTable";
import { FilterChip } from "@/components/FilterChip";
import { Pagination } from "@/components/Pagination";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Auction History" };

const ORIGINS = [
  "Ethiopia", "Colombia", "Guatemala", "Honduras",
  "El Salvador", "Costa Rica", "Brazil", "Peru", "Bolivia", "Rwanda",
];

const YEARS = Array.from({ length: 2026 - 1999 + 1 }, (_, i) => 2026 - i);

type SearchParams = Promise<{ [k: string]: string | string[] | undefined }>;

function str(v: string | string[] | undefined): string {
  return Array.isArray(v) ? (v[0] ?? "") : (v ?? "");
}

export default async function AuctionsPage({ searchParams }: { searchParams: SearchParams }) {
  const sp        = await searchParams;
  const origin    = str(sp.origin);
  const yearStr   = str(sp.year);
  const minScore  = str(sp.min_score);
  const page      = Math.max(1, Number(sp.page ?? 1));

  const data = await api.lots.list({
    origin:    origin    || undefined,
    year:      yearStr   ? Number(yearStr)   : undefined,
    min_score: minScore  ? Number(minScore)  : undefined,
    page,
    page_size: 50,
  });

  const currentParams: Record<string, string> = {};
  if (origin)   currentParams.origin    = origin;
  if (yearStr)  currentParams.year      = yearStr;
  if (minScore) currentParams.min_score = minScore;

  const qs = new URLSearchParams(currentParams).toString();
  const hrefBase = `/auctions${qs ? `?${qs}&` : "?"}`;

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-text">Auction History</h1>
        <p className="mt-1 text-sm text-muted">
          {data.total.toLocaleString()} lots · Cup of Excellence 1999–2026
        </p>
      </div>

      {/* Filters */}
      <div className="mb-6 flex flex-col gap-4">
        {/* Origin chips */}
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs text-muted">Origin:</span>
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

        {/* Score chips */}
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs text-muted">Min score:</span>
          {[["90+", "90"], ["87+", "87"], ["84+", "84"]].map(([label, value]) => (
            <FilterChip
              key={value}
              label={label}
              param="min_score"
              value={value}
              isActive={minScore === value}
              currentParams={{ ...currentParams, min_score: "" }}
            />
          ))}
        </div>

        {/* Year chips — show last 10 */}
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs text-muted">Year:</span>
          {YEARS.slice(0, 10).map((y) => (
            <FilterChip
              key={y}
              label={String(y)}
              param="year"
              value={String(y)}
              isActive={yearStr === String(y)}
              currentParams={{ ...currentParams, year: "" }}
            />
          ))}
        </div>
      </div>

      <LotTable lots={data.items} />
      <Pagination page={data.page} pages={data.pages} hrefBase={hrefBase} />
    </div>
  );
}
