#! /usr/bin/env python3
"""
🏺 Polyglot Vessel — Core Implementation v1.0

See parent __init__.py for full concept description.
"""

import json
import os
import random
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-vessel"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = str(
    Path(__file__).parent.parent.parent.parent / "language_rotation.json"
)

# The 8-language rotation sequence
ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ── Vessel substance data ──────────────────────────────────────────────────────
# Each language has a "vessel certificate" — the physical properties of its essence.
# These are handcrafted to reflect the language's true nature.

VESSEL_DATA: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "core_essence": "Ownership & Borrowing — the language that proves memory safety at compile time",
        "pressure_rating": 9.2,        # Very demanding (borrow checker is strict)
        "density": 9.5,               # Extremely information-dense concepts
        "volatility": 2.1,            # Very stable — language and ecosystem mature
        "buoyancy": 3.0,              # Steep initial learning curve
        "pour_temperature": "Cold (Compile-Time Verification)",  # Safety-first
        "distillation_notes": [
            "The borrow checker IS the vessel's pressure valve — respect it.",
            "Unsafe{} is the crack in the vessel — use sparingly.",
            "Lifetime annotations are the vessel's seam welds — visible but essential.",
            "Cargo is the vessel's integrity — always use it.",
        ],
        "appearance": "Amber liquid with visible ownership 'particles' — each variable a distinct glowing bead",
        "odour": "Cold steel and compiler warnings — the smell of guaranteed safety",
        "flame_test": "Burns bright orange-red — passionate community, intense standards",
        "shelf_life": "Virtually unlimited — compiled binaries last decades",
        "compatible_with": ["C/C++", "Swift"],
        "vessel_shape": "Blown-glass borosilicate — beautiful but demands careful handling",
    },
    "Go": {
        "core_essence": "CSP Concurrency — goroutines as lightweight threads of execution",
        "pressure_rating": 4.5,        # Relatively low pressure — straightforward mental model
        "density": 6.5,               # Lean — Go favours simplicity over density
        "volatility": 3.5,            # Low — the language is intentionally conservative
        "buoyancy": 8.5,              # Extremely easy to float — beginners love it
        "pour_temperature": "Room Temperature (Pragmatic, Ambient Use)",
        "distillation_notes": [
            "Goroutines are the vessel's contents — cheap, abundant, communicative.",
            "Channels are the vessel's neck — narrow and purposeful.",
            "The GC is the vessel's ambient pressure — always there, rarely noticed.",
            "Error values are the vessel's steam — let them escape or catch them.",
        ],
        "appearance": "Clear, pale liquid — like filtered water — transparency is the aesthetic",
        "odour": "Coffee and pragmatism — the scent of getting things done",
        "flame_test": "Steady blue flame — reliable, consistent, workmanlike",
        "shelf_life": "Stable — Go 1.x compatibility promise means long shelf life",
        "compatible_with": ["JavaScript", "Java"],
        "vessel_shape": "Stainless steel thermos — practical, utilitarian, keeps contents at steady temp",
    },
    "Swift": {
        "core_essence": "Protocol-Oriented Value Semantics — protocols as the architecture",
        "pressure_rating": 7.0,        # Demanding — but elegant when understood
        "density": 7.5,               # Rich type system with inference
        "volatility": 5.5,            # Moderate — Swift is still evolving (Swift 6 concurrency)
        "buoyancy": 6.0,              # Moderate — Apple ecosystem helps, else steeper
        "pour_temperature": "Warm (iOS/macOS Ecosystem — cosy, integrated)",
        "distillation_notes": [
            "Optional is the vessel's pressure release — use it to handle absence safely.",
            "Copy-on-write is the vessel's expansion joints — preventing spills.",
            "Structs are the vessel's preferred form — value types keep things contained.",
            "Actors (Swift 6) are the vessel's threaded sections — isolated but connected.",
        ],
        "appearance": "Silky silver liquid — like liquid metal — elegant and refined",
        "odour": "Apple blossom and clean compilation — the smell of XCode building",
        "flame_test": "White-hot bright flame — Apple-driven, premium quality",
        "shelf_life": "Excellent within Apple ecosystem — tied to platform longevity",
        "compatible_with": ["Rust", "Kotlin"],
        "vessel_shape": "Crystal decanter — beautiful, transparent, shows contents perfectly",
    },
    "Kotlin": {
        "core_essence": "JVM Null Safety + Coroutines — nullable types as first-class citizens",
        "pressure_rating": 5.5,        # Moderate — nullable types add checking overhead
        "density": 7.5,               # Rich features: coroutines, extensions, data classes
        "volatility": 4.0,            # Low — Kotlin is stable, JetBrains-backed
        "buoyancy": 7.5,              # High — runs on JVM, great tooling, Android adoption
        "pour_temperature": "Lukewarm (JVM Warmth — server-side and Android)",
        "distillation_notes": [
            "The nullable type (T?) is the vessel's distinct shape — you can always tell it by this.",
            "Coroutines are the vessel's internal bubbles — suspending without blocking.",
            "Extension functions are the vessel's custom nozzles — adding without altering.",
            "Data classes are the vessel's labelled compartments — structured and organised.",
        ],
        "appearance": "Deep amber liquid with emerald swirls — the JVM colour plus Kotlin green",
        "odour": "Cedar wood and Android — the scent of JetBrains polish",
        "flame_test": "Green-edged flame — distinctive, shows the Kotlin identity",
        "shelf_life": "Excellent — backed by JetBrains and Google, strong Android lock-in",
        "compatible_with": ["Swift", "Java"],
        "vessel_shape": "Copper Kettle — traditional, reliable, modernised for the JVM kitchen",
    },
    "TypeScript": {
        "core_essence": "Structural Gradual Typing — types as documentation that the compiler verifies",
        "pressure_rating": 5.0,        # Moderate — typing is opt-in, forgiving
        "density": 7.0,               # Generics, decorators, utility types — rich type system
        "volatility": 7.0,            # Higher — JS ecosystem moves fast, TS releases quarterly
        "buoyancy": 9.0,              # Extremely easy — if you know JS, you already partly know TS
        "pour_temperature": "Hot (Web-First — JavaScript ecosystem heat)",
        "distillation_notes": [
            "Type erasure at runtime is the vessel's invisible wall — types don't exist after compilation.",
            "The any type is the vessel's leak — avoid it or the contents spill everywhere.",
            "Generics are the vessel's custom moulds — reusable type shapes.",
            "Utility types (Partial, Required, etc.) are the vessel's handy accessories.",
        ],
        "appearance": "Translucent amber with visible type 'particles' floating — types as suspended matter",
        "odour": "Coffee and npm — the scent of a busy web server",
        "flame_test": "Orange flickering flame — dynamic, reactive, web-powered",
        "shelf_life": "Variable — web ecosystem moves quickly; LTS versions help",
        "compatible_with": ["JavaScript", "Rust"],
        "vessel_shape": "Plastic water bottle — ubiquitous, accessible, slightly permeable",
    },
    "JavaScript": {
        "core_essence": "Prototype-Based Dynamic Object Orientation — objects as prototype chains",
        "pressure_rating": 3.0,        # Low pressure — extremely permissive and flexible
        "density": 5.0,               # Low conceptual density per line — but powerful runtime
        "volatility": 8.0,            # Very high — ecosystem churn, framework wars
        "buoyancy": 9.5,              # Easiest to float — if you can run a browser, you run JS
        "pour_temperature": "Scalding (Runtime — executes immediately, no compile wait)",
        "distillation_notes": [
            "Prototype chain is the vessel's inheritance architecture — linked, not branched.",
            "Hoisting is the vessel's surprise — contents shift before you look.",
            "this is the vessel's chameleon — changes meaning in different contexts.",
            "The event loop is the vessel's circulation — keeps everything moving async.",
        ],
        "appearance": "Clear carbonated liquid — bubbly, reactive, full of suspended async events",
        "odour": "Node modules and callback pyramids — the npm install aroma",
        "flame_test": "Yellow-white hot flame — burns fast, runs everywhere",
        "shelf_life": "Short — ecosystem changes rapidly; frameworks have 2-3 year lifespans",
        "compatible_with": ["TypeScript", "Go"],
        "vessel_shape": "Paper cup — no ceremony, no pressure, everywhere at once",
    },
    "Java": {
        "core_essence": "JVM Platform + Object Orientation — write once, run everywhere on the JVM",
        "pressure_rating": 6.0,        # Moderate — checked exceptions, strict OO
        "density": 7.0,               # Generics, streams, annotations — rich platform
        "volatility": 2.5,            # Very low — Java 8 LTS ecosystems last a decade
        "buoyancy": 7.0,              # Good — mature tooling, huge talent pool, Android
        "pour_temperature": "Warm (JVM Warmth — long-running servers, enterprise kitchens)",
        "distillation_notes": [
            "The JVM is the vessel's universal container — contents are the same everywhere.",
            "Checked exceptions are the vessel's mandatory safety warnings — you must handle them.",
            "Generics are the vessel's type moulds — compile-time erasure with runtime flexibility.",
            "Streams are the vessel's pipelines — data flows through without individual handling.",
        ],
        "appearance": "Rich brown liquid — coffee-dark, enterprise-strength, with a cream of tooling on top",
        "odour": "Dark roast and Apache libraries — enterprise coffee shop",
        "flame_test": "Slow steady burn — long flame, sustainable, enterprise-grade",
        "shelf_life": "Exceptional — Java 8 codebases run unchanged for 10+ years",
        "compatible_with": ["Kotlin", "Go"],
        "vessel_shape": "French press — big, dependable, produces large batches steadily",
    },
    "C/C++": {
        "core_essence": "Zero-Abstraction Memory Control — direct access to hardware with maximum performance",
        "pressure_rating": 9.8,        # Extremely high — manual memory, undefined behaviour
        "density": 10.0,               # Maximum density — everything is explicit, nothing hidden
        "volatility": 1.5,            # Extremely stable — the language hasn't fundamentally changed in decades
        "buoyancy": 1.5,              # Sinks fast — UB, pointers, manual memory are dangerous
        "pour_temperature": "Cryogenic (Systems Level — close to the metal)",
        "distillation_notes": [
            "Undefined behaviour is the vessel's invisible crack — contents escape silently.",
            "Pointers are the vessel's exposed seams — handle with extreme care.",
            "RAII is the vessel's auto-seal — resources freed when scope exits.",
            "Templates are the vessel's custom-casting capability — compile-time metaprogramming.",
        ],
        "appearance": "Dark, almost black liquid — like liquid iron, dense and unforgiving",
        "odour": "Machine oil and meltedsolder — the scent of bare metal",
        "flame_test": "White-hot blowtorch flame — maximum heat, maximum danger",
        "shelf_life": "Virtually eternal — C89 code still compiles. Nothing lasts longer.",
        "compatible_with": ["Rust"],
        "vessel_shape": "Open crucible — no lid, no safety guards — raw, powerful, demands mastery",
    },
}


# ── Helper functions ───────────────────────────────────────────────────────────

def load_rotation() -> dict:
    """Load language rotation config."""
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: dict) -> None:
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def advance_rotation() -> Tuple[str, int, str]:
    """Advance rotation, return (language, old_index, next_language)."""
    config = load_rotation()
    languages = config.get("languages", ROTATION_ORDER)
    current_index = config.get("current_index", 0)

    current_language = languages[current_index % len(languages)]

    next_index = (current_index + 1) % len(languages)
    next_language = languages[next_index]

    config["current_index"] = next_index
    config["last_language"] = current_language
    config["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation(config)

    return current_language, current_index, next_language


def get_current_language() -> str:
    """Return the current rotation language without advancing."""
    config = load_rotation()
    languages = config.get("languages", ROTATION_ORDER)
    current_index = config.get("current_index", 0)
    return languages[current_index % len(languages)]


# ── Core report generation ────────────────────────────────────────────────────

def _pressure_label(rating: float) -> str:
    """Convert pressure rating to descriptive label."""
    if rating >= 9.0:
        return "CRITICAL — Extreme caution required"
    elif rating >= 7.5:
        return "HIGH — Significant mental overhead"
    elif rating >= 5.0:
        return "MODERATE — Balanced demands"
    elif rating >= 3.0:
        return "LOW — Approachable"
    else:
        return "MINIMAL — Forgiving and permissive"


def _density_label(density: float) -> str:
    """Convert density to descriptive label."""
    if density >= 9.0:
        return "EXTREMELY DENSE — Every concept is rich and layered"
    elif density >= 7.0:
        return "DENSE — High information density per line"
    elif density >= 5.0:
        return "MODERATE — Balanced concept density"
    else:
        return "LIGHT — Lean, minimal concepts per construct"


def _volatility_label(volatility: float) -> str:
    """Convert volatility to descriptive label."""
    if volatility >= 7.5:
        return "VOLATILE — Ecosystem/versions change rapidly"
    elif volatility >= 5.0:
        return "MODERATE — Regular but managed evolution"
    elif volatility >= 3.0:
        return "STABLE — Slow, careful language evolution"
    else:
        return "CRYSTALLISED — Virtually no breaking changes"


def _buoyancy_label(buoyancy: float) -> str:
    """Convert buoyancy to descriptive label."""
    if buoyancy >= 8.5:
        return "EXCELLENT — Floats immediately; beginners welcome"
    elif buoyancy >= 6.5:
        return "GOOD — Moderate learning curve"
    elif buoyancy >= 4.0:
        return "MODERATE — Some learning investment required"
    elif buoyancy >= 2.0:
        return "POOR — Steep curve; not recommended for beginners"
    else:
        return "SINKS FAST — Extreme difficulty; demands deep expertise"


def _make_bar(value: float, width: int = 20) -> str:
    """Create a visual bar for a 0-10 scale value."""
    filled = int((value / 10.0) * width)
    empty = width - filled
    return "[" + "█" * filled + "░" * empty + "]"


def _overall_vessel_score(pressure: float, density: float,
                           volatility: float, buoyancy: float) -> Dict[str, Any]:
    """Calculate overall vessel quality/professionalism score."""
    # Balance: low pressure + high buoyancy = easy to use
    # Density + low volatility = reliable, informative
    usability = ((10 - pressure) / 10.0) * 0.4 + (buoyancy / 10.0) * 0.4
    reliability = ((10 - volatility) / 10.0) * 0.5 + (density / 10.0) * 0.5

    overall = usability * 0.5 + reliability * 0.5

    if overall >= 0.75:
        grade = "A — Premium vessel"
    elif overall >= 0.60:
        grade = "B — Professional grade"
    elif overall >= 0.45:
        grade = "C — Trade-grade vessel"
    elif overall >= 0.30:
        grade = "D — Specialised, niche tool"
    else:
        grade = "F — Raw material (handle with extreme care)"

    return {
        "overall_score": round(overall, 3),
        "grade": grade,
        "usability": round(usability, 3),
        "reliability": round(reliability, 3),
    }


def generate_vessel_report(seed: Optional[int] = None) -> Dict[str, Any]:
    """Generate a vessel report for the current rotation language."""
    if seed is not None:
        rng = random.Random(seed)
    else:
        rng = random.Random()

    language, old_index, next_language = advance_rotation()

    if language not in VESSEL_DATA:
        raise ValueError(f"Unknown language: {language}. Available: {list(VESSEL_DATA.keys())}")

    vd = VESSEL_DATA[language]

    # Build bar visualizations
    pressure_bar = _make_bar(vd["pressure_rating"])
    density_bar = _make_bar(vd["density"])
    volatility_bar = _make_bar(vd["volatility"])
    buoyancy_bar = _make_bar(vd["buoyancy"])

    overall = _overall_vessel_score(
        vd["pressure_rating"], vd["density"],
        vd["volatility"], vd["buoyancy"]
    )

    # Build the structured report
    report = {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": language,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "rotation_advanced": True,
        "previous_index": old_index,
        "next_language": next_language,
        "rotation_order": ROTATION_ORDER,

        "vessel_certificate": {
            "core_essence": vd["core_essence"],
            "vessel_shape": vd["vessel_shape"],
            "appearance": vd["appearance"],
            "odour": vd["odour"],
            "flame_test": vd["flame_test"],
            "shelf_life": vd["shelf_life"],
        },

        "physical_properties": {
            "pressure_rating": {
                "value": vd["pressure_rating"],
                "label": _pressure_label(vd["pressure_rating"]),
                "bar": pressure_bar,
                "description": "How demanding the language is on the programmer's mental model",
            },
            "density": {
                "value": vd["density"],
                "label": _density_label(vd["density"]),
                "bar": density_bar,
                "description": "How much is packed into each concept/construct",
            },
            "volatility": {
                "value": vd["volatility"],
                "label": _volatility_label(vd["volatility"]),
                "bar": volatility_bar,
                "description": "How stable/changing the language ecosystem is",
            },
            "buoyancy": {
                "value": vd["buoyancy"],
                "label": _buoyancy_label(vd["buoyancy"]),
                "bar": buoyancy_bar,
                "description": "How easy the language is to get started with",
            },
        },

        "pour_temperature": vd["pour_temperature"],

        "distillation_notes": vd["distillation_notes"],

        "compatible_with": vd["compatible_with"],

        "overall_assessment": overall,
    }

    return report


def format_vessel_report(report: Dict[str, Any]) -> str:
    """Format a vessel report as a human-readable ASCII report."""
    lang = report["language"]
    cert = report["vessel_certificate"]
    props = report["physical_properties"]
    overall = report["overall_assessment"]

    lines = [
        "",
        "=" * 60,
        f"  🏺 POLYGLOT VESSEL — CERTIFICATE OF ANALYSIS",
        f"  {report['tool']} v{report['version']}",
        "=" * 60,
        "",
        f"  Language:    {lang}",
        f"  Essence:     {cert['core_essence']}",
        f"  Vessel:      {cert['vessel_shape']}",
        f"  Temp:        {report['pour_temperature']}",
        "",
        "-" * 60,
        "  PHYSICAL PROPERTIES",
        "-" * 60,
        f"  Pressure   {props['pressure_rating']['bar']} {props['pressure_rating']['value']}/10",
        f"             {props['pressure_rating']['label']}",
        f"  Density    {props['density']['bar']} {props['density']['value']}/10",
        f"             {props['density']['label']}",
        f"  Volatility {props['volatility']['bar']} {props['volatility']['value']}/10",
        f"             {props['volatility']['label']}",
        f"  Buoyancy   {props['buoyancy']['bar']} {props['buoyancy']['value']}/10",
        f"             {props['buoyancy']['label']}",
        "",
        "-" * 60,
        "  ORGANOLEPTIC PROPERTIES",
        "-" * 60,
        f"  Appearance: {cert['appearance']}",
        f"  Odour:      {cert['odour']}",
        f"  Flame Test: {cert['flame_test']}",
        "",
        "-" * 60,
        "  DISTILLATION NOTES",
        "-" * 60,
    ]

    for i, note in enumerate(report["distillation_notes"], 1):
        lines.append(f"  {i}. {note}")

    lines.extend([
        "",
        "-" * 60,
        "  OVERALL ASSESSMENT",
        "-" * 60,
        f"  Grade:       {overall['grade']}",
        f"  Score:       {overall['overall_score']} / 1.000",
        f"  Usability:   {overall['usability']:.3f}",
        f"  Reliability: {overall['reliability']:.3f}",
        f"  Shelf Life:  {cert['shelf_life']}",
        "",
        "-" * 60,
        "  COMPATIBILITY",
        "-" * 60,
        f"  Compatible with: {', '.join(report['compatible_with'])}",
        "",
        "-" * 60,
        "  ROTATION",
        "-" * 60,
        f"  Previous Index: {report['previous_index']}",
        f"  Next Language:  {report['next_language']}",
        f"  Rotation Order: {' → '.join(report['rotation_order'])} → {report['rotation_order'][0]}",
        "",
        "=" * 60,
        f"  🏺 {lang} — The {cert['vessel_shape'].split()[0]} vessel",
        f"  {cert['core_essence'][:55]}",
        "=" * 60,
        "",
    ])

    return "\n".join(lines)


# ── Tests ──────────────────────────────────────────────────────────────────────

def run_tests():
    """Run all unit tests for polyglot_vessel."""
    import sys

    errors = []
    passed = 0

    def t(name: str, cond: bool, msg: str = ""):
        nonlocal passed, errors
        if cond:
            print(f"  ✅ {name}")
            passed += 1
        else:
            print(f"  ❌ {name}: {msg}")
            errors.append(name)

    print("🏺 Polyglot Vessel — Running Tests\n")

    # Test: load_rotation
    try:
        config = load_rotation()
        t("load_rotation() returns valid dict", isinstance(config, dict))
        t("rotation has 'languages' key", "languages" in config)
        t("rotation has 'current_index' key", "current_index" in config)
        t("languages is a list", isinstance(config["languages"], list))
        t("languages has 8 entries", len(config["languages"]) == 8)
    except Exception as e:
        t("load_rotation() succeeds", False, str(e))

    # Test: ROTATION_ORDER
    for lang in ROTATION_ORDER:
        t(f"ROTATION_ORDER contains '{lang}'", lang in ROTATION_ORDER)

    # Test: VESSEL_DATA has all 8 languages
    for lang in ROTATION_ORDER:
        t(f"VESSEL_DATA has '{lang}'", lang in VESSEL_DATA)
        if lang in VESSEL_DATA:
            vd = VESSEL_DATA[lang]
            t(f"  - {lang} has 'core_essence'", "core_essence" in vd)
            t(f"  - {lang} has 'pressure_rating'", "pressure_rating" in vd)
            t(f"  - {lang} has 'density'", "density" in vd)
            t(f"  - {lang} has 'volatility'", "volatility" in vd)
            t(f"  - {lang} has 'buoyancy'", "buoyancy" in vd)
            t(f"  - {lang} pressure_rating is 0-10", 0 <= vd["pressure_rating"] <= 10)
            t(f"  - {lang} density is 0-10", 0 <= vd["density"] <= 10)
            t(f"  - {lang} volatility is 0-10", 0 <= vd["volatility"] <= 10)
            t(f"  - {lang} buoyancy is 0-10", 0 <= vd["buoyancy"] <= 10)
            t(f"  - {lang} has 'distillation_notes'", "distillation_notes" in vd)
            t(f"  - {lang} distillation_notes is list of 4", isinstance(vd["distillation_notes"], list) and len(vd["distillation_notes"]) == 4)
            t(f"  - {lang} has 'compatible_with'", "compatible_with" in vd)
            t(f"  - {lang} has 'vessel_shape'", "vessel_shape" in vd)
            t(f"  - {lang} has 'appearance'", "appearance" in vd)
            t(f"  - {lang} has 'odour'", "odour" in vd)
            t(f"  - {lang} has 'flame_test'", "flame_test" in vd)
            t(f"  - {lang} has 'shelf_life'", "shelf_life" in vd)
            t(f"  - {lang} has 'pour_temperature'", "pour_temperature" in vd)

    # Test: helper functions
    t("_pressure_label works", _pressure_label(9.5) == "CRITICAL — Extreme caution required")
    t("_density_label works", _density_label(9.5) == "EXTREMELY DENSE — Every concept is rich and layered")
    t("_volatility_label works", _volatility_label(8.0) == "VOLATILE — Ecosystem/versions change rapidly")
    t("_buoyancy_label works", _buoyancy_label(9.5) == "EXCELLENT — Floats immediately; beginners welcome")
    t("_make_bar produces correct width", len(_make_bar(5.0)) == 22)  # [████████░░░░░░░░░░]

    # Test: _overall_vessel_score
    score = _overall_vessel_score(9.8, 10.0, 1.5, 1.5)
    t("_overall_vessel_score returns dict", isinstance(score, dict))
    t("_overall_vessel_score has 'overall_score'", "overall_score" in score)
    t("_overall_vessel_score has 'grade'", "grade" in score)
    t("_overall_vessel_score overall_score is 0-1", 0 <= score["overall_score"] <= 1)

    # Test: generate_vessel_report
    cfg_before = load_rotation()
    idx_before = cfg_before["current_index"]
    report = generate_vessel_report()
    cfg_after = load_rotation()
    idx_after = cfg_after["current_index"]

    t("generate_vessel_report() returns dict", isinstance(report, dict))
    t("report has 'language' key", "language" in report)
    t("report has 'vessel_certificate' key", "vessel_certificate" in report)
    t("report has 'physical_properties' key", "physical_properties" in report)
    t("report has 'distillation_notes' key", "distillation_notes" in report)
    t("report has 'overall_assessment' key", "overall_assessment" in report)
    t("report has 'rotation_advanced' == True", report.get("rotation_advanced") is True)
    t("report has 'next_language' key", "next_language" in report)
    t("report has 'rotation_order' key", "rotation_order" in report)
    t("rotation_order has 8 languages", len(report["rotation_order"]) == 8)
    t("generate_vessel_report advances current_index",
      idx_after == (idx_before + 1) % len(cfg_before["languages"]))

    # Test: report has 4 physical properties
    props = report["physical_properties"]
    t("physical_properties has 4 entries", len(props) == 4)
    for key in ["pressure_rating", "density", "volatility", "buoyancy"]:
        t(f"  - physical_properties has '{key}'", key in props)
        t(f"  - {key} has 'value'", "value" in props[key])
        t(f"  - {key} has 'label'", "label" in props[key])
        t(f"  - {key} has 'bar'", "bar" in props[key])
        t(f"  - {key}.bar is 22 chars wide", len(props[key]["bar"]) == 22)

    # Test: format_vessel_report
    formatted = format_vessel_report(report)
    t("format_vessel_report returns string", isinstance(formatted, str))
    t("format_vessel_report mentions language", lang in formatted)
    t("format_vessel_report has separators", "=" in formatted)
    t("format_vessel_report has bar characters", "█" in formatted)
    t("format_vessel_report mentions next_language", report["next_language"] in formatted)

    # Test: get_current_language (does not advance)
    cfg_before2 = load_rotation()
    lang_now = get_current_language()
    cfg_after2 = load_rotation()
    t("get_current_language() does not advance rotation",
      cfg_before2["current_index"] == cfg_after2["current_index"])
    t("get_current_language() returns a string", isinstance(lang_now, str))
    t("get_current_language() returns valid language", lang_now in ROTATION_ORDER)

    # Test: generate_vessel_report with seed is functional (seed param accepted)
    try:
        r1 = generate_vessel_report(seed=123)
        r2 = generate_vessel_report(seed=456)
        t("generate_vessel_report(seed=N) accepts seed parameter", isinstance(r1, dict) and isinstance(r2, dict))
        t("generate_vessel_report(seed=N) returns valid language", r1["language"] in ROTATION_ORDER)
        # Seed affects internal rng for any future random selections within the report
        t("generate_vessel_report(seed=N) returns report with all required keys",
          all(k in r1 for k in ["language", "vessel_certificate", "physical_properties", "distillation_notes", "overall_assessment"]))
    except Exception as e:
        t("generate_vessel_report(seed=N) succeeds", False, str(e))

    # Test: unknown language (after exhausting)
    try:
        # Cycle through all languages
        for _ in range(10):
            generate_vessel_report()
        t("multiple generate_vessel_report calls succeed", True)
    except Exception as e:
        t("multiple generate_vessel_report calls succeed", False, str(e))

    print(f"\n{'=' * 50}")
    if errors:
        print(f"❌ {len(errors)} test(s) failed:")
        for e in errors:
            print(f"   - {e}")
        sys.exit(1)
    else:
        print(f"✅ All {passed} tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        result = generate_vessel_report()
        print(format_vessel_report(result))
