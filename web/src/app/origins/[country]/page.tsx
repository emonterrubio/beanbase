import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { api } from "@/lib/api";
import { LotTable } from "@/components/LotTable";

type Params = Promise<{ country: string }>;

const MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

export async function generateStaticParams() {
  try {
    const origins = await api.origins.list();
    return origins
      .filter((o) => !o.region)
      .map((o) => ({ country: encodeURIComponent(o.country) }));
  } catch {
    return [];
  }
}

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { country } = await params;
  const name = decodeURIComponent(country);
  const title = `${name} Coffee Origins | BeanBase`;
  const description = `Explore ${name} specialty coffee — altitude, harvest windows, varietals, and Cup of Excellence auction data on BeanBase.`;
  return {
    title,
    description,
    openGraph: { title, description, type: "website" },
  };
}

export default async function OriginDetailPage({ params }: { params: Params }) {
  const { country } = await params;
  const name = decodeURIComponent(country);

  let origin;
  try {
    origin = await api.origins.get(name);
  } catch {
    notFound();
  }

  const lotsData = await api.lots
    .list({ origin: origin.country, min_score: 87, page_size: 20 })
    .catch(() => null);

  const harvest =
    origin.harvest_start_month && origin.harvest_end_month
      ? `${MONTHS[origin.harvest_start_month - 1]} – ${MONTHS[origin.harvest_end_month - 1]}`
      : null;

  return (
    <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-text">{origin.country}</h1>
        {origin.notes && (
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted">{origin.notes}</p>
        )}
      </div>

      {/* Stats */}
      <dl className="mb-10 grid grid-cols-2 gap-4 rounded-card border border-border bg-white p-6 sm:grid-cols-4">
        {[
          {
            label: "Altitude",
            value: origin.altitude_min_m != null
              ? `${origin.altitude_min_m}–${origin.altitude_max_m ?? "?"}m`
              : null,
          },
          { label: "Harvest",  value: harvest },
        ]
          .filter((d) => d.value)
          .map(({ label, value }) => (
            <div key={label}>
              <dt className="text-xs text-muted">{label}</dt>
              <dd className="mt-0.5 font-medium text-text">{value}</dd>
            </div>
          ))}

        {origin.dominant_varietals && origin.dominant_varietals.length > 0 && (
          <div className="col-span-2">
            <dt className="mb-1 text-xs text-muted">Varietals</dt>
            <dd className="flex flex-wrap gap-1">
              {origin.dominant_varietals.map((v) => (
                <span key={v} className="rounded-badge bg-cream-100 px-2 py-0.5 text-xs text-fog-700">
                  {v}
                </span>
              ))}
            </dd>
          </div>
        )}

        {origin.flavor_tags && origin.flavor_tags.length > 0 && (
          <div className="col-span-2">
            <dt className="mb-1 text-xs text-muted">Flavor profile</dt>
            <dd className="flex flex-wrap gap-1">
              {origin.flavor_tags.map((t) => (
                <span key={t} className="rounded-badge bg-honey-50 px-2 py-0.5 text-xs text-honey-700">
                  {t}
                </span>
              ))}
            </dd>
          </div>
        )}
      </dl>

      {/* Top lots */}
      <div className="flex items-baseline justify-between mb-4">
        <h2 className="text-lg font-semibold text-text">Top lots (score ≥ 87)</h2>
        <a
          href={`/auctions?origin=${encodeURIComponent(origin.country)}`}
          className="text-sm text-accent hover:underline"
        >
          See all →
        </a>
      </div>
      {lotsData ? (
        <LotTable lots={lotsData.items} />
      ) : (
        <p className="text-sm text-muted">Could not load lots.</p>
      )}
    </div>
  );
}
