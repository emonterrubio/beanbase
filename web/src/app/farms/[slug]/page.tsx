import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { api } from "@/lib/api";
import { CountryBanner } from "@/components/CountryBanner";
import { LotTable } from "@/components/LotTable";
import { ScoreBadge } from "@/components/ScoreBadge";

type Params = Promise<{ slug: string }>;

export async function generateStaticParams() {
  try {
    const pages = await Promise.all(
      [1, 2, 3, 4, 5].map((page) => api.farms.list({ page, page_size: 100 }))
    );
    return pages.flatMap((d) => d.items.map((f) => ({ slug: f.slug })));
  } catch {
    return [];
  }
}

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { slug } = await params;
  try {
    const farm = await api.farms.get(slug);
    const title = `${farm.canonical_name}${farm.country ? ` — ${farm.country}` : ""} | BeanBase`;
    const description = `${farm.canonical_name} is a specialty coffee farm${farm.country ? ` in ${farm.country}` : ""}. Explore auction history, scores, and lot data on BeanBase.`;
    return {
      title,
      description,
      openGraph: { title, description, type: "website" },
    };
  } catch {
    return { title: "Farm | BeanBase" };
  }
}

export default async function FarmDetailPage({ params }: { params: Params }) {
  const { slug } = await params;

  let farm;
  try {
    farm = await api.farms.get(slug);
  } catch {
    notFound();
  }

  const lotsData = await api.lots.list({ farm_id: farm.id, page_size: 50 }).catch(() => null);

  const topScore = lotsData?.items
    .map((l) => l.score)
    .filter((s): s is number => s != null)
    .sort((a, b) => b - a)[0] ?? null;

  return (
    <>
      <CountryBanner country={farm.country} variant="banner" priority />

      <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="mb-1 text-sm text-muted">{farm.country ?? "Unknown origin"}</p>
          <h1 className="text-2xl font-bold text-text">{farm.canonical_name}</h1>
          {farm.owner_name && (
            <p className="mt-1 text-sm text-muted">Owner: {farm.owner_name}</p>
          )}
        </div>
        {topScore != null && (
          <div className="flex flex-col items-end gap-1">
            <span className="text-xs text-muted">Best score</span>
            <ScoreBadge score={topScore} />
          </div>
        )}
      </div>

      {/* Metadata grid */}
      <dl className="mb-10 grid grid-cols-2 gap-x-8 gap-y-3 rounded-card border border-border bg-white p-6 text-sm sm:grid-cols-3">
        {[
          { label: "Altitude",    value: farm.altitude_m ? `${farm.altitude_m}m` : null },
          { label: "Source",      value: farm.source },
          { label: "Cooperative", value: farm.cooperative_name },
        ].map(({ label, value }) =>
          value ? (
            <div key={label}>
              <dt className="text-xs text-muted">{label}</dt>
              <dd className="mt-0.5 font-medium text-text">{value}</dd>
            </div>
          ) : null
        )}

        {farm.process_methods && farm.process_methods.length > 0 && (
          <div className="col-span-2 sm:col-span-3">
            <dt className="mb-1 text-xs text-muted">Process methods</dt>
            <dd className="flex flex-wrap gap-1">
              {farm.process_methods.map((p) => (
                <span key={p} className="rounded-badge bg-honey-50 px-2.5 py-0.5 text-xs text-honey-700">
                  {p}
                </span>
              ))}
            </dd>
          </div>
        )}

        {farm.flavor_tags && farm.flavor_tags.length > 0 && (
          <div className="col-span-2 sm:col-span-3">
            <dt className="mb-1 text-xs text-muted">Flavor profile</dt>
            <dd className="flex flex-wrap gap-1">
              {farm.flavor_tags.map((t) => (
                <span key={t} className="rounded-badge bg-cream-100 px-2.5 py-0.5 text-xs text-fog-600">
                  {t}
                </span>
              ))}
            </dd>
          </div>
        )}
      </dl>

      {/* Auction history */}
      <h2 className="mb-4 text-lg font-semibold text-text">
        Auction lots{lotsData ? ` (${lotsData.total})` : ""}
      </h2>
      {lotsData ? (
        <LotTable lots={lotsData.items} />
      ) : (
        <p className="text-sm text-muted">Could not load auction history.</p>
      )}
      </div>
    </>
  );
}
