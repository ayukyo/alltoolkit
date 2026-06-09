#! /usr/bin/env python3
"""
🌡️ Polyglot Meridian v1.0
A creative tool that maps programming languages on spectral dimensions.

Creative concept: "Every language exists on a spectrum — between static and dynamic,
between manual and automatic memory, between young and mature. Polyglot Meridian
charts these positions on visual spectrum lines, like coordinates on a cartographer's
map, revealing where each language stands in the design space."

The tool generates:
  1. A "meridian chart" showing language positions on 6 spectrum dimensions
  2. Coordinate summary (latitude/longitude metaphor in language design space)
  3. A "design climate" classification based on position clusters
  4. Distance calculation to other languages on the spectrum

Distinct from existing tools:
  - polyglot_dna:          genetic/molecular metaphor (traits as nucleotides)
  - language_compass:       learning journey maps (progress/rrogress)
  - language_synapse:       conceptual bridges between languages (connections)
  - polyglot_chronicle:     daily diary + history + challenge (temporal)
  - polyglot_digest:        side-by-side syntax parallel (syntax comparison)
  - language_ethos:         philosophical manifesto (beliefs/identity)
  - language_sage:          idioms, tips, pitfalls (practical wisdom)
  - language_ecohub:        package ecosystem guide (tooling/infrastructure)
  - language_archaeology:   historical lineage & design philosophy (origin/history)
  - polyglot_flavor:        taste/texture of language aesthetics
  - polyglot_resonator:     harmonic relationships between languages

Polyglot Meridian is about SPECTRAL POSITIONING — where each language sits
on key design spectrums, visualized as coordinates in language design space.
"""

import json
import os
import math
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-meridian"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "language_rotation.json"
)

# The 8-language rotation sequence for this tool
ROTATION_SEQUENCE = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]

# ── Meridian dimensions (spectrum definitions) ───────────────────────────────
# Each dimension has two poles and a midpoint
# Values: 0.0 (pole A) → 0.5 (balanced) → 1.0 (pole B)
MERIDIAN_DIMENSIONS = [
    {
        "id": "memory_model",
        "name": "Memory Model",
        "pole_a": "Manual (Programmer)",
        "pole_b": "Automatic (GC/Runtime)",
        "description": "Who controls memory allocation and deallocation?",
    },
    {
        "id": "type_system",
        "name": "Type System",
        "pole_a": "Dynamic",
        "pole_b": "Static",
        "description": "When are types checked?",
    },
    {
        "id": "safety_focus",
        "name": "Safety Focus",
        "pole_a": "Speed First",
        "pole_b": "Safe First",
        "description": "Does the language prioritize performance or safety?",
    },
    {
        "id": "abstraction_level",
        "name": "Abstraction Level",
        "pole_a": "Low-Level (Systems)",
        "pole_b": "High-Level (Application)",
        "description": "How close to the metal does the language operate?",
    },
    {
        "id": "concurrency_model",
        "name": "Concurrency Model",
        "pole_a": "Async/Event-Driven",
        "pole_b": "Sync/Thread-Based",
        "description": "How does the language handle parallel work?",
    },
    {
        "id": "paradigm",
        "name": "Paradigm",
        "pole_a": "Functional",
        "pole_b": "Object-Oriented",
        "description": "What is the primary programming paradigm?",
    },
]

# ── Language meridian positions ───────────────────────────────────────────────
# Each language has a position (0.0 to 1.0) on each dimension
LANGUAGE_MERIDIANS: Dict[str, Dict[str, float]] = {
    "Rust": {
        "memory_model": 0.15,    # Manual/Ownership-based (no GC, compile-time)
        "type_system": 0.95,      # Static with inference
        "safety_focus": 0.95,      # Memory + concurrency safety first
        "abstraction_level": 0.55, # Mid-range: systems + app
        "concurrency_model": 0.80, # Thread-based with Send/Sync
        "paradigm": 0.40,          # Multi-paradigm (functional influence)
    },
    "Go": {
        "memory_model": 0.85,     # GC (automatic)
        "type_system": 0.90,      # Static
        "safety_focus": 0.75,      # Safe but pragmatic
        "abstraction_level": 0.60, # Mid to high
        "concurrency_model": 0.10, # Async/CSP (goroutines)
        "paradigm": 0.50,          # Multi-paradigm
    },
    "Swift": {
        "memory_model": 0.70,     # ARC (reference counting, not tracing GC)
        "type_system": 0.95,       # Static with inference
        "safety_focus": 0.90,      # Safe by default
        "abstraction_level": 0.65, # High-level application
        "concurrency_model": 0.70, # Thread-based (actors in newer Swift)
        "paradigm": 0.60,          # Multi-paradigm (OO + functional)
    },
    "Kotlin": {
        "memory_model": 0.85,      # JVM GC
        "type_system": 0.95,       # Static
        "safety_focus": 0.85,      # Null safety, coroutines
        "abstraction_level": 0.70, # High-level application
        "concurrency_model": 0.30, # Coroutines (structured async)
        "paradigm": 0.65,          # OO + functional
    },
    "TypeScript": {
        "memory_model": 0.95,      # JS runtime (GC)
        "type_system": 0.85,       # Static (gradual)
        "safety_focus": 0.60,      # Opt-in types, not mandatory
        "abstraction_level": 0.80, # High-level web
        "concurrency_model": 0.20, # Async/await (event loop)
        "paradigm": 0.45,          # Multi-paradigm
    },
    "JavaScript": {
        "memory_model": 0.95,      # JS runtime (GC)
        "type_system": 0.20,       # Dynamic
        "safety_focus": 0.40,      # Flexible, footguns exist
        "abstraction_level": 0.85, # Very high-level (web)
        "concurrency_model": 0.15,  # Async/await (event loop)
        "paradigm": 0.50,          # Multi-paradigm (prototype OO, functional)
    },
    "Java": {
        "memory_model": 0.85,      # JVM GC
        "type_system": 0.95,        # Static
        "safety_focus": 0.75,      # Type safety, checked exceptions
        "abstraction_level": 0.65, # Mid-high (JVM abstraction)
        "concurrency_model": 0.75, # Thread-based
        "paradigm": 0.70,          # OO-primary
    },
    "C/C++": {
        "memory_model": 0.05,      # Fully manual
        "type_system": 0.80,       # Static (C) to mostly static (C++)
        "safety_focus": 0.15,       # Performance first
        "abstraction_level": 0.25,  # Low-level systems
        "concurrency_model": 0.85, # Thread-based (native)
        "paradigm": 0.55,          # Multi-paradigm
    },
}


def load_rotation():
    """Load language rotation config."""
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data):
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _value_to_label(value: float, pole_a: str, pole_b: str) -> str:
    """Convert a 0.0-1.0 value to a descriptive label."""
    if value < 0.2:
        return pole_a
    elif value > 0.8:
        return pole_b
    else:
        mid = (pole_a + " / " + pole_b).replace("First", "First\n/ ").replace("Driven", "Driven\n/ ")
        return f"Balanced ({pole_a[:10]}-{pole_b[:10]})"


def _build_spectrum_bar(value: float, width: int = 20) -> str:
    """Build a visual spectrum bar like [██░░░░░░░░░░░░░░░]."""
    filled = int(value * width)
    empty = width - filled
    return "[" + "█" * filled + "░" * empty + "]"


def generate_meridian_chart(language: str) -> Dict[str, Any]:
    """Generate full meridian chart for a language."""
    if language not in LANGUAGE_MERIDIANS:
        raise ValueError(f"Unknown language: {language}. Available: {list(LANGUAGE_MERIDIANS.keys())}")

    positions = LANGUAGE_MERIDIANS[language]

    # Build spectrum lines
    spectrum_lines = []
    for dim in MERIDIAN_DIMENSIONS:
        dim_id = dim["id"]
        value = positions.get(dim_id, 0.5)
        bar = _build_spectrum_bar(value)
        label = _value_to_label(value, dim["pole_a"], dim["pole_b"])

        spectrum_lines.append({
            "dimension": dim["name"],
            "dimension_id": dim_id,
            "value": value,
            "pole_a": dim["pole_a"],
            "pole_b": dim["pole_b"],
            "label": label,
            "bar": bar,
            "description": dim["description"],
        })

    # Calculate "coordinates" (latitude/longitude in design space)
    # Longitude: average of memory_model + type_system + abstraction_level
    # Latitude: average of safety_focus + paradigm
    longitude = (positions.get("memory_model", 0.5) +
                 positions.get("type_system", 0.5) +
                 positions.get("abstraction_level", 0.5)) / 3.0
    latitude = (positions.get("safety_focus", 0.5) +
                positions.get("paradigm", 0.5)) / 2.0

    # Design climate based on position
    if longitude < 0.4 and latitude < 0.4:
        climate = "Arctic Systems (Low-level, Performance-first)"
    elif longitude < 0.4 and latitude > 0.6:
        climate = "Tundra Functional (Low-level, Safety-first)"
    elif longitude > 0.7 and latitude < 0.4:
        climate = "Tropical Scripting (High-level, Flexible)"
    elif longitude > 0.7 and latitude > 0.6:
        climate = "Equatorial Enterprise (High-level, Safe Application)"
    else:
        climate = "Temperate Balanced (Mid-range, Pragmatic)"

    # Overall "energy level" (average of all positions)
    energy = sum(positions.values()) / len(positions)

    return {
        "language": language,
        "coordinates": {
            "longitude": round(longitude, 3),
            "latitude": round(latitude, 3),
            "energy": round(energy, 3),
        },
        "climate": climate,
        "spectrum_dimensions": spectrum_lines,
        "raw_positions": positions,
    }


def calculate_distance(lang_a: str, lang_b: str) -> Dict[str, Any]:
    """Calculate Euclidean distance between two languages in design space."""
    if lang_a not in LANGUAGE_MERIDIANS:
        raise ValueError(f"Unknown language: {lang_a}")
    if lang_b not in LANGUAGE_MERIDIANS:
        raise ValueError(f"Unknown language: {lang_b}")

    pos_a = LANGUAGE_MERIDIANS[lang_a]
    pos_b = LANGUAGE_MERIDIANS[lang_b]

    # Euclidean distance in 6-dimensional space
    sum_sq = 0.0
    dimension_distances = []
    for dim in MERIDIAN_DIMENSIONS:
        dim_id = dim["id"]
        da = pos_a.get(dim_id, 0.5)
        db = pos_b.get(dim_id, 0.5)
        diff = da - db
        sum_sq += diff * diff
        dimension_distances.append({
            "dimension": dim["name"],
            f"{lang_a}_value": da,
            f"{lang_b}_value": db,
            "difference": round(abs(diff), 3),
        })

    distance = math.sqrt(sum_sq)
    max_distance = math.sqrt(len(MERIDIAN_DIMENSIONS))  # Max possible = sqrt(6) ≈ 2.45
    normalized = distance / max_distance

    # Classification
    if normalized < 0.2:
        classification = "Nearly Identical"
    elif normalized < 0.4:
        classification = "Similar"
    elif normalized < 0.6:
        classification = "Distinct"
    else:
        classification = "Fundamentally Different"

    return {
        "language_a": lang_a,
        "language_b": lang_b,
        "euclidean_distance": round(distance, 3),
        "normalized_distance": round(normalized, 3),
        "max_distance": round(max_distance, 3),
        "classification": classification,
        "dimension_distances": dimension_distances,
        "summary": f"{lang_a} and {lang_b} are {classification.lower()} in design space (distance: {round(normalized*100,1)}% of max).",
    }


def generate_all_positions() -> Dict[str, Any]:
    """Generate meridian positions for all 8 languages."""
    all_positions = {}
    for lang in LANGUAGE_MERIDIANS:
        all_positions[lang] = generate_meridian_chart(lang)
    return all_positions


# ── Rotation-aware entry point ─────────────────────────────────────────────────

def meridian() -> Dict[str, Any]:
    """
    Main entry: advance rotation and generate meridian chart for the selected language.
    Reads current_index from language_rotation.json, selects that language,
    advances index, saves, then returns the meridian analysis.
    """
    config = load_rotation()
    languages = config.get("languages", [])
    if not languages:
        raise ValueError("No languages found in rotation config")

    current_index = config.get("current_index", 0)

    # Find the next language in the rotation sequence
    # We need to find which language in the full list corresponds to our sequence
    sequence_index = 0
    for i in range(len(languages)):
        candidate = languages[(current_index + i) % len(languages)]
        if candidate in ROTATION_SEQUENCE:
            sequence_index = (current_index + i) % len(languages)
            break

    current_language = languages[sequence_index]
    if current_language not in LANGUAGE_MERIDIANS:
        # Fall back to first in rotation sequence that exists
        current_language = ROTATION_SEQUENCE[0]

    # Advance for next run
    next_index = (sequence_index + 1) % len(languages)
    config["current_index"] = next_index
    config["last_language"] = current_language
    config["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation(config)

    result = generate_meridian_chart(current_language)
    result["rotation_advanced"] = True
    result["next_language"] = languages[next_index] if next_index < len(languages) else languages[0]
    result["next_index"] = next_index
    result["rotation_sequence"] = ROTATION_SEQUENCE
    return result


# ── Tests ─────────────────────────────────────────────────────────────────────

def run_tests():
    """Run all tests for the polyglot_meridian module."""
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

    print("🌡️ Polyglot Meridian — Running Tests\n")

    # Test: rotation file exists and is valid JSON
    try:
        config = load_rotation()
        t("load_rotation() returns valid dict", isinstance(config, dict))
        t("rotation has languages list", "languages" in config)
        t("rotation has current_index", "current_index" in config)
    except Exception as e:
        t("load_rotation() succeeds", False, str(e))

    # Test: ROTATION_SEQUENCE has all 8 languages
    for lang in ROTATION_SEQUENCE:
        t(f"ROTATION_SEQUENCE has '{lang}'", lang in ROTATION_SEQUENCE)

    # Test: LANGUAGE_MERIDIANS has all 8 languages
    for lang in ROTATION_SEQUENCE:
        t(f"LANGUAGE_MERIDIANS has '{lang}'", lang in LANGUAGE_MERIDIANS)

    # Test: All languages have positions for all 6 dimensions
    for lang in LANGUAGE_MERIDIANS:
        positions = LANGUAGE_MERIDIANS[lang]
        t(f"{lang} has 6 dimension positions", len(positions) == 6)
        for dim in MERIDIAN_DIMENSIONS:
            t(f"  - {lang} has '{dim['id']}'", dim["id"] in positions)
            value = positions[dim["id"]]
            t(f"  - {lang}.{dim['id']} is 0.0-1.0", 0.0 <= value <= 1.0)

    # Test: MERIDIAN_DIMENSIONS has 6 dimensions
    t("MERIDIAN_DIMENSIONS has 6 dimensions", len(MERIDIAN_DIMENSIONS) == 6)

    # Test: generate_meridian_chart
    for lang in LANGUAGE_MERIDIANS:
        try:
            result = generate_meridian_chart(lang)
            t(f"generate_meridian_chart('{lang}') succeeds", True)
            t(f"  - returns 'coordinates'", "coordinates" in result)
            t(f"  - returns 'climate'", "climate" in result)
            t(f"  - returns 'spectrum_dimensions'", "spectrum_dimensions" in result)
            t(f"  - returns 'raw_positions'", "raw_positions" in result)
            t(f"  - spectrum has 6 entries", len(result["spectrum_dimensions"]) == 6)

            # Check coordinates structure
            coords = result["coordinates"]
            t(f"  - coordinates has longitude", "longitude" in coords)
            t(f"  - coordinates has latitude", "latitude" in coords)
            t(f"  - coordinates has energy", "energy" in coords)

            # Check spectrum entries have required keys
            for entry in result["spectrum_dimensions"]:
                t(f"  - spectrum entry has required keys",
                  all(k in entry for k in ["dimension", "value", "bar", "pole_a", "pole_b"]))
        except Exception as e:
            t(f"generate_meridian_chart('{lang}')", False, str(e))

    # Test: calculate_distance
    try:
        dist = calculate_distance("Rust", "C/C++")
        t("calculate_distance('Rust', 'C/C++') succeeds", True)
        t("  - returns euclidean_distance", "euclidean_distance" in dist)
        t("  - returns normalized_distance", "normalized_distance" in dist)
        t("  - returns classification", "classification" in dist)
        t("  - distance is positive", dist["euclidean_distance"] > 0)
        t("  - normalized is 0-1", 0 <= dist["normalized_distance"] <= 1)
    except Exception as e:
        t("calculate_distance", False, str(e))

    # Test: calculate_distance symmetric
    try:
        dist_ab = calculate_distance("Rust", "Go")
        dist_ba = calculate_distance("Go", "Rust")
        t("calculate_distance is symmetric", dist_ab["euclidean_distance"] == dist_ba["euclidean_distance"])
    except Exception as e:
        t("calculate_distance symmetry", False, str(e))

    # Test: generate_all_positions
    try:
        all_pos = generate_all_positions()
        t("generate_all_positions() succeeds", True)
        t("  - returns dict", isinstance(all_pos, dict))
        t("  - has 8 entries", len(all_pos) == 8)
    except Exception as e:
        t("generate_all_positions", False, str(e))

    # Test: meridian() advances rotation
    try:
        cfg_before = load_rotation()
        idx_before = cfg_before["current_index"]
        result = meridian()
        cfg_after = load_rotation()
        idx_after = cfg_after["current_index"]
        t("meridian() advances current_index", idx_after == (idx_before + 1) % len(cfg_before["languages"]))
        t("meridian() returns rotation_advanced=True", result.get("rotation_advanced") is True)
        t("meridian() returns selected language", "language" in result)
        t("meridian() returns next_language", "next_language" in result)
        t("meridian() returns rotation_sequence", "rotation_sequence" in result)
    except Exception as e:
        t("meridian() rotation advancement", False, str(e))

    # Test: unknown language raises ValueError
    try:
        generate_meridian_chart("Brainfuck")
        t("Unknown language raises ValueError", False, "did not raise")
    except ValueError as e:
        t("Unknown language raises ValueError", True)
    except Exception as e:
        t("Unknown language raises ValueError", False, f"wrong exception: {e}")

    print(f"\n{'='*50}")
    if errors:
        print(f"❌ {len(errors)} test(s) failed: {', '.join(errors)}")
        sys.exit(1)
    else:
        print(f"✅ All {passed} tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        result = meridian()
        print(json.dumps(result, indent=2))