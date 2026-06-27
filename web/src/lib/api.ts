type ParamValue = string | number | boolean | undefined | null;

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

// ---------------------------------------------------------------------------
// Response types — mirror FastAPI schemas exactly
// ---------------------------------------------------------------------------

export interface Page<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface FarmSummary {
  id: number;
  slug: string;
  canonical_name: string;
  owner_name: string | null;
  municipality: string | null;
  department: string | null;
  lot_varietal: string | null;
  lot_process: string | null;
  packaging_type: string | null;
  origin_id: number | null;
  country: string | null;
  process_methods: string[] | null;
  varietals: string[] | null;
  source: string | null;
}

export interface FarmFacets {
  origins: string[];
  sources: string[];
  processes: string[];
}

export interface FarmDetail extends FarmSummary {
  altitude_m: number | null;
  cooperative_name: string | null;
  latitude: number | null;
  longitude: number | null;
  flavor_tags: string[] | null;
  importer_ids: Record<string, unknown> | null;
  source_lot_title: string | null;
}

export interface LotRow {
  id: number;
  auction_event_id: number | null;
  farm_id: number | null;
  farm_name: string | null;
  country: string | null;
  year: number | null;
  lot_rank: string | null;
  lot_number: number | null;
  score: number | null;
  process_method: string | null;
  varietal: string[] | null;
  weight_kg: number | null;
  winning_price_usd_per_kg: number | null;
  buyer_name: string | null;
}

export interface LotDetail extends LotRow {
  tasting_notes: string | null;
  flavor_tags: string[] | null;
}

export interface OriginCard {
  id: number;
  country: string;
  region: string | null;
  latitude: number | null;
  longitude: number | null;
  altitude_min_m: number | null;
  altitude_max_m: number | null;
  harvest_start_month: number | null;
  harvest_end_month: number | null;
  dominant_varietals: string[] | null;
  flavor_tags: string[] | null;
  notes: string | null;
}

// ---------------------------------------------------------------------------
// Query param types
// ---------------------------------------------------------------------------

export interface FarmParams extends Record<string, ParamValue> {
  q?: string;
  origin?: string;
  process?: string;
  source?: string;
  sort?: "asc" | "desc";
  page?: number;
  page_size?: number;
}

export interface FarmFacetParams extends Record<string, ParamValue> {
  q?: string;
  origin?: string;
  process?: string;
  source?: string;
}

export interface LotParams extends Record<string, ParamValue> {
  origin?: string;
  year?: number;
  min_score?: number;
  max_score?: number;
  process?: string;
  min_price?: number;
  max_price?: number;
  farm_id?: number;
  page?: number;
  page_size?: number;
}

// ---------------------------------------------------------------------------
// Fetch helper
// ---------------------------------------------------------------------------

type Params = Record<string, ParamValue>;

async function apiFetch<T>(
  path: string,
  params?: Params,
  init?: RequestInit,
): Promise<T> {
  const url = new URL(`${API_URL}${path}`);
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      if (v != null) url.searchParams.set(k, String(v));
    }
  }
  const res = await fetch(url.toString(), {
    next: { revalidate: 3600 },
    ...init,
  });
  if (!res.ok) {
    throw new Error(`BeanBase API ${res.status} at ${path}`);
  }
  return res.json() as Promise<T>;
}

// ---------------------------------------------------------------------------
// Endpoint functions
// ---------------------------------------------------------------------------

export const api = {
  farms: {
    list: (params?: FarmParams) =>
      apiFetch<Page<FarmSummary>>("/farms", params),

    facets: (params?: FarmFacetParams) =>
      apiFetch<FarmFacets>("/farms/facets", params),

    get: (slug: string) =>
      apiFetch<FarmDetail>(`/farms/${encodeURIComponent(slug)}`),
  },

  lots: {
    list: (params?: LotParams) =>
      apiFetch<Page<LotRow>>("/lots", params),

    get: (id: number) =>
      apiFetch<LotDetail>(`/lots/${id}`),
  },

  origins: {
    list: () =>
      apiFetch<OriginCard[]>("/origins"),

    get: (country: string) =>
      apiFetch<OriginCard>(`/origins/${encodeURIComponent(country)}`),
  },
};
