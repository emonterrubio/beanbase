"use client";

import { PLANS } from "@/lib/stripe";
import { useRouter } from "next/navigation";
import { useState } from "react";

function CheckIcon() {
  return (
    <svg className="h-4 w-4 shrink-0 text-honey-500" viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clipRule="evenodd" />
    </svg>
  );
}

export default function ProPage() {
  const router = useRouter();
  const [loading, setLoading] = useState<string | null>(null);

  async function upgrade(tier: keyof typeof PLANS) {
    setLoading(tier);
    try {
      const res = await fetch("/api/billing/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tier }),
      });
      if (res.status === 401) { router.push("/sign-up"); return; }
      const { url } = await res.json();
      if (url) window.location.href = url;
    } finally {
      setLoading(null);
    }
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-16 sm:px-6 lg:px-8">
      <div className="mb-12 text-center">
        <h1 className="text-3xl font-bold text-text">Upgrade to Pro</h1>
        <p className="mt-3 text-muted">
          Price intelligence, alerts, and roaster tools — built on 25 years of auction data.
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2">
        {(Object.entries(PLANS) as [keyof typeof PLANS, typeof PLANS[keyof typeof PLANS]][]).map(
          ([key, plan]) => (
            <div
              key={key}
              className="flex flex-col rounded-card border border-border bg-white p-8 shadow-sm"
            >
              <div className="mb-6">
                <p className="text-sm font-medium text-muted">{plan.name}</p>
                <p className="mt-1 text-4xl font-bold text-text">
                  ${plan.price}
                  <span className="text-lg font-normal text-muted">/mo</span>
                </p>
              </div>

              <ul className="mb-8 flex-1 space-y-3">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-start gap-2 text-sm text-text">
                    <CheckIcon />
                    {f}
                  </li>
                ))}
              </ul>

              <button
                onClick={() => upgrade(key)}
                disabled={loading !== null}
                className="w-full rounded-badge bg-brand py-2.5 text-sm font-semibold text-white transition-colors hover:bg-bean-brown-700 disabled:opacity-60"
              >
                {loading === key ? "Redirecting…" : `Get ${plan.name}`}
              </button>
            </div>
          )
        )}
      </div>

      <p className="mt-8 text-center text-xs text-muted">
        Cancel anytime. Payments secured by Stripe.
      </p>
    </div>
  );
}
