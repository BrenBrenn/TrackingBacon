from __future__ import annotations

from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse

from app.config import REGIONAL_SOURCES, REGIONAL_SIZZLE_SIGNALS
from app.repository import init_db, list_products
from app.sizzle import send_webhook_alert
from app.sniffer import run_sniffer_once

app = FastAPI(title="TrackingBacon", version="0.1.0")
LAST_RUN_REPORT: dict = {
    "report": "No run yet. Click 'Run Sniffer Now' on the homepage.",
    "inserted": 0,
    "updated": 0,
    "sizzle_events": [],
}


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
    body { margin: 0; font-family: Inter, Segoe UI, Arial, sans-serif; background: #0b0d10; color: #e6edf3; }
    .wrap { max-width: 980px; margin: 24px auto; padding: 0 16px; }
    .card { background: #11161c; border: 1px solid #26313d; border-radius: 14px; padding: 20px; box-shadow: 0 8px 24px rgba(0,0,0,.25); }
    h1 { margin: 0 0 8px; font-size: 30px; }
    p { margin: 8px 0 16px; color: #b7c3d0; }
    .grid { display: grid; gap: 10px; grid-template-columns: repeat(auto-fit,minmax(220px,1fr)); }
    a { display: block; text-decoration: none; color: #d9ecff; background: #16202a; border: 1px solid #334455; border-radius: 10px; padding: 12px 14px; }
    a:hover { border-color: #61dafb; background: #1b2733; }
    .controls { display: grid; gap: 10px; grid-template-columns: 1fr auto auto; margin-top: 16px; }
    input, button { border-radius: 10px; border: 1px solid #334455; background: #0e141a; color: #e6edf3; padding: 10px 12px; font-size: 14px; }
    button { cursor: pointer; background: #173148; }
    button:hover { background: #20405c; }
    .report { margin-top: 12px; white-space: pre-wrap; background: #0e141a; border: 1px solid #2c3946; border-radius: 10px; padding: 12px; color: #9bd3ff; min-height: 120px; }
    .hint { color: #95a8ba; font-size: 13px; margin-top: 6px; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>🥓 TrackingBacon</h1>
      <p>Run once manually, get an instant report, and optionally send a reminder to webhook.</p>
      <div class="grid">
        <a href="/docs"><strong>API Docs</strong><br/>Swagger UI</a>
        <a href="/health"><strong>Health</strong><br/>GET /health</a>
        <a href="/plan"><strong>Plan</strong><br/>GET /plan</a>
        <a href="/products"><strong>Products</strong><br/>GET /products?limit=100</a>
      </div>
      <div class="controls">
        <input id="webhook" placeholder="Optional webhook URL for reminder (The Sizzle)" />
        <button id="run-btn">Run Sniffer Now</button>
        <button id="send-btn">Send Reminder</button>
      </div>
      <div class="hint">Tip: Click "Run Sniffer Now" first, then "Send Reminder" if you configured webhook.</div>
      <div id="report" class="report">No run yet. Click \"Run Sniffer Now\".</div>
    </div>
  </div>
  <script>
    const reportEl = document.getElementById('report');
    const runBtn = document.getElementById('run-btn');
    const sendBtn = document.getElementById('send-btn');
    const webhookInput = document.getElementById('webhook');

    async function loadLatestReport() {
      const res = await fetch('/report/latest');
      const data = await res.json();
      reportEl.textContent = data.report || JSON.stringify(data, null, 2);
    }

    runBtn.addEventListener('click', async () => {
      runBtn.disabled = true;
      reportEl.textContent = 'Running sniffer...';
      try {
        const res = await fetch('/sniffer/run', { method: 'POST' });
        const data = await res.json();
        reportEl.textContent = data.report || JSON.stringify(data, null, 2);
      } catch (e) {
        reportEl.textContent = 'Run failed: ' + e;
      } finally {
        runBtn.disabled = false;
      }
    });

    sendBtn.addEventListener('click', async () => {
      const webhook = webhookInput.value.trim();
      const q = webhook ? '?webhook_url=' + encodeURIComponent(webhook) : '';
      const res = await fetch('/alerts/test' + q, { method: 'POST' });
      const data = await res.json();
      reportEl.textContent += '\n\nReminder result:\n' + JSON.stringify(data, null, 2);
    });

    loadLatestReport();
  </script>
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
    result = run_sniffer_once()
    LAST_RUN_REPORT.update(result)
    return result


@app.get("/report/latest")
def report_latest() -> dict:
    return LAST_RUN_REPORT


@app.post("/alerts/test")
def alerts_test(webhook_url: str | None = None) -> dict:
    if not webhook_url:
        return {
            "sent": False,
            "reason": "No webhook_url provided. Add one in homepage input or query param.",
            "preview": LAST_RUN_REPORT.get("report", "No report yet."),
        }
    return send_webhook_alert(webhook_url=webhook_url, report_text=LAST_RUN_REPORT.get("report", "No report yet."))


@app.get("/products")
def products(limit: int = 100) -> dict:
    return {"items": list_products(limit=limit)}
