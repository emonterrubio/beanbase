import { NextRequest, NextResponse } from "next/server";

const CLERK_CONFIGURED = Boolean(process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY);

const isPublicPath = (pathname: string) =>
  /^\/(farms|auctions|origins|pro$|sign-in|sign-up|api\/billing\/webhook|sitemap\.xml|_next|favicon)/.test(pathname) ||
  pathname === "/";

const isProPath = (pathname: string) =>
  /^\/pro\/(dashboard|alerts)/.test(pathname);

async function clerkProxy(req: NextRequest) {
  const { clerkMiddleware, createRouteMatcher } = await import("@clerk/nextjs/server");

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

  return clerkMiddleware(async (auth, request) => {
    if (!isPublicRoute(request)) {
      await auth.protect();
    }

    if (isProRoute(request)) {
      const { userId } = await auth();
      if (!userId) return;

      const { clerkClient } = await import("@clerk/nextjs/server");
      const client = await clerkClient();
      const user = await client.users.getUser(userId);
      const isPro = user.publicMetadata?.subscription_status === "active";

      if (!isPro) {
        return NextResponse.redirect(new URL("/pro", request.url));
      }
    }
  })(req, {} as never);
}

export default async function proxy(req: NextRequest) {
  if (!CLERK_CONFIGURED) return NextResponse.next();

  const { pathname } = req.nextUrl;

  // Skip Clerk entirely for public paths when not hitting a protected route
  if (isPublicPath(pathname) && !isProPath(pathname)) {
    return NextResponse.next();
  }

  return clerkProxy(req);
}

export const config = {
  matcher: [
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/(api|trpc)(.*)",
  ],
};
