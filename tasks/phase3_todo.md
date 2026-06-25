# Phase 3 — API Access (Months 6–12)

Validation gate: **3 API paying customers** before unlocking Enterprise tier.
Unlock condition: 10 Pro Dashboard subscribers achieved (Phase 2 gate).

---

### Sprint 11: REST API v1
- [ ] API key management — generate/revoke keys, scopes
- [ ] Rate limiting middleware — per-key request counters (Redis or Postgres)
- [ ] Full endpoint coverage: GET /farms, /lots, /origins, /producers, /prices, /certifications
- [ ] Pagination, filtering, and field selection on all list endpoints

### Sprint 12: Billing & Metering
- [ ] Stripe usage-based metering — count API calls per key per billing period
- [ ] Tier enforcement — 10K / 100K / 1M call limits per plan
- [ ] Overage alerts — email when approaching limit

### Sprint 13: Developer Experience
- [ ] OpenAPI docs — auto-generated from FastAPI, hosted at /docs
- [ ] Developer portal — key management UI, usage dashboard, quickstart guide
- [ ] Client SDK (Python) — thin wrapper around REST API
- [ ] Webhook support — notify on new auction results

### Sprint 14: Enterprise
- [ ] Custom SLA agreements
- [ ] Dedicated rate limit tiers
- [ ] White-label data export (bulk JSON/CSV delivery)
- [ ] Rainforest Alliance + Fair Trade certification registry integration
