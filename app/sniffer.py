from __future__ import annotations

from datetime import datetime, timezone

from app.classifier import infer_licensing, infer_region, infer_status, is_roleplay_language_product, normalize_text
from app.repository import upsert_product
from app.sources.mock_global import MockGlobalConnector
from app.sizzle import detect_sizzle


def _build_run_report(inserted: int, updated: int, sizzle_events: list[dict]) -> str:
    now = datetime.now(timezone.utc).isoformat()
    lines = [
        f"TrackingBacon Run Report ({now})",
        f"- inserted: {inserted}",
        f"- updated: {updated}",
        f"- sizzle_events: {len(sizzle_events)}",
    ]

    if sizzle_events:
        lines.append("- top events:")
        for event in sizzle_events[:5]:
            lines.append(
                f"  * [{event['weight']}] {event['region']} | {event['reason']} | {event['product_name']} ({event['product_url']})"
            )

    return "\n".join(lines)


def run_sniffer_once() -> dict:
    connector = MockGlobalConnector()
    inserted = 0
    updated = 0
    sizzle_events: list[dict] = []

    for raw in connector.fetch():
        text = normalize_text(raw.title, raw.summary)
        if not is_roleplay_language_product(text):
            continue

        record = {
            "name": raw.title,
            "url": raw.url,
            "summary": raw.summary,
            "source_platform": raw.platform,
            "region": infer_region(text, raw.region_hint),
            "status": infer_status(text),
            "licensing": infer_licensing(text, raw.url),
            "tags": sorted(set([*raw.tags, "roleplay_ai", "language_learning"])),
        }

        action, persisted = upsert_product(record)
        if action == "inserted":
            inserted += 1
        else:
            updated += 1

        for event in detect_sizzle(persisted):
            sizzle_events.append(
                {
                    "region": event.region,
                    "weight": event.weight,
                    "reason": event.reason,
                    "product_name": event.product_name,
                    "product_url": event.product_url,
                }
            )

    report = _build_run_report(inserted=inserted, updated=updated, sizzle_events=sizzle_events)

    return {
        "inserted": inserted,
        "updated": updated,
        "sizzle_events": sizzle_events,
        "report": report,
    }
