# BeanBase — Architecture

> Companion status doc: [status.md](./status.md)

## System Overview

BeanBase is a three-tier system: a data pipeline that collects and normalizes coffee data, a REST API that serves it, and a Next.js frontend that makes it discoverable.

```
┌─────────────────────────────────────────────────────────────┐
│                        External Sources                     │
│  Live: CoE | Cafe Imports | Onyx                            │
│  Planned: BoP | Kenya NCE | USDA FAS | ICO | Cert registries│
└──────────────────────┬──────────────────────────────────────┘
                       │ scrape / API pull
┌──────────────────────▼──────────────────────────────────────┐
│                    ETL Pipeline (Python)                     │
│   Ingest → Normalize → Entity Resolve* → Enrich* → Load     │
│                   pipeline/src/                             │
└──────────────────────┬──────────────────────────────────────┘
                       │ writes
┌──────────────────────▼──────────────────────────────────────┐
│             PostgreSQL (Neon)                               │
│   farms | lots | auction_events | certifications | origins  │
│   importer_products                                         │
└──────────────────────┬──────────────────────────────────────┘
                       │ reads
┌──────────────────────▼──────────────────────────────────────┐
│                FastAPI Backend (Railway)                     │
│   /farms | /farms/facets | /lots | /origins | /health       │
│   Planned: /prices | /producers | API keys | metering       │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP
┌──────────────────────▼──────────────────────────────────────┐
│               Next.js Frontend (Vercel)                     │
│   Farm Explorer | Auction Browser | Origin Cards | /pro     │
│   Static pages (SSG) for SEO + Dynamic for dashboard        │
└─────────────────────────────────────────────────────────────┘
```

\*Entity resolution and enrichers are **planned**, not yet implemented as pipeline modules.

## Hosting (as deployed)

| Component | Provider | Notes |
|-----------|----------|--------|
| Web | Vercel | Root Directory = `web` |
| API | Railway | Root Directory = `api`; healthcheck `/health` |
| Database | Neon | Pooler URL for API; direct URL preferred for Alembic/backfills |

## Database Schema (implemented)

ORM models use integer primary keys (see Alembic `0001`–`0003`). Conceptual fields:

### Core tables

- **origins** — country/region taxonomy (seeded ~30 countries)
- **farms** — canonical farm records; includes `owner_name`, `process_methods`, `varietals`, `importer_ids`, `source`, and lot-title fields from migration `0003`:
  - `municipality`, `department`, `lot_varietal`, `lot_process`, `packaging_type`, `source_lot_title`
- **auction_events** — CoE (and future BoP / Kenya NCE) events
- **lots** — auction lots with `lot_rank`, score, price, process, varietal, `raw_source_data`
- **certifications** — table exists; registry ingest not yet populated at scale
- **importer_products** — Onyx (and similar) product rows (`0002`)

Exact DDL: `api/alembic/versions/`.

## Enrichment Pipeline Stages

| Stage | Status | Notes |
|-------|--------|--------|
| **Ingest** | Done (partial) | CoE archives, Cafe Imports, Onyx |
| **Normalize** | Done (partial) | Process taxonomy; importer lot-title parser |
| **Entity Resolution** | Not started | Cross-source farm joins are the long-term moat |
| **Enrich** | Not started | Flavor tags, indices, longitudinal stats |
| **Serve** | Done | FastAPI + Next.js |

## Entity Resolution Strategy

The entity resolution problem: the same farm appears in CoE results as "Finca La Esperanza," in an importer catalog as "La Esperanza Estate," and in a cert registry as "Finca Esperanza S.A."

**Current (Phase 1):** separate records per source slug; Cafe Imports titles parsed into display fields; CoE uses `FarmName` / `ProducerName`. No cross-source merge yet.

**Next:** fuzzy name + country/region matching with low-confidence review queue.

**Later:** GPS (Wikidata / OSM) as a dedup signal (farms within ~0.5 km + similar names).

## SEO Strategy

Farm and origin detail pages are statically generated:

- `/farms/[slug]` → `generateStaticParams()`
- `/origins/[country]` → country-level origin pages
- `sitemap.ts` covers static + farm + origin routes

Target search queries:

- `"Cup of Excellence Ethiopia 2023 results"`
- `"Yirgacheffe farm profiles"`
- `"Best of Panama 2022 lot scores"` (once BoP data exists)

## Decisions

See [decisions/](./decisions/) for Architecture Decision Records.
