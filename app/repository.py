from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path("trackingbacon.db")


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def connect():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS product_signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                summary TEXT NOT NULL,
                source_platform TEXT NOT NULL,
                region TEXT NOT NULL,
                status TEXT NOT NULL,
                licensing TEXT NOT NULL,
                tags TEXT NOT NULL,
                first_seen_at TEXT NOT NULL,
                last_seen_at TEXT NOT NULL
            );
            """
        )
        conn.commit()


def upsert_product(record: dict) -> tuple[str, dict]:
    now = utcnow()
    with connect() as conn:
        row = conn.execute(
            "SELECT id, status, licensing FROM product_signals WHERE url = ?",
            (record["url"],),
        ).fetchone()

        if row:
            conn.execute(
                """
                UPDATE product_signals
                SET name = ?, summary = ?, source_platform = ?, region = ?, status = ?, licensing = ?, tags = ?, last_seen_at = ?
                WHERE url = ?
                """,
                (
                    record["name"],
                    record["summary"],
                    record["source_platform"],
                    record["region"],
                    record["status"],
                    record["licensing"],
                    json.dumps(record["tags"], ensure_ascii=False),
                    now,
                    record["url"],
                ),
            )
            conn.commit()
            return "updated", record

        conn.execute(
            """
            INSERT INTO product_signals
                (name, url, summary, source_platform, region, status, licensing, tags, first_seen_at, last_seen_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["name"],
                record["url"],
                record["summary"],
                record["source_platform"],
                record["region"],
                record["status"],
                record["licensing"],
                json.dumps(record["tags"], ensure_ascii=False),
                now,
                now,
            ),
        )
        conn.commit()
        return "inserted", record


def list_products(limit: int = 100) -> list[dict]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT name, url, summary, source_platform, region, status, licensing, tags, first_seen_at, last_seen_at
            FROM product_signals
            ORDER BY last_seen_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [
        {
            "name": row[0],
            "url": row[1],
            "summary": row[2],
            "source_platform": row[3],
            "region": row[4],
            "status": row[5],
            "licensing": row[6],
            "tags": json.loads(row[7]),
            "first_seen_at": row[8],
            "last_seen_at": row[9],
        }
        for row in rows
    ]
