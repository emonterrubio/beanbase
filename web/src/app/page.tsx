export const dynamic = "force-dynamic";
export const revalidate = 0;

import Link from "next/link";
import { api } from "@/lib/api";
import { PricingSection } from "@/components/PricingSection";

async function getStats() {
  try {
    const [farms, lots, origins] = await Promise.all([
      api.farms.list({ page_size: 1 }),
      api.lots.list({ page_size: 1 }),
      api.origins.list(),
    ]);
    return {
      farms: farms.total,
      lots: lots.total,
      origins: origins.filter((o) => !o.region).length,
    };
  } catch {
    return { farms: 4290, lots: 6049, origins: 18 };
  }
}

export default async function HomePage() {
  const stats = await getStats();

  return (
    <>
      {/* Hero */}
      <section className="border-b border-border bg-bean-brown-900 px-4 py-20 text-white sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <p className="mb-3 text-sm font-medium uppercase tracking-widest text-honey-400">
            Cup of Excellence · 25 Years of Data
          </p>
          <h1 className="mb-6 text-4xl font-bold leading-tight sm:text-5xl">
            The Global Intelligence Layer for{" "}
            <span className="text-honey-400">Specialty Coffee</span>
          </h1>
          <p className="mx-auto mb-10 max-w-xl text-lg text-bean-brown-200">
            Normalized farm profiles, lot scores, and auction results from Cup
            of Excellence — publicly available data made commercially accessible.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              href="/farms"
              className="rounded-badge bg-honey-500 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-honey-600"
            >
              Explore Farms
            </Link>
            <Link
              href="/auctions"
              className="rounded-badge border border-bean-brown-600 px-6 py-3 text-sm font-semibold text-white transition-colors hover:border-honey-400 hover:text-honey-400"
            >
              Browse Auctions
            </Link>
          </div>
        </div>
      </section>

      {/* Stats bar */}
      <section className="border-b border-border bg-white px-4 py-6 sm:px-6 lg:px-8">
        <dl className="mx-auto grid max-w-4xl grid-cols-3 divide-x divide-border text-center">
          {[
            { value: stats.farms.toLocaleString(), label: "Farm profiles" },
            { value: stats.lots.toLocaleString(),  label: "Auction lots"  },
            { value: `${stats.origins}`,           label: "Origins"       },
          ].map(({ value, label }) => (
            <div key={label} className="px-4 py-2">
              <dt className="text-2xl font-bold text-brand">{value}</dt>
              <dd className="mt-0.5 text-xs text-muted">{label}</dd>
            </div>
          ))}
        </dl>
      </section>

      {/* Feature cards */}
      <section className="px-4 py-16 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-5xl">
          <h2 className="mb-10 text-center text-2xl font-bold text-text">
            What you can do with BeanBase
          </h2>
          <div className="grid gap-6 sm:grid-cols-3">
            {[
              {
                href:  "/farms",
                title: "Farm Explorer",
                body:  "Search thousands of farm profiles across 18+ countries, filtered by origin, process method, and certification.",
              },
              {
                href:  "/auctions",
                title: "Auction History",
                body:  "25 years of Cup of Excellence results — filter by country, year, score band, or price to spot trends.",
              },
              {
                href:  "/origins",
                title: "Origin Intelligence",
                body:  "Country-level cards with altitude bands, harvest windows, dominant varietals, and flavor profiles.",
              },
            ].map(({ href, title, body }) => (
              <Link
                key={href}
                href={href}
                className="group flex flex-col gap-3 rounded-card border border-border bg-white p-6 transition-shadow hover:shadow-md"
              >
                <span className="inline-block h-2 w-8 rounded-full bg-honey-500 transition-all group-hover:w-12" />
                <h3 className="text-base font-semibold text-text group-hover:text-brand">{title}</h3>
                <p className="text-sm leading-relaxed text-muted">{body}</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <PricingSection />
    </>
  );
}
