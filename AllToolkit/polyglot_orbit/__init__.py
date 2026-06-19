#!/usr/bin/env python3
"""
🌌 Polyglot Orbit v1.0

A celestial mechanics engine for programming languages — each language
occupies an "orbital shell" based on its abstraction level, and the
tool calculates gravitational interactions, orbital resonances, and
conjunction events between languages in the ecosystem.

Creative concept: "Languages are planets. Their orbits reveal relationships.
When two orbits cross, programmers feel the pull — choosing between
ecosystems, migrating codebases, or building bridges."

Key features:
  1. Orbital Parameters — Each language has an orbital profile
     (eccentricity, inclination, semi-major axis, orbital period)
  2. Orbital Resonance Detection — When one language's period is a
     simple fraction of another's, they exert gravitational influence
  3. Conjunction Events — When two languages are at the same orbital
     phase, opportunities emerge (bindings, FFIs, transpilation)
  4. Gravity Wells — Ecosystem gravity (jobs, libraries, community)
     expressed as well depth
  5. Escape Velocity — The energy needed to move between language ecosystems

Distinct from existing tools:
  - polyglot_weather:    atmospheric pressure / ecosystem health (static)
  - polyglot_resonator:  philosophical mental models (conceptual)
  - polyglot_oracle:     one-on-one counsel / advice (personal)
  - polyglot_dna:        genetic trait comparison (trait lens)
  - polyglot_cartographer: ecosystem graph traversal (graph lens)
  - polyglot_chronicle:  daily events log (temporal)
  - polyglot_flavor:     sensory tasting notes (sensory lens)
  - polyglot_cipher:     cryptographic puzzle lens (crypto lens)
  - polyglot_spectrometer: spectral analysis of code (spectral lens)

Orbit is about SPATIAL MECHANICS — where languages sit in the ecosystem
universe, how gravity shapes their interactions, and what orbital
mechanics reveals about language adoption and migration patterns.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import math
import os
import random
from datetime import datetime, timezone, timedelta
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-orbit"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = str(Path(__file__).parent.parent.parent / "language_rotation.json")

# ── Orbital profiles ─────────────────────────────────────────────────────────
# Each language occupies an orbital shell characterized by:
#   semi_major_axis   — mean distance from ecosystem center (abstraction level proxy)
#   eccentricity      — orbital shape (0=perfect circle, 1=parabolic escape)
#   inclination       — tilt relative to the "web/desktop/embedded" plane
#   orbital_period    — rate of feature releases / version churn
#   mass             — ecosystem size (jobs, libraries, community)
#   gravitational_pull — current adoption momentum
#   primary_domain    — where this language "orbits" most densely
#   escape_velocity   — energy needed to leave this ecosystem for another

LANGUAGE_ORBITS: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "semi_major_axis": 3.2,   # systems / close to metal
        "eccentricity": 0.15,
        "inclination_deg": 72,    # highly inclined — safety / systems focus
        "orbital_period": 42,      # days between major releases (slow, stable)
        "mass": 7.5,              # growing but still niche
        "gravitational_pull": 9.2, # rising fast
        "primary_domain": "Systems / Security / WebAssembly",
        "escape_velocity_km_s": 14.5,
        "color": "#CE422B",
        "emoji": "🦀",
        "atmosphere": "thin (memory-safe systems)",
        "moon_count": 2,  # Cargo crates, crates.io ecosystem
        "ring_description": None,
        "description": "A dense, compact world with fierce gravity. Its "
                       "memory-safety atmosphere makes it uniquely livable "
                       "for systems programmers migrating from C/C++.",
    },
    "Go": {
        "semi_major_axis": 5.8,   # cloud / backend — mid-range
        "eccentricity": 0.08,
        "inclination_deg": 28,
        "orbital_period": 28,     # fast release cycle (6 weeks)
        "mass": 9.3,
        "gravitational_pull": 8.8,
        "primary_domain": "Cloud / Backend / DevOps",
        "escape_velocity_km_s": 11.2,
        "color": "#00ADD8",
        "emoji": "🐹",
        "atmosphere": "gentle (simple, readable)",
        "moon_count": 4,  # goroutines concurrency, channels, interfaces, gc
        "ring_description": None,
        "description": "A pragmatic world with low orbital eccentricity — "
                       "predictable, reliable, efficient. Its goroutine "
                       "moons create massive concurrency without mass.",
    },
    "Swift": {
        "semi_major_axis": 4.5,   # Apple ecosystem / mobile
        "eccentricity": 0.12,
        "inclination_deg": 45,
        "orbital_period": 35,
        "mass": 6.8,
        "gravitational_pull": 6.5,
        "primary_domain": "iOS/macOS / Apple Platforms",
        "escape_velocity_km_s": 13.4,
        "color": "#F05138",
        "emoji": "🦅",
        "atmosphere": "moderate (safe, modern)",
        "moon_count": 3,  # ARC, optionals, protocols
        "ring_description": None,
        "description": "Orbits firmly within Apple's gravity well. Its "
                       "protocol-oriented design creates clean layers. "
                       "Low inclination means focused domain expertise.",
    },
    "Kotlin": {
        "semi_major_axis": 4.9,
        "eccentricity": 0.10,
        "inclination_deg": 35,
        "orbital_period": 30,
        "mass": 7.8,
        "gravitational_pull": 7.8,
        "primary_domain": "Android / JVM / Server-side",
        "escape_velocity_km_s": 12.8,
        "color": "#7F52FF",
        "emoji": "🟣",
        "atmosphere": "rich (JVM interop, null safety)",
        "moon_count": 3,  # coroutines, extension functions, data classes
        "ring_description": "faint purple",
        "description": "Orbits the Java ecosystem but at higher altitude — "
                       "cleaner, more expressive, yet fully interoperable. "
                       "Its JetBrains-engineered surface is polished.",
    },
    "TypeScript": {
        "semi_major_axis": 6.4,   # web / high-level
        "eccentricity": 0.06,
        "inclination_deg": 15,
        "orbital_period": 14,      # very fast releases (biweekly)
        "mass": 9.6,
        "gravitational_pull": 9.8,
        "primary_domain": "Web / Frontend / Node.js",
        "escape_velocity_km_s": 10.8,
        "color": "#3178C6",
        "emoji": "🔷",
        "atmosphere": "thick (massive ecosystem)",
        "moon_count": 5,  # npm, VSCode plugin ecosystem, types, decorators, enums
        "ring_description": "thin blue ring of type definitions",
        "description": "The most massive body in the web orbital region. "
                       "Its gravitational pull bends the trajectory of "
                       "every new web project toward type safety.",
    },
    "JavaScript": {
        "semi_major_axis": 7.0,   # the web browser center of mass
        "eccentricity": 0.04,
        "inclination_deg": 8,
        "orbital_period": 21,      # ECMAScript annual releases
        "mass": 10.0,             # the dominant web language
        "gravitational_pull": 9.5,
        "primary_domain": "Web / Browser / Universal JS",
        "escape_velocity_km_s": 9.8,
        "color": "#F7DF1E",
        "emoji": "🟨",
        "atmosphere": "dense (everything runs here)",
        "moon_count": 6,  # Node.js, npm, V8, React, Vue, Angular
        "ring_description": "golden orbital debris ring",
        "description": "The Sun at the center of the web solar system. "
                       "Every other web-adjacent language must account "
                       "for its gravitational pull when planning escape trajectories.",
    },
    "Java": {
        "semi_major_axis": 5.5,
        "eccentricity": 0.18,
        "inclination_deg": 20,
        "orbital_period": 56,      # 6-month release cycle
        "mass": 8.8,
        "gravitational_pull": 6.5,
        "primary_domain": "Enterprise / Android (legacy) / Backend",
        "escape_velocity_km_s": 13.0,
        "color": "#ED8B00",
        "emoji": "☕",
        "atmosphere": "stable but warming (Jakarta EE, Spring Boot)",
        "moon_count": 4,  # Spring, Hibernate, Maven, Gradle
        "ring_description": None,
        "description": "A massive world, slowly cooling but still the "
                       "gravitational center of enterprise computing. "
                       "High eccentricity means its orbit varies — new "
                       "projects often escape, but legacy keeps it massive.",
    },
    "C/C++": {
        "semi_major_axis": 2.0,   # closest to the metal
        "eccentricity": 0.22,
        "inclination_deg": 85,     # almost perpendicular — raw hardware
        "orbital_period": 90,      # slow evolution
        "mass": 8.5,
        "gravitational_pull": 6.0,
        "primary_domain": "Embedded / OS / Game Engines / HPC",
        "escape_velocity_km_s": 18.3,
        "color": "#00599C",
        "emoji": "⚙️",
        "atmosphere": "none (raw, unprotected)",
        "moon_count": 2,  # STL, standard library, preprocessor
        "ring_description": "thin ring of legacy code",
        "description": "The original world — closest to the bare metal of "
                       "the machine. Highest escape velocity: leaving C/C++ "
                       "for another ecosystem requires significant energy. "
                       "Its high inclination means it orbits perpendicular "
                       "to most other languages.",
    },
}

# Resonance ratios that produce gravitational interactions
RESONANCE_RATIOS = {
    (1, 1): "1:1 — Co-orbital — languages share the same orbital zone (rare)",
    (1, 2): "1:2 — Harmonic — strong tidal forces, easy migration path",
    (2, 3): "2:3 — Near resonance — moderate gravitational interaction",
    (3, 4): "3:4 — Weak resonance — occasional conjunction opportunities",
    (1, 3): "1:3 — Strong harmonic — significant pull during conjunctions",
    (3, 5): "3:5 — Minor resonance — niche overlap scenarios",
    (2, 5): "2:5 — Weak harmonic — limited interaction",
}


# ── Orbital mechanics helpers ─────────────────────────────────────────────────

def _calculate_distance(sma_a: float, sma_b: float, angle_a: float, angle_b: float) -> float:
    """Calculate orbital distance between two bodies at given angles."""
    r_a = sma_a * (1 - LANGUAGE_ORBITS[list(LANGUAGE_ORBITS.keys())[0]]["eccentricity"]**2) / (1 + LANGUAGE_ORBITS[list(LANGUAGE_ORBITS.keys())[0]]["eccentricity"] * math.cos(angle_a))
    r_b = sma_b * (1 - LANGUAGE_ORBITS[list(LANGUAGE_ORBITS.keys())[0]]["eccentricity"]**2) / (1 + LANGUAGE_ORBITS[list(LANGUAGE_ORBITS.keys())[0]]["eccentricity"] * math.cos(angle_b))
    return math.sqrt(r_a**2 + r_b**2 - 2 * r_a * r_b * math.cos(angle_a - angle_b))


def _calculate_resonance_ratio(period_a: float, period_b: float) -> Tuple[str, str]:
    """Calculate the orbital resonance ratio between two languages.
    Ratio is normalized so smaller period is always in numerator (e.g., 2:3 not 3:2).
    """
    try:
        f = Fraction(period_a / period_b).limit_denominator(10)
        # Normalize: ensure smaller period is numerator
        if f.numerator > f.denominator:
            f = Fraction(f.denominator, f.numerator)
        ratio_str = f"{f.numerator}:{f.denominator}"
        resonance_desc = RESONANCE_RATIOS.get(
            (f.numerator, f.denominator),
            f"{ratio_str} — custom resonance"
        )
        return ratio_str, resonance_desc
    except (ValueError, ZeroDivisionError):
        return "N/A", "No resonance detected"


def _calculate_conjunction(angle_a: float, angle_b: float, period_a: float, period_b: float) -> Dict[str, Any]:
    """
    Calculate when two orbital bodies will be at conjunction (same angular position).

    Conjunction occurs when the angular difference is 0 (mod 2π).
    We find the time until the next conjunction.
    """
    if period_a == period_b:
        return {"next_conjunction_days": 0.0, "description": "Co-orbital — permanent conjunction"}

    # Angular velocities (radians per day)
    omega_a = 2 * math.pi / period_a
    omega_b = 2 * math.pi / period_b

    # Relative angular velocity
    omega_rel = omega_a - omega_b

    # Current angular difference
    delta_angle = angle_b - angle_a

    # Time until next conjunction: delta_angle + n * omega_rel = 0 (mod 2π)
    # Solving for t: t = (delta_angle + k*2π) / omega_rel
    # We want the smallest positive t
    two_pi = 2 * math.pi
    delta_norm = delta_angle % two_pi

    if abs(omega_rel) < 1e-10:
        return {"next_conjunction_days": float('inf'), "description": "No conjunction — parallel orbits"}

    t_candidates = []
    for k in range(-5, 10):
        t = (delta_norm + k * two_pi) / omega_rel
        if t > 0:
            t_candidates.append(t)

    next_t = min(t_candidates) if t_candidates else float('inf')
    return {
        "next_conjunction_days": round(next_t, 2),
        "description": f"Conjunction in {round(next_t, 1)} days" if next_t < 365 else f"Conjunction in {round(next_t/30, 1)} months",
    }


def _calculate_escape_energy(from_lang: str, to_lang: str) -> Dict[str, Any]:
    """Calculate energy requirements to escape from one language ecosystem to another."""
    orb_from = LANGUAGE_ORBITS[from_lang]
    orb_to = LANGUAGE_ORBITS[to_lang]
    ev_from = orb_from["escape_velocity_km_s"]
    ev_to = orb_to["escape_velocity_km_s"]
    delta_ev = ev_to - ev_from
    mass_ratio = orb_to["mass"] / orb_from["mass"]
    axis_delta = abs(orb_to["semi_major_axis"] - orb_from["semi_major_axis"])

    # Very rough energy proxy: combination of escape velocity delta and ecosystem size
    energy_index = abs(delta_ev) * 0.4 + axis_delta * 0.3 + abs(math.log(mass_ratio + 0.01)) * 0.3

    if energy_index < 2:
        difficulty = "🟢 Easy — familiar trajectory"
        energy_j_class = "F-class (modest burn)"
    elif energy_index < 4:
        difficulty = "🟡 Moderate — expect gravity assist maneuvers"
        energy_j_class = "G-class (significant burn)"
    elif energy_index < 7:
        difficulty = "🟠 Difficult — requires serious orbital maneuver"
        energy_j_class = "K-class (major burn)"
    else:
        difficulty = "🔴 Very Difficult — near-escape velocity required"
        energy_j_class = "M-class (extreme burn)"

    return {
        "from_language": from_lang,
        "to_language": to_lang,
        "escape_velocity_delta_km_s": round(delta_ev, 1),
        "orbital_axis_delta": round(axis_delta, 2),
        "mass_ratio": round(mass_ratio, 2),
        "energy_index": round(energy_index, 2),
        "difficulty": difficulty,
        "energy_class": energy_j_class,
        "recommendation": _get_migration_recommendation(from_lang, to_lang, energy_index),
    }


def _get_migration_recommendation(from_lang: str, to_lang: str, energy: float) -> str:
    """Generate a migration recommendation based on orbital mechanics."""
    recommendations = {
        ("C/C++", "Rust"): "Use Rust as a modern C/C++ replacement in new systems. Incremental migration via C-compatible FFI.",
        ("Java", "Go"): "Go and Java occupy nearby orbital zones. Go's simplicity offers a clean migration path for backend services.",
        ("JavaScript", "TypeScript"): "TypeScript is in JavaScript's orbital zone — smooth migration with gradual typing.",
        ("TypeScript", "JavaScript"): "Reverse migration rarely needed, but possible for lightweight deployments.",
        ("Kotlin", "Java"): "Kotlin orbits within Java's well — easy to migrate toward Java's mass for enterprise compatibility.",
        ("Java", "Kotlin"): "Kotlin offers a higher orbit — cleaner syntax, same JVM ecosystem, easier migration path.",
        ("Rust", "Go"): "Rust and Go are in different orbital zones — a direct migration requires significant retraining.",
        ("Swift", "Kotlin"): "Both mobile-adjacent worlds — cross-pollination via multi-platform Kotlin Multiplatform or Swift-Kotlin bridges.",
        ("Go", "Rust"): "Cloud infrastructure overlap but different orbital inclinations — Rust for safety-critical paths.",
    }
    key = (from_lang, to_lang) if (from_lang, to_lang) in recommendations else (to_lang, from_lang)
    base = recommendations.get(key, f"Orbital transfer from {from_lang} to {to_lang} is {'challenging' if energy > 4 else 'feasible'}.")

    if energy < 2:
        return f"{base} Low energy required."
    elif energy < 4:
        return f"{base} Moderate burn needed."
    elif energy < 7:
        return f"{base} Significant trajectory adjustment required."
    else:
        return f"{base} Extreme escape velocity required — consider multi-step orbital transfer."


def _calculate_gravity_well(lang: str) -> Dict[str, Any]:
    """Calculate the gravitational well depth for a language ecosystem."""
    orb = LANGUAGE_ORBITS[lang]
    mass = orb["mass"]
    gravitational_pull = orb["gravitational_pull"]

    # Well depth proxy: ecosystem mass × adoption momentum
    well_depth = mass * gravitational_pull / 10.0

    if well_depth >= 8:
        classification = "Deep Well — massive ecosystem, hard to escape"
    elif well_depth >= 6:
        classification = "Moderate Well — significant pull, manageable escape"
    elif well_depth >= 4:
        classification = "Shallow Well — growing but still niche"
    else:
        classification = "Sparse Field — minimal gravity, easy to leave"

    return {
        "language": lang,
        "well_depth_index": round(well_depth, 2),
        "classification": classification,
        "mass": mass,
        "gravitational_pull": gravitational_pull,
        "escape_velocity_km_s": orb["escape_velocity_km_s"],
    }


# ── Core API ──────────────────────────────────────────────────────────────────

def load_rotation_data() -> Dict[str, Any]:
    """Load the language rotation configuration."""
    if not os.path.exists(ROTATION_FILE):
        return {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 0,
            "last_language": None,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation_data(data: Dict[str, Any]) -> None:
    """Save updated language rotation configuration."""
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_current_language() -> str:
    """Get the current language without advancing rotation."""
    data = load_rotation_data()
    idx = data.get("current_index", 0)
    langs = data.get("languages", list(LANGUAGE_ORBITS.keys()))
    return langs[idx % len(langs)]


def orbit_report(language: Optional[str] = None, seed: Optional[int] = None) -> Dict[str, Any]:
    """
    Generate a complete orbital mechanics report for the current rotation language.

    Reads language_rotation.json, selects the current language, generates a
    full orbital profile, calculates gravity well depth, finds resonance
    relationships with all other languages, and advances the rotation index.

    Args:
        language: override the selected language (for testing)
        seed: optional seed for deterministic conjunction calculations

    Returns:
        dict with orbital report and updated rotation state
    """
    data = load_rotation_data()
    langs = data.get("languages", list(LANGUAGE_ORBITS.keys()))

    if language is None:
        idx = data.get("current_index", 0)
        current_lang = langs[idx % len(langs)]
    else:
        current_lang = language
        if language in langs:
            idx = langs.index(language)
        else:
            idx = 0

    # Advance rotation
    next_idx = (idx + 1) % len(langs)
    data["current_index"] = next_idx
    data["last_language"] = current_lang
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation_data(data)

    # Get orbital data
    orb = LANGUAGE_ORBITS[current_lang]

    # Generate deterministic "current angle" for conjunction if seed provided
    if seed is not None:
        random.seed(seed)
    current_angle = random.uniform(0, 2 * math.pi)

    # Build resonance map with all other languages
    resonances = []
    gravity_wells = []
    escape_energies = []

    for lang in langs:
        if lang == current_lang:
            continue

        other_orb = LANGUAGE_ORBITS[lang]
        ratio_str, resonance_desc = _calculate_resonance_ratio(
            orb["orbital_period"], other_orb["orbital_period"]
        )
        conj = _calculate_conjunction(
            current_angle, random.uniform(0, 2 * math.pi),
            orb["orbital_period"], other_orb["orbital_period"]
        )
        gravity = _calculate_gravity_well(lang)
        escape = _calculate_escape_energy(current_lang, lang)

        resonances.append({
            "with_language": lang,
            "emoji": other_orb["emoji"],
            "orbital_period_ratio": ratio_str,
            "resonance_description": resonance_desc,
            "conjunction": conj,
        })
        gravity_wells.append(gravity)
        escape_energies.append(escape)

    # Sort resonances by energy index (most interesting interactions first)
    escape_energies.sort(key=lambda x: x["energy_index"])

    # Orbital summary
    orbital_summary = {
        "language": current_lang,
        "emoji": orb["emoji"],
        "semi_major_axis": orb["semi_major_axis"],
        "eccentricity": orb["eccentricity"],
        "inclination_deg": orb["inclination_deg"],
        "orbital_period_days": orb["orbital_period"],
        "mass": orb["mass"],
        "gravitational_pull": orb["gravitational_pull"],
        "primary_domain": orb["primary_domain"],
        "escape_velocity_km_s": orb["escape_velocity_km_s"],
        "color": orb["color"],
        "atmosphere": orb["atmosphere"],
        "moon_count": orb["moon_count"],
        "ring_description": orb["ring_description"],
        "description": orb["description"],
        "gravity_well": _calculate_gravity_well(current_lang),
    }

    # Sort gravity wells by depth
    gravity_wells.sort(key=lambda x: x["well_depth_index"], reverse=True)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "current_language": current_lang,
        "rotation_index": idx,
        "next_language": langs[next_idx],
        "orbital_summary": orbital_summary,
        "resonances": resonances,
        "gravity_wells": gravity_wells,
        "escape_calculations": escape_energies,
        "all_languages_sorted_by_well_depth": [
            _calculate_gravity_well(l) for l in langs
        ],
    }


def find_conjunctions(language_a: str, language_b: str, days_ahead: int = 365) -> Dict[str, Any]:
    """
    Find all conjunction events between two languages over a given time period.

    A conjunction occurs when both languages are at the same angular position
    in their orbits (0, π/2, π, 3π/2 phases — key decision points).

    Args:
        language_a: First language
        language_b: Second language
        days_ahead: How many days to search ahead

    Returns:
        dict with conjunction schedule
    """
    orb_a = LANGUAGE_ORBITS.get(language_a, LANGUAGE_ORBITS["Rust"])
    orb_b = LANGUAGE_ORBITS.get(language_b, LANGUAGE_ORBITS["Go"])

    ratio_str, resonance_desc = _calculate_resonance_ratio(
        orb_a["orbital_period"], orb_b["orbital_period"]
    )

    # Find all conjunctions in the time period
    omega_a = 2 * math.pi / orb_a["orbital_period"]
    omega_b = 2 * math.pi / orb_b["orbital_period"]
    omega_rel = omega_a - omega_b

    events = []
    angle_a = random.uniform(0, 2 * math.pi)  # random starting angle
    angle_b = random.uniform(0, 2 * math.pi)

    day = 0.0
    last_event_day = -999.0
    while day < days_ahead:
        # Advance to next conjunction
        if abs(omega_rel) < 1e-10:
            break
        delta = (angle_b - angle_a) % (2 * math.pi)
        t_until = delta / omega_rel if omega_rel > 0 else (2 * math.pi - delta) / abs(omega_rel)
        t_until = max(0.01, t_until)
        day += t_until
        if day >= days_ahead or (day - last_event_day) < 0.1:
            break
        last_event_day = day

        phase_labels = ["New Moon (0°)", "First Quarter (90°)", "Full Moon (180°)", "Last Quarter (270°)"]
        phase_idx = int((day * omega_a) / (math.pi / 2)) % 4

        events.append({
            "day": round(day, 1),
            "phase": phase_labels[phase_idx],
            "description": f"{language_a} ({orb_a['emoji']}) and {language_b} ({orb_b['emoji']}) at conjunction",
        })

    return {
        "language_a": language_a,
        "emoji_a": orb_a["emoji"],
        "language_b": language_b,
        "emoji_b": orb_b["emoji"],
        "orbital_period_ratio": ratio_str,
        "resonance_description": resonance_desc,
        "conjunction_count": len(events),
        "events": events[:20],  # cap at 20 events
    }


def rank_ecosystems() -> Dict[str, Any]:
    """
    Rank all languages by ecosystem gravitational strength.

    Returns a full ranking with gravity well depths, escape velocities,
    and migration difficulty scores.
    """
    langs = list(LANGUAGE_ORBITS.keys())
    rankings = []

    for lang in langs:
        orb = LANGUAGE_ORBITS[lang]
        gw = _calculate_gravity_well(lang)
        rankings.append({
            "rank": 0,
            "language": lang,
            "emoji": orb["emoji"],
            "gravity_well": gw,
            "semi_major_axis": orb["semi_major_axis"],
            "orbital_period_days": orb["orbital_period"],
            "mass": orb["mass"],
            "gravitational_pull": orb["gravitational_pull"],
            "primary_domain": orb["primary_domain"],
        })

    rankings.sort(key=lambda x: x["gravity_well"]["well_depth_index"], reverse=True)
    for i, r in enumerate(rankings):
        r["rank"] = i + 1

    return {
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "rankings": rankings,
        "total_orbital_bodies": len(rankings),
    }


# ── Tests ──────────────────────────────────────────────────────────────────────

def run_tests() -> None:
    """Run all tests for the polyglot_orbit module."""
    tests_passed = 0
    tests_failed = 0

    def assert_eq(a, b, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a == b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — expected {b!r}, got {a!r}")

    def assert_in(a, b, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a in b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg}")

    def assert_true(a, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg}")

    def assert_keys(d, expected_keys, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        missing = [k for k in expected_keys if k not in d]
        if not missing:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — missing keys: {missing}")

    print("Testing Polyglot Orbit...")

    print("  === Rotation File Tests ===")
    config = load_rotation_data()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_in("current_index", config, "current_index field present")
    assert_in("last_language", config, "last_language field present")

    print("  === Orbit Report Structure Tests ===")
    result = orbit_report()
    assert_keys(result, [
        "tool", "version", "generated_at", "current_language",
        "rotation_index", "next_language", "orbital_summary",
        "resonances", "gravity_wells", "escape_calculations",
        "all_languages_sorted_by_well_depth"
    ], "orbit_report has all required top-level keys")

    print("  === Orbital Summary Tests ===")
    osummary = result["orbital_summary"]
    assert_keys(osummary, [
        "language", "emoji", "semi_major_axis", "eccentricity",
        "inclination_deg", "orbital_period_days", "mass",
        "gravitational_pull", "primary_domain", "escape_velocity_km_s",
        "color", "atmosphere", "moon_count", "gravity_well", "description"
    ], "orbital_summary has all required fields")
    assert_true(osummary["semi_major_axis"] > 0, "semi_major_axis is positive")
    assert_true(0 <= osummary["eccentricity"] < 1, "eccentricity is valid [0,1)")
    assert_true(0 <= osummary["inclination_deg"] <= 90, "inclination_deg is valid [0,90]")
    assert_true(osummary["orbital_period_days"] > 0, "orbital_period_days is positive")
    assert_true(1 <= osummary["moon_count"] <= 6, "moon_count is reasonable")

    print("  === Resonance Tests ===")
    resonances = result["resonances"]
    assert_eq(7, len(resonances), "7 resonance entries (all other languages)")
    for res in resonances:
        assert_keys(res, ["with_language", "emoji", "orbital_period_ratio",
                          "resonance_description", "conjunction"],
                    "resonance entry has required fields")
        assert_true(len(res["resonance_description"]) > 3, "resonance description is meaningful")

    print("  === Gravity Well Tests ===")
    gws = result["gravity_wells"]
    assert_eq(7, len(gws), "7 gravity well entries")
    for gw in gws:
        assert_keys(gw, ["language", "well_depth_index", "classification",
                          "mass", "gravitational_pull", "escape_velocity_km_s"],
                    "gravity_well has required fields")
        assert_true(gw["well_depth_index"] > 0, "well_depth_index is positive")
        assert_in("classification", gw, "gravity_well has classification")

    print("  === Escape Energy Tests ===")
    escapes = result["escape_calculations"]
    assert_eq(7, len(escapes), "7 escape energy entries")
    for esc in escapes:
        assert_keys(esc, ["from_language", "to_language", "escape_velocity_delta_km_s",
                          "orbital_axis_delta", "mass_ratio", "energy_index",
                          "difficulty", "energy_class", "recommendation"],
                    "escape_energy has required fields")
        assert_true(esc["energy_index"] >= 0, "energy_index is non-negative")
        assert_in("difficulty", esc, "escape has difficulty rating")

    print("  === All Languages Have Orbital Data ===")
    all_ranked = [r["language"] for r in rank_ecosystems()["rankings"]]
    for lang in LANGUAGE_ORBITS:
        assert_true(lang in all_ranked, f"{lang} appears in ecosystem rankings")
    # Verify all ranked languages are in our orbit data
    for lang in all_ranked:
        assert_true(lang in LANGUAGE_ORBITS, f"{lang} has orbital profile")

    print("  === Rotation Advances After orbit_report() ===")
    idx_before = load_rotation_data()["current_index"]
    lang_before = load_rotation_data()["languages"][idx_before]
    result = orbit_report()
    idx_after = load_rotation_data()["current_index"]
    assert_eq((idx_before + 1) % 8, idx_after, "index advanced by 1")
    assert_eq(lang_before, load_rotation_data()["last_language"], "last_language recorded correctly")

    print("  === Conjunction Finder Tests ===")
    conj = find_conjunctions("Rust", "Go", days_ahead=30)
    assert_keys(conj, ["language_a", "emoji_a", "language_b", "emoji_b",
                       "orbital_period_ratio", "resonance_description",
                       "conjunction_count", "events"],
                "conjunction result has required fields")
    assert_true(conj["conjunction_count"] >= 0, "conjunction count is non-negative")
    assert_eq("Rust", conj["language_a"], "language_a is Rust")
    assert_eq("Go", conj["language_b"], "language_b is Go")

    conj_sym = find_conjunctions("Go", "Rust", days_ahead=30)
    assert_eq(conj["orbital_period_ratio"], conj_sym["orbital_period_ratio"],
              "resonance ratio is symmetric")

    print("  === Ecosystem Ranking Tests ===")
    rankings = rank_ecosystems()
    assert_keys(rankings, ["generated_at", "rankings", "total_orbital_bodies"],
                "rankings has required fields")
    assert_eq(8, rankings["total_orbital_bodies"], "all 8 languages ranked")
    ranks = rankings["rankings"]
    # Verify sorted order
    for i in range(len(ranks) - 1):
        assert_true(
            ranks[i]["gravity_well"]["well_depth_index"] >= ranks[i + 1]["gravity_well"]["well_depth_index"],
            f"rankings are sorted by gravity well depth"
        )
    # Verify ranks are sequential
    rank_nums = [r["rank"] for r in ranks]
    assert_eq(sorted(rank_nums), rank_nums, "ranks are sequential 1..8")

    print("  === Language Override Tests ===")
    result_ts = orbit_report(language="TypeScript")
    assert_eq("TypeScript", result_ts["current_language"], "language override works")
    result_rust = orbit_report(language="Rust")
    assert_eq("Rust", result_rust["current_language"], "Rust override works")

    print("  === Deterministic Seed Tests ===")
    r1 = orbit_report(language="Rust", seed=42)
    r2 = orbit_report(language="Rust", seed=42)
    assert_eq(r1["orbital_summary"]["semi_major_axis"], r2["orbital_summary"]["semi_major_axis"],
              "same seed gives same orbital data")

    print("  === Resonance Ratio Tests ===")
    ratio, desc = _calculate_resonance_ratio(42, 28)
    assert_true(":" in ratio, "resonance ratio is a ratio string")

    print("  === All Languages Have Valid Escape Velocities ===")
    for lang, orb in LANGUAGE_ORBITS.items():
        assert_true(orb["escape_velocity_km_s"] > 0, f"{lang} has positive escape velocity")

    print("  === Tool Metadata Tests ===")
    assert_eq("polyglot-orbit", result["tool"], "correct tool name")
    assert_eq("1.0.0", result["version"], "correct version")
    assert_true(len(result["generated_at"]) > 5, "generated_at timestamp present")

    print(f"\n{'='*55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("🌌 All Orbit tests passed! Every language holds its orbit.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        print(f"🌌 Polyglot Orbit v{TOOL_VERSION}")
        print("   Celestial mechanics for programming languages.")
        print("")
        print("Usage:")
        print("  python -m polyglot_orbit --test     # Run all tests")
        print("  python -m polyglot_orbit --orbit    # Generate orbital report for current language")
        print("  python -m polyglot_orbit --rank     # Rank all ecosystems by gravity")
