#!/usr/bin/env python3
"""
🗼 Polyglot Lighthouse v1.0

A maritime-navigation model for programming languages. Each language is a
lighthouse standing on the coastline of the computing world, broadcasting
a characteristic light signal, warning of foggy waters, and illuminating
a reach that ships (developers) can navigate by.

Creative concept:
  "Every language is a lighthouse. Its beam is its idiom. Its height is
   its abstraction level. Its foghorn names the rocks it's saved us from.
   Sailors navigate from beacon to beacon — Rust for memory-safe shores,
   Go for cloud seas, Swift for the Apple archipelago, Kotlin for the
   JVM continent, TypeScript for the Web ocean, JavaScript for the
   shore where all ships first land, Java for the enterprise fleet,
   and C/C++ for the bare-metal rocks of the deep."

Key features:
  1. Lighthouse Beacon Profile — every language has a beam characteristic
     (flashing pattern, color, period) representing its idiomatic rhythm.
  2. Nominal Range — how far the light reaches in nautical miles
     (ecosystem reach: jobs, libraries, community).
  3. Focal Height — tower height above sea (abstraction level).
  4. Foghorn Catalogue — the named "rocks" the language has warned us
     about (footguns, anti-patterns, gotchas).
  5. Sea Conditions — current visibility (market buzz, community mood).
  6. Light Lists — a maritime-style Light List catalogue of every
     language in the rotation.
  7. Bearing & Distance — calculate the navigation angle and nautical
     distance between two languages (porting effort estimate).
  8. Safe Harbor Report — for a given use-case, which lighthouse offers
     the safest harbor (best-fit language).

Distinct from existing tools:
  - polyglot_orbit:        celestial mechanics / gravitational pulls
  - polyglot_weather:      atmospheric pressure / climate lens
  - polyglot_resonance:    wave-physics lens
  - polyglot_quantum:      quantum-physics lens
  - polyglot_spectrometer: spectral / wavelength lens
  - polyglot_oracle:       one-on-one advice
  - polyglot_dna:          genetic / trait lens
  - polyglot_recovery:     restorative / health lens
  - polyglot_geography‑like: there is none — Lighthouse is the first
    maritime / coastal-navigation lens.

Lighthouse is about MARITIME NAVIGATION — beacons, foghorns, bearings,
nautical distance, sea conditions, light lists, and safe harbors.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import math
import os
import random
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-lighthouse"
TOOL_VERSION = "1.0.0"

# Path to language_rotation.json, walking up to the workspace root.
# This file lives at /home/admin/.openclaw/workspace/AllToolkit/AllToolkit/polyglot_lighthouse/__init__.py
ROTATION_FILE = str(
    Path(__file__).resolve().parent.parent.parent.parent.parent
    / "language_rotation.json"
)


# ── Lighthouse profiles ───────────────────────────────────────────────────────
# Each language is a lighthouse with:
#   beam_color            — the lantern color (W, R, G, Y, etc.)
#   light_character       — IALA light characteristic string
#   period_seconds        — full cycle of the light signal
#   flash_count           — number of flashes per period
#   nominal_range_nm      — visible reach in nautical miles (ecosystem reach)
#   focal_height_m        — tower height above sea (abstraction level)
#   tower_shape           — silhouette / structure shape
#   year_first_lit        — release year of the language
#   automatized           — does the keeper live on-site (managed runtime)?
#   sea_location          — body of water / coast it stands on
#   foghorn_pattern       — Morse code of warning tone
#   foghorn_period_s      — seconds between foghorn blasts
#   foghorn_tone_hz       — base frequency of foghorn
#   known_rocks           — list of named "rocks" the language warns about
#   current_visibility_km — current sea-conditions visibility
#   keeper_name           — organization / foundation behind the language
#   characteristic_icon    — emoji
#   description           — short prose

LIGHTHOUSES: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "beam_color": "W",
        "beam_color_name": "White",
        "light_character": "Fl W 4s",
        "period_seconds": 4.0,
        "flash_count": 1,
        "nominal_range_nm": 22,
        "focal_height_m": 38,
        "tower_shape": "Octagonal stone tower",
        "year_first_lit": 2010,
        "automatized": True,
        "sea_location": "Memory-Safe Strait",
        "foghorn_pattern": "... --- ...",
        "foghorn_period_s": 60,
        "foghorn_tone_hz": 220,
        "known_rocks": [
            "Borrow-checker cliffs",
            "Lifetime annotations shoal",
            "Async-cancel reef",
        ],
        "current_visibility_km": 18,
        "keeper_name": "Rust Foundation",
        "characteristic_icon": "🦀",
        "color_hex": "#CE422B",
        "description": (
            "A modern, lean tower on a memory-safe headland. Its slow, "
            "steady white flash every four seconds is unmistakable in "
            "fog. Climbers love its cliffs; sailors respect its warnings."
        ),
    },
    "Go": {
        "beam_color": "W",
        "beam_color_name": "White",
        "light_character": "Iso W 2s",
        "period_seconds": 2.0,
        "flash_count": 1,
        "nominal_range_nm": 28,
        "focal_height_m": 24,
        "tower_shape": "Cylindrical concrete tower",
        "year_first_lit": 2009,
        "automatized": True,
        "sea_location": "Cloud Sea",
        "foghorn_pattern": ".. - ..",
        "foghorn_period_s": 30,
        "foghorn_tone_hz": 330,
        "known_rocks": [
            "Nil-deref reef",
            "Error-handling shallows",
            "Goroutine-leak trench",
        ],
        "current_visibility_km": 25,
        "keeper_name": "Google",
        "characteristic_icon": "🐹",
        "color_hex": "#00ADD8",
        "description": (
            "A squat but extremely bright tower on the Cloud Sea. Its "
            "isophase light is steady — easy to read in any weather. "
            "Its foghorn is short and to the point."
        ),
    },
    "Swift": {
        "beam_color": "R",
        "beam_color_name": "Red",
        "light_character": "Fl R 3s (2)",
        "period_seconds": 6.0,
        "flash_count": 2,
        "nominal_range_nm": 17,
        "focal_height_m": 30,
        "tower_shape": "Square aluminum tower",
        "year_first_lit": 2014,
        "automatized": True,
        "sea_location": "Apple Archipelago",
        "foghorn_pattern": ".- .",
        "foghorn_period_s": 45,
        "foghorn_tone_hz": 440,
        "known_rocks": [
            "ARC retain-cycle reef",
            "Optional unwrap cliff",
            "Protocol-existential shoal",
        ],
        "current_visibility_km": 14,
        "keeper_name": "Apple Inc.",
        "characteristic_icon": "🦅",
        "color_hex": "#F05138",
        "description": (
            "A red-beamed tower guarding the Apple archipelago. Its "
            "double-flash every six seconds reads as 'A' in Morse — "
            "fitting for a tower that shines only for Apple vessels."
        ),
    },
    "Kotlin": {
        "beam_color": "G",
        "beam_color_name": "Green",
        "light_character": "Fl G 5s (3)",
        "period_seconds": 10.0,
        "flash_count": 3,
        "nominal_range_nm": 20,
        "focal_height_m": 26,
        "tower_shape": "Modern cylindrical steel tower",
        "year_first_lit": 2011,
        "automatized": True,
        "sea_location": "JVM Bay",
        "foghorn_pattern": "-.- -",
        "foghorn_period_s": 50,
        "foghorn_tone_hz": 392,
        "known_rocks": [
            "Null-safety illusion shoal",
            "Coroutine-cancel cliff",
            "Java-interop reef",
        ],
        "current_visibility_km": 17,
        "keeper_name": "JetBrains",
        "characteristic_icon": "🟣",
        "color_hex": "#7F52FF",
        "description": (
            "A purple-and-green tower on JVM Bay. Its triple-flash every "
            "ten seconds is unmistakable and lets vessels distinguish it "
            "from Java's tower across the bay."
        ),
    },
    "TypeScript": {
        "beam_color": "W",
        "beam_color_name": "White",
        "light_character": "VQ W 1s",
        "period_seconds": 1.0,
        "flash_count": 5,
        "nominal_range_nm": 30,
        "focal_height_m": 42,
        "tower_shape": "Hyperboloid steel lattice",
        "year_first_lit": 2012,
        "automatized": True,
        "sea_location": "Web Ocean",
        "foghorn_pattern": "-.-. -.-",
        "foghorn_period_s": 20,
        "foghorn_tone_hz": 523,
        "known_rocks": [
            "`any` black-hole reef",
            "Type-narrowing shallows",
            "Decorator-metadata trench",
        ],
        "current_visibility_km": 28,
        "keeper_name": "Microsoft",
        "characteristic_icon": "🔷",
        "color_hex": "#3178C6",
        "description": (
            "A very-quick flashing white tower — so fast it almost "
            "looks like a strobe. Its immense lattice soars above the "
            "Web Ocean; from far away its typing ring is the only "
            "signal vessels trust."
        ),
    },
    "JavaScript": {
        "beam_color": "Y",
        "beam_color_name": "Yellow",
        "light_character": "Fl Y 2s",
        "period_seconds": 2.0,
        "flash_count": 1,
        "nominal_range_nm": 35,
        "focal_height_m": 18,
        "tower_shape": "Broad cylindrical tower",
        "year_first_lit": 1995,
        "automatized": True,
        "sea_location": "Web Ocean (central strait)",
        "foghorn_pattern": ". .-..",
        "foghorn_period_s": 25,
        "foghorn_tone_hz": 466,
        "known_rocks": [
            "Callback-pyramid reef",
            "Prototype-pollution shoal",
            "this-binding trench",
        ],
        "current_visibility_km": 30,
        "keeper_name": "ECMA TC39",
        "characteristic_icon": "🟨",
        "color_hex": "#F7DF1E",
        "description": (
            "The oldest, broadest, most-seen tower in the world. Its "
            "yellow flash every two seconds is the lingua franca of "
            "the Web Ocean. Every other lighthouse on this stretch of "
            "coast was built in its shadow."
        ),
    },
    "Java": {
        "beam_color": "Y",
        "beam_color_name": "Yellow",
        "light_character": "LFl Y 8s",
        "period_seconds": 8.0,
        "flash_count": 1,
        "nominal_range_nm": 26,
        "focal_height_m": 32,
        "tower_shape": "Square brick tower with gallery",
        "year_first_lit": 1995,
        "automatized": True,
        "sea_location": "Enterprise Harbor",
        "foghorn_pattern": ".--- .-",
        "foghorn_period_s": 60,
        "foghorn_tone_hz": 349,
        "known_rocks": [
            "NullPointer reef",
            "ClassLoader trench",
            "Checked-exception cliff",
        ],
        "current_visibility_km": 22,
        "keeper_name": "Oracle & Eclipse",
        "characteristic_icon": "☕",
        "color_hex": "#ED8B00",
        "description": (
            "A long, slow-flashing yellow tower on the enterprise "
            "harbor. Long flash, long wavelength — and a foghorn that "
            "blares the letter 'J' every minute, like a metronome."
        ),
    },
    "C/C++": {
        "beam_color": "W",
        "beam_color_name": "White",
        "light_character": "Fl W 7.5s",
        "period_seconds": 7.5,
        "flash_count": 1,
        "nominal_range_nm": 38,
        "focal_height_m": 14,
        "tower_shape": "Bare-metal skeletal tower",
        "year_first_lit": 1972,
        "automatized": False,
        "sea_location": "Bare-Metal Reef",
        "foghorn_pattern": "-.-. -.-",
        "foghorn_period_s": 90,
        "foghorn_tone_hz": 196,
        "known_rocks": [
            "Dangling-pointer reef",
            "Buffer-overflow cliff",
            "Undefined-behavior trench",
            "Preprocessor-macro shoal",
        ],
        "current_visibility_km": 32,
        "keeper_name": "ISO & community keepers",
        "characteristic_icon": "⚙️",
        "color_hex": "#00599C",
        "description": (
            "The oldest tower still standing. No automation, no "
            "keeper's cottage — just raw skeletal iron bolted to the "
            "rock. Its white flash is the slowest, deepest, widest "
            "beam of any, but the rocks around it are the most "
            "treacherous."
        ),
    },
}

# IALA light characteristic codes (simplified — for human-readable labels)
LIGHT_CHARACTER_LABELS = {
    "F":  "Fixed",
    "Fl": "Flashing",
    "LFl": "Long-flashing",
    "Iso": "Isophase",
    "VQ":  "Very-quick flashing",
    "Oc":  "Occulting",
}

# Morse code dictionary (subset)
MORSE_CODE: Dict[str, str] = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..",
}

# Inverse lookup so decoder returns the exact letter (no ambiguity with
# overlapping codes like "-.-" -> K only, not C).
_MORSE_TO_LETTER: Dict[str, str] = {code: letter for letter, code in MORSE_CODE.items()}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_light_character(char_str: str) -> Tuple[str, int, str]:
    """Parse an IALA-style light characteristic into (class, count, period_str).

    Examples:
      "Fl W 4s"            -> ("Fl", 1, "4s")
      "Fl R 3s (2)"        -> ("Fl", 2, "3s")
      "Fl G 5s (3)"        -> ("Fl", 3, "5s")
      "Iso W 2s"           -> ("Iso", 1, "2s")
      "VQ W 1s"            -> ("VQ", 5, "1s")   # by definition VQ = ~120 flashes/min
      "LFl Y 8s"           -> ("LFl", 1, "8s")
    """
    # Strip color (single capital letter at any point)
    parts = char_str.split()
    char_class = parts[0]
    # find period token (ends with 's')
    period = next((p for p in parts if p.endswith("s")), "?")
    # find count (in parentheses) or default to 1
    count = 1
    for p in parts:
        m = re.match(r"\((\d+)\)", p)
        if m:
            count = int(m.group(1))
    if char_class == "VQ":
        count = 5  # very-quick ≈ 120 flashes/min → ~5/second window
    return char_class, count, period


def _morse_to_letters(pattern: str) -> str:
    """Convert a sequence of morse letters (separated by spaces) to text.

    Empty / unknown patterns return empty string.
    """
    if not pattern:
        return ""
    letters: List[str] = []
    for token in pattern.strip().split():
        token = token.strip()
        if not token:
            continue
        letter = _MORSE_TO_LETTER.get(token)
        if letter is not None:
            letters.append(letter)
    return "".join(letters)


def _nautical_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Haversine distance in nautical miles."""
    R_nm = 3440.065  # Earth radius in nautical miles
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R_nm * c


def _bearing_deg(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Initial bearing in degrees [0, 360)."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dlam = math.radians(lon2 - lon1)
    y = math.sin(dlam) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(dlam)
    theta = math.degrees(math.atan2(y, x))
    return (theta + 360.0) % 360.0


def _bearing_cardinal(deg: float) -> str:
    """Convert bearing in degrees to a 16-point compass cardinal."""
    points = [
        "N",   "NbE", "NNE", "NEbN", "NE",  "NEbE", "ENE", "EbN",
        "E",   "EbS", "ESE", "SEbE", "SE", "SEbS", "SSE", "SbE",
        "S",   "SbW", "SSW", "SWbS", "SW", "SWbW", "WSW", "WbS",
        "W",   "WbN", "WNW", "NWbW", "NW", "NWbN", "NNW", "NbW",
    ]
    idx = int(((deg + 11.25) % 360) / 11.25)
    return points[idx]


# Deterministic "lantern coordinates" — purely synthetic so the bearing/distance
# API has something meaningful to compute on. Stable across runs.
LIGHTHOUSE_COORDS: Dict[str, Tuple[float, float]] = {
    "Rust":     (47.6062, -122.3321),   # Seattle-ish — systems / Pacific NW
    "Go":       (37.7749, -122.4194),   # San Francisco — cloud
    "Swift":    (37.3349, -122.0090),   # Cupertino — Apple archipelago
    "Kotlin":   (50.0755,  14.4378),    # Prague — JetBrains
    "TypeScript":(47.6738, -122.1215),  # Redmond — Microsoft
    "JavaScript":(51.5074,  -0.1278),   # London — TC39 / web standard
    "Java":     (37.4419, -122.1430),   # Palo Alto — Oracle vicinity
    "C/C++":    (42.3601, -71.0589),    # Boston — Bell Labs / MIT heritage
}


# ── Rotation file I/O ─────────────────────────────────────────────────────────

def load_rotation_data() -> Dict[str, Any]:
    """Load the language rotation configuration from language_rotation.json."""
    if not os.path.exists(ROTATION_FILE):
        return {
            "languages": list(LIGHTHOUSES.keys()),
            "current_index": 0,
            "last_language": None,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation_data(data: Dict[str, Any]) -> None:
    """Save updated language rotation configuration."""
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_current_language() -> str:
    """Return the currently-selected rotation language (without advancing)."""
    data = load_rotation_data()
    langs = data.get("languages", list(LIGHTHOUSES.keys()))
    idx = data.get("current_index", 0)
    return langs[idx % len(langs)]


# ── Core API ──────────────────────────────────────────────────────────────────

def light_list() -> Dict[str, Any]:
    """Return the full maritime Light List — every lighthouse in rotation."""
    entries = []
    for lang, profile in LIGHTHOUSES.items():
        char_class, flash_count, period_str = _parse_light_character(profile["light_character"])
        entries.append({
            "language": lang,
            "icon": profile["characteristic_icon"],
            "color_hex": profile["color_hex"],
            "light_character": profile["light_character"],
            "character_class": char_class,
            "character_label": LIGHT_CHARACTER_LABELS.get(char_class, char_class),
            "flash_count": flash_count,
            "period_seconds": profile["period_seconds"],
            "beam_color_name": profile["beam_color_name"],
            "focal_height_m": profile["focal_height_m"],
            "nominal_range_nm": profile["nominal_range_nm"],
            "year_first_lit": profile["year_first_lit"],
            "tower_shape": profile["tower_shape"],
            "sea_location": profile["sea_location"],
            "keeper_name": profile["keeper_name"],
            "foghorn_pattern": profile["foghorn_pattern"],
            "foghorn_decoded": _morse_to_letters(profile["foghorn_pattern"]),
        })
    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "light_list": entries,
        "total_lighthouses": len(entries),
    }


def lighthouse_report(language: Optional[str] = None, seed: Optional[int] = None) -> Dict[str, Any]:
    """Generate a complete lighthouse report for the currently selected language.

    Reads language_rotation.json, picks the language at current_index, builds
    the full beacon profile, calculates bearings and distances to every other
    language, lists foghorn warnings, sea conditions, and safe-harbor
    recommendation. Advances current_index by one at the end.

    Args:
        language: override the selected language (useful for tests).
        seed: optional seed for deterministic random elements (current visibility).

    Returns:
        dict with the full lighthouse report.
    """
    data = load_rotation_data()
    langs = data.get("languages", list(LIGHTHOUSES.keys()))

    if language is None:
        idx = data.get("current_index", 0)
        current_lang = langs[idx % len(langs)]
    else:
        if language not in langs:
            raise ValueError(f"Unknown language: {language}")
        current_lang = language
        idx = langs.index(language)

    # Advance the rotation
    next_idx = (idx + 1) % len(langs)
    data["current_index"] = next_idx
    data["last_language"] = current_lang
    save_rotation_data(data)

    profile = LIGHTHOUSES[current_lang]
    if seed is not None:
        random.seed(seed)
    current_visibility = max(
        0.5,
        profile["current_visibility_km"] + random.uniform(-2.0, 2.0),
    )

    # Bearings and distances to every other lighthouse
    bearings: List[Dict[str, Any]] = []
    for other in langs:
        if other == current_lang:
            continue
        lat1, lon1 = LIGHTHOUSE_COORDS[current_lang]
        lat2, lon2 = LIGHTHOUSE_COORDS[other]
        dist = _nautical_distance(lat1, lon1, lat2, lon2)
        brg = _bearing_deg(lat1, lon1, lat2, lon2)
        other_profile = LIGHTHOUSES[other]
        bearings.append({
            "to_language": other,
            "icon": other_profile["characteristic_icon"],
            "nautical_miles": round(dist, 2),
            "bearing_deg": round(brg, 1),
            "bearing_cardinal": _bearing_cardinal(brg),
            "within_nominal_range": dist <= profile["nominal_range_nm"],
            "their_nominal_range_nm": other_profile["nominal_range_nm"],
            "mutually_visible": (
                dist <= profile["nominal_range_nm"]
                and dist <= other_profile["nominal_range_nm"]
            ),
        })

    # Parse light characteristic
    char_class, flash_count, period_str = _parse_light_character(profile["light_character"])

    # Safe-harbor score: combine focal height, range, automatization, foghorn
    foghorn_letters = _morse_to_letters(profile["foghorn_pattern"])
    harbor_score = (
        0.30 * min(profile["nominal_range_nm"] / 40.0, 1.0)
        + 0.25 * min(profile["focal_height_m"] / 50.0, 1.0)
        + 0.15 * (1.0 if profile["automatized"] else 0.4)
        + 0.15 * min(current_visibility / 30.0, 1.0)
        + 0.15 * min(len(profile["known_rocks"]) / 5.0, 1.0)
    )
    if harbor_score >= 0.85:
        harbor_grade = "🟢 First-class harbor"
    elif harbor_score >= 0.65:
        harbor_grade = "🟡 Good harbor — minor cautions"
    elif harbor_score >= 0.45:
        harbor_grade = "🟠 Adequate harbor — heed foghorn"
    else:
        harbor_grade = "🔴 Treacherous harbor — proceed with caution"

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "current_language": current_lang,
        "rotation_index": idx,
        "next_language": langs[next_idx],
        "beacon": {
            "language": current_lang,
            "icon": profile["characteristic_icon"],
            "color_hex": profile["color_hex"],
            "light_character": profile["light_character"],
            "character_class": char_class,
            "character_label": LIGHT_CHARACTER_LABELS.get(char_class, char_class),
            "flash_count": flash_count,
            "period_seconds": profile["period_seconds"],
            "period_label": period_str,
            "beam_color_name": profile["beam_color_name"],
            "tower_shape": profile["tower_shape"],
            "year_first_lit": profile["year_first_lit"],
            "age_years": datetime.now().year - profile["year_first_lit"],
            "automatized": profile["automatized"],
            "keeper_name": profile["keeper_name"],
            "foghorn_pattern": profile["foghorn_pattern"],
            "foghorn_decoded_letters": foghorn_letters,
            "foghorn_period_s": profile["foghorn_period_s"],
            "foghorn_tone_hz": profile["foghorn_tone_hz"],
            "known_rocks": profile["known_rocks"],
            "sea_location": profile["sea_location"],
            "description": profile["description"],
        },
        "sea_conditions": {
            "current_visibility_km": round(current_visibility, 2),
            "nominal_range_nm": profile["nominal_range_nm"],
            "focal_height_m": profile["focal_height_m"],
            "harbor_score": round(harbor_score, 3),
            "harbor_grade": harbor_grade,
            "fog_density_pct": round(max(0.0, 100.0 - current_visibility * 3.3), 1),
            "wind_note": _wind_note(current_visibility, profile),
        },
        "bearings": bearings,
        "visible_lighthouses": [b["to_language"] for b in bearings if b["within_nominal_range"]],
        "mutually_visible_lighthouses": [b["to_language"] for b in bearings if b["mutually_visible"]],
    }


def _wind_note(visibility: float, profile: Dict[str, Any]) -> str:
    """A tiny bit of poetic flavor about current conditions."""
    if visibility < 5:
        return "Thick fog — only the strongest beams cut through."
    if visibility < 15:
        return "Misty — foghorn traffic is busy."
    if visibility < 25:
        return "Hazy but workable — most beams visible."
    return "Clear skies — every beacon readable."


def bearing_between(language_a: str, language_b: str) -> Dict[str, Any]:
    """Calculate the bearing and nautical distance from one lighthouse to another."""
    if language_a not in LIGHTHOUSE_COORDS or language_b not in LIGHTHOUSE_COORDS:
        raise ValueError(f"Unknown language(s): {language_a}, {language_b}")
    lat1, lon1 = LIGHTHOUSE_COORDS[language_a]
    lat2, lon2 = LIGHTHOUSE_COORDS[language_b]
    dist = _nautical_distance(lat1, lon1, lat2, lon2)
    brg = _bearing_deg(lat1, lon1, lat2, lon2)
    a = LIGHTHOUSE_COORDS[language_a]
    b = LIGHTHOUSE_COORDS[language_b]
    return {
        "from_language": language_a,
        "to_language": language_b,
        "from_coordinates": {"latitude": a[0], "longitude": a[1]},
        "to_coordinates": {"latitude": b[0], "longitude": b[1]},
        "bearing_deg": round(brg, 1),
        "bearing_cardinal": _bearing_cardinal(brg),
        "nautical_miles": round(dist, 2),
        "within_a_range": dist <= LIGHTHOUSES[language_a]["nominal_range_nm"],
        "within_b_range": dist <= LIGHTHOUSES[language_b]["nominal_range_nm"],
    }


def safe_harbor(use_case_keywords: List[str]) -> Dict[str, Any]:
    """Recommend the safest lighthouse/harbor for a given set of use-case keywords.

    Scoring is simple and transparent: each profile has a list of (keyword, score)
    pairs and we sum them. Ties broken by alphabetical order.
    """
    HARBOR_AFFINITIES: Dict[str, Dict[str, int]] = {
        "Rust":     {"systems": 3, "embedded": 3, "wasm": 2, "safety": 3, "performance": 3, "cli": 1, "low-level": 3},
        "Go":       {"cloud": 3, "backend": 3, "microservices": 3, "devops": 3, "cli": 3, "concurrency": 2, "containers": 3},
        "Swift":    {"ios": 3, "macos": 3, "apple": 3, "mobile": 2, "ui": 2},
        "Kotlin":   {"android": 3, "jvm": 3, "server": 2, "mobile": 2, "coroutines": 2},
        "TypeScript":{"web": 3, "frontend": 3, "node": 2, "types": 3, "large-codebases": 2},
        "JavaScript":{"web": 3, "browser": 3, "frontend": 2, "node": 2, "scripting": 2},
        "Java":     {"enterprise": 3, "jvm": 3, "android-legacy": 2, "backend": 2, "bigdata": 2},
        "C/C++":    {"embedded": 3, "os": 3, "game": 3, "hpc": 3, "systems": 3, "low-level": 3, "performance": 3},
    }

    kw_norm = [k.strip().lower() for k in use_case_keywords if k and k.strip()]
    scores: List[Tuple[str, int]] = []
    for lang, affinities in HARBOR_AFFINITIES.items():
        score = sum(affinities.get(k, 0) for k in kw_norm)
        scores.append((lang, score))
    scores.sort(key=lambda x: (-x[1], x[0]))

    recommended = scores[0][0] if scores else None
    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "use_case_keywords": kw_norm,
        "scores": [{"language": l, "score": s, "icon": LIGHTHOUSES[l]["characteristic_icon"]} for l, s in scores],
        "recommended_language": recommended,
        "harbor_grade": LIGHTHOUSES[recommended]["description"] if recommended else None,
    }


# ── Tests ─────────────────────────────────────────────────────────────────────

def run_tests() -> None:
    """Run all tests for the polyglot_lighthouse module."""
    passed = 0
    failed = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal passed, failed
        if cond:
            passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            failed += 1
            print(f"  ❌ FAIL: {msg}")

    def check_eq(a: Any, b: Any, msg: str) -> None:
        check(a == b, f"{msg} (expected {b!r}, got {a!r})")

    def check_in(a: Any, b: Any, msg: str) -> None:
        check(a in b, f"{msg} ({a!r} in {b!r})")

    def check_keys(d: Dict[str, Any], keys: List[str], msg: str) -> None:
        missing = [k for k in keys if k not in d]
        check(not missing, f"{msg} (missing: {missing})")

    print("Testing Polyglot Lighthouse...")

    print("  === Rotation File Tests ===")
    config = load_rotation_data()
    check_eq(8, len(config["languages"]), "8 languages in rotation")
    check_in("current_index", config, "current_index field present")
    check_in("last_language", config, "last_language field present")

    print("  === Light Character Parser Tests ===")
    char_class, count, period = _parse_light_character("Fl W 4s")
    check_eq("Fl", char_class, "Fl W 4s -> class Fl")
    check_eq(1, count, "Fl W 4s -> count 1")
    check_eq("4s", period, "Fl W 4s -> period 4s")

    char_class, count, period = _parse_light_character("Fl R 3s (2)")
    check_eq("Fl", char_class, "Fl R 3s (2) -> class Fl")
    check_eq(2, count, "Fl R 3s (2) -> count 2")
    check_eq("3s", period, "Fl R 3s (2) -> period 3s")

    char_class, count, period = _parse_light_character("VQ W 1s")
    check_eq("VQ", char_class, "VQ W 1s -> class VQ")
    check_eq(5, count, "VQ W 1s -> flash count 5")

    print("  === Morse Decoder Tests ===")
    check_eq("SOS", _morse_to_letters("... --- ..."), "morse SOS")
    check_eq("J", _morse_to_letters(".---"), "morse J")
    check_eq("CK", _morse_to_letters("-.-. -.-"), "morse CK (-.-. -> C, -.- -> K)")
    check_eq("", _morse_to_letters(""), "empty morse -> empty")

    print("  === Light List Tests ===")
    ll = light_list()
    check_keys(ll, ["tool", "version", "generated_at", "light_list", "total_lighthouses"],
               "light_list top-level keys")
    check_eq(8, ll["total_lighthouses"], "all 8 lighthouses in list")
    for entry in ll["light_list"]:
        check_keys(entry, ["language", "icon", "color_hex", "light_character",
                            "character_class", "character_label", "flash_count",
                            "period_seconds", "beam_color_name", "focal_height_m",
                            "nominal_range_nm", "year_first_lit", "tower_shape",
                            "sea_location", "keeper_name", "foghorn_pattern",
                            "foghorn_decoded"],
                    f"light_list entry {entry['language']} has required keys")
        check(entry["nominal_range_nm"] > 0, f"{entry['language']} nominal_range_nm > 0")
        check(entry["focal_height_m"] > 0, f"{entry['language']} focal_height_m > 0")
        check(entry["year_first_lit"] > 1960, f"{entry['language']} year_first_lit sane")
        check(entry["period_seconds"] > 0, f"{entry['language']} period_seconds > 0")

    print("  === Lighthouse Report Tests ===")
    result = lighthouse_report()
    check_keys(result, ["tool", "version", "generated_at", "current_language",
                         "rotation_index", "next_language", "beacon",
                         "sea_conditions", "bearings",
                         "visible_lighthouses", "mutually_visible_lighthouses"],
               "lighthouse_report top-level keys")
    check_in(result["current_language"], LIGHTHOUSES, "current_language exists in LIGHTHOUSES")
    check_keys(result["beacon"], ["language", "icon", "color_hex", "light_character",
                                   "character_class", "character_label", "flash_count",
                                   "period_seconds", "period_label", "beam_color_name",
                                   "tower_shape", "year_first_lit", "age_years",
                                   "automatized", "keeper_name", "foghorn_pattern",
                                   "foghorn_decoded_letters", "foghorn_period_s",
                                   "foghorn_tone_hz", "known_rocks", "sea_location",
                                   "description"],
               "beacon section has required fields")
    check(isinstance(result["beacon"]["known_rocks"], list) and len(result["beacon"]["known_rocks"]) >= 1,
          "known_rocks is a non-empty list")
    check(isinstance(result["beacon"]["age_years"], int) and result["beacon"]["age_years"] > 0,
          "age_years is a positive int")

    print("  === Sea Conditions Tests ===")
    sc = result["sea_conditions"]
    check_keys(sc, ["current_visibility_km", "nominal_range_nm", "focal_height_m",
                     "harbor_score", "harbor_grade", "fog_density_pct", "wind_note"],
               "sea_conditions has required keys")
    check(0.0 <= sc["harbor_score"] <= 1.0, "harbor_score in [0,1]")
    check(sc["fog_density_pct"] >= 0.0 and sc["fog_density_pct"] <= 100.0,
          "fog_density_pct in [0,100]")
    check_in("harbor", sc["harbor_grade"], "harbor_grade mentions 'harbor'")

    print("  === Bearings Tests ===")
    bearings = result["bearings"]
    check_eq(7, len(bearings), "7 bearing entries (all other languages)")
    for b in bearings:
        check_keys(b, ["to_language", "icon", "nautical_miles", "bearing_deg",
                        "bearing_cardinal", "within_nominal_range",
                        "their_nominal_range_nm", "mutually_visible"],
                    f"bearing entry for {b['to_language']} has keys")
        check(0.0 <= b["bearing_deg"] < 360.0, f"{b['to_language']} bearing_deg in [0,360)")
        check(b["nautical_miles"] >= 0.0, f"{b['to_language']} nautical_miles >= 0")
        check_in(b["bearing_cardinal"],
                  ["N", "NbE", "NNE", "NEbN", "NE", "NEbE", "ENE", "EbN",
                   "E", "EbS", "ESE", "SEbE", "SE", "SEbS", "SSE", "SbE",
                   "S", "SbW", "SSW", "SWbS", "SW", "SWbW", "WSW", "WbS",
                   "W", "WbN", "WNW", "NWbW", "NW", "NWbN", "NNW", "NbW"],
                  f"{b['to_language']} bearing_cardinal is a valid compass point")
        check(isinstance(b["within_nominal_range"], bool), "within_nominal_range is bool")
        check(isinstance(b["mutually_visible"], bool), "mutually_visible is bool")

    print("  === Lighthouse Coordinates Tests ===")
    for lang, (lat, lon) in LIGHTHOUSE_COORDS.items():
        check_in(lang, LIGHTHOUSES, f"{lang} has coordinates")
        check(-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0,
              f"{lang} coordinates are valid lat/lon")

    print("  === Distance / Bearing Function Tests ===")
    same = bearing_between("Go", "Go")
    check_eq(0.0, same["nautical_miles"], "distance Go->Go is 0")
    check_eq(0.0, same["bearing_deg"], "bearing Go->Go is 0")

    ab = bearing_between("Rust", "Go")
    ba = bearing_between("Go", "Rust")
    check_eq(ab["nautical_miles"], ba["nautical_miles"], "distance is symmetric")
    check(ab["bearing_deg"] != ba["bearing_deg"] or ab["bearing_deg"] == 0.0,
          "reciprocal bearings differ (or are both 0 along the same meridian)")

    print("  === Rotation Advance Tests ===")
    idx_before = load_rotation_data()["current_index"]
    lang_before = load_rotation_data()["languages"][idx_before]
    _ = lighthouse_report()
    idx_after = load_rotation_data()["current_index"]
    check_eq((idx_before + 1) % 8, idx_after, "index advanced by 1")
    check_eq(lang_before, load_rotation_data()["last_language"], "last_language recorded")

    print("  === Safe Harbor Tests ===")
    sh = safe_harbor(["systems", "embedded", "performance"])
    check_keys(sh, ["tool", "version", "use_case_keywords", "scores",
                     "recommended_language", "harbor_grade"],
               "safe_harbor has required keys")
    check_eq(["systems", "embedded", "performance"], sh["use_case_keywords"],
             "use_case_keywords preserved")
    # Rust and C/C++ should be top contenders for systems/embedded
    top_two = [s["language"] for s in sh["scores"][:2]]
    check_in("Rust", top_two + [s["language"] for s in sh["scores"]], "Rust appears in scores")
    check_in("C/C++", top_two + [s["language"] for s in sh["scores"]], "C/C++ appears in scores")
    check(sh["recommended_language"] in LIGHTHOUSES, "recommended_language is a known lighthouse")

    sh_empty = safe_harbor([])
    check(sh_empty["recommended_language"] is None or sh_empty["recommended_language"] in LIGHTHOUSES,
          "empty keywords handled gracefully")

    sh_web = safe_harbor(["web", "frontend"])
    check_in("JavaScript", [s["language"] for s in sh_web["scores"]], "JavaScript appears for web")
    check_in("TypeScript", [s["language"] for s in sh_web["scores"]], "TypeScript appears for web")

    sh_apple = safe_harbor(["ios", "apple", "macos"])
    check_eq("Swift", sh_apple["recommended_language"], "Swift recommended for ios/apple/macos")

    sh_android = safe_harbor(["android", "mobile"])
    check_in("Kotlin", [s["language"] for s in sh_android["scores"][:3]], "Kotlin in top 3 for android")

    sh_cloud = safe_harbor(["cloud", "backend", "microservices", "containers"])
    check_eq("Go", sh_cloud["recommended_language"], "Go recommended for cloud/backend")

    print("  === Language Override Tests ===")
    res_ts = lighthouse_report(language="TypeScript")
    check_eq("TypeScript", res_ts["current_language"], "TypeScript override")
    res_rust = lighthouse_report(language="Rust")
    check_eq("Rust", res_rust["current_language"], "Rust override")

    print("  === Deterministic Seed Tests ===")
    r1 = lighthouse_report(language="Rust", seed=42)
    r2 = lighthouse_report(language="Rust", seed=42)
    check_eq(r1["sea_conditions"]["current_visibility_km"],
             r2["sea_conditions"]["current_visibility_km"],
             "same seed -> same visibility")

    print("  === Tool Metadata Tests ===")
    check_eq("polyglot-lighthouse", result["tool"], "correct tool name")
    check_eq("1.0.0", result["version"], "correct version")
    check(len(result["generated_at"]) > 5, "generated_at timestamp present")

    print("  === Foghorn Decoding for All Languages ===")
    for lang, profile in LIGHTHOUSES.items():
        decoded = _morse_to_letters(profile["foghorn_pattern"])
        check(isinstance(decoded, str), f"{lang} foghorn decodes to a string ({decoded!r})")

    print("  === Harbor Affinity Score Symmetry Tests ===")
    sh_a = safe_harbor(["systems"])
    sh_b = safe_harbor(["systems", "embedded"])
    check(sh_b["scores"][0]["score"] >= sh_a["scores"][0]["score"],
          "more matching keywords never decrease the top score")

    print(f"\n{'='*60}")
    print(f"Tests: {passed} passed, {failed} failed")
    if failed == 0:
        print("🗼 All Lighthouse tests passed! Every beacon shines steady.")
    else:
        print(f"💥 {failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        print(f"🗼 Polyglot Lighthouse v{TOOL_VERSION}")
        print("   Maritime navigation for programming languages.")
        print("")
        print("Usage:")
        print("  python -m polyglot_lighthouse --test       # Run all tests")
        print("  python -m polyglot_lighthouse --report     # Generate lighthouse report")
        print("  python -m polyglot_lighthouse --lightlist  # Show the full Light List")
        print("  python -m polyglot_lighthouse --bearing <a> <b>  # Bearing between two languages")
        print("  python -m polyglot_lighthouse --harbor <kw1,kw2,...>  # Find a safe harbor")