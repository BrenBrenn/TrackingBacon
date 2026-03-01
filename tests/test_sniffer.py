from app.repository import DB_PATH, init_db, list_products
from app.sniffer import run_sniffer_once


def setup_module():
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db()


def test_sniffer_ingestion_and_sizzle():
    result = run_sniffer_once()
    assert result["inserted"] >= 1
    assert isinstance(result["sizzle_events"], list)

    items = list_products()
    assert len(items) >= 1
    assert any("roleplay_ai" in item["tags"] for item in items)
