# Phase 2 — Pro Dashboard (Months 3–6)

Validation gate: **10 Pro Dashboard subscribers** before starting Phase 3.  
Unlock condition: 500 free signups (Phase 1 commercial gate) — *engineering may proceed in parallel*.  
**Critical path:** this phase delivers Gate 4 (Pro tier launch) and enables Gates 5–6 (first $ → $1K MRR).  
Canonical overview: [docs/status.md](../docs/status.md)

**Status:** Sprint 7 **code complete**; production activation pending. Alerts + Shopify generator are **P0 for first dollar** (not optional polish).

---

### Sprint 7: Auth + Billing ✓ (code) / ☐ (activation) — Gate 4
- [x] Clerk v7 installed; ClerkProvider in layout; proxy.ts protects /dashboard and /pro/* routes
- [x] Nav: server-side auth check — sign-in/up buttons when signed out, Dashboard + UserButton when signed in
- [x] /sign-in and /sign-up pages using Clerk hosted UI components
- [x] /dashboard: post-auth landing showing free vs Pro state with upgrade CTA
- [x] /pro: pricing page with Pro Micro-Roaster ($29/mo) and Pro ($99/mo) cards + billing toggle
- [x] Stripe: lazy getStripe() client; /api/billing/checkout creates sessions; /api/billing/webhook writes subscription_status to Clerk publicMetadata
- [x] Gated routes: /pro/dashboard and /pro/alerts check publicMetadata.subscription_status === "active", redirect to /pro if not
- [ ] **Activate:** set `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` + `CLERK_SECRET_KEY` in Vercel
- [ ] **Activate:** create Stripe products + set `STRIPE_PRICE_PRO_MICRO` / `STRIPE_PRICE_PRO` + `STRIPE_WEBHOOK_SECRET`
- [ ] **Verify:** end-to-end signup → checkout → webhook → Pro unlock

### Sprint 8: Pro Features — Gate 4 (alerts required)
- [ ] Lot alert system — watchlists + email notifications (price threshold, new auction) **← critical path**
- [ ] Price intelligence layer — historical $/lb trend charts per origin/varietal
- [ ] CSV export — filtered lot search results downloadable as CSV

### Sprint 9: Roaster Tools — Gate 4 (Shopify required)
- [ ] Shopify description generator — produce copy for roaster product listings from lot data **← critical path**
- [ ] Harvest calendar with farm-level availability windows

### Sprint 10: Data Partnerships — after first dollar preferred
- [ ] Importer partnership pipeline — Royal Coffee, Cafe Imports direct data feeds
- [ ] Best of Panama scraper — bopauction.com
- [ ] Kenya NCE weekly auction scraper

### Commercial checkpoints (critical path)

- [ ] Gate 4: Pro tier publicly sellable (Stripe live + alerts + Shopify generator)
- [ ] Gate 5: First paying customer at $29/mo
- [ ] Gate 6: Path to ~$1K MRR (~12–35 subscribers depending on tier mix)
