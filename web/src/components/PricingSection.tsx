"use client";

import { useState } from "react";
import Link from "next/link";

const PLANS = [
  {
    name: "Free",
    monthly: 0,
    yearly: 0,
    period: "forever",
    features: [
      "Farm Explorer",
      "25 years of CoE auction history",
      "Origin intelligence cards",
      "Unlimited browsing",
    ],
    cta: "Get started free",
    href: "/sign-up",
    highlighted: false,
  },
  {
    name: "Pro Micro-Roaster",
    monthly: 29,
    yearly: 23,
    yearlyTotal: 276,
    features: [
      "Everything in Free",
      "Price alerts on saved origins",
      "Shopify description generator",
      "Harvest calendar",
      "CSV export (500 rows/mo)",
    ],
    cta: "Start free trial",
    href: "/pro",
    highlighted: true,
  },
  {
    name: "Pro",
    monthly: 99,
    yearly: 79,
    yearlyTotal: 948,
    features: [
      "Everything in Micro-Roaster",
      "Full price intelligence layer",
      "Historical $/lb trend charts",
      "CSV export (unlimited)",
      "Priority support",
    ],
    cta: "View plan",
    href: "/pro",
    highlighted: false,
  },
] as const;

export function PricingSection() {
  const [billing, setBilling] = useState<"monthly" | "yearly">("monthly");
  const yearly = billing === "yearly";

  return (
    <section className="border-t border-border bg-cream-50 px-4 py-20 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-5xl">
        {/* Header */}
        <div className="mb-10 text-center">
          <h2 className="text-2xl font-bold text-text">Simple, transparent pricing</h2>
          <p className="mt-2 text-sm text-muted">Start free. Upgrade when the data pays for itself.</p>
        </div>

        {/* Toggle */}
        <div className="mb-12 flex items-center justify-center gap-4">
          <span className={`text-sm font-medium transition-colors ${!yearly ? "text-text" : "text-muted"}`}>
            Monthly
          </span>
          <button
            onClick={() => setBilling(yearly ? "monthly" : "yearly")}
            aria-label="Toggle billing period"
            className="relative h-7 w-14 rounded-full bg-fog-200 transition-colors duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-honey-500"
          >
            <span
              className={`absolute top-1 h-5 w-5 rounded-full bg-honey-500 shadow transition-transform duration-300 ease-in-out ${
                yearly ? "translate-x-8" : "translate-x-1"
              }`}
            />
          </button>
          <span className={`flex items-center gap-2 text-sm font-medium transition-colors ${yearly ? "text-text" : "text-muted"}`}>
            Yearly
            <span className="rounded-badge bg-green-100 px-2 py-0.5 text-xs font-semibold text-green-700">
              Save 20%
            </span>
          </span>
        </div>

        {/* Cards */}
        <div className="grid gap-6 sm:grid-cols-3">
          {PLANS.map((plan) => {
            const price = yearly ? plan.yearly : plan.monthly;
            const period = plan.monthly === 0
              ? "forever"
              : yearly
              ? "per month, billed yearly"
              : "per month";

            return (
              <div
                key={plan.name}
                className={`flex flex-col rounded-card border bg-white p-8 ${
                  plan.highlighted
                    ? "border-honey-300 shadow-md"
                    : "border-border"
                }`}
              >
                {plan.highlighted && (
                  <div className="mb-2 self-start rounded-badge bg-honey-100 px-2.5 py-0.5 text-xs font-semibold text-honey-700">
                    Most popular
                  </div>
                )}

                <p className="text-sm font-medium text-muted">{plan.name}</p>

                {/* Animated price */}
                <div className="mt-1 flex items-end gap-1">
                  <span
                    key={`${plan.name}-${billing}`}
                    className="animate-fade-in text-4xl font-bold tabular-nums text-text"
                  >
                    {price === 0 ? "Free" : `$${price}`}
                  </span>
                </div>
                <p className="mt-1 text-xs text-muted">{period}</p>

                {"yearlyTotal" in plan && yearly && (
                  <p className="mt-1 text-xs font-medium text-green-600">
                    ${plan.yearlyTotal}/yr — save ${(plan.monthly - plan.yearly) * 12}/yr
                  </p>
                )}

                <ul className="my-8 flex-1 space-y-3 text-sm text-text">
                  {plan.features.map((f) => (
                    <li key={f} className="flex items-start gap-2">
                      <span className="mt-0.5 text-honey-500">✓</span>
                      {f}
                    </li>
                  ))}
                </ul>

                <Link
                  href={plan.href}
                  className={`block w-full rounded-badge py-2.5 text-center text-sm font-semibold transition-colors ${
                    plan.highlighted
                      ? "bg-honey-500 text-white hover:bg-honey-600"
                      : "border border-brand text-brand hover:bg-cream-100"
                  }`}
                >
                  {plan.cta}
                </Link>
              </div>
            );
          })}
        </div>

        <p className="mt-8 text-center text-xs text-muted">
          Need bulk data access?{" "}
          <Link href="/pro" className="text-accent hover:underline">
            See API plans →
          </Link>
        </p>
      </div>
    </section>
  );
}
