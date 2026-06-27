import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { api } from "@/lib/api";
import { sanitizeFarmFilters, type FarmSort } from "@/lib/farmFilters";
import { FarmFilterSidebar } from "@/components/FarmFilterSidebar";
import { FarmPagination } from "@/components/FarmPagination";
import { FarmSortSelect } from "@/components/FarmSortSelect";
import { FarmTable } from "@/components/FarmTable";
import { SearchBar } from "@/components/SearchBar";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Farm Explorer" };

type SearchParams = Promise<{ [k: string]: string | string[] | undefined }>;

function str(v: string | string[] | undefined): string {
  return Array.isArray(v) ? (v[0] ?? "") : (v ?? "");
}

function buildFarmQuery(params: {
  q: string;
  origin: string;
  source: string;
  process: string;
  sort: FarmSort;
  page?: number;
}): string {
  const qs = new URLSearchParams();
  if (params.q) qs.set("q", params.q);
  if (params.origin) qs.set("origin", params.origin);
  if (params.source) qs.set("source", params.source);
  if (params.process) qs.set("process", params.process);
  if (params.sort !== "asc") qs.set("sort", params.sort);
  if (params.page && params.page > 1) qs.set("page", String(params.page));
  return qs.toString();
}

function resultsTitle(origin: string, source: string, process: string, q: string): string {
  if (origin) return origin;
  if (q) return `Results for "${q}"`;
  return "All farms";
}

export default async function FarmsPage({ searchParams }: { searchParams: SearchParams }) {
  const sp = await searchParams;
  const q = str(sp.q);
  let origin = str(sp.origin);
  let source = str(sp.source);
  let process = str(sp.process);
  const sortRaw = str(sp.sort);
  const sort: FarmSort = sortRaw === "desc" ? "desc" : "asc";
  const page = Math.max(1, Number(sp.page ?? 1));

  const facets = await api.farms.facets({ q, origin, source, process }).catch(() => ({
    origins: [] as string[],
    sources: [] as string[],
    processes: [] as string[],
  }));

  const sanitized = sanitizeFarmFilters({ origin, source, process }, facets);
  if (sanitized.changed) {
    const query = buildFarmQuery({
      q,
      origin: sanitized.origin,
      source: sanitized.source,
      process: sanitized.process,
      sort,
    });
    redirect(query ? `/farms?${query}` : "/farms");
  }

  origin = sanitized.origin;
  source = sanitized.source;
  process = sanitized.process;

  const data = await api.farms.list({
    q,
    origin,
    source,
    process,
    sort,
    page,
    page_size: 24,
  });

  const currentParams: Record<string, string> = {};
  if (q) currentParams.q = q;
  if (origin) currentParams.origin = origin;
  if (source) currentParams.source = source;
  if (process) currentParams.process = process;
  if (sort !== "asc") currentParams.sort = sort;

  const qs = new URLSearchParams(currentParams).toString();
  const hrefBase = `/farms${qs ? `?${qs}&` : "?"}`;

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="flex flex-col gap-8 lg:flex-row lg:items-start">
        {/* Sidebar filters */}
        <div className="w-full shrink-0 lg:sticky lg:top-24 lg:w-60 xl:w-64">
          <FarmFilterSidebar
            availableOrigins={facets.origins}
            availableSources={facets.sources}
            availableProcesses={facets.processes}
            origin={origin}
            source={source}
            process={process}
            searchQuery={q}
            sort={sort}
          />
        </div>

        {/* Main results */}
        <div className="min-w-0 flex-1">
          <SearchBar
            placeholder="Search farm names…"
            defaultValue={q}
            currentParams={currentParams}
          />

          <div className="mt-6 mb-5 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h1 className="text-xl font-bold text-text">
                {resultsTitle(origin, source, process, q)}
              </h1>
              <p className="mt-0.5 text-sm text-muted">
                {data.total.toLocaleString()} farm{data.total === 1 ? "" : "s"} found
              </p>
            </div>
            <FarmSortSelect
              sort={sort}
              searchQuery={q}
              origin={origin}
              source={source}
              process={process}
            />
          </div>

          <FarmTable farms={data.items} />

          <FarmPagination page={data.page} pages={data.pages} hrefBase={hrefBase} />
        </div>
      </div>
    </div>
  );
}
