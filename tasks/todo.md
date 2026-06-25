# BeanBase — Tasks

## Phase 1 — Free Discovery Dashboard (Months 1–3)

### Sprint 0: Project Setup ✓
- [x] Scaffold repo structure (web, api, pipeline, db, docs)
- [x] Create CLAUDE.md, README.md, DESIGN.md
- [x] Next.js 15 + Tailwind CSS initialized
- [x] FastAPI skeleton + Python venv
- [x] Pipeline Python venv

### Sprint 1: Database Foundation ✓
- [x] PostgreSQL 15 via Homebrew; beanbase database created
- [x] SQLAlchemy ORM models: origins, farms, auction_events, lots, certifications
- [x] Alembic migration 0001 — all 5 tables + GIN FTS index
- [x] Seed 30 canonical origin rows (db/seeds/seed_origins.py)
- [x] pipeline/src/scrapers/cafe_imports.py + onyx.py registered in run_monthly.py

### Sprint 2: CoE Historical Scraper ✓
- [x] pipeline/src/scrapers/coe_scraper.py — run(month_stamp) -> list[dict]
- [x] 239 auction pages registered across 18 countries (1999–2026)
- [x] Auto-backfill on first run; incremental (current year only) on subsequent runs
- [x] Archive raw JSON per auction to pipeline/data/coe/{slug}.json
- [x] Registered in run_monthly.py SCRAPERS list
- [ ] Known gap: some old pages (e.g. Ethiopia 2020) have non-standard table layouts

### Sprint 3: Normalizers & DB Loaders (next)
- [ ] pipeline/src/normalizers/process_method.py — shared process taxonomy
- [ ] pipeline/src/loaders/coe_loader.py — upsert CoE lots → origins, farms, auction_events, lots
- [ ] pipeline/src/loaders/cafe_imports_loader.py — upsert importer inventory → farms
- [ ] pipeline/src/loaders/onyx_loader.py — importer_products table
- [ ] Wire loaders into run_monthly.py after scraping loop

### Sprint: Frontend Foundation (Weeks 4–8)
- [ ] Tailwind theme with BeanBase design tokens (brown accent)
- [ ] Layout + navigation shell
- [ ] Farm Explorer: search + filter UI
- [ ] Farm detail page (SSG)
- [ ] Auction History Browser: table + filters
- [ ] Lot/producer detail page (SSG)

### Sprint: Origin Intelligence (Weeks 6–10)
- [ ] Origin Intelligence Cards (country-level profiles)
- [ ] Harvest calendar component
- [ ] Certification display components

### Sprint: SEO + Launch (Weeks 7–12)
- [ ] Static generation for farm + lot pages (Next.js generateStaticParams)
- [ ] OG meta tags for shareable farm/lot URLs
- [ ] Sitemap generation
- [ ] Sentry setup: web + api + pipeline
- [ ] ETL pipeline Sentry alerting (REQUIRED before launch)
- [ ] Beta launch on Vercel

## Phase 2 — Pro Dashboard (Months 3–6)
- [ ] Clerk auth integration
- [ ] Stripe subscription setup ($29 / $99 tiers)
- [ ] Lot alert system (watchlists + email)
- [ ] Price intelligence layer
- [ ] CSV export
- [ ] Shopify description generator
- [ ] Importer partnership pipeline (Royal Coffee, Cafe Imports)

## Phase 3 — API Access (Months 6–12)
- [ ] REST API v1: /farms, /lots, /origins, /producers
- [ ] API key management + rate limiting
- [ ] Stripe usage-based metering
- [ ] OpenAPI docs + developer portal
- [ ] /prices + /certifications endpoints

## Validation Gates
- [ ] 500 free signups → unlock Phase 2 build
- [ ] 10 Pro Dashboard subscribers → unlock Phase 3 (API)
- [ ] 3 API paying customers → unlock Enterprise tier
