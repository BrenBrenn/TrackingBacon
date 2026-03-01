# TrackingBacon

TrackingBacon monitors newly emerging products that combine **Roleplay AI + Language Learning**.

It supports global coverage including:
- China-focused channels
- North America innovation channels
- Japan/Korea persona-heavy ecosystems
- Europe multi-language startup ecosystems
- Global open-source infrastructure signals

## Product Concepts

### The Sniffer
The Sniffer captures and normalizes product signals from region-specific channels.

Current implementation includes:
- Region-aware source plan (`/plan` API)
- Classification for lifecycle stage (`in_production`, `beta`, `launched`)
- Licensing classification (`open_source`, `closed_source`)
- Region inference (`north_america`, `japan_korea`, `europe`, `china`, `global_open_source`)

### The Sizzle
The Sizzle emits high-priority alerts when market-specific heat signals appear.

Examples:
- North America: HN frontpage / Product Hunt top ranking
- Japan/Korea: Shorts/TikTok-driven UGC surge
- Europe: GDPR + education partnership milestone
- Global OSS: GitHub stars spike (+1000 / 24h)
- China (CN): signals from `zhihu`, `juejin`, `wechat` / `weixin` / `mp.weixin`, `xiaohongshu`, `bilibili`, `36kr`, `中国`, `中文`, and `cn`

## How to Use

### 1) Start the service

**macOS / Linux (bash)**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Windows (PowerShell)**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

If you see `-m: The term '-m' is not recognized`, it means the `python` (or `py`) executable was omitted. Use `py -m venv .venv` instead of just `-m venv .venv`.

### 2) Check health

```bash
curl http://127.0.0.1:8000/health
```

### 3) View the monitoring plan

```bash
curl http://127.0.0.1:8000/plan
```

### 4) Run one Sniffer cycle

```bash
curl -X POST http://127.0.0.1:8000/sniffer/run
```

### 5) Inspect detected products

```bash
curl http://127.0.0.1:8000/products
```

Tip: to verify CN detection, check product items where `region` is `china`.

## Project Structure

- `app/config.py`: Regional source and sizzle configuration
- `app/classifier.py`: Roleplay-language matching and metadata inference
- `app/sniffer.py`: End-to-end ingestion pipeline
- `app/sizzle.py`: Regional heat-event detector
- `app/repository.py`: SQLite persistence layer
- `app/main.py`: FastAPI endpoints
- `tests/`: Unit tests for classifiers and ingestion

## Next Steps

- Replace mock connector with real connectors (X/HN/Discord/Crunchbase/Appfigures)
- Add deduplication via semantic hashing
- Add scheduled workers (APScheduler/Celery)
- Add webhook dispatchers for Telegram/Discord/Feishu/WeCom
