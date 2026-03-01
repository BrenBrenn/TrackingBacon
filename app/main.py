from __future__ import annotations

from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse

from app.config import REGIONAL_SOURCES, REGIONAL_SIZZLE_SIGNALS
from app.repository import init_db, list_products
from app.sniffer import run_sniffer_once

app = FastAPI(title="TrackingBacon", version="0.1.0")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def root() -> HTMLResponse:
    return HTMLResponse(
        """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>TrackingBacon</title>
  <style>
    :root { color-scheme: dark; }
    body {
      margin: 0; font-family: Inter, Segoe UI, Arial, sans-serif;
      background: #0b0d10; color: #e6edf3;
    }
    .wrap { max-width: 860px; margin: 32px auto; padding: 0 16px; }
    .card {
      background: #11161c; border: 1px solid #26313d; border-radius: 14px;
      padding: 20px; box-shadow: 0 8px 24px rgba(0,0,0,.25);
    }
    h1 { margin: 0 0 8px; font-size: 28px; }
    p { margin: 8px 0 16px; color: #b7c3d0; }
    .grid { display: grid; gap: 10px; grid-template-columns: repeat(auto-fit,minmax(260px,1fr)); }
    a {
      display: block; text-decoration: none; color: #d9ecff;
      background: #16202a; border: 1px solid #334455; border-radius: 10px;
      padding: 12px 14px;
    }
    a:hover { border-color: #61dafb; background: #1b2733; }
    code {
      display: block; margin-top: 14px; white-space: pre-wrap;
      background: #0e141a; border: 1px solid #2c3946; border-radius: 10px;
      padding: 12px; color: #9bd3ff;
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>🥓 TrackingBacon</h1>
      <p>Roleplay AI + Language Learning monitor. Use links below to run and inspect signals.</p>
      <div class="grid">
        <a href="/docs"><strong>API Docs</strong><br/>Swagger UI</a>
        <a href="/health"><strong>Health</strong><br/>GET /health</a>
        <a href="/plan"><strong>Plan</strong><br/>GET /plan</a>
        <a href="/products"><strong>Products</strong><br/>GET /products?limit=100</a>
      </div>
      <code>Run Sniffer:
curl -X POST http://127.0.0.1:8000/sniffer/run</code>
    </div>
  </div>
</body>
</html>
        """.strip()
    )


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    return Response(status_code=204)


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
