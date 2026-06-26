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

### Sprint 3: Normalizers & DB Loaders ✓
- [x] api/alembic/versions/0002 — lot_rank column, uq constraints, importer_products table
- [x] pipeline/src/normalizers/process_method.py — 30-entry canonical taxonomy
- [x] pipeline/src/normalizers/__init__.py — shared slugify()
- [x] pipeline/src/loaders/coe_loader.py — upserts CoE lots → farms + auction_events + lots
- [x] pipeline/src/loaders/cafe_imports_loader.py — upserts producers → farms with importer_ids JSONB
- [x] pipeline/src/loaders/onyx_loader.py — upserts products → importer_products
- [x] run_monthly.py wired: Phase 1 scrape → Phase 2 DB load (skipped if no DATABASE_URL)
- [x] Verified: 329 farms, 95 lots, 178 importer_products loaded from sample data

### Sprint 3.5: Cloud Infrastructure ✓
- [x] Neon PostgreSQL — project "beanbase" (us-east-1), direct + pooler connection strings
- [x] Alembic migrations 0001 + 0002 applied to Neon
- [x] 30 canonical origin rows seeded into Neon (db/seeds/seed_origins.py)
- [x] Railway service deployed from api/ subdirectory; /health endpoint live; auto-deploys on push to main
- [x] api/Procfile — uvicorn start command
- [x] api/.python-version — pinned to 3.11 for Railway/nixpacks
- [x] railway.toml — healthcheck path /health, restart policy on_failure (3 retries)
- [x] api/app/config.py — ALLOWED_ORIGINS parses comma-separated env var (needed for Vercel URL in prod)
- [x] pipeline/load_archives_to_neon.py — one-shot loader for backfilling 211 archive files → Neon
- [x] CoE backfill: 6,049 lots → Neon (all 211 archive files)
- [x] Cafe Imports: 245 farms → Neon; Onyx: 177 products → Neon
- [x] Bug fix: coe_loader score normalization — pages encoding 90.65 as 9065 now handled
- [x] Bug fix: run_monthly.py --dry-run now threads dry_run flag into CoE scraper (no stale archive writes)

### Sprint 4: FastAPI Data Layer ✓
- [x] api/app/db/session.py — async SQLAlchemy engine (asyncpg) + get_db dependency; strips sslmode/channel_binding for asyncpg compat
- [x] api/app/schemas/ — Pydantic v2 response models: FarmSummary, FarmDetail, LotRow, LotDetail, OriginCard, Page[T]
- [x] api/app/routers/farms.py — GET /farms (q/origin/process/source filters, paginated), GET /farms/{slug}
- [x] api/app/routers/lots.py — GET /lots (origin/year/score/price/process/farm_id filters, paginated), GET /lots/{id}
- [x] api/app/routers/origins.py — GET /origins, GET /origins/{country}
- [x] Register all routers in api/app/main.py
- [x] Bug fix: greenlet added to requirements (asyncpg async runtime dependency)
- [x] Bug fix: all ORM models imported in models/__init__.py to resolve mapper relationships at startup
- [x] Bug fix: ALLOWED_ORIGINS stored as str to avoid pydantic-settings JSON-decode on List[str] fields
- [x] Verified against Neon: /origins 30 rows, /lots?origin=Ethiopia&min_score=90 → 19 lots, /farms?origin=Colombia → 470 farms

### Sprint 5: Next.js Frontend ✓
- [x] web/src/styles/tokens.css — Tailwind v4 @theme design tokens (bean-brown, honey, cream, fog palettes + semantic aliases)
- [x] web/src/lib/api.ts — typed fetch wrapper (FarmSummary, FarmDetail, LotRow, LotDetail, OriginCard, Page<T>) pointing at NEXT_PUBLIC_API_URL
- [x] Layout: Nav.tsx (sticky header, brand logo, CTA) + Footer.tsx
- [x] Pages: /farms (Farm Explorer, SearchBar + origin/process FilterChips, paginated), /farms/[slug] (farm detail + lot history)
- [x] Pages: /auctions (origin/score/year FilterChips + LotTable, paginated), /origins (country grid), /origins/[country] (altitude/harvest/varietals + top lots)
- [x] Pages: / (home hero, live stats with try/catch fallback, feature cards)
- [x] Components: FarmCard, FarmGrid, LotTable, OriginCard, ScoreBadge, CertBadge, SearchBar, FilterChip, Pagination
- [x] API docs: replaced Swagger UI with Scalar (theme: kepler, dark mode, Python default client)
- [x] Deployed to Vercel — beanbase-theta.vercel.app live (Root Directory=web, web/vercel.json)

### Sprint 6: SEO + Sentry ✓
- [x] generateStaticParams on /farms/[slug] (500 pages) and /origins/[country] (18 pages) — SSG at build time
- [x] generateMetadata — OG title + description on farm and origin detail pages
- [x] web/src/app/sitemap.ts — dynamic sitemap covering static routes + all farm + origin pages
- [x] @sentry/nextjs wired via src/instrumentation.ts + sentry.{client,server}.config.ts + withSentryConfig in next.config.ts
- [x] sentry-sdk wired into api/app/main.py (FastApiIntegration + StarletteIntegration, gated on SENTRY_DSN)
- [x] ETL pipeline Sentry alerting — sentry_sdk.init in run_monthly.py; capture_exception on all scraper + loader failures
- [x] Beta launch — SENTRY_DSN set in Vercel + Railway; beanbase-theta.vercel.app live and open for signups
