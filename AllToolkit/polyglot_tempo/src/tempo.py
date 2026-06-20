#!/usr/bin/env python3
"""
🎵 Polyglot Tempo v1.0
Language Rhythm Engine — musical tempo profiles for programming languages.
"""

import json
import os
import random
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

TOOL_NAME = "polyglot-tempo"
TOOL_VERSION = "1.0.0"

# Resolve rotation file from module location
_MODULE_DIR = Path(__file__).parent          # src/
_POLYGLOT_DIR = _MODULE_DIR.parent           # polyglot_tempo/
_WORKSPACE_ROOT = _POLYGLOT_DIR.parent       # AllToolkit/
_ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

# ── Language tempo signatures ─────────────────────────────────────────────────
# Each language has a BPM range, time signature, and rhythm character.
LANGUAGE_RHYTHMS: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "bpm_range": (110, 130),
        "time_signature": "4/4",
        "character": "precise metronome",
        "feel": "measured, deliberate, unapologetically strict",
        "signature_note": "quarter",
        "syncopation": 0.15,
        "groove_factor": 0.3,
        "rhythm_tags": ["steady", "disciplined", "architectural", "formal"],
        "composer_equivalent": "Bach — mathematical precision with emotional depth",
        "mood_keywords": ["controlled", "intense", "structured"],
    },
    "Go": {
        "bpm_range": (120, 140),
        "time_signature": "4/4",
        "character": "drum machine",
        "feel": "steady, utilitarian, no wasted beats",
        "signature_note": "eighth",
        "syncopation": 0.25,
        "groove_factor": 0.5,
        "rhythm_tags": ["steady", "pragmatic", "goroutine-pulse", "minimalist"],
        "composer_equivalent": "Philip Glass — repetitive patterns with subtle evolution",
        "mood_keywords": ["consistent", "efficient", "relaxed confidence"],
    },
    "Swift": {
        "bpm_range": (100, 125),
        "time_signature": "4/4",
        "character": "legato melody",
        "feel": "smooth, expressive, elegant phrasing",
        "signature_note": "dotted quarter",
        "syncopation": 0.35,
        "groove_factor": 0.65,
        "rhythm_tags": ["smooth", "expressive", "elegant", "flowing"],
        "composer_equivalent": "Debussy — impressionistic, flowing, beautiful",
        "mood_keywords": ["graceful", "refined", "aesthetic"],
    },
    "Kotlin": {
        "bpm_range": (105, 130),
        "time_signature": "4/4",
        "character": "chamber ensemble",
        "feel": "harmonious layers, cooperative voices, clean counterpoint",
        "signature_note": "quarter",
        "syncopation": 0.3,
        "groove_factor": 0.55,
        "rhythm_tags": ["harmonious", "layered", "pragmatic", "modern"],
        "composer_equivalent": "Mendelssohn — polished, balanced, melodic wit",
        "mood_keywords": ["balanced", "cooperative", "polished"],
    },
    "TypeScript": {
        "bpm_range": (115, 140),
        "time_signature": "4/4",
        "character": "synth pop beat",
        "feel": "bright, rhythmic, modern energy with type-safe structure",
        "signature_note": "eighth",
        "syncopation": 0.45,
        "groove_factor": 0.7,
        "rhythm_tags": ["bright", "rhythmic", "modern", "typed"],
        "composer_equivalent": "Daft Punk — electronic precision with dance energy",
        "mood_keywords": ["energetic", "structured", "forward-looking"],
    },
    "JavaScript": {
        "bpm_range": (120, 155),
        "time_signature": "4/4",
        "character": "syncopated jazz",
        "feel": "improvisational, loose, creative, sometimes chaotic",
        "signature_note": "sixteenth",
        "syncopation": 0.65,
        "groove_factor": 0.85,
        "rhythm_tags": ["syncopated", "improvisational", "dynamic", "free-form"],
        "composer_equivalent": "Herbie Hancock — technically grounded, wildly creative",
        "mood_keywords": ["free", "expressive", "versatile", "rule-bending"],
    },
    "Java": {
        "bpm_range": (90, 115),
        "time_signature": "4/4",
        "character": "symphonic march",
        "feel": "grand, structured, ceremonial, heavyweight procession",
        "signature_note": "half",
        "syncopation": 0.2,
        "groove_factor": 0.4,
        "rhythm_tags": ["grand", "structured", "ceremonial", "enterprise"],
        "composer_equivalent": "Beethoven (late period) — monumental, formal, authoritative",
        "mood_keywords": ["authoritative", "ceremonial", "grand"],
    },
    "C/C++": {
        "bpm_range": (60, 90),
        "time_signature": "4/4",
        "character": "slow heartbeat",
        "feel": "deep, powerful, low-frequency pulse — each beat carries weight",
        "signature_note": "whole",
        "syncopation": 0.1,
        "groove_factor": 0.2,
        "rhythm_tags": ["deep", "powerful", "low-frequency", "weighty"],
        "composer_equivalent": "Philip Glass (slow movements) — minimalist weight",
        "mood_keywords": ["powerful", "deliberate", "ancient", "heavy"],
    },
}

LANGUAGE_NOTE_VALUES: Dict[str, str] = {
    lang: data["signature_note"] for lang, data in LANGUAGE_RHYTHMS.items()
}

GENRE_DESCRIPTIONS: Dict[str, str] = {
    "precise metronome": "A language that enforces discipline through its type system and ownership model. Every beat is accounted for.",
    "drum machine": "A language built for reliability and speed. Think of a drum machine laying down a perfect groove every time.",
    "legato melody": "A language designed for expressiveness and elegance. Like a long, connected melodic line with no breaks.",
    "chamber ensemble": "A language that harmonizes multiple paradigms. Different parts work together like a string quartet.",
    "synth pop beat": "A modern, electronic feel — structured beneath but danceable on the surface. Type safety meets rapid iteration.",
    "syncopated jazz": "Free-form and expressive. The rules are more like guidelines. Expect surprises and creative solutions.",
    "symphonic march": "Grand and ceremonial. Built for large ensembles. Everything has a place and a formal role.",
    "slow heartbeat": "Deep, powerful, and foundational. Low frequency means each beat resonates long after it's struck.",
}

TEMPO_TIER_LABELS: Dict[str, str] = {
    "prestissimo": "⚡ Prestissimo — Blazing fast (>150 BPM)",
    "presto": "🎹 Presto — Fast and fluid (135-150 BPM)",
    "allegro": "🎸 Allegro — Quick and lively (110-134 BPM)",
    "andante": "🚶 Andante — Walking pace (85-109 BPM)",
    "adagio": "🌊 Adagio — Slow and expressive (<85 BPM)",
}


def _resolve_rotation_path() -> str:
    """Resolve the rotation file path, checking multiple locations."""
    paths_to_try = [
        _ROTATION_FILE,
        os.path.join(os.path.dirname(__file__), "..", "..", "language_rotation.json"),
    ]
    for p in paths_to_try:
        if os.path.exists(p):
            return p
    # Fallback: use workspace root
    return _ROTATION_FILE


def load_rotation() -> dict:
    """Load language rotation config from language_rotation.json."""
    path = _resolve_rotation_path()
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: dict) -> None:
    """Save updated rotation config to language_rotation.json."""
    path = _resolve_rotation_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def compute_next_language(language: str) -> str:
    """Advance rotation and return the next language."""
    config = load_rotation()
    languages = config["languages"]
    if language not in languages:
        raise ValueError(f"Language '{language}' not in rotation list")
    current_idx = languages.index(language)
    next_idx = (current_idx + 1) % len(languages)
    next_language = languages[next_idx]
    # Update rotation state
    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation(config)
    return next_language


def get_tempo_tier(bpm: int) -> str:
    """Classify a BPM into a tempo tier (standard music terminology)."""
    if bpm > 150:
        return "prestissimo"
    elif bpm >= 135:
        return "presto"
    elif bpm >= 110:
        return "allegro"
    elif bpm >= 85:
        return "andante"
    else:
        return "adagio"


def get_tempo_profile(language: str) -> Dict[str, Any]:
    """Get the musical tempo profile for a language."""
    if language not in LANGUAGE_RHYTHMS:
        raise ValueError(f"Language '{language}' not recognized. "
                         f"Available: {list(LANGUAGE_RHYTHMS.keys())}")
    data = LANGUAGE_RHYTHMS[language]
    # Deterministic BPM based on language name
    rng = random.Random(hash(language))
    bpm_low, bpm_high = data["bpm_range"]
    bpm = rng.randint(bpm_low, bpm_high)
    tier = get_tempo_tier(bpm)
    tier_label = TEMPO_TIER_LABELS[tier]
    return {
        "bpm": bpm,
        "bpm_range": data["bpm_range"],
        "time_signature": data["time_signature"],
        "tempo_tier": tier,
        "tempo_tier_label": tier_label,
        "character": data["character"],
        "feel": data["feel"],
        "signature_note": data["signature_note"],
        "syncopation": data["syncopation"],
        "groove_factor": data["groove_factor"],
        "rhythm_tags": data["rhythm_tags"],
        "composer_equivalent": data["composer_equivalent"],
        "mood_keywords": data["mood_keywords"],
        "genre_description": GENRE_DESCRIPTIONS[data["character"]],
    }


def generate_beat_pattern(language: str, bars: int = 4) -> List[str]:
    """Generate an ASCII drum/beat pattern for the language.
    
    Each bar has 4 beats (time signature 4/4). The pattern uses:
      - ● = strong beat (downbeat)
      - ○ = weak beat (upbeat)
      - ◑ = syncopated/off-beat
      - ░ = rest/rests between phrases
    """
    if language not in LANGUAGE_RHYTHMS:
        raise ValueError(f"Language '{language}' not recognized")
    data = LANGUAGE_RHYTHMS[language]
    syncopation = data["syncopation"]
    groove = data["groove_factor"]
    rng = random.Random(hash(language + str(bars)))

    beats_map = {
        "quarter": 4,
        "eighth": 8,
        "dotted quarter": 6,
        "half": 2,
        "whole": 1,
        "sixteenth": 16,
    }
    subdivision = beats_map.get(data["signature_note"], 4)

    pattern_lines = []
    for bar in range(bars):
        bar_beats = []
        for beat in range(4):
            r = rng.random()
            # Determine what to play on this beat
            if beat == 0:  # Always strong downbeat
                bar_beats.append("●")
            elif r < syncopation * 0.5:
                bar_beats.append("◑")
            elif r < groove:
                bar_beats.append("○")
            else:
                bar_beats.append("░")
        pattern_lines.append("  ".join(bar_beats))

    return pattern_lines


def get_language_genre(language: str) -> str:
    """Get a short genre tag for the language's musical character."""
    if language not in LANGUAGE_RHYTHMS:
        raise ValueError(f"Language '{language}' not recognized")
    return LANGUAGE_RHYTHMS[language]["character"]


def analyze_tempo(language: str) -> Dict[str, Any]:
    """Main entry point — full tempo analysis for a language."""
    config = load_rotation()
    languages = config["languages"]

    if language not in languages:
        raise ValueError(f"Language '{language}' not in rotation list. "
                         f"Available: {languages}")

    profile = get_tempo_profile(language)
    beat_pattern = generate_beat_pattern(language, bars=4)
    genre = get_language_genre(language)
    next_language = compute_next_language(language)

    # Find rotation position
    current_idx = languages.index(language)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": language,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tempo_profile": profile,
        "beat_pattern": beat_pattern,
        "genre": genre,
        "next_language": next_language,
        "rotation_position": current_idx,
        "rotation_size": len(languages),
    }


def format_tempo_report(analysis: Dict[str, Any]) -> str:
    """Format the tempo analysis as a human-readable report."""
    lang = analysis["language"]
    profile = analysis["tempo_profile"]
    beats = analysis["beat_pattern"]

    lines = [
        f"🎵 Polyglot Tempo — {lang}",
        "=" * 45,
        f"BPM: {profile['bpm']} ({profile['bpm_range'][0]}-{profile['bpm_range'][1]})",
        f"Time: {profile['time_signature']} | Tier: {profile['tempo_tier_label']}",
        f"Character: {profile['character']}",
        f"Feel: {profile['feel']}",
        f"Signature Note: {profile['signature_note']}",
        f"Syncopation: {profile['syncopation']} | Groove: {profile['groove_factor']}",
        f"Composer: {profile['composer_equivalent']}",
        f"Mood: {', '.join(profile['mood_keywords'])}",
        "",
        f"Beat Pattern (4 bars):",
    ]
    for bar in beats:
        lines.append(f"  | {bar} |")

    lines += [
        "",
        f"Next in rotation → {analysis['next_language']}",
        f"Position: {analysis['rotation_position'] + 1}/{analysis['rotation_size']}",
    ]
    return "\n".join(lines)


def run_tests() -> None:
    """Run the test suite."""
    import unittest
    from pathlib import Path

    test_file = Path(__file__).parent.parent / "tests" / "test_tempo.py"
    if test_file.exists():
        # Discover and run tests
        loader = unittest.TestLoader()
        suite = loader.discover(str(test_file.parent), pattern="test_tempo.py")
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        if not result.wasSuccessful():
            raise SystemExit(1)
    else:
        print("No test file found. Running inline tests...")

        # ── Inline tests ──────────────────────────────────────────
        tests_passed = 0
        tests_failed = 0

        def assert_eq(a, b, msg=""):
            nonlocal tests_passed, tests_failed
            if a == b:
                tests_passed += 1
                print(f"  ✅ PASS: {msg}")
            else:
                tests_failed += 1
                print(f"  ❌ FAIL: {msg} — expected {b!r}, got {a!r}")

        def assert_true(cond, msg=""):
            nonlocal tests_passed, tests_failed
            if cond:
                tests_passed += 1
                print(f"  ✅ PASS: {msg}")
            else:
                tests_failed += 1
                print(f"  ❌ FAIL: {msg}")

        def assert_in(needle, haystack, msg=""):
            nonlocal tests_passed, tests_failed
            if needle in haystack:
                tests_passed += 1
                print(f"  ✅ PASS: {msg}")
            else:
                tests_failed += 1
                print(f"  ❌ FAIL: {msg}")

        print("=" * 50)
        print("🎵 Polyglot Tempo — Test Suite")
        print("=" * 50)

        print("\n[1] Module constants...")
        assert_eq(TOOL_NAME, "polyglot-tempo", "tool name correct")
        assert_eq(TOOL_VERSION, "1.0.0", "version correct")

        print("\n[2] LANGUAGE_RHYTHMS completeness...")
        ROTATION_ORDER = ["Rust", "Go", "Swift", "Kotlin",
                          "TypeScript", "JavaScript", "Java", "C/C++"]
        for lang in ROTATION_ORDER:
            assert_true(lang in LANGUAGE_RHYTHMS, f"{lang} in LANGUAGE_RHYTHMS")
            assert_true("bpm_range" in LANGUAGE_RHYTHMS[lang], f"{lang} has bpm_range")

        print("\n[3] Tempo profile generation...")
        for lang in ROTATION_ORDER:
            profile = get_tempo_profile(lang)
            assert_true("bpm" in profile, f"{lang} has bpm")
            assert_true(60 <= profile["bpm"] <= 160, f"{lang} BPM in valid range")
            assert_true("tempo_tier" in profile, f"{lang} has tempo_tier")
            assert_true("genre_description" in profile, f"{lang} has genre_description")
            assert_true("composer_equivalent" in profile, f"{lang} has composer_equivalent")

        print("\n[4] Beat pattern generation...")
        for lang in ROTATION_ORDER:
            pattern = generate_beat_pattern(lang, bars=4)
            assert_eq(len(pattern), 4, f"{lang} generates 4 bars")
            for bar in pattern:
                beats = bar.split("  ")
                assert_eq(len(beats), 4, f"{lang} bar has 4 beats")

        print("\n[5] Tempo tier classification...")
        assert_eq(get_tempo_tier(155), "prestissimo", "155 BPM is prestissimo")
        assert_eq(get_tempo_tier(130), "allegro", "130 BPM is allegro")
        assert_eq(get_tempo_tier(105), "andante", "105 BPM is andante")
        assert_eq(get_tempo_tier(75), "adagio", "75 BPM is adagio")

        print("\n[6] analyze_tempo returns correct structure...")
        analysis = analyze_tempo("Rust")
        assert_true("language" in analysis, "language key present")
        assert_true("tempo_profile" in analysis, "tempo_profile key present")
        assert_true("beat_pattern" in analysis, "beat_pattern key present")
        assert_true("next_language" in analysis, "next_language key present")
        assert_eq(analysis["language"], "Rust", "language is Rust")
        assert_eq(analysis["next_language"], "Go", "next language after Rust is Go")

        print("\n[7] Rotation state update...")
        config_before = load_rotation()
        idx_before = config_before["current_index"]
        lang_before = config_before["languages"][idx_before]
        analyze_tempo(lang_before)
        config_after = load_rotation()
        expected = (idx_before + 1) % len(config_before["languages"])
        assert_eq(config_after["current_index"], expected, "index advanced correctly")

        print("\n[8] Invalid language raises ValueError...")
        try:
            get_tempo_profile("Python")
            tests_failed += 1
            print("  ❌ FAIL: No error for invalid language")
        except ValueError as e:
            assert_in("Python", str(e), "Python in error message")
            tests_passed += 1
            print("  ✅ PASS: ValueError raised for invalid language")

        print("\n[9] Genre descriptions cover all characters...")
        characters_seen = set(LANGUAGE_RHYTHMS[lang]["character"] for lang in ROTATION_ORDER)
        for char in characters_seen:
            assert_true(char in GENRE_DESCRIPTIONS, f"'{char}' has genre description")

        print("\n[10] All languages produce valid reports...")
        for lang in ROTATION_ORDER:
            r = analyze_tempo(lang)
            assert_true("tempo_profile" in r, f"{lang} has tempo_profile")
            assert_true("beat_pattern" in r, f"{lang} has beat_pattern")
            assert_true("rotation_position" in r, f"{lang} has rotation_position")
            assert_true("rotation_size" in r, f"{lang} has rotation_size")

        print("\n" + "=" * 50)
        print(f"Results: {tests_passed} passed, {tests_failed} failed")
        print("=" * 50)

        if tests_failed == 0:
            print("🎉 All tests passed! Polyglot Tempo is in perfect rhythm.")
        else:
            print(f"💥 {tests_failed} test(s) failed.")
            raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--analyze":
        language = sys.argv[2] if len(sys.argv) > 2 else None
        if language:
            analysis = analyze_tempo(language)
            print(format_tempo_report(analysis))
        else:
            config = load_rotation()
            current = config["languages"][config["current_index"]]
            analysis = analyze_tempo(current)
            print(format_tempo_report(analysis))
    else:
        print(f"🎵 Polyglot Tempo v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_tempo --test          # Run test suite")
        print("  python -m polyglot_tempo --analyze       # Analyze current language")
        print("  python -m polyglot_tempo --analyze Rust  # Analyze specific language")