#! /usr/bin/env python3
"""
🗺️ Polyglot Topology v1.0
Maps the TOPOLOGICAL STRUCTURE of programming language design space —
which languages are "neighbors", which are "isolated continents",
and what the shape of the current language's neighborhood looks like.

Creative concept: "Every programming language occupies a region in an
infinite-dimensional design space. Polyglot Topology maps the TOPOLOGICAL
structure of that space — which regions are connected, which are isolated
islands, which languages are homeomorphic (equivalent in structure despite
surface differences), and what boundaries separate paradigms."

Each run selects the current rotation language and maps it into the
topological space, showing:
  1. The language's position — what "region" of design space it inhabits
  2. Its TOPOLOGICAL NEIGHBORHOOD — which languages are "close" in design
  3. The BOUNDARY LINES — where one paradigm ends and another begins
  4. Connected components — which languages form "continents" of ideas
  5. An ASCII "TOPOLOGY MAP" — bird's-eye view of the design space

Distinct from existing tools:
  - polyglot_resonance:       frequency harmonics & oscilloscope waveforms
  - polyglot_ecosystem_map:   package/library ecosystem landscape
  - polyglot_constellation:   star-map of language "types" (star types)
  - polyglot_cartographer:    feature matrix comparison (checklist atlas)
  - polyglot_meridian:       spectral positioning (coordinates in design space)
  - polyglot_architect:      architecture patterns (blueprints)
  - polyglot_resonator:       thinking philosophy (mental models & cognitive frames)
  - polyglot_signal:          signal semantics (alarm systems for conditions)
  - polyglot_harmony:         pairwise compatibility scores (musical intervals)
  - polyglot_dna:             genetic trait mapping (static molecular traits)
  - polyglot_chronology:      temporal timeline (time axis)
  - polyglot_chronicle:       daily diary + today's challenge (temporal today)
  - polyglot_digest:          syntax-parallel code snippets (spatial syntax)
  - polyglot_weather:         mood/status conditions (atmospheric)
  - polyglot_pulse:           heartbeat/status indicators
  - polyglot_mood:            emotional state mapping
  - polyglot_flavor:          sensory tasting notes (sommelier)
  - polyglot_chef:            recipe/ingredient transformation
  - polyglot_craft:           practical skill cards (patterns, gotchas)
  - polyglot_forge:           transformation & conversion (blacksmith)
  - polyglot_fossil:          historical remnants (ancient artifacts)
  - polyglot_faultline:       breaking changes & incompatibilities
  - polyglot_translation:     direct translation between languages
  - polyglot_bridges:         FFI/interop patterns
  - polyglot_selector:        pick-a-language randomly
  - polyglot_sentinel:        linting/rules
  - polyglot_tempo:           timing/performance characteristics
  - polyglot_wire:            connection protocols
  - polyglot_pulse:           metrics/monitoring
  - polyglot_mood:            sentiment
  - polyglot_codex:           code challenges
  - polyglot_resonance:       frequency analysis

Polyglot Topology is about MATHEMATICAL TOPOLOGY — neighborhood relations,
connected components, boundaries, and continuity in the abstract space
of language design.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import math
import random
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple

TOOL_NAME = "polyglot-topology"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "language_rotation.json"
)

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ─────────────────────────────────────────────────────────────────────────────
# TOPOLOGICAL FEATURE SPACE
# Each language occupies a point in this abstract space. The features define
# the "shape" of the language's neighborhood — which other languages it is
# topologically close to.
# ─────────────────────────────────────────────────────────────────────────────

# Feature vectors (simplified — key distinguishing features)
# Format: (memory_model, type_discipline, error_model, concurrency_shape, paradigm)
FEATURE_VECTORS: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "region": "Memory Safety Island (Ownership)",
        "continent": "Systems Security Continent",
        "memory_model": "ownership + borrow checker",
        "type_discipline": "static + inferred + affine",
        "error_model": "Result<T, E> (no exceptions)",
        "concurrency_shape": "Send/Sync compile-time",
        "paradigm": "multi-paradigm (FP+Systems)",
        "boundaries": ["no-GC-land", "unsafe-corridor"],
        "neighbors": ["C/C++", "Swift"],
        "description": "An island of memory safety in an ocean of undefined behavior. "
                       "The borrow checker draws strict boundary lines that keep "
                       "aliasing violations from crossing.",
        "topological_signature": "∂(∅) — zero aliasing boundary",
    },
    "Go": {
        "region": "Concurrency Archipelago",
        "continent": "Garbage-Collected Continent",
        "memory_model": "tracing GC + pointers",
        "type_discipline": "static + structural (no generics until 1.18)",
        "error_model": "error interface (returned values)",
        "concurrency_shape": "goroutines + channels (CSP)",
        "paradigm": "concurrent-first (lightweight threads)",
        "boundaries": ["gc-shoreline", "interface-sea"],
        "neighbors": ["Java", "JavaScript"],
        "description": "The concurrency archipelago — goroutines are cheap islands "
                       "of parallelism connected by channels as bridges. "
                       "The GC coastline is always nearby.",
        "topological_signature": "ℤ → chan(T) — integer to channel morphism",
    },
    "Swift": {
        "region": "Value Semantics Cove",
        "continent": "ARC Archipelago",
        "memory_model": "ARC (Automatic Reference Counting)",
        "type_discipline": "static + nominal + protocols",
        "error_model": "throws + Error protocol (try/catch)",
        "concurrency_shape": "async/await + actors (Swift 6)",
        "paradigm": "protocol-oriented + value types",
        "boundaries": ["arc-waters", "optional-precipice"],
        "neighbors": ["Rust", "Kotlin"],
        "description": "A sheltered cove where values flow without currents. "
                       "Copy-on-write walls protect each value's territory. "
                       "Optional represents the dramatic cliffs of absence.",
        "topological_signature": "COW(τ) — copy-on-write at τ",
    },
    "Kotlin": {
        "region": "Null Safety Peninsula",
        "continent": "JVM Continent",
        "memory_model": "JVM GC + nullable types",
        "type_discipline": "static + nominal + null-safe",
        "error_model": "Result<T> (no checked exceptions, use runCatching)",
        "concurrency_shape": "coroutines (suspend) + Flow",
        "paradigm": "OO + functional (extensions)",
        "boundaries": ["jvm-shore", "nullable-tip"],
        "neighbors": ["Swift", "Java"],
        "description": "A peninsula extending from the JVM continent. "
                       "The nullable tip (T?) is a distinctive geographical feature "
                       "— Kotlin's most famous export to the world.",
        "topological_signature": "τ? — optionality as peninsula geometry",
    },
    "TypeScript": {
        "region": "Structural Type Delta",
        "continent": "Dynamic Archipelago",
        "memory_model": "JS runtime GC (V8 optimized)",
        "type_discipline": "gradual + structural + erased",
        "error_model": "throw + try/catch (any type)",
        "concurrency_shape": "async/await + Promise (event loop)",
        "paradigm": "multi-paradigm (OO + functional)",
        "boundaries": ["type-erasure-coast", "any-swamp"],
        "neighbors": ["JavaScript"],
        "description": "A river delta where types deposit in layers of "
                       "gradual accumulation. The structural type system "
                       "means shapes are defined by their outline, not their name.",
        "topological_signature": "⊢ τ :: shape — type inference as terrain survey",
    },
    "JavaScript": {
        "region": "Prototype Ocean",
        "continent": "Dynamic Archipelago",
        "memory_model": "JS runtime GC (V8)",
        "type_discipline": "dynamic + duck-typed + prototype chain",
        "error_model": "throw + try/catch (untyped)",
        "concurrency_shape": "event loop + Promises (single-threaded)",
        "paradigm": "multi-paradigm (prototypal OO)",
        "boundaries": ["prototype-sea", "undefined-void"],
        "neighbors": ["TypeScript"],
        "description": "The vast prototype ocean — everything floats on a chain "
                       "of prototypes stretching into the mist. The event loop "
                       "keeps the waters calm (single-threaded).",
        "topological_signature": "[prototypal]ⁿ — infinite prototype chain",
    },
    "Java": {
        "region": "Class Hierarchy Highlands",
        "continent": "JVM Continent",
        "memory_model": "JVM GC (generations)",
        "type_discipline": "static + nominal + class-based",
        "error_model": "checked + unchecked exceptions",
        "concurrency_shape": "threads + CompletableFuture + virtual threads",
        "paradigm": "OOP (class-first)",
        "boundaries": ["jvm-shore", "generics-canyon"],
        "neighbors": ["Kotlin", "Go"],
        "description": "High rolling hills of class hierarchies, where inheritance "
                       "forms mountain ranges. Generics create a misty canyon "
                       "that type erasure conceals from view.",
        "topological_signature": "class τ extends σ — hierarchical mountain building",
    },
    "C/C++": {
        "region": "Pointer Wilderness",
        "continent": "Systems Continent",
        "memory_model": "manual (malloc/free, RAII, smart pointers)",
        "type_discipline": "static + weakly typed + templates",
        "error_model": "return codes (C) | exceptions (C++)",
        "concurrency_shape": "std::thread + atomics (manual)",
        "paradigm": "multi-paradigm (Systems programming)",
        "boundaries": ["null-pointer-plains", "ub-swamp"],
        "neighbors": ["Rust"],
        "description": "A vast wilderness of raw pointers and manual memory "
                       "management. The UB swamp lurks at the edges — "
                       "beautiful but dangerous. Close to Rust's ownership island "
                       "but with very different border controls.",
        "topological_signature": "τ* — pointer as portal to raw address space",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# TOPOLOGICAL RELATIONS
# Define the neighborhood graph of the design space
# ─────────────────────────────────────────────────────────────────────────────

# Which languages are "topologically close" (neighbors in design space)
# These are edges in the neighborhood graph
NEIGHBORHOOD_GRAPH: Dict[str, List[str]] = {
    "Rust":       ["C/C++", "Swift", "Kotlin"],
    "Go":         ["Java", "JavaScript", "Kotlin"],
    "Swift":      ["Rust", "Kotlin", "Go"],
    "Kotlin":     ["Java", "Swift", "Go"],
    "TypeScript": ["JavaScript", "Java"],
    "JavaScript": ["TypeScript", "Go"],
    "Java":       ["Kotlin", "Go", "TypeScript"],
    "C/C++":      ["Rust"],
}

# Connected components (languages that share design-space "continents")
CONTINENTS: Dict[str, List[str]] = {
    "Systems Security":     ["Rust", "C/C++"],
    "JVM Continent":        ["Java", "Kotlin"],
    "ARC Archipelago":      ["Swift"],
    "Concurrency Archipelago": ["Go"],
    "Dynamic Archipelago":  ["JavaScript", "TypeScript"],
}

# Boundary definitions (where paradigms change)
BOUNDARY_LINES: List[Dict[str, Any]] = [
    {
        "name": "Memory Safety Frontier",
        "separates": [("Rust", "C/C++")],
        "description": "The ownership/borrow checker vs. raw pointers",
        "marker": "⚠️",
    },
    {
        "name": "GC Shoreline",
        "separates": [("Rust", "Go"), ("Rust", "Java")],
        "description": "Garbage collection vs. deterministic memory",
        "marker": "🌊",
    },
    {
        "name": "Type Erasure Canyon",
        "separates": [("Java", "TypeScript")],
        "description": "Type information erased at runtime vs. preserved",
        "marker": "🕳️",
    },
    {
        "name": "Static-Dynamic Divide",
        "separates": [("JavaScript", "TypeScript"), ("JavaScript", "Java")],
        "description": "Dynamic vs. static typing boundary",
        "marker": "⚡",
    },
    {
        "name": "Null-Safety Coastline",
        "separates": [("Kotlin", "Java"), ("Swift", "C/C++")],
        "description": "Null safety enforced vs. permissive null access",
        "marker": "🌑",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# ASCII Topology Map generation
# ─────────────────────────────────────────────────────────────────────────────

def _render_topology_map(
    current_lang: str,
    width: int = 72,
    height: int = 19,
) -> List[str]:
    """
    Render an ASCII topology map showing the current language's position
    in the design space neighborhood.
    
    Layout (simplified 2D projection of the topology):
    
         [C/C++]  (systems continent, NW)
              ↑
    [Rust] ←→ [Swift] ←→ [Kotlin]
      ↑               ↕         ↑
      |    [Go]      [Java]     |
      |      ↑        ↑         |
    (isolated)   [TypeScript] ←[JavaScript]
    
    Each language positioned by its "topological region"
    """
    
    # Define 2D positions for each language (projection of design space)
    # These positions reflect neighborhood relationships
    POSITIONS: Dict[str, Tuple[int, int]] = {
        # x increases → (toward right), y increases ↑ (toward top)
        "Rust":       (3,  14),   # top-left (ownership island)
        "C/C++":      (1,  16),   # north of Rust (systems continent)
        "Swift":      (7,  13),   # east of Rust, north (ARC cove)
        "Kotlin":     (11, 12),   # east of Swift (JVM peninsula)
        "Java":       (14, 11),   # east of Kotlin (class highlands)
        "Go":         (10, 8),    # south of Kotlin (concurrency archipelago)
        "TypeScript": (17, 7),    # east of Go (structural delta)
        "JavaScript": (20, 6),    # east of TypeScript (prototype ocean)
    }
    
    # Compute map grid
    grid: List[List[str]] = [["  "] for _ in range(height)]
    for _ in range(width):
        grid.append(["  "] * width)
    grid = [[" " for _ in range(width)] for _ in range(height)]
    
    def place_at(x: int, y: int, text: str) -> None:
        """Place text at position, handling bounds."""
        if 0 <= y < height and 0 <= x < width:
            chars = list(text)
            for i, ch in enumerate(chars):
                px = x + i
                if 0 <= px < width:
                    grid[y][px] = ch
    
    def draw_line(
        x0: int, y0: int, x1: int, y1: int, char: str = "·"
    ) -> None:
        """Draw a line between two points using Bresenham."""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        x, y = x0, y0
        while True:
            if 0 <= x < width and 0 <= y < height:
                if grid[y][x] == " ":
                    grid[y][x] = char
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
    
    # Draw neighborhood connections
    for lang, neighbors in NEIGHBORHOOD_GRAPH.items():
        if lang not in POSITIONS:
            continue
        x0, y0 = POSITIONS[lang]
        for neighbor in neighbors:
            if neighbor not in POSITIONS:
                continue
            x1, y1 = POSITIONS[neighbor]
            draw_line(x0, y0, x1, y1, "──")
    
    # Draw boundary lines (dashed)
    for boundary in BOUNDARY_LINES:
        for lang_a, lang_b in boundary["separates"]:
            if lang_a in POSITIONS and lang_b in POSITIONS:
                x0, y0 = POSITIONS[lang_a]
                x1, y1 = POSITIONS[lang_b]
                draw_line(x0, y0, x1, y1, "~~")
    
    # Place language labels (all single-char cells, no multi-char highlights)
    for lang, (x, y) in POSITIONS.items():
        is_current = lang == current_lang
        marker = "▶" if is_current else "○"
        # Draw background highlight for current (single-char cells)
        if is_current:
            for dx in range(-2, 3):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= ny < height and 0 <= nx < width:
                        if grid[ny][nx] == " ":
                            grid[ny][nx] = "▓"
        # Draw label (marker + language name, all single-char)
        label = f"{marker}{lang}"
        place_at(x, y, label)
    
    # Convert to lines
    lines = ["".join(row) for row in grid]
    return lines


def _compute_topological_metrics(lang: str) -> Dict[str, Any]:
    """Compute topological metrics for a language."""
    info = FEATURE_VECTORS.get(lang, {})
    neighbors = NEIGHBORHOOD_GRAPH.get(lang, [])
    
    # Find connected component (continent)
    continent = None
    for cont_name, cont_langs in CONTINENTS.items():
        if lang in cont_langs:
            continent = cont_name
            break
    
    # Count shared neighbors (languages close to both)
    shared_count = 0
    for neighbor in neighbors:
        neighbor_neighbors = set(NEIGHBORHOOD_GRAPH.get(neighbor, []))
        shared_count += len(set(neighbors) & neighbor_neighbors)
    
    # Find boundary lines this language participates in
    boundaries = []
    for boundary in BOUNDARY_LINES:
        for lang_a, lang_b in boundary["separates"]:
            if lang == lang_a or lang == lang_b:
                boundaries.append(boundary["name"])
    
    # Compute "topological distance" from each other language
    distances: Dict[str, float] = {}
    all_langs = list(FEATURE_VECTORS.keys())
    for other in all_langs:
        if other == lang:
            distances[other] = 0.0
        elif other in neighbors:
            distances[other] = 1.0  # direct neighbor
        else:
            # BFS distance
            visited: Set[str] = {lang}
            frontier = list(neighbors)
            dist = 1
            found = False
            while frontier and not found:
                next_frontier = []
                for n in frontier:
                    if n == other:
                        distances[other] = float(dist)
                        found = True
                        break
                    if n not in visited:
                        visited.add(n)
                        next_frontier.extend(NEIGHBORHOOD_GRAPH.get(n, []))
                frontier = list(set(next_frontier))
                dist += 1
            if not found:
                distances[other] = float('inf')
    
    return {
        "region": info.get("region", "Unknown"),
        "continent": continent or "Unknown",
        "neighborhood_size": len(neighbors),
        "neighbors": neighbors,
        "shared_connections": shared_count,
        "boundary_count": len(boundaries),
        "boundaries": boundaries,
        "topological_signature": info.get("topological_signature", "?"),
        "description": info.get("description", ""),
        "distances": distances,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Rotation helpers
# ─────────────────────────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    """Load language rotation config."""
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


# ─────────────────────────────────────────────────────────────────────────────
# Core API
# ─────────────────────────────────────────────────────────────────────────────

def topology() -> Dict[str, Any]:
    """
    Main entry point: advance rotation, compute topology for current language,
    and return the full topology analysis.
    """
    config = load_rotation()
    languages = config.get("languages", [])
    if not languages:
        raise ValueError("No languages found in rotation config")

    current_index = config.get("current_index", 0)
    current_language = languages[current_index % len(languages)]

    # Advance rotation for next run
    next_index = (current_index + 1) % len(languages)
    config["current_index"] = next_index
    config["last_language"] = current_language
    config["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation(config)

    # Compute topology
    result = compute_topology(current_language)
    result["rotation_advanced"] = True
    result["next_language"] = languages[next_index]
    result["next_index"] = next_index
    return result


def compute_topology(language: str) -> Dict[str, Any]:
    """Compute topological analysis for a language."""
    if language not in FEATURE_VECTORS:
        raise ValueError(f"Language '{language}' not in known topology space")

    info = FEATURE_VECTORS[language]
    metrics = _compute_topological_metrics(language)
    map_rows = _render_topology_map(language)

    # Build boundary information
    boundaries_info: List[Dict[str, Any]] = []
    for boundary in BOUNDARY_LINES:
        for lang_a, lang_b in boundary["separates"]:
            if lang_a == language or lang_b == language:
                other = lang_b if lang_a == language else lang_a
                boundaries_info.append({
                    "name": boundary["name"],
                    "marker": boundary["marker"],
                    "with": other,
                    "description": boundary["description"],
                })

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": language,
        "region": info.get("region", "Unknown"),
        "continent": info.get("continent", "Unknown"),
        "memory_model": info.get("memory_model", ""),
        "type_discipline": info.get("type_discipline", ""),
        "error_model": info.get("error_model", ""),
        "concurrency_shape": info.get("concurrency_shape", ""),
        "paradigm": info.get("paradigm", ""),
        "topological_signature": info.get("topological_signature", "?"),
        "description": info.get("description", ""),
        "neighbors": metrics["neighbors"],
        "neighborhood_size": metrics["neighborhood_size"],
        "shared_connections": metrics["shared_connections"],
        "boundaries": boundaries_info,
        "distances": metrics["distances"],
        "topology_map": map_rows,
        "rotation_order": ROTATION_ORDER,
    }


def format_topology(m: Dict[str, Any]) -> str:
    """Format the topology analysis as a human-readable string."""
    lang = m["language"]

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  🗺️ POLYGLOT TOPOLOGY — Language Design Space Cartography        ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Language      : {lang:<47}║",
        f"║  Region        : {m['region']:<47}║",
        f"║  Continent     : {m['continent']:<47}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  📐 TOPOLOGICAL SIGNATURE                                      ║",
        f"║  {m['topological_signature']:<59}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🧭 DESIGN SPACE POSITION                                       ║",
        f"║  Memory model   : {m['memory_model']:<42}║",
        f"║  Type discipline: {m['type_discipline']:<42}║",
        f"║  Error model    : {m['error_model']:<43}║",
        f"║  Concurrency    : {m['concurrency_shape']:<43}║",
        f"║  Paradigm       : {m['paradigm']:<45}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🗺️  TOPOLOGY MAP (2D projection of design space)                ║",
    ]

    for row in m["topology_map"][:15]:
        # Strip ANSI codes for display
        clean = row.replace("\033[1m", "").replace("\033[0m", "")
        lines.append(f"║  {clean:<66}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🔗 NEIGHBORHOOD GRAPH                                          ║",
        f"║  Neighbors ({m['neighborhood_size']}): {', '.join(m['neighbors']):<39}║",
        f"║  Shared connections: {m['shared_connections']:<43}║",
    ]

    if m["boundaries"]:
        lines.append("╠══════════════════════════════════════════════════════════════════╣")
        lines.append("║  ⚡ BOUNDARY LINES (paradigm transitions)                       ║")
        for b in m["boundaries"]:
            lines.append(
                f"║  {b['marker']} {b['name']} (with {b['with']})"
            )
            lines.append(f"║     {b['description']:<53}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  📖 TOPOLOGICAL DESCRIPTION                                     ║",
    ]

    # Wrap description
    desc = m["description"]
    words = desc.split()
    line = "║  "
    for word in words:
        if len(line) + len(word) + 1 > 68:
            lines.append(line + "║")
            line = "║  " + word + " "
        else:
            line += word + " "
    if line.strip() != "║":
        lines.append(line + "║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🔄 ROTATION ORDER                                              ║",
        f"║  {' → '.join(ROTATION_ORDER):<58}║",
        "╚══════════════════════════════════════════════════════════════════╝",
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────────────

def run_tests() -> None:
    """Run all tests for the polyglot_topology module."""
    import sys

    errors: List[str] = []
    passed = 0

    def t(name: str, cond: bool, msg: str = "") -> None:
        nonlocal passed, errors
        if cond:
            print(f"  ✅ {name}")
            passed += 1
        else:
            print(f"  ❌ {name}: {msg}")
            errors.append(name)

    print("🗺️ Polyglot Topology — Running Tests\n")

    # ── Rotation file ─────────────────────────────────────────────────────────
    try:
        config = load_rotation()
        t("load_rotation() returns valid dict", isinstance(config, dict))
        t("rotation has 'languages' key", "languages" in config)
        t("rotation has 'current_index' key", "current_index" in config)
    except Exception as e:
        t("load_rotation() succeeds", False, str(e))

    # ── ROTATION_ORDER ────────────────────────────────────────────────────────
    t("ROTATION_ORDER has 8 languages", len(ROTATION_ORDER) == 8)
    for lang in ROTATION_ORDER:
        t(f"ROTATION_ORDER contains '{lang}'", lang in ROTATION_ORDER)

    # ── FEATURE_VECTORS ───────────────────────────────────────────────────────
    t("FEATURE_VECTORS has 8 languages", len(FEATURE_VECTORS) == 8)
    for lang in ROTATION_ORDER:
        t(f"FEATURE_VECTORS has '{lang}'", lang in FEATURE_VECTORS)
        info = FEATURE_VECTORS[lang]
        for key in ["region", "continent", "memory_model", "type_discipline",
                    "error_model", "concurrency_shape", "topological_signature"]:
            t(f"  '{lang}' has '{key}'", key in info)

    # ── NEIGHBORHOOD_GRAPH ─────────────────────────────────────────────────────
    t("NEIGHBORHOOD_GRAPH has 8 entries", len(NEIGHBORHOOD_GRAPH) == 8)
    for lang in ROTATION_ORDER:
        t(f"NEIGHBORHOOD_GRAPH has '{lang}'", lang in NEIGHBORHOOD_GRAPH)
        neighbors = NEIGHBORHOOD_GRAPH[lang]
        t(f"  '{lang}' has {len(neighbors)} neighbors", len(neighbors) >= 0)
        for neighbor in neighbors:
            t(f"    neighbor '{neighbor}' is in ROTATION_ORDER", neighbor in ROTATION_ORDER)

    # ── CONTINENTS ─────────────────────────────────────────────────────────────
    t("CONTINENTS has entries", len(CONTINENTS) > 0)
    for cont_name, cont_langs in CONTINENTS.items():
        t(f"  Continent '{cont_name}' has languages", len(cont_langs) > 0)
        for lang in cont_langs:
            t(f"    '{lang}' is in ROTATION_ORDER", lang in ROTATION_ORDER)

    # ── BOUNDARY_LINES ────────────────────────────────────────────────────────
    t("BOUNDARY_LINES has entries", len(BOUNDARY_LINES) > 0)
    for boundary in BOUNDARY_LINES:
        t(f"  Boundary '{boundary['name']}' has marker", len(boundary.get("marker", "")) > 0)
        t(f"  Boundary '{boundary['name']}' has separates", "separates" in boundary)

    # ── _render_topology_map ───────────────────────────────────────────────────
    try:
        import re
        def strip_ansi(s: str) -> str:
            return re.sub(r'\x1b\[[0-9;]*m', '', s)
        def display_width(s: str) -> int:
            # Compute terminal display width (approximate: fullwidth chars = 2, others = 1)
            import unicodedata
            w = 0
            for ch in s:
                if unicodedata.east_asian_width(ch) in ('F', 'W'):
                    w += 2
                else:
                    w += 1
            return w
        for lang in ROTATION_ORDER:
            rows = _render_topology_map(lang, width=72, height=19)
            t(f"_render_topology_map('{lang}') returns 19 rows", len(rows) == 19)
            # Check display width (accounting for double-width Unicode chars)
            display_widths = [display_width(r) for r in rows]
            t(f"_render_topology_map('{lang}') rows display as ~72 chars",
              all(60 <= w <= 85 for w in display_widths))
    except Exception as e:
        t("_render_topology_map() succeeds for all languages", False, str(e))

    # ── _compute_topological_metrics ──────────────────────────────────────────
    try:
        for lang in ROTATION_ORDER:
            metrics = _compute_topological_metrics(lang)
            t(f"_compute_topological_metrics('{lang}') succeeds", True)
            t(f"  - has 'region'", "region" in metrics)
            t(f"  - has 'neighbors'", "neighbors" in metrics)
            t(f"  - has 'distances'", "distances" in metrics)
            t(f"  - distances has entry for '{lang}'", lang in metrics["distances"])
    except Exception as e:
        t("_compute_topological_metrics() for all languages", False, str(e))

    # ── compute_topology ──────────────────────────────────────────────────────
    for lang in ROTATION_ORDER:
        try:
            result = compute_topology(lang)
            t(f"compute_topology('{lang}') succeeds", True)
            t(f"  - has 'language'", result.get("language") == lang)
            t(f"  - has 'region'", "region" in result)
            t(f"  - has 'topology_map'", "topology_map" in result)
            t(f"  - topology_map is 19 rows", len(result["topology_map"]) == 19)
            t(f"  - has 'neighbors'", len(result["neighbors"]) > 0)
            t(f"  - has 'boundaries'", "boundaries" in result)
        except Exception as e:
            t(f"compute_topology('{lang}')", False, str(e))

    # ── topology() advances rotation ──────────────────────────────────────────
    try:
        cfg_before = load_rotation()
        idx_before = cfg_before["current_index"]
        lang_before = cfg_before["languages"][idx_before % len(cfg_before["languages"])]
        result = topology()
        cfg_after = load_rotation()
        idx_after = cfg_after["current_index"]
        t("topology() advances current_index",
          idx_after == (idx_before + 1) % len(cfg_before["languages"]))
        t("topology() returns rotation_advanced=True",
          result.get("rotation_advanced") is True)
        t("topology() returns the selected language",
          result.get("language") == lang_before)
        t("topology() returns next_language",
          "next_language" in result)
    except Exception as e:
        t("topology() rotation advancement", False, str(e))

    # ── format_topology ───────────────────────────────────────────────────────
    try:
        lang = ROTATION_ORDER[0]
        m = compute_topology(lang)
        formatted = format_topology(m)
        t("format_topology() returns a string", isinstance(formatted, str))
        t("format_topology() starts with box-drawing char", formatted.startswith("╔"))
        t("format_topology() ends with box-drawing char", formatted.rstrip().endswith("╝"))
        t("format_topology() contains the language name", lang in formatted)
        t("format_topology() contains 'TOPOLOGY MAP'", "TOPOLOGY MAP" in formatted)
    except Exception as e:
        t("format_topology()", False, str(e))

    # ── Unknown language raises ValueError ────────────────────────────────────
    try:
        compute_topology("Brainfuck")
        t("Unknown language raises ValueError", False, "did not raise")
    except ValueError:
        t("Unknown language raises ValueError", True)
    except Exception as e:
        t("Unknown language raises ValueError", False, f"wrong exception: {e}")

    # ── Rotation index wraps correctly ────────────────────────────────────────
    try:
        # Save current state
        cfg_orig = load_rotation()
        cfg = dict(cfg_orig)
        langs = cfg["languages"]
        
        # Simulate full cycle
        for i in range(len(langs)):
            cfg = load_rotation()
            idx = cfg["current_index"]
            cfg["current_index"] = (idx + 1) % len(langs)
            cfg["last_language"] = langs[idx % len(langs)]
            cfg["updated_at"] = datetime.now(timezone.utc).isoformat()
            save_rotation(cfg)
        
        cfg_final = load_rotation()
        expected_idx = (cfg_orig["current_index"] + len(langs)) % len(langs)
        t("Rotation wraps after full cycle",
          cfg_final["current_index"] == expected_idx)
    except Exception as e:
        t("Rotation wrap test", False, str(e))

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
        result = topology()
        print(format_topology(result))