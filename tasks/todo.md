# BeanBase — Tasks

## Phase 1 — Free Discovery Dashboard (Months 1–3)

### Sprint: Project Setup
- [x] Scaffold repo structure (web, api, pipeline, db, docs)
- [x] Create CLAUDE.md, README.md, DESIGN.md
- [x] Next.js 15 + Tailwind CSS initialized
- [x] FastAPI skeleton + Python venv
- [x] Pipeline Python venv
- [ ] Set up PostgreSQL local dev (Docker)
- [ ] Alembic migration setup
- [ ] Vercel project connected
- [ ] Railway project connected

### Sprint: Data Foundation (Weeks 1–4)
- [ ] CoE historical scraper (1999–present) — pipeline/src/scrapers/coe_scraper.py
- [ ] Farm entity schema design (farms, regions, varietals, process_methods)
- [ ] Auction schema design (auction_events, lots, scores, buyers)
- [ ] Certification schema (certifications, farm_certifications)
- [ ] Alembic migrations for all schemas
- [ ] Seed CoE data (start with 2020–present, expand back)

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
