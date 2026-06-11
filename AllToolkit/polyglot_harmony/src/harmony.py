"""
Core harmony analysis engine for Polyglot Harmony.
"""

from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path
import json
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class DimensionScore:
    score: float  # 0.0 - 1.0
    label: str
    description: str

@dataclass
class HarmonyReport:
    previous_language: str
    current_language: str
    overall_score: float
    dimensions: list
    transfer_tips: list
    synergy_summary: str
    rotated: bool = False
    new_index: Optional[int] = None


# ---------------------------------------------------------------------------
# Language compatibility matrix
# ---------------------------------------------------------------------------

LANGUAGE_FEATURES = {
    "Rust": {
        "paradigm": ["systems", "functional", "ownership"],
        "syntax_family": "curly-brace",
        "memory_model": "ownership_borrow",
        "strengths": ["safety", "performance", "concurrency"],
        "learning_curve": "steep",
    },
    "Go": {
        "paradigm": ["concurrent", "procedural", "light-oo"],
        "syntax_family": "curly-brace",
        "memory_model": "garbage_collected",
        "strengths": ["simplicity", "concurrency", "fast-compile"],
        "learning_curve": "gentle",
    },
    "Swift": {
        "paradigm": ["oo", "functional", "protocol-oriented"],
        "syntax_family": "curly-brace",
        "memory_model": "arc",
        "strengths": ["safety", "expressive", "ios-development"],
        "learning_curve": "moderate",
    },
    "Kotlin": {
        "paradigm": ["oo", "functional", "interoperable"],
        "syntax_family": "curly-brace",
        "memory_model": "jvm-gc",
        "strengths": ["concise", "null-safe", "android"],
        "learning_curve": "gentle",
    },
    "TypeScript": {
        "paradigm": ["oo", "functional", "structural"],
        "syntax_family": "curly-brace",
        "memory_model": "gc-dynamic",
        "strengths": ["types", "dx", "js-ecosystem"],
        "learning_curve": "gentle",
    },
    "JavaScript": {
        "paradigm": ["multi-paradigm", "prototype", "event-driven"],
        "syntax_family": "curly-brace",
        "memory_model": "gc-dynamic",
        "strengths": ["ubiquity", "flexibility", "web"],
        "learning_curve": "moderate",
    },
    "Java": {
        "paradigm": ["oo", "static", "class-based"],
        "syntax_family": "curly-brace",
        "memory_model": "jvm-gc",
        "strengths": ["portability", "ecosystem", "enterprise"],
        "learning_curve": "moderate",
    },
    "C/C++": {
        "paradigm": ["procedural", "systems", "multi-paradigm"],
        "syntax_family": "curly-brace",
        "memory_model": "manual",
        "strengths": ["control", "performance", "portability"],
        "learning_curve": "steep",
    },
}

COMPATIBILITY_PAIRS = {
    ("Rust", "Go"): {"syntax": 0.85, "paradigm": 0.55, "interop": 0.60, "transfer": 0.70},
    ("Go", "Swift"): {"syntax": 0.80, "paradigm": 0.60, "interop": 0.50, "transfer": 0.65},
    ("Swift", "Kotlin"): {"syntax": 0.90, "paradigm": 0.85, "interop": 0.80, "transfer": 0.88},
    ("Kotlin", "TypeScript"): {"syntax": 0.75, "paradigm": 0.70, "interop": 0.65, "transfer": 0.72},
    ("TypeScript", "JavaScript"): {"syntax": 0.95, "paradigm": 0.85, "interop": 0.95, "transfer": 0.92},
    ("JavaScript", "Java"): {"syntax": 0.70, "paradigm": 0.65, "interop": 0.60, "transfer": 0.68},
    ("Java", "C/C++"): {"syntax": 0.75, "paradigm": 0.70, "interop": 0.55, "transfer": 0.65},
    ("C/C++", "Rust"): {"syntax": 0.88, "paradigm": 0.75, "interop": 0.40, "transfer": 0.68},
}

DEFAULT_COMPATIBILITY = {"syntax": 0.60, "paradigm": 0.50, "interop": 0.45, "transfer": 0.55}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def _get_compatibility(lang_a: str, lang_b: str) -> dict:
    """Look up compatibility scores for an ordered pair."""
    return COMPATIBILITY_PAIRS.get((lang_a, lang_b), DEFAULT_COMPATIBILITY)


def _score_to_dimension(score: float, name: str, desc: str) -> DimensionScore:
    return DimensionScore(score=score, label=name, description=desc)


def _build_transfer_tips(prev: str, curr: str, scores: dict) -> list:
    tips = []
    if scores["syntax"] >= 0.85:
        tips.append(f"High syntax overlap — your muscle memory transfers well between {prev} and {curr}")
    if scores["paradigm"] >= 0.80:
        tips.append(f"Strong paradigm alignment — concepts from {prev} map directly to {curr}")
    if scores["interop"] >= 0.80:
        tips.append(f"Excellent interoperability — these languages can call each other via FFI or WASM")
    if scores["transfer"] >= 0.80:
        tips.append(f"High learning transfer — skills built in {prev} accelerate {curr} mastery")
    if scores["syntax"] < 0.70:
        tips.append(f"Syntax bridge ahead — expect some adjustment period when moving from {prev} to {curr}")
    if scores["transfer"] < 0.60:
        tips.append(f"Paradigm shift detected — approach {curr} with fresh eyes, don't rely on {prev} patterns")
    if prev in LANGUAGE_FEATURES and curr in LANGUAGE_FEATURES:
        prev_features = LANGUAGE_FEATURES[prev]
        curr_features = LANGUAGE_FEATURES[curr]
        shared = set(prev_features["paradigm"]) & set(curr_features["paradigm"])
        if shared:
            tips.append(f"Shared paradigms: {', '.join(sorted(shared))}")
        if prev_features["memory_model"] != curr_features["memory_model"]:
            tips.append(
                f"Memory model transition: {prev_features['memory_model']} → "
                f"{curr_features['memory_model']} — this is the key mental shift"
            )
    return tips


def _build_synergy_summary(prev: str, curr: str, scores: dict, tips: list) -> str:
    avg = (scores["syntax"] + scores["paradigm"] + scores["interop"] + scores["transfer"]) / 4
    if avg >= 0.85:
        tone = f"{prev} → {curr} is a smooth transition with strong synergies."
    elif avg >= 0.70:
        tone = f"{prev} → {curr} is a natural progression with good learning transfer."
    elif avg >= 0.55:
        tone = f"{prev} → {curr} offers meaningful cross-pollination between different paradigms."
    else:
        tone = f"{prev} → {curr} is a bold leap — expect to unlearn habits and build new mental models."
    return tone


def analyze_harmony(config_path: str, rotate: bool = True) -> HarmonyReport:
    """Analyze harmony between current and next language in the rotation.

    Args:
        config_path: Path to language_rotation.json.
        rotate: If True, advance the rotation index after reading.

    Returns:
        HarmonyReport with scores, tips, and summary.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    languages = data["languages"]
    current_index = data["current_index"]

    previous_language = languages[current_index]
    new_index = (current_index + 1) % len(languages)
    current_language = languages[new_index]

    new_current_index = current_index
    rotated = False
    if rotate:
        new_current_index = new_index
        rotated = True
        data["current_index"] = new_index
        data["last_language"] = current_language
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")

    scores = _get_compatibility(previous_language, current_language)

    dimensions = [
        _score_to_dimension(scores["syntax"], "Syntax Overlap", "Lexical and structural similarity"),
        _score_to_dimension(scores["paradigm"], "Paradigm Alignment", "Conceptual overlap in programming models"),
        _score_to_dimension(scores["interop"], "Ecosystem Interop", "Ability to interface, FFI, and share code"),
        _score_to_dimension(scores["transfer"], "Learning Transfer", "Speed of skill acquisition between languages"),
    ]

    tips = _build_transfer_tips(previous_language, current_language, scores)
    summary = _build_synergy_summary(previous_language, current_language, scores, tips)

    return HarmonyReport(
        previous_language=previous_language,
        current_language=current_language,
        overall_score=(scores["syntax"] + scores["paradigm"] + scores["interop"] + scores["transfer"]) / 4,
        dimensions=dimensions,
        transfer_tips=tips,
        synergy_summary=summary,
        rotated=rotated,
        new_index=new_current_index,
    )


def get_consecutive_pair(config_path: str) -> tuple:
    """Return (previous_language, current_language) without rotating."""
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    languages = data["languages"]
    idx = data["current_index"]
    next_idx = (idx + 1) % len(languages)
    return languages[idx], languages[next_idx]