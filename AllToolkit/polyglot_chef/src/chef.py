#!/usr/bin/env python3
"""
🧑‍🍳 Polyglot Chef v1.0

Kitchen Brigade Tribute to Programming Languages — each language is a station
in a professional brigade kitchen, with its own cooking philosophy, mise
en place requirements, service rhythm, plating style, and signature dish.

Creative concept: "Every language is a station in the brigade. Rust is the
Sautoir who meticulously prepares every ingredient with precision, Go is the
Rôtisseur who keeps the pass flowing at speed, JavaScript is the Entremetier
who improvises with whatever arrives on the pass, and C/C++ is the
Charcutier who prepares raw provisions without safety nets."

Each language is mapped to:
  - Station name & role in the brigade
  - Cooking philosophy (technique: braising, sautéing, etc.)
  - Signature dish (what the language cooks best)
  - Mise en place requirements
  - Service rhythm (how orders flow through the station)
  - Plating philosophy (how output is presented)
  - Kitchen tool equivalents (the "knives and pans" of the language)
  - Chef's philosophy (guiding quote)

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-chef"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent  # polyglot_chef/src/ -> polyglot_chef/
_WORKSPACE_ROOT = _MODULE_DIR.parent       # polyglot_chef/ -> workspace/
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ─────────────────────────────────────────────────────────────────────────────
# Kitchen Brigade Database — each language is a kitchen station
# ─────────────────────────────────────────────────────────────────────────────

KITCHEN_DB: Dict[str, Dict[str, Any]] = {

    "Rust": {
        "station": "Sautoir Station (Sauté Chef)",
        "brigade_role": "Precision Preparations — every ingredient measured, tested, and proven",
        "cooking_philosophy": "Precision sautéing — nothing touches the pan without ownership validation",
        "technique": "Flash sauté with mandatory mise en place — prep everything before the first flame",
        "signature_dish": "Tasting Menu: Memory-Safe Systems tasting flights, concurrency consommé",
        "mise_en_place": [
            "Ownership manifests (pre-printed, laminated)",
            "Borrow validation tongs",
            "Lifetime labeling system",
            "Compile-time recipe cards only — no runtime surprises",
        ],
        "service_rhythm": "Deliberate and measured — each dish checked before leaving the pass",
        "plating_philosophy": "Architectural minimalism — clean lines, precise portions, zero clutter",
        "kitchen_tools": [
            "Borrow-checker tongs (controlled mutable access)",
            "Ownership ledger clipboard",
            "Lifetime labeling station",
            "Compile-time recipe validator",
        ],
        "chef_quote": "Mise en place is not optional. The pan is never left unguarded.",
        "service_note": "Service is slow but every plate that leaves is bulletproof.",
        "plating_style": "Modernist — white plate, geometric garnish, precisely placed",
        "station_emoji": "🍳",
        "prep_style": "Mise en place perfectionist",
        "execution_tag": "Proof-first cooking",
    },

    "Go": {
        "station": "Rôtisseur Station (Roast Chef)",
        "brigade_role": "Fast, clean roasts — keeping the pass moving at steady pace",
        "cooking_philosophy": "Clean roast technique — goroutine multitasking, no flambé drama",
        "technique": "Steady-state roasting at 130°C — reliable, fast, predictable browning",
        "signature_dish": "Roasted microservices, distributed hash-brown hash, network consommé",
        "mise_en_place": [
            "Goroutine ticketDispenser (pre-spawned and ready)",
            "Channel colanders (for draining concurrency)",
            "Lightweight mise — minimal prep, fast fire",
        ],
        "service_rhythm": "Fast 4/4 cadence — orders in, plates out, clean pass between services",
        "plating_philosophy": "Clean bistro style — functional, fast, appetizing, no fuss",
        "kitchen_tools": [
            "Goroutine ticketDispenser",
            "Channel colander set",
            "Mutex whisk (for sync when needed)",
            "Defer cleaning torch",
        ],
        "chef_quote": "A clean roast doesn't need a flambé. Just fire and timing.",
        "service_note": "Service is fast and reliable. The pass never clogs.",
        "plating_style": "Bistro — generous portions, simple garnish, speed is the garnish",
        "station_emoji": "🥩",
        "prep_style": "Minimal mise, fast fire",
        "execution_tag": "Steady-state roasting",
    },

    "Swift": {
        "station": "Entremetier Station (Vegetable & Pasta Chef)",
        "brigade_role": "Elegant plant-forward dishes — optional ingredients handled with grace",
        "cooking_philosophy": "Refined vegetable cookery — nil-safe handling, protocol-driven recipes",
        "technique": "Low-and-slow braising with graceful optional reductions",
        "signature_dish": "Protocol tasting menus, optional tasting flights, protocol-tasting menus",
        "mise_en_place": [
            "Optional ingredient rack (ingredients that may or may not arrive)",
            "Protocol recipe cards (what any dish must satisfy)",
            "Guard statement prep station",
            "Copy-on-write prep board",
        ],
        "service_rhythm": "Smooth syncopated flow — guard statements hold the line, swift plating",
        "plating_philosophy": "Fine dining elegance — micro herbs, tweezers, negative space as garnish",
        "kitchen_tools": [
            "Optional rack tongs",
            "Protocol conformance checklist",
            "Guard statement prep counter",
            "Copy-on-write cutting board",
        ],
        "chef_quote": "If an ingredient isn't on the station, we gracefully continue.",
        "service_note": "Service is smooth and lyrical. Even missing ingredients are handled with elegance.",
        "plating_style": "Fine dining — tweezers, micro herbs, artistic negative space",
        "station_emoji": "🥗",
        "prep_style": "Protocol-driven, nil-safe",
        "execution_tag": "Graceful braising",
    },

    "Kotlin": {
        "station": "Garde Manager Station (Cold Kitchen)",
        "brigade_role": "Null-safe cold preparations with extension chain plating",
        "cooking_philosophy": "Cold kitchen efficiency — null-safe mise, chain-plating, suspend-and-serve",
        "technique": "Chain-plating with extension technique — build the plate as you go",
        "signature_dish": "Extension chain tasting flights, coroutine cold bar, null-safe amuse-bouche",
        "mise_en_place": [
            "Extension chain mise station",
            "Coroutines cold prep counter",
            "Null-safe ingredient labeling",
            "Data class prep boards",
        ],
        "service_rhythm": "Flowing chain rhythm — extensions build the plate, suspend between courses",
        "plating_philosophy": "Modern cold kitchen — clean layers, build-from-bottom plating, minimal garnishes",
        "kitchen_tools": [
            "Extension chain tongs",
            "Coroutines prep torch",
            "Null-safe labeling gun",
            "Data class portioner",
        ],
        "chef_quote": "Every plate is built with extension chains — start from the base, layer up.",
        "service_note": "Service flows like a sequence. Suspend between courses, resume with grace.",
        "plating_style": "Modern layered — bottom-up construction, clean lines, functional garnish",
        "station_emoji": "🧊",
        "prep_style": "Chain-plating, null-safe",
        "execution_tag": "Flow-state cooking",
    },

    "TypeScript": {
        "station": "Chef de Partie — Type Saucer Station",
        "brigade_role": "Fast iteration, type-checked sauces, runtime surprises on the pass",
        "cooking_philosophy": "Double-time sautéing — compile-time type sauce, runtime chaos garnish",
        "technique": "Fast sauté with mandatory type reduction — sauce must reduce before service",
        "signature_dish": "Type-reduced tasting flights, interface deconstructed plates, any-ingredient mise",
        "mise_en_place": [
            "Type annotation labeling station",
            "Interface recipe cards",
            "Union type ingredient rack",
            "Any-type emergency pantry",
        ],
        "service_rhythm": "Double-time — rapid fire, type-check every sauce before it leaves",
        "plating_philosophy": "Gastro-pub creativity — bold flavors, informal plating, type-driven",
        "kitchen_tools": [
            "Type annotation squeeze bottle",
            "Interface recipe card holder",
            "Union type ingredient rack",
            "Type guard tasting spoons",
        ],
        "chef_quote": "The sauce must type-check before it hits the pass. Runtime is chaos, and that's the fun.",
        "service_note": "Service is fast-paced. Type errors are returned to station. Runtime surprises happen.",
        "plating_style": "Gastro-pub — bold, fast, creative, a little messy around the edges",
        "station_emoji": "📘",
        "prep_style": "Type-first, runtime-ready",
        "execution_tag": "Double-time sauté",
    },

    "JavaScript": {
        "station": "Entremetier Station — The Improv Station",
        "brigade_role": "Creative improvisation — whatever arrives, the kitchen adapts",
        "cooking_philosophy": "Improv cookery — prototype sharing, callback timing, async chaos",
        "technique": "Open-flame improvisation — no two services are the same",
        "signature_dish": "Prototype sharing flights, callback tasting menus, event-loop specials",
        "mise_en_place": [
            "Prototype pantry (shared ingredients across all stations)",
            "Callback timing clock",
            "Eval prep station (open flame)",
            "Late-night menu that changes every service",
        ],
        "service_rhythm": "Swing-time — callbacks create syncopated rhythm, event loop drives orders",
        "plating_philosophy": "Street food energy — bold, fast, creative, served on anything available",
        "kitchen_tools": [
            "Prototype pantry sharing system",
            "Callback timing clock",
            "setTimeout oven timer",
            "JSON ingredient manifest",
        ],
        "chef_quote": "Every plate is a prototype. We ship first, garnish later.",
        "service_note": "Service is funky and syncopated. The kitchen runs on callbacks.",
        "plating_style": "Street food energy — bold, creative, served hot, occasionally messy",
        "station_emoji": "🍳",
        "prep_style": "Prototype improvisation",
        "execution_tag": "Event-loop cooking",
    },

    "Java": {
        "station": "Charcutier Station (Cold Pantry & Cured Meats)",
        "brigade_role": "Ceremonial cold preparations — enterprise-grade charcuterie boards",
        "cooking_philosophy": "Ceremonial cookery — formal mise, checked exceptions are formal quality checks",
        "technique": "Slow-braise with formal tasting — every course must pass QC",
        "signature_dish": "Enterprise tasting flights, try-catch charcuterie boards, JVM slow-roast",
        "mise_en_place": [
            "Class hierarchy prep boards",
            "Checked exception quality-control station",
            "Interface conformance checklist",
            "JVM prep counter (the heart of the kitchen)",
        ],
        "service_rhythm": "Ceremonial march — formal timing, QC checks between courses, enterprise service",
        "plating_philosophy": "Formal banquet style — symmetrical plating, uniform garnishes, professional presentation",
        "kitchen_tools": [
            "Class hierarchy board",
            "Checked exception QC station",
            "JVM immersion circulator",
            "Generics labeling system",
        ],
        "chef_quote": "Every plate passes through QC. If it doesn't pass, we try-catch and retry.",
        "service_note": "Service is ceremonial and formal. The kitchen is a well-oiled enterprise machine.",
        "plating_style": "Formal banquet — symmetrical, uniform, professional, generous portions",
        "station_emoji": "☕",
        "prep_style": "Ceremonial enterprise",
        "execution_tag": "QC-first cooking",
    },

    "C/C++": {
        "station": "Charcutier Station — Raw Provisions",
        "brigade_role": "Raw preparations — no safety nets, full control, maximum risk",
        "cooking_philosophy": "Raw fire cooking — direct flame, manual memory, pointer precision",
        "technique": "Direct flame cooking — no safety rails, raw speed and power",
        "signature_dish": "Direct flame charcuterie, raw pointer carpaccio, buffer overflow tasting flights",
        "mise_en_place": [
            "Raw pointer prep station (no safety guards)",
            "Manual memory allocation counter",
            "Stack/heap mise separation",
            "No exception safety net — raw technique only",
        ],
        "service_rhythm": "Death metal blast beat — relentless, aggressive, maximum throughput",
        "plating_philosophy": "Industrial brutalism — no garnish, pure function, raw power on the plate",
        "kitchen_tools": [
            "Raw pointer knife set",
            "Manual memory allocation station",
            "Stack/heap mise boards",
            "Direct memory access torches",
        ],
        "chef_quote": "The kitchen has no safety nets. If you can handle the heat, you earn the pass.",
        "service_note": "Service is aggressive and relentless. Buffer overflows send plates back for rework.",
        "plating_style": "Industrial brutalism — raw, fast, functional, no garnish needed",
        "station_emoji": "⚙️",
        "prep_style": "Raw fire, no safety nets",
        "execution_tag": "Manual-memory cooking",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────────────────────

def _load_rotation(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load language rotation config."""
    path = config_path if config_path is not None else ROTATION_FILE
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_rotation(data: Dict[str, Any], config_path: Optional[str] = None) -> None:
    """Save updated rotation config."""
    path = config_path if config_path is not None else ROTATION_FILE
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _compute_next_index(current_index: int, languages: List[str]) -> int:
    """Advance index by 1, wrapping at end."""
    if not languages:
        return 0
    return (current_index + 1) % len(languages)


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def get_current_language(config_path: Optional[str] = None) -> str:
    """Return the current language from rotation config (no rotation)."""
    data = _load_rotation(config_path)
    idx = data["current_index"]
    return data["languages"][idx]


def get_station_for_language(language: str) -> Optional[Dict[str, Any]]:
    """Return the kitchen station data for a given language, or None if unknown."""
    return KITCHEN_DB.get(language)


def generate_station_report(rotate: bool = True,
                             config_path: Optional[str] = None,
                             output_format: str = "card") -> Dict[str, Any]:
    """
    Generate a kitchen brigade report for the current rotation language.

    Args:
        rotate: If True, advance the rotation index after generating the report.
        config_path: Optional path to language_rotation.json (defaults to workspace).
        output_format: "card" (human-readable) or "json" (structured dict).

    Returns:
        {
            "current_language": str,
            "current_index": int,
            "station": str,
            "brigade_role": str,
            "cooking_philosophy": str,
            "technique": str,
            "signature_dish": str,
            "mise_en_place": List[str],
            "service_rhythm": str,
            "plating_philosophy": str,
            "kitchen_tools": List[str],
            "chef_quote": str,
            "service_note": str,
            "plating_style": str,
            "station_emoji": str,
            "prep_style": str,
            "execution_tag": str,
            "rotated": bool,
            "new_index": Optional[int],
        }
    """
    data = _load_rotation(config_path)
    languages = data["languages"]
    current_index = data["current_index"]

    current_language = languages[current_index]
    station_data = KITCHEN_DB.get(current_language)

    new_index = _compute_next_index(current_index, languages)
    if rotate:
        data["current_index"] = new_index
        data["last_language"] = current_language
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        _save_rotation(data, config_path)

    if station_data is None:
        return {
            "current_language": current_language,
            "current_index": current_index,
            "station": "Unknown Station",
            "brigade_role": "Unknown role",
            "cooking_philosophy": "Unknown philosophy",
            "technique": "",
            "signature_dish": "",
            "mise_en_place": [],
            "service_rhythm": "",
            "plating_philosophy": "",
            "kitchen_tools": [],
            "chef_quote": "",
            "service_note": "",
            "plating_style": "Unknown",
            "station_emoji": "❓",
            "prep_style": "",
            "execution_tag": "Unknown",
            "rotated": rotate,
            "new_index": new_index if rotate else None,
        }

    return {
        "current_language": current_language,
        "current_index": current_index,
        **station_data,
        "rotated": rotate,
        "new_index": new_index if rotate else None,
    }


def format_station_card(m: Dict[str, Any]) -> str:
    """
    Format the station report result as a human-readable kitchen brigade card.
    """
    mise_lines = "\n".join(f"║    • {item}" for item in m.get("mise_en_place", []))
    tools_lines = "\n".join(f"║    • {item}" for item in m.get("kitchen_tools", []))

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  🧑‍🍳  POLYGLOT CHEF — Kitchen Brigade Report                        ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Language         : {m['current_language']:<47}║",
        f"║  Station          : {m['station']:<47}║",
        f"║  Role             : {m['brigade_role']:<47}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🔥  COOKING PHILOSOPHY                                          ║",
        f"║  {m['cooking_philosophy']:<64}║",
        f"║  Technique        : {m['technique']:<47}║",
        f"║  Execution Tag     : {m['execution_tag']:<47}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🍽️  SIGNATURE DISH                                              ║",
        f"║  {m['signature_dish']:<64}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  📋  MISE EN PLACE                                               ║",
        mise_lines,
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🔔  SERVICE RHYTHM                                              ║",
        f"║  {m['service_rhythm']:<64}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🍽️  PLATING PHILOSOPHY                                          ║",
        f"║  {m['plating_philosophy']:<64}║",
        f"║  Style            : {m['plating_style']:<47}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🔪  KITCHEN TOOLS                                               ║",
        tools_lines,
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🧑‍🍳  CHEF'S PHILOSOPHY                                           ║",
        f"║  \"{m['chef_quote']}\"",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  📝  SERVICE NOTE                                                 ║",
        f"║  {m['service_note']:<64}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Rotated          : {str(m['rotated']):<47}║",
        f"║  New Index        : {str(m.get('new_index', '')):<47}║",
        "╚══════════════════════════════════════════════════════════════════╝",
    ]
    return "\n".join(lines)


def run_tests() -> None:
    """Run all tests and exit."""
    import pytest
    import sys
    sys.exit(pytest.main([str(Path(__file__).parent.parent / "tests"), "-v"]))