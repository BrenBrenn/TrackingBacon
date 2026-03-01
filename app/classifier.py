from __future__ import annotations

from app.config import LANGUAGE_TERMS, ROLEPLAY_TERMS, STATUS_TERMS


def normalize_text(*parts: str) -> str:
    return "\n".join(p for p in parts if p).lower()


def is_roleplay_language_product(text: str) -> bool:
    roleplay_hit = any(term in text for term in ROLEPLAY_TERMS)
    language_hit = any(term in text for term in LANGUAGE_TERMS)
    return roleplay_hit and language_hit


def infer_status(text: str) -> str:
    for status in ("launched", "beta", "in_production"):
        if any(term in text for term in STATUS_TERMS[status]):
            return status
    return "unknown"


def infer_licensing(text: str, url: str) -> str:
    target = f"{text}\n{url}".lower()
    if any(k in target for k in ["github.com", "gitlab.com", "apache-2.0", "mit license", "open source", "开源"]):
        return "open_source"
    if any(k in target for k in ["pricing", "subscribe", "pro plan", "closed source", "enterprise"]):
        return "closed_source"
    return "unknown"


def infer_region(text: str, region_hint: str) -> str:
    hint = (region_hint or "").lower()
    if hint in {"north_america", "japan_korea", "europe", "china", "global_open_source"}:
        return hint

    if any(k in text for k in ["zhihu", "juejin", "wechat", "weixin", "mp.weixin", "xiaohongshu", "bilibili", "36kr", "cn", "中国", "中文"]):
        return "china"
    if any(k in text for k in ["naver", "ai 튜터", "英会話", "キャラクタ"]):
        return "japan_korea"
    if any(k in text for k in ["gdpr", "station f", "eu-startups", "berlin", "paris"]):
        return "europe"
    if any(k in text for k in ["hacker news", "yc", "product hunt"]):
        return "north_america"
    return "unknown"
