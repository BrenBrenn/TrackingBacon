from __future__ import annotations

from dataclasses import dataclass

from app.config import REGIONAL_SIZZLE_SIGNALS


@dataclass(slots=True)
class SizzleEvent:
    region: str
    weight: str
    reason: str
    product_name: str
    product_url: str


def detect_sizzle(record: dict) -> list[SizzleEvent]:
    events: list[SizzleEvent] = []
    region = record["region"]
    name = record["name"]

    if region == "north_america" and any(k in record["summary"].lower() for k in ["hacker news", "product hunt"]):
        events.append(SizzleEvent(region, "critical", REGIONAL_SIZZLE_SIGNALS[region][0], name, record["url"]))

    if region == "japan_korea" and any(k in record["summary"].lower() for k in ["shorts", "tiktok", "hashtag"]):
        events.append(SizzleEvent(region, "high", REGIONAL_SIZZLE_SIGNALS[region][0], name, record["url"]))

    if region == "europe" and any(k in record["summary"].lower() for k in ["gdpr", "education authority", "school partnership"]):
        events.append(SizzleEvent(region, "medium", REGIONAL_SIZZLE_SIGNALS[region][0], name, record["url"]))

    if record["licensing"] == "open_source" and any(k in record["summary"].lower() for k in ["1k stars", "1000 stars"]):
        events.append(
            SizzleEvent("global_open_source", "critical", REGIONAL_SIZZLE_SIGNALS["global_open_source"][0], name, record["url"])
        )

    return events
