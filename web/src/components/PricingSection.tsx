"use client";

import { useState } from "react";
import Link from "next/link";
import { BillingToggle } from "@/components/BillingToggle";

type Billing = "monthly" | "yearly";

const PLANS = [
  {
    name: "Free",
    monthly: 0,
    yearly: 0,
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

function getPrice(plan: typeof PLANS[number], billing: Billing) {
  return billing === "yearly" ? plan.yearly : plan.monthly;
}

function getPeriod(plan: typeof PLANS[number], billing: Billing) {
  if (plan.monthly === 0) return "forever";
  return billing === "yearly" ? "per month, billed yearly" : "per month";
}

function getSavings(plan: typeof PLANS[number], billing: Billing) {
  if (plan.monthly === 0 || billing === "monthly") return null;
  const saved = (plan.monthly - plan.yearly) * 12;
  return `Save $${saved}/yr`;
}

export function PricingSection() {
  const [billing, setBilling] = useState<Billing>("monthly");

  return (
    <section className="border-t border-border bg-cream-50 px-4 py-20 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-5xl">
        {/* Header */}
        <div className="mb-8 text-center">
          <h2 className="text-4xl font-bold text-text">Simple, transparent pricing</h2>
          <p className="mt-2 text-base text-muted">Start free. Upgrade when the data pays for itself.</p>
        </div>

        {/* Toggle */}
        <div className="mb-10 flex justify-center">
          <BillingToggle value={billing} onChange={setBilling} />
        </div>

        {/* Cards */}
        <div className="grid gap-6 sm:grid-cols-3">
          {PLANS.map((plan) => {
            const price = getPrice(plan, billing);
            const period = getPeriod(plan, billing);
            const savings = getSavings(plan, billing);

            return (
              <div
                key={plan.name}
                className={`flex flex-col rounded-card border bg-white p-8 ${
                  plan.highlighted ? "border-honey-300 shadow-md" : "border-border"
                }`}
              >
                {plan.highlighted && (
                  <div className="mb-3 self-start rounded-badge bg-honey-100 px-2.5 py-0.5 text-xs font-semibold text-honey-700">
                    Most popular
                  </div>
                )}

                <p className="text-sm font-medium text-muted">{plan.name}</p>

                <div className="mt-1 flex items-baseline gap-1">
                  <span
                    key={`${plan.name}-${billing}`}
                    className="animate-fade-in text-4xl font-bold tabular-nums text-text"
                  >
                    {price === 0 ? "Free" : `$${price}`}
                  </span>
                </div>

                <div className="mt-1 min-h-[2.5rem]">
                  <p className="text-xs text-muted">{period}</p>
                  {savings && (
                    <p className="animate-fade-in text-xs font-medium text-green-600">{savings}</p>
                  )}
                </div>

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
