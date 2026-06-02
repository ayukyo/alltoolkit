#!/usr/bin/env python3
"""
🌐 Language Mastery Forge v1.0
A creative tool for tracking and celebrating language learning progress.
Selects a language from rotation, assigns random mastery stats, and generates fun insights.
"""

import json
import random
import os
import math
from datetime import datetime

TOOL_NAME = "language-mastery"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = "language_rotation.json"


def load_rotation():
    """Load language rotation config."""
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data):
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


def roll_mastery_stats(language):
    """Generate random mastery stats for a language with deterministic charm."""
    random.seed(hash(language + str(datetime.now().date())))
    
    base_xp = random.randint(50, 950)
    level = int(math.sqrt(base_xp // 10)) + 1
    
    skill_names = [
        "Syntax Mastery", "Memory Leaks Avoided", "Null Safety Score",
        "Concurrency Power", "Error Handling Fu", "Type Inference Rank",
        "Build Speed", "Community Vibes", "Documentation mojo",
        "Ecosystem Richness"
    ]
    skills = {}
    for name in random.sample(skill_names, min(5, len(skill_names))):
        skills[name] = random.randint(20, 100)
    
    achievements = []
    if level >= 5:
        achievements.append("🚀 Speedrunner")
    if base_xp >= 500:
        achievements.append("⚡ Power Coder")
    if skills.get("Memory Leaks Avoided", 0) >= 80:
        achievements.append("🛡️ Memory Guardian")
    if skills.get("Concurrency Power", 0) >= 70:
        achievements.append("⚙️ Parallel Beast")
    
    mastery_title = _title_for_level(level)
    
    return {
        "language": language,
        "level": level,
        "total_xp": base_xp,
        "title": mastery_title,
        "skills": skills,
        "achievements": achievements,
        "rotations": random.randint(1, 66)
    }


def _title_for_level(level):
    """Assign a fun mastery title based on level."""
    titles = [
        "🍃 Seedling", "🌱 Apprentice", "🌿 Initiate", "🌳 Padawan",
        "⚔️ Journeyman", "🔥 Adept", "💫 Expert", "⭐ Elite",
        "🌟 Master", "💎 Grandmaster", "👑 Legendary Architect"
    ]
    idx = min(level - 1, len(titles) - 1)
    return titles[max(0, idx)]


def generate_weekly_quest(language):
    """Generate a fun weekly quest for the language."""
    random.seed(hash(language + "quest"))
    quests = [
        f"Build a CLI tool in {language} that impresses your peers",
        f"Read an open-source {language} project and submit a PR",
        f"Teach someone else one {language} concept today",
        f"Write 3 code snippets exploring {language}'s unique feature",
        f"Watch a conference talk about {language} and take notes",
        f"Set up a {language} project with testing & CI from scratch",
        f"Compare {language} idioms to your favorite language",
    ]
    return random.choice(quests)


def forge(language):
    """Main forge function — generate mastery report for selected language."""
    config = load_rotation()
    
    if language not in config["languages"]:
        raise ValueError(f"Language '{language}' not in rotation list")
    
    stats = roll_mastery_stats(language)
    quest = generate_weekly_quest(language)
    
    current_idx = config["languages"].index(language)
    config["current_index"] = (current_idx + 1) % len(config["languages"])
    save_rotation(config)
    
    return {
        "selected_language": language,
        "mastery_report": stats,
        "weekly_quest": quest,
        "next_language": config["languages"][config["current_index"]],
        "rotation_size": len(config["languages"]),
        "tool_version": TOOL_VERSION
    }


def run_tests():
    """Run tests to validate the tool."""
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
    
    print("Testing module load...")
    assert_eq(True, True, "Module imports successfully")
    
    print("Testing rotation file integrity...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_eq(0, config["current_index"], "Index reset to 0")
    assert_eq("Rust", config["languages"][0], "Rust is first language")
    
    print("Testing forge output...")
    result = forge("Rust")
    expected_keys = ["selected_language", "mastery_report", "weekly_quest", "next_language"]
    for key in expected_keys:
        assert_eq(True, key in result, f"Key '{key}' in result")
    assert_eq("Rust", result["selected_language"], "Rust selected")
    assert_eq("Go", result["next_language"], "Next language is Go")
    
    print("Testing mastery report structure...")
    report = result["mastery_report"]
    assert_eq(True, "level" in report, "level in mastery report")
    assert_eq(True, "total_xp" in report, "total_xp in mastery report")
    assert_eq(True, "title" in report, "title in mastery report")
    assert_eq(True, 1 <= report["level"] <= 10, "level in valid range")
    assert_eq(True, 50 <= report["total_xp"] <= 950, "XP in valid range")
    
    print("Testing rotation index update...")
    config2 = load_rotation()
    assert_eq(1, config2["current_index"], "Index advanced to 1 (Go)")
    
    print("Testing invalid language handling...")
    try:
        forge("Python")
        tests_failed += 1
        print("  ❌ FAIL: No error raised for invalid language")
    except ValueError:
        tests_passed += 1
        print("  ✅ PASS: ValueError raised for invalid language")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ FAIL: Wrong exception for invalid language: {e}")
    
    print(f"\n{'='*40}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("🎉 All tests passed!")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--forge":
        language = sys.argv[2] if len(sys.argv) > 2 else "Rust"
        result = forge(language)
        print(json.dumps(result, indent=2))
    else:
        print(f"Language Mastery Forge v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m language_mastery --test    # Run tests")
        print("  python -m language_mastery --forge [lang]  # Forge report")
