#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⛪ Polyglot Cathedral v1.0.0
A gothic-architecture engine for programming languages — every language
is a cathedral, with a floor plan, nave, transepts, flying buttresses,
stained glass, gargoyles, bell tower, rose window, vaulted ceiling,
foundation, and a long lineage of architects.

Creative concept:
  "Every program is a building, and every language is the cathedral
   that hosts it. Some cathedrals are Romanesque and stout (C), some
   are Gothic and soaring (Rust), some are Baroque with too many
   decorations (Java), some are Modernist and minimalist (Go), some
   are airy glass-roofed atria (TypeScript), some are organic Gaudí
   shapes (JavaScript). The developer is the architect who decides
   where the foundation stones are, what the vaulted ceiling looks
   like, what gargoyles guard the corners, and how the light comes
   in through the rose window. This tool shows the floor plan, the
   buttresses, the stained glass, and the bell-tower rhythm for
   whichever cathedral the rotation has selected."

Key features:
  1. Cathedral Catalogue     — every language mapped to a cathedral
  2. Floor Plan             — paradigm blueprint
  3. Nave                   — main central runtime chamber
  4. Transepts              — ecosystem chambers (libraries, tools)
  5. Flying Buttresses      — type-system supports
  6. Stained Glass          — syntax highlighting palette
  7. Gargoyles              — footguns / sharp edges
  8. Bell Tower             — concurrency rhythm & cadence
  9. Rose Window            — central abstraction (core idea)
 10. Vaulted Ceiling        — control flow architecture
 11. Foundation             — VM / runtime substrate
 12. Architect Lineage      — creator/maintainer history
 13. Construction Era       — age & construction milestones
 14. Pilgrimage Count       — adoption / visitors per year
 15. Cathedral Tour         — visit all 8 cathedrals in rotation order
 16. Side-By-Side Naves     — pairwise comparison of two cathedrals
 17. Blueprint Snippet      — for a given code snippet, which cathedral fits
 18. Rotation Advance       — reads/updates language_rotation.json

Distinct from existing tools:
  - polyglot_bloom:        gardening / phenology
  - polyglot_loom:         weaving / textile arts
  - polyglot_lighthouse:    maritime / pharos (light over the sea)
  - polyglot_horology:     watchmaking / clockwork
  - polyglot_reef:         marine ecosystem (organisms)
  - polyglot_orbit:        celestial mechanics (planets/moons)
  - polyglot_vessel:       alchemical distillation
  - polyglot_wire:         electrical FFI
  - polyglot_forge:        metalworking / smithing
  - polyglot_pulse:        vital signs (medical)
  - polyglot_mood:         emotional profiling
  - polyglot_flavor:       sensory sommelier
  - polyglot_architect:    (already exists) — building planner, different lens

Cathedral is about GOTHIC ARCHITECTURE — plans, naves, transepts,
flying buttresses, stained glass, gargoyles, bell towers, rose windows,
vaulted ceilings, foundations, architects. No other tool does that.

Rotation: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import math
import os
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-cathedral"
TOOL_VERSION = "1.0.0"

# Resolve rotation file at workspace root (one level above AllToolkit/).
# We walk upward looking for `language_rotation.json`.
ROTATION_FILE = str(
    Path(__file__).parent.parent.parent / "language_rotation.json"
)


# ── Cathedral catalogue ──────────────────────────────────────────────────────
# Each language is a cathedral. A cathedral has:
#   name                — the language
#   diocese             — the conceptual diocese it serves
#   built               — year construction began
#   completed           — year it became stable
#   style               — architectural style (Gothic / Romanesque / ...)
#   floor_plan          — paradigm blueprint (OOP, functional, ...)
#   nave                — main central chamber (runtime)
#   nave_length_m       — length of the nave (expressiveness)
#   transepts           — ecosystem chambers
#   flying_buttresses   — type system supports
#   stained_glass       — syntax highlighting palette (3-5 colors)
#   gargoyles           — footguns / sharp edges
#   bell_tower          — concurrency mechanism
#   bell_cadence        — characteristic rhythm
#   rose_window         — central abstraction (core idea)
#   vaulted_ceiling     — control flow architecture
#   foundation          — VM / runtime substrate
#   architects          — creator/maintainer lineage
#   construction_log    — historical milestones
#   pilgrimage_count    — adoption / visitors per year (0-100)
#   light_intensity     — perceived DX / ergonomics (0-100)
#   height_m            — spire height (expressiveness ceiling)
#   alignment_deg       — compass bearing (unique angle)
#   emoji               — species marker
#   stone               — primary building material

CATHEDRALS: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "name": "Rust",
        "diocese": "Diocese of Memory-Safety",
        "built": 2006,
        "completed": 2015,
        "style": "Bourges Gothic (soaring, mathematically pure)",
        "floor_plan": "Centralised Latin cross — types, ownership, lifetimes",
        "nave": "Ownership-Nave — three aisles: Owner, &Borrower, &mut Borrower",
        "nave_length_m": 184,
        "transepts": [
            "cargo (north transept — the registry of crates)",
            "rustc (south transept — the stonemason's workshop)",
            "Clippy (chancel — the moral theologian)",
        ],
        "flying_buttresses": [
            "Lifetime buttresses connecting each stone to its birth-certificate",
            "Send/Sync flying-buttresses across the aisle of threads",
            "Trait-arc buttresses — abstract stone arches",
        ],
        "stained_glass": ["#ff6b35", "#1e6091", "#5b8e7d", "#dec146"],
        "gargoyles": [
            "the Borrow-Checker Gargoyle (lifetime annotations spit on newcomers)",
            "the Async-Trait Gargoyle (still under restoration)",
            "the Compile-Time Fog Gargoyle (long build seasons)",
        ],
        "bell_tower": "Single great bell — async/await, with a worker-bee carillon",
        "bell_cadence": "Group-Flash (3) every 12 s — predict, validate, commit",
        "rose_window": "The Ownership Rose — Owner / & / &mut / *const — light through capability",
        "vaulted_ceiling": "Ribbed vault — every function is a rib returning to its origin type",
        "foundation": "LLVM bedrock (stable, deep, hand-laid)",
        "architects": "Graydon Hoare → Niko Matsakis → Steve Klabnik → Ferrous Steering Guild",
        "construction_log": [
            "2006 — Graydon Hoare lays the cornerstone at Mozilla Research",
            "2010 — First public service held (pre-1.0)",
            "2015 — Consecration: Rust 1.0 declared a stable cathedral",
            "2018 — Async-await chapel dedicated",
            "2021 — Edition 2021 reshapes the north transept",
            "2024 — Async-trait rose-window fully restored",
        ],
        "pilgrimage_count": 82,
        "light_intensity": 78,
        "height_m": 184,
        "alignment_deg": 7,
        "emoji": "🛡️",
        "stone": "Wrought-iron lifetime granite",
    },
    "Go": {
        "name": "Go",
        "diocese": "Diocese of Simplicity",
        "built": 2007,
        "completed": 2012,
        "style": "Modernist Functional (clean lines, no ornament)",
        "floor_plan": "Open plan — packages and funcs, no private chapels",
        "nave": "Goroutine-Nave — thousands of small pews under one roof",
        "nave_length_m": 110,
        "transepts": [
            "go (north — the bell-ringer for new processes)",
            "gofmt (south — the mason who keeps stones uniform)",
            "net/http (chancel — the public cloister)",
        ],
        "flying_buttresses": [
            "Interface buttresses — every duck-shaped arch is supported",
            "Channel flying-buttresses across the courtyard of goroutines",
        ],
        "stained_glass": ["#00add8", "#9bdf6c", "#fefefe", "#7a7a7a"],
        "gargoyles": [
            "the Verbosity Gargoyle (no map/filter chain)",
            "the Error-Wrapping Gargoyle (if err != nil)",
            "the GC Gargoyle (latency pauses at scale)",
        ],
        "bell_tower": "Iso-phase carillon — predictable, one bell at a time",
        "bell_cadence": "Steady even chime every 6 s — predictable like a tide",
        "rose_window": "The Interface Rose — methods grouped by shape, not name",
        "vaulted_ceiling": "Flat roof — no metaprogramming vault overhead",
        "foundation": "Hand-laid runtime stone (no VM, no JIT)",
        "architects": "Pike → Thompson → Griesemer → Russ Cox → Go team",
        "construction_log": [
            "2007 — Google architects sketch the floor plan",
            "2009 — Public unveiling — first service held",
            "2012 — Consecration: Go 1.0 declared stable",
            "2018 — Modules chapel added to the south transept",
            "2021 — Generics rose-window finally installed",
            "2024 — Range-over-func illuminates new corridors",
        ],
        "pilgrimage_count": 88,
        "light_intensity": 80,
        "height_m": 110,
        "alignment_deg": 90,
        "emoji": "🐹",
        "stone": "Plain concrete — no frills",
    },
    "Swift": {
        "name": "Swift",
        "diocese": "Diocese of Apple",
        "built": 2010,
        "completed": 2015,
        "style": "Late-Baroque with Modernist Inflection",
        "floor_plan": "Cupertino cross — protocols, extensions, structs, enums",
        "nave": "ARC-Nave — every pew holds an automatic reference counter",
        "nave_length_m": 142,
        "transepts": [
            "Xcode (north transept — the workshop of the cathedral)",
            "SwiftUI (south — the rose-coloured chapel)",
            "Combine (chancel — the event-bell hall)",
        ],
        "flying_buttresses": [
            "Protocol-extension buttresses — adding stones without rebuilding",
            "Result / Optional flying-buttresses over the channel of failure",
        ],
        "stained_glass": ["#f05138", "#ffac45", "#0a84ff", "#5e5ce6"],
        "gargoyles": [
            "the iOS-Only Gargoyle (server Swift is a small porch)",
            "the ABI-Drift Gargoyle (toolchain churn between Xcodes)",
            "the Closure-Capture Gargoyle (retain cycles under the floor)",
        ],
        "bell_tower": "Long-flash 2 s + eclipse 6 s — show, hide, show",
        "bell_cadence": "Long-Flash 2 s + Eclipse 6 s",
        "rose_window": "The Protocol Rose — shapes first, identity never",
        "vaulted_ceiling": "Optional-vault — every ceiling supports the load-bearing Optional",
        "foundation": "LLVM bedrock (shared with Rust, but frescoed differently)",
        "architects": "Chris Lattner → Joe Groff → Apple Swift Core Team",
        "construction_log": [
            "2010 — Chris Lattner sketches the first drawing at Apple",
            "2014 — Public consecration — Swift 1.0 opens",
            "2015 — Swift 2.0 reshapes the error-handling nave",
            "2017 — ABI stability completes the foundation",
            "2019 — SwiftUI chapel dedicated",
            "2023 — Concurrency tower (async/await + actors) topped out",
        ],
        "pilgrimage_count": 70,
        "light_intensity": 86,
        "height_m": 142,
        "alignment_deg": 215,
        "emoji": "🦅",
        "stone": "Polished aluminium & protocol granite",
    },
    "Kotlin": {
        "name": "Kotlin",
        "diocese": "Diocese of Pragmatism",
        "built": 2010,
        "completed": 2016,
        "style": "Reformed Gothic with Russian-Orthodox cupolas",
        "floor_plan": "Pragmatic Greek cross — JVM at the altar, Native side-chapel",
        "nave": "JVM-Nave — bytecode pews, with a Native-coroutine side-aisle",
        "nave_length_m": 128,
        "transepts": [
            "IntelliJ IDEA (north transept — the architect's drafting table)",
            "Coroutines (south — the side-chapel of structured concurrency)",
            "Compose (chancel — the new liturgical screen)",
        ],
        "flying_buttresses": [
            "Null-safety buttresses — NPE gargoyles banished from the eaves",
            "Extension-function flying-buttresses over any type",
            "Coroutine-scope buttresses across the aisle of threads",
        ],
        "stained_glass": ["#7f52ff", "#c711e1", "#a8c545", "#f4d03f"],
        "gargoyles": [
            "the Compile-Speed Gargoyle (slower than Java in big builds)",
            "the Coroutine-Cancellation Gargoyle (structured concurrency rocks)",
            "the Magic-Function Gargoyle (implicit conversions surprise pilgrims)",
        ],
        "bell_tower": "Quick-flash 0.3 s every 4 s — concise, expressive pulses",
        "bell_cadence": "Quick-Flash 0.3 s every 4 s",
        "rose_window": "The Extension Rose — adding methods to old stones",
        "vaulted_ceiling": "Coroutine-vault — every ceiling suspends the load-bearing suspend",
        "foundation": "JVM bedrock (ancient, well-known, stable)",
        "architects": "Andrey Breslav → JetBrains → Kotlin Foundation",
        "construction_log": [
            "2010 — JetBrains lays the cornerstone in St. Petersburg",
            "2016 — Consecration: Kotlin 1.0 declared stable",
            "2017 — Google declares it a first-class Android cathedral",
            "2019 — Coroutines tower topped out",
            "2023 — K2 compiler (FIR) re-points the entire nave",
            "2024 — Compose Multiplatform opens new cloisters",
        ],
        "pilgrimage_count": 76,
        "light_intensity": 90,
        "height_m": 128,
        "alignment_deg": 270,
        "emoji": "🟣",
        "stone": "Stainless coroutine steel with null-safety inlays",
    },
    "TypeScript": {
        "name": "TypeScript",
        "diocese": "Diocese of Static Discipline",
        "built": 2010,
        "completed": 2014,
        "style": "Blueprint-Gothic (plans first, building later)",
        "floor_plan": "JavaScript floor plan, but with surveyed elevations",
        "nave": "TSC-Nave — the compiler's lantern room transcribes plans into JS",
        "nave_length_m": 156,
        "transepts": [
            "tsc (north transept — the surveyor)",
            "ts-node / tsx (south — the lay-clerk who runs plans directly)",
            "DefinitelyTyped (chancel — the open library of borrowed plans)",
        ],
        "flying_buttresses": [
            "Structural-typing buttresses — every stone supports every shape-compatible stone",
            "Conditional-type flying-buttresses across the type-aisle",
        ],
        "stained_glass": ["#3178c6", "#235a97", "#ffffff", "#f5f5f5"],
        "gargoyles": [
            "the Type-Erasure Gargoyle (runtime still JS)",
            "the any-Gargoyle (escape hatch still lit)",
            "the Strict-Mode Gargoyle (opt-in cleanup still ongoing)",
        ],
        "bell_tower": "Strobe 0.05 s every 2 s — incremental types, quick ticks",
        "bell_cadence": "Strobe 0.05 s every 2 s",
        "rose_window": "The Structural Rose — shapes win, identity loses",
        "vaulted_ceiling": "Mapped-type vault — every key on every stone",
        "foundation": "JavaScript bedrock (transmuted, but original soil)",
        "architects": "Anders Hejlsberg → Microsoft → TS Core Team",
        "construction_log": [
            "2010 — Anders Hejlsberg drafts the original plans at Microsoft",
            "2014 — Consecration: TS 1.0 declares stable plans",
            "2016 — Async/await chapel built",
            "2020 — Variadic Tuple Types refine the rose window",
            "2022 — satisfies / const type parameters widen the nave",
            "2024 — Type-level performance polish for huge cathedrals",
        ],
        "pilgrimage_count": 96,
        "light_intensity": 88,
        "height_m": 156,
        "alignment_deg": 333,
        "emoji": "🟦",
        "stone": "Structural-type concrete, transmuted from JS bedrock",
    },
    "JavaScript": {
        "name": "JavaScript",
        "diocese": "Diocese of the Open Web",
        "built": 1995,
        "completed": 1997,
        "style": "Gaudí Organic (asymmetric, growing, surprising)",
        "floor_plan": "Event-Loop labyrinth — one central cloister, many side-chapels",
        "nave": "Event-Loop-Nave — single-threaded, with a microtask queue",
        "nave_length_m": 132,
        "transepts": [
            "Browser DOM (north transept — the public cloister)",
            "Node.js (south — the back-alley chapel of servers)",
            "npm (chancel — the reliquary of packages)",
        ],
        "flying_buttresses": [
            "Prototype-chain buttresses — every stone knows its ancestor",
            "Promise-flying-buttresses across the aisle of async",
            "WeakMap / WeakSet flying-buttresses over the crypt",
        ],
        "stained_glass": ["#f7df1e", "#000000", "#ffffff", "#264de4"],
        "gargoyles": [
            "the == Gargoyle (coercion rocks)",
            "the this-Whirlpool Gargoyle (binding changes with context)",
            "the Callback-Pyramid Gargoyle",
        ],
        "bell_tower": "Single tick every 1 s — quick ticks of the event loop",
        "bell_cadence": "Single-Flash every 1 s",
        "rose_window": "The Object Rose — everything is an object, until it isn't",
        "vaulted_ceiling": "Closure-vault — every function is a flying buttress with a private ceiling",
        "foundation": "Engine-specific bedrock (V8, SpiderMonkey, JSC)",
        "architects": "Brendan Eich → Netscape → ECMA TC39 → Open Web",
        "construction_log": [
            "1995 — Brendan Eich lays the cornerstone in 10 days at Netscape",
            "1997 — ECMAScript 1 standardises the plans",
            "2009 — Node.js builds the south transept for the server cloister",
            "2015 — ES6 (ES2015) reshapes the entire nave",
            "2020 — Optional chaining, nullish-coalescing open new chapels",
            "2024 — Records/Tuples, Temporal API focus the time-window",
        ],
        "pilgrimage_count": 99,
        "light_intensity": 72,
        "height_m": 132,
        "alignment_deg": 18,
        "emoji": "🟨",
        "stone": "Living vines — grows new branches every TC39 meeting",
    },
    "Java": {
        "name": "Java",
        "diocese": "Diocese of Enterprise",
        "built": 1991,
        "completed": 1996,
        "style": "Romanesque-Classical (load-bearing pillars, lots of marble)",
        "floor_plan": "Class-hierarchy basilica — inheritance dominates the plan",
        "nave": "JVM-Nave — the eternal flame keeps burning, version after version",
        "nave_length_m": 168,
        "transepts": [
            "JDK (north — the workshop of the cathedral)",
            "Spring / Jakarta EE (south — the cloister of enterprise)",
            "Maven / Gradle (chancel — the liturgy of building)",
        ],
        "flying_buttresses": [
            "Class-hierarchy buttresses — every stone is a child of another",
            "Generics-erasure buttresses (phantom at compile, gone at runtime)",
            "Annotation flying-buttresses across the aisle of metadata",
        ],
        "stained_glass": ["#f89820", "#5382a1", "#ffffff", "#000000"],
        "gargoyles": [
            "the Verbose-Reef Gargoyle (boilerplate-heavy)",
            "the NullPointerException Gargoyle (still ever-present)",
            "the Slow-Startup Gargoyle (cold JVM)",
        ],
        "bell_tower": "Group-flash (2) every 10 s — write once, run anywhere",
        "bell_cadence": "Group-Flash (2) every 10 s",
        "rose_window": "The Class Rose — every object descends from Object",
        "vaulted_ceiling": "Interface-vault — every ceiling is an abstract contract",
        "foundation": "JVM bedrock (ancient, deep, multi-versioned)",
        "architects": "James Gosling → Sun → Oracle → OpenJDK community",
        "construction_log": [
            "1991 — Sun's Green Project lays the cornerstone",
            "1995 — First public service held — Java 1.0a",
            "1998 — Java 2 (J2SE) re-points the entire nave",
            "2004 — Generics rose-window installed",
            "2014 — Lambda expressions reshape the vault",
            "2017 — var (local type inference) reaches the deck",
            "2021 — Records & sealed classes shore up the gargoyles",
            "2024 — Virtual threads loom large in the bell tower",
        ],
        "pilgrimage_count": 90,
        "light_intensity": 70,
        "height_m": 168,
        "alignment_deg": 135,
        "emoji": "☕",
        "stone": "Classical class-hierarchy marble, very load-bearing",
    },
    "C/C++": {
        "name": "C/C++",
        "diocese": "Diocese of Bare Metal",
        "built": 1969,
        "completed": 1985,
        "style": "Original Romanesque (you can see the chisel marks)",
        "floor_plan": "Original load-bearing plan — no automatic lifeguards",
        "nave": "Pointer-Nave — raw flame, handle with care",
        "nave_length_m": 220,
        "transepts": [
            "GCC / Clang (north — the workshop of the cathedral)",
            "glibc / STL (south — the relics of the standard library)",
            "OS kernels (chancel — the operating-system cloister)",
        ],
        "flying_buttresses": [
            "Pointer-arithmetic buttresses — raw, manual, exact",
            "Template-macro flying-buttresses (C++) — every shape can be built",
            "Const-correctness buttresses over the variable-courtyard",
        ],
        "stained_glass": ["#555555", "#00599c", "#a8b9cc", "#f34b7d"],
        "gargoyles": [
            "the Segfault Gargoyle (no guardrails)",
            "the Undefined-Behaviour Gargoyle",
            "the Manual-Memory Gargoyle (you own every leak)",
        ],
        "bell_tower": "Morse beacon — classic, no automation, the keeper winds it",
        "bell_cadence": "Morse Beacon every 5 s",
        "rose_window": "The Pointer Rose — you look directly at the light",
        "vaulted_ceiling": "Template-vault (C++) / no vault (C) — every ceiling is a choice",
        "foundation": "Hand-laid native bedrock (assembly under the floor)",
        "architects": "Dennis Ritchie → Brian Kernighan → Bjarne Stroustrup → ISO C/C++ committees",
        "construction_log": [
            "1969 — Dennis Ritchie lays the cornerstone at Bell Labs",
            "1972 — C consecrated — first public service",
            "1979 — Bjarne Stroustrup adds C++ classes to the nave",
            "1989 — ANSI C stabilises the foundation",
            "2011 — C++11 re-points the entire rose window",
            "2017/2020 — C++17/20 concepts, ranges, coroutines arrive",
            "2023 — C23 closes gaps in the C nave",
            "2024 — Carbon experiments as a side-chapel on C++'s foundation",
        ],
        "pilgrimage_count": 95,
        "light_intensity": 60,
        "height_m": 220,
        "alignment_deg": 250,
        "emoji": "⚙️",
        "stone": "Original-stack granite (you can see the chisel marks)",
    },
}


# ── Rotation helpers ──────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    """Load language_rotation.json from the workspace root."""
    if not os.path.exists(ROTATION_FILE):
        return {
            "languages": list(CATHEDRALS.keys()),
            "current_index": 0,
            "last_language": None,
            "updated_at": None,
        }
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    """Persist language_rotation.json."""
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_current_language() -> str:
    """Return the language at the rotation's current index."""
    rot = load_rotation()
    langs = rot.get("languages", list(CATHEDRALS.keys()))
    idx = rot.get("current_index", 0) % len(langs)
    return langs[idx]


def advance_rotation() -> Tuple[str, str]:
    """
    Advance the rotation by one step and persist.
    Returns (previous_language, next_language).
    """
    rot = load_rotation()
    langs = rot.get("languages", list(CATHEDRALS.keys()))
    idx = rot.get("current_index", 0) % len(langs)
    prev = langs[idx]
    nxt = langs[(idx + 1) % len(langs)]

    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz).isoformat(timespec="seconds")

    new_rot = {
        "languages": langs,
        "current_index": (idx + 1) % len(langs),
        "last_language": prev,
        "updated_at": now,
    }
    save_rotation(new_rot)
    return prev, nxt


# ── Cathedral rendering ──────────────────────────────────────────────────────

# A simple set of stone glyphs for ASCII renderings
_STONES = ["▒", "▓", "█"]
_GARGOYLE_GLYPHS = ["◬", "⟁", "▲", "◆", "✸"]
_PILLAR = "│"
_ROOF = "╱╲"


def _ascii_plan(style: str, width: int = 26) -> List[str]:
    """Render a small ASCII floor plan."""
    rows = max(7, min(14, width // 2))
    lines: List[str] = []
    lines.append("       /\\       ")
    lines.append("      /  \\      ")
    lines.append("     /    \\     ")
    lines.append("    +______+    ")
    lines.append("    |      |    ")
    # nave
    for _ in range(rows):
        lines.append("    |  ||  |    ")
    lines.append("    +______+    ")
    # transepts
    lines.append("   ---    ---   ")
    lines.append("  |   |  |   |  ")
    lines.append("  +---+  +---+  ")
    lines.append("    |      |    ")
    lines.append("  bell   bell   ")
    return lines


def _ascii_stained_glass(palette: List[str]) -> str:
    """Render a small stained-glass strip from a color palette."""
    glyphs = ["◆", "◇", "✦", "✧", "●"]
    out = []
    for i, color in enumerate(palette):
        out.append(f"{glyphs[i % len(glyphs)]} {color}")
    return "  ".join(out)


def _gargoyle_strip(gargoyles: List[str]) -> str:
    """Turn the gargoyle list into a small ASCII warning strip."""
    if not gargoyles:
        return "  (no gargoyles — smooth sailing)"
    return "  " + " ".join(g for g in _GARGOYLE_GLYPHS[: len(gargoyles)])


def _light_quality(pilgrims: int, height_m: int, light_intensity: int) -> str:
    """Combine a few metrics into a coarse 'light through the rose window'."""
    score = (pilgrims + height_m // 4 + light_intensity) // 3
    bars = max(1, min(8, score // 12))
    return "▁▂▃▄▅▆▇█"[:bars] + "·" * (8 - bars) + f"  ({score}/100)"


# ── Snippet-based "which cathedral fits?" heuristic ──────────────────────────

_SNIPPET_SIGNALS = {
    "Rust":     [r"\bfn\s+main\b", r"->\s*&\w+", r"\bimpl\b", r"\blet\s+mut\b",
                r"\bResult<", r"\bOption<", r"\bunwrap\(\)", r"\bVec<"],
    "Go":       [r"\bfunc\s+\w+", r"\bpackage\s+main\b", r"\bgo\s+\w+\(",
                r"\bchan\s+\w+", r"\:=\s*", r"\bdefer\s+", r"\bgoroutine\b"],
    "Swift":    [r"\bvar\s+\w+\s*:\s*\w+", r"\bguard\s+let\b", r"\?\?",
                r"\bprotocol\s+\w+", r"\b@IBOutlet\b", r"\bextension\s+\w+"],
    "Kotlin":   [r"\bfun\s+\w+\s*\(", r"\bval\s+\w+", r"\?\.", r"\bdata\s+class\b",
                r"\bcompanion\s+object\b", r"\bcoroutine\b", r"\blaunch\s*\{"],
    "TypeScript":[r"\binterface\s+\w+", r"\:\s*\w+\s*=", r"\bas\s+\w+",
                 r"\benum\s+\w+", r"\breadonly\b", r"\btype\s+\w+\s*="],
    "JavaScript":[r"\bfunction\s+\w+", r"\bconst\s+\w+\s*=", r"=>",
                 r"\bawait\s+", r"\bPromise\b", r"\bconsole\.log\b"],
    "Java":     [r"\bpublic\s+class\b", r"\bstatic\s+void\s+main\b",
                r"\bSystem\.out\.print", r"\bextends\s+\w+", r"\bnew\s+\w+\("],
    "C/C++":    [r"#include\s*<", r"\bint\s+main\s*\(", r"\bprintf\s*\(",
                r"\bmalloc\s*\(", r"\bfree\s*\(", r"std::", r"\bnullptr\b"],
}


def _score_snippet(snippet: str) -> Dict[str, int]:
    """Return per-language match scores for a code snippet (regex-based)."""
    import re
    scores: Dict[str, int] = {lang: 0 for lang in _SNIPPET_SIGNALS}
    if not snippet:
        return scores
    for lang, patterns in _SNIPPET_SIGNALS.items():
        for pat in patterns:
            if re.search(pat, snippet):
                scores[lang] += 1
    return scores


# ── Public API ────────────────────────────────────────────────────────────────

def _cathedral_report(lang: str, snippet: str = "") -> Dict[str, Any]:
    """Build the full report for one cathedral."""
    c = CATHEDRALS.get(lang)
    if c is None:
        return {"error": f"unknown language: {lang}"}

    rot = load_rotation()
    idx = rot.get("current_index", 0)
    langs = rot.get("languages", list(CATHEDRALS.keys()))

    snippet_top = []
    if snippet:
        ranked = sorted(
            _score_snippet(snippet).items(),
            key=lambda kv: kv[1],
            reverse=True,
        )
        snippet_top = [
            {"language": k, "score": v}
            for k, v in ranked if v > 0
        ][:5]

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": lang,
        "rotation": {
            "position": langs.index(lang) if lang in langs else -1,
            "current_index": idx,
            "total_cathedrals": len(langs),
            "is_current": langs[idx] == lang,
        },
        "cathedral": {
            "name": c["name"],
            "diocese": c["diocese"],
            "built": c["built"],
            "completed": c["completed"],
            "age_years": max(0, datetime.now().year - c["built"]),
            "style": c["style"],
            "stone": c["stone"],
            "height_m": c["height_m"],
        },
        "floor_plan": {
            "blueprint": c["floor_plan"],
            "nave": c["nave"],
            "nave_length_m": c["nave_length_m"],
            "transepts": c["transepts"],
            "vaulted_ceiling": c["vaulted_ceiling"],
        },
        "structure": {
            "flying_buttresses": c["flying_buttresses"],
            "foundation": c["foundation"],
            "rose_window": c["rose_window"],
        },
        "bell_tower": {
            "tower": c["bell_tower"],
            "cadence": c["bell_cadence"],
        },
        "ornament": {
            "stained_glass_palette": c["stained_glass"],
            "stained_glass_strip": _ascii_stained_glass(c["stained_glass"]),
        },
        "gargoyles": {
            "shadows": c["gargoyles"],
            "warning_strip": _gargoyle_strip(c["gargoyles"]),
        },
        "architects": {
            "lineage": c["architects"],
            "construction_log": c["construction_log"],
        },
        "visitors": {
            "pilgrimage_count": c["pilgrimage_count"],
            "light_intensity": c["light_intensity"],
            "alignment_compass": c["alignment_deg"],
            "emoji": c["emoji"],
            "light_quality_bar": _light_quality(
                c["pilgrimage_count"], c["height_m"], c["light_intensity"]
            ),
        },
        "ascii_art": {
            "floor_plan": _ascii_plan(c["style"]),
        },
        "snippet_homing": {
            "input_chars": len(snippet),
            "top_matches": snippet_top,
        },
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(
            timespec="seconds"
        ),
    }


def cathedral_report(
    language: Optional[str] = None,
    snippet: str = "",
    advance: bool = True,
) -> Dict[str, Any]:
    """
    Build a cathedral report.

    If `language` is None, the rotation's current language is used.
    If `advance` is True, the rotation index is bumped after building.
    """
    rot = load_rotation()
    langs = rot.get("languages", list(CATHEDRALS.keys()))

    if language is None:
        idx = rot.get("current_index", 0) % len(langs)
        language = langs[idx]
    elif language not in CATHEDRALS:
        # Try fuzzy match
        for k in CATHEDRALS:
            if k.lower() == language.lower():
                language = k
                break
        else:
            return {"error": f"unknown language: {language}"}

    report = _cathedral_report(language, snippet=snippet)

    if advance:
        prev, nxt = advance_rotation()
        report["rotation"]["advanced"] = {
            "from": prev,
            "to": nxt,
        }

    return report


def cathedral_tour() -> List[Dict[str, Any]]:
    """Visit every cathedral in rotation order (without advancing)."""
    rot = load_rotation()
    langs = rot.get("languages", list(CATHEDRALS.keys()))
    return [
        _cathedral_report(lang) for lang in langs
    ]


def side_by_side_naves(lang_a: str, lang_b: str) -> Dict[str, Any]:
    """
    Compare two cathedrals side-by-side and produce a recommendation:
    which is taller, which has more pilgrims, which lets in more light, etc.
    """
    if lang_a not in CATHEDRALS:
        return {"error": f"unknown language: {lang_a}"}
    if lang_b not in CATHEDRALS:
        return {"error": f"unknown language: {lang_b}"}
    a, b = CATHEDRALS[lang_a], CATHEDRALS[lang_b]

    age_a = max(0, datetime.now().year - a["built"])
    age_b = max(0, datetime.now().year - b["built"])

    metrics_pairs = [
        ("height_m", a["height_m"], b["height_m"]),
        ("nave_length_m", a["nave_length_m"], b["nave_length_m"]),
        ("pilgrimage_count", a["pilgrimage_count"], b["pilgrimage_count"]),
        ("light_intensity", a["light_intensity"], b["light_intensity"]),
        ("age_years", age_a, age_b),
    ]
    comparison: Dict[str, Any] = {}
    for m, av, bv in metrics_pairs:
        winner = lang_a if av > bv else (lang_b if bv > av else "tie")
        comparison[m] = {lang_a: av, lang_b: bv, "leader": winner}

    diff = abs(a["alignment_deg"] - b["alignment_deg"]) % 360
    diff = min(diff, 360 - diff)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "a": lang_a,
        "b": lang_b,
        "metrics": comparison,
        "alignment_diff_deg": diff,
        "shared_transepts": sorted(
            set(a["transepts"]) & set(b["transepts"])
        ),
        "unique_to_a": sorted(set(a["transepts"]) - set(b["transepts"])),
        "unique_to_b": sorted(set(b["transepts"]) - set(a["transepts"])),
        "shared_gargoyles": sorted(
            set(a["gargoyles"]) & set(b["gargoyles"])
        ),
    }


# ── Self-tests ────────────────────────────────────────────────────────────────

def _t(name: str, cond: bool, detail: str = "") -> bool:
    """Run a single test, return True if pass, else print & return False."""
    if cond:
        return True
    print(f"  FAIL: {name} {detail}")
    return False


def run_tests() -> List[str]:
    """Run a small self-test battery, returning a list of failure messages."""
    failures: List[str] = []

    # 1. CATHEDRALS covers every language in the rotation
    rot = load_rotation()
    langs = rot["languages"]
    for lang in langs:
        if not _t(f"catalogue has {lang}", lang in CATHEDRALS):
            failures.append(f"missing cathedral: {lang}")

    # 2. Each cathedral has the required fields
    required = [
        "name", "diocese", "built", "completed", "style",
        "floor_plan", "nave", "nave_length_m", "transepts",
        "flying_buttresses", "stained_glass", "gargoyles",
        "bell_tower", "bell_cadence", "rose_window", "vaulted_ceiling",
        "foundation", "architects", "construction_log",
        "pilgrimage_count", "light_intensity", "height_m",
        "alignment_deg", "emoji", "stone",
    ]
    for lang, c in CATHEDRALS.items():
        for f in required:
            if not _t(f"{lang} has field {f}", f in c, f"got keys: {sorted(c)}"):
                failures.append(f"{lang} missing field: {f}")

    # 3. Report generation works for every language
    for lang in langs:
        rep = cathedral_report(language=lang, snippet="", advance=False)
        if not _t(
            f"report for {lang}", rep.get("language") == lang
        ):
            failures.append(f"bad report: {lang}")

    # 4. Unknown language returns an error, not a crash
    rep = cathedral_report(language="Klingon", advance=False)
    if not _t("unknown language returns error", "error" in rep):
        failures.append("unknown language did not return error")

    # 5. Cross-cathedral comparison works
    cb = side_by_side_naves("Rust", "Go")
    if not _t("side_by_side_naves metrics present", "metrics" in cb):
        failures.append("side_by_side_naves missing metrics")
    if not _t(
        "side_by_side_naves reports a leader for height_m",
        "leader" in cb.get("metrics", {}).get("height_m", {}),
    ):
        failures.append("side_by_side_naves missing leader")

    # 6. Tour returns one entry per language
    tour = cathedral_tour()
    if not _t(
        "tour length matches rotation",
        len(tour) == len(langs),
        f"got {len(tour)} expected {len(langs)}",
    ):
        failures.append("bad tour length")

    # 7. Rotation advance moves forward and persists
    rot0 = load_rotation()
    idx0 = rot0["current_index"]
    prev, nxt = advance_rotation()
    rot1 = load_rotation()
    if not _t(
        "rotation advances",
        rot1["current_index"] == (idx0 + 1) % len(rot1["languages"]),
        f"{idx0} -> {rot1['current_index']}",
    ):
        failures.append("rotation did not advance")
    # restore original index so we don't disturb state
    rot1["current_index"] = idx0
    rot1["last_language"] = rot0.get("last_language")
    save_rotation(rot1)

    # 8. Snippet scoring returns non-zero for a Rust snippet
    rs = _score_snippet("fn main() { let mut v = Vec::new(); v.push(1); }")
    if not _t(
        "snippet scoring detects Rust",
        rs.get("Rust", 0) >= 2,
        f"got: {rs}",
    ):
        failures.append("snippet scoring wrong for Rust")

    # 9. ASCII floor plan renders without errors
    for lang in langs:
        rows = _ascii_plan(CATHEDRALS[lang]["style"])
        if not _t(
            f"ascii floor plan for {lang}",
            isinstance(rows, list) and len(rows) >= 7,
        ):
            failures.append(f"bad ascii floor plan for {lang}")

    # 10. Light-quality bar is a string with the right format
    bar = _light_quality(80, 160, 80)
    if not _t(
        "light quality bar contains (score)",
        isinstance(bar, str) and "/100)" in bar,
        f"got: {bar}",
    ):
        failures.append("bad light quality bar")

    # 11. Gargoyle strip handles empty list
    g = _gargoyle_strip([])
    if not _t("empty gargoyle list handled", "(no gargoyles" in g):
        failures.append("empty gargoyle list not handled")

    # 12. Stained glass strip has all palette entries
    strip = _ascii_stained_glass(["#fff", "#000", "#abc"])
    if not _t(
        "stained glass strip contains hex codes",
        "#fff" in strip and "#000" in strip and "#abc" in strip,
        f"got: {strip}",
    ):
        failures.append("bad stained glass strip")

    # 13. Built year is sane (all > 1950)
    for lang, c in CATHEDRALS.items():
        if not _t(
            f"{lang} built year sane",
            c["built"] > 1950,
            f"built={c['built']}",
        ):
            failures.append(f"{lang} built year is not sane")

    return failures


if __name__ == "__main__":
    failures = run_tests()
    if failures:
        print("FAIL")
        for f in failures:
            print(" -", f)
        raise SystemExit(1)
    print("OK — all cathedral self-tests passed ⛪")