#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 Polyglot Bloom v1.0.0

A phenological garden engine for programming languages — each language is
treated as a plant species with its own flowering schedule, hardiness zone,
companion species, pollinators, soil chemistry, and seasonal events.

Creative concept: "Every language blooms on its own schedule. Some bloom
in spring (fresh releases), some in autumn (steady enterprise), some
year-round. This garden reveals what grows beside each language, who
pollinates it, what soil it needs, and when to expect the next bloom."

Key features:
  1. Phenology Schedule — each language's release cycle mapped to a
     flowering calendar (annual / biennial / perennial, bloom month)
  2. Companion Planting — libraries and sister languages that thrive
     when grown alongside (Spring↔Java, Cargo↔Rust, etc.)
  3. Pollinators — the projects / companies / conferences that spread
     a language's pollen (CNCF, Google, Apple, JetBrains, MS, Meta, etc.)
  4. Soil Chemistry — community health: pH (acidity = drama), NPK
     (nitrogen=jobs, phosphorus=libraries, potassium=stability)
  5. Hardiness Zone — where the language survives: startups, enterprise,
     embedded, education, finance, gaming, mobile
  6. Phenological Events — a year-long bloom calendar showing when each
     language's major releases, conferences, and ecosystem events occur
  7. Garden Health Score — composite vitality metric
  8. Bloom Forecast — predicts next bloom strength for the rotation language

Distinct from existing tools:
  - polyglot_orbit:    celestial mechanics / gravity (spatial)
  - polyglot_weather:  atmospheric pressure / ecosystem health (meteorology)
  - polyglot_fossil:   archaeological record / dead languages (fossil lens)
  - polyglot_oracle:   one-on-one wisdom counsel (oracle lens)
  - polyglot_lullaby:  bedtime narrative / soothing refactor (calming lens)
  - polyglot_reef:     coral reef ecosystem simulation (marine lens)
  - polyglot_topology: shape & connectivity (topology lens)
  - polyglot_tempo:    rhythm / beat (musical-time lens)
  - polyglot_chef:     cooking recipes for code (culinary lens)
  - polyglot_chronicle: daily events log (newspaper lens)
  - polyglot_signal:   signal processing / waveform (signal lens)
  - polyglot_metamorphosis: AST transformation (metamorphosis lens)

Bloom is about GARDENING / PHENOLOGY — when languages grow, what grows
near them, what feeds them, and what seasons shape their lifecycle.

Rotation: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import math
import os
import random
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-bloom"
TOOL_VERSION = "1.0.0"

# Resolve rotation file at workspace root (one level above AllToolkit/)
ROTATION_FILE = str(
    Path(__file__).parent.parent.parent / "language_rotation.json"
)


# ── Phenology profiles ────────────────────────────────────────────────────────
# Each language is a "species" with horticultural characteristics:
#   flowering_type      — annual / biennial / perennial
#   bloom_months        — primary release months (1-12)
#   hardiness_zone      — USDA-style ecosystem zones where it thrives
#   soil_ph             — community acidity (low=chill, high=alkaline=stable)
#   npk                 — N (jobs), P (libraries), K (stability)
#   companion_species   — sister languages / libraries that grow well beside
#   pollinators         — companies / foundations / conferences spreading it
#   bloom_color         — release / announcement color
#   emoji               — species marker
#   perennial_age_years — years since first major release
#   germination_days    — typical onboarding ramp for a new adopter
#   native_habitat      — where it originally germinated

LANGUAGE_PLANTS: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "common_name": "Memory-Safe Hawthorn",
        "scientific_name": "Rusticus borrowsii",
        "flowering_type": "perennial",
        "bloom_months": [5, 11],   # May & November (Rust releases every 6 weeks-ish, anchored on these)
        "hardiness_zone": "Zone 4-9 (Systems, WebAssembly, Embedded)",
        "soil_ph": 6.8,            # slightly acidic — opinionated
        "npk": {"N": 7.5, "P": 8.2, "K": 9.5},
        "companion_species": ["C/C++", "Zig", "TypeScript"],
        "pollinators": ["Mozilla", "AWS", "Microsoft", "Google", "Ferrous Systems", "RustConf"],
        "bloom_color": "#CE422B",
        "emoji": "🌹",
        "perennial_age_years": 16,
        "germination_days": 90,
        "native_habitat": "Mozilla research lab, 2010",
        "sun_requirement": "full sun",
        "water_need": "moderate (strict type-system watering)",
        "growth_pattern": "slow start, deep roots, blooms late but durable",
        "leaf_signature": "ownership-shaped leaves that fall only when borrow-checked",
        "threats": ["steep learning curve", "compile-time frost"],
        "uses": ["systems programming", "WebAssembly", "embedded", "cryptography"],
    },
    "Go": {
        "common_name": "Goroutine Gourd",
        "scientific_name": "Goferi concurrencyi",
        "flowering_type": "perennial",
        "bloom_months": [2, 8],   # Feb & Aug (Go's 6-month release cycle)
        "hardiness_zone": "Zone 5-10 (Cloud, DevOps, Backend)",
        "soil_ph": 7.2,            # near-neutral — pragmatic
        "npk": {"N": 9.5, "P": 7.8, "K": 8.5},
        "companion_species": ["Kubernetes", "Docker", "Rust", "TypeScript"],
        "pollinators": ["Google", "CNCF", "HashiCorp", "Uber", "Cloudflare", "GopherCon"],
        "bloom_color": "#00ADD8",
        "emoji": "🎃",
        "perennial_age_years": 16,
        "germination_days": 30,
        "native_habitat": "Google, 2009",
        "sun_requirement": "full sun",
        "water_need": "low (garbage-collected watering)",
        "growth_pattern": "fast germination, hardy vines, prolific fruit",
        "leaf_signature": "tiny leaves that pack in vast gourds of concurrency",
        "threats": ["error-handling fatigue", "package sprawl"],
        "uses": ["cloud services", "CLI tools", "DevOps", "microservices"],
    },
    "Swift": {
        "common_name": "Apple Blossom",
        "scientific_name": "Swiftii applescenti",
        "flowering_type": "perennial",
        "bloom_months": [6, 9],   # June (WWDC) & Sept (Xcode releases)
        "hardiness_zone": "Zone 6-9 (Apple ecosystem, Mobile, Server)",
        "soil_ph": 6.5,
        "npk": {"N": 7.2, "P": 7.5, "K": 8.8},
        "companion_species": ["Objective-C", "Kotlin", "Rust"],
        "pollinators": ["Apple", "IBM", "WWDC", "Swift Server Work Group"],
        "bloom_color": "#F05138",
        "emoji": "🍎",
        "perennial_age_years": 11,
        "germination_days": 45,
        "native_habitat": "Apple, 2014",
        "sun_requirement": "partial sun (sheltered by Apple canopy)",
        "water_need": "moderate",
        "growth_pattern": "showy spring blooms, fruit in autumn",
        "leaf_signature": "optional-shaped leaves (some fall, some don't)",
        "threats": ["platform lock-in", "ABI maturation weather"],
        "uses": ["iOS", "macOS", "server-side Swift", "SwiftUI"],
    },
    "Kotlin": {
        "common_name": "JetBrains Jasmine",
        "scientific_name": "Kotlini jetbrainensis",
        "flowering_type": "perennial",
        "bloom_months": [5, 11],  # Spring & Autumn Kotlin releases
        "hardiness_zone": "Zone 5-9 (Android, JVM, Multiplatform)",
        "soil_ph": 7.0,
        "npk": {"N": 8.2, "P": 8.0, "K": 8.2},
        "companion_species": ["Java", "Swift", "TypeScript"],
        "pollinators": ["JetBrains", "Google Android", "KotlinConf", "Gradle"],
        "bloom_color": "#7F52FF",
        "emoji": "🪻",
        "perennial_age_years": 14,
        "germination_days": 25,
        "native_habitat": "JetBrains, Prague, 2011",
        "sun_requirement": "full sun to partial shade",
        "water_need": "moderate (coroutine irrigation)",
        "growth_pattern": "fragrant vines, spreads along JVM trellises",
        "leaf_signature": "null-safe leaves — never wither from missing water",
        "threats": ["Android-only perception", "K2 compiler winter"],
        "uses": ["Android", "backend", "multiplatform mobile", "data science"],
    },
    "TypeScript": {
        "common_name": "Typed Tulip",
        "scientific_name": "Typescriptus strictivarietal",
        "flowering_type": "perennial",
        "bloom_months": [1, 4, 7, 10],  # quarterly minor releases
        "hardiness_zone": "Zone 3-10 (Web, Frontend, Node.js, everywhere)",
        "soil_ph": 6.9,
        "npk": {"N": 9.6, "P": 9.8, "K": 8.5},
        "companion_species": ["JavaScript", "React", "Node.js", "Deno", "Bun"],
        "pollinators": ["Microsoft", "Google", "Meta", "Vercel", "Deno Land", "npm Inc."],
        "bloom_color": "#3178C6",
        "emoji": "🌷",
        "perennial_age_years": 13,
        "germination_days": 14,
        "native_habitat": "Microsoft, 2012",
        "sun_requirement": "full sun",
        "water_need": "moderate",
        "growth_pattern": "rapid spring growth, blooms through summer, hardy in winter",
        "leaf_signature": "leaves with type annotations etched in (no any-drops)",
        "threats": ["transpiler bloat", "type-system complexity storms"],
        "uses": ["frontend", "Node.js backends", "cross-platform apps", "Deno"],
    },
    "JavaScript": {
        "common_name": "ECMAScript Elderflower",
        "scientific_name": "Javascriptus universalis",
        "flowering_type": "perennial",
        "bloom_months": [6, 12],  # June TC39 meetings & December spec freeze
        "hardiness_zone": "Zone 1-13 (everywhere)",
        "soil_ph": 7.4,            # neutral — accommodates many gardens
        "npk": {"N": 10.0, "P": 10.0, "K": 7.5},
        "companion_species": ["TypeScript", "Node.js", "Bun", "Deno", "React", "Vue"],
        "pollinators": ["TC39", "ECMA International", "Google", "Mozilla", "Apple", "Meta"],
        "bloom_color": "#F7DF1E",
        "emoji": "🌻",
        "perennial_age_years": 30,
        "germination_days": 7,
        "native_habitat": "Netscape, 1995",
        "sun_requirement": "full sun, will grow anywhere",
        "water_need": "variable (depends on the week's framework)",
        "growth_pattern": "rampant, sprawling, blooms year-round",
        "leaf_signature": "async-shaped leaves that resolve after a microtask",
        "threats": ["framework churn", "browser compatibility windstorms"],
        "uses": ["web", "server", "mobile (React Native)", "embedded (Espruino)", "ML"],
    },
    "Java": {
        "common_name": "Enterprise Oak",
        "scientific_name": "Javai robustus",
        "flowering_type": "perennial",
        "bloom_months": [3, 9],   # March & September (6-month cadence)
        "hardiness_zone": "Zone 4-10 (Enterprise, Android legacy, Backend)",
        "soil_ph": 7.6,            # slightly alkaline — stable, traditional
        "npk": {"N": 9.0, "P": 8.5, "K": 9.8},
        "companion_species": ["Kotlin", "Scala", "Spring", "Maven"],
        "pollinators": ["Oracle", "IBM", "Red Hat", "Eclipse Foundation", "JetBrains", "Jakarta EE WG"],
        "bloom_color": "#ED8B00",
        "emoji": "🌳",
        "perennial_age_years": 30,
        "germination_days": 60,
        "native_habitat": "Sun Microsystems, 1995",
        "sun_requirement": "full sun",
        "water_need": "high (JVM heap watering)",
        "growth_pattern": "slow to grow but lives for decades, deep taproot",
        "leaf_signature": "verbose leaves (each one has a clear type annotation)",
        "threats": ["verbosity blight", "GC pause droughts"],
        "uses": ["enterprise systems", "Android", "big data", "banking"],
    },
    "C/C++": {
        "common_name": "Foundational Fern",
        "scientific_name": "Cplusplus primordialis",
        "flowering_type": "perennial",
        "bloom_months": [2, 6, 10],  # ISO C/C++ committee meetings
        "hardiness_zone": "Zone 1-13 (everywhere, especially bare metal)",
        "soil_ph": 5.5,            # acidic — raw, untamed
        "npk": {"N": 8.0, "P": 6.5, "K": 9.5},
        "companion_species": ["Rust", "Zig", "Assembly"],
        "pollinators": ["ISO", "WG21", "C++ Standards Committee", "Bell Labs", "Bjarne Stroustrup"],
        "bloom_color": "#00599C",
        "emoji": "🌿",
        "perennial_age_years": 53,
        "germination_days": 365,
        "native_habitat": "Bell Labs, 1972",
        "sun_requirement": "any",
        "water_need": "manual (you must water it yourself with malloc/free)",
        "growth_pattern": "ancient lineage, spores everywhere, survives ice ages",
        "leaf_signature": "manual memory leaves — easy to forget to water",
        "threats": ["buffer overflows", "undefined behavior storms", "segmentation fault hail"],
        "uses": ["operating systems", "game engines", "embedded", "HPC", "compilers"],
    },
}


# ── Phenological helper functions ─────────────────────────────────────────────

def _calc_soil_health(plant: Dict[str, Any]) -> Dict[str, Any]:
    """Compute the soil health (community vitality) of a language ecosystem.

    soil pH near 7 is healthiest; NPK balance yields the soil rating.
    """
    ph = plant["soil_ph"]
    # distance from neutral (7.0)
    ph_balance = max(0.0, 1.0 - abs(ph - 7.0) / 2.0)
    npk = plant["npk"]
    # ideal: high & balanced; we use min() penalty
    balance = min(npk["N"], npk["P"], npk["K"]) / 10.0
    # overall soil health index 0-10
    health = (ph_balance * 0.4 + balance * 0.6) * 10.0
    if health >= 8.5:
        rating = "🌱 Rich loam — thriving soil"
    elif health >= 7.0:
        rating = "🪴 Healthy topsoil — stable community"
    elif health >= 5.5:
        rating = "🟫 Adequate soil — needs compost"
    else:
        rating = "🟨 Sandy soil — fragile foundation"

    return {
        "ph": ph,
        "ph_balance_pct": round(ph_balance * 100, 1),
        "npk": npk,
        "balance_index": round(balance, 2),
        "health_index": round(health, 2),
        "rating": rating,
    }


def _find_companion_benefit(a: str, b: str) -> Dict[str, Any]:
    """Calculate how well two languages grow together (companion planting).

    Positive benefit: shared JVM, common ecosystem, FFI.
    Negative: direct competition, paradigm mismatch.
    """
    pa = LANGUAGE_PLANTS[a]
    pb = LANGUAGE_PLANTS[b]
    benefit = 0.0
    reasons: List[str] = []

    # Companion list reciprocity
    if b in pa["companion_species"]:
        benefit += 2.5
        reasons.append(f"{b} is a registered companion of {a}")
    if a in pb["companion_species"]:
        benefit += 2.5
        reasons.append(f"{a} is a registered companion of {b}")

    # Shared pollinators
    shared_pollinators = set(pa["pollinators"]) & set(pb["pollinators"])
    if shared_pollinators:
        benefit += 1.2 * len(shared_pollinators)
        reasons.append(f"Shared pollinators: {', '.join(sorted(shared_pollinators))}")

    # Same hardiness zone overlap
    pa_zones = pa["hardiness_zone"]
    pb_zones = pb["hardiness_zone"]
    if any(z in pb_zones for z in pa_zones.split()):
        benefit += 0.8
        reasons.append("Overlapping hardiness zones")

    # Same habitat proximity
    if pa["native_habitat"].split(",")[0] == pb["native_habitat"].split(",")[0]:
        benefit += 0.5
        reasons.append("Related native habitat")

    # pH compatibility
    ph_diff = abs(pa["soil_ph"] - pb["soil_ph"])
    if ph_diff < 0.5:
        benefit += 0.6
        reasons.append("Compatible soil pH")

    if benefit >= 5:
        classification = "🌻 Thriving polyculture — excellent companions"
    elif benefit >= 3:
        classification = "🌼 Healthy guild — good companions"
    elif benefit >= 1.5:
        classification = "🌱 Neutral neighbors — coexist peacefully"
    else:
        classification = "🥀 Distant species — independent growth"

    return {
        "language_a": a,
        "language_b": b,
        "benefit_score": round(benefit, 2),
        "classification": classification,
        "reasons": reasons,
        "recommendation": _companion_recommendation(a, b, benefit),
    }


def _companion_recommendation(a: str, b: str, benefit: float) -> str:
    """Practical companion-planting advice for two languages."""
    if benefit >= 5:
        return f"Plant {a} and {b} together — they form a productive guild."
    if benefit >= 3:
        return f"{a} and {b} grow well in the same garden bed."
    if benefit >= 1.5:
        return f"{a} and {b} can share a plot but won't strongly benefit each other."
    return f"{a} and {b} prefer separate gardens — different climate needs."


def _predict_next_bloom(language: str, today: Optional[datetime] = None) -> Dict[str, Any]:
    """Predict when the language's next major bloom will occur.

    Uses the bloom_months schedule and current date.
    """
    plant = LANGUAGE_PLANTS[language]
    if today is None:
        today = datetime.now()

    bloom_months = sorted(plant["bloom_months"])
    current_month = today.month

    # Find the next bloom month >= current_month, else wrap to next year
    next_month = None
    months_ahead = 0
    for offset in range(0, 24):
        candidate = ((current_month - 1 + offset) % 12) + 1
        if candidate in bloom_months:
            next_month = candidate
            months_ahead = offset
            break

    # Strength of bloom correlates with NPK and recent activity
    strength_score = (
        plant["npk"]["N"] * 0.3
        + plant["npk"]["P"] * 0.3
        + plant["npk"]["K"] * 0.4
    )
    # More pollinators = stronger bloom
    strength_score += min(len(plant["pollinators"]), 8) * 0.4

    if strength_score >= 9:
        strength = "🌺 Spectacular bloom — major release expected"
    elif strength_score >= 7:
        strength = "🌸 Strong bloom — significant update likely"
    elif strength_score >= 5:
        strength = "🌼 Moderate bloom — incremental growth"
    else:
        strength = "🌱 Quiet bloom — minor patch expected"

    return {
        "language": language,
        "next_bloom_month": next_month,
        "months_until_bloom": months_ahead,
        "predicted_bloom_strength": strength,
        "strength_score": round(strength_score, 2),
        "bloom_color": plant["bloom_color"],
        "expected_color_hex": plant["bloom_color"],
    }


def _generate_bloom_calendar(year: int = 2026) -> Dict[str, Any]:
    """Generate a year-long bloom calendar showing when each language flowers.

    Returns a 12-month calendar with each language's bloom month marked.
    """
    calendar = []
    for month in range(1, 13):
        bloomers = []
        for lang, plant in LANGUAGE_PLANTS.items():
            if month in plant["bloom_months"]:
                bloomers.append({
                    "language": lang,
                    "emoji": plant["emoji"],
                    "bloom_color": plant["bloom_color"],
                    "common_name": plant["common_name"],
                })
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        ]
        calendar.append({
            "month": month,
            "month_name": month_names[month - 1],
            "bloomers": bloomers,
            "bloom_count": len(bloomers),
        })

    return {
        "year": year,
        "calendar": calendar,
        "peak_month": max(calendar, key=lambda m: m["bloom_count"])["month_name"],
        "quiet_month": min(calendar, key=lambda m: m["bloom_count"])["month_name"],
    }


def _pollinator_strength(language: str) -> Dict[str, Any]:
    """Assess the strength of a language's pollinator ecosystem."""
    plant = LANGUAGE_PLANTS[language]
    pollinators = plant["pollinators"]
    n = len(pollinators)

    # Categorize pollinators
    foundations = [p for p in pollinators if any(k in p for k in ["Foundation", "CNCF", "ISO", "ECMA", "WG"])]
    corporations = [p for p in pollinators if any(k in p for k in ["Google", "Apple", "Microsoft", "Meta", "IBM", "Oracle", "AWS", "Mozilla", "HashiCorp", "JetBrains", "Red Hat", "Vercel", "Deno Land", "npm", "Bell Labs"])]
    events = [p for p in pollinators if "Conf" in p or "Con" in p]

    diversity = (
        (1.0 if foundations else 0.0)
        + (1.0 if corporations else 0.0)
        + (1.0 if events else 0.0)
    )

    strength = min(10.0, n * 1.2 + diversity * 1.5)

    return {
        "language": language,
        "pollinator_count": n,
        "foundations": foundations,
        "corporations": corporations,
        "events": events,
        "diversity_score": diversity,
        "strength_index": round(strength, 2),
        "all_pollinators": pollinators,
    }


# ── Core API ──────────────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    """Load the language rotation JSON, returning a default if missing."""
    if not os.path.exists(ROTATION_FILE):
        return {
            "languages": list(LANGUAGE_PLANTS.keys()),
            "current_index": 0,
            "last_language": None,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    """Persist rotation data back to the JSON file."""
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_current_language() -> str:
    """Return the current language at rotation index without advancing."""
    cfg = load_rotation()
    langs = cfg.get("languages", list(LANGUAGE_PLANTS.keys()))
    idx = cfg.get("current_index", 0) % len(langs)
    return langs[idx]


def bloom_report(
    language: Optional[str] = None,
    advance: bool = True,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Generate a phenological report for the current rotation language.

    Reads language_rotation.json, picks the language, generates its
    botanical profile, soil health, next bloom prediction, companion
    analysis, pollinator strength, and a year-long bloom calendar.
    Advances the rotation index by default.

    Args:
        language: override the selected language (for testing)
        advance: whether to advance the rotation index after the call
        seed: optional seed for deterministic randomness

    Returns:
        dict containing the bloom report and updated rotation state
    """
    cfg = load_rotation()
    langs = cfg.get("languages", list(LANGUAGE_PLANTS.keys()))

    if language is None:
        idx = cfg.get("current_index", 0) % len(langs)
        current_lang = langs[idx]
    else:
        if language not in langs:
            raise ValueError(f"Unknown language: {language}")
        current_lang = language
        idx = langs.index(current_lang)

    if seed is not None:
        random.seed(seed)

    # Advance rotation if requested
    if advance:
        cfg["current_index"] = (idx + 1) % len(langs)
        cfg["last_language"] = current_lang
        save_rotation(cfg)

    plant = LANGUAGE_PLANTS[current_lang]
    soil = _calc_soil_health(plant)
    next_bloom = _predict_next_bloom(current_lang)
    pollinators = _pollinator_strength(current_lang)

    # Companion analysis with all other languages
    companions = []
    for other in langs:
        if other == current_lang:
            continue
        companions.append(_find_companion_benefit(current_lang, other))
    companions.sort(key=lambda c: c["benefit_score"], reverse=True)

    calendar = _generate_bloom_calendar()

    # Garden health composite score (0-10)
    health_components = [
        soil["health_index"] / 10.0,
        pollinators["strength_index"] / 10.0,
        next_bloom["strength_score"] / 12.0,
        (companions[0]["benefit_score"] / 6.0) if companions else 0.5,
    ]
    garden_health = sum(health_components) / len(health_components) * 10.0

    if garden_health >= 8.5:
        garden_class = "🌳 Verdant — flourishing garden"
    elif garden_health >= 7.0:
        garden_class = "🌲 Thriving — productive ecosystem"
    elif garden_health >= 5.5:
        garden_class = "🌿 Healthy — steady growth"
    elif garden_health >= 4.0:
        garden_class = "🍂 Stable but quiet — needs attention"
    else:
        garden_class = "🥀 Wilting — requires care"

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "current_language": current_lang,
        "rotation_index": idx,
        "next_language": langs[(idx + 1) % len(langs)] if advance else langs[idx],
        "plant_profile": plant,
        "soil_health": soil,
        "next_bloom": next_bloom,
        "pollinator_strength": pollinators,
        "companions": companions,
        "garden_health": {
            "score": round(garden_health, 2),
            "classification": garden_class,
        },
        "bloom_calendar_2026": calendar,
    }


def companion_analysis(language_a: str, language_b: str) -> Dict[str, Any]:
    """Public API: companion planting analysis between two languages."""
    return _find_companion_benefit(language_a, language_b)


def bloom_calendar(year: int = 2026) -> Dict[str, Any]:
    """Public API: full bloom calendar for the given year."""
    return _generate_bloom_calendar(year)


def garden_tour() -> Dict[str, Any]:
    """Tour all 8 language gardens with brief summaries."""
    summary = []
    for lang, plant in LANGUAGE_PLANTS.items():
        soil = _calc_soil_health(plant)
        next_bloom = _predict_next_bloom(lang)
        pollinators = _pollinator_strength(lang)
        summary.append({
            "language": lang,
            "emoji": plant["emoji"],
            "common_name": plant["common_name"],
            "scientific_name": plant["scientific_name"],
            "soil_rating": soil["rating"],
            "next_bloom": next_bloom["months_until_bloom"],
            "pollinator_count": pollinators["pollinator_count"],
            "companion_count": len(plant["companion_species"]),
        })
    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "gardens": summary,
        "total_species": len(summary),
    }


# ── Self-tests ────────────────────────────────────────────────────────────────

def run_tests() -> List[str]:
    """Run all tests for polyglot_bloom.

    Returns a list of failure messages (empty if all pass).
    """
    failures: List[str] = []
    passed = 0

    def check(cond: bool, name: str) -> None:
        nonlocal passed
        if cond:
            passed += 1
            print(f"  ✅ {name}")
        else:
            failures.append(name)
            print(f"  ❌ {name}")

    def check_eq(a: Any, b: Any, name: str) -> None:
        check(a == b, f"{name} (expected {b!r}, got {a!r})")

    def check_in(needle: Any, haystack: Any, name: str) -> None:
        check(needle in haystack, f"{name} ({needle!r} not in {haystack!r})")

    print("🌸 Polyglot Bloom v1.0.0 — Running tests")
    print()
    print("  --- Rotation File ---")
    cfg = load_rotation()
    check_eq(len(cfg["languages"]), 8, "8 languages in rotation file")
    check_in("current_index", cfg, "current_index field present")
    check_in("last_language", cfg, "last_language field present")

    print("  --- Plant Catalogue ---")
    expected_langs = [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ]
    for lang in expected_langs:
        check_in(lang, LANGUAGE_PLANTS, f"{lang} has a plant profile")

    for lang, plant in LANGUAGE_PLANTS.items():
        for field in [
            "common_name", "scientific_name", "flowering_type",
            "bloom_months", "hardiness_zone", "soil_ph", "npk",
            "companion_species", "pollinators", "bloom_color",
            "emoji", "perennial_age_years", "germination_days",
            "native_habitat",
        ]:
            check_in(field, plant, f"{lang}.{field} present")
        check(
            all(1 <= m <= 12 for m in plant["bloom_months"]),
            f"{lang} bloom_months are valid months",
        )
        check(
            0.0 <= plant["soil_ph"] <= 14.0,
            f"{lang} soil_ph is a valid pH",
        )
        check(
            all(0 <= v <= 10 for v in plant["npk"].values()),
            f"{lang} NPK values are 0-10",
        )

    print("  --- Soil Health ---")
    for lang in expected_langs:
        soil = _calc_soil_health(LANGUAGE_PLANTS[lang])
        check_in("health_index", soil, f"{lang} soil.health_index present")
        check_in("rating", soil, f"{lang} soil.rating present")
        check(
            0.0 <= soil["health_index"] <= 10.0,
            f"{lang} health_index in [0,10]",
        )

    print("  --- Companion Analysis ---")
    for a in expected_langs:
        for b in expected_langs:
            if a == b:
                continue
            c = _find_companion_benefit(a, b)
            check_in("benefit_score", c, f"{a}↔{b} benefit_score present")
            check_in("classification", c, f"{a}↔{b} classification present")
            check(c["benefit_score"] >= 0, f"{a}↔{b} benefit_score ≥ 0")
            check_eq(c["language_a"], a, f"{a} recorded as language_a")
            check_eq(c["language_b"], b, f"{b} recorded as language_b")

    # Symmetry check
    c1 = _find_companion_benefit("Rust", "Go")
    c2 = _find_companion_benefit("Go", "Rust")
    check_eq(c1["benefit_score"], c2["benefit_score"], "companion score is symmetric")

    # Registered companions should have decent scores
    c_rg = _find_companion_benefit("Rust", "C/C++")
    check(c_rg["benefit_score"] >= 2.0, "Rust↔C/C++ are listed companions")

    print("  --- Bloom Prediction ---")
    for lang in expected_langs:
        b = _predict_next_bloom(lang)
        check_in("months_until_bloom", b, f"{lang} bloom prediction present")
        check(0 <= b["months_until_bloom"] <= 12, f"{lang} bloom within 12 months")
        check_in(b["next_bloom_month"], LANGUAGE_PLANTS[lang]["bloom_months"],
                 f"{lang} predicted month is a bloom month")

    print("  --- Bloom Calendar ---")
    cal = _generate_bloom_calendar(2026)
    check_eq(cal["year"], 2026, "calendar year is 2026")
    check_eq(len(cal["calendar"]), 12, "calendar has 12 months")
    total_blooms = sum(m["bloom_count"] for m in cal["calendar"])
    expected_total = sum(len(p["bloom_months"]) for p in LANGUAGE_PLANTS.values())
    check_eq(total_blooms, expected_total, "calendar covers every bloom month")
    for m in cal["calendar"]:
        check(1 <= m["month"] <= 12, f"month {m['month']} valid")

    print("  --- Pollinator Strength ---")
    for lang in expected_langs:
        p = _pollinator_strength(lang)
        check_in("strength_index", p, f"{lang} pollinator strength present")
        check(p["pollinator_count"] >= 1, f"{lang} has at least 1 pollinator")
        check(len(p["all_pollinators"]) > 0, f"{lang} pollinator list non-empty")

    print("  --- Bloom Report ---")
    # Use language override to avoid mutating the live rotation file repeatedly
    r = bloom_report(language="Java", advance=False)
    for key in [
        "tool", "version", "generated_at", "current_language",
        "rotation_index", "next_language", "plant_profile",
        "soil_health", "next_bloom", "pollinator_strength",
        "companions", "garden_health", "bloom_calendar_2026",
    ]:
        check_in(key, r, f"report has key '{key}'")
    check_eq(r["tool"], "polyglot-bloom", "tool name correct")
    check_eq(r["version"], "1.0.0", "version correct")
    check_eq(r["current_language"], "Java", "language override works")
    check_eq(len(r["companions"]), 7, "7 companion entries (one per other language)")

    # Verify report fields are well-formed
    check(0.0 <= r["garden_health"]["score"] <= 10.0,
          "garden_health.score in [0,10]")
    check_in("classification", r["garden_health"], "garden_health.classification present")

    print("  --- Garden Tour ---")
    tour = garden_tour()
    check_eq(len(tour["gardens"]), 8, "tour covers all 8 languages")
    for entry in tour["gardens"]:
        check_in("language", entry, "tour entry has language")
        check_in("emoji", entry, "tour entry has emoji")
        check_in("common_name", entry, "tour entry has common_name")

    print("  --- Companion Analysis Public API ---")
    c = companion_analysis("Kotlin", "Java")
    check_eq(c["language_a"], "Kotlin", "companion_analysis preserves order")
    check_eq(c["language_b"], "Java", "companion_analysis preserves order")
    check(c["benefit_score"] >= 2.0, "Kotlin↔Java are listed companions")

    print("  --- Deterministic Seed ---")
    r1 = bloom_report(language="Rust", advance=False, seed=42)
    r2 = bloom_report(language="Rust", advance=False, seed=42)
    check_eq(r1["next_bloom"]["strength_score"], r2["next_bloom"]["strength_score"],
             "same seed → same strength score")

    print("  --- Rotation Advance ---")
    cfg_before = load_rotation()
    idx_before = cfg_before["current_index"]
    lang_before = cfg_before["languages"][idx_before]
    _ = bloom_report(language=lang_before, advance=True)
    cfg_after = load_rotation()
    idx_after = cfg_after["current_index"]
    check_eq((idx_before + 1) % 8, idx_after, "rotation index advanced by 1")
    check_eq(cfg_after["last_language"], lang_before,
             "last_language recorded correctly")

    # Restore rotation file to its original state to avoid pollution
    save_rotation(cfg_before)

    print("  --- All Languages Have Valid Profiles ---")
    for lang, plant in LANGUAGE_PLANTS.items():
        check(len(plant["common_name"]) > 0, f"{lang} common_name non-empty")
        check(len(plant["emoji"]) > 0, f"{lang} emoji non-empty")
        check(plant["perennial_age_years"] > 0, f"{lang} perennial_age_years > 0")
        check(plant["germination_days"] > 0, f"{lang} germination_days > 0")
        check(len(plant["companion_species"]) >= 1,
              f"{lang} has at least one companion species")
        check(len(plant["pollinators"]) >= 1,
              f"{lang} has at least one pollinator")
        check(len(plant["uses"]) >= 1, f"{lang} has at least one use")

    print()
    print(f"  Total: {passed} passed, {len(failures)} failed")
    return failures


if __name__ == "__main__":
    print("🌸 Polyglot Bloom v1.0.0 — botanical analysis for programming languages")
    print("   Import as a library, or use python -m polyglot_bloom --test")