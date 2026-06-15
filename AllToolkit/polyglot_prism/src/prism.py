#!/usr/bin/env python3
"""
🔮 Polyglot Prism v1.0

Spectral Analysis of Programming Languages — each language
decomposes into its constituent "wavelengths": performance,
type safety, concurrency model, memory model, abstraction
level, and ecosystem maturity. The prism reveals what a
language truly contains, beyond syntax.

Creative concept: "When white light passes through a prism, it
splits into a spectrum. When a programming language passes
through the Polyglot Prism, it reveals its true wavelengths.
Rust splits into deep amber (ownership), Go into electric blue
(goroutines), JavaScript into shifting violet (prototypes),
Java into stable green (JVM). This tool breaks down the current
rotation language into its spectral components, producing a
scientific-looking analysis card that would be at home in a
physics lab — but for code."

Distinct from existing tools:
  - polyglot_signal:      signal vocabulary (error handling words)
  - polyglot_digest:      syntax parallels (same code, different syntax)
  - polyglot_translation: cultural idioms/proverbs (social cargo)
  - polyglot_chronology:  geological timeline (deep time epochs)
  - polyglot_harmony:      pair compatibility analysis
  - polyglot_resonator:   mental model differences
  - polyglot_tempo:       rhythm patterns (feel and cadence)
  - polyglot_mood:        emotional personality profiles
  - polyglot_craft:       practical signature patterns
  - polyglot_cartographer: geospatial world map (spatial)
  - polyglot_codex:       literary traditions (wisdom, philosophy)

Prism is about DECOMPOSING a language into measurable
scientific-seeming dimensions — wavelengths, intensities,
spectral peaks — like a spectrograph reading a star's light.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-prism"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent.parent
_WORKSPACE_ROOT = _MODULE_DIR.parent
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]


# ─────────────────────────────────────────────────────────────────────────────
# Spectral Database — wavelength analysis for each language
# Each language has 6 dimensions scored 0-100
# ─────────────────────────────────────────────────────────────────────────────

SPECTRAL_DB: Dict[str, Dict[str, Any]] = {

    "Rust": {
        "spectral_theme": "Deep Amber — Precision Instruments for High-Stakes Environments",
        "prism_description": (
            "Rust's light splits into distinct amber bands: ownership (100), "
            "type safety (98), zero-cost abstractions (95), and fearless "
            "concurrency (90). There is no infrared — Rust never模糊 — "
            "nor ultraviolet — it never over-abstracts."
        ),
        "wavelengths": {
            "performance":          {"score": 96, "label": "Native Performance",      "unit": "W/m²",  "description": "Near-C speed with zero runtime cost"},
            "type_safety":          {"score": 98, "label": "Type Safety",             "unit": "T·s",   "description": "Ownership type system prevents entire bug classes"},
            "concurrency_model":    {"score": 90, "label": "Fearless Concurrency",    "unit": "Gorout/s", "description": "Send+Sync bounds guarantee thread safety"},
            "memory_model":         {"score": 100, "label": "Ownership & Borrowing",  "unit": "Refs",  "description": "No GC, no dangling ptrs, no data races by design"},
            "abstraction_level":    {"score": 85, "label": "Zero-Cost Abstraction",   "unit": "Abstr", "description": "High-level ergonomics compile to optimal machine code"},
            "ecosystem_maturity":   {"score": 72, "label": "Ecosystem Maturity",      "unit": "Crates", "description": "Cargo ecosystem growing rapidly but still maturing"},
        },
        "spectral_peaks": [
            {"wavelength": "ownership",     "description": "The borrow checker is the defining feature — static analysis at compile time"},
            {"wavelength": "lifetimes",     "description": "Lifetime annotations prevent use-after-free at zero runtime cost"},
            {"wavelength": "traits",       "description": "Trait system enables generics, interfaces, and polymorphism without vtables"},
        ],
        "spectral_troughs": [
            {"wavelength": "compile_times", "description": "Rust compiles slowly — a trade-off for runtime safety"},
            {"wavelength": "learning_curve", "description": "Ownership and borrowing have a steep learning curve"},
        ],
        "spectral_color": "🟡",
        "waveform": "▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░",
        "spectral_class": "F-Class Star (Extreme Precision)",
    },

    "Go": {
        "spectral_theme": "Electric Blue — Pragmatic Light for Networked Systems",
        "prism_description": (
            "Go's light is clean electric blue: fast compilation (100), "
            "goroutine concurrency (95), simplicity (90), and garbage "
            "collection (80). There is no ultraviolet — Go resists complexity — "
            "nor infrared — it never drifts into hidden complexity."
        ),
        "wavelengths": {
            "performance":          {"score": 78, "label": "Native Performance",       "unit": "W/m²",  "description": "Good native speed, slightly behind Rust/C"},
            "type_safety":          {"score": 75, "label": "Type Safety",              "unit": "T·s",   "description": "Static types, but no generics until Go 1.18"},
            "concurrency_model":    {"score": 95, "label": "Goroutine Concurrency",   "unit": "Gorout/s", "description": "CSP model with channels — elegant and scalable"},
            "memory_model":         {"score": 80, "label": "GC Memory Management",    "unit": "Refs",  "description": "Mark-sweep GC, pause times managed but present"},
            "abstraction_level":    {"score": 65, "label": "Simple Abstraction",       "unit": "Abstr", "description": "Deliberately minimal — no inheritance, no generics (pre-1.18)"},
            "ecosystem_maturity":   {"score": 92, "label": "Ecosystem Maturity",      "unit": "Modules", "description": "Mature stdlib, huge CNCF ecosystem, Go modules"},
        },
        "spectral_peaks": [
            {"wavelength": "goroutines",    "description": "Lightweight threads, cheap to create, multiplexed onto OS threads"},
            {"wavelength": "channels",     "description": "CSP-style communication — typed, synchronous or buffered"},
            {"wavelength": "simplicity",   "description": "Rob Pike's philosophy: simple syntax, minimal features, fast compile"},
        ],
        "spectral_troughs": [
            {"wavelength": "generics",      "description": "Generics only arrived in Go 1.18 — decades late for some use cases"},
            {"wavelength": "error_handling", "description": "'if err != nil' repeated ad nauseam — no sum types"},
        ],
        "spectral_color": "🔵",
        "waveform": "▓▓▓▓▓▓▓▓░░░░░░░░░░░░░",
        "spectral_class": "A-Class Star (Blue-White Clarity)",
    },

    "Swift": {
        "spectral_theme": "Warm Orange — Elegant Light for Apple Ecosystems",
        "prism_description": (
            "Swift's light glows warm orange: safety (95), expressiveness (92), "
            "performance (85), and native iOS/macOS integration (100). "
            "There is no infrared — Swift is modern, not legacy — "
            "nor ultraviolet — it stays grounded in practical utility."
        ),
        "wavelengths": {
            "performance":          {"score": 85, "label": "Native Performance",       "unit": "W/m²",  "description": "Near-C performance via LLVM, competitive with C++"},
            "type_safety":          {"score": 95, "label": "Type Safety",             "unit": "T·s",   "description": "Optionals, strong type inference, no nil derefs by design"},
            "concurrency_model":    {"score": 88, "label": "Structured Concurrency", "unit": "Gorout/s", "description": "async/await, actors, Sendable — modern concurrency model"},
            "memory_model":         {"score": 82, "label": "ARC Memory Management",  "unit": "Refs",  "description": "Automatic Reference Counting with compile-time cycle detection"},
            "abstraction_level":    {"score": 92, "label": "High Abstraction",        "unit": "Abstr", "description": "Protocols, extensions, generics, high-level ergonomics"},
            "ecosystem_maturity":   {"score": 80, "label": "Ecosystem Maturity",      "unit": "SPM",   "description": "Swift Package Manager growing, strong Apple ecosystem"},
        },
        "spectral_peaks": [
            {"wavelength": "optionals",     "description": "nil safety built into the type system — no null pointer exceptions"},
            {"wavelength": "protocols",      "description": "Protocol-oriented programming — not class inheritance, but composition"},
            {"wavelength": "closures",      "description": "First-class closures with capture semantics, trailing closure syntax"},
        ],
        "spectral_troughs": [
            {"wavelength": "apple_lockin",   "description": "Best ecosystem on Apple platforms — less universal than cross-platform languages"},
            {"wavelength": "abi_stability",  "description": "ABI stability only recent — binary compatibility historically challenging"},
        ],
        "spectral_color": "🟠",
        "waveform": "▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░",
        "spectral_class": "G-Class Star (Warm, Balanced, Reliable)",
    },

    "Kotlin": {
        "spectral_theme": "Royal Purple — Pragmatic Magic on the JVM",
        "prism_description": (
            "Kotlin's light shimmers purple: null safety (95), coroutines (92), "
            "JVM compatibility (100), and pragmatic pragmatism (90). "
            "There is no infrared — Kotlin is modern — "
            "nor ultraviolet — it never abandons JVM roots."
        ),
        "wavelengths": {
            "performance":          {"score": 80, "label": "JVM Performance",         "unit": "W/m²",  "description": "Runs on JVM — performance tied to JIT, generally excellent"},
            "type_safety":          {"score": 95, "label": "Null Safety",             "unit": "T·s",   "description": "Nullable types (?.) make null explicit — eliminates NPEs"},
            "concurrency_model":    {"score": 92, "label": "Coroutines",              "unit": "Gorout/s", "description": "Lightweight coroutines, structured concurrency, non-blocking I/O"},
            "memory_model":         {"score": 80, "label": "JVM Memory (Managed)",    "unit": "Refs",  "description": "Runs on JVM GC — managed memory with Kotlin-specific tuning"},
            "abstraction_level":    {"score": 90, "label": "High Abstraction",        "unit": "Abstr", "description": "Extension functions, DSLs, type-safe builders, coroutines"},
            "ecosystem_maturity":   {"score": 88, "label": "Ecosystem Maturity",      "unit": "Maven", "description": "Full JVM ecosystem access, JetBrains tooling, Android first-class"},
        },
        "spectral_peaks": [
            {"wavelength": "coroutines",     "description": "Structured concurrency with suspend — lighter than threads, safer than callbacks"},
            {"wavelength": "extension_fns",   "description": "Add methods to existing classes without inheritance — the ultimate DSL tool"},
            {"wavelength": "smart_casts",     "description": "Kotlin's compiler tracks type narrowing within blocks — no manual casting"},
        ],
        "spectral_troughs": [
            {"wavelength": "jvm_runtime",     "description": "Requires JVM — Android excepted, not ideal for iOS or WASM"},
            {"wavelength": "compilation",     "description": "Kotlin compilation is slower than Java — a known pain point"},
        ],
        "spectral_color": "🟣",
        "waveform": "▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░",
        "spectral_class": "M-Class Star (Pragmatic Purple Giant)",
    },

    "TypeScript": {
        "spectral_theme": "Deep Indigo — Structural Discipline for Scale",
        "prism_description": (
            "TypeScript's light is disciplined indigo: type safety (90), "
            "scalability (92), JavaScript compatibility (100), and tooling (95). "
            "There is no infrared — TypeScript is not loosely typed — "
            "nor ultraviolet — it transpiles to JS, never truly escaping it."
        ),
        "wavelengths": {
            "performance":          {"score": 70, "label": "Transpiled Performance",  "unit": "W/m²",  "description": "Runs as JavaScript — same V8 optimizations apply"},
            "type_safety":          {"score": 90, "label": "Structural Type Safety",  "unit": "T·s",   "description": "Structural typing, interface segregation, generics — scales well"},
            "concurrency_model":    {"score": 75, "label": "Async/Promise Concurrency", "unit": "Gorout/s", "description": "Promises, async/await, web workers — JS concurrency model"},
            "memory_model":         {"score": 70, "label": "JS Memory (GC)",          "unit": "Refs",  "description": "JavaScript GC — V8 manages memory automatically"},
            "abstraction_level":    {"score": 88, "label": "High Abstraction",        "unit": "Abstr", "description": "Interfaces, generics, conditional types, mapped types, template literal types"},
            "ecosystem_maturity":   {"score": 95, "label": "Ecosystem Maturity",      "unit": "npm",   "description": "Largest package registry on earth — JavaScript's ecosystem"},
        },
        "spectral_peaks": [
            {"wavelength": "structural_types", "description": "Duck typing with explicit interfaces — scales across large codebases"},
            {"wavelength": "generics",        "description": "Parametric polymorphism — generic constraints, conditional types, infer"},
            {"wavelength": "tooling",          "description": "TSServer, tsconfig, declaration files — best IDE support in PL ecosystem"},
        ],
        "spectral_troughs": [
            {"wavelength": "runtime_escape",    "description": "Types erased at runtime — any is always lurking, type assertions bypass safety"},
            {"wavelength": "null_undefined",   "description": "Both null and undefined exist — two 'no value' concepts, not one"},
        ],
        "spectral_color": "📘",
        "waveform": "▓▓▓▓▓▓▓▓░░░░░░░░░░░░░",
        "spectral_class": "B-Class Star (Indigo Giant — Disciplined Scale)",
    },

    "JavaScript": {
        "spectral_theme": "Shifting Violet — Ubiquitous Light of the Web",
        "prism_description": (
            "JavaScript's light is paradoxical violet: universal (100), "
            "dynamic (85), first-class functions (98), prototype-based (90), "
            "and event-loop driven (92). There is no infrared — it never "
            "pretends to be statically typed — nor ultraviolet — it never "
            "over-abstracts from the machine."
        ),
        "wavelengths": {
            "performance":          {"score": 70, "label": "V8 JIT Performance",      "unit": "W/m²",  "description": "V8 JIT compiler produces excellent real-world performance"},
            "type_safety":          {"score": 55, "label": "Dynamic Type Safety",      "unit": "T·s",   "description": "Dynamic types, typeof helps, but entire bug classes exist"},
            "concurrency_model":    {"score": 92, "label": "Event Loop Concurrency",   "unit": "Gorout/s", "description": "Non-blocking event loop, Promises, async/await, web workers"},
            "memory_model":         {"score": 70, "label": "GC Memory (V8)",            "unit": "Refs",  "description": "V8 GC — generational, incremental, optimized but still GC pauses"},
            "abstraction_level":    {"score": 80, "label": "High Abstraction",        "unit": "Abstr", "description": "Closures, prototypes, Proxy, Reflect — powerful meta-programming"},
            "ecosystem_maturity":   {"score": 100, "label": "Ecosystem Maturity",     "unit": "npm",   "description": "Largest ecosystem on earth — 2M+ packages"},
        },
        "spectral_peaks": [
            {"wavelength": "first_class_fns", "description": "Functions as values — store, pass, return, compose — the foundation of FP in JS"},
            {"wavelength": "prototypes",      "description": "Prototype chain — inheritance without classes, objects delegate to other objects"},
            {"wavelength": "event_loop",      "description": "Non-blocking async — the engine that powers the modern web"},
        ],
        "spectral_troughs": [
            {"wavelength": "type_coercion",   "description": "== vs ===, implicit conversions — the most infamous JS footgun"},
            {"wavelength": "global_scope",   "description": "Historically global by default — var, now let/const in module scope"},
        ],
        "spectral_color": "💜",
        "waveform": "▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░",
        "spectral_class": "O-Class Star (Violet Giant — Universal, Paradoxical)",
    },

    "Java": {
        "spectral_theme": "Stable Green — Institutional Light of the Enterprise Campus",
        "prism_description": (
            "Java's light is stable institutional green: portability (100), "
            "JVM ecosystem (98), checked exceptions (75), OOP orthodoxy (80), "
            "and garbage collection (85). There is no infrared — Java is "
            "not going away — nor ultraviolet — it rarely chases trends."
        ),
        "wavelengths": {
            "performance":          {"score": 82, "label": "JVM Performance",         "unit": "W/m²",  "description": "JIT compilation produces excellent long-running performance"},
            "type_safety":          {"score": 85, "label": "Type Safety",            "unit": "T·s",   "description": "Strong static types, checked exceptions, no pointer arithmetic"},
            "concurrency_model":    {"score": 78, "label": "Thread Concurrency",     "unit": "Gorout/s", "description": "Thread-based, synchronized, java.util.concurrent excellent"},
            "memory_model":         {"score": 85, "label": "GC Memory (JVM)",        "unit": "Refs",  "description": "Sophisticated GC with G1, ZGC, Shenandoah — tunable"},
            "abstraction_level":    {"score": 80, "label": "Moderate Abstraction",    "unit": "Abstr", "description": "Interfaces, abstract classes, generics — strong OOP, but verbose"},
            "ecosystem_maturity":   {"score": 98, "label": "Ecosystem Maturity",      "unit": "Maven", "description": "Massive enterprise ecosystem, Spring, Jakarta EE, decades of libs"},
        },
        "spectral_peaks": [
            {"wavelength": "portability",      "description": "Write once, run everywhere — JVM is the ultimate portability layer"},
            {"wavelength": "gc_tuning",        "description": "G1, ZGC, Shenandoah — production-grade GC with pause-time controls"},
            {"wavelength": "enterprise_libs",  "description": "Spring, Hibernate, Kafka, Spark — the enterprise stack"},
        ],
        "spectral_troughs": [
            {"wavelength": "verbosity",        "description": "Boilerplate — getters, setters, checked exceptions, ceremony everywhere"},
            {"wavelength": "checked_exceptions", "description": "Gosling's admitted mistake — error handling noise in caller"},
        ],
        "spectral_color": "🟢",
        "waveform": "▓▓▓▓▓▓▓▓░░░░░░░░░░░░░",
        "spectral_class": "K-Class Star (Stable Green Dwarf — Institutional)",
    },

    "C/C++": {
        "spectral_theme": "Blinding White — Raw Light of the Machine",
        "prism_description": (
            "C/C++'s light is raw white: performance (100), manual control (100), "
            "zero abstraction cost (100), and no safety net (70). "
            "There is no infrared — undefined behavior lurks in the dark — "
            "nor ultraviolet — you are always close to the machine."
        ),
        "wavelengths": {
            "performance":          {"score": 100, "label": "Native Performance",     "unit": "W/m²",  "description": "The benchmark — as fast as hardware allows"},
            "type_safety":          {"score": 55, "label": "Manual Type Safety",     "unit": "T·s",   "description": "Static types but void*, casts, undefined behavior — no net"},
            "concurrency_model":    {"score": 65, "label": "Manual Concurrency",     "unit": "Gorout/s", "description": "Threads, atomics, mutexes — all manual, all error-prone"},
            "memory_model":         {"score": 40, "label": "Manual Memory",           "unit": "Refs",  "description": "malloc/free, no safety — buffer overflows, use-after-free"},
            "abstraction_level":    {"score": 100, "label": "Zero-Cost Abstraction",  "unit": "Abstr", "description": "Templates, constexpr, concepts — high-level without runtime cost"},
            "ecosystem_maturity":   {"score": 98, "label": "Ecosystem Maturity",      "unit": " Conan", "description": "Decades of libraries, Boost, STL, massive C ecosystem"},
        },
        "spectral_peaks": [
            {"wavelength": "zero_cost_abstr", "description": "Templates, RAII, constexpr — abstractions that compile to optimal machine code"},
            {"wavelength": "manual_control",   "description": "Memory layout, allocation, scheduling — you control everything"},
            {"wavelength": "constexpr",        "description": "Compile-time computation — computations that run at compile time, not runtime"},
        ],
        "spectral_troughs": [
            {"wavelength": "undefined_behavior", "description": "UB is the norm, not the exception — buffer overflows, signed overflow, strict aliasing"},
            {"wavelength": "memory_safety",     "description": "No safety net — buffer overflows, double-free, use-after-free are your responsibility"},
        ],
        "spectral_color": "⚪",
        "waveform": "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓",
        "spectral_class": "O-Class Star (White-Blue Giant — Maximum Performance, Maximum Risk)",
    },
}


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


def get_spectral_data(language: str) -> Optional[Dict[str, Any]]:
    """Return the spectral data for a given language, or None."""
    return SPECTRAL_DB.get(language)


def generate_spectral_report(
    rotate: bool = True,
    config_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a spectral analysis report for the current rotation language.

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
            "spectral_theme": str,
            "prism_description": str,
            "wavelengths": Dict[...],
            "spectral_peaks": List[...],
            "spectral_troughs": List[...],
            "spectral_color": str,
            "waveform": str,
            "spectral_class": str,
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

    spectral = SPECTRAL_DB.get(current_language, {})

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": current_language,
        "current_index": old_idx,
        "new_index": new_idx if rotate else None,
        "rotated": rotate,
        "spectral_theme": spectral.get("spectral_theme", "Unknown Theme"),
        "prism_description": spectral.get("prism_description", ""),
        "wavelengths": spectral.get("wavelengths", {}),
        "spectral_peaks": spectral.get("spectral_peaks", []),
        "spectral_troughs": spectral.get("spectral_troughs", []),
        "spectral_color": spectral.get("spectral_color", "⚪"),
        "waveform": spectral.get("waveform", ""),
        "spectral_class": spectral.get("spectral_class", "Unknown Class"),
        "rotation_order": ROTATION_ORDER,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def format_spectral_report(m: Dict[str, Any]) -> str:
    """Format the spectral report as a scientific-looking card."""

    # Build wavelength bars
    wl_lines = []
    for key, val in m["wavelengths"].items():
        score = val["score"]
        bar_len = int(score / 5)  # scale to ~20 chars
        bar = "█" * bar_len + "░" * (20 - bar_len)
        wl_lines.append(
            f"│ {val['label']:<22} │ {bar} │ {score:>3} {val['unit']:<10} │ {val['description']}"
        )

    # Build peak/trough lists
    peak_lines = [
        f"│ 🔺 {p['wavelength']:<16} │ {p['description']}"
        for p in m["spectral_peaks"]
    ]
    trough_lines = [
        f"│ 🔻 {t['wavelength']:<16} │ {t['description']}"
        for t in m["spectral_troughs"]
    ]

    lines = [
        "╔══════════════════════════════════════════════════════════════════════╗",
        "║  🔮  POLYGLOT PRISM — Spectral Analysis of Programming Languages     ║",
        "╠══════════════════════════════════════════════════════════════════════╣",
        f"║  Subject            : {m['spectral_theme']:<49}║",
        f"║  Language           : {m['language']:<49}║",
        f"║  Index              : {m['current_index']:<49}║",
        f"║  Rotated            : {str(m['rotated']):<49}║",
        f"║  {m['spectral_color']} Spectral Class    : {m['spectral_class']:<41}║",
        "╠══════════════════════════════════════════════════════════════════════╣",
        "║  📡  SPECTRAL DESCRIPTION                                          ║",
    ]

    # Word-wrap description
    for line in _wrap_text(m["prism_description"], 62):
        lines.append(f"║  {line:<63}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════════╣",
        "║  📊  WAVELENGTH INTENSITIES                                        ║",
        "║  Dimension                │ ████████████████████ │ Score   Unit      │ Description              ║",
        "╟───────────────────────────────────────────────────────────────────────╢",
    ]
    lines += wl_lines

    lines += [
        "╠══════════════════════════════════════════════════════════════════════╣",
        "║  🔺  SPECTRAL PEAKS (Bright Wavelengths)                            ║",
    ]
    lines += peak_lines if peak_lines else ["║  (no peaks recorded)                                         ║"]

    lines += [
        "╠══════════════════════════════════════════════════════════════════════╣",
        "║  🔻  SPECTRAL TROUGHS (Dim Wavelengths)                             ║",
    ]
    lines += trough_lines if trough_lines else ["║  (no troughs recorded)                                        ║"]

    lines += [
        "╠══════════════════════════════════════════════════════════════════════╣",
        "║  📈  WAVEFORM                                                      ║",
        f"║  {m['waveform']:<63}║",
        "╠══════════════════════════════════════════════════════════════════════╣",
        "║  🔄  ROTATION ORDER                                                 ║",
        f"║  {' → '.join(ROTATION_ORDER):<63}║",
        "╚══════════════════════════════════════════════════════════════════════╝",
    ]
    return "\n".join(lines)


def _wrap_text(text: str, width: int) -> List[str]:
    """Simple word-wrap for long text strings."""
    if not text:
        return [""]
    words = text.split()
    if not words:
        return [""]
    if len(words) == 1 and len(words[0]) > width:
        return [text[i:i+width] for i in range(0, len(text), width)]
    lines = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 <= width:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines if lines else [""]


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
        report = generate_spectral_report()
        print(format_spectral_report(report))
    else:
        print(f"Polyglot Prism v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_prism --test   # Run tests")
        print("  python -m polyglot_prism --report # Generate spectral report")