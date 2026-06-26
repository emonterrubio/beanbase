import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";

const isPublicRoute = createRouteMatcher([
  "/",
  "/farms(.*)",
  "/auctions(.*)",
  "/origins(.*)",
  "/pro",
  "/sign-in(.*)",
  "/sign-up(.*)",
  "/api/billing/webhook",
  "/sitemap.xml",
]);

const isProRoute = createRouteMatcher(["/pro/dashboard(.*)", "/pro/alerts(.*)"]);

export default clerkMiddleware(async (auth, req) => {
  if (!isPublicRoute(req)) {
    await auth.protect();
  }

  if (isProRoute(req)) {
    const { userId } = await auth();
    if (!userId) return;

    const { clerkClient } = await import("@clerk/nextjs/server");
    const client = await clerkClient();
    const user = await client.users.getUser(userId);
    const isPro = user.publicMetadata?.subscription_status === "active";

    if (!isPro) {
      return NextResponse.redirect(new URL("/pro", req.url));
    }
  }
});

export const config = {
  matcher: [
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/(api|trpc)(.*)",
  ],
};
