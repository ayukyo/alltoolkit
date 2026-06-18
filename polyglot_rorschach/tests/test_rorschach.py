#!/usr/bin/env python3
"""Tests for polyglot_rorschach module."""

import json
import os
import tempfile
import pytest
from pathlib import Path

# Ensure src/ is importable
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from polyglot_rorschach import (
    TOOL_NAME,
    TOOL_VERSION,
    RORSCHACH_DATA,
    ROTATION_ORDER,
    load_rotation,
    save_rotation,
    get_current_language,
    advance_rotation,
    rorschach,
    format_rorschach,
)


# ─────────────────────────────────────────────────────────────────────────────
# Test Data
# ─────────────────────────────────────────────────────────────────────────────

ALL_LANGUAGES = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]

MOCK_ROTATION = {
    "languages": ALL_LANGUAGES,
    "current_index": 0,
    "last_language": "C/C++",
    "updated_at": "2026-06-18T00:00:00.000000+00:00",
}


# ─────────────────────────────────────────────────────────────────────────────
# Rotation Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestRotation:
    def test_load_rotation_returns_dict(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(MOCK_ROTATION, f)
            path = f.name
        try:
            data = load_rotation(path)
            assert isinstance(data, dict)
            assert "languages" in data
            assert "current_index" in data
            assert data["languages"] == ALL_LANGUAGES
        finally:
            os.unlink(path)

    def test_load_rotation_missing_file(self):
        with pytest.raises(FileNotFoundError):
            load_rotation("/nonexistent/path/rotation.json")

    def test_save_and_load_rotation(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            path = f.name
        try:
            save_rotation(MOCK_ROTATION, path)
            data = load_rotation(path)
            assert data["languages"] == MOCK_ROTATION["languages"]
            assert data["current_index"] == MOCK_ROTATION["current_index"]
        finally:
            os.unlink(path)

    def test_get_current_language(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(MOCK_ROTATION, f)
            path = f.name
        try:
            lang, idx = get_current_language(path)
            assert lang == "Rust"  # current_index=0
            assert idx == 0
        finally:
            os.unlink(path)

    def test_get_current_language_various_indices(self):
        for idx in range(len(ALL_LANGUAGES)):
            mock = dict(MOCK_ROTATION, current_index=idx)
            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                json.dump(mock, f)
                path = f.name
            try:
                lang, i = get_current_language(path)
                assert lang == ALL_LANGUAGES[idx]
                assert i == idx
            finally:
                os.unlink(path)

    def test_advance_rotation_cycles_forward(self):
        for start_idx in range(len(ALL_LANGUAGES)):
            mock = dict(MOCK_ROTATION, current_index=start_idx)
            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                json.dump(mock, f)
                path = f.name
            try:
                new_lang, old_idx, new_idx = advance_rotation(path)
                expected_new_idx = (start_idx + 1) % len(ALL_LANGUAGES)
                assert new_idx == expected_new_idx
                assert new_lang == ALL_LANGUAGES[expected_new_idx]
                assert old_idx == start_idx

                # Verify file was updated
                data = load_rotation(path)
                assert data["current_index"] == expected_new_idx
            finally:
                os.unlink(path)

    def test_advance_rotation_full_cycle(self):
        """All languages are visited before cycle repeats."""
        visited = set()
        mock = dict(MOCK_ROTATION, current_index=0)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(mock, f)
            path = f.name
        try:
            for _ in range(len(ALL_LANGUAGES)):
                new_lang, _, _ = advance_rotation(path)
                visited.add(new_lang)
            assert visited == set(ALL_LANGUAGES)
        finally:
            os.unlink(path)

    def test_advance_rotation_wraps_after_last(self):
        mock = dict(MOCK_ROTATION, current_index=len(ALL_LANGUAGES) - 1)  # last index (7)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(mock, f)
            path = f.name
        try:
            new_lang, old_idx, new_idx = advance_rotation(path)
            assert new_idx == 0  # wraps to 0
            assert new_lang == "Rust"  # first language
        finally:
            os.unlink(path)

    def test_advance_rotation_updates_timestamp(self):
        import re
        mock = dict(MOCK_ROTATION, current_index=0)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(mock, f)
            path = f.name
        try:
            advance_rotation(path)
            data = load_rotation(path)
            assert "updated_at" in data
            # ISO format timestamp
            assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", data["updated_at"])
        finally:
            os.unlink(path)


# ─────────────────────────────────────────────────────────────────────────────
# Core Rorschach Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestRorschachCore:
    def test_all_languages_in_database(self):
        for lang in ALL_LANGUAGES:
            assert lang in RORSCHACH_DATA, f"{lang} not in RORSCHACH_DATA"

    def test_rorschach_returns_all_required_fields(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(dict(MOCK_ROTATION, current_index=0), f)
            path = f.name
        try:
            result = rorschach(rotation_path=path)
            required = [
                "tool", "version", "timestamp", "language",
                "rotation_index", "rotation_order",
                "inkblot_shape", "primary_interpretation",
                "secondary_reveals", "shadow_denial",
                "projection_strength", "response_sequence",
                "signature_phrase", "themes",
            ]
            for field in required:
                assert field in result, f"Missing field: {field}"
        finally:
            os.unlink(path)

    def test_rorschach_language_matches_rotation(self):
        """rorschach() advances rotation so result reflects the NEW index."""
        for idx in range(len(ALL_LANGUAGES)):
            mock = dict(MOCK_ROTATION, current_index=idx)
            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                json.dump(mock, f)
                fname = f.name
            try:
                result = rorschach(rotation_path=fname)
                # After advance: new_index = (idx + 1) % 8, new_lang = languages[new_index]
                expected_new_idx = (idx + 1) % len(ALL_LANGUAGES)
                assert result["language"] == ALL_LANGUAGES[expected_new_idx]
                assert result["rotation_index"] == expected_new_idx
            finally:
                os.unlink(fname)

    def test_rorschach_unknown_language_raises(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(MOCK_ROTATION, f)
            path = f.name
        try:
            with pytest.raises(ValueError, match="Unknown language"):
                rorschach("Python")
        finally:
            os.unlink(path)

    def test_rorschach_with_explicit_language(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(MOCK_ROTATION, f)
            path = f.name
        try:
            result = rorschach("Rust")
            assert result["language"] == "Rust"
            # Index should not change when explicit language given
            data = load_rotation(path)
            assert data["current_index"] == 0
        finally:
            os.unlink(path)

    def test_rorschach_secondary_reveals_count(self):
        for lang in ALL_LANGUAGES:
            data = RORSCHACH_DATA[lang]
            assert isinstance(data["secondary_reveals"], list)
            assert len(data["secondary_reveals"]) == 3, f"{lang} should have 3 secondary reveals"

    def test_rorschach_response_sequence_count(self):
        for lang in ALL_LANGUAGES:
            data = RORSCHACH_DATA[lang]
            assert isinstance(data["response_sequence"], list)
            assert len(data["response_sequence"]) == 3, f"{lang} should have 3 response sequences"

    def test_rorschach_themes_count(self):
        for lang in ALL_LANGUAGES:
            data = RORSCHACH_DATA[lang]
            assert isinstance(data["themes"], list)
            assert len(data["themes"]) >= 2, f"{lang} should have at least 2 themes"


# ─────────────────────────────────────────────────────────────────────────────
# Format Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestFormat:
    def test_format_rorschach_contains_language(self):
        # Set current_index=7 (C/C++) so that advance() wraps to Rust (index 0)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(dict(MOCK_ROTATION, current_index=7), f)
            path = f.name
        try:
            result = rorschach(rotation_path=path)
            formatted = format_rorschach(result)
            assert "Rust" in formatted
            assert "Polyglot Rorschach" in formatted
        finally:
            os.unlink(path)

    def test_format_rorschach_contains_shadow_denial(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(dict(MOCK_ROTATION, current_index=0), f)
            path = f.name
        try:
            result = rorschach(rotation_path=path)
            formatted = format_rorschach(result)
            assert "Shadow Denial" in formatted
            assert "refuses to see" in formatted
        finally:
            os.unlink(path)

    def test_format_rorschach_contains_response_sequence(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(dict(MOCK_ROTATION, current_index=0), f)
            path = f.name
        try:
            result = rorschach(rotation_path=path)
            formatted = format_rorschach(result)
            assert "Response Sequence" in formatted
            assert "First:" in formatted
        finally:
            os.unlink(path)


# ─────────────────────────────────────────────────────────────────────────────
# Tool Metadata Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestMetadata:
    def test_tool_name(self):
        assert TOOL_NAME == "polyglot-rorschach"

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"

    def test_rotation_order_matches_all_languages(self):
        assert ROTATION_ORDER == ALL_LANGUAGES
