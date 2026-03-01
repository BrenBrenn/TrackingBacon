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

## Why this update (vs China-only setup)

This version expands the strategy into a **global matrix** so you can avoid blind spots:

1. **North America** catches earliest technical launches.
2. **Japan/Korea** catches roleplay-native consumer behavior.
3. **Europe** catches compliance-first education rollouts.
4. **Global OSS** catches foundational framework shifts.


## China (CN) Coverage

Yes — CN detection is supported.

Current CN detection signals include:
- Region hint from connector: `china`
- Keyword/domain heuristics: `zhihu`, `juejin`, `wechat`, `weixin`, `mp.weixin`, `xiaohongshu`, `bilibili`, `36kr`, `中国`, `中文`, and `cn`

How to verify quickly:
1. Call `POST /sniffer/run`
2. Call `GET /products`
3. Check items where `region` equals `china`

> Note: current ingestion uses a mock connector. Real CN source connectors should be added next (e.g., Zhihu/Juejin/WeChat/Gitee feeds) to improve recall.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pytest
uvicorn app.main:app --reload
```

Run one sniffer cycle:

```bash
curl -X POST http://127.0.0.1:8000/sniffer/run
```

Inspect current product records:

```bash
curl http://127.0.0.1:8000/products
```

Check the global monitoring plan:

```bash
curl http://127.0.0.1:8000/plan
```

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
