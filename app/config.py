"""Region-specific monitoring configuration for The Global Sniffer and The Regional Sizzle."""

REGIONAL_SOURCES: dict[str, list[str]] = {
    "north_america": [
        "Hacker News (Show HN)",
        "Product Hunt",
        "Discord communities (Character.ai, JanitorAI, YC alumni)",
        "Substack/Beehiiv AI newsletters",
    ],
    "japan_korea": [
        "X / Twitter JP hashtags (#AI英会話, #キャラクタAI)",
        "note.com maker posts",
        "Naver Blog/Cafe (AI 튜터, 회화)",
        "YouTube Shorts / TikTok trends",
    ],
    "europe": [
        "Station F / French Tech announcements",
        "EU-Startups funding news",
        "Berlin/Paris accelerator updates",
        "Local education partnership announcements",
    ],
    "china": [
        "Zhihu",
        "Juejin",
        "Gitee/GitCode",
        "WeChat public article aggregators",
    ],
    "global_open_source": [
        "GitHub trending/new repos",
        "GitLab explore",
        "Hugging Face spaces/models",
    ],
}

ROLEPLAY_TERMS = [
    "roleplay",
    "character ai",
    "persona",
    "npc",
    "story mode",
    "剧情",
    "角色扮演",
    "キャラクタ",
]

LANGUAGE_TERMS = [
    "language learning",
    "speaking practice",
    "pronunciation",
    "vocabulary",
    "grammar",
    "conversation tutor",
    "语言学习",
    "口语",
    "会话",
    "英会話",
]

STATUS_TERMS: dict[str, list[str]] = {
    "in_production": ["waitlist", "coming soon", "building", "prototype", "roadmap", "开发中"],
    "beta": ["beta", "private beta", "公测", "内测"],
    "launched": ["launched", "launch", "available now", "上线", "发布"],
}

REGIONAL_SIZZLE_SIGNALS: dict[str, list[str]] = {
    "north_america": [
        "Hacker News frontpage",
        "Product Hunt weekly top 5",
    ],
    "japan_korea": [
        "TikTok or YouTube Shorts UGC spike",
        "X/Twitter hashtag velocity spike",
    ],
    "europe": [
        "GDPR compliance milestone",
        "Partnership with local education authority",
    ],
    "global_open_source": [
        "GitHub stars +1000 within 24h",
    ],
}
