from __future__ import annotations

from app.types import RawSignal


class MockGlobalConnector:
    """Bootstrapping connector with region-tagged examples.

    Replace this with real APIs/scrapers for X, HackerNews, Discord, Crunchbase, Appfigures, etc.
    """

    name = "mock_global"

    def fetch(self) -> list[RawSignal]:
        return [
            RawSignal(
                title="Show HN: Roleplay English tutor in private beta",
                url="https://example.com/na-roleplay-beta",
                summary="Character-based speaking practice app, private beta waitlist, YC alumni project.",
                platform="hacker_news",
                region_hint="north_america",
                tags=["show_hn", "beta"],
            ),
            RawSignal(
                title="AI英会話 キャラクタAI app launched on iOS",
                url="https://example.com/jp-launched",
                summary="Japanese roleplay conversation tutor launched with vocabulary summary.",
                platform="x_twitter_jp",
                region_hint="japan_korea",
                tags=["ai英会話", "launched"],
            ),
            RawSignal(
                title="Berlin startup announces GDPR-ready AI conversation coach",
                url="https://example.com/eu-gdpr",
                summary="Language learning roleplay assistant enters beta with school partnership pilot.",
                platform="eu_startups",
                region_hint="europe",
                tags=["gdpr", "beta"],
            ),
            RawSignal(
                title="Open-source roleplay language tutor framework gets 1k stars/day",
                url="https://github.com/example/rp-language-tutor",
                summary="MIT licensed framework for roleplay-based language learning scenarios.",
                platform="github",
                region_hint="global_open_source",
                tags=["open-source", "stars-spike"],
            ),
        ]
