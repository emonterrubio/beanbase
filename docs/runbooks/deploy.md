# Runbook — Deploy

## Web (Vercel)

1. Root Directory must be `web`.
2. Framework Preset: **Next.js**. Leave Output Directory blank (do not set `public` or `.`).
3. Required env:
   - `NEXT_PUBLIC_API_URL` → Railway API base URL (e.g. `https://beanbase-production.up.railway.app`)
   - Optional: Clerk, Stripe, Sentry, PostHog keys
4. Deploy: push to `main` (auto) or `cd web && npx vercel --prod`.

## API (Railway)

1. Service Root Directory must be `api`.
2. Healthcheck: `/health` (see root `railway.toml`).
3. Required env:
   - `DATABASE_URL` — Neon pooler URL with `?sslmode=require`
   - `ALLOWED_ORIGINS` — JSON array or comma-separated Vercel URL(s)
   - Optional: `SENTRY_DSN`, Clerk/Stripe secrets if API needs them later
4. Deploy: push to `main` with Railway connected, or `railway up` from `api/`.

## Smoke checks

```bash
curl -s https://<api-host>/health
curl -s "https://<api-host>/farms?page_size=1"
curl -s -o /dev/null -w "%{http_code}\n" https://beanbase-theta.vercel.app/farms
```
