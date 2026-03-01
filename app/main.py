from __future__ import annotations

from fastapi import FastAPI

from app.config import REGIONAL_SOURCES, REGIONAL_SIZZLE_SIGNALS
from app.repository import init_db, list_products
from app.sniffer import run_sniffer_once

app = FastAPI(title="TrackingBacon", version="0.1.0")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.get("/plan")
def get_plan() -> dict:
    return {
        "sniffer": REGIONAL_SOURCES,
        "sizzle": REGIONAL_SIZZLE_SIGNALS,
    }


@app.post("/sniffer/run")
def run_now() -> dict:
    return run_sniffer_once()


@app.get("/products")
def products(limit: int = 100) -> dict:
    return {"items": list_products(limit=limit)}
