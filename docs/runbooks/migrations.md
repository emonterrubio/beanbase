# Runbook — Database Migrations

Migrations live in `api/alembic/versions/`.

| Revision | Summary |
|----------|---------|
| `0001` | Initial schema (origins, farms, lots, auctions, certifications) |
| `0002` | lot_rank, unique constraints, importer_products |
| `0003` | Farm lot-title fields (municipality, department, lot_varietal, lot_process, packaging_type, source_lot_title) |

## Apply

```bash
cd api
source .venv/bin/activate
# Prefer Neon direct (non-pooler) URL for Alembic
export DATABASE_URL=postgresql://...sslmode=require
alembic upgrade head
```

## Create

```bash
cd api
alembic revision --autogenerate -m "description"
# Review the generated file, then:
alembic upgrade head
```

## Rules

- Always include `?sslmode=require` for Neon.
- Do not use `channel_binding=require` with psycopg2.
- After schema changes that affect parsers, run the relevant backfill (see [pipeline.md](./pipeline.md)).
