# BeanBase — CLAUDE.md

> The Global Intelligence Layer for Specialty Coffee

## Project Overview

BeanBase is a data intelligence platform for the specialty coffee industry combining two data layers:
- **Layer 1 — Origin & Traceability**: Normalized farm profiles, certifications, processing methods, flavor tags
- **Layer 2 — Auction & Lot Intelligence**: 25+ years of Cup of Excellence and specialty auction results

**Core thesis**: BeanBase is the Plaid of specialty coffee data — publicly available information made commercially accessible through normalization, enrichment, and a clean API. The moat is in the joins, not the data itself.

## Repository Structure

```
beanbase/
├── web/                    # Next.js 15 + Tailwind CSS (Vercel)
│   └── src/
│       ├── app/            # App Router pages
│       ├── components/     # Shared UI components
│       └── lib/            # Utilities, API client, types
├── api/                    # FastAPI Python backend (Railway/Render)
│   ├── app/
│   │   ├── routers/        # Route handlers (/farms, /lots, /origins, etc.)
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── services/       # Business logic layer
│   │   ├── middleware/      # Auth, rate limiting, logging
│   │   └── db/             # Database connection, session management
│   └── tests/
├── pipeline/               # Python ETL data pipeline
│   ├── src/
│   │   ├── scrapers/       # Source scrapers (CoE, BoP, Kenya NCE, importers)
│   │   ├── normalizers/    # Field standardization, taxonomy mapping
│   │   ├── enrichers/      # Computed fields, entity resolution
│   │   └── loaders/        # DB write layer
│   └── tests/
├── db/
│   ├── migrations/         # Alembic migration files
│   └── seeds/              # Seed data for local dev
├── docs/
│   ├── architecture.md     # System architecture decisions
│   ├── decisions/          # ADRs (Architecture Decision Records)
│   └── runbooks/           # Ops runbooks
└── tasks/
    ├── todo.md             # Current sprint tasks
    └── lessons.md          # Accumulated lessons
```

## Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Frontend | Next.js 15 + Tailwind CSS | App Router, static gen for SEO |
| Backend API | FastAPI (Python 3.9+) | Async, OpenAPI auto-docs |
| Database | PostgreSQL + PostGIS | Entity graph + geo queries |
| Data Pipeline | Python (pandas, BS4, httpx) | ETL for CoE, importers, certs |
| Search | Postgres FTS (v1) → Typesense (v2) | Avoid Elasticsearch ops overhead |
| Auth | Clerk | Zero-ops, up to 10K MAU free |
| Billing | Stripe | Usage-based metering for API |
| Hosting | Vercel (web) + Railway (api + db) | Solo-friendly |
| Monitoring | Sentry + PostHog | Error tracking + product analytics |

## Development Setup

### Prerequisites
- Node.js 20+
- Python 3.9+
- PostgreSQL 15+ with PostGIS extension

### Frontend (web/)
```bash
cd web
npm install
cp .env.example .env.local
npm run dev          # http://localhost:3000
```

### API (api/)
```bash
cd api
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head        # Run migrations
uvicorn app.main:app --reload --port 8000
```

### Pipeline (pipeline/)
```bash
cd pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python src/scrapers/coe_scraper.py   # Test a scraper
```

### Database
```bash
# Local dev with Docker
docker run --name beanbase-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=beanbase \
  -p 5432:5432 \
  postgis/postgis:15-3.4 -d
```

## Key Commands

```bash
# Frontend
cd web && npm run dev          # Dev server
cd web && npm run build        # Production build
cd web && npm run type-check   # TypeScript check

# API
cd api && uvicorn app.main:app --reload
cd api && pytest               # Run tests
cd api && alembic revision --autogenerate -m "description"
cd api && alembic upgrade head

# Pipeline
cd pipeline && python src/scrapers/coe_scraper.py
cd pipeline && pytest
```

## Environment Variables

### web/.env.local
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=
NEXT_PUBLIC_POSTHOG_KEY=
SENTRY_DSN=
```

### api/.env
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/beanbase
CLERK_SECRET_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
SENTRY_DSN=
ALLOWED_ORIGINS=http://localhost:3000
```

### pipeline/.env
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/beanbase
SENTRY_DSN=
APIFY_API_TOKEN=           # Optional, for scraping proxy
```

## API Endpoints (Phase 3)

| Endpoint | Description |
|----------|-------------|
| `GET /farms` | Search farm profiles with enrichment |
| `GET /farms/{id}` | Single farm detail |
| `GET /lots` | Query auction lots (farm, score, origin, year, process, price) |
| `GET /origins` | Country/region-level origin intelligence |
| `GET /certifications` | Certification status by farm or region |
| `GET /prices` | Price indices and trend data |
| `GET /producers` | Longitudinal producer profiles |

## Data Pipeline — Enrichment Stages

1. **Ingest** → Raw data pulled from sources, stored in staging schema
2. **Normalize** → Field standardization, taxonomy mapping
3. **Entity Resolution** → Cross-source deduplication to canonical records
4. **Enrich** → Computed fields (flavor tags, altitude bands, score/price indices)
5. **Serve** → Clean records exposed via REST API and dashboard

## Current Phase

**Phase 1 — Free Discovery Dashboard** (Months 1–3)
- [ ] CoE historical scraper (1999–present)
- [ ] Farm entity schema + PostgreSQL setup
- [ ] Next.js Farm Explorer + Auction History browser
- [ ] Origin Intelligence Cards
- [ ] SEO-optimized static pages
- [ ] Sentry alerting on all ETL pipeline parsers

Validation gate before Phase 2: **500 free signups**

## Architecture Principles

1. **Data moat over features** — Every engineering decision should deepen the normalized dataset. The UI is distribution; the data is the product.
2. **SEO-first frontend** — Farm and lot pages must be statically generated and indexable. `'Cup of Excellence Ethiopia 2023 results'` is a search query we should own.
3. **Pipeline reliability** — Broken scrapers silently failing will corrupt paid user data. Sentry alerting on all ETL parsers is required before launch.
4. **Entity resolution is the moat** — Same farm in CoE, importer site, and Rainforest Alliance registry must resolve to one canonical record. This join is what competitors can't replicate quickly.
5. **Simplicity first** — Solo build. No premature abstraction. Add Airflow scheduling, Typesense, and Kafka when the data volume requires it — not before.

## Workflow Guidelines

- Enter plan mode for any non-trivial task (3+ steps or architectural decisions)
- Use subagents for research, exploration, and parallel analysis
- After corrections: update `tasks/lessons.md`
- Never mark a task complete without demonstrating it works
- Review `tasks/lessons.md` at session start

## Data Sources

| Source | Type | Access | Refresh |
|--------|------|--------|---------|
| Cup of Excellence | Auction results, farm data | Scrape | Per auction (~20/yr) |
| Best of Panama | Geisha auction results | Scrape | Per auction |
| Kenya NCE | Weekly auction results | Scrape | Weekly |
| USDA FAS | Crop/trade data | Free API | Monthly |
| ICO | Global trade statistics | Free datasets | Monthly |
| Rainforest Alliance / Fair Trade USA | Certification registries | Public search | Quarterly |
| Wikidata | Farm/region geo enrichment | SPARQL API (CC0) | Monthly |
| Royal Coffee, Cafe Imports, etc. | Importer lot data | Partnership preferred | Weekly |

## Pricing Tiers

| Tier | Price | Target | Limit |
|------|-------|--------|-------|
| Free | $0 | Enthusiasts | Dashboard only |
| Pro Micro-Roaster | $29/mo | Indie roasters | Alerts + Shopify gen |
| Pro | $99/mo | Roasters + curators | Full price intelligence |
| API Starter | $79/mo | Dev teams | 10K calls/mo |
| API Pro | $149/mo | Growing apps | 100K calls/mo |
| API Scale | $499/mo | Production apps | 1M calls/mo |
| Enterprise | Custom | Importers, café chains | Unlimited + SLA |
