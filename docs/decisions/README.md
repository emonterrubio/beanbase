# Architecture Decision Records

ADRs capture significant technical choices and their rationale.

| ID | Title | Status |
|----|-------|--------|
| — | *(none filed yet)* | — |

## Template

When adding an ADR, create `NNNN-short-title.md`:

```markdown
# NNNN — Title

- Status: Proposed | Accepted | Superseded
- Date: YYYY-MM-DD

## Context
## Decision
## Consequences
```

## Candidate ADRs to capture (from shipped work)

- Neon PostgreSQL (vs Railway Postgres) for primary data store
- Railway root directory = `api/` for monorepo deploys
- Vercel root directory = `web/`
- Clerk for auth; Stripe for Pro billing via Clerk `publicMetadata`
- Scalar (not Swagger UI) for API docs
- Importer lot-title heuristic parsing into farm columns
