from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pathlib
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from app.config import settings
import app.models  # noqa: F401 — registers all ORM models before first request
from app.routers import farms, lots, origins

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[StarletteIntegration(), FastApiIntegration()],
        traces_sample_rate=0.2,
        environment=settings.environment,
    )

app = FastAPI(
    title="BeanBase API",
    description="The Global Intelligence Layer for Specialty Coffee",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
)

_static_dir = pathlib.Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=_static_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(origins.router, prefix="/origins", tags=["origins"])
app.include_router(farms.router, prefix="/farms", tags=["farms"])
app.include_router(lots.router, prefix="/lots", tags=["lots"])


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}


@app.get("/docs", include_in_schema=False)
async def scalar_docs() -> HTMLResponse:
    return HTMLResponse("""<!DOCTYPE html>
<html>
<head>
  <title>BeanBase API</title>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
</head>
<body>
  <script
    id="api-reference"
    data-url="/openapi.json"
    data-configuration='{
      "theme": "kepler",
      "darkMode": true,
      "metaData": {
        "title": "BeanBase API"
      },
      "hiddenClients": [],
      "defaultHttpClient": {
        "targetKey": "python",
        "clientKey": "requests"
      }
    }'
  ></script>
  <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
</body>
</html>""")
