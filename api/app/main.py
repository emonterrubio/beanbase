from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
import app.models  # noqa: F401 — registers all ORM models before first request
from app.routers import farms, lots, origins

app = FastAPI(
    title="BeanBase API",
    description="The Global Intelligence Layer for Specialty Coffee",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

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
