import Stripe from "stripe";

let _stripe: Stripe | null = null;

export function getStripe(): Stripe {
  if (!_stripe) {
    const key = process.env.STRIPE_SECRET_KEY;
    if (!key) throw new Error("STRIPE_SECRET_KEY is not set");
    _stripe = new Stripe(key);
  }
  return _stripe;
}

export const PLANS = {
  pro_micro: {
    name: "Pro Micro-Roaster",
    price: 29,
    priceId: process.env.STRIPE_PRICE_PRO_MICRO ?? "",
    features: [
      "Price alerts on saved origins",
      "Shopify description generator",
      "Harvest calendar",
      "CSV export (500 rows/mo)",
    ],
  },
  pro: {
    name: "Pro",
    price: 99,
    priceId: process.env.STRIPE_PRICE_PRO ?? "",
    features: [
      "Everything in Micro-Roaster",
      "Full price intelligence layer",
      "Historical $/lb trend charts",
      "CSV export (unlimited)",
      "Priority support",
    ],
  },
} as const;

export type PlanKey = keyof typeof PLANS;
