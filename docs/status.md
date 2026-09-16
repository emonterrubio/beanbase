# BeanBase — Project Status & Roadmap

> Last updated: September 2026  
> Canonical status document. Phase checklists live in [`tasks/`](../tasks/).

## Snapshot

| Item | Status |
|------|--------|
| **Product stage** | Public beta (free discovery dashboard) |
| **Critical-path position** | Gates 1–2 **done** → next: **500 free signups**, then **Pro tier live** |
| **Engineering phase** | Phase 1 code ✓ · Phase 2 Sprint 7 coded (activation pending) · Phase 3 not started |
| **Web** | Live — [beanbase-theta.vercel.app](https://beanbase-theta.vercel.app) |
| **API** | Live — Railway (`/health` OK) |
| **Database** | Neon PostgreSQL (~4,200+ farms; CoE lots + Cafe Imports) |
| **Auth / billing** | Clerk + Stripe **coded**; production keys/products **not fully activated** |

---

## Critical path to first dollar

Planning priority follows this commercial sequence. Engineering phases (1–3) support these gates; they do not replace them.

| Gate | What has to be true | Guide timeline | Status |
|------|---------------------|----------------|--------|
| **1. Data foundation** | CoE historical scrape complete, farm entity schema seeded | Weeks 1–4 | **Done** — CoE archives + Neon schema + Cafe Imports/Onyx loaded |
| **2. Free dashboard live** | Farm Explorer + Auction History publicly accessible, SEO-indexed | Weeks 5–10 | **Done** — live on Vercel with SSG/sitemap |
| **3. First 500 free signups** | Organic via r/coffee, Home Barista, Product Hunt | Weeks 10–16 | **Not met** — dashboard live; acquisition not yet executed/measured |
| **4. Pro tier launch** | Alerts + Shopify generator live, Stripe billing active | Weeks 12–16 | **Partial** — Stripe/Clerk **code** ✓; alerts + Shopify + prod activation **open** |
| **5. First paying customer** | One roaster converts at $29/mo | Weeks 14–18 | **Not started** — blocked on gates 3–4 |
| **6. $1K MRR** | ~12–35 paying subscribers depending on tier mix | Months 6–10 | **Not started** |

```
Data foundation ──► Free dashboard ──► 500 signups ──► Pro launch ──► First $ ──► $1K MRR
     [DONE]              [DONE]           [NEXT]         [NEXT*]        [ ]         [ ]
```

\*Pro launch can **overlap** signup growth (weeks 12–16): activate Stripe and ship alerts + Shopify generator while driving organic signups — do not wait for 500 before starting Pro build, but treat **500 signups** as the conversion funnel prerequisite for reliable first revenue.

### How engineering phases map to gates

| Critical-path gate | Primary engineering work |
|--------------------|--------------------------|
| 1 Data foundation | Phase 1 Sprints 0–3.5 |
| 2 Free dashboard | Phase 1 Sprints 4–6.5 |
| 3 Five hundred signups | Growth / distribution (not a code sprint) + analytics |
| 4 Pro tier launch | Phase 2 Sprints 7–9 (billing, alerts, Shopify gen) |
| 5–6 First $ → $1K MRR | Phase 2 product quality + sales; Phase 3 API is **after** first-dollar path |

**Implication:** Prioritize signup acquisition + Pro activation (alerts, Shopify, Stripe) over Phase 3 API keys/metering until first dollar and early MRR are proven.

---

## Engineering phases (build track)

```
Phase 1 ──► Phase 2 ──► Phase 3 ──► Enterprise
 Free         Pro          API
 Discovery    Dashboard    Access
     │            │            │
  [DONE*]      [ACTIVE]     [DEFER until first $]
     │            │
  Gate: 500     Gate: 10
  signups       Pro subs
```

\*Phase 1 engineering is complete. Commercial gate (500 signups) is still open.

| Phase | Goal | Status | Gate to next |
|-------|------|--------|--------------|
| [Phase 1](../tasks/phase1_todo.md) — Free Discovery Dashboard | SEO farm/auction/origin explorer | **Code complete** | 500 free signups |
| [Phase 2](../tasks/phase2_todo.md) — Pro Dashboard | Paid alerts, Shopify gen, price intel | **In progress** | 10 Pro subscribers |
| [Phase 3](../tasks/phase3_todo.md) — API Access | API keys, metering, developer portal | **Not started** (after first-dollar path) | 3 paying API customers |

---

## Phase 1 — Done vs remaining

### Done (shipped) — unlocks critical-path gates 1–2

| Milestone | Notes |
|-----------|--------|
| Repo scaffold (web / api / pipeline / db / docs) | Monorepo |
| Neon DB + Alembic migrations `0001`–`0003` | Farms, lots, auctions, origins, certifications, importer products, lot-title fields |
| CoE scraper + archive JSON (1999–present) | ~211 auction archives; COVID-year gaps expected |
| Cafe Imports + Onyx scrapers/loaders | Farms + importer products |
| Process method normalizer + farm lot-title parser | `farm_name.py` → owner, farm, municipality, department, varietal, process, packaging |
| FastAPI: `/farms`, `/farms/facets`, `/lots`, `/origins` | Paginated list + detail |
| Next.js Farm Explorer, Auctions, Origins, Home | Origins vertical nav; structured farm table |
| SEO: SSG farm/origin pages, sitemap, metadata | Gate 2 requirement |
| Sentry on web, API, ETL | |
| Production deploy (Vercel + Railway + Neon) | |

### Still open

| Item | Critical-path role | Priority |
|------|--------------------|----------|
| Hit **500 free signups** (r/coffee, Home Barista, Product Hunt) | **Gate 3** | **P0** |
| Measure signups (Clerk dashboard / PostHog) | Gate 3 instrumentation | **P0** |
| Known CoE scrape gaps (non-standard historical tables) | Data quality | P2 |
| Entity resolution across CoE ↔ importer farms | Moat (helps retention later) | P1 after first $ |
| Enrichers layer (flavor tags, score/price indices) | Pro/API value | P2 |
| Certification registry scrape | Later differentiation | P2 |

Detailed sprint checklist: [`tasks/phase1_todo.md`](../tasks/phase1_todo.md)

---

## Phase 2 — Done vs remaining (Pro / first dollar)

### Done (code)

| Milestone | Notes |
|-----------|--------|
| Clerk auth (sign-in/up, Nav, `/dashboard`) | Guarded when keys missing |
| Pricing page `/pro` (Micro $29 / Pro $99) | Billing toggle UI |
| Stripe checkout + webhook → Clerk `subscription_status` | Needs prod activation |
| Gated `/pro/dashboard`, `/pro/alerts` routes | Alerts **product** not built yet |

### Still open — ordered for critical-path gate 4

| Item | Sprint | Gate | Priority |
|------|--------|------|----------|
| **Activate** Clerk + Stripe env vars & products in production | 7 | 4 | **P0** |
| Lot alert system — watchlists + email | 8 | 4 | **P0** |
| Shopify description generator | 9 → **pull forward** | 4 | **P0** (on critical path) |
| Verify E2E: signup → checkout → Pro unlock | 7 | 4–5 | **P0** |
| Price intelligence charts ($/lb trends) | 8 | Strengthens Pro | P1 |
| CSV export of filtered lots | 8 | Pro value | P1 |
| Harvest calendar | 9 | Nice-to-have | P2 |
| Best of Panama / Kenya NCE scrapers | 10 | Data depth | P1 after first $ |
| Importer partnership feeds | 10 | Moat | P1 after first $ |

Detailed checklist: [`tasks/phase2_todo.md`](../tasks/phase2_todo.md)

---

## Phase 3 — Not started (after first-dollar path)

Defer paid API product work until gates 5–6 are in motion unless a design partner explicitly needs keys sooner.

| Milestone | Sprint | Status |
|-----------|--------|--------|
| API key management + scopes | 11 | Not started |
| Rate limiting | 11 | Not started |
| `/producers`, `/prices`, `/certifications` product endpoints | 11 | Not started |
| Stripe usage metering + tier limits | 12 | Not started |
| Developer portal + Python SDK + webhooks | 13 | Not started |
| Enterprise SLA / bulk export / cert registries | 14 | Not started |

Detailed checklist: [`tasks/phase3_todo.md`](../tasks/phase3_todo.md)

---

## Data coverage (current)

| Source | Ingestion | In production DB |
|--------|-----------|------------------|
| Cup of Excellence | Scraper + JSON archives | Yes (~6k lots historically loaded) |
| Cafe Imports | Scraper + loader | Yes (~245 farms; lot titles parsed) |
| Onyx Coffee Lab | Scraper + loader | Yes (importer products) |
| Best of Panama | Planned | No |
| Kenya NCE | Planned | No |
| Cert registries / USDA / ICO | Planned | No |

---

## Recommended next actions (critical-path order)

1. **Gate 3 — Acquisition:** Publish to r/coffee, Home Barista, Product Hunt; track free signups toward 500.
2. **Gate 4 — Activate billing:** Clerk + Stripe keys/products in production; E2E checkout test.
3. **Gate 4 — Pro MVP:** Ship **alerts** + **Shopify generator** (minimum for “Pro tier launch”).
4. **Gate 5:** Convert one roaster at $29/mo; learn messaging from that sale.
5. **Gate 6:** Iterate Pro value toward ~12–35 subscribers / $1K MRR.
6. Only then push Phase 3 API Access hard (unless a pilot customer pulls it forward).

---

## Doc map

| Doc | Purpose |
|-----|---------|
| [README.md](../README.md) | Product overview + quick start |
| [CLAUDE.md](../CLAUDE.md) | Agent/dev context |
| [DESIGN.md](../DESIGN.md) | Design system |
| [architecture.md](./architecture.md) | System design |
| [tasks/todo.md](../tasks/todo.md) | Phase index |
| [tasks/lessons.md](../tasks/lessons.md) | Operational lessons |
| [runbooks/](./runbooks/) | Ops procedures |
| [decisions/](./decisions/) | ADRs |
