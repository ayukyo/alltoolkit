#!/usr/bin/env python3
"""
🍷 Polyglot Flavor v1.0
A "language sommelier" — applies sensory tasting notes to programming languages,
just like a sommelier rates fine wine or coffee.

Creative concept: "Every language has a flavor profile. This tool tastes them."

Each language is described across five sensory dimensions:
  • Body        — weight and texture of the language (light → full-bodied)
  • Aroma      — complexity of the type system and tooling ecosystem
  • Acidity    — how strict/fastidious the compiler or type checker is
  • Finish     — runtime performance and memory characteristics
  • Notes      — unique "terroir" — the cultural and design philosophy that makes it unique

Each run produces a structured tasting card for the current rotation language,
updates the index, and commits to git.

Distinct from existing tools:
  - language_archaeology: historical lineage & design philosophy (temporal depth)
  - language_compass:     learning journey maps (future-oriented milestones)
  - language_ecohub:      package ecosystem field guide (tooling landscape)
  - language_mastery:     XP/level progress tracking (progress dimension)
  - language_sage:        idioms, pro tips, pitfalls (practical wisdom)
  - language_synapse:    conceptual bridges between languages (cross-section)
  - language_ethos:      philosophical manifesto (belief/identity)
  - polyglot_digest:      syntax-parallel code snippets (spatial comparison)
  - polyglot_chronicle:   daily history and trivia (temporal NOW)
  - polyglot_codex:       kata/code challenges (practice)
  - dev_metrics:          cyclomatic/cognitive complexity (code analysis)

Flavor is about SENSORY PARALLELISM — a totally different lens for thinking
about what makes each language unique.
"""

import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

TOOL_NAME = "polyglot-flavor"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = str(
    Path(__file__).parent.parent.parent / "language_rotation.json"
)


# ── Flavor profiles for each rotation language ─────────────────────────────────
# Five dimensions scored 1–5:
#   Body (1=minimal, 5=full-bodied)
#   Aroma (1=simple, 5=complex)
#   Acidity (1=loose/dynamic, 5=strict/pedantic)
#   Finish (1=slow/verbose, 5=fast/optimized)
#   Uniqueness (1=generic, 5=uniquely itself)

LANGUAGE_PROFILES: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "body": 5,
        "aroma": 4,
        "acidity": 5,
        "finish": 5,
        "uniqueness": 5,
        "tasting_note": "Intense dark chocolate and espresso with a smoky oak finish. \
The tannins (ownership model) grip the palate with insistence. \
Expect a long, complex aftertaste of zero-cost abstractions.",
        "sommelier_quote": "A bold, age-worthy vintage for those who believe \
pain is the best teacher — and the compiler is always right.",
        "ideal_pairing": "Pairs well with system-level dishes, concurrent courses, \
and anyone who takes themselves very seriously at 3 AM.",
        "best_served": "When you need the compiler to personally attack your \
wrongthink. Not for the faint of heart.",
        "varietal": "Cabernet Sauvignon of Systems Programming",
    },
    "Go": {
        "body": 3,
        "aroma": 3,
        "acidity": 2,
        "finish": 4,
        "uniqueness": 3,
        "tasting_note": "Crisp and refreshing with bright citrus notes. \
Light body, clean minerality from the channels. \
The goroutine effervescence tickles the mid-palate. \
Short finish — it knows when to leave the party.",
        "sommelier_quote": "The people's champagne: approachable, celebratory, \
and excellent for toasting infrastructure milestones.",
        "ideal_pairing": "Ideal with microservices, CLI tools, and distributed \
hash browns served across a distributed table.",
        "best_served": "When you want to ship fast, stay clean, and never \
fight the borrow checker over wine pairings.",
        "varietal": "Sauvignon Blanc of Cloud Services",
    },
    "Swift": {
        "body": 3,
        "aroma": 4,
        "acidity": 4,
        "finish": 4,
        "uniqueness": 4,
        "tasting_note": "Elegant and floral with honeysuckle and crisp apple. \
The value semantics offer a clean, bright attack with no bitter aftertaste. \
Optional nil leaves a delicate, peppery finish.",
        "sommelier_quote": "A refined Burgundy for those who believe \
C should have had better manners all along.",
        "ideal_pairing": "Pairs beautifully with iOS apps, servers, \
and anyone who thinks Optional is actually a nice gesture.",
        "best_served": "When you want your code to read like poetry \
and your optionals to never surprise you.",
        "varietal": "Pinot Noir of Platform Development",
    },
    "Kotlin": {
        "body": 3,
        "aroma": 4,
        "acidity": 3,
        "finish": 4,
        "uniqueness": 3,
        "tasting_note": "Rich velvet texture with dark berry and espresso. \
The coroutines give it a pleasant effervescence. \
Null safety arrives like a knowledgeable server — \
 anticipatory, never intrusive.",
        "sommelier_quote": "A smooth Tempranillo for the JVM table — \
structured, modern, and surprisingly flexible for such a serious vintage.",
        "ideal_pairing": "Best with Android applications, Spring services, \
and anyone who believes every problem is solvable with an extension function.",
        "best_served": "When you want Java's infrastructure but with \
considerably better table manners.",
        "varietal": "Tempranillo of JVM Languages",
    },
    "TypeScript": {
        "body": 2,
        "aroma": 4,
        "acidity": 3,
        "finish": 3,
        "uniqueness": 3,
        "tasting_note": "Bright citrus and tropical fruit with a surprising \
vanilla note from the type system. The structural types give it \
unexpected depth. The finish is smooth but can turn bitter \
if you forget to define your types.",
        "sommelier_quote": "The Sauvignon Blanc for JavaScript refugees — \
suddenly the world makes sense and you can invite types to dinner.",
        "ideal_pairing": "Pairs with web frontends, Node.js backends, \
and anyone who has ever wished JavaScript came with a manual.",
        "best_served": "When productivity matters more than purity, \
and autocomplete is your best friend.",
        "varietal": "Sauvignon Blanc of the JavaScript Ecosystem",
    },
    "JavaScript": {
        "body": 2,
        "aroma": 3,
        "acidity": 1,
        "finish": 2,
        "uniqueness": 3,
        "tasting_note": "Surprisingly complex for its humble origins. \
Event loop gives it a unique sparkling quality. \
Prototype chain adds a funky, barnyard note that \
connoisseurs either love or find bizarre. \
The `this` binding is genuinely confusing, like a wine \
with an unlabeled grape variety.",
        "sommelier_quote": "A wild-card Zinfandel that somehow became \
the most popular drink on the planet. Nobody expected it.",
        "ideal_pairing": "Pairs with web pages, server scripts, \
mobile apps, coffee shop POS systems, and IoT toasters.",
        "best_served": "When you need to ship something yesterday \
and the runtime is already installed on every machine on Earth.",
        "varietal": "Zinfandel of Ubiquity",
    },
    "Java": {
        "body": 4,
        "aroma": 4,
        "acidity": 4,
        "finish": 3,
        "uniqueness": 2,
        "tasting_note": "Full-bodied Bordeaux with a long, storied finish. \
The tannins (checked exceptions) are firm and traditional. \
Virtual threads add a modern effervescence. \
The oak barrel aging (JVM) gives it consistent character \
across every vintage.",
        "sommelier_quote": "A distinguished Napa Cabernet — once controversial \
for its bold statements about enterprise, now a respected classic \
found on every corporate menu.",
        "ideal_pairing": "Pairs with enterprise applications, Android \
(JDK legacy), and large-scale distributed systems \
where you want fifteen years of backward compatibility.",
        "best_served": "When your CTO requires 'battle-tested' on the tin, \
and your HR department has been hiring Java developers since 1998.",
        "varietal": "Cabernet Sauvignon of Enterprise Computing",
    },
    "C/C++": {
        "body": 5,
        "aroma": 5,
        "acidity": 5,
        "finish": 5,
        "uniqueness": 5,
        "tasting_note": "The rarest and most complex vintage in existence. \
Barolo from a 100-year-old vineyard. The terroir includes \
buffer overflows, undefined behavior, and segfaults that \
require a medium rare sacrifice to appease. \
Not for beginners. Absolutely not.",
        "sommelier_quote": "A Barolo from the original vineyard — magnificent, \
mysterious, and capable of making you weep when you realize \
you've been drinking coffee when you could have been drinking this. \
No safety net. No training wheels. Pure, unadulterated power.",
        "ideal_pairing": "Pairs with operating systems, game engines, \
embedded systems, quantum physics simulations, and anyone \
who reads assembly in their spare time for fun.",
        "best_served": "When performance is the only metric that matters \
and you have personally memorized the entire C standard. \
Not recommended for projects with deadlines, junior developers, \
or a desire to keep your sanity intact.",
        "varietal": "Barolo of Systems Programming",
    },
}


# ── Helpers ──────────────────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    """Load language rotation config."""
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    """Save updated rotation state."""
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _bar(value: int, width: int = 10) -> str:
    """Render a 1–5 score as a visual bar (normalized to 5-point scale)."""
    # value is 1–5; normalize to width of 10 characters
    filled_count = round(value * width / 5)
    filled = "█" * filled_count
    empty = "░" * (width - filled_count)
    return f"[{filled}{empty}]"


def _dimension_label(score: int) -> str:
    labels = {
        1: "Minimal",
        2: "Light",
        3: "Medium",
        4: "Complex",
        5: "Intense",
    }
    return labels.get(score, "Medium")


def _overall_score(profile: Dict[str, Any]) -> float:
    """Average of the five scores, rounded to 1 decimal."""
    keys = ["body", "aroma", "acidity", "finish", "uniqueness"]
    return round(sum(profile[k] for k in keys) / len(keys), 1)


def _flavor_wheel(profile: Dict[str, Any]) -> str:
    """ASCII radar chart."""
    dims = ["Body", "Aroma", "Acidity", "Finish", "Unique"]
    values = [
        profile["body"],
        profile["aroma"],
        profile["acidity"],
        profile["finish"],
        profile["uniqueness"],
    ]
    lines = []
    for dim, val in zip(dims, values):
        lines.append(f"  {dim:<8} {_bar(val)}  ({val}/5 — {_dimension_label(val)})")
    return "\n".join(lines)


def _tasting_card(language: str, profile: Dict[str, Any]) -> str:
    """Render a full tasting card."""
    score = _overall_score(profile)
    stars = "★" * round(score) + "☆" * (5 - round(score))

    def _section(label: str, text: str, width: int = 58) -> str:
        lines = _wrap(text, width)
        header = f"║  {label}"
        padded = header + " " * (62 - len(header)) + "║"
        content = "\n".join(f"║  {line}" + " " * (60 - len(line)) + "║" for line in lines)
        return padded + "\n" + content

    return f"""
╔══════════════════════════════════════════════════════════════════╗
║          🍷  POLYGLOT FLAVOR — TASTING CARD  🍷               ║
╠══════════════════════════════════════════════════════════════════╣
║  Language     : {language:<50} ║
║  Varietal     : {profile['varietal']:<50} ║
║  Overall Score: {stars} ({score}/5.0){" " * max(0, 37 - len(stars) - len(f"{score}/5.0") - 9)}║
╠══════════════════════════════════════════════════════════════════╣
║  FLAVOR PROFILE                                              ║
{_flavor_wheel(profile)}
╠══════════════════════════════════════════════════════════════════╣
{_section("TASTING NOTE", profile['tasting_note'])}
╠══════════════════════════════════════════════════════════════════╣
{_section("SOMMELIER QUOTE", profile['sommelier_quote'])}
╠══════════════════════════════════════════════════════════════════╣
{_section("PAIRING RECOMMENDATION", profile['ideal_pairing'])}
╠══════════════════════════════════════════════════════════════════╣
{_section("WHEN TO SERVE", profile['best_served'])}
╚══════════════════════════════════════════════════════════════════╝"""


def _wrap(text: str, width: int) -> List[str]:
    """Wrap text to a fixed width, returning a list of lines (no prefix padding)."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        if len(current) + len(word) + 1 <= width:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# ── Core API ───────────────────────────────────────────────────────────────────

def flavor() -> Dict[str, Any]:
    """
    Main entry point: rotate to the next language, build its tasting card,
    update the rotation file, and return structured data.
    """
    config = load_rotation()
    languages = config["languages"]
    idx = config.get("current_index", 0) % len(languages)
    language = languages[idx]

    if language not in LANGUAGE_PROFILES:
        raise ValueError(f"Language '{language}' not in flavor profile database.")

    profile = LANGUAGE_PROFILES[language]
    card = _tasting_card(language, profile)

    # Advance index for next run
    next_idx = (idx + 1) % len(languages)
    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation(config)

    return {
        "language": language,
        "profile": profile,
        "tasting_card": card,
        "overall_score": _overall_score(profile),
        "rotated_at": config["updated_at"],
    }


def run_tests() -> None:
    """Run unit tests."""
    import traceback

    print("Running Polyglot Flavor tests...\n")

    def assert_eq(a: Any, b: Any, msg: str) -> None:
        if a != b:
            raise AssertionError(f"{msg}: got {a!r}, expected {b!r}")
        print(f"  ✓ {msg}")

    errors = []

    # ── Test 1: load + save round-trip ────────────────────────────────────────
    try:
        config = load_rotation()
        assert isinstance(config, dict), "config should be a dict"
        assert "languages" in config, "config should have 'languages'"
        assert "current_index" in config, "config should have 'current_index'"
        assert_eq(type(config["languages"]), list, "languages is a list")
        assert_eq(type(config["current_index"]), int, "current_index is an int")
        print("  ✓ load_rotation returns valid structure")
    except Exception as e:
        errors.append(("load_rotation", e))

    # ── Test 2: bar rendering ─────────────────────────────────────────────────
    try:
        assert_eq(_bar(1), "[██░░░░░░░░]", "bar renders 1 correctly")
        assert_eq(_bar(5), "[██████████]", "bar renders 5 correctly")
        assert_eq(_bar(3), "[██████░░░░]", "bar renders 3 correctly")
        assert_eq(_bar(2), "[████░░░░░░]", "bar renders 2 correctly")
        assert_eq(_bar(4), "[████████░░]", "bar renders 4 correctly")
    except Exception as e:
        errors.append(("_bar", e))

    # ── Test 3: dimension label ────────────────────────────────────────────────
    try:
        assert_eq(_dimension_label(1), "Minimal", "label 1")
        assert_eq(_dimension_label(3), "Medium", "label 3")
        assert_eq(_dimension_label(5), "Intense", "label 5")
    except Exception as e:
        errors.append(("_dimension_label", e))

    # ── Test 4: overall score ──────────────────────────────────────────────────
    try:
        assert_eq(_overall_score(LANGUAGE_PROFILES["Rust"]), 4.8, "Rust score")
        assert_eq(_overall_score(LANGUAGE_PROFILES["Go"]), 3.0, "Go score")
        assert_eq(_overall_score(LANGUAGE_PROFILES["JavaScript"]), 2.2, "JS score")
        assert_eq(_overall_score(LANGUAGE_PROFILES["C/C++"]), 5.0, "C/C++ score")
    except Exception as e:
        errors.append(("_overall_score", e))

    # ── Test 5: all languages have profiles ────────────────────────────────────
    try:
        config = load_rotation()
        for lang in config["languages"]:
            assert lang in LANGUAGE_PROFILES, f"{lang} has no profile"
        print(f"  ✓ All {len(config['languages'])} languages have flavor profiles")
    except Exception as e:
        errors.append(("profile completeness", e))

    # ── Test 6: flavor() rotates and saves ─────────────────────────────────────
    try:
        config = load_rotation()
        before_idx = config["current_index"]
        before_lang = config["last_language"]
        result = flavor()
        config2 = load_rotation()
        assert_eq(config2["current_index"], (before_idx + 1) % len(config["languages"]), "index advanced")
        assert_eq(config2["last_language"], result["language"], "last_language updated")
        assert result["language"] in LANGUAGE_PROFILES, "returned language has profile"
        assert "overall_score" in result, "result has overall_score"
        assert "tasting_card" in result, "result has tasting_card"
        print("  ✓ flavor() rotates and saves correctly")
    except Exception as e:
        errors.append(("flavor rotation", e))

    # ── Test 7: tasting_card contains key sections ─────────────────────────────
    try:
        result = flavor()
        card = result["tasting_card"]
        assert result["language"] in card, "card mentions language"
        assert "FLAVOR PROFILE" in card, "card has flavor profile section"
        assert "TASTING NOTE" in card, "card has tasting note section"
        assert "SOMMELIER QUOTE" in card, "card has sommelier quote section"
        print("  ✓ tasting_card renders all sections")
    except Exception as e:
        errors.append(("tasting_card sections", e))

    # ── Test 8: flavor wheel renders without error ─────────────────────────────
    try:
        for lang, prof in LANGUAGE_PROFILES.items():
            wheel = _flavor_wheel(prof)
            assert "Body" in wheel, f"{lang}: Body dimension missing"
            assert "Aroma" in wheel, f"{lang}: Aroma dimension missing"
            assert "Acidity" in wheel, f"{lang}: Acidity dimension missing"
            assert "Finish" in wheel, f"{lang}: Finish dimension missing"
            assert "Unique" in wheel, f"{lang}: Unique dimension missing"
        print(f"  ✓ All {len(LANGUAGE_PROFILES)} flavor wheels render correctly")
    except Exception as e:
        errors.append(("flavor_wheel", e))

    # ── Test 9: _wrap handles long and short text ───────────────────────────────
    try:
        lines = _wrap("Short", 78)
        assert_eq(len(lines), 1, "short text stays on one line")
        long_text = " ".join(["word"] * 50)
        lines = _wrap(long_text, 40)
        assert all(len(l) <= 42 for l in lines), "all lines respect width"
        print("  ✓ _wrap handles edge cases")
    except Exception as e:
        errors.append(("_wrap", e))

    # ── Test 10: index wraps around ────────────────────────────────────────────
    try:
        # Set index to last position
        config = load_rotation()
        last_idx = len(config["languages"]) - 1
        config["current_index"] = last_idx
        save_rotation(config)
        # flavor() advances last → first (index 0), returns last language (C/C++)
        result = flavor()
        config2 = load_rotation()
        assert_eq(config2["current_index"], 0, "index wraps from last to first")
        assert_eq(result["language"], "C/C++", "flavor() returns last language before wrap")
        # Next call should return the first language (Rust)
        result2 = flavor()
        assert_eq(result2["language"], config["languages"][0], "next call returns first language after wrap")
        print("  ✓ rotation wraps around correctly")
    except Exception as e:
        errors.append(("wrap-around", e))

    # ── Summary ────────────────────────────────────────────────────────────────
    print()
    if errors:
        for name, err in errors:
            print(f"  ✗ {name}: {err}")
            traceback.print_exception(type(err), err, err.__traceback__)
        print(f"\nTests: {len(errors)} failure(s)")
        raise SystemExit(1)
    else:
        print("All tests passed! ✓")


if __name__ == "__main__":
    run_tests()