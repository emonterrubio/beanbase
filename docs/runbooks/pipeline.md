# Runbook — Data Pipeline

## Monthly scrape + load

```bash
cd pipeline
source .venv/bin/activate
export DATABASE_URL=postgresql://...   # Neon URL with sslmode=require
python src/run_monthly.py              # add --dry-run to skip writes
```

Scrapers (CoE, Cafe Imports, Onyx) run first; loaders write to Neon when `DATABASE_URL` is set.

## CoE archive reload (recovery)

If archives exist but DB load failed:

```bash
cd pipeline
python load_archives_to_neon.py
```

Archives under `pipeline/data/coe/` are the source of truth for historical CoE pages.

## Farm name / lot-title backfill

After changing `farm_name.py` or migration `0003`:

```bash
cd pipeline
export DATABASE_URL=postgresql://...
python scripts/backfill_farm_names.py --dry-run
python scripts/backfill_farm_names.py
```

## Notes

- CoE 2020 pages often have no results (COVID cancellations) — expected parse “failures.”
- Prefer Neon **direct** URL for long Alembic/backfill jobs; pooler is fine for the API.
