# BeanBase — Lessons

> Accumulated lessons from corrections and validated decisions.
> Review at the start of each session.

---

## Pipeline

### CoE score encoding varies by page era
Some CoE auction pages (e.g. Colombia 2022) encode scores as integers without a decimal point — `9065` instead of `90.65`. The fix: if `score > 100`, divide by 100. Applied in `coe_loader.py:_upsert_lot()`.

### psycopg2 cannot adapt raw dicts to JSONB
When inserting into a JSONB column, pass `json.dumps(dict(row), default=str)` — not a bare Python dict. psycopg2 raises `ProgrammingError: can't adapt type 'dict'` otherwise. Applied in all three loaders.

### CoE buyer_name can exceed VARCHAR(300)
Some lots have 10+ buyers concatenated into one string (500+ chars). Truncate to 300 before insert: `str(buyer)[:300]`.

### Python 3.9 union type syntax fails at runtime
`float | None` in function annotations raises `TypeError` on Python 3.9. Use `Optional[float]` from `typing` instead. Applies to all pipeline code targeting 3.9+.

### run_monthly.py --dry-run must be threaded into scrapers
`--dry-run` skips CSV/DB writes in the orchestrator, but scrapers with their own file-write side effects (CoE archive JSON) need `dry_run=True` passed explicitly. Use `inspect.signature` to detect which scrapers accept the param and forward it. Fixed in Sprint 3.5.

### CoE archive files are the source of truth for historical data
The scraper skips any page whose archive file exists AND whose year < current year. If the DB load fails after the archive is written, those rows will never be retried by the normal pipeline. For recovery, use `pipeline/load_archives_to_neon.py` to reload from all archives.

---

## Database / Alembic

### Use the direct (non-pooler) Neon URL for Alembic migrations
Neon provides two connection strings: pooler (`-pooler` in hostname) and direct. Alembic migrations need a persistent connection — use the direct URL. The running API can use either, but pooler is preferred for production.

### Neon requires `?sslmode=require` in connection string
Without it, psycopg2 connects unencrypted and Neon rejects it. Always include `sslmode=require` in the DATABASE_URL. `channel_binding=require` shown in the Neon console UI is not supported by psycopg2 — omit it.

### Numeric(4,2) is max 99.99 — sufficient for CoE scores
CoE competition scores range from ~84 to ~97 in practice. `Numeric(4, 2)` fits after the score normalization fix. No migration needed.

---

## Cloud Infrastructure

### Railway: set Root Directory to `api/` for monorepo deploys
Railway auto-detects nixpacks by finding `requirements.txt`. In a monorepo, set the service root directory to `api/` in Railway UI so it finds the right `requirements.txt` and `Procfile`. The `railway.toml` at repo root handles health check and restart policy.

### Railway picks up `ALLOWED_ORIGINS` as a comma-separated string
Pydantic `list[str]` fields from env vars need a custom validator to parse comma-separated input. Added `@field_validator("allowed_origins", mode="before")` in `api/app/config.py`.

### JSON archive + Neon write order is guaranteed
The CoE scraper writes `pipeline/data/coe/{slug}-{year}.json` before adding lots to `all_lots` (lines 609–618 in coe_scraper.py). The loader only runs after `run()` returns. Archive always exists before Neon write — JSON and Neon are always in sync for normal pipeline runs.

---

## Data

### CoE 2020 pages have no results tables
Brazil 2020, Colombia 2020, Costa Rica 2020, El Salvador 2020, Ethiopia 2020, Guatemala 2020, Nicaragua 2020, Peru 2020 all return "no results tables found". These are COVID-year cancellations — the pages exist but contain no competition data. 12 parse failures are expected; not a scraper bug.

### CoE backfill takes ~45 minutes against remote Neon
The `coe_loader` does 5–6 DB round trips per lot (origin cache lookup, farm upsert SELECT+INSERT, auction event get-or-create, lot upsert SELECT+INSERT). At ~100ms RTT to Neon, 6,049 lots takes ~45 minutes. This is a one-time cost; subsequent monthly runs process only 5–20 new lots.
