import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { api } from "@/lib/api";
import { sanitizeOriginFilter, type FarmSort } from "@/lib/farmFilters";
import { FarmOriginsNav } from "@/components/FarmOriginsNav";
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
  sort: FarmSort;
  page?: number;
}): string {
  const qs = new URLSearchParams();
  if (params.q) qs.set("q", params.q);
  if (params.origin) qs.set("origin", params.origin);
  if (params.sort !== "asc") qs.set("sort", params.sort);
  if (params.page && params.page > 1) qs.set("page", String(params.page));
  return qs.toString();
}

function resultsTitle(origin: string, q: string): string {
  if (origin) return origin;
  if (q) return `Results for "${q}"`;
  return "All farms";
}

async function loadOriginCountries(): Promise<string[]> {
  const [originRecords, farmFacets] = await Promise.all([
    api.origins.list().catch(() => []),
    api.farms.facets({}).catch(() => ({ origins: [] as string[] })),
  ]);

  const countries = new Set<string>();
  for (const o of originRecords) {
    if (!o.region) countries.add(o.country);
  }
  for (const o of farmFacets.origins) {
    countries.add(o);
  }

  return [...countries].sort((a, b) => a.localeCompare(b));
}

export default async function FarmsPage({ searchParams }: { searchParams: SearchParams }) {
  const sp = await searchParams;
  const q = str(sp.q);
  let origin = str(sp.origin);
  const sortRaw = str(sp.sort);
  const sort: FarmSort = sortRaw === "desc" ? "desc" : "asc";
  const page = Math.max(1, Number(sp.page ?? 1));

  const allOrigins = await loadOriginCountries();

  const sanitized = sanitizeOriginFilter(origin, allOrigins);
  if (sanitized.changed || str(sp.source) || str(sp.process)) {
    const query = buildFarmQuery({
      q,
      origin: sanitized.origin,
      sort,
    });
    redirect(query ? `/farms?${query}` : "/farms");
  }

  origin = sanitized.origin;

  const data = await api.farms.list({
    q,
    origin,
    sort,
    page,
    page_size: 24,
  });

  const currentParams: Record<string, string> = {};
  if (q) currentParams.q = q;
  if (origin) currentParams.origin = origin;
  if (sort !== "asc") currentParams.sort = sort;

  const qs = new URLSearchParams(currentParams).toString();
  const hrefBase = `/farms${qs ? `?${qs}&` : "?"}`;

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="flex flex-col gap-8 lg:flex-row lg:items-start">
        <div className="w-full shrink-0 lg:sticky lg:top-24 lg:w-52 xl:w-56">
          <FarmOriginsNav
            origins={allOrigins}
            selectedOrigin={origin}
            searchQuery={q}
            sort={sort}
          />
        </div>

        <div className="min-w-0 flex-1">
          <SearchBar
            placeholder="Search farm names…"
            defaultValue={q}
            currentParams={currentParams}
          />

          <div className="mt-6 mb-5 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h1 className="text-xl font-bold text-text">
                {resultsTitle(origin, q)}
              </h1>
              <p className="mt-0.5 text-sm text-muted">
                {data.total.toLocaleString()} farm{data.total === 1 ? "" : "s"} found
              </p>
            </div>
            <FarmSortSelect sort={sort} searchQuery={q} origin={origin} />
          </div>

          <FarmTable farms={data.items} />

          <FarmPagination page={data.page} pages={data.pages} hrefBase={hrefBase} />
        </div>
      </div>
    </div>
  );
}
