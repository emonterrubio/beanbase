import type { Metadata } from "next";
import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import Link from "next/link";

export const metadata: Metadata = { title: "Dashboard" };

export default async function DashboardPage() {
  const user = await currentUser();
  if (!user) redirect("/sign-in");

  const isPro = user.publicMetadata?.subscription_status === "active";
  const firstName = user.firstName ?? user.emailAddresses[0]?.emailAddress.split("@")[0];

  return (
    <div className="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-10">
        <h1 className="text-2xl font-bold text-text">Welcome back, {firstName}</h1>
        <p className="mt-1 text-sm text-muted">
          {isPro ? "Pro plan" : "Free plan"} · {user.emailAddresses[0]?.emailAddress}
        </p>
      </div>

      {/* Quick links */}
      <div className="mb-10 grid gap-4 sm:grid-cols-3">
        {[
          { href: "/farms",    label: "Farm Explorer",    body: "Search 4,000+ farm profiles" },
          { href: "/auctions", label: "Auction History",  body: "25 years of CoE results"     },
          { href: "/origins",  label: "Origins",          body: "18 producing countries"       },
        ].map(({ href, label, body }) => (
          <Link
            key={href}
            href={href}
            className="rounded-card border border-border bg-white p-5 transition-shadow hover:shadow-md"
          >
            <p className="font-semibold text-text">{label}</p>
            <p className="mt-1 text-sm text-muted">{body}</p>
          </Link>
        ))}
      </div>

      {/* Upgrade CTA for free users */}
      {!isPro && (
        <div className="rounded-card border border-honey-200 bg-honey-50 p-6">
          <h2 className="mb-1 font-semibold text-text">Unlock Pro features</h2>
          <p className="mb-4 text-sm text-muted">
            Price alerts, trend charts, CSV exports, and the Shopify description generator.
          </p>
          <Link
            href="/pro"
            className="rounded-badge bg-honey-500 px-5 py-2 text-sm font-semibold text-white transition-colors hover:bg-honey-600"
          >
            View plans →
          </Link>
        </div>
      )}

      {isPro && (
        <div className="rounded-card border border-green-200 bg-green-50 p-6">
          <h2 className="mb-1 font-semibold text-text">You&apos;re on Pro</h2>
          <p className="text-sm text-muted">
            Pro features (alerts, charts, CSV export) are shipping in Sprint 8 — stay tuned.
          </p>
        </div>
      )}
    </div>
  );
}
