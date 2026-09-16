# BeanBase

**The Global Intelligence Layer for Specialty Coffee**

BeanBase is a data intelligence platform for the specialty coffee industry, combining a Coffee Origin & Traceability API with a Coffee Auction & Lot Tracking database. Roasters, importers, cafés, and developer teams get a single source of truth for where coffee comes from, how it scored, and what it sold for — normalized, enriched, and API-accessible.

> BeanBase is the Plaid of specialty coffee data — publicly available information made commercially accessible through normalization, enrichment, and a clean API.

## What It Does

**Layer 1 — Origin & Traceability**
- Farm profiles: region, altitude, varietal, owner/cooperative, processing methods
- Certification cross-mapping: Fair Trade, Rainforest Alliance, UTZ, Bird Friendly, Organic
- Flavor profile tagging against the SCA Flavor Wheel
- Harvest calendars by origin country

**Layer 2 — Auction & Lot Intelligence**
- 25+ years of Cup of Excellence auction results (1999–present)
- Best of Panama and Kenya Nairobi Exchange results
- Score-to-price correlation models by origin
- Producer longitudinal tracking across multiple auction years
- Buyer identity normalization (which roasters win which origins)

## Quick Start

### Prerequisites

- Node.js 20+
- Python 3.9+
- PostgreSQL 15+ with PostGIS extension

### Run the database locally

```bash
docker run --name beanbase-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=beanbase \
  -p 5432:5432 \
  postgis/postgis:15-3.4 -d
```

### Frontend

```bash
cd web
npm install
cp .env.example .env.local   # fill in keys
npm run dev
# → http://localhost:3000
```

### API

```bash
cd api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # fill in keys
alembic upgrade head
uvicorn app.main:app --reload
# → http://localhost:8000/docs
```

### Pipeline

```bash
cd pipeline
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/scrapers/coe_scraper.py
```

## Architecture

See [docs/architecture.md](docs/architecture.md) and [docs/status.md](docs/status.md) for the live system map and phase roadmap.

```
┌─────────────────────────────────────────────────────────┐
│                        Users                            │
│        Enthusiasts | Roasters | Developers              │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              Next.js Frontend (Vercel)                  │
│    Farm Explorer | Auction Browser | Origin Cards       │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              FastAPI Backend (Railway)                  │
│         /farms | /lots | /origins | /health             │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│           PostgreSQL (Neon)                             │
│    Farm entity graph | Auction lots | Origins           │
└─────────────────────▲───────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────┐
│              Python ETL Pipeline                        │
│  Ingest → Normalize → (Entity Resolve*) → Enrich* → Serve │
│                                                         │
│  Live sources: CoE | Cafe Imports | Onyx                │
│  Planned: BoP | Kenya NCE | USDA | Cert registries      │
└─────────────────────────────────────────────────────────┘
```

\*Entity resolution and enrichers are planned (Phase 1 remaining / Phase 2–3); not yet implemented as pipeline stages.

## API Endpoints (live today)

```
GET /health                  Health check
GET /farms                   Search farm profiles (q, origin, source, process, sort)
GET /farms/facets            Contextual filter facets
GET /farms/{slug}            Farm detail
GET /lots                    Query auction lots
GET /lots/{id}               Lot detail
GET /origins                 Country/region origin cards
GET /origins/{country}       Single origin
```

**Planned (Phase 3):** `/certifications`, `/prices`, `/producers`, API keys, metering.

Interactive docs: Scalar UI at `/docs` when the API server is running.

## Pricing

| Tier | Price | Calls/Month |
|------|-------|-------------|
| Free | $0 | Dashboard only |
| Pro Micro-Roaster | $29/mo | Alerts + Shopify integration |
| Pro | $99/mo | Full price intelligence + export |
| API Starter | $79/mo | 10,000 calls |
| API Pro | $149/mo | 100,000 calls |
| API Scale | $499/mo | 1,000,000 calls |
| Enterprise | Custom | Unlimited + SLA |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15+, Tailwind CSS, TypeScript |
| Backend | FastAPI, Python 3.11 (prod) |
| Database | Neon PostgreSQL 15 |
| Pipeline | BeautifulSoup4, httpx / requests, SQLAlchemy |
| Auth | Clerk |
| Billing | Stripe |
| Monitoring | Sentry (+ PostHog planned) |
| Hosting | Vercel (web) + Railway (api) + Neon (db) |

## Project Status

**Current focus: Phase 2 — Pro Dashboard** (Sprint 7 coded; activate billing, then Sprint 8).  
**Phase 1 engineering: complete** — free discovery dashboard is live in beta.

| Phase | Status | Gate |
|-------|--------|------|
| Phase 1 — Free Discovery | Code ✓ — live beta | 500 free signups |
| Phase 2 — Pro Dashboard | In progress | 10 Pro subscribers |
| Phase 3 — API Access | Not started | 3 API customers |

**Shipped (high level):** CoE + Cafe Imports data, Farm Explorer (Origins nav + structured table), Auctions, Origins, SEO/SSG, Sentry, Clerk/Stripe code paths.

**Still to do:** signup gate, Stripe/Clerk activation, Pro alerts/price intel, entity resolution, BoP/Kenya scrapers, paid API product.

Full milestone lists: **[docs/status.md](docs/status.md)** · sprint checklists in [`tasks/`](tasks/).

See [CLAUDE.md](CLAUDE.md) for development context.

---

*Built by Ed Monterrubio | Beta | September 2026*