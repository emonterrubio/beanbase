export const dynamic = "force-dynamic";
export const revalidate = 0;

import Link from "next/link";
import { api } from "@/lib/api";

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

      {/* Pricing */}
      <section className="border-t border-border bg-cream-50 px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-5xl">
          <div className="mb-12 text-center">
            <h2 className="text-2xl font-bold text-text">Simple, transparent pricing</h2>
            <p className="mt-2 text-sm text-muted">Start free. Upgrade when the data pays for itself.</p>
          </div>

          <div className="grid gap-6 sm:grid-cols-3">
            {/* Free */}
            <div className="flex flex-col rounded-card border border-border bg-white p-8">
              <p className="text-sm font-medium text-muted">Free</p>
              <p className="mt-1 text-4xl font-bold text-text">$0</p>
              <p className="mt-1 text-xs text-muted">forever</p>
              <ul className="my-8 flex-1 space-y-3 text-sm text-text">
                {["Farm Explorer", "25 years of CoE auction history", "Origin intelligence cards", "Unlimited browsing"].map((f) => (
                  <li key={f} className="flex items-start gap-2">
                    <span className="mt-0.5 text-honey-500">✓</span>{f}
                  </li>
                ))}
              </ul>
              <Link
                href="/sign-up"
                className="block w-full rounded-badge border border-brand py-2.5 text-center text-sm font-semibold text-brand transition-colors hover:bg-cream-100"
              >
                Get started free
              </Link>
            </div>

            {/* Pro Micro-Roaster */}
            <div className="flex flex-col rounded-card border border-honey-300 bg-white p-8 shadow-md">
              <div className="mb-2 self-start rounded-badge bg-honey-100 px-2.5 py-0.5 text-xs font-semibold text-honey-700">
                Most popular
              </div>
              <p className="text-sm font-medium text-muted">Pro Micro-Roaster</p>
              <p className="mt-1 text-4xl font-bold text-text">$29</p>
              <p className="mt-1 text-xs text-muted">per month</p>
              <ul className="my-8 flex-1 space-y-3 text-sm text-text">
                {["Everything in Free", "Price alerts on saved origins", "Shopify description generator", "Harvest calendar", "CSV export (500 rows/mo)"].map((f) => (
                  <li key={f} className="flex items-start gap-2">
                    <span className="mt-0.5 text-honey-500">✓</span>{f}
                  </li>
                ))}
              </ul>
              <Link
                href="/pro"
                className="block w-full rounded-badge bg-honey-500 py-2.5 text-center text-sm font-semibold text-white transition-colors hover:bg-honey-600"
              >
                Start free trial
              </Link>
            </div>

            {/* Pro */}
            <div className="flex flex-col rounded-card border border-border bg-white p-8">
              <p className="text-sm font-medium text-muted">Pro</p>
              <p className="mt-1 text-4xl font-bold text-text">$99</p>
              <p className="mt-1 text-xs text-muted">per month</p>
              <ul className="my-8 flex-1 space-y-3 text-sm text-text">
                {["Everything in Micro-Roaster", "Full price intelligence layer", "Historical $/lb trend charts", "CSV export (unlimited)", "Priority support"].map((f) => (
                  <li key={f} className="flex items-start gap-2">
                    <span className="mt-0.5 text-honey-500">✓</span>{f}
                  </li>
                ))}
              </ul>
              <Link
                href="/pro"
                className="block w-full rounded-badge border border-brand py-2.5 text-center text-sm font-semibold text-brand transition-colors hover:bg-cream-100"
              >
                View plan
              </Link>
            </div>
          </div>

          <p className="mt-8 text-center text-xs text-muted">
            Need bulk data access?{" "}
            <Link href="/pro" className="text-accent hover:underline">
              See API plans →
            </Link>
          </p>
        </div>
      </section>
    </>
  );
}
