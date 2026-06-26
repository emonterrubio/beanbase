# Phase 2 — Pro Dashboard (Months 3–6)

Validation gate: **10 Pro Dashboard subscribers** before starting Phase 3.
Unlock condition: 500 free signups achieved (Phase 1 gate).

---

### Sprint 7: Auth + Billing ✓
- [x] Clerk v7 installed; ClerkProvider in layout; proxy.ts protects /dashboard and /pro/* routes
- [x] Nav: server-side auth check — sign-in/up buttons when signed out, Dashboard + UserButton when signed in
- [x] /sign-in and /sign-up pages using Clerk hosted UI components
- [x] /dashboard: post-auth landing showing free vs Pro state with upgrade CTA
- [x] /pro: pricing page with Pro Micro-Roaster ($29/mo) and Pro ($99/mo) cards
- [x] Stripe: lazy getStripe() client; /api/billing/checkout creates sessions; /api/billing/webhook writes subscription_status to Clerk publicMetadata
- [x] Gated routes: /pro/dashboard and /pro/alerts check publicMetadata.subscription_status === "active", redirect to /pro if not
- [ ] Activate: set NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY + CLERK_SECRET_KEY in Vercel; create Stripe products + set STRIPE_PRICE_PRO_MICRO / STRIPE_PRICE_PRO + STRIPE_WEBHOOK_SECRET

### Sprint 8: Pro Features
- [ ] Lot alert system — watchlists + email notifications (price threshold, new auction)
- [ ] Price intelligence layer — historical $/lb trend charts per origin/varietal
- [ ] CSV export — filtered lot search results downloadable as CSV

### Sprint 9: Roaster Tools
- [ ] Shopify description generator — produce copy for roaster product listings from lot data
- [ ] Harvest calendar with farm-level availability windows

### Sprint 10: Data Partnerships
- [ ] Importer partnership pipeline — Royal Coffee, Cafe Imports direct data feeds
- [ ] Best of Panama scraper — bopauction.com
- [ ] Kenya NCE weekly auction scraper
