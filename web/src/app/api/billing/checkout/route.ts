import { auth, currentUser } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";
import { getStripe, PLANS, type PlanKey } from "@/lib/stripe";

const SITE = process.env.NEXT_PUBLIC_SITE_URL ?? "https://beanbase-theta.vercel.app";

export async function POST(req: Request) {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { tier } = (await req.json()) as { tier: PlanKey };
  const plan = PLANS[tier];
  if (!plan?.priceId) {
    return NextResponse.json({ error: "Invalid tier or missing price ID" }, { status: 400 });
  }

  const user = await currentUser();
  const email = user?.emailAddresses[0]?.emailAddress;

  const session = await getStripe().checkout.sessions.create({
    mode: "subscription",
    payment_method_types: ["card"],
    customer_email: email,
    line_items: [{ price: plan.priceId, quantity: 1 }],
    metadata: { clerk_user_id: userId },
    success_url: `${SITE}/dashboard?upgraded=1`,
    cancel_url: `${SITE}/pro`,
  });

  return NextResponse.json({ url: session.url });
}
