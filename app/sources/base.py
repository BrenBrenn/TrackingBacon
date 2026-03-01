from __future__ import annotations

from typing import Protocol

from app.types import RawSignal


class SourceConnector(Protocol):
    name: str

    def fetch(self) -> list[RawSignal]:
        ...
