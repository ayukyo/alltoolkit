#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🪡 Polyglot Loom v1.0.0
A weaving/textile arts engine for programming languages — every language
is treated as a hand-loomed tapestry, with warp/weft, threads, bobbins,
heddles, shuttles, looms, patterns, dye-pots, and cloth-of-state.

Creative concept:
  "Every program is a tapestry, and every language is a loom. Some looms
   are sturdy oaken floor-looms (C/C++), some are sleek modern rigid-
   heddle (TypeScript), some are circular knitting rings (Kotlin), some
   are Jacquard punched-card marvels (Rust's ownership checker). The
   weaver — the developer — chooses the warp (the static skeleton) and
   the weft (the dynamic behaviour), threads libraries through the
   heddles, dyes the palette, and produces a unique cloth. This tool
   shows the loom, the threads, the cloth, and the pattern book for
   whichever language the rotation has spun to."

Key features:
  1. Loom Catalogue     — every language mapped to a loom archetype
  2. Warp & Weft        — static (syntax/keywords) vs dynamic (runtime)
  3. Thread Library     — package/library ecosystem as dyed threads
  4. Heddle Map         — how the type system combs the warp threads
  5. Shuttle Patterns   — control-flow motifs (looping, branching, async)
  6. Bobbin Inventory   — primitives & value types in the loom's bin
  7. Dye-Pot Palette    — color mapping for syntax highlighting
  8. Cloth Tension      — performance / efficiency profile
  9. Pattern Book       — idiomatic "weave patterns" for each language
 10. Tapestry Output    — ASCII-art cloth preview woven from snippets
 11. Loom Tour          — visit all 8 looms in sequence
 12. Rotation Advance   — reads/updates language_rotation.json

Distinct from existing tools:
  - polyglot_bloom:    gardening / phenology (organic growth lens)
  - polyglot_lullaby:  bedtime narrative (calming lens)
  - polyglot_mood:     emotional profiling (psychological lens)
  - polyglot_flavor:   sensory sommelier (taste lens)
  - polyglot_vessel:   essence distillation (alembic lens)
  - polyglot_pulse:    vital signs (medical lens)
  - polyglot_wire:     cross-language FFI (electrical lens)
  - polyglot_reef:     marine ecosystem (oceanic lens)
  - polyglot_forge:    metalworking / smithing lens
  - polyglot_orbit:    celestial mechanics (spatial lens)
  - polyglot_rorschach: inkblot projection (psychoanalytic lens)
  - polyglot_metamorphosis: AST transformation (transmutation lens)

Loom is about WEAVING / TEXTILE ARTS — threads, heddles, shuttles, warps,
wefts, bobbins, dye-pots, patterns, and cloth. No other tool does that.

Rotation: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import math
import os
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-loom"
TOOL_VERSION = "1.0.0"

# Resolve rotation file at workspace root (one level above AllToolkit/).
# We walk upward looking for `language_rotation.json`.
ROTATION_FILE = str(
    Path(__file__).parent.parent.parent / "language_rotation.json"
)


# ── Loom catalogue ────────────────────────────────────────────────────────────
# Each language is a loom archetype. A loom has:
#   archetype         — kind of loom (floor/rigid-heddle/circular/...)
#   fabric            — primary cloth it weaves
#   warp_threads      — static constructs (syntax, keywords)
#   weft_threads      — dynamic constructs (runtime, eval, JIT)
#   heddles           — type system rules that comb the warp
#   shuttles          — control-flow mechanisms
#   bobbins           — primitive types / value units
#   dye_palette       — colors used in syntax highlighting
#   tension           — how tight the cloth is (perf vs ergonomics)
#   pattern_books     — idiomatic weave patterns
#   motif             — short craft metaphor
#   thread_library    — package/library ecosystem
#   emoji             — species marker
#   heddle_count      — number of heddles (≈ complexity of type system)
#   reed_dpi          — threads per inch (≈ density / precision)
#   cloth_weight_gsm  — cloth weight in g/m² (≈ memory footprint)
#   selvedge          — the language's "selvedge" (edge) — what holds the
#                       cloth together at the boundary (FFI / ABI)
#   warp_yarn         — the yarn of the warp (core type system)
#   weft_yarn         — the yarn of the weft (core execution model)

LOOMS: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "archetype": "Jacquard Loom (punched-card)",
        "fabric": "Borrowed Ownership Cloth — tight, durable, memory-safe",
        "motif": "the weaver's heddles are punched-cards of lifetimes",
        "emoji": "🧵",
        "warp_yarn": "Affine types + lifetimes (the warp is statically tensioned)",
        "weft_yarn": "Move semantics + async/await (the weft slides by ownership)",
        "warp_threads": [
            "fn", "let", "mut", "const", "static", "struct", "enum",
            "trait", "impl", "use", "mod", "pub", "crate", "self",
            "Self", "where", "as", "ref", "move",
        ],
        "weft_threads": [
            "async", "await", ".await", "spawn", "join", "channel",
            "Box", "Rc", "Arc", "Mutex", "RefCell",
        ],
        "heddles": [
            "borrow checker", "lifetime elision", "trait bounds",
            "where clauses", "Send + Sync", "dyn safety",
        ],
        "shuttles": [
            "for-loop", "while let", "match arms", "if-let chains",
            "?  operator", "iterator adapters",
        ],
        "bobbins": [
            "i8..i128", "u8..u128", "f32", "f64", "bool", "char",
            "()", "str", "String", "Vec", "HashMap", "Result", "Option",
        ],
        "dye_palette": {
            "keyword": "#CE422B",   # Rust orange-red
            "type":    "#2B5F7E",   # deep blue
            "string":  "#5C8A2A",   # olive
            "comment": "#8C8C8C",   # grey
            "macro":   "#A65959",   # dusty rose
        },
        "tension": "very tight (zero-cost abstractions)",
        "pattern_books": [
            "Newtype Wrapper — a single thread wrapped once for type safety",
            "Builder Pattern — chaining bobbins one at a time",
            "Iterator Chain — adapters on a continuous warp",
            "RAII Drop — the loom's automatic warp-cutting at scope end",
        ],
        "thread_library": ["Cargo", "crates.io", "Tokio", "Serde", "Diesel", "Actix"],
        "heddle_count": 64,
        "reed_dpi": 120,
        "cloth_weight_gsm": 220,
        "selvedge": "C ABI / FFI (the firm selvedge that holds the cloth)",
        "loom_width_cm": 180,
    },
    "Go": {
        "archetype": "Sturdy Floor Loom (rigid-heddle, simple)",
        "fabric": "Goroutine Plain-Weave — fast, plain, plentiful",
        "motif": "a workshop loom — small, fast, and produces thousands of yards",
        "emoji": "🧶",
        "warp_yarn": "Static structural typing (no generics cleverness)",
        "weft_yarn": "Goroutines + channels (concurrency slides the weft)",
        "warp_threads": [
            "func", "var", "const", "package", "import", "type", "struct",
            "interface", "go", "defer", "return", "if", "else", "for",
            "range", "switch", "select", "chan",
        ],
        "weft_threads": [
            "go func()", "chan T", "context.Context", "sync.WaitGroup",
            "sync.Mutex", "defer", "panic/recover",
        ],
        "heddles": [
            "interface satisfaction", "structural typing",
            "embedding", "package visibility",
        ],
        "shuttles": [
            "goroutine", "channel send/receive", "select on multiple channels",
            "range over channel", "defer stack",
        ],
        "bobbins": [
            "bool", "byte", "rune", "int", "int8..int64",
            "uint", "uint8..uint64", "float32", "float64",
            "string", "error", "interface{}", "struct{}",
        ],
        "dye_palette": {
            "keyword": "#00ADD8",   # Go cyan
            "type":    "#005C8F",   # navy
            "string":  "#5C8A2A",   # olive
            "comment": "#8C8C8C",   # grey
            "func":    "#E08A00",   # amber
        },
        "tension": "medium (ergonomics over zero-cost)",
        "pattern_books": [
            "Worker Pool — many shuttles, one warp",
            "Pipeline — channels as rollers between stages",
            "Context Propagation — the weaver's bell that ends every weave",
            "Table-Driven Tests — the canonical pattern card",
        ],
        "thread_library": ["go mod", "Kubernetes", "Docker", "Terraform", "Hugo", "Cobra"],
        "heddle_count": 16,
        "reed_dpi": 80,
        "cloth_weight_gsm": 180,
        "selvedge": "cgo (the carefully woven selvedge to C)",
        "loom_width_cm": 220,
    },
    "Swift": {
        "archetype": "Tartan Loom (patterned, decorative)",
        "fabric": "Optional-Value Tartan — showy, careful, Apple-curated",
        "motif": "the weaver must always check for the empty bobbin",
        "emoji": "🪡",
        "warp_yarn": "Protocol-oriented static typing",
        "weft_yarn": "Optional chaining + async/await + ARC",
        "warp_threads": [
            "func", "let", "var", "class", "struct", "enum", "protocol",
            "extension", "import", "guard", "if let", "switch", "where",
            "self", "Self", "init", "deinit", "throws", "try",
        ],
        "weft_threads": [
            "?", "!", "??", "async", "await", "Task", "Actor",
            "@MainActor", "weak", "unowned",
        ],
        "heddles": [
            "Optional binding", "Protocol conformance", "Generics",
            "Result builders", "Property wrappers",
        ],
        "shuttles": [
            "guard let", "if let", "for-in", "while let",
            "defer", "do-try-catch",
        ],
        "bobbins": [
            "Int", "UInt", "Double", "Float", "Bool", "String",
            "Character", "Array", "Dictionary", "Set", "Optional",
            "Result", "Data", "URL",
        ],
        "dye_palette": {
            "keyword": "#F05138",   # Swift orange
            "type":    "#7E2DBE",   # purple
            "string":  "#5C8A2A",   # olive
            "comment": "#8C8C8C",   # grey
            "decorator": "#0E80C5", # attribute blue
        },
        "tension": "medium-tight (Apple-curated patterns)",
        "pattern_books": [
            "Optional Chaining — pass the empty bobbin without crashing",
            "Protocol Witness Table — the heddle card",
            "Result Builders — DSLs as woven tartan",
            "Property Wrappers — decorative borders on plain weave",
        ],
        "thread_library": ["SwiftPM", "Vapor", "Combine", "SwiftUI", "Alamofire"],
        "heddle_count": 40,
        "reed_dpi": 96,
        "cloth_weight_gsm": 200,
        "selvedge": "Objective-C bridging (the historical selvedge)",
        "loom_width_cm": 160,
    },
    "Kotlin": {
        "archetype": "Circular Knitting Loom (round, flowing)",
        "fabric": "Null-Safe Knit — stretchy, JVM-hosted, multiplatform",
        "motif": "no thread drops, no null tears",
        "emoji": "🪢",
        "warp_yarn": "Statically typed, null-safe by default",
        "weft_yarn": "Coroutines + DSL builders",
        "warp_threads": [
            "fun", "val", "var", "class", "object", "interface",
            "data class", "sealed class", "when", "if", "else",
            "import", "package", "companion", "init", "private",
            "internal", "public", "open", "abstract",
        ],
        "weft_threads": [
            "suspend", "launch", "async", "await", "runBlocking",
            "withContext", "Flow", "Channel", "let", "apply", "also",
        ],
        "heddles": [
            "Null safety", "Smart casts", "Sealed classes", "When expressions",
            "Extension receivers", "Inline classes",
        ],
        "shuttles": [
            "for-each", "for (x in xs)", "while", "when", "let scope",
            "apply scope", "with scope",
        ],
        "bobbins": [
            "Int", "Long", "Short", "Byte", "Float", "Double", "Boolean",
            "Char", "String", "Array", "List", "Map", "Set", "Pair",
            "Triple", "Sequence", "Result",
        ],
        "dye_palette": {
            "keyword": "#7F52FF",   # Kotlin purple
            "type":    "#B388EA",   # light purple
            "string":  "#5C8A2A",   # olive
            "comment": "#8C8C8C",   # grey
            "decorator": "#F4A02A", # annotation amber
        },
        "tension": "medium (JVM-friendly, ergonomic)",
        "pattern_books": [
            "Scope Functions — let/apply/also/run/with as the five basic weaves",
            "Sealed Class Hierarchies — when-expressions on a closed loom",
            "DSL Builders — type-safe builders as a chained warp",
            "Coroutines & Flow — reactive weft that flows naturally",
        ],
        "thread_library": ["Gradle", "Kotlinx", "Jetpack Compose", "Exposed", "Ktor"],
        "heddle_count": 36,
        "reed_dpi": 100,
        "cloth_weight_gsm": 195,
        "selvedge": "JVM ABI (the JVM selvedge that holds everything)",
        "loom_width_cm": 170,
    },
    "TypeScript": {
        "archetype": "Rigid-Heddle Modern Loom (precision, fast)",
        "fabric": "Typed Huck-a-Back — textured but soft, everywhere-woven",
        "motif": "the loom comb reads every warp thread twice",
        "emoji": "🪡",
        "warp_yarn": "Structural typing with generics",
        "weft_yarn": "Promises, async/await, generators",
        "warp_threads": [
            "function", "const", "let", "var", "interface", "type",
            "class", "enum", "namespace", "import", "export",
            "extends", "implements", "abstract", "readonly",
            "private", "public", "protected", "async",
        ],
        "weft_threads": [
            "Promise<T>", "async/await", "Observable", "Generator",
            "Iterator", "Map", "Set", "WeakMap", "Proxy",
        ],
        "heddles": [
            "Type inference", "Union types", "Intersection types",
            "Generics", "Mapped types", "Conditional types",
            "Template literal types", "Satisfies operator",
        ],
        "shuttles": [
            "for-of", "for-in", "Array.map", "Array.filter", "Array.reduce",
            "async for-await-of", "Promise.all",
        ],
        "bobbins": [
            "number", "string", "boolean", "null", "undefined",
            "symbol", "bigint", "any", "unknown", "never", "void",
            "object", "Array<T>", "Record<K,V>", "Partial<T>", "Readonly<T>",
        ],
        "dye_palette": {
            "keyword": "#3178C6",   # TypeScript blue
            "type":    "#0E80C5",   # attribute blue
            "string":  "#A65959",   # dusty rose
            "comment": "#8C8C8C",   # grey
            "decorator": "#B388EA", # decorator purple
        },
        "tension": "tight (structural typing is precise)",
        "pattern_books": [
            "Discriminated Union — tagged baskets on the same warp",
            "Branded Type — a single thread dyed with a type-stamp",
            "Builder Pattern — chained setters as a smooth warp",
            "Mapped Type — transform one weave into another in place",
        ],
        "thread_library": ["npm", "React", "Next.js", "Deno", "Bun", "tRPC", "Zod"],
        "heddle_count": 56,
        "reed_dpi": 110,
        "cloth_weight_gsm": 175,
        "selvedge": "JS interop (every TS thread can weave back to JS)",
        "loom_width_cm": 200,
    },
    "JavaScript": {
        "archetype": "Backstrap Loom (portable, hand-held, everywhere)",
        "fabric": "Async Huck — texturally rich, async-shifted, ubiquitous",
        "motif": "the loom goes wherever the weaver goes",
        "emoji": "🧶",
        "warp_yarn": "Dynamic typing (the warp is forgiving)",
        "weft_yarn": "Event loop + Promises + async/await",
        "warp_threads": [
            "function", "const", "let", "var", "class", "import",
            "export", "default", "new", "this", "return", "if",
            "else", "for", "while", "do", "switch", "try", "catch",
            "throw", "typeof", "instanceof",
        ],
        "weft_threads": [
            "Promise", "async", "await", "setTimeout", "setInterval",
            "requestAnimationFrame", "fetch", "EventTarget",
            "WeakRef", "FinalizationRegistry",
        ],
        "heddles": [
            "Truthiness", "Type coercion", "Prototypes",
            "Closure scope", "this binding",
        ],
        "shuttles": [
            "for-of", "for-in", "Array methods", "Promise.all",
            "Promise.race", "async iterator",
        ],
        "bobbins": [
            "number", "string", "boolean", "null", "undefined",
            "symbol", "bigint", "object", "Array", "Map", "Set",
            "WeakMap", "WeakSet", "Date", "RegExp", "Promise",
        ],
        "dye_palette": {
            "keyword": "#F7DF1E",   # JS yellow
            "type":    "#0E80C5",   # attribute blue
            "string":  "#A65959",   # dusty rose
            "comment": "#8C8C8C",   # grey
            "decorator": "#7F52FF", # decorator purple
        },
        "tension": "loose (dynamic, ergonomic)",
        "pattern_books": [
            "Callback to Promise to async/await — three generations of weft",
            "Module Pattern — IIFE as a tiny private loom",
            "Event Emitter — pub-sub as a shared warp",
            "Higher-Order Functions — functions as shuttle, function as warp",
        ],
        "thread_library": ["npm", "React", "Vue", "Express", "Node.js", "Bun", "Deno"],
        "heddle_count": 12,
        "reed_dpi": 70,
        "cloth_weight_gsm": 160,
        "selvedge": "V8 / SpiderMonkey ABI (the engine's hidden selvedge)",
        "loom_width_cm": 240,
    },
    "Java": {
        "archetype": "Heavy Industrial Loom (production-line)",
        "fabric": "Enterprise Twill — sturdy, verbose, decades-long",
        "motif": "the loom is verbose because the cloth must outlast empires",
        "emoji": "🏭",
        "warp_yarn": "Nominal static typing + class hierarchy",
        "weft_yarn": "JVM bytecode + JIT + GC",
        "warp_threads": [
            "public", "private", "protected", "static", "final",
            "abstract", "class", "interface", "extends", "implements",
            "package", "import", "void", "int", "long", "double",
            "float", "boolean", "char", "if", "else", "for", "while",
            "do", "switch", "try", "catch", "finally", "throw", "throws",
            "return", "new",
        ],
        "weft_threads": [
            "synchronized", "volatile", "transient", "Thread",
            "ExecutorService", "CompletableFuture", "Stream",
            "Optional", "var", "record", "sealed",
        ],
        "heddles": [
            "Class hierarchy", "Generics with erasure", "Access modifiers",
            "Checked exceptions", "Annotation processing",
        ],
        "shuttles": [
            "for-each", "Stream pipeline", "Optional chaining",
            "try-with-resources", "switch expression",
        ],
        "bobbins": [
            "byte", "short", "int", "long", "float", "double",
            "boolean", "char", "String", "Object", "List",
            "Map", "Set", "Optional", "Stream", "LocalDate",
        ],
        "dye_palette": {
            "keyword": "#ED8B00",   # Java orange
            "type":    "#5C2D91",   # royal purple
            "string":  "#5C8A2A",   # olive
            "comment": "#8C8C8C",   # grey
            "annotation": "#A65959", # dusty rose
        },
        "tension": "very tight (decades-long stability)",
        "pattern_books": [
            "Factory Method — a single shuttle that produces many bobbins",
            "Builder — the canonical verbose builder",
            "DAO/Repository — separated warp and weft of data access",
            "Strategy — interchangeable shuttles on the same warp",
        ],
        "thread_library": ["Maven", "Gradle", "Spring", "Hibernate", "JUnit", "Guava"],
        "heddle_count": 48,
        "reed_dpi": 90,
        "cloth_weight_gsm": 260,
        "selvedge": "JNI / JVM ABI (the iron selvedge)",
        "loom_width_cm": 200,
    },
    "C/C++": {
        "archetype": "Handloom of Antiquity (the original loom)",
        "fabric": "Foundational Linen — bare thread, ancient, durable",
        "motif": "the weaver must wind every bobbin by hand",
        "emoji": "🪢",
        "warp_yarn": "Static (C) + templates / generics (C++)",
        "weft_yarn": "Manual memory + pointer arithmetic + RAII",
        "warp_threads": [
            "int", "char", "float", "double", "void", "short", "long",
            "signed", "unsigned", "struct", "union", "enum", "typedef",
            "static", "extern", "const", "volatile", "register", "auto",
            "if", "else", "for", "while", "do", "switch", "case",
            "break", "continue", "return", "goto",
        ],
        "weft_threads": [
            "malloc", "free", "new", "delete", "memcpy", "memset",
            "sizeof", "offsetof", "reinterpret_cast", "std::move",
            "std::unique_ptr", "std::shared_ptr",
        ],
        "heddles": [
            "Pointer rules", "Const correctness", "Template metaprogramming",
            "SFINAE", "Concepts", "constexpr", "ABI rules",
        ],
        "shuttles": [
            "for-loop", "while-loop", "do-while", "range-for",
            "switch fall-through", "lambda capture",
        ],
        "bobbins": [
            "char", "short", "int", "long", "long long", "float",
            "double", "long double", "_Bool", "void*", "int*",
            "std::array", "std::vector", "std::string", "std::map",
        ],
        "dye_palette": {
            "keyword": "#00599C",   # C blue
            "type":    "#7E2DBE",   # purple
            "string":  "#A65959",   # dusty rose
            "comment": "#8C8C8C",   # grey
            "preprocessor": "#CE422B", # preprocessor red
        },
        "tension": "ancient-strong (the cloth outlasts everything)",
        "pattern_books": [
            "RAII — every resource is a guarded bobbin",
            "Rule of Five — five shuttles for one warp",
            "Template Specialization — dyed threads for every cloth",
            "PIMPL — a hidden warp that lets the weaver move freely",
        ],
        "thread_library": ["CMake", "Conan", "vcpkg", "Boost", "STL", "Qt"],
        "heddle_count": 72,
        "reed_dpi": 130,
        "cloth_weight_gsm": 280,
        "selvedge": "C ABI (the original selvedge, all other selvedges descend from this)",
        "loom_width_cm": 150,
    },
}


# ── Helper functions ──────────────────────────────────────────────────────────

def _now_iso() -> str:
    """Current local-time ISO timestamp."""
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def _digest(*parts: str) -> str:
    """Stable short hash of concatenated strings."""
    h = hashlib.sha1("::".join(parts).encode("utf-8")).hexdigest()
    return h[:8]


def _cloth_density(loom: Dict[str, Any]) -> Dict[str, Any]:
    """Compute the cloth density (ergonomics vs precision vs weight).

    Density reflects how tightly the loom is strung. We combine:
      - heddle_count      (type-system complexity)
      - reed_dpi          (precision)
      - cloth_weight_gsm  (memory footprint)

    Returns a density index 0-10 and a classification.
    """
    heddle = loom["heddle_count"]
    dpi = loom["reed_dpi"]
    gsm = loom["cloth_weight_gsm"]

    # Normalize each to [0, 1]
    h_norm = min(1.0, heddle / 80.0)
    d_norm = min(1.0, dpi / 140.0)
    g_norm = min(1.0, gsm / 300.0)

    density = (h_norm * 0.4 + d_norm * 0.35 + g_norm * 0.25) * 10.0

    if density >= 8.5:
        classification = "🏛️ Tapestry-grade — museum-piece cloth"
    elif density >= 7.0:
        classification = "🧵 Heavy brocade — robust and detailed"
    elif density >= 5.5:
        classification = "🧶 Balanced cloth — everyday weave"
    elif density >= 4.0:
        classification = "🪶 Light linen — airy and fast"
    else:
        classification = "🌫️ Gossamer — featherlight, fragile"

    return {
        "heddle_count": heddle,
        "reed_dpi": dpi,
        "cloth_weight_gsm": gsm,
        "density_index": round(density, 2),
        "classification": classification,
    }


def _thread_health(loom: Dict[str, Any]) -> Dict[str, Any]:
    """Compute the health of the loom's thread library (ecosystem)."""
    threads = loom["thread_library"]
    n = len(threads)

    # Categorize threads (heuristic)
    foundation = [t for t in threads if any(k in t.lower() for k in ["cargo", "go mod", "swiftpm", "gradle", "npm", "maven", "cmake", "conan", "vcpkg"])]
    runtime = [t for t in threads if any(k in t.lower() for k in ["tokio", "spring", "react", "vue", "compose", "swiftui", "node", "bun", "deno", "actix", "ktor", "express", "vapor", "hibernate"])]
    utility = [t for t in threads if any(k in t.lower() for k in ["serde", "junit", "boost", "stl", "qt", "guava", "exposed", "diesel", "trpc", "zod", "cobra", "terraform", "kubernetes", "docker", "hugo", "alamofire", "combine"])]

    diversity = sum(1 for c in (foundation, runtime, utility) if c)
    strength = min(10.0, n * 1.4 + diversity * 1.2)

    if strength >= 8.5:
        rating = "🧵 Plentiful — overflowing thread bins"
    elif strength >= 7.0:
        rating = "🧶 Well-stocked — strong selection"
    elif strength >= 5.5:
        rating = "🪡 Adequate — enough for most weaves"
    else:
        rating = "🪶 Sparse — fewer threads to choose from"

    return {
        "thread_count": n,
        "foundation": foundation,
        "runtime": runtime,
        "utility": utility,
        "diversity_score": diversity,
        "strength_index": round(strength, 2),
        "rating": rating,
    }


def _weave_pattern(language: str, snippet: str = "") -> Dict[str, Any]:
    """Detect which weave pattern is most relevant for a code snippet.

    Returns the matched patterns (up to 2) and a tension reading.
    """
    loom = LOOMS[language]
    patterns = loom["pattern_books"]

    # No snippet: deterministic fallback picks a single pattern from the book
    if not snippet or not snippet.strip():
        seed = _digest(language, "silent")
        chosen = patterns[int(seed[0], 16) % len(patterns)]
        return {
            "matched": [{"label": "default", "pattern": chosen}],
            "tension_reading": "no snippet — loom at rest",
            "line_count": 0,
            "char_count": 0,
            "digest": seed,
        }

    text = snippet.lower()

    # Token-style hints per language for pattern matching
    pattern_keywords = {
        "Rust": [
            ("newtype", ["newtype", "wrapper struct"]),
            ("builder", ["builder", ".build()"]),
            ("iterator", [".iter()", ".map(", ".filter(", ".collect()"]),
            ("raii", ["drop", "raii", "scope"]),
        ],
        "Go": [
            ("worker pool", ["worker", "pool", "go func"]),
            ("pipeline", ["chan", "pipeline"]),
            ("context", ["context.", "ctx"]),
            ("table-driven", ["tests := []struct"]),
        ],
        "Swift": [
            ("optional chaining", ["?", "!", "??"]),
            ("protocol witness", ["protocol", "witness"]),
            ("result builder", ["@resultbuilder", "builder"]),
            ("property wrapper", ["@published", "propertywrapper"]),
        ],
        "Kotlin": [
            ("scope functions", [".let", ".apply", ".also", ".run", ".with"]),
            ("sealed class", ["sealed class", "sealed interface"]),
            ("dsl builders", ["dsl", "builder", "@DslMarker"]),
            ("coroutines", ["suspend", "launch", "async"]),
        ],
        "TypeScript": [
            ("discriminated union", ["type ", " | ", "kind:", "tag:"]),
            ("branded type", ["__brand", "branded"]),
            ("builder", [".with(", ".set(", "builder"]),
            ("mapped type", ["readonly", "partial", "pick<", "omit<"]),
        ],
        "JavaScript": [
            ("callback→promise→async", ["async", "await", "promise", "then("]),
            ("module pattern", ["iife", "(function("]),
            ("event emitter", ["emitter", "on(", "emit("]),
            ("higher-order", [".map(", ".filter(", ".reduce("]),
        ],
        "Java": [
            ("factory method", ["factory", "create("]),
            ("builder", ["builder", ".build()"]),
            ("dao", ["repository", "dao"]),
            ("strategy", ["strategy", "interface"]),
        ],
        "C/C++": [
            ("raii", ["raii", "~class", "destructor"]),
            ("rule of five", ["copy constructor", "rule of"]),
            ("template", ["template<", "typename "]),
            ("pimpl", ["pimpl", "impl", "unique_ptr"]),
        ],
    }

    matched = []
    keyword_table = pattern_keywords.get(language, [])
    for label, keywords in keyword_table:
        if any(k in text for k in keywords):
            for p in patterns:
                if label.lower() in p.lower() or any(k in p.lower() for k in keywords[:1]):
                    matched.append({"label": label, "pattern": p})
                    break

    # If nothing matched, fall back to the first pattern deterministically
    if not matched:
        seed = _digest(language, snippet)
        chosen = patterns[int(seed[0], 16) % len(patterns)]
        matched.append({"label": "default", "pattern": chosen})

    # Tension reading: how stretched the snippet seems
    lines = snippet.count("\n") + 1
    chars = len(snippet)
    tension_ratio = min(1.0, chars / 1000.0)
    if tension_ratio < 0.3:
        tension = "loose — barely stretched"
    elif tension_ratio < 0.7:
        tension = "taut — properly tensioned"
    else:
        tension = "over-stretched — risk of warp breakage"

    return {
        "matched": matched[:2],
        "tension_reading": tension,
        "line_count": lines,
        "char_count": chars,
        "digest": _digest(language, snippet),
    }


def _dye_recipe(loom: Dict[str, Any]) -> Dict[str, Any]:
    """Compose a 'dye recipe' — how the loom's colors combine to dye a cloth."""
    palette = loom["dye_palette"]
    dyes = []
    for role, hex_color in palette.items():
        # convert hex to a coarse RGB tuple
        h = hex_color.lstrip("#")
        rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        dyes.append({
            "role": role,
            "hex": hex_color,
            "rgb": list(rgb),
        })

    # build a 4-stop gradient suggestion
    stops = [palette["keyword"], palette["type"], palette["string"], palette["comment"]]
    return {
        "tool_note": "Dye pots for the loom — each role gets a colour so the eye can follow threads",
        "dyes": dyes,
        "gradient_suggestion": " → ".join(stops),
        "total_dyes": len(dyes),
    }


def _weave_preview(language: str, width: int = 32) -> str:
    """Generate a deterministic ASCII 'woven cloth' preview for the language.

    The pattern is a small tartan/checkered weave derived from the digest
    of the loom + language, with thread characters for warp vs weft.
    """
    loom = LOOMS[language]
    digest = _digest("weave", language)
    # Use bytes of digest to seed a simple PRNG (deterministic)
    seed_int = int(digest, 16)
    rows = []
    height = width // 2
    # Two thread characters
    warp_ch = "┃"
    weft_ch = "━"
    knot_ch = "╋"

    for r in range(height):
        line_chars = []
        for c in range(width):
            # pseudo-random bit from seed_int shifting
            bit = (seed_int >> ((r * width + c) % 64)) & 1
            char = warp_ch if bit == 0 else weft_ch
            line_chars.append(char)
        # add a knot at the selvedge edge every other row
        if r % 2 == 0:
            line_chars[0] = knot_ch
            line_chars[-1] = knot_ch
        rows.append("".join(line_chars))

    # Top and bottom selvedge lines
    selvedge_ch = "═"
    selvedge = selvedge_ch * (width + 2)
    body = "\n".join("║" + r + "║" for r in rows)
    return f"┌{selvedge}┐\n{body}\n└{selvedge}┘"


# ── Rotation file I/O ─────────────────────────────────────────────────────────

def load_rotation(path: Optional[str] = None) -> Dict[str, Any]:
    """Load language_rotation.json from the resolved path."""
    p = Path(path) if path else Path(ROTATION_FILE)
    if not p.is_absolute():
        # Try a few likely parents
        candidates = [
            Path(__file__).parent.parent.parent / p.name,
            Path(__file__).parent.parent / p.name,
            p,
        ]
        for c in candidates:
            if c.exists():
                p = c
                break
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any], path: Optional[str] = None) -> None:
    """Persist rotation data back to the JSON file."""
    p = Path(path) if path else Path(ROTATION_FILE)
    if not p.is_absolute():
        candidates = [
            Path(__file__).parent.parent.parent / p.name,
            Path(__file__).parent.parent / p.name,
            p,
        ]
        for c in candidates:
            # Choose the first existing parent path; fall back to canonical.
            if c.parent.exists():
                p = c
                break
        else:
            p = Path(__file__).parent.parent.parent / p.name
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_current_language() -> str:
    """Return the language at the current rotation index (no advance)."""
    cfg = load_rotation()
    langs = cfg.get("languages", list(LOOMS.keys()))
    idx = cfg.get("current_index", 0) % len(langs)
    return langs[idx]


# ── Core API ──────────────────────────────────────────────────────────────────

def loom_report(
    language: Optional[str] = None,
    advance: bool = True,
    snippet: str = "",
) -> Dict[str, Any]:
    """
    Generate a loom report for the current rotation language.

    Reads language_rotation.json, picks the language, generates its
    loom archetype, density, thread health, dye recipe, weave patterns,
    ASCII cloth preview, and rotation state. Advances the rotation
    index by default.

    Args:
        language: override the selected language (for testing)
        advance: whether to advance the rotation index after the call
        snippet: optional code snippet to drive weave-pattern detection

    Returns:
        dict containing the loom report and updated rotation state
    """
    cfg = load_rotation()
    langs = cfg.get("languages", list(LOOMS.keys()))

    if language is None:
        idx = cfg.get("current_index", 0) % len(langs)
        current_lang = langs[idx]
    else:
        if language not in langs:
            raise ValueError(f"Unknown language: {language}")
        current_lang = language
        idx = langs.index(current_lang)

    # Advance rotation if requested
    if advance:
        cfg["current_index"] = (idx + 1) % len(langs)
        cfg["last_language"] = current_lang
        save_rotation(cfg)

    loom = LOOMS[current_lang]
    density = _cloth_density(loom)
    threads = _thread_health(loom)
    weave = _weave_pattern(current_lang, snippet)
    dyes = _dye_recipe(loom)
    preview = _weave_preview(current_lang)

    # Overall loom vitality: average of density, thread health, weave digest
    vitality_components = [
        density["density_index"] / 10.0,
        threads["strength_index"] / 10.0,
        (1.0 if weave["matched"] else 0.5),
    ]
    vitality = sum(vitality_components) / len(vitality_components) * 10.0

    if vitality >= 8.5:
        vitality_class = "🏛️ Master loom — legendary craftsmanship"
    elif vitality >= 7.0:
        vitality_class = "🧵 Skilled loom — accomplished weaving"
    elif vitality >= 5.5:
        vitality_class = "🧶 Working loom — solid daily output"
    elif vitality >= 4.0:
        vitality_class = "🪡 Apprentice loom — still learning patterns"
    else:
        vitality_class = "🪶 Fragile loom — needs a careful weaver"

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "generated_at": _now_iso(),
        "current_language": current_lang,
        "rotation_index": idx,
        "next_language": langs[(idx + 1) % len(langs)],
        "loom": {
            "archetype": loom["archetype"],
            "fabric": loom["fabric"],
            "motif": loom["motif"],
            "warp_yarn": loom["warp_yarn"],
            "weft_yarn": loom["weft_yarn"],
            "loom_width_cm": loom["loom_width_cm"],
            "selvedge": loom["selvedge"],
            "emoji": loom["emoji"],
            "tension": loom["tension"],
        },
        "warp_threads": loom["warp_threads"],
        "weft_threads": loom["weft_threads"],
        "heddles": loom["heddles"],
        "shuttles": loom["shuttles"],
        "bobbins": loom["bobbins"],
        "pattern_books": loom["pattern_books"],
        "thread_library": loom["thread_library"],
        "density": density,
        "thread_health": threads,
        "weave": weave,
        "dye_recipe": dyes,
        "preview": preview,
        "vitality": {
            "score": round(vitality, 2),
            "classification": vitality_class,
        },
    }


def loom_tour() -> Dict[str, Any]:
    """Visit all 8 looms in sequence with brief summaries."""
    summary = []
    for lang, loom in LOOMS.items():
        density = _cloth_density(loom)
        threads = _thread_health(loom)
        summary.append({
            "language": lang,
            "emoji": loom["emoji"],
            "archetype": loom["archetype"],
            "fabric": loom["fabric"],
            "density_class": density["classification"],
            "thread_rating": threads["rating"],
            "thread_count": threads["thread_count"],
            "loom_width_cm": loom["loom_width_cm"],
        })
    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "generated_at": _now_iso(),
        "looms": summary,
        "total_looms": len(summary),
    }


def dye_comparison(language_a: str, language_b: str) -> Dict[str, Any]:
    """Compare two looms' dye palettes — how their threads color the cloth."""
    if language_a not in LOOMS or language_b not in LOOMS:
        raise ValueError(f"Unknown language: {language_a} or {language_b}")

    pa = LOOMS[language_a]["dye_palette"]
    pb = LOOMS[language_b]["dye_palette"]

    # Compute similarity across shared roles
    shared_roles = set(pa.keys()) & set(pb.keys())
    diffs = []
    for role in shared_roles:
        ha = pa[role].lstrip("#")
        hb = pb[role].lstrip("#")
        ra = tuple(int(ha[i:i+2], 16) for i in (0, 2, 4))
        rb = tuple(int(hb[i:i+2], 16) for i in (0, 2, 4))
        # Euclidean distance normalized to [0, ~441]
        dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(ra, rb)))
        diffs.append({"role": role, "color_a": pa[role], "color_b": pb[role], "distance": round(dist, 2)})

    avg_dist = sum(d["distance"] for d in diffs) / len(diffs) if diffs else 0.0

    if avg_dist < 30:
        classification = "🧵 Twin looms — nearly identical palettes"
    elif avg_dist < 80:
        classification = "🧶 Cousin looms — kindred palette"
    elif avg_dist < 150:
        classification = "🪡 Distant looms — different palettes"
    else:
        classification = "🌈 Foreign looms — strikingly different palettes"

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language_a": language_a,
        "language_b": language_b,
        "shared_roles": sorted(shared_roles),
        "role_distances": diffs,
        "average_distance": round(avg_dist, 2),
        "classification": classification,
    }


def run_tests() -> List[str]:
    """Run all tests for polyglot_loom.

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
        if a == b:
            check(True, name)
        else:
            # Truncate long reprs to keep output readable
            ra, rb = repr(a), repr(b)
            if len(ra) > 60:
                ra = ra[:57] + "..."
            if len(rb) > 60:
                rb = rb[:57] + "..."
            check(False, f"{name} (expected {rb}, got {ra})")

    def check_in(needle: Any, haystack: Any, name: str) -> None:
        if needle in haystack:
            check(True, name)
        else:
            # Show only the type of haystack to avoid dumping huge dicts
            rn = repr(needle)
            if len(rn) > 60:
                rn = rn[:57] + "..."
            check(False, f"{name} ({rn} not present)")

    print("🪡 Polyglot Loom v1.0.0 — Running tests")
    print()

    print("  --- Rotation File ---")
    cfg = load_rotation()
    check_eq(len(cfg["languages"]), 8, "8 languages in rotation file")
    check_in("current_index", cfg, "current_index field present")
    check_in("last_language", cfg, "last_language field present")
    check_in("updated_at", cfg, "updated_at field present")

    print("  --- Loom Catalogue ---")
    expected_langs = [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ]
    for lang in expected_langs:
        check_in(lang, LOOMS, f"{lang} has a loom profile")

    for lang, loom in LOOMS.items():
        for field in [
            "archetype", "fabric", "motif", "emoji",
            "warp_yarn", "weft_yarn", "warp_threads", "weft_threads",
            "heddles", "shuttles", "bobbins", "dye_palette",
            "tension", "pattern_books", "thread_library",
            "heddle_count", "reed_dpi", "cloth_weight_gsm",
            "selvedge", "loom_width_cm",
        ]:
            check_in(field, loom, f"{lang}.{field} present")

        check(len(loom["warp_threads"]) >= 8,
              f"{lang} warp_threads >= 8")
        check(len(loom["weft_threads"]) >= 3,
              f"{lang} weft_threads >= 3")
        check(len(loom["heddles"]) >= 2,
              f"{lang} heddles >= 2")
        check(len(loom["shuttles"]) >= 3,
              f"{lang} shuttles >= 3")
        check(len(loom["bobbins"]) >= 5,
              f"{lang} bobbins >= 5")
        check(len(loom["pattern_books"]) >= 3,
              f"{lang} pattern_books >= 3")
        check(len(loom["thread_library"]) >= 4,
              f"{lang} thread_library >= 4")
        check(loom["heddle_count"] > 0,
              f"{lang} heddle_count > 0")
        check(loom["reed_dpi"] > 0,
              f"{lang} reed_dpi > 0")
        check(loom["cloth_weight_gsm"] > 0,
              f"{lang} cloth_weight_gsm > 0")
        check(len(loom["emoji"]) > 0,
              f"{lang} emoji non-empty")
        check(loom["loom_width_cm"] > 0,
              f"{lang} loom_width_cm > 0")

        # Palette has all 5 roles
        for role in ("keyword", "type", "string", "comment"):
            check_in(role, loom["dye_palette"], f"{lang} palette has {role}")
            color = loom["dye_palette"][role]
            check(color.startswith("#") and len(color) == 7,
                  f"{lang} palette.{role} is a valid hex")

    print("  --- Cloth Density ---")
    for lang in expected_langs:
        d = _cloth_density(LOOMS[lang])
        check_in("density_index", d, f"{lang} density present")
        check_in("classification", d, f"{lang} density classification present")
        check(0.0 <= d["density_index"] <= 10.0,
              f"{lang} density_index in [0,10]")
        check_eq(d["heddle_count"], LOOMS[lang]["heddle_count"],
                 f"{lang} density.heddle_count matches loom")

    print("  --- Thread Health ---")
    for lang in expected_langs:
        t = _thread_health(LOOMS[lang])
        check_in("strength_index", t, f"{lang} thread strength present")
        check_in("rating", t, f"{lang} thread rating present")
        check_eq(t["thread_count"], len(LOOMS[lang]["thread_library"]),
                 f"{lang} thread_count matches library")
        check(t["thread_count"] >= 4,
              f"{lang} thread_count >= 4")
        check(0.0 <= t["strength_index"] <= 10.0,
              f"{lang} thread strength in [0,10]")

    print("  --- Weave Pattern Detection ---")
    # Each language: with snippet → matched; without → fallback
    for lang in expected_langs:
        w = _weave_pattern(lang, "")
        check_in("matched", w, f"{lang} weave.matched present")
        check_in("tension_reading", w, f"{lang} weave.tension_reading present")
        check(len(w["matched"]) >= 1, f"{lang} weave fallback present")

    # Snippet-driven match (Rust iterator)
    w = _weave_pattern("Rust", "let v: Vec<i32> = xs.iter().map(|x| x*2).collect();")
    matched_labels = [m["label"] for m in w["matched"]]
    check("iterator" in matched_labels or "builder" in matched_labels or "newtype" in matched_labels,
          "Rust snippet matches a known pattern")

    # Snippet-driven match (Go context)
    w = _weave_pattern("Go", "ctx, cancel := context.WithCancel(parentCtx)")
    matched_labels = [m["label"] for m in w["matched"]]
    check("context" in matched_labels or "worker pool" in matched_labels,
          "Go context snippet matches context pattern")

    # Snippet-driven match (TS discriminated union)
    w = _weave_pattern("TypeScript", "type Shape = { kind: 'circle' } | { kind: 'square' };")
    matched_labels = [m["label"] for m in w["matched"]]
    check("discriminated union" in matched_labels or "branded type" in matched_labels,
          "TS discriminated union snippet matches")

    print("  --- Dye Recipe ---")
    for lang in expected_langs:
        d = _dye_recipe(LOOMS[lang])
        check_eq(d["total_dyes"], 5, f"{lang} 5 dyes in recipe")
        check_eq(len(d["dyes"]), 5, f"{lang} 5 dye entries")
        check(len(d["gradient_suggestion"]) > 0,
              f"{lang} gradient suggestion present")

    print("  --- ASCII Weave Preview ---")
    for lang in expected_langs:
        p = _weave_preview(lang)
        check(len(p) > 0, f"{lang} preview non-empty")
        check("\n" in p, f"{lang} preview is multi-line")
        check(p.startswith("┌") and p.endswith("┘"),
              f"{lang} preview is framed")

    # Deterministic preview
    p1 = _weave_preview("Rust")
    p2 = _weave_preview("Rust")
    check_eq(p1, p2, "weave preview is deterministic per language")

    print("  --- Loom Report ---")
    # Use language override to avoid mutating the live rotation file
    r = loom_report(language="Java", advance=False)
    for key in [
        "tool", "version", "generated_at", "current_language",
        "rotation_index", "next_language", "loom",
        "warp_threads", "weft_threads", "heddles", "shuttles",
        "bobbins", "pattern_books", "thread_library", "density",
        "thread_health", "weave", "dye_recipe", "preview", "vitality",
    ]:
        check_in(key, r, f"report has key '{key}'")
    check_eq(r["tool"], "polyglot-loom", "tool name correct")
    check_eq(r["version"], "1.0.0", "version correct")
    check_eq(r["current_language"], "Java", "language override works")
    check_in("archetype", r["loom"], "report.loom.archetype present")
    check_in("fabric", r["loom"], "report.loom.fabric present")

    print("  --- Loom Tour ---")
    tour = loom_tour()
    check_eq(len(tour["looms"]), 8, "tour covers all 8 looms")
    check_eq(tour["total_looms"], 8, "tour total is 8")
    for entry in tour["looms"]:
        check_in("language", entry, "tour entry has language")
        check_in("archetype", entry, "tour entry has archetype")
        check_in("emoji", entry, "tour entry has emoji")
        check_in("fabric", entry, "tour entry has fabric")

    print("  --- Dye Comparison ---")
    c = dye_comparison("Rust", "Go")
    check_eq(c["language_a"], "Rust", "comparison preserves language_a")
    check_eq(c["language_b"], "Go", "comparison preserves language_b")
    check_in("average_distance", c, "comparison has average_distance")
    check_in("classification", c, "comparison has classification")
    check(c["average_distance"] >= 0, "comparison distance non-negative")
    check(len(c["role_distances"]) >= 4, "comparison has 4+ role distances")

    # Symmetry check
    c1 = dye_comparison("Rust", "Go")
    c2 = dye_comparison("Go", "Rust")
    check_eq(c1["average_distance"], c2["average_distance"],
             "comparison distance is symmetric")

    print("  --- Deterministic Snippet Digest ---")
    r1 = loom_report(language="Rust", advance=False, snippet="let v = vec![1, 2, 3];")
    r2 = loom_report(language="Rust", advance=False, snippet="let v = vec![1, 2, 3];")
    check_eq(r1["weave"]["digest"], r2["weave"]["digest"],
             "same snippet → same weave digest")

    print("  --- Rotation Advance ---")
    cfg_before = load_rotation()
    idx_before = cfg_before["current_index"]
    lang_before = cfg_before["languages"][idx_before]
    _ = loom_report(language=lang_before, advance=True)
    cfg_after = load_rotation()
    idx_after = cfg_after["current_index"]
    check_eq((idx_before + 1) % 8, idx_after,
             "rotation index advanced by 1")
    check_eq(cfg_after["last_language"], lang_before,
             "last_language recorded correctly")

    # Restore rotation file to its original state to avoid pollution
    save_rotation(cfg_before)

    print("  --- Rotation File Resilience ---")
    # Save and reload should be a no-op on the JSON shape
    cfg = load_rotation()
    check_eq(len(cfg["languages"]), 8, "rotation has 8 languages after reload")
    check_in("Rust", cfg["languages"], "Rust in rotation languages")
    check_in("C/C++", cfg["languages"], "C/C++ in rotation languages")

    print("  --- Vitality Score Range ---")
    for lang in expected_langs:
        r = loom_report(language=lang, advance=False)
        check(0.0 <= r["vitality"]["score"] <= 10.0,
              f"{lang} vitality score in [0,10]")
        check_in("classification", r["vitality"],
                 f"{lang} vitality classification present")

    print()
    print(f"  Total: {passed} passed, {len(failures)} failed")
    return failures


__all__ = [
    "TOOL_NAME", "TOOL_VERSION", "LOOMS", "ROTATION_FILE",
    "load_rotation", "save_rotation", "get_current_language",
    "loom_report", "loom_tour", "dye_comparison", "run_tests",
]


if __name__ == "__main__":
    # Allow `python -m polyglot_loom` to also work as `python polyglot_loom/__init__.py`
    print("polyglot_loom is a package; use `python -m polyglot_loom` instead.")