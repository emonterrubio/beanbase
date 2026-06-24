# BeanBase — Architecture

## System Overview

BeanBase is a three-tier system: a data pipeline that collects and enriches coffee data, a REST API that serves it, and a Next.js frontend that makes it discoverable.

```
┌─────────────────────────────────────────────────────────────┐
│                        External Sources                     │
│  CoE | BoP | Kenya NCE | USDA FAS | ICO | Rainforest | RA   │
└──────────────────────┬──────────────────────────────────────┘
                       │ scrape / API pull
┌──────────────────────▼──────────────────────────────────────┐
│                    ETL Pipeline (Python)                     │
│   Ingest → Normalize → Entity Resolve → Enrich → Load       │
│                   pipeline/src/                             │
└──────────────────────┬──────────────────────────────────────┘
                       │ writes
┌──────────────────────▼──────────────────────────────────────┐
│             PostgreSQL + PostGIS (Railway)                   │
│   farms | lots | auction_events | certifications | origins  │
└──────────────────────┬──────────────────────────────────────┘
                       │ reads
┌──────────────────────▼──────────────────────────────────────┐
│                FastAPI Backend (Railway)                     │
│   /farms | /lots | /origins | /prices | /producers          │
│   + Auth (Clerk JWT) | Rate limiting | Stripe metering      │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP
┌──────────────────────▼──────────────────────────────────────┐
│               Next.js Frontend (Vercel)                     │
│   Farm Explorer | Auction Browser | Origin Cards            │
│   Static pages (SSG) for SEO + Dynamic for dashboard        │
└─────────────────────────────────────────────────────────────┘
```

## Database Schema (Phase 1)

### Core Tables

```sql
-- Country/region taxonomy
CREATE TABLE origins (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  country     TEXT NOT NULL,
  region      TEXT,
  latitude    FLOAT,
  longitude   FLOAT,
  geo         GEOGRAPHY(POINT, 4326),
  altitude_min_m  INT,
  altitude_max_m  INT,
  harvest_start_month INT,
  harvest_end_month   INT,
  dominant_varietals  TEXT[],
  flavor_tags         TEXT[],
  created_at  TIMESTAMPTZ DEFAULT now(),
  updated_at  TIMESTAMPTZ DEFAULT now()
);

-- Farm entity graph (canonical records across sources)
CREATE TABLE farms (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  canonical_name  TEXT NOT NULL,
  origin_id       UUID REFERENCES origins(id),
  altitude_m      INT,
  varietal        TEXT[],
  process_methods TEXT[],
  owner_name      TEXT,
  cooperative_name TEXT,
  geo             GEOGRAPHY(POINT, 4326),
  flavor_tags     TEXT[],
  coe_producer_id TEXT,    -- cross-reference key
  importer_ids    JSONB,   -- {royal_coffee: "...", cafe_imports: "..."}
  created_at      TIMESTAMPTZ DEFAULT now(),
  updated_at      TIMESTAMPTZ DEFAULT now()
);

-- Auction events (CoE, BoP, Kenya NCE)
CREATE TABLE auction_events (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source      TEXT NOT NULL,   -- 'cup_of_excellence' | 'best_of_panama' | 'kenya_nce'
  country     TEXT NOT NULL,
  year        INT NOT NULL,
  event_name  TEXT,
  event_date  DATE,
  created_at  TIMESTAMPTZ DEFAULT now()
);

-- Individual auction lots
CREATE TABLE lots (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  auction_event_id UUID REFERENCES auction_events(id),
  farm_id          UUID REFERENCES farms(id),
  lot_number       INT,
  score            NUMERIC(4,2),
  process_method   TEXT,
  varietal         TEXT[],
  weight_kg        NUMERIC(8,2),
  winning_price_usd_per_kg NUMERIC(8,2),
  buyer_name       TEXT,
  flavor_tags      TEXT[],
  tasting_notes    TEXT,
  raw_source_data  JSONB,    -- original scraped record
  created_at       TIMESTAMPTZ DEFAULT now()
);

-- Certification cross-map
CREATE TABLE certifications (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  farm_id     UUID REFERENCES farms(id),
  body        TEXT NOT NULL,  -- 'rainforest_alliance' | 'fair_trade' | 'organic' | 'utz' | 'bird_friendly'
  cert_number TEXT,
  valid_from  DATE,
  valid_until DATE,
  created_at  TIMESTAMPTZ DEFAULT now()
);
```

## Enrichment Pipeline Stages

| Stage | Input | Output |
|-------|-------|--------|
| **Ingest** | Raw source data | Staging tables with `raw_source_data` JSONB |
| **Normalize** | Staging rows | Standardized fields (process methods, region names, varietal taxonomy) |
| **Entity Resolution** | Normalized records from multiple sources | Merged canonical `farms` records with `importer_ids` cross-references |
| **Enrich** | Canonical records | Computed fields: `flavor_tags`, altitude bands, score/price indices, longitudinal stats |
| **Serve** | Clean DB records | REST API + Next.js data layer |

## Entity Resolution Strategy

The entity resolution problem: the same farm appears in CoE results as "Finca La Esperanza," in Royal Coffee's catalog as "La Esperanza Estate," and in the Rainforest Alliance registry as "Finca Esperanza S.A."

**Phase 1 approach** (simple): fuzzy name matching + country + region. Flag low-confidence matches for manual review.

**Phase 2 approach** (improved): add GPS coordinates (from Wikidata + OpenStreetMap) as a deduplication signal. Farms within 0.5km with similar names = same canonical record.

## SEO Strategy

Farm and lot detail pages must be statically generated at build time:
- `/farms/[slug]` → `generateStaticParams()` for all farms in DB
- `/lots/[id]` → `generateStaticParams()` for all lots
- `/origins/[country]` → country-level origin pages

Target search queries:
- `"Cup of Excellence Ethiopia 2023 results"`
- `"Yirgacheffe farm profiles"`
- `"Best of Panama 2022 lot scores"`

## Decisions

See [decisions/](./decisions/) for Architecture Decision Records.
