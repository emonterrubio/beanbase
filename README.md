# BeanBase

**The Global Intelligence Layer for Specialty Coffee**

BeanBase is a data intelligence platform for the specialty coffee industry, combining a Coffee Origin & Traceability API with a Coffee Auction & Lot Tracking database. Roasters, importers, cafés, and developer teams get a single source of truth for where coffee comes from, how it scored, and what it sold for — normalized, enriched, and API-accessible.

> BeanBase is the Plaid of specialty coffee data — publicly available information made commercially accessible through normalization, enrichment, and a clean API.

## What It Does

**Layer 1 — Origin & Traceability**
- Farm profiles: region, altitude, varietal, owner/cooperative, processing methods
- Certification cross-mapping: Fair Trade, Rainforest Alliance, UTZ, Bird Friendly, Organic
- Flavor profile tagging against the SCA Flavor Wheel
- Harvest calendars by origin country

**Layer 2 — Auction & Lot Intelligence**
- 25+ years of Cup of Excellence auction results (1999–present)
- Best of Panama and Kenya Nairobi Exchange results
- Score-to-price correlation models by origin
- Producer longitudinal tracking across multiple auction years
- Buyer identity normalization (which roasters win which origins)

## Quick Start

### Prerequisites

- Node.js 20+
- Python 3.9+
- PostgreSQL 15+ with PostGIS extension

### Run the database locally

```bash
docker run --name beanbase-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=beanbase \
  -p 5432:5432 \
  postgis/postgis:15-3.4 -d
```

### Frontend

```bash
cd web
npm install
cp .env.example .env.local   # fill in keys
npm run dev
# → http://localhost:3000
```

### API

```bash
cd api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # fill in keys
alembic upgrade head
uvicorn app.main:app --reload
# → http://localhost:8000/docs
```

### Pipeline

```bash
cd pipeline
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/scrapers/coe_scraper.py
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        Users                            │
│        Enthusiasts | Roasters | Developers              │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              Next.js Frontend (Vercel)                  │
│    Farm Explorer | Auction Browser | Origin Cards       │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              FastAPI Backend (Railway)                  │
│    /farms | /lots | /origins | /prices | /producers     │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│           PostgreSQL + PostGIS (Railway)                │
│    Farm entity graph | Auction lots | Certifications    │
└─────────────────────▲───────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────┐
│              Python ETL Pipeline                        │
│  Ingest → Normalize → Entity Resolve → Enrich → Serve  │
│                                                         │
│  Sources: CoE | BoP | Kenya NCE | USDA | Importers      │
└─────────────────────────────────────────────────────────┘
```

## API Endpoints

```
GET /farms                   Search farm profiles
GET /farms/{id}              Farm detail with full enrichment
GET /lots                    Query auction lots
GET /origins                 Country/region origin intelligence
GET /certifications          Certification status
GET /prices                  Price indices and trends
GET /producers               Longitudinal producer profiles
```

Full API docs available at `/docs` (Swagger UI) when the API server is running.

## Pricing

| Tier | Price | Calls/Month |
|------|-------|-------------|
| Free | $0 | Dashboard only |
| Pro Micro-Roaster | $29/mo | Alerts + Shopify integration |
| Pro | $99/mo | Full price intelligence + export |
| API Starter | $79/mo | 10,000 calls |
| API Pro | $149/mo | 100,000 calls |
| API Scale | $499/mo | 1,000,000 calls |
| Enterprise | Custom | Unlimited + SLA |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, Tailwind CSS, TypeScript |
| Backend | FastAPI, Python 3.9 |
| Database | PostgreSQL 15, PostGIS |
| Pipeline | pandas, BeautifulSoup4, httpx |
| Auth | Clerk |
| Billing | Stripe |
| Monitoring | Sentry, PostHog |
| Hosting | Vercel + Railway |

## Project Status

**Current Phase: Phase 1 — Free Discovery Dashboard**

- [ ] CoE historical scraper (1999–present)
- [ ] PostgreSQL schema (farms, lots, auctions, certifications)
- [ ] Farm Explorer UI
- [ ] Auction History Browser
- [ ] Origin Intelligence Cards
- [ ] SEO-optimized static pages
- [ ] Sentry ETL pipeline alerting

See [CLAUDE.md](CLAUDE.md) for full development context and architecture details.

---

*Built by Ed Monterrubio | v1.0 | June 2026*
