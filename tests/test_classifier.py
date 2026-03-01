from app.classifier import infer_licensing, infer_region, infer_status, is_roleplay_language_product, normalize_text


def test_roleplay_and_language_detection():
    text = normalize_text("Character roleplay tutor", "Language learning with speaking practice")
    assert is_roleplay_language_product(text)


def test_status_inference_priority():
    text = "launched today after private beta"
    assert infer_status(text) == "launched"


def test_region_inference():
    text = "station f startup got gdpr approval"
    assert infer_region(text, "unknown") == "europe"


def test_licensing_inference():
    text = "MIT license open source"
    assert infer_licensing(text, "https://github.com/a/b") == "open_source"


def test_region_inference_for_china():
    text = "New roleplay tutor trend on mp.weixin and 小红书 in 中国 market"
    assert infer_region(text.lower(), "unknown") == "china"
