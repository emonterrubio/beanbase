# BeanBase — Project Status & Roadmap

> Last updated: September 2026  
> Canonical status document. Phase checklists live in [`tasks/`](../tasks/).

## Snapshot

| Item | Status |
|------|--------|
| **Product stage** | Public beta (free discovery dashboard) |
| **Current phase** | **Phase 2** — Pro Dashboard (Sprint 7 coded; activation + Sprint 8 next) |
| **Phase 1 gate** | Awaiting **500 free signups** (code complete; gate not yet met) |
| **Web** | Live — [beanbase-theta.vercel.app](https://beanbase-theta.vercel.app) |
| **API** | Live — Railway (`/health` OK) |
| **Database** | Neon PostgreSQL (~4,200+ farms; CoE lots + Cafe Imports) |
| **Auth / billing** | Clerk + Stripe **coded**; production keys/products **not fully activated** |

---

## Phase overview

```
Phase 1 ──► Phase 2 ──► Phase 3 ──► Enterprise
 Free         Pro          API
 Discovery    Dashboard    Access
     │            │            │
  [DONE*]      [ACTIVE]     [NOT STARTED]
     │            │
  Gate: 500     Gate: 10
  signups       Pro subs
```

\*Phase 1 engineering is complete. Commercial gate (500 signups) is still open.

| Phase | Goal | Status | Gate to next |
|-------|------|--------|--------------|
| [Phase 1](../tasks/phase1_todo.md) — Free Discovery Dashboard | SEO farm/auction/origin explorer | **Code complete** | 500 free signups |
| [Phase 2](../tasks/phase2_todo.md) — Pro Dashboard | Paid alerts, price intel, roaster tools | **In progress** (Sprint 7 ✓ code; 8–10 open) | 10 Pro subscribers |
| [Phase 3](../tasks/phase3_todo.md) — API Access | API keys, metering, developer portal | **Not started** | 3 paying API customers |

---

## Phase 1 — Done vs remaining

### Done (shipped)

| Milestone | Notes |
|-----------|--------|
| Repo scaffold (web / api / pipeline / db / docs) | Monorepo |
| Neon DB + Alembic migrations `0001`–`0003` | Farms, lots, auctions, origins, certifications, importer products, lot-title fields |
| CoE scraper + archive JSON (1999–present) | ~211 auction archives; COVID-year gaps expected |
| Cafe Imports + Onyx scrapers/loaders | Farms + importer products |
| Process method normalizer + farm lot-title parser | `farm_name.py` → owner, farm, municipality, department, varietal, process, packaging |
| FastAPI: `/farms`, `/farms/facets`, `/lots`, `/origins` | Paginated list + detail |
| Next.js Farm Explorer, Auctions, Origins, Home | Origins vertical nav; structured farm table |
| SEO: SSG farm/origin pages, sitemap, metadata | |
| Sentry on web, API, ETL | |
| Production deploy (Vercel + Railway + Neon) | |

### Still open (Phase 1 gaps / polish)

| Item | Priority |
|------|----------|
| Hit **500 free signup** validation gate | **P0 — commercial** |
| Activate analytics (PostHog) if not already | P1 |
| Known CoE scrape gaps (non-standard historical tables) | P2 |
| Entity resolution across CoE ↔ importer farms | P1 (moat) — not built |
| Enrichers layer (flavor tags, score/price indices) | P2 — folder empty |
| PostGIS / geo enrichment | P2 — schema aspirational; not fully used |
| Certification registry scrape (RA / Fair Trade) | P2 |

Detailed sprint checklist: [`tasks/phase1_todo.md`](../tasks/phase1_todo.md)

---

## Phase 2 — Done vs remaining

### Done (code)

| Milestone | Notes |
|-----------|--------|
| Clerk auth (sign-in/up, Nav, `/dashboard`) | Guarded when keys missing |
| Pricing page `/pro` (Micro $29 / Pro $99) | Billing toggle UI |
| Stripe checkout + webhook → Clerk `subscription_status` | |
| Gated `/pro/dashboard`, `/pro/alerts` routes | |

### Still open

| Item | Sprint | Priority |
|------|--------|----------|
| **Activate** Clerk + Stripe env vars & products in production | 7 | **P0** |
| Lot alerts / watchlists + email | 8 | P0 product |
| Price intelligence charts ($/lb trends) | 8 | P0 product |
| CSV export of filtered lots | 8 | P1 |
| Shopify description generator | 9 | P1 |
| Harvest calendar | 9 | P2 |
| Best of Panama scraper | 10 | P1 data |
| Kenya NCE scraper | 10 | P1 data |
| Importer partnership feeds | 10 | P1 |

Detailed checklist: [`tasks/phase2_todo.md`](../tasks/phase2_todo.md)

---

## Phase 3 — Not started

| Milestone | Sprint | Status |
|-----------|--------|--------|
| API key management + scopes | 11 | Not started |
| Rate limiting | 11 | Not started |
| `/producers`, `/prices`, `/certifications` product endpoints | 11 | Not started (schemas/docs mention them) |
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

## Recommended next actions

1. **Activate** Clerk + Stripe in Vercel/Railway; verify signup → checkout → webhook.
2. **Measure** free signups toward the Phase 1 gate (PostHog or Clerk dashboard).
3. **Ship Sprint 8** (alerts + price trends + CSV) once billing is live.
4. **Deepen data moat**: entity resolution + one new auction source (BoP or Kenya NCE).

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
