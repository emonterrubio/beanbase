from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pathlib

from app.config import settings
import app.models  # noqa: F401 — registers all ORM models before first request
from app.routers import farms, lots, origins

app = FastAPI(
    title="BeanBase API",
    description="The Global Intelligence Layer for Specialty Coffee",
    version="0.1.0",
    docs_url=None,    # disable default; we serve custom below
    redoc_url=None,
)

# Serve static assets (custom Swagger CSS, future favicon, etc.)
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
async def custom_docs() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="BeanBase API",
        swagger_css_url="/static/swagger-custom.css",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,   # collapse schemas section by default
            "syntaxHighlight.theme": "monokai",
            "tryItOutEnabled": True,
        },
    )
