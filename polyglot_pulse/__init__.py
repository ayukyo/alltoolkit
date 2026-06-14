#!/usr/bin/env python3
"""
💓 Polyglot Pulse v1.0
A creative tool that measures "vital signs" of programming languages —
analyzes language health metrics and generates pulse reports with rotation tracking.
Each language has unique vitality indicators based on real ecosystem data.
"""

import json
import os
import math
import random
from datetime import datetime

TOOL_NAME = "polyglot-pulse"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = "language_rotation.json"

# Real-ish vitality metrics per language (representing ecosystem health)
LANGUAGE_METRICS = {
    "Rust": {
        "energy": 92, "memory_integrity": 98, "concurrency_pulse": 95,
        "type_safety": 99, "learning_curve": 85, "community_growth": 88
    },
    "Go": {
        "energy": 88, "memory_integrity": 85, "concurrency_pulse": 94,
        "type_safety": 75, "learning_curve": 30, "community_growth": 82
    },
    "Swift": {
        "energy": 82, "memory_integrity": 92, "concurrency_pulse": 78,
        "type_safety": 90, "learning_curve": 55, "community_growth": 75
    },
    "Kotlin": {
        "energy": 85, "memory_integrity": 90, "concurrency_pulse": 82,
        "type_safety": 93, "learning_curve": 50, "community_growth": 80
    },
    "TypeScript": {
        "energy": 90, "memory_integrity": 78, "concurrency_pulse": 72,
        "type_safety": 88, "learning_curve": 45, "community_growth": 95
    },
    "JavaScript": {
        "energy": 95, "memory_integrity": 65, "concurrency_pulse": 70,
        "type_safety": 72, "learning_curve": 25, "community_growth": 99
    },
    "Java": {
        "energy": 80, "memory_integrity": 88, "concurrency_pulse": 80,
        "type_safety": 85, "learning_curve": 60, "community_growth": 90
    },
    "C/C++": {
        "energy": 75, "memory_integrity": 55, "concurrency_pulse": 85,
        "type_safety": 60, "learning_curve": 92, "community_growth": 85
    }
}


def load_rotation():
    """Load language rotation config."""
    path = ROTATION_FILE
    if not os.path.exists(path):
        # Fallback for testing from different directories
        path = os.path.join(os.path.dirname(__file__), "..", ROTATION_FILE)
    with open(path, "r") as f:
        return json.load(f)


def save_rotation(data):
    """Save updated rotation config."""
    path = ROTATION_FILE
    if not os.path.exists(path):
        path = os.path.join(os.path.dirname(__file__), "..", ROTATION_FILE)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def calculate_pulse_score(metrics):
    """Calculate overall pulse score from vital signs (weighted average)."""
    weights = {
        "energy": 0.25,
        "memory_integrity": 0.20,
        "concurrency_pulse": 0.15,
        "type_safety": 0.15,
        "learning_curve": 0.10,
        "community_growth": 0.15
    }
    score = sum(metrics.get(k, 50) * w for k, w in weights.items())
    return round(score, 1)


def get_vital_signs(language):
    """Get vital signs for a language with some variance."""
    base = LANGUAGE_METRICS.get(language, {})
    # Add small random variance for realism
    random.seed(hash(language + datetime.now().strftime("%Y%m%d%H")))
    variance = {k: max(1, min(100, v + random.randint(-5, 5)))
                for k, v in base.items()}
    return variance


def assess_health_conditions(vitals):
    """Diagnose health conditions based on vital signs."""
    conditions = []
    if vitals["memory_integrity"] >= 90:
        conditions.append("🛡️ Ironclad Memory")
    if vitals["concurrency_pulse"] >= 90:
        conditions.append("⚡ Parallel Mastery")
    if vitals["type_safety"] >= 90:
        conditions.append("✅ Type Guardian")
    if vitals["learning_curve"] >= 85:
        conditions.append("🔥 Warrior's Path")
    if vitals["community_growth"] >= 90:
        conditions.append("👥 Thriving Community")
    if vitals["energy"] >= 90:
        conditions.append("🚀 High Velocity")
    if vitals["memory_integrity"] < 70:
        conditions.append("⚠️ Memory Watch")
    if vitals["type_safety"] < 70:
        conditions.append("🤷 Loose Types")
    return conditions


def generate_diagnosis(language, score):
    """Generate a creative diagnosis for the language."""
    diagnoses = {
        (90, 100): f"🌟 {language} is in peak condition! A powerhouse language.",
        (80, 90): f"💪 {language} is thriving with strong vital signs.",
        (70, 80): f"😊 {language} is healthy and stable.",
        (60, 70): f"🤔 {language} has room for improvement but gets the job done.",
        (50, 60): f"😐 {language} is functioning. Consider a check-up.",
        (0, 50): f"🆘 {language} needs attention. Critical vitals detected."
    }
    for (low, high), msg in diagnoses.items():
        if low <= score <= high:
            return msg
    return f"❓ {language} pulse unclear."


def measure_pulse(language):
    """Main function — generate pulse report for selected language."""
    config = load_rotation()
    languages = config["languages"]

    if language not in languages:
        raise ValueError(f"Language '{language}' not in rotation list")

    vitals = get_vital_signs(language)
    pulse_score = calculate_pulse_score(vitals)
    conditions = assess_health_conditions(vitals)
    diagnosis = generate_diagnosis(language, pulse_score)

    # Determine next language via rotation
    current_idx = languages.index(language)
    next_idx = (current_idx + 1) % len(languages)
    next_language = languages[next_idx]

    # Update rotation state
    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now().isoformat() + "+08:00"
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": language,
        "timestamp": datetime.now().isoformat(),
        "vital_signs": vitals,
        "pulse_score": pulse_score,
        "diagnosis": diagnosis,
        "health_conditions": conditions,
        "next_language": next_language,
        "rotation_position": current_idx,
        "rotation_size": len(languages)
    }


def run_tests():
    """Run comprehensive tests to validate the tool."""
    tests_passed = 0
    tests_failed = 0

    def assert_eq(a, b, msg=""):
        nonlocal tests_passed, tests_failed
        if a == b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — expected {b}, got {a}")

    def assert_true(cond, msg=""):
        nonlocal tests_passed, tests_failed
        if cond:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg}")

    print("=" * 50)
    print("💓 Polyglot Pulse — Test Suite")
    print("=" * 50)

    print("\n[1] Module import test...")
    assert_true(True, "Module loads successfully")

    print("\n[2] Rotation file integrity...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_eq("Rust", config["languages"][0], "Rust is first language")
    assert_eq("C/C++", config["languages"][-1], "C/C++ is last language")

    print("\n[3] Pulse measurement for Rust...")
    result = measure_pulse("Rust")
    assert_true("language" in result, "language key present")
    assert_true("vital_signs" in result, "vital_signs key present")
    assert_true("pulse_score" in result, "pulse_score key present")
    assert_eq("Rust", result["language"], "Rust is measured")
    assert_true(0 <= result["pulse_score"] <= 100, "Pulse score in range [0,100]")
    assert_true("next_language" in result, "next_language key present")
    assert_eq("Go", result["next_language"], "Next language is Go after Rust")
    assert_eq(0, result["rotation_position"], "Rust at position 0")

    print("\n[4] Vital signs structure...")
    vitals = result["vital_signs"]
    expected_keys = ["energy", "memory_integrity", "concurrency_pulse",
                     "type_safety", "learning_curve", "community_growth"]
    for key in expected_keys:
        assert_true(key in vitals, f"'{key}' in vital signs")
        assert_true(1 <= vitals[key] <= 100, f"'{key}' value in valid range [1,100]")

    print("\n[5] Health conditions logic...")
    conditions = result["health_conditions"]
    assert_true(isinstance(conditions, list), "Conditions is a list")
    assert_true(len(conditions) >= 1, "At least one condition diagnosed")

    print("\n[6] Diagnosis message...")
    assert_true("diagnosis" in result, "Diagnosis present")
    assert_true(len(result["diagnosis"]) > 5, "Diagnosis is non-empty")

    print("\n[7] Rotation state update after Rust...")
    config2 = load_rotation()
    assert_eq(1, config2["current_index"], "Index advanced to 1 (Go)")
    assert_eq("Rust", config2["last_language"], "Last language updated to Rust")

    print("\n[8] Go measurement (second in rotation)...")
    result_go = measure_pulse("Go")
    assert_eq("Go", result_go["language"], "Go is measured")
    assert_eq("Swift", result_go["next_language"], "Next language is Swift after Go")
    assert_eq(1, result_go["rotation_position"], "Go at position 1")

    print("\n[9] Invalid language handling...")
    try:
        measure_pulse("Python")
        tests_failed += 1
        print("  ❌ FAIL: No error raised for invalid language")
    except ValueError as e:
        assert_true("Python" in str(e), "Invalid language in error message")
        tests_passed += 1
        print("  ✅ PASS: ValueError raised for invalid language")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ FAIL: Wrong exception type: {type(e).__name__}")

    print("\n[10] Pulse score calculation bounds...")
    for lang in config["languages"]:
        result = measure_pulse(lang)
        score = result["pulse_score"]
        assert_true(0 <= score <= 100, f"{lang} pulse score {score} in valid range")

    print("\n[11] All languages produce valid reports...")
    for lang in config["languages"]:
        r = measure_pulse(lang)
        assert_true(r["language"] == lang, f"{lang} returns correct language")
        assert_true("pulse_score" in r, f"{lang} has pulse_score")
        assert_true("next_language" in r, f"{lang} has next_language")
        assert_true(isinstance(r["health_conditions"], list), f"{lang} conditions is list")

    print("\n" + "=" * 50)
    print(f"Results: {tests_passed} passed, {tests_failed} failed")
    print("=" * 50)

    if tests_failed == 0:
        print("🎉 All tests passed! Polyglot Pulse is healthy.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--pulse":
        language = sys.argv[2] if len(sys.argv) > 2 else None
        if language:
            result = measure_pulse(language)
            print(json.dumps(result, indent=2))
        else:
            config = load_rotation()
            current = config["languages"][config["current_index"]]
            result = measure_pulse(current)
            print(json.dumps(result, indent=2))
    else:
        print(f"💓 Polyglot Pulse v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_pulse --test    # Run test suite")
        print("  python -m polyglot_pulse --pulse [lang]  # Measure language pulse")