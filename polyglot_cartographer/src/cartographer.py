#!/usr/bin/env python3
"""
🗺️ Polyglot Cartographer v1.0

Geopolitical World Map of Programming Languages — maps each language
as a nation on an ASCII map, with shared features as trade routes,
type systems as governance models, memory models as resource economies,
and ecosystems as geographical terrain.

Creative concept: "Every programming language is a nation with its own
territory, trade agreements, and economic model. Rust is a fortified
highland republic with strict resource contracts. JavaScript is a
coastal trade empire with open ports and prototype merchants.
Go is a pragmatic city-state with clean infrastructure and goroutine
harbors. This tool renders that world as a navigable ASCII map."

The tool generates a geopolitical map for the current rotation language:
- An ASCII world map with all 8 language-nations
- The current language highlighted as the "active nation"
- Trade routes (shared features) shown as dotted lines between nations
- Resource economy description per nation
- Governance model (type system)
- Terrain type (execution environment)

Distinct from existing tools:
  - polyglot_signal:      signal vocabulary (how languages signal conditions)
  - polyglot_digest:      syntax-parallel code (same logic, different syntax)
  - polyglot_translation: cultural idioms/proverbs (social cargo)
  - polyglot_chronology:  geological timeline (deep time, epochs)
  - polyglot_harmony:     pair compatibility analysis
  - polyglot_resonator:   mental model differences
  - polyglot_tempo:       rhythm patterns (feel and cadence)
  - polyglot_mood:        emotional personality profiles
  - polyglot_craft:       practical signature patterns

Cartographer is about SPATIAL RELATIONSHIPS between languages —
where they sit relative to each other, what they trade, and what
borders and terrain separate them. It's a geopolitical map of the
PL world.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-cartographer"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent.parent  # polyglot_cartographer/src/ -> polyglot_cartographer/ -> workspace/
_WORKSPACE_ROOT = _MODULE_DIR.parent             # workspace/ -> /home/admin/.openclaw/
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ─────────────────────────────────────────────────────────────────────────────
# Nation Database — each language is a nation with geopolitical attributes
# ─────────────────────────────────────────────────────────────────────────────

NATION_DB: Dict[str, Dict[str, Any]] = {

    "Rust": {
        "nation_name": "The Ownership Republic",
        "terrain": "Mountain Highlands",
        "climate": "Cold & Precise",
        "government": "Constitutional Council (Ownership Constitution)",
        "economy": "Closed Resource Economy (no GC, manual allocation by contract)",
        "imports": ["Low-level systems programming", "Zero-cost abstractions"],
        "exports": ["Memory-safe systems", "Fearless concurrency"],
        "trade_routes": {
            "C/C++": ["Systems programming", "Manual control"],
        },
        "border_policy": "Fortified borders — strict ownership contracts govern all resources",
        "unique_features": [
            "Ownership ledger — every resource has exactly one owner",
            "Borrow enforcement — no aliasing for mutable resources",
            "Lifetime annotations — resources are valid only within proven scopes",
        ],
        "cartography_symbol": "[R]",
        "map_color": "🔶",
        "diplomatic_status": {
            "Go": "mutual respect (different paradigms)",
            "Swift": "shared love of safety",
            "Kotlin": "shared null-safety values",
            "TypeScript": "distant neighbors (type layers)",
            "JavaScript": "open trade (JS/TS interoperability)",
            "Java": "enterprise trade agreements",
            "C/C++": "historic rivalry (memory model debates)",
        },
        "cartographer_note": "The Ownership Republic is the most fortified nation — every resource is contracted, every reference is validated. It builds lasting monuments.",
    },

    "Go": {
        "nation_name": "The Goroutine Harbor",
        "terrain": "Coastal Trade City-State",
        "climate": "Temperate & Practical",
        "government": "Clean Oligarchy (minimalist stdlib philosophy)",
        "economy": "Harbor Economy (goroutine channels, lightweight concurrency)",
        "imports": ["Networking infrastructure", "Cloud-native tooling"],
        "exports": ["Web servers", "Cloud tooling", "Network proxies"],
        "trade_routes": {
            "Rust": ["systems programming"],
            "JavaScript": ["server-side scripting"],
            "Java": ["enterprise services"],
        },
        "border_policy": "Open ports — goroutines can spawn freely, channels are public highways",
        "unique_features": [
            "Goroutine harbors — thousands of lightweight threads",
            "Channel waterways — typed communication between goroutines",
            "defer mechanism — automatic cleanup at border crossing",
        ],
        "cartography_symbol": "[G]",
        "map_color": "🟦",
        "diplomatic_status": {
            "Rust": "mutual respect",
            "Swift": "shared simplicity values",
            "Kotlin": "coroutine cooperation",
            "TypeScript": "backend partnership",
            "JavaScript": "full trade reciprocity",
            "Java": "enterprise mutual understanding",
            "C/C++": "pragmatic coexistence",
        },
        "cartographer_note": "The Goroutine Harbor is the world's busiest port — thousands of ships (goroutines) can be at sea simultaneously, and the channel waterways never deadlock.",
    },

    "Swift": {
        "nation_name": "The Protocol Federation",
        "terrain": "Rolling Hills & Orchards",
        "climate": "Mild & Graceful",
        "government": "Federated Council (protocols + value types)",
        "economy": "Graceful Artisan Economy (safety, expressiveness, value semantics)",
        "imports": ["Apple ecosystem", "iOS development"],
        "exports": ["iOS apps", "Safe systems code"],
        "trade_routes": {
            "Rust": ["safe systems"],
            "Kotlin": ["shared safety values"],
            "TypeScript": ["type safety advocacy"],
        },
        "border_policy": "Friendly borders — protocols define contracts, not walls",
        "unique_features": [
            "Protocol composition — mix behaviors without inheritance",
            "Value semantics — structs copy on assignment, no aliasing surprises",
            "Optional meadows — nil is a first-class concept with safe handling",
        ],
        "cartography_symbol": "[S]",
        "map_color": "🟠",
        "diplomatic_status": {
            "Rust": "shared safety values",
            "Go": "shared simplicity",
            "Kotlin": "optional safety alliance",
            "TypeScript": "type safety trade",
            "JavaScript": "cautious trade (different paradigms)",
            "Java": "enterprise dialogue",
            "C/C++": "historic tension (safety vs control)",
        },
        "cartographer_note": "The Protocol Federation is the most graceful nation — every construct is designed to be read aloud like poetry. Safety is not a feature, it's a culture.",
    },

    "Kotlin": {
        "nation_name": "The Coroutine Valley",
        "terrain": "Fertile River Valley",
        "climate": "Warm & Flowing",
        "government": "River Guilds (extension functions + coroutine flows)",
        "economy": "Flow Economy (reactive streams, suspending functions)",
        "imports": ["JVM infrastructure", "Android development"],
        "exports": ["Android apps", "JVM tooling", "Spring ecosystem"],
        "trade_routes": {
            "Go": ["coroutine cooperation"],
            "Java": ["JVM compatibility"],
            "Swift": ["safety values"],
            "Rust": ["null safety"],
        },
        "border_policy": "Open valleys — coroutines flow across borders freely",
        "unique_features": [
            "Extension function farms — add behavior without inheritance",
            "Coroutines as rivers — async flows across the entire codebase",
            "Null safety as law — nullable types are flagged at every border",
        ],
        "cartography_symbol": "[K]",
        "map_color": "🟣",
        "diplomatic_status": {
            "Rust": "null safety alliance",
            "Go": "coroutine cooperation",
            "Swift": "optional alliance",
            "TypeScript": "pragmatic trade",
            "JavaScript": "Android trade route",
            "Java": "JVM partnership",
            "C/C++": "pragmatic coexistence",
        },
        "cartographer_note": "Kotlin Valley's rivers never flood — coroutines suspend safely at border crossings. Extension functions let you farm new behavior anywhere in the territory.",
    },

    "TypeScript": {
        "nation_name": "The Type Checkpoint",
        "terrain": "Border Fort Town",
        "climate": "High Alert",
        "government": "Type Guard Council (structural typing + type erasure)",
        "economy": "Checkpoint Economy (compile-time checking, runtime flexibility)",
        "imports": ["JavaScript legacy codebases", "Web frameworks"],
        "exports": ["Web applications", "Type-safe JavaScript"],
        "trade_routes": {
            "JavaScript": ["open border — same territory, different governance"],
            "Rust": ["type safety trade"],
            "Go": ["backend partnership"],
        },
        "border_policy": "Checkpoint borders — type guards check all cargo at entry points",
        "unique_features": [
            "Structural typing — any object with the right shape can cross",
            "Type erasure at runtime — guards disappear after crossing",
            "Interface declarations — trade agreements written in plain sight",
        ],
        "cartography_symbol": "[T]",
        "map_color": "📘",
        "diplomatic_status": {
            "Rust": "type safety trade",
            "Go": "backend partnership",
            "Swift": "type safety trade",
            "Kotlin": "pragmatic trade",
            "JavaScript": "same homeland, different governance",
            "Java": "enterprise type dialogue",
            "C/C++": "distant neighbors",
        },
        "cartographer_note": "The Type Checkpoint is a fortress of type guards — every cargo crossing the border is checked at compile time, but the cargo itself runs unaccompanied at runtime.",
    },

    "JavaScript": {
        "nation_name": "The Coastal Trade Empire",
        "terrain": "Coastal Archipelago",
        "climate": "Warm & Chaotic",
        "government": "Event-Loop Parliament (prototype chain + event-driven)",
        "economy": "Prototyping Economy (prototype-based inheritance, dynamic trade)",
        "imports": ["Web browsers", "npm trade goods", "node modules"],
        "exports": ["Web applications", "npm packages", "Server tooling"],
        "trade_routes": {
            "TypeScript": ["type trade agreements (TS is a JS dialect)"],
            "Go": ["server-side trade"],
            "Java": ["enterprise trade"],
        },
        "border_policy": "Open sea borders — anyone can dock, prototypes are public warehouses",
        "unique_features": [
            "Prototype warehouses — objects clone from other objects",
            "Event-loop harbor — async ships load and unload continuously",
            "Dynamic cargo — types change at runtime like weather",
        ],
        "cartography_symbol": "[J]",
        "map_color": "💛",
        "diplomatic_status": {
            "Rust": "distant neighbors",
            "Go": "server trade",
            "Swift": "cautious trade",
            "Kotlin": "Android trade",
            "TypeScript": "same homeland, different governance",
            "Java": "enterprise trade",
            "C/C++": "historic rivalry",
        },
        "cartographer_note": "The Coastal Trade Empire is the world's largest trading nation — every ship (function) can carry any cargo (value) and the harbor (event loop) never sleeps.",
    },

    "Java": {
        "nation_name": "The Enterprise Federation",
        "terrain": "Corporate Campus Grid",
        "climate": "Stable & Institutional",
        "government": "Enterprise Board (checked exceptions + class hierarchy)",
        "economy": "Campus Economy (JVM infrastructure, institutional frameworks)",
        "imports": ["Enterprise software", "Android platform"],
        "exports": ["Enterprise software", "Android apps", "Spring frameworks"],
        "trade_routes": {
            "Kotlin": ["JVM compatibility"],
            "Go": ["enterprise services"],
            "JavaScript": ["enterprise web"],
        },
        "border_policy": "Institutional borders — checked exception forms must be signed at every crossing",
        "unique_features": [
            "Checked exception bureaucracy — every throwing function requires paperwork",
            "Class hierarchy — noble families (classes) with strict inheritance rules",
            "JVM campus — a single shared campus across all provinces",
        ],
        "cartography_symbol": "[Jv]",
        "map_color": "☕",
        "diplomatic_status": {
            "Rust": "enterprise dialogue",
            "Go": "enterprise mutual understanding",
            "Swift": "enterprise dialogue",
            "Kotlin": "JVM partnership",
            "TypeScript": "enterprise type dialogue",
            "JavaScript": "enterprise web trade",
            "C/C++": "historic enterprise rivalry",
        },
        "cartographer_note": "The Enterprise Federation is the most bureaucratic nation — every contract (method) must list its throwing obligations, and the campus (JVM) is shared by all provinces.",
    },

    "C/C++": {
        "nation_name": "The Iron Highlands",
        "terrain": "Industrial Mountain Range",
        "climate": "Harsh & Powerful",
        "government": "Anarchist Workshop (no runtime, no safety nets)",
        "economy": "Raw Resource Economy (manual memory, zero abstraction cost)",
        "imports": ["Systems programming", "Game engines", "Embedded systems"],
        "exports": ["Operating systems", "Game engines", "Embedded firmware", "Compilers"],
        "trade_routes": {
            "Rust": ["systems programming rivalry"],
            "JavaScript": ["historical rivalry"],
        },
        "border_policy": "Unmarked borders — no safety checks, raw access to all resources",
        "unique_features": [
            "Raw resource access — direct memory pointers, no guardrails",
            "Template factories — generic code generated at compile time",
            "Manual labor — every resource allocation and deallocation is hand-crafted",
        ],
        "cartography_symbol": "[C]",
        "map_color": "⚙️",
        "diplomatic_status": {
            "Rust": "historic rivalry (memory model debates)",
            "Go": "pragmatic coexistence",
            "Swift": "safety vs control tension",
            "Kotlin": "pragmatic coexistence",
            "TypeScript": "distant neighbors",
            "JavaScript": "historic rivalry",
            "Java": "historic enterprise rivalry",
        },
        "cartographer_note": "The Iron Highlands has no fences — every resource is accessible, every pointer can cross any border. It builds the fastest machines, but the terrain claims many travelers.",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# ASCII World Map — simplified geopolitical layout
# ─────────────────────────────────────────────────────────────────────────────

WORLD_MAP = """
                          ┌─────────────────────────────────────────────────────┐
                          │              POLYGLOT WORLD CARTOGRAPHY              │
                          │           Geopolitical Map of Programming Nations    │
                          └─────────────────────────────────────────────────────┘

                                      [C/C++]「Iron Highlands」
                                              │
                                              │ raw trade
                                              │
         ┌────────────────────────────────────┼────────────────────────────────────┐
         │                                    │                                    │
  ┌──────┴──────┐                    [Kotlin]「Coroutine Valley」            ┌────┴────┐
  │   [Rust]    │                    🟣  fertile river valleys                 │  Java  │
  │「Ownership  │                      │                                       │「Enter-│
  │ Republic」  │         ┌────────────┼────────────┐                        │prise」 │
  │ 🔶 highlands│         │            │             │                        │ ☕     │
  └─────────────┘         │   ┌────────┴────────┐  │                         └────────┘
         │                 │   │                 │  │                              │
         │                 │   │  [Swift]        │  │                              │
         │                 │   │「Protocol       │  │                              │
         │                 │   │ Federation」     │  │                              │
         │                 │   │ 🟠 hills         │  │                              │
         │                 │   └──────────────────┘  │                              │
         │                 │            │           │                              │
         │                 │            │           │                              │
         │                 │   ┌────────┴────────┐  │                              │
         │                 │   │                 │  │                              │
         │                 │   │ [Go]            │  │                              │
         │                 │   │「Goroutine      │  │                              │
         │                 │   │ Harbor」         │  │                              │
         │                 │   │ 🟦 coastal       │  │                              │
         │                 │   └──────────────────┘  │                              │
         │                 │            │           │                              │
         │                 │            │           │                              │
         │                 │   ┌─────────┴────────┐  │                              │
         │                 │   │                │  │                              │
         │                 │   │ [TypeScript]   │  │                              │
         │                 │   │「Type           │  │                              │
         │                 │   │ Checkpoint」    │  │                              │
         │                 │   │ 📘 border fort  │  │                              │
         │                 │   └─────────────────┘  │                              │
         │                 │            │           │                              │
         │                 │            │           │                              │
         │                 │   ┌─────────┴────────┐  │                              │
         │                 │   │                  │  │                              │
         │                 │   │ [JavaScript]     │  │                              │
         │                 │   │「Coastal Trade   │  │                              │
         │                 │   │ Empire」          │  │                              │
         │                 │   │ 💛 archipelago   │  │                              │
         │                 │   └──────────────────┘  │                              │
         │                 └──────────────────────────┘                              │
         │                                                                             │
         └─────────────────────────────────────────────────────────────────────────────┘

                                    LEGEND — Nation Terrain & Government
                                    ─────────────────────────────────────
                                    [R]   Rust — Mountain Highlands / Ownership Constitution
                                    [G]   Go — Coastal Harbor / Clean Oligarchy
                                    [S]   Swift — Rolling Hills / Protocol Federation
                                    [K]   Kotlin — River Valley / Guild Rivers
                                    [T]   TypeScript — Border Fort / Type Guard Council
                                    [J]   JavaScript — Coastal Archipelago / Event-Loop Parliament
                                    [Jv]  Java — Campus Grid / Enterprise Board
                                    [C]   C/C++ — Iron Highlands / Anarchist Workshop
"""


# ─────────────────────────────────────────────────────────────────────────────
# Trade route definitions (shared features between nations)
# ─────────────────────────────────────────────────────────────────────────────

TRADE_ROUTES: List[Dict[str, Any]] = [
    {"from": "Rust", "to": "C/C++", "routes": ["systems programming", "manual control", "zero-cost abstractions"]},
    {"from": "Rust", "to": "Swift", "routes": ["memory safety", "strong type systems"]},
    {"from": "Rust", "to": "Kotlin", "routes": ["null safety", "ownership concepts"]},
    {"from": "Go", "to": "Kotlin", "routes": ["coroutines / async concurrency"]},
    {"from": "Go", "to": "JavaScript", "routes": ["server-side scripting", "networking"]},
    {"from": "Go", "to": "Java", "routes": ["enterprise services", "cloud tooling"]},
    {"from": "Swift", "to": "Kotlin", "routes": ["null safety", "protocols vs interfaces"]},
    {"from": "Swift", "to": "TypeScript", "routes": ["type safety", "protocols / interfaces"]},
    {"from": "Kotlin", "to": "Java", "routes": ["JVM compatibility", "Android platform"]},
    {"from": "TypeScript", "to": "JavaScript", "routes": ["type layer over JS", "web ecosystem"]},
    {"from": "JavaScript", "to": "Java", "routes": ["enterprise web", "JVM interop"]},
    {"from": "Java", "to": "C/C++", "routes": ["systems programming heritage", "compiled execution"]},
]


# ─────────────────────────────────────────────────────────────────────────────
# Core API
# ─────────────────────────────────────────────────────────────────────────────

def _load_rotation(config_path: Optional[str] = None) -> Dict[str, Any]:
    path = config_path if config_path is not None else ROTATION_FILE
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_rotation(data: Dict[str, Any], config_path: Optional[str] = None) -> None:
    path = config_path if config_path is not None else ROTATION_FILE
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_current_language(config_path: Optional[str] = None) -> str:
    """Return the language at current_index."""
    data = _load_rotation(config_path)
    idx = data.get("current_index", 0)
    return data["languages"][idx % len(data["languages"])]


def get_nation_data(language: str) -> Optional[Dict[str, Any]]:
    """Return the nation data for a given language, or None."""
    return NATION_DB.get(language)


def get_trade_routes_for_language(language: str) -> List[Dict[str, Any]]:
    """Return all trade routes involving the given language."""
    routes = []
    for route in TRADE_ROUTES:
        if route["from"] == language or route["to"] == language:
            routes.append(route)
    return routes


def generate_world_report(
    rotate: bool = True,
    config_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a geopolitical cartography report for the current rotation language.

    Args:
        rotate: If True, advance the rotation index after generating the report.
        config_path: Optional path to language_rotation.json.

    Returns:
        {
            "tool": str,
            "version": str,
            "language": str,
            "current_index": int,
            "new_index": Optional[int],
            "rotated": bool,
            "nation_name": str,
            "terrain": str,
            "climate": str,
            "government": str,
            "economy": str,
            "imports": List[str],
            "exports": List[str],
            "border_policy": str,
            "unique_features": List[str],
            "cartography_symbol": str,
            "map_color": str,
            "trade_routes": List[Dict],
            "diplomatic_status": Dict[str, str],
            "cartographer_note": str,
            "world_map": str,
            "rotation_order": List[str],
            "timestamp": str,
        }
    """
    data = _load_rotation(config_path)
    langs = data["languages"]
    old_idx = data["current_index"]

    current_language = langs[old_idx]
    new_idx = (old_idx + 1) % len(langs)

    if rotate:
        data["current_index"] = new_idx
        data["last_language"] = current_language
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        _save_rotation(data, config_path)

    nation = NATION_DB.get(current_language, {})
    trade_routes = get_trade_routes_for_language(current_language)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": current_language,
        "current_index": old_idx,
        "new_index": new_idx if rotate else None,
        "rotated": rotate,
        "nation_name": nation.get("nation_name", "Unknown Nation"),
        "terrain": nation.get("terrain", "Unknown terrain"),
        "climate": nation.get("climate", "Unknown climate"),
        "government": nation.get("government", "Unknown government"),
        "economy": nation.get("economy", "Unknown economy"),
        "imports": nation.get("imports", []),
        "exports": nation.get("exports", []),
        "border_policy": nation.get("border_policy", "Unknown border policy"),
        "unique_features": nation.get("unique_features", []),
        "cartography_symbol": nation.get("cartography_symbol", "[?]"),
        "map_color": nation.get("map_color", "🌐"),
        "trade_routes": trade_routes,
        "diplomatic_status": nation.get("diplomatic_status", {}),
        "cartographer_note": nation.get("cartographer_note", ""),
        "world_map": WORLD_MAP,
        "rotation_order": ROTATION_ORDER,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def format_world_report(m: Dict[str, Any]) -> str:
    """Format the world report as a human-readable cartography card."""

    # Highlight the active nation in the world map
    lang = m["language"]
    symbol = m["cartography_symbol"]
    nation_name = m["nation_name"]

    # Build trade route lines
    trade_lines = []
    for route in m["trade_routes"]:
        partner = route["to"] if route["from"] == lang else route["from"]
        goods = ", ".join(route["routes"])
        trade_lines.append(f"  🌐 {partner}: {goods}")
    if not trade_lines:
        trade_lines = ["  (no active trade routes)"]

    # Build diplomatic status lines
    dip_lines = []
    for partner, status in m["diplomatic_status"].items():
        dip_lines.append(f"  ⚖ {partner}: {status}")
    if not dip_lines:
        dip_lines = ["  (no diplomatic relations recorded)"]

    # Build import/export lines
    imports = ", ".join(m["imports"]) if m["imports"] else "none"
    exports = ", ".join(m["exports"]) if m["exports"] else "none"

    # Build unique features lines
    feature_lines = [f"  ✦ {f}" for f in m["unique_features"]] if m["unique_features"] else ["  (no unique features recorded)"]

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  🗺️  POLYGLOT CARTOGRAPHER — Geopolitical World Map               ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Active Nation    : {nation_name:<43}║",
        f"║  Language         : {lang:<43}║",
        f"║  Index            : {m['current_index']:<43}║",
        f"║  Rotated          : {str(m['rotated']):<43}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🌍  NATION PROFILE                                             ║",
        f"║  Terrain          : {m['terrain']:<43}║",
        f"║  Climate          : {m['climate']:<43}║",
        f"║  Government       : {m['government']:<43}║",
        f"║  Economy          : {m['economy']:<43}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🚢  TRADE                                                       ║",
        f"║  Imports          : {imports:<43}║",
        f"║  Exports          : {exports:<43}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🔒  BORDER POLICY                                               ║",
        f"║  {m['border_policy']:<58}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  ✦  UNIQUE FEATURES                                              ║",
    ]

    for fl in feature_lines:
        lines.append(f"║{fl:<59}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🌐  TRADE ROUTES (shared features with neighbors)               ║",
    ]
    for tl in trade_lines:
        lines.append(f"║{tl:<59}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  ⚖  DIPLOMATIC STATUS                                           ║",
    ]
    for dl in dip_lines:
        lines.append(f"║{dl:<59}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  📝  CARTOGRAPHER'S NOTE                                        ║",
        f"║  {m['cartographer_note']:<58}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🔄  ROTATION ORDER                                             ║",
        f"║  {' → '.join(ROTATION_ORDER):<58}║",
        "╚══════════════════════════════════════════════════════════════════╝",
    ]
    return "\n".join(lines)


def run_tests() -> None:
    """Run all tests and exit."""
    import pytest
    import sys
    sys.exit(pytest.main([str(Path(__file__).parent.parent / "tests"), "-v"]))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        report = generate_world_report()
        print(format_world_report(report))
    else:
        print(f"Polyglot Cartographer v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_cartographer --test   # Run tests")
        print("  python -m polyglot_cartographer --report # Generate world report")