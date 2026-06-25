# Phase 1 — Free Discovery Dashboard (Months 1–3)

Validation gate: **500 free signups** before starting Phase 2.

---

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
- [ ] Known gap: some old pages (e.g. Ethiopia 2020) have non-standard table layouts — fix in later sprint

### Sprint 3: Normalizers & DB Loaders
- [ ] pipeline/src/normalizers/process_method.py — shared process taxonomy
- [ ] pipeline/src/loaders/coe_loader.py — upsert CoE lots → origins, farms, auction_events, lots
- [ ] pipeline/src/loaders/cafe_imports_loader.py — upsert importer inventory → farms (with importer_ids JSONB)
- [ ] pipeline/src/loaders/onyx_loader.py — importer_products table
- [ ] Wire loaders into run_monthly.py after scraping loop

### Sprint 4: FastAPI Data Layer
- [ ] api/app/db/session.py — async SQLAlchemy engine + get_db dependency
- [ ] api/app/schemas/ — Pydantic v2 response models: FarmSummary, FarmDetail, LotRow, OriginCard
- [ ] api/app/schemas/ — filter models: FarmFilter, LotFilter
- [ ] api/app/routers/farms.py — GET /farms (search, paginated), GET /farms/{slug}
- [ ] api/app/routers/lots.py — GET /lots (filter by origin/year/score/process/price), GET /lots/{id}
- [ ] api/app/routers/origins.py — GET /origins, GET /origins/{country}
- [ ] Register all routers in api/app/main.py

### Sprint 5: Next.js Frontend
- [ ] web/src/styles/tokens.css — BeanBase CSS vars (--bean-brown, --dark-roast, --honey-gold, etc.)
- [ ] web/tailwind.config.ts — wire design tokens into theme.extend.colors
- [ ] web/src/lib/api.ts — typed fetch wrapper pointing at NEXT_PUBLIC_API_URL
- [ ] Layout: Nav.tsx + Footer.tsx
- [ ] Pages: /farms (Farm Explorer, paginated), /farms/[slug] (Farm detail, SSG)
- [ ] Pages: /auctions (Auction History Browser), /origins (Origin Cards), /origins/[country]
- [ ] Pages: /producers/[slug] (longitudinal producer profile)
- [ ] Components: FarmCard, FarmGrid, LotTable, LotRow, OriginCard, ScoreBadge, CertBadge, SearchBar, FilterChip

### Sprint 6: SEO + Sentry (Required Before Beta)
- [ ] generateStaticParams on /farms/[slug] and /origins/[country] — static HTML at build time
- [ ] generateMetadata — dynamic OG tags (farm name + country + score in title)
- [ ] web/src/app/sitemap.ts — generate sitemap for all static pages
- [ ] @sentry/nextjs install + wizard in web/
- [ ] sentry-sdk wired into api/app/main.py (on startup)
- [ ] ETL pipeline Sentry alerting — wrap each scraper call in try/except → capture_exception (REQUIRED before launch)
- [ ] Beta launch on Vercel
