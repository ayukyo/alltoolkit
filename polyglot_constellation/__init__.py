#!/usr/bin/env python3
"""
🌌 Polyglot Constellation v1.0

A creative tool that maps programming languages as stars in a constellation —
visualizing language relationships as gravitational fields, stellar distances,
and constellation patterns across the "polyglot night sky."

Creative concept: "Every language is a star in a constellation. Some burn bright
and close (high compatibility), others are distant and dim (paradigm leaps).
This tool maps the night sky of languages — showing the gravitational pull
between them, the stellar distances you must travel, and the constellation
patterns they form."

For the selected rotation language, this tool:
  1. Maps the language as the "current star" in the constellation
  2. Shows gravitational fields (ecosystem strength, paradigm alignment, learning transfer)
  3. Displays distances to all other language "stars" as light-year equivalents
  4. Reveals the constellation pattern (which languages form recognizable shapes)
  5. Generates star metadata (magnitude, spectral class, luminosity)
  6. Updates language_rotation.json

Distinct from existing tools:
  - polyglot_dna:         genetic trait mapping (molecular biology)
  - polyglot_resonator:   mental model frames (how each language THINKS)
  - polyglot_harmony:     compatibility scores between consecutive pairs
  - polyglot_chronicle:   daily diary + challenge (temporal today)
  - polyglot_translation: cultural translation cards (cultural linguistics)
  - polyglot_bridges:     semantic problem→solution maps (conceptual translation)
  - polyglot_wire:        FFI/interop mapping (wire protocols)
  - language_archaeology: historical lineage (temporal depth)
  - language_compass:     learning journey maps (progress/milestones)
  - language_ecohub:      package ecosystem guide (tooling)

Constellation is about SPATIAL NAVIGATION — where a language sits in the
broader firmament, how close it burns to its neighbors, and what
constellation patterns emerge across the polyglot sky.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import math
import random
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field

TOOL_NAME = "polyglot-constellation"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "language_rotation.json"
)


# ── Stellar data for each language star ───────────────────────────────────────
STELLAR_DATA: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "spectral_class": "M",
        "temperature_k": 3500,
        "magnitude": 1.2,
        "luminosity": "VII",
        "description": "A red giant star — immense power, sharp edges, burns hot",
        "color": "#FF6B6B",
        "color_name": "crimson",
        "radius_solar": 1.8,
        "orbital_period_days": 365,
        "star_type": "red_giant",
        "known_for": "Fearless concurrency, zero-cost abstractions, memory safety without GC",
    },
    "Go": {
        "spectral_class": "G",
        "temperature_k": 5800,
        "magnitude": 2.8,
        "luminosity": "V",
        "description": "A yellow dwarf star — stable, warm, reliable light for all",
        "color": "#4ECDC4",
        "color_name": "teal",
        "radius_solar": 1.05,
        "orbital_period_days": 180,
        "star_type": "yellow_dwarf",
        "known_for": "Goroutines, simplicity, fast compilation, CSP concurrency",
    },
    "Swift": {
        "spectral_class": "F",
        "temperature_k": 7000,
        "magnitude": 2.1,
        "luminosity": "V",
        "description": "A white-yellow star — elegant, bright, modern",
        "color": "#FF9F43",
        "color_name": "amber",
        "radius_solar": 1.4,
        "orbital_period_days": 270,
        "star_type": "white_yellow",
        "known_for": "Protocols, value types, safety, Apple ecosystem",
    },
    "Kotlin": {
        "spectral_class": "G",
        "temperature_k": 5700,
        "magnitude": 2.4,
        "luminosity": "V",
        "description": "A yellow star with JVM heritage — interoperable, pragmatic",
        "color": "#A855F7",
        "color_name": "violet",
        "radius_solar": 1.1,
        "orbital_period_days": 200,
        "star_type": "yellow_dwarf",
        "known_for": "Coroutines, null safety, extension functions, JVM interop",
    },
    "TypeScript": {
        "spectral_class": "A",
        "temperature_k": 8500,
        "magnitude": 1.8,
        "luminosity": "V",
        "description": "A blue-white star — bright, modern, illuminating the web",
        "color": "#3B82F6",
        "color_name": "sapphire",
        "radius_solar": 2.0,
        "orbital_period_days": 220,
        "star_type": "blue_white",
        "known_for": "Static typing over JavaScript, structural types, excellent tooling",
    },
    "JavaScript": {
        "spectral_class": "O",
        "temperature_k": 35000,
        "magnitude": 1.5,
        "luminosity": "Ia",
        "description": "A blue supergiant — the most powerful star in the web galaxy",
        "color": "#FACC15",
        "color_name": "gold",
        "radius_solar": 12.0,
        "star_type": "blue_supergiant",
        "known_for": "Runs everywhere, event loop, prototype inheritance, first-class functions",
    },
    "Java": {
        "spectral_class": "G",
        "temperature_k": 5750,
        "magnitude": 2.6,
        "luminosity": "V",
        "description": "A mature yellow star — stable, massive ecosystem, enterprise backbone",
        "color": "#F97316",
        "color_name": "orange",
        "radius_solar": 1.1,
        "orbital_period_days": 365,
        "star_type": "yellow_dwarf",
        "known_for": "JVM, enterprise scale, backwards compatibility, virtual threads",
    },
    "C/C++": {
        "spectral_class": "K",
        "temperature_k": 4500,
        "magnitude": 3.0,
        "luminosity": "Ib",
        "description": "An orange supergiant — enormous, ancient, still burns bright",
        "color": "#6B7280",
        "color_name": "steel",
        "radius_solar": 8.0,
        "orbital_period_days": 400,
        "star_type": "orange_supergiant",
        "known_for": "Systems programming, manual memory, maximum control, performance",
    },
}


# ── Gravitational relationships between language stars ───────────────────────
GRAVITY_PAIRS: Dict[Tuple[str, str], Dict[str, float]] = {
    ("Rust", "Go"): {"syntax": 0.75, "paradigm": 0.50, "interop": 0.60, "learning_transfer": 0.65, "gravity_strength": 0.65},
    ("Go", "Swift"): {"syntax": 0.70, "paradigm": 0.75, "interop": 0.70, "learning_transfer": 0.72, "gravity_strength": 0.72},
    ("Swift", "Kotlin"): {"syntax": 0.90, "paradigm": 0.85, "interop": 0.80, "learning_transfer": 0.88, "gravity_strength": 0.88},
    ("Kotlin", "TypeScript"): {"syntax": 0.75, "paradigm": 0.65, "interop": 0.75, "learning_transfer": 0.72, "gravity_strength": 0.72},
    ("TypeScript", "JavaScript"): {"syntax": 0.95, "paradigm": 0.90, "interop": 0.95, "learning_transfer": 0.95, "gravity_strength": 0.95},
    ("JavaScript", "Java"): {"syntax": 0.55, "paradigm": 0.55, "interop": 0.65, "learning_transfer": 0.58, "gravity_strength": 0.58},
    ("Java", "C/C++"): {"syntax": 0.70, "paradigm": 0.60, "interop": 0.55, "learning_transfer": 0.62, "gravity_strength": 0.62},
    ("C/C++", "Rust"): {"syntax": 0.80, "paradigm": 0.70, "interop": 0.75, "learning_transfer": 0.75, "gravity_strength": 0.75},
}


# ── Constellation patterns ─────────────────────────────────────────────────────
CONSTELLATION_PATTERNS: Dict[str, Dict[str, Any]] = {
    "the_chain": {
        "name": "The Toolchain",
        "emoji": "⛓️",
        "description": "Languages ordered by compilation model: interpreted → JIT → AOT",
        "members": ["JavaScript", "Java", "C/C++", "Rust"],
        "shape": "linear",
    },
    "the_web_triangle": {
        "name": "The Web Triangle",
        "emoji": "🔺",
        "description": "The three pillars of web development",
        "members": ["JavaScript", "TypeScript", "Go"],
        "shape": "triangle",
    },
    "the_mobile_cluster": {
        "name": "The Mobile Cluster",
        "emoji": "📱",
        "description": "Native mobile development stars",
        "members": ["Swift", "Kotlin"],
        "shape": "binary",
    },
    "the_systems_duo": {
        "name": "The Systems Duo",
        "emoji": "⚙️",
        "description": "Systems programming pair",
        "members": ["Rust", "C/C++"],
        "shape": "binary",
    },
    "the_garbage_collector_cluster": {
        "name": "The GC Cluster",
        "emoji": "🗑️",
        "description": "Languages with garbage collectors",
        "members": ["Go", "Java", "JavaScript", "Kotlin"],
        "shape": "cluster",
    },
    "the_type_safe_zone": {
        "name": "The Type Safe Zone",
        "emoji": "🛡️",
        "description": "Statically typed languages",
        "members": ["Rust", "Swift", "Kotlin", "TypeScript", "Java", "C/C++"],
        "shape": "zone",
    },
}


# ── Star position in 2D sky (x, y) ────────────────────────────────────────────
STAR_POSITIONS: Dict[str, Tuple[float, float]] = {
    "Rust": (2.0, 1.0),
    "Go": (3.5, 2.0),
    "Swift": (5.0, 3.5),
    "Kotlin": (6.5, 2.5),
    "TypeScript": (8.0, 4.0),
    "JavaScript": (9.5, 3.0),
    "Java": (8.0, 1.0),
    "C/C++": (4.0, 0.0),
}


@dataclass
class Star:
    """Represents a language as a star in the constellation."""
    name: str
    spectral_class: str
    magnitude: float
    luminosity: str
    description: str
    color: str
    color_name: str
    radius_solar: float
    orbital_period_days: int
    star_type: str
    known_for: str
    x: float
    y: float

    def distance_to(self, other: "Star") -> float:
        """Calculate Euclidean distance in the constellation sky."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "spectral_class": self.spectral_class,
            "magnitude": self.magnitude,
            "luminosity": self.luminosity,
            "description": self.description,
            "color": self.color,
            "color_name": self.color_name,
            "radius_solar": self.radius_solar,
            "orbital_period_days": self.orbital_period_days,
            "star_type": self.star_type,
            "known_for": self.known_for,
            "position": {"x": self.x, "y": self.y},
        }


@dataclass
class GravitationalBond:
    """A gravitational bond between two language stars."""
    from_lang: str
    to_lang: str
    strength: float
    syntax_score: float
    paradigm_score: float
    interop_score: float
    learning_transfer: float

    def gravity_label(self) -> str:
        if self.strength >= 0.85:
            return "very strong"
        elif self.strength >= 0.70:
            return "strong"
        elif self.strength >= 0.50:
            return "moderate"
        else:
            return "distant"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from": self.from_lang,
            "to": self.to_lang,
            "strength": self.strength,
            "gravity_label": self.gravity_label(),
            "dimensions": {
                "syntax": self.syntax_score,
                "paradigm": self.paradigm_score,
                "interop": self.interop_score,
                "learning_transfer": self.learning_transfer,
            },
        }


def load_rotation() -> Dict[str, Any]:
    """Load language rotation config."""
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def get_star(language: str) -> Star:
    """Construct a Star object for a language."""
    sd = STELLAR_DATA.get(language, {})
    x, y = STAR_POSITIONS.get(language, (5.0, 5.0))
    return Star(
        name=language,
        spectral_class=sd.get("spectral_class", "G"),
        magnitude=sd.get("magnitude", 3.0),
        luminosity=sd.get("luminosity", "V"),
        description=sd.get("description", "An uncharted star"),
        color=sd.get("color", "#9CA3AF"),
        color_name=sd.get("color_name", "gray"),
        radius_solar=sd.get("radius_solar", 1.0),
        orbital_period_days=sd.get("orbital_period_days", 365),
        star_type=sd.get("star_type", "unknown"),
        known_for=sd.get("known_for", "Unknown capabilities"),
        x=x,
        y=y,
    )


def get_gravity(from_lang: str, to_lang: str) -> GravitationalBond:
    """Get gravitational bond data between two language stars."""
    pair_key = (from_lang, to_lang)
    reverse_key = (to_lang, from_lang)

    data = GRAVITY_PAIRS.get(pair_key) or GRAVITY_PAIRS.get(reverse_key)

    if data:
        return GravitationalBond(
            from_lang=from_lang,
            to_lang=to_lang,
            strength=data.get("gravity_strength", 0.5),
            syntax_score=data.get("syntax", 0.5),
            paradigm_score=data.get("paradigm", 0.5),
            interop_score=data.get("interop", 0.5),
            learning_transfer=data.get("learning_transfer", 0.5),
        )

    return GravitationalBond(
        from_lang=from_lang,
        to_lang=to_lang,
        strength=0.40,
        syntax_score=0.40,
        paradigm_score=0.40,
        interop_score=0.40,
        learning_transfer=0.40,
    )


def find_constellation_patterns(languages: List[str]) -> List[Dict[str, Any]]:
    """Find which constellation patterns include the current language."""
    found = []
    for pattern_id, pattern in CONSTELLATION_PATTERNS.items():
        if any(lang in pattern["members"] for lang in languages):
            found.append({
                "id": pattern_id,
                "name": pattern["name"],
                "emoji": pattern["emoji"],
                "description": pattern["description"],
                "members": pattern["members"],
                "shape": pattern["shape"],
                "overlap": [l for l in languages if l in pattern["members"]],
            })
    return found


def compute_stellar_distances(current_lang: str, all_languages: List[str]) -> List[Dict[str, Any]]:
    """Compute distances from current language star to all others."""
    current_star = get_star(current_lang)
    distances = []

    for lang in all_languages:
        other_star = get_star(lang)
        dist = current_star.distance_to(other_star)

        max_dist = 15.0
        normalized_dist = min(dist / max_dist, 1.0)
        proximity_score = round(1.0 - normalized_dist, 3)

        gravity = get_gravity(current_lang, lang)

        distances.append({
            "language": lang,
            "distance_ly": round(dist, 3),
            "proximity_score": proximity_score,
            "gravity": gravity.to_dict(),
        })

    distances.sort(key=lambda x: x["distance_ly"])
    return distances


def constellation(language: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate a constellation map for the selected rotation language.

    Reads the rotation config, selects the current language, maps it as a star
    in the polyglot night sky, and computes gravitational relationships with
    all other language stars.
    """
    config = load_rotation()
    languages = config["languages"]

    if language is None:
        current_idx = config.get("current_index", 0)
        language = languages[current_idx % len(languages)]

    current_star = get_star(language)

    stellar_distances = compute_stellar_distances(language, languages)

    patterns = find_constellation_patterns(languages)

    sky_map = {lang: get_star(lang).to_dict() for lang in languages}

    bonds = []
    for lang in languages:
        if lang != language:
            gravity = get_gravity(language, lang)
            bonds.append(gravity.to_dict())

    bonds.sort(key=lambda x: x["strength"], reverse=True)

    current_idx = languages.index(language) if language in languages else 0
    next_idx = (current_idx + 1) % len(languages)
    next_lang = languages[next_idx]

    strongest_bond = bonds[0] if bonds else None

    constellation_membership = []
    for pattern_id, pattern in CONSTELLATION_PATTERNS.items():
        if language in pattern["members"]:
            constellation_membership.append({
                "id": pattern_id,
                "name": pattern["name"],
                "emoji": pattern["emoji"],
            })

    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "current_star": current_star.to_dict(),
        "constellation_membership": constellation_membership,
        "stellar_distances": stellar_distances,
        "gravitational_bonds": bonds,
        "strongest_bond": strongest_bond,
        "constellation_patterns": patterns,
        "sky_map": sky_map,
        "rotation": languages,
        "next_language": next_lang,
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def run_tests() -> None:
    """Run all tests to validate the Polyglot Constellation module."""
    tests_passed = 0
    tests_failed = 0

    def assert_eq(a, b, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a == b:
            tests_passed += 1
            print("  ✅ PASS: " + msg)
        else:
            tests_failed += 1
            print("  ❌ FAIL: " + msg + " — expected " + repr(b) + ", got " + repr(a))

    def assert_in(a: str, b, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a in b:
            tests_passed += 1
            print("  ✅ PASS: " + msg)
        else:
            tests_failed += 1
            print("  ❌ FAIL: " + msg + " — '" + a + "' not found in " + repr(b))

    def assert_true(a, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a:
            tests_passed += 1
            print("  ✅ PASS: " + msg)
        else:
            tests_failed += 1
            print("  ❌ FAIL: " + msg)

    def assert_keys(d: Dict, expected_keys: List[str], msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        missing = [k for k in expected_keys if k not in d]
        if not missing:
            tests_passed += 1
            print("  ✅ PASS: " + msg)
        else:
            tests_failed += 1
            print("  ❌ FAIL: " + msg + " — missing keys: " + str(missing))

    print("Testing Polyglot Constellation...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_eq("Rust", config["languages"][0], "Rust is first language")
    assert_in("current_index", config, "current_index field present")

    print("  Testing Star construction...")
    rust = get_star("Rust")
    assert_eq("Rust", rust.name, "star name is Rust")
    assert_eq("M", rust.spectral_class, "Rust spectral class is M")
    assert_true(rust.magnitude > 0, "Rust has positive magnitude")
    assert_true(rust.radius_solar > 1.0, "Rust is larger than solar (red giant)")
    assert_eq("red_giant", rust.star_type, "Rust star type is red_giant")
    assert_true(len(rust.description) > 10, "Rust has a description")
    assert_true(len(rust.known_for) > 5, "Rust has known_for text")

    print("  Testing Star.distance_to()...")
    go = get_star("Go")
    rust_to_go = rust.distance_to(go)
    assert_true(rust_to_go > 0, "Rust and Go have non-zero distance")
    assert_true(rust_to_go < 5.0, "Rust and Go are relatively close in sky")
    assert_eq(rust_to_go, go.distance_to(rust), "distance is symmetric")

    print("  Testing GravitationalBond construction...")
    bond = get_gravity("Rust", "Go")
    assert_eq("Rust", bond.from_lang, "bond from Rust")
    assert_eq("Go", bond.to_lang, "bond to Go")
    assert_true(bond.strength > 0, "bond has strength")
    assert_true(0.0 <= bond.strength <= 1.0, "strength is in [0, 1]")
    assert_true(bond.syntax_score > 0, "bond has syntax score")
    assert_true(bond.paradigm_score > 0, "bond has paradigm score")

    print("  Testing gravity labels...")
    assert_eq("moderate", GravitationalBond("A", "B", 0.55, 0.5, 0.5, 0.5, 0.5).gravity_label(), "0.55 → moderate")
    assert_eq("strong", GravitationalBond("A", "B", 0.72, 0.5, 0.5, 0.5, 0.5).gravity_label(), "0.72 → strong")
    assert_eq("very strong", GravitationalBond("A", "B", 0.90, 0.5, 0.5, 0.5, 0.5).gravity_label(), "0.90 → very strong")
    assert_eq("distant", GravitationalBond("A", "B", 0.30, 0.5, 0.5, 0.5, 0.5).gravity_label(), "0.30 → distant")

    print("  Testing undefined pair gets default gravity...")
    unknown_bond = get_gravity("Python", "Zig")
    assert_true(unknown_bond.strength < 0.5, "undefined pair has low gravity")

    print("  Testing constellation() output structure...")
    result = constellation()
    expected_keys = [
        "tool", "version", "current_star", "constellation_membership",
        "stellar_distances", "gravitational_bonds", "strongest_bond",
        "constellation_patterns", "sky_map", "rotation", "next_language", "timestamp"
    ]
    assert_keys(result, expected_keys, "All expected keys present in constellation() output")

    print("  Testing current_star structure...")
    star = result["current_star"]
    assert_keys(star, [
        "name", "spectral_class", "magnitude", "luminosity", "description",
        "color", "color_name", "radius_solar", "orbital_period_days",
        "star_type", "known_for", "position"
    ], "current_star has all required fields")
    assert_in("x", star["position"], "current_star has x position")
    assert_in("y", star["position"], "current_star has y position")
    assert_true(isinstance(star["position"]["x"], (int, float)), "position x is numeric")
    assert_true(isinstance(star["position"]["y"], (int, float)), "position y is numeric")

    print("  Testing stellar_distances structure...")
    distances = result["stellar_distances"]
    assert_true(len(distances) == 8, "8 stellar distances (all languages)")
    for d in distances:
        assert_keys(d, ["language", "distance_ly", "proximity_score", "gravity"], "distance entry has required fields for " + d["language"])
        assert_true(0.0 <= d["proximity_score"] <= 1.0, d["language"] + " proximity is in [0,1]")
        assert_true(d["distance_ly"] >= 0, d["language"] + " distance is non-negative")
    for i in range(len(distances) - 1):
        assert_true(distances[i]["distance_ly"] <= distances[i + 1]["distance_ly"], "distances sorted ascending")

    print("  Testing gravitational_bonds structure...")
    bonds = result["gravitational_bonds"]
    assert_true(len(bonds) == 7, "7 bonds (all languages except current)")
    for bond in bonds:
        assert_keys(bond, ["from", "to", "strength", "gravity_label", "dimensions"], "bond has required fields")
        assert_true("syntax" in bond["dimensions"], "bond has syntax dimension")
        assert_true("paradigm" in bond["dimensions"], "bond has paradigm dimension")
    for i in range(len(bonds) - 1):
        assert_true(bonds[i]["strength"] >= bonds[i + 1]["strength"], "bonds sorted by strength descending")

    print("  Testing strongest_bond...")
    strongest = result["strongest_bond"]
    assert_true(strongest is not None, "strongest_bond is not None")
    assert_true(strongest["strength"] >= bonds[0]["strength"], "strongest is the first in sorted list")

    print("  Testing sky_map has all 8 stars...")
    sky = result["sky_map"]
    for lang in config["languages"]:
        assert_true(lang in sky, lang + " is in sky_map")
        assert_keys(sky[lang], ["name", "spectral_class", "magnitude", "position"], lang + " has required sky_map fields")

    print("  Testing constellation_membership...")
    membership = result["constellation_membership"]
    assert_true(isinstance(membership, list), "constellation_membership is a list")
    current_lang = result["current_star"]["name"]
    found_any = False
    for m in membership:
        if current_lang in CONSTELLATION_PATTERNS.get(m["id"], {}).get("members", []):
            found_any = True
    assert_true(found_any, current_lang + " is in at least one constellation pattern")

    print("  Testing constellation_patterns...")
    patterns = result["constellation_patterns"]
    assert_true(isinstance(patterns, list), "patterns is a list")
    assert_true(len(patterns) > 0, "at least one pattern found")
    for p in patterns:
        assert_keys(p, ["id", "name", "emoji", "description", "members", "shape", "overlap"], "pattern has all fields")

    print("  Testing rotation advances after constellation()...")
    idx_before = load_rotation()["current_index"]
    lang_before = load_rotation()["languages"][idx_before]
    result = constellation()
    idx_after = load_rotation()["current_index"]
    assert_eq((idx_before + 1) % 8, idx_after, "index advanced by 1")
    assert_eq(lang_before, load_rotation()["last_language"], "last_language recorded correctly")

    print("  Testing constellation() with language override...")
    result = constellation(language="Rust")
    assert_eq("Rust", result["current_star"]["name"], "override sets correct language")
    assert_eq("Rust", load_rotation()["last_language"], "override language is saved as last_language")

    print("  Testing next_language is in the rotation list...")
    assert_true(result["next_language"] in result["rotation"], "next_language is in rotation list")
    assert_true(result["next_language"] != result["current_star"]["name"], "next != current (rotation working)")

    print("  Testing stellar distances are correct for Rust → Go...")
    result = constellation(language="Rust")
    rust_distances = {d["language"]: d for d in result["stellar_distances"]}
    assert_true("Go" in rust_distances, "Go is in Rust distances")
    go_dist = rust_distances["Go"]["distance_ly"]
    assert_true(go_dist > 0, "Rust → Go has non-zero distance")

    print("  Testing spectral classes are correct...")
    for lang in config["languages"]:
        result = constellation(language=lang)
        star_data = result["current_star"]
        expected_class = STELLAR_DATA.get(lang, {}).get("spectral_class")
        assert_eq(expected_class, star_data["spectral_class"], lang + " spectral class matches")

    print("  Testing colors are valid hex...")
    for lang in config["languages"]:
        result = constellation(language=lang)
        color = result["current_star"]["color"]
        assert_true(color.startswith("#"), lang + " color starts with #")
        assert_eq(7, len(color), lang + " color is 7 chars (#RRGGBB)")

    print("  Testing tool name and version...")
    assert_eq("polyglot-constellation", result["tool"], "correct tool name")
    assert_eq("1.0.0", result["version"], "correct tool version")

    print("  Testing Star.to_dict() produces valid dict...")
    rust_star = get_star("Rust")
    d = rust_star.to_dict()
    assert_keys(d, ["name", "spectral_class", "magnitude", "description", "position"], "Star.to_dict() has required fields")

    print("  Testing GravitationalBond.to_dict() produces valid dict...")
    bond = get_gravity("Swift", "Kotlin")
    bd = bond.to_dict()
    assert_keys(bd, ["from", "to", "strength", "gravity_label", "dimensions"], "Bond.to_dict() has required fields")

    print("  Testing known gravitational pairs...")
    swift_kotlin = get_gravity("Swift", "Kotlin")
    assert_true(swift_kotlin.strength > 0.80, "Swift↔Kotlin has strong gravity (0.88)")
    ts_js = get_gravity("TypeScript", "JavaScript")
    assert_true(ts_js.strength > 0.90, "TS↔JS has very strong gravity (0.95)")

    print("  Testing constellation patterns are not empty...")
    assert_true(len(CONSTELLATION_PATTERNS) > 0, "CONSTELLATION_PATTERNS is not empty")
    for pid, pdata in CONSTELLATION_PATTERNS.items():
        assert_keys(pdata, ["name", "emoji", "description", "members", "shape"], "pattern " + pid + " has required fields")
        assert_true(len(pdata["members"]) >= 2, "pattern " + pid + " has >= 2 members")

    print("  Testing all stellar data is defined for all 8 languages...")
    for lang in config["languages"]:
        assert_true(lang in STELLAR_DATA, lang + " in STELLAR_DATA")
        sd = STELLAR_DATA[lang]
        required_keys = ["spectral_class", "temperature_k", "magnitude", "luminosity", "description", "color", "color_name", "radius_solar", "star_type", "known_for"]
        for key in required_keys:
            assert_true(key in sd, lang + " has " + key + " in STELLAR_DATA")

    print("  Testing STAR_POSITIONS are defined for all languages...")
    for lang in config["languages"]:
        assert_true(lang in STAR_POSITIONS, lang + " in STAR_POSITIONS")
        pos = STAR_POSITIONS[lang]
        assert_eq(2, len(pos), lang + " position is (x, y)")

    print("  Testing distance calculation symmetry...")
    for lang1 in config["languages"]:
        for lang2 in config["languages"]:
            if lang1 != lang2:
                star1 = get_star(lang1)
                star2 = get_star(lang2)
                d12 = star1.distance_to(star2)
                d21 = star2.distance_to(star1)
                assert_eq(d12, d21, "distance " + lang1 + "↔" + lang2 + " is symmetric")

    print("")
    print("=" * 55)
    print("Tests: " + str(tests_passed) + " passed, " + str(tests_failed) + " failed")
    if tests_failed == 0:
        print("🌌 All Constellation tests passed! The sky is mapped.")
    else:
        print("💥 " + str(tests_failed) + " test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--constellation":
        result = constellation()
        print(json.dumps(result, indent=2))
    else:
        print("Polyglot Constellation v" + TOOL_VERSION)
        print("Usage:")
        print("  python -m polyglot_constellation --test           # Run tests")
        print("  python -m polyglot_constellation --constellation # Generate constellation map")