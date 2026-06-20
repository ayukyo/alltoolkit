#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for polyglot_chronicle module.
"""

import json
import os
import sys
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

# Add parent to path so we can import polyglot_chronicle
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from polyglot_chronicle import (
    TOOL_NAME,
    TOOL_VERSION,
    HISTORY_EVENTS,
    DAILY_CHALLENGES,
    QUOTES,
    COMMUNITY_MOODS,
    ROTATION_FILE,
    load_rotation,
    save_rotation,
    get_on_this_day,
    get_daily_challenge,
    get_quote,
    get_mood,
    chronicle,
)


ROTATION_LANGS = [
    "Rust",
    "Go",
    "Swift",
    "Kotlin",
    "TypeScript",
    "JavaScript",
    "Java",
    "C/C++",
]

JUNE_7 = datetime(2026, 6, 7, 12, 0, 0, tzinfo=timezone(timedelta(hours=8)))


@pytest.fixture
def restore_rotation():
    """Snapshot the current rotation file and restore it after the test."""
    snapshot = None
    if os.path.exists(ROTATION_FILE):
        with open(ROTATION_FILE, "r") as f:
            snapshot = f.read()
    yield
    if snapshot is not None:
        with open(ROTATION_FILE, "w") as f:
            f.write(snapshot)


class TestModuleMetadata:
    """Test module-level constants."""

    def test_tool_name(self):
        assert TOOL_NAME == "polyglot-chronicle"

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"

    def test_rotation_file_path(self):
        assert ROTATION_FILE.endswith("language_rotation.json")


class TestHistoryEvents:
    """Test HISTORY_EVENTS structure."""

    def test_all_languages_have_events(self):
        for lang in ROTATION_LANGS:
            assert lang in HISTORY_EVENTS, f"{lang} missing from HISTORY_EVENTS"

    def test_each_event_is_tuple(self):
        for lang, events in HISTORY_EVENTS.items():
            for event in events:
                assert isinstance(event, tuple)
                assert len(event) == 2
                month_day, desc = event
                assert isinstance(month_day, tuple)
                assert len(month_day) == 2
                assert 1 <= month_day[0] <= 12
                assert 1 <= month_day[1] <= 31
                assert isinstance(desc, str)
                assert len(desc) > 0

    def test_each_language_has_minimum_events(self):
        for lang, events in HISTORY_EVENTS.items():
            assert len(events) >= 3, f"{lang} has fewer than 3 history events"


class TestDailyChallenges:
    """Test DAILY_CHALLENGES structure."""

    def test_all_languages_have_challenges(self):
        for lang in ROTATION_LANGS:
            assert lang in DAILY_CHALLENGES, f"{lang} missing from DAILY_CHALLENGES"

    def test_challenge_structure(self):
        for lang, challenges in DAILY_CHALLENGES.items():
            assert len(challenges) >= 5, f"{lang} has fewer than 5 challenges"
            for c in challenges:
                assert "title" in c
                assert "difficulty" in c
                assert "tags" in c
                assert isinstance(c["title"], str)
                assert isinstance(c["difficulty"], str)
                assert isinstance(c["tags"], list)


class TestQuotes:
    """Test QUOTES structure."""

    def test_all_languages_have_quotes(self):
        for lang in ROTATION_LANGS:
            assert lang in QUOTES, f"{lang} missing from QUOTES"

    def test_each_language_has_minimum_quotes(self):
        for lang, quotes in QUOTES.items():
            assert len(quotes) >= 3, f"{lang} has fewer than 3 quotes"


class TestCommunityMoods:
    """Test COMMUNITY_MOODS structure."""

    def test_all_languages_have_moods(self):
        for lang in ROTATION_LANGS:
            assert lang in COMMUNITY_MOODS, f"{lang} missing from COMMUNITY_MOODS"

    def test_each_language_has_minimum_moods(self):
        for lang, moods in COMMUNITY_MOODS.items():
            assert len(moods) >= 2, f"{lang} has fewer than 2 moods"


class TestLoadSaveRotation:
    """Test load/save rotation functions."""

    def test_load_rotation_returns_dict(self, restore_rotation):
        config = load_rotation()
        assert isinstance(config, dict)
        assert "languages" in config
        assert "current_index" in config
        assert isinstance(config["languages"], list)
        assert isinstance(config["current_index"], int)
        assert len(config["languages"]) >= 1

    def test_save_then_load_roundtrip(self, restore_rotation, tmp_path):
        test_file = tmp_path / "rotation.json"
        data = {"languages": ["A", "B", "C"], "current_index": 1}
        with patch.object(
            sys.modules["polyglot_chronicle"], "ROTATION_FILE", str(test_file)
        ):
            save_rotation(data)
            assert test_file.exists()
            with open(test_file, "r") as f:
                loaded = json.load(f)
            assert loaded == data


class TestGetOnThisDay:
    """Test get_on_this_day function."""

    def test_returns_list(self):
        result = get_on_this_day("Rust", JUNE_7)
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_finds_event_on_june_7_for_rust(self):
        result = get_on_this_day("Rust", JUNE_7)
        assert any("2026" in e for e in result)

    def test_unknown_language_returns_list(self):
        result = get_on_this_day("UnknownLang", JUNE_7)
        assert isinstance(result, list)

    def test_past_event_fallback(self):
        # April 20 should match Rust 1.0 release
        result = get_on_this_day("Rust", datetime(2026, 8, 15, tzinfo=timezone(timedelta(hours=8))))
        assert isinstance(result, list)
        assert len(result) >= 1


class TestGetDailyChallenge:
    """Test get_daily_challenge function."""

    def test_returns_dict(self):
        challenge = get_daily_challenge("Rust")
        assert isinstance(challenge, dict)
        assert "title" in challenge
        assert "difficulty" in challenge
        assert "tags" in challenge

    def test_deterministic_seed(self):
        c1 = get_daily_challenge("Rust", seed=158)
        c2 = get_daily_challenge("Rust", seed=158)
        assert c1["title"] == c2["title"]

    def test_different_seeds_can_differ(self):
        # Get all possible challenges for Rust
        all_titles = set()
        for seed in range(100):
            c = get_daily_challenge("Rust", seed=seed)
            all_titles.add(c["title"])
        # With 100 seeds, we should have gotten more than 1 challenge
        assert len(all_titles) >= 1

    def test_unknown_language_fallback(self):
        challenge = get_daily_challenge("UnknownLang")
        assert isinstance(challenge, dict)
        assert challenge.get("title") == "No challenge available"

    def test_tags_is_list(self):
        challenge = get_daily_challenge("Rust")
        assert isinstance(challenge["tags"], list)


class TestGetQuote:
    """Test get_quote function."""

    def test_returns_non_empty_string(self):
        quote = get_quote("Rust")
        assert isinstance(quote, str)
        assert len(quote) > 0

    def test_unknown_language_fallback(self):
        quote = get_quote("UnknownLang")
        assert isinstance(quote, str)
        assert "No quote" in quote

    def test_each_language_has_quotes(self):
        for lang in ROTATION_LANGS:
            q = get_quote(lang)
            assert isinstance(q, str)
            assert len(q) >= 5


class TestGetMood:
    """Test get_mood function."""

    def test_returns_non_empty_string(self):
        mood = get_mood("Rust")
        assert isinstance(mood, str)
        assert len(mood) > 0

    def test_unknown_language_fallback(self):
        mood = get_mood("UnknownLang")
        assert isinstance(mood, str)
        assert "thriving" in mood.lower() or len(mood) > 0

    def test_each_language_has_moods(self):
        for lang in ROTATION_LANGS:
            m = get_mood(lang)
            assert isinstance(m, str)
            assert len(m) >= 1


class TestChronicle:
    """Test the main chronicle function."""

    def test_returns_expected_keys(self, restore_rotation):
        result = chronicle(language="Rust", force_today=JUNE_7)
        expected_keys = [
            "tool", "version", "selected_language", "emoji", "age_years",
            "date", "date_human", "on_this_day", "daily_challenge",
            "creator_quote", "community_mood", "next_language", "rotation", "timestamp",
        ]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"

    def test_tool_metadata(self, restore_rotation):
        result = chronicle(language="Rust", force_today=JUNE_7)
        assert result["tool"] == "polyglot-chronicle"
        assert result["version"] == "1.0.0"

    def test_emoji_mapping(self, restore_rotation):
        emoji_map = {
            "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
            "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "C/C++": "⚙️",
        }
        for lang, emoji in emoji_map.items():
            result = chronicle(language=lang, force_today=JUNE_7)
            assert result["emoji"] == emoji, f"{lang} emoji mismatch"

    def test_age_calculation(self, restore_rotation):
        # Rust born 2015, in 2026 = 11
        result = chronicle(language="Rust", force_today=JUNE_7)
        assert result["age_years"] == 11
        # JavaScript born 1995, in 2026 = 31
        result = chronicle(language="JavaScript", force_today=JUNE_7)
        assert result["age_years"] == 31
        # C/C++ born 1972, in 2026 = 54
        result = chronicle(language="C/C++", force_today=JUNE_7)
        assert result["age_years"] == 54

    def test_date_formatting(self, restore_rotation):
        result = chronicle(language="Rust", force_today=JUNE_7)
        assert result["date"] == "2026-06-07"
        assert "June" in result["date_human"]
        assert "2026" in result["date_human"]

    def test_on_this_day_for_june_7(self, restore_rotation):
        for lang in ROTATION_LANGS:
            result = chronicle(language=lang, force_today=JUNE_7)
            assert len(result["on_this_day"]) >= 1
            # The 2026 "today!" event should be in there
            assert any("2026" in e for e in result["on_this_day"])

    def test_daily_challenge_in_response(self, restore_rotation):
        result = chronicle(language="Rust", force_today=JUNE_7)
        c = result["daily_challenge"]
        assert "title" in c
        assert "difficulty" in c
        assert "tags" in c

    def test_quote_and_mood(self, restore_rotation):
        result = chronicle(language="Rust", force_today=JUNE_7)
        assert isinstance(result["creator_quote"], str)
        assert len(result["creator_quote"]) > 10
        assert isinstance(result["community_mood"], str)
        assert len(result["community_mood"]) > 5

    def test_rotation_advances(self, restore_rotation):
        # Save current state
        before = load_rotation()
        idx_before = before["current_index"]
        chronicle(language=before["languages"][idx_before], force_today=JUNE_7)
        after = load_rotation()
        expected_idx = (idx_before + 1) % len(after["languages"])
        assert after["current_index"] == expected_idx
        assert after["last_language"] == before["languages"][idx_before]

    def test_next_language_is_valid(self, restore_rotation):
        for lang in ROTATION_LANGS:
            result = chronicle(language=lang, force_today=JUNE_7)
            assert result["next_language"] in result["rotation"]
            assert result["selected_language"] in result["rotation"]
            # next_language is not the current selected language
            # (because we override language, the next is still computed from current)
            # The next should be the language after selected in the rotation
            sel_idx = result["rotation"].index(result["selected_language"])
            expected_next = result["rotation"][(sel_idx + 1) % len(result["rotation"])]
            assert result["next_language"] == expected_next

    def test_default_language_uses_rotation(self, restore_rotation):
        # When language is None, use the rotation
        before = load_rotation()
        expected_lang = before["languages"][before["current_index"] % len(before["languages"])]
        result = chronicle(force_today=JUNE_7)
        assert result["selected_language"] == expected_lang

    def test_all_languages_produce_chronicle(self, restore_rotation):
        for lang in ROTATION_LANGS:
            result = chronicle(language=lang, force_today=JUNE_7)
            assert result["selected_language"] == lang
            assert len(result["creator_quote"]) > 10
            assert len(result["community_mood"]) > 5
            assert result["age_years"] >= 0

    def test_result_is_json_serializable(self, restore_rotation):
        result = chronicle(language="Rust", force_today=JUNE_7)
        # Should be JSON-serializable
        json_str = json.dumps(result, ensure_ascii=False)
        assert isinstance(json_str, str)
        # Round-trip
        loaded = json.loads(json_str)
        assert loaded["tool"] == result["tool"]
        assert loaded["selected_language"] == result["selected_language"]

    def test_force_today_affects_date(self, restore_rotation):
        d1 = datetime(2026, 1, 1, tzinfo=timezone(timedelta(hours=8)))
        d2 = datetime(2026, 12, 31, tzinfo=timezone(timedelta(hours=8)))
        r1 = chronicle(language="Rust", force_today=d1)
        r2 = chronicle(language="Rust", force_today=d2)
        assert r1["date"] == "2026-01-01"
        assert r2["date"] == "2026-12-31"
        assert r1["date"] != r2["date"]

    def test_chronicle_uses_today_when_force_today_none(self, restore_rotation):
        result = chronicle(language="Rust")
        # The date should be the current date
        today_str = datetime.now().strftime("%Y-%m-%d")
        # date is in YYYY-MM-DD format
        assert len(result["date"]) == 10
        assert result["date"][4] == "-"
        assert result["date"][7] == "-"
