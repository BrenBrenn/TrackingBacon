from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

Status = Literal["in_production", "beta", "launched", "unknown"]
Licensing = Literal["open_source", "closed_source", "unknown"]


@dataclass(slots=True)
class RawSignal:
    title: str
    url: str
    summary: str
    platform: str
    region_hint: str = "unknown"
    tags: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ProductRecord:
    name: str
    url: str
    summary: str
    source_platform: str
    region: str
    status: Status
    licensing: Licensing
    tags: list[str]
    first_seen_at: datetime
    last_seen_at: datetime
