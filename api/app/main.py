from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(
    title="BeanBase API",
    description="The Global Intelligence Layer for Specialty Coffee",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}


# Routers registered in Phase 1–3
# from app.routers import farms, lots, origins, certifications, prices, producers
# app.include_router(farms.router, prefix="/farms", tags=["farms"])
# app.include_router(lots.router, prefix="/lots", tags=["lots"])
# app.include_router(origins.router, prefix="/origins", tags=["origins"])
# app.include_router(certifications.router, prefix="/certifications", tags=["certifications"])
# app.include_router(prices.router, prefix="/prices", tags=["prices"])
# app.include_router(producers.router, prefix="/producers", tags=["producers"])
