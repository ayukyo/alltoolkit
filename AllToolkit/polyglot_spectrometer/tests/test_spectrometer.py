"""Test suite for polyglot_spectrometer."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from src import (
    spectrometer, analyze_language, format_spectrometer,
    load_rotation, save_rotation, ROTATION_ORDER, HELLO_WORLD,
    SPECTRAL_BANDS, BAR_CHARS, ANALYZERS,
)


def test_rotation_file():
    config = load_rotation()
    assert isinstance(config, dict)
    assert "languages" in config
    assert "current_index" in config


def test_rotation_order():
    for lang in ROTATION_ORDER:
        assert lang in ROTATION_ORDER


def test_hello_world():
    for lang in ROTATION_ORDER:
        assert lang in HELLO_WORLD
        assert bool(HELLO_WORLD[lang])


def test_spectral_bands():
    assert len(SPECTRAL_BANDS) == 7
    for band in SPECTRAL_BANDS:
        assert "id" in band
        assert "name" in band
        assert "emoji" in band


def test_bar_chars():
    assert len(BAR_CHARS) == 11
    assert BAR_CHARS[0] == " "


def test_analyzers():
    sample = HELLO_WORLD["Rust"]
    for band_id, analyzer in ANALYZERS.items():
        result = analyzer(sample)
        assert isinstance(result, dict)
        assert "score" in result
        assert 0 <= result["score"] <= 10
        assert "bar" in result
        assert "detail" in result


def test_analyze_language():
    for lang in HELLO_WORLD:
        m = analyze_language(lang)
        assert len(m["bands"]) == 7
        assert "composite_score" in m
        assert "source_code" in m
        assert all(0 <= b["score"] <= 10 for b in m["bands"])
        assert all("bar" in b for b in m["bands"])


def test_spectrometer_rotation():
    cfg_before = load_rotation()
    idx_before = cfg_before["current_index"]
    lang_before = cfg_before["languages"][idx_before % len(cfg_before["languages"])]
    result = spectrometer()
    cfg_after = load_rotation()
    idx_after = cfg_after["current_index"]
    assert idx_after == (idx_before + 1) % len(cfg_before["languages"])
    assert result["rotation_advanced"] is True
    assert result["language"] == lang_before
    assert "next_language" in result
    assert "next_index" in result


def test_format_spectrometer():
    m = analyze_language("Rust")
    formatted = format_spectrometer(m)
    assert isinstance(formatted, str)
    assert formatted.startswith("╔")
    assert formatted.rstrip().endswith("╝")
    assert "Rust" in formatted
    assert "│" in formatted


def test_unknown_language():
    try:
        analyze_language("Brainfuck")
        assert False, "should have raised ValueError"
    except ValueError:
        pass


def test_composite_score_range():
    for lang in HELLO_WORLD:
        m = analyze_language(lang)
        cs = m["composite_score"]
        assert 0.0 <= cs <= 10.0


def test_rotation_wrap():
    cfg = load_rotation()
    langs = cfg["languages"]
    idx = cfg["current_index"]
    for _ in range(len(langs) + 1):
        cfg = load_rotation()
        idx = cfg["current_index"]
        lang = cfg["languages"][idx % len(langs)]
        cfg["current_index"] = (idx + 1) % len(langs)
        cfg["last_language"] = lang
        from datetime import datetime, timezone
        cfg["updated_at"] = datetime.now(timezone.utc).isoformat()
        save_rotation(cfg)
    cfg_final = load_rotation()
    assert cfg_final["current_index"] == (idx + len(langs) + 1) % len(langs)


if __name__ == "__main__":
    import traceback

    tests = [
        test_rotation_file,
        test_rotation_order,
        test_hello_world,
        test_spectral_bands,
        test_bar_chars,
        test_analyzers,
        test_analyze_language,
        test_spectrometer_rotation,
        test_format_spectrometer,
        test_unknown_language,
        test_composite_score_range,
        test_rotation_wrap,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  ✅ {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {test.__name__}: {e}")
            traceback.print_exc()
            failed += 1

    print(f"\n{'='*50}")
    if failed:
        print(f"❌ {failed} test(s) failed, {passed} passed")
        sys.exit(1)
    else:
        print(f"✅ All {passed} tests passed!")
        sys.exit(0)
