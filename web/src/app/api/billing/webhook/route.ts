import { NextResponse } from "next/server";
import { getStripe } from "@/lib/stripe";
import { clerkClient } from "@clerk/nextjs/server";
import type Stripe from "stripe";

export async function POST(req: Request) {
  const body = await req.text();
  const sig = req.headers.get("stripe-signature");

  if (!sig || !process.env.STRIPE_WEBHOOK_SECRET) {
    return NextResponse.json({ error: "Missing signature or secret" }, { status: 400 });
  }

  let event: Stripe.Event;
  try {
    event = getStripe().webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch {
    return NextResponse.json({ error: "Invalid signature" }, { status: 400 });
  }

  const client = await clerkClient();

  if (event.type === "checkout.session.completed") {
    const session = event.data.object as Stripe.Checkout.Session;
    const userId = session.metadata?.clerk_user_id;
    if (userId) {
      await client.users.updateUserMetadata(userId, {
        publicMetadata: {
          subscription_status: "active",
          stripe_customer_id: session.customer as string,
          stripe_subscription_id: session.subscription as string,
        },
      });
    }
  }

  if (event.type === "customer.subscription.deleted") {
    const sub = event.data.object as Stripe.Subscription;
    // Look up user by customer ID
    const users = await client.users.getUserList({
      limit: 1,
    });
    // Find user with matching stripe_customer_id in publicMetadata
    const match = users.data.find(
      (u) => u.publicMetadata?.stripe_customer_id === sub.customer
    );
    if (match) {
      await client.users.updateUserMetadata(match.id, {
        publicMetadata: { subscription_status: "canceled" },
      });
    }
  }

  return NextResponse.json({ received: true });
}
