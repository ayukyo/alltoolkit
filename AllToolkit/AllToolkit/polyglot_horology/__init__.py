#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🕰️ Polyglot Horology v1.0.0
A watchmaking/clockwork engine for programming languages — every language
is treated as a precision timepiece, with movements, mainsprings, escapements,
balance wheels, jewels, gears, plates, bridges, complications, and
chronometric profiles.

Creative concept:
  "Every program tells time. Some languages are grandfather clocks — slow,
   loud, accurate, and meant to outlast generations (Java). Some are
   skeleton tourbillons — every gear visible, every jewel polished, every
   millisecond accounted for (Rust). Some are quartz tickers — battery-
   powered, ubiquitous, near-perfect (Go). Some are digital smartwatches —
   a haptic crown, an OLED dial, a chip-set ecosystem (Swift). Some are
   mechanical chronographs — three sub-dials and a bezel that clicks
   (C/C++). The horologist — the developer — winds the mainspring, oils
   the jewels, assembles the plates, fits the bridges, and produces a
   movement. This tool shows the movement, the escapement, the jewels,
   the dial, the complications, and the timekeeping profile for whichever
   language the rotation has spun to."

Key features:
  1. Movement Catalogue — every language mapped to a watch archetype
  2. Mainspring         — the power source (runtime / language spec)
  3. Escapement         — the cadence (control flow / scheduler)
  4. Balance Wheel       — the regulator (type system / memory model)
  5. Jewels             — anti-friction bearings (primitive types)
  6. Gear Train         — operation pipeline (compile → link → run)
  7. Bridges & Plates   — internal architecture (frameworks, std lib)
  8. Complications      — extra features (async, generics, FFI, GC)
  9. Chronograph        — stopwatch capability (profiling, tracing)
 10. Dial               — the public interface (syntax + idioms)
 11. Crown              — the user input mechanism (REPL / build tool)
 12. Timekeeping Rate   — performance & precision profile
 13. Power Reserve      — runtime longevity (memory / startup)
 14. Movement Tour      — visit all 8 movements in sequence
 15. Chronometer Compare — chronometric comparison between two languages
 16. Rotation Advance   — reads/updates language_rotation.json

Distinct from existing tools:
  - polyglot_loom:    textile / weaving lens
  - polyglot_tempo:   musical rhythm lens
  - polyglot_odyssey: time-travel journey lens
  - polyglot_forge:   metalworking lens
  - polyglot_orbit:   celestial mechanics lens
  - polyglot_metamorphosis: AST transformation lens
  - polyglot_reef:    marine ecosystem lens
  - polyglot_pulse:   vital signs / medical lens
  - polyglot_loom:    warp/weft/cloth lens
  - polyglot_vessel:  alembic / distillation lens

Horology is about WATCHMAKING — movements, escapements, balance wheels,
jewels, mainsprings, gears, bridges, plates, complications, and the precise
art of telling time. No other tool covers this.

Rotation: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import math
import os
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-horology"
TOOL_VERSION = "1.0.0"

# Resolve rotation file at workspace root (one level above AllToolkit/).
ROTATION_FILE = str(
    Path(__file__).parent.parent.parent / "language_rotation.json"
)


# ── Movement catalogue ────────────────────────────────────────────────────────
# Each language is a watch movement archetype. A movement has:
#   archetype         — kind of timepiece (tourbillon, quartz, smart, ...)
#   dial_face         — the public syntax/idioms the user sees
#   mainspring        — power source (the runtime / language spec)
#   escapement        — cadence (control flow / scheduler)
#   balance_wheel     — regulator (type system / memory model)
#   jewels            — anti-friction bearings (primitive types)
#   gear_train        — operation pipeline
#   bridges           — internal architecture pieces
#   plates            — base plate (stdlib, build system)
#   crown             — user input mechanism (REPL, CLI, build tool)
#   complications     — extra features
#   chronograph       — stopwatch capability
#   power_reserve_hr  — runtime longevity
#   beat_rate_vph     — operations per hour (perf)
#   precision         — accuracy / determinism
#   jewel_count       — number of primitives
#   weight_g          — binary / memory footprint
#   water_resist_m    — protection (FFI / isolation)
#   case_material     — the "case" surrounding the movement (tooling)
#   lume_color        — visible glow (debug / print)
#   strap             — what holds the watch to the world (ecosystem)
#   emoji             — species marker
#   maker             — who crafts it
#   year_introduced   — historical era
#   motif             — short craft metaphor
#   caliber           — caliber reference (model designation)

MOVEMENTS: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "archetype": "Skeleton Tourbillon (every gear exposed)",
        "dial_face": "Bare metal movement, jewels visible, no logos, no clutter",
        "motif": "the watchmaker polishes each wheel by hand and you can see every jewel",
        "emoji": "🕰️",
        "maker": "Mozilla Research & open community",
        "year_introduced": 2010,
        "caliber": "RST-001 Tourbillon",
        "mainspring": "Borrow checker + lifetimes (the spring is wound at compile time)",
        "escapement": "Ownership transfer + move semantics (the escapement is strict, no over-winding)",
        "balance_wheel": "Affine type system with lifetime annotations",
        "jewels": [
            "i8", "i16", "i32", "i64", "i128", "isize",
            "u8", "u16", "u32", "u64", "u128", "usize",
            "f32", "f64", "bool", "char", "()", "str", "String",
            "Vec", "HashMap", "Result", "Option", "Box", "Rc", "Arc",
        ],
        "gear_train": "Source → macro expansion → borrow check → MIR → LLVM IR → machine code",
        "bridges": [
            "std::core (the alarm bridge — minimal)",
            "std::alloc (the mainspring barrel)",
            "std::collections (the gear train)",
            "tokio (the chronograph bridge)",
        ],
        "plates": ["Cargo.toml", "Cargo.lock", "target/", "src/"],
        "crown": "cargo build / cargo run / cargo test (the click of a screw-down crown)",
        "complications": [
            "Lifetime ellipsis (the perpetual calendar)",
            "Trait objects & dyn dispatch (the minute repeater)",
            "Async/await (the equation of time)",
            "Macros (the equation of time hand)",
            "Const generics (the moonphase)",
        ],
        "chronograph": "tokio-console, perf, flamegraph (full chronograph with sub-dials)",
        "power_reserve_hr": 70,
        "beat_rate_vph": 28800,  # 8 Hz balance wheel
        "precision": "±0.5s/day (chronometer-grade)",
        "jewel_count": 25,
        "weight_g": 95,
        "water_resist_m": 100,
        "case_material": "AISI 316L stainless — strict, rust-proof",
        "lume_color": "Pale amber (compiler warnings)",
        "strap": "Crates.io — 150,000+ straps available",
        "complication_count": 5,
    },
    "Go": {
        "archetype": "Quartz Field Watch (rugged, ubiquitous, accurate)",
        "dial_face": "High-contrast, sans-serif, minimal clutter",
        "motif": "the watch that goes on every outdoor wrist and never fails",
        "emoji": "⌚",
        "maker": "Google & the open-source community",
        "year_introduced": 2009,
        "caliber": "GO-Q9 Quartz",
        "mainspring": "Goroutine scheduler (the battery never runs out — you spawn another)",
        "escapement": "Goroutines + channels (the escapement is concurrent)",
        "balance_wheel": "Static structural typing with interfaces",
        "jewels": [
            "bool", "byte", "rune", "int", "int8", "int16", "int32", "int64",
            "uint", "uint8", "uint16", "uint32", "uint64", "uintptr",
            "float32", "float64", "complex64", "complex128", "string",
            "error", "interface{}", "struct{}", "chan T",
        ],
        "gear_train": "Source → gofmt → type-check → SSA → machine code",
        "bridges": [
            "net/http (the bezel bridge)",
            "sync (the chronograph bridge)",
            "context (the gmt bridge)",
            "testing (the lume bridge)",
        ],
        "plates": ["go.mod", "go.sum", "pkg/"],
        "crown": "go build / go run / go test (the screw-down crown that everyone uses)",
        "complications": [
            "Goroutines (the split-second chronograph)",
            "Channels (the gmt hand)",
            "Select statement (the countdown bezel)",
            "Defer (the power-reserve indicator)",
            "Generics 1.18+ (the moonphase)",
        ],
        "chronograph": "pprof, go trace, expvar (a precision chronograph)",
        "power_reserve_hr": 100,
        "beat_rate_vph": 32000,  # quartz
        "precision": "±0.1s/day (quartz-grade)",
        "jewel_count": 23,
        "weight_g": 60,
        "water_resist_m": 200,
        "case_material": "Composite polymer — light, durable",
        "lume_color": "Cool green (go test -v output)",
        "strap": "Module proxy — 1M+ modules",
        "complication_count": 5,
    },
    "Swift": {
        "archetype": "Apple Watch Series (digital crown, OLED dial)",
        "dial_face": "Sleek, minimalist, customisable complications",
        "motif": "the watch that pairs with your iPhone and tells you to stand",
        "emoji": "⌚",
        "maker": "Apple Inc.",
        "year_introduced": 2014,
        "caliber": "SWT-A18 Digital Crown",
        "mainspring": "ARC (Automatic Reference Counting) — the spring is automatic",
        "escapement": "Optional chaining + async/await (the escapement never null-crashes)",
        "balance_wheel": "Protocol-oriented static typing",
        "jewels": [
            "Int", "UInt", "Int8", "Int16", "Int32", "Int64",
            "UInt8", "UInt16", "UInt32", "UInt64",
            "Float", "Double", "Bool", "String", "Character",
            "Array", "Dictionary", "Set", "Optional", "Result",
            "Data", "Date", "URL", "UUID",
        ],
        "gear_train": "Source → SIL → IR → LLVM → native (or interpreter for scripting)",
        "bridges": [
            "Foundation (the alarm bridge)",
            "SwiftUI (the dial bridge)",
            "Combine (the chronograph bridge)",
            "SwiftPM (the strap bridge)",
        ],
        "plates": ["Package.swift", ".build/", "Sources/", "Tests/"],
        "crown": "swift build / swift run / xcodebuild (the digital crown)",
        "complications": [
            "Optionals (the gmt hand — never null)",
            "Result builders (the split-second chronograph)",
            "Property wrappers (the moonphase)",
            "Actors (the equation of time)",
            "Generics with protocol witnesses (the perpetual calendar)",
        ],
        "chronograph": "Instruments, XCTest, os.log (a polished Apple chronograph)",
        "power_reserve_hr": 18,  # all-day battery
        "beat_rate_vph": 36000,  # high-frequency quartz
        "precision": "±0.05s/day (chronometer-grade)",
        "jewel_count": 24,
        "weight_g": 50,
        "water_resist_m": 50,
        "case_material": "Aluminium / titanium / ceramic — Apple-curated",
        "lume_color": "Cool blue (print() output)",
        "strap": "SwiftPM + CocoaPods + Carthage — Apple-curated straps",
        "complication_count": 5,
    },
    "Kotlin": {
        "archetype": "Perpetual Calendar Chronograph (auto-adjusts to leap years)",
        "dial_face": "Clean, friendly, modern with playful complications",
        "motif": "the watch that knows what day it is even on Feb 29th",
        "emoji": "🕰️",
        "maker": "JetBrains & the open-source community",
        "year_introduced": 2011,
        "caliber": "KTL-1.9 Perpetual",
        "mainspring": "JVM bytecode + coroutine scheduler",
        "escapement": "Coroutines + structured concurrency",
        "balance_wheel": "Null-safe static typing with smart casts",
        "jewels": [
            "Int", "Long", "Short", "Byte", "Float", "Double",
            "Boolean", "Char", "String", "Array", "List",
            "Map", "Set", "Pair", "Triple", "Sequence",
            "Result", "Flow", "Channel",
        ],
        "gear_train": "Source → kotlinc → JVM bytecode → JIT → native",
        "bridges": [
            "kotlinx.coroutines (the chronograph bridge)",
            "kotlinx.serialization (the gmt bridge)",
            "Jetpack Compose (the dial bridge)",
            "Ktor (the bezel bridge)",
        ],
        "plates": ["build.gradle.kts", "settings.gradle.kts", "gradle/"],
        "crown": "gradle build / gradle test / IDEA (the knurled crown)",
        "complications": [
            "Null safety (the never-empty bobbin)",
            "Coroutines (the gmt hand)",
            "DSL builders (the perpetual calendar)",
            "Sealed classes (the equation of time)",
            "Inline value classes (the moonphase)",
        ],
        "chronograph": "kotlinx-coroutines-debug, IntelliJ profiler (full chronograph)",
        "power_reserve_hr": 80,
        "beat_rate_vph": 28800,
        "precision": "±1s/day (JIT-compiled, near-chronometer)",
        "jewel_count": 19,
        "weight_g": 75,
        "water_resist_m": 100,
        "case_material": "Stainless steel with JVM case-back",
        "lume_color": "Warm orange (compiler hints)",
        "strap": "Maven Central + JetBrains Space",
        "complication_count": 5,
    },
    "TypeScript": {
        "archetype": "Modern Field Watch with Sapphire Crystal (sharp, typed, everywhere)",
        "dial_face": "Crisp, monospace, with explicit type labels",
        "motif": "the watch with AR coating on every glass surface",
        "emoji": "🕰️",
        "maker": "Microsoft & the open-source community",
        "year_introduced": 2012,
        "caliber": "TS-5.4 Sapphire",
        "mainspring": "Type checker as power source — the spring is wound at type-check time",
        "escapement": "Structural typing with strict null checks",
        "balance_wheel": "Type inference + generics + mapped types",
        "jewels": [
            "number", "string", "boolean", "null", "undefined",
            "symbol", "bigint", "any", "unknown", "never", "void",
            "object", "Array<T>", "Record<K,V>", "Partial<T>",
            "Readonly<T>", "Pick<T,K>", "Omit<T,K>",
        ],
        "gear_train": "Source → tsc → type-check → esbuild/swc → JS → V8",
        "bridges": [
            "tsserver (the lsp bridge)",
            "tsc (the gear-train bridge)",
            "tslib (the helpers bridge)",
            "@types/* (the parts bridge)",
        ],
        "plates": ["tsconfig.json", "package.json", "node_modules/"],
        "crown": "tsc / ts-node / deno / bun (a multi-position crown)",
        "complications": [
            "Discriminated unions (the gmt hand)",
            "Mapped types (the perpetual calendar)",
            "Conditional types (the split-second chronograph)",
            "Template literal types (the moonphase)",
            "Satisfies operator (the equation of time)",
        ],
        "chronograph": "tsc --watch, source maps, vscode profiler (modern chronograph)",
        "power_reserve_hr": 60,
        "beat_rate_vph": 32000,
        "precision": "±0.2s/day (very precise)",
        "jewel_count": 18,
        "weight_g": 55,
        "water_resist_m": 100,
        "case_material": "Brushed titanium — modern, light",
        "lume_color": "Cool blue (tsc errors)",
        "strap": "npm + DefinitelyTyped — vast ecosystem",
        "complication_count": 5,
    },
    "JavaScript": {
        "archetype": "Smartwatch with Web-Connected Apps (the wearOS of languages)",
        "dial_face": "Wildly variable — every developer's dial is different",
        "motif": "the watch whose dial changes with every app you install",
        "emoji": "⌚",
        "maker": "The open web — Brendan Eich & the ECMA committee",
        "year_introduced": 1995,
        "caliber": "JS-ES2024 Smart Dial",
        "mainspring": "V8 / SpiderMonkey — the engine winds itself",
        "escapement": "Event loop + microtask queue + macrotask queue",
        "balance_wheel": "Dynamic typing with truthiness rules",
        "jewels": [
            "number", "string", "boolean", "null", "undefined",
            "symbol", "bigint", "object", "Array", "Map",
            "Set", "WeakMap", "WeakSet", "Date", "RegExp",
            "Promise", "Generator", "AsyncIterator",
        ],
        "gear_train": "Source → parser → AST → bytecode → JIT → machine code",
        "bridges": [
            "V8 (the engine bridge)",
            "Node.js (the strap bridge)",
            "Deno (the modern strap)",
            "Bun (the fast strap)",
        ],
        "plates": ["package.json", "package-lock.json", "node_modules/"],
        "crown": "node script.js / deno run / bun run (a side-mounted crown)",
        "complications": [
            "Promise/async-await (the gmt hand)",
            "Proxies (the equation of time)",
            "Generators (the perpetual calendar)",
            "WeakRef (the power-reserve indicator)",
            "Optional chaining (the moonphase)",
        ],
        "chronograph": "console.time, Chrome DevTools, 0x (a Web-grade chronograph)",
        "power_reserve_hr": 24,  # smartwatches need daily charging
        "beat_rate_vph": 28000,
        "precision": "±2s/day (varying by engine)",
        "jewel_count": 18,
        "weight_g": 45,
        "water_resist_m": 30,
        "case_material": "Aluminium — light, ubiquitous",
        "lume_color": "Yellow (console.log)",
        "strap": "npm — 2M+ packages",
        "complication_count": 5,
    },
    "Java": {
        "archetype": "Grandfather Clock (heavy, loud, lasts centuries)",
        "dial_face": "Roman numerals, brass hands, ornate",
        "motif": "the clock that chimes in every office lobby and never stops",
        "emoji": "🕰️",
        "maker": "Sun Microsystems (now Oracle) & the open-source community",
        "year_introduced": 1995,
        "caliber": "JVM-21 Longcase",
        "mainspring": "JVM heap + generational GC (the spring is wound by the user)",
        "escapement": "Thread scheduler + synchronized locks",
        "balance_wheel": "Nominal static typing with class hierarchy",
        "jewels": [
            "byte", "short", "int", "long", "float", "double",
            "boolean", "char", "String", "Object", "List",
            "Map", "Set", "Optional", "Stream", "LocalDate",
            "LocalTime", "LocalDateTime", "Duration", "Instant",
        ],
        "gear_train": "Source → javac → bytecode → classloader → JIT → native",
        "bridges": [
            "java.lang (the mainspring barrel)",
            "java.util (the gear train)",
            "java.io / java.nio (the dial bridge)",
            "java.util.concurrent (the chronograph bridge)",
        ],
        "plates": ["pom.xml", "build.gradle", "META-INF/", "classes/"],
        "crown": "java / javac / mvn / gradle (a heavy brass crown)",
        "complications": [
            "Generics with erasure (the gmt hand)",
            "Concurrency utilities (the chronograph)",
            "Streams (the moonphase)",
            "Records & sealed classes (the equation of time)",
            "Pattern matching (the perpetual calendar)",
        ],
        "chronograph": "JFR, JMX, VisualVM (an enterprise chronograph)",
        "power_reserve_hr": 168,  # a week's uptime
        "beat_rate_vph": 18000,  # slow and steady
        "precision": "±5s/day (but always running)",
        "jewel_count": 20,
        "weight_g": 350,  # heavy grandfather clock
        "water_resist_m": 30,
        "case_material": "Solid oak — decades-long",
        "lume_color": "Pale green (System.out.println)",
        "strap": "Maven Central — 500K+ artifacts",
        "complication_count": 5,
    },
    "C/C++": {
        "archetype": "Marine Chronometer (the original precision timepiece)",
        "dial_face": "Brass, engraved, with detachable seconds bit",
        "motif": "the watch that won longitude prizes and still anchors every system",
        "emoji": "🕰️",
        "maker": "Dennis Ritchie / Bjarne Stroustrup & the original Unix crew",
        "year_introduced": 1972,
        "caliber": "C-ANSI Marine",
        "mainspring": "Manual winding — the developer winds every bobbin",
        "escapement": "Pointer arithmetic + manual memory management",
        "balance_wheel": "Static (C) + template metaprogramming (C++)",
        "jewels": [
            "char", "short", "int", "long", "long long",
            "unsigned char", "unsigned short", "unsigned int", "unsigned long",
            "float", "double", "long double", "_Bool", "void*",
            "std::array", "std::vector", "std::string", "std::map",
        ],
        "gear_train": "Source → preprocessor → compiler → assembler → linker → ELF",
        "bridges": [
            "libc (the mainspring barrel)",
            "STL (the gear train, C++)",
            "POSIX (the bezel bridge)",
            "Boost (the parts bridge)",
        ],
        "plates": ["Makefile", "CMakeLists.txt", "build/", ".o files"],
        "crown": "gcc / g++ / clang / make / cmake (a wind-up crown with no ratchet)",
        "complications": [
            "Preprocessor macros (the equation of time)",
            "Templates & SFINAE (the perpetual calendar)",
            "Move semantics & RAII (the gmt hand)",
            "constexpr (the moonphase)",
            "Concepts C++20 (the chronograph)",
        ],
        "chronograph": "perf, valgrind, gdb (the original Unix chronograph)",
        "power_reserve_hr": 240,  # runs forever if you feed it
        "beat_rate_vph": 14400,  # 4 Hz balance — antique precision
        "precision": "±0.01s/day (marine chronometer-grade)",
        "jewel_count": 19,
        "weight_g": 200,
        "water_resist_m": 300,
        "case_material": "Solid brass — centuries-old",
        "lume_color": "Pale amber (compiler warnings)",
        "strap": "CMake / Conan / vcpkg / apt — established strap-makers",
        "complication_count": 5,
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


def _chronometric_rate(movement: Dict[str, Any]) -> Dict[str, Any]:
    """Compute the chronometric rate of a movement.

    Combines:
      - beat_rate_vph     (precision)
      - precision string  (accuracy class)
      - jewel_count       (anti-friction bearings)

    Returns a chronometric index 0-10 and a class.
    """
    vph = movement["beat_rate_vph"]
    jewels = movement["jewel_count"]
    precision = movement["precision"]

    # Normalize each to [0, 1]
    vph_norm = min(1.0, vph / 36000.0)
    jewel_norm = min(1.0, jewels / 30.0)

    # Map precision string to a score
    precision_score = {
        "±0.01s/day (marine chronometer-grade)": 1.0,
        "±0.05s/day (chronometer-grade)": 0.95,
        "±0.1s/day (quartz-grade)": 0.9,
        "±0.2s/day (very precise)": 0.85,
        "±0.5s/day (chronometer-grade)": 0.8,
        "±1s/day (JIT-compiled, near-chronometer)": 0.7,
        "±2s/day (varying by engine)": 0.5,
        "±5s/day (but always running)": 0.4,
    }.get(precision, 0.5)

    rate = (vph_norm * 0.4 + jewel_norm * 0.3 + precision_score * 0.3) * 10.0

    if rate >= 8.5:
        classification = "🏆 Marine chronometer — extreme precision"
    elif rate >= 7.0:
        classification = "🏅 Chronometer-certified — competition-grade"
    elif rate >= 5.5:
        classification = "⌚ Quality timepiece — daily wear"
    elif rate >= 4.0:
        classification = "🕰️ Field watch — adequate precision"
    else:
        classification = "⏳ Wall clock — gentle accuracy"

    return {
        "beat_rate_vph": vph,
        "jewel_count": jewels,
        "precision_class": precision,
        "precision_score": precision_score,
        "chronometric_index": round(rate, 2),
        "classification": classification,
    }


def _power_reserve_profile(movement: Dict[str, Any]) -> Dict[str, Any]:
    """Compute the power-reserve profile of a movement."""
    power_hr = movement["power_reserve_hr"]
    weight = movement["weight_g"]
    water = movement["water_resist_m"]

    # Normalize each to [0, 1]
    power_norm = min(1.0, power_hr / 240.0)
    weight_norm = 1.0 - min(1.0, weight / 400.0)  # lighter is better
    water_norm = min(1.0, water / 300.0)

    profile = (power_norm * 0.5 + weight_norm * 0.25 + water_norm * 0.25) * 10.0

    if power_hr >= 168:
        era = "🏛️ Heirloom — a week's reserve"
    elif power_hr >= 72:
        era = "⏱️ Weekend — three-day reserve"
    elif power_hr >= 24:
        era = "⌚ Daily — one-day reserve"
    else:
        era = "🪫 Frequent — daily winding"

    return {
        "power_reserve_hr": power_hr,
        "weight_g": weight,
        "water_resist_m": water,
        "profile_index": round(profile, 2),
        "era": era,
    }


def _complication_dial(movement: Dict[str, Any]) -> Dict[str, Any]:
    """Compute the complication dial — which sub-dials and indicators are present."""
    complications = movement["complications"]
    n = len(complications)
    count = movement["complication_count"]

    # Categorize complications (heuristic)
    precision = [c for c in complications if any(k in c.lower() for k in ["lifetime", "type", "static", "compile", "null", "structural", "nominal", "affine", "dynamic", "interface"])]
    concurrency = [c for c in complications if any(k in c.lower() for k in ["goroutine", "async", "await", "actor", "coroutine", "channel", "select", "promise", "thread", "concurrent"])]
    abstraction = [c for c in complications if any(k in c.lower() for k in ["generic", "trait", "protocol", "macro", "template", "constexpr", "concept", "property wrapper", "result builder", "mapped type", "conditional type", "template literal", "satisfies", "sealed", "record", "pattern", "inline"])]

    diversity = sum(1 for c in (precision, concurrency, abstraction) if c)
    strength = min(10.0, n * 1.4 + diversity * 1.2)

    if strength >= 8.5:
        rating = "🏆 Grand complication — haute horlogerie"
    elif strength >= 7.0:
        rating = "🏅 Complicated — multiple sub-dials"
    elif strength >= 5.5:
        rating = "⌚ Standard complications — date and day"
    else:
        rating = "🪶 Minimalist — no date"

    return {
        "complication_count": count,
        "complications": complications,
        "precision_dial": precision,
        "concurrency_dial": concurrency,
        "abstraction_dial": abstraction,
        "diversity_score": diversity,
        "strength_index": round(strength, 2),
        "rating": rating,
    }


def _crown_signature(
    movement: Dict[str, Any],
    snippet: str = "",
    language: Optional[str] = None,
) -> Dict[str, Any]:
    """Detect which crown signature is most relevant for a code snippet.

    Returns the matched complications (up to 2) and a beat-rate reading.
    """
    complications = movement["complications"]

    # No snippet: deterministic fallback picks a single complication
    if not snippet or not snippet.strip():
        seed = _digest(movement["caliber"], "silent")
        chosen = complications[int(seed[0], 16) % len(complications)]
        return {
            "matched": [{"label": "default", "complication": chosen}],
            "beat_rate_reading": "no snippet — movement at rest",
            "line_count": 0,
            "char_count": 0,
            "digest": seed,
        }

    text = snippet.lower()

    # Token-style hints per language for complication matching
    complication_keywords = {
        "Rust": [
            ("lifetime", ["'static", "lifetime", "&'a"]),
            ("trait object", ["dyn ", "trait object", "box<dyn"]),
            ("async/await", ["async", ".await", "tokio"]),
            ("macro", ["#["]),
            ("const generics", ["const n: usize", "const generic"]),
        ],
        "Go": [
            ("goroutine", ["go func", "goroutine"]),
            ("channel", ["chan ", "channel", "make(chan"]),
            ("select", ["select {"]),
            ("defer", ["defer "]),
            ("generics", ["[t any]", "comparable"]),
        ],
        "Swift": [
            ("optional", ["?", "!", "??"]),
            ("result builder", ["@resultbuilder", "@ViewBuilder"]),
            ("property wrapper", ["@state", "@binding", "@published", "propertywrapper"]),
            ("actor", ["actor ", "@mainactor"]),
            ("protocol witness", ["protocol "]),
        ],
        "Kotlin": [
            ("null safety", ["?", "!!"]),
            ("coroutine", ["suspend", "launch", "async"]),
            ("dsl", ["@DslMarker", "builder"]),
            ("sealed", ["sealed class", "sealed interface"]),
            ("inline value", ["@jvminline", "value class"]),
        ],
        "TypeScript": [
            ("discriminated union", ["type ", " | ", "kind:", "tag:"]),
            ("mapped type", ["readonly", "partial", "pick<", "omit<"]),
            ("conditional type", ["extends ?", "infer "]),
            ("template literal", ["`${", "template literal"]),
            ("satisfies", [" satisfies "]),
        ],
        "JavaScript": [
            ("promise/async", ["async", "await", "promise", "then("]),
            ("proxy", ["new proxy", "proxy("]),
            ("generator", ["function*", "yield "]),
            ("weakref", ["weakref", "finalizationregistry"]),
            ("optional chaining", ["?."]),
        ],
        "Java": [
            ("generics with erasure", ["<t>", "generics"]),
            ("concurrent", ["concurrent", "executor", "completablefuture"]),
            ("stream", [".stream(", "stream<"]),
            ("record", ["record "]),
            ("pattern matching", ["switch ", "instanceof ", "pattern"]),
        ],
        "C/C++": [
            ("preprocessor", ["#define", "#include", "macro"]),
            ("template/sfinae", ["template<", "typename ", "enable_if"]),
            ("move/raii", ["std::move", "~class", "destructor"]),
            ("constexpr", ["constexpr"]),
            ("concept", ["concept ", "requires "]),
        ],
    }

    matched = []
    caliber = movement["caliber"]
    # Look up the language key — prefer explicit `language` parameter, then
    # the caliber's prefix, then complication strings
    lang_key = None
    if language and language in complication_keywords:
        lang_key = language
    if lang_key is None:
        for key in complication_keywords.keys():
            if caliber.startswith(key) or key in caliber:
                lang_key = key
                break
    if lang_key is None:
        for c in complications:
            for key in complication_keywords.keys():
                if key.lower() in c.lower():
                    lang_key = key
                    break
            if lang_key:
                break
    if lang_key is None:
        lang_key = list(complication_keywords.keys())[0]

    keyword_table = complication_keywords[lang_key]
    for label, keywords in keyword_table:
        if any(k in text for k in keywords):
            for c in complications:
                if label.lower() in c.lower() or any(k in c.lower() for k in keywords[:1]):
                    matched.append({"label": label, "complication": c})
                    break

    # If nothing matched, fall back to the first complication deterministically
    if not matched:
        seed = _digest(caliber, snippet)
        chosen = complications[int(seed[0], 16) % len(complications)]
        matched.append({"label": "default", "complication": chosen})

    # Beat-rate reading: how fast the snippet seems to run
    lines = snippet.count("\n") + 1
    chars = len(snippet)
    if chars < 200:
        beat = "slow tick — barely moving"
    elif chars < 1000:
        beat = "steady tick — normal rate"
    else:
        beat = "fast tick — high-frequency"

    return {
        "matched": matched[:2],
        "beat_rate_reading": beat,
        "line_count": lines,
        "char_count": chars,
        "digest": _digest(caliber, snippet),
    }


def _dial_face_art(movement: Dict[str, Any]) -> str:
    """Generate a deterministic ASCII dial-face art for the movement."""
    caliber = movement["caliber"]
    digest = _digest("dial", caliber)
    seed_int = int(digest, 16)

    # 12 hour positions
    positions = []
    for i in range(12):
        # pseudo-random bit per position
        bit = (seed_int >> i) & 1
        if i == 0:
            mark = "12"
        elif i % 3 == 0:
            mark = str(i if i <= 6 else 12 - (i - 6))
        else:
            mark = "·" if bit == 0 else "•"
        positions.append(mark)

    # Center: hands (deterministic)
    hour = (seed_int >> 4) & 0xFF
    minute = (seed_int >> 12) & 0xFF
    second = (seed_int >> 20) & 0xFF

    # Build the dial
    width = 25
    height = 11
    grid = [[" "] * width for _ in range(height)]
    cx, cy = width // 2, height // 2

    # Place the 12 markers
    import math
    for i, mark in enumerate(positions):
        angle = (i / 12) * 2 * math.pi - math.pi / 2
        x = int(cx + 10 * math.cos(angle))
        y = int(cy + 4 * math.sin(angle))
        if 0 <= y < height and 0 <= x < width:
            grid[y][x] = mark[0] if len(mark) == 1 else mark

    # Place center dot
    grid[cy][cx] = "✦"

    # Draw a hand to roughly (hour, minute) angle
    h_angle = (hour / 256) * 2 * math.pi - math.pi / 2
    m_angle = (minute / 256) * 2 * math.pi - math.pi / 2
    hx = int(cx + 4 * math.cos(h_angle))
    hy = int(cy + 2 * math.sin(h_angle))
    mx = int(cx + 7 * math.cos(m_angle))
    my = int(cy + 3 * math.sin(m_angle))
    for x, y in [(hx, hy), (mx, my)]:
        if 0 <= y < height and 0 <= x < width:
            grid[y][x] = "○"

    # Frame the dial
    out_lines = []
    out_lines.append("┌" + "─" * width + "┐")
    for row in grid:
        line = "".join(row)
        out_lines.append("│" + line + "│")
    out_lines.append("└" + "─" * width + "┘")
    return "\n".join(out_lines)


# ── Rotation file I/O ─────────────────────────────────────────────────────────

def load_rotation(path: Optional[str] = None) -> Dict[str, Any]:
    """Load language_rotation.json from the resolved path."""
    p = Path(path) if path else Path(ROTATION_FILE)
    if not p.is_absolute():
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
    langs = cfg.get("languages", list(MOVEMENTS.keys()))
    idx = cfg.get("current_index", 0) % len(langs)
    return langs[idx]


# ── Core API ──────────────────────────────────────────────────────────────────

def movement_report(
    language: Optional[str] = None,
    advance: bool = True,
    snippet: str = "",
) -> Dict[str, Any]:
    """
    Generate a movement report for the current rotation language.

    Reads language_rotation.json, picks the language, generates its
    movement archetype, chronometric rate, power-reserve profile,
    complication dial, crown signature, ASCII dial-face art, and
    rotation state. Advances the rotation index by default.

    Args:
        language: override the selected language (for testing)
        advance: whether to advance the rotation index after the call
        snippet: optional code snippet to drive complication matching

    Returns:
        dict containing the movement report and updated rotation state
    """
    cfg = load_rotation()
    langs = cfg.get("languages", list(MOVEMENTS.keys()))

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

    movement = MOVEMENTS[current_lang]
    rate = _chronometric_rate(movement)
    power = _power_reserve_profile(movement)
    complications = _complication_dial(movement)
    crown = _crown_signature(movement, snippet, language=current_lang)
    dial_art = _dial_face_art(movement)

    # Overall movement vitality: average of rate, power, complications
    vitality_components = [
        rate["chronometric_index"] / 10.0,
        power["profile_index"] / 10.0,
        complications["strength_index"] / 10.0,
    ]
    vitality = sum(vitality_components) / len(vitality_components) * 10.0

    if vitality >= 8.5:
        vitality_class = "🏆 Master horologist — grand complication"
    elif vitality >= 7.0:
        vitality_class = "⌚ Skilled horologist — accomplished craft"
    elif vitality >= 5.5:
        vitality_class = "🕰️ Working horologist — solid daily craft"
    elif vitality >= 4.0:
        vitality_class = "🪡 Apprentice horologist — still learning"
    else:
        vitality_class = "🪶 Fragile movement — needs a careful watchmaker"

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "generated_at": _now_iso(),
        "current_language": current_lang,
        "rotation_index": idx,
        "next_language": langs[(idx + 1) % len(langs)],
        "movement": {
            "archetype": movement["archetype"],
            "dial_face": movement["dial_face"],
            "motif": movement["motif"],
            "mainspring": movement["mainspring"],
            "escapement": movement["escapement"],
            "balance_wheel": movement["balance_wheel"],
            "crown": movement["crown"],
            "caliber": movement["caliber"],
            "maker": movement["maker"],
            "year_introduced": movement["year_introduced"],
            "case_material": movement["case_material"],
            "strap": movement["strap"],
            "lume_color": movement["lume_color"],
            "emoji": movement["emoji"],
        },
        "jewels": movement["jewels"],
        "bridges": movement["bridges"],
        "plates": movement["plates"],
        "complications": movement["complications"],
        "chronograph": movement["chronograph"],
        "gear_train": movement["gear_train"],
        "chronometric_rate": rate,
        "power_reserve": power,
        "complication_dial": complications,
        "crown_signature": crown,
        "dial_art": dial_art,
        "vitality": {
            "score": round(vitality, 2),
            "classification": vitality_class,
        },
    }


def movement_tour() -> Dict[str, Any]:
    """Visit all 8 movements in sequence with brief summaries."""
    summary = []
    for lang, m in MOVEMENTS.items():
        rate = _chronometric_rate(m)
        power = _power_reserve_profile(m)
        summary.append({
            "language": lang,
            "emoji": m["emoji"],
            "archetype": m["archetype"],
            "dial_face": m["dial_face"],
            "caliber": m["caliber"],
            "year_introduced": m["year_introduced"],
            "chronometric_class": rate["classification"],
            "power_era": power["era"],
            "complication_count": m["complication_count"],
            "beat_rate_vph": m["beat_rate_vph"],
        })
    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "generated_at": _now_iso(),
        "movements": summary,
        "total_movements": len(summary),
    }


def chronometer_compare(language_a: str, language_b: str) -> Dict[str, Any]:
    """Compare two movements' chronometric profiles."""
    if language_a not in MOVEMENTS or language_b not in MOVEMENTS:
        raise ValueError(f"Unknown language: {language_a} or {language_b}")

    a = MOVEMENTS[language_a]
    b = MOVEMENTS[language_b]

    a_rate = _chronometric_rate(a)
    b_rate = _chronometric_rate(b)
    rate_diff = abs(a_rate["chronometric_index"] - b_rate["chronometric_index"])

    # Compare jewel counts
    jewel_diff = abs(a["jewel_count"] - b["jewel_count"])

    # Compare power reserves
    power_diff = abs(a["power_reserve_hr"] - b["power_reserve_hr"])

    # Compare beat rates
    beat_diff = abs(a["beat_rate_vph"] - b["beat_rate_vph"])

    # Overall distance
    overall = (rate_diff * 0.4 + jewel_diff * 0.1 + power_diff * 0.025 + beat_diff / 3600.0 * 0.4)
    overall = min(10.0, overall)

    if overall < 1.5:
        classification = "🏆 Twin calibers — virtually identical"
    elif overall < 3.0:
        classification = "⌚ Cousin movements — kindred profile"
    elif overall < 5.0:
        classification = "🕰️ Distant movements — different profiles"
    else:
        classification = "⏳ Foreign movements — strikingly different"

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language_a": language_a,
        "language_b": language_b,
        "caliber_a": a["caliber"],
        "caliber_b": b["caliber"],
        "rate_index_a": a_rate["chronometric_index"],
        "rate_index_b": b_rate["chronometric_index"],
        "rate_difference": round(rate_diff, 2),
        "jewel_count_a": a["jewel_count"],
        "jewel_count_b": b["jewel_count"],
        "jewel_difference": jewel_diff,
        "power_reserve_a_hr": a["power_reserve_hr"],
        "power_reserve_b_hr": b["power_reserve_hr"],
        "power_difference_hr": power_diff,
        "beat_rate_a_vph": a["beat_rate_vph"],
        "beat_rate_b_vph": b["beat_rate_vph"],
        "beat_rate_difference_vph": beat_diff,
        "overall_distance": round(overall, 2),
        "classification": classification,
    }


def run_tests() -> List[str]:
    """Run all tests for polyglot_horology.

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
            rn = repr(needle)
            if len(rn) > 60:
                rn = rn[:57] + "..."
            check(False, f"{name} ({rn} not present)")

    print("🕰️ Polyglot Horology v1.0.0 — Running tests")
    print()

    print("  --- Rotation File ---")
    cfg = load_rotation()
    check_eq(len(cfg["languages"]), 8, "8 languages in rotation file")
    check_in("current_index", cfg, "current_index field present")
    check_in("last_language", cfg, "last_language field present")
    check_in("updated_at", cfg, "updated_at field present")

    print("  --- Movement Catalogue ---")
    expected_langs = [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ]
    for lang in expected_langs:
        check_in(lang, MOVEMENTS, f"{lang} has a movement profile")

    for lang, m in MOVEMENTS.items():
        for field in [
            "archetype", "dial_face", "motif", "emoji", "maker",
            "year_introduced", "caliber", "mainspring", "escapement",
            "balance_wheel", "jewels", "bridges", "plates",
            "crown", "complications", "chronograph", "gear_train",
            "power_reserve_hr", "beat_rate_vph", "precision",
            "jewel_count", "weight_g", "water_resist_m",
            "case_material", "lume_color", "strap",
            "complication_count",
        ]:
            check_in(field, m, f"{lang}.{field} present")

        check(len(m["jewels"]) >= 5,
              f"{lang} jewels >= 5")
        check(len(m["bridges"]) >= 2,
              f"{lang} bridges >= 2")
        check(len(m["complications"]) >= 3,
              f"{lang} complications >= 3")
        check(len(m["plates"]) >= 2,
              f"{lang} plates >= 2")
        check(m["jewel_count"] > 0,
              f"{lang} jewel_count > 0")
        check(m["beat_rate_vph"] > 0,
              f"{lang} beat_rate_vph > 0")
        check(m["power_reserve_hr"] > 0,
              f"{lang} power_reserve_hr > 0")
        check(m["year_introduced"] >= 1970,
              f"{lang} year_introduced >= 1970")
        check(len(m["caliber"]) > 0,
              f"{lang} caliber non-empty")
        check(len(m["emoji"]) > 0,
              f"{lang} emoji non-empty")
        check(len(m["case_material"]) > 0,
              f"{lang} case_material non-empty")
        check(len(m["lume_color"]) > 0,
              f"{lang} lume_color non-empty")
        check(len(m["strap"]) > 0,
              f"{lang} strap non-empty")
        check(m["complication_count"] == len(m["complications"]),
              f"{lang} complication_count matches complications list")

    print("  --- Chronometric Rate ---")
    for lang in expected_langs:
        r = _chronometric_rate(MOVEMENTS[lang])
        check_in("chronometric_index", r, f"{lang} rate present")
        check_in("classification", r, f"{lang} rate classification present")
        check(0.0 <= r["chronometric_index"] <= 10.0,
              f"{lang} rate in [0,10]")
        check_eq(r["beat_rate_vph"], MOVEMENTS[lang]["beat_rate_vph"],
                 f"{lang} rate.beat_rate matches movement")

    print("  --- Power Reserve Profile ---")
    for lang in expected_langs:
        p = _power_reserve_profile(MOVEMENTS[lang])
        check_in("profile_index", p, f"{lang} power profile present")
        check_in("era", p, f"{lang} power era present")
        check_eq(p["power_reserve_hr"], MOVEMENTS[lang]["power_reserve_hr"],
                 f"{lang} power_reserve_hr matches movement")
        check(0.0 <= p["profile_index"] <= 10.0,
              f"{lang} profile_index in [0,10]")

    print("  --- Complication Dial ---")
    for lang in expected_langs:
        c = _complication_dial(MOVEMENTS[lang])
        check_in("strength_index", c, f"{lang} complication strength present")
        check_in("rating", c, f"{lang} complication rating present")
        check_eq(c["complication_count"], len(MOVEMENTS[lang]["complications"]),
                 f"{lang} complication_count matches")
        check(c["complication_count"] >= 3,
              f"{lang} complication_count >= 3")
        check(0.0 <= c["strength_index"] <= 10.0,
              f"{lang} complication strength in [0,10]")
        check(len(c["complications"]) >= 3,
              f"{lang} complications list has >= 3 entries")

    print("  --- Crown Signature Detection ---")
    # Each language: with snippet → matched; without → fallback
    for lang in expected_langs:
        c = _crown_signature(MOVEMENTS[lang], "")
        check_in("matched", c, f"{lang} crown.matched present")
        check_in("beat_rate_reading", c, f"{lang} crown.beat_rate_reading present")
        check(len(c["matched"]) >= 1, f"{lang} crown fallback present")

    # Snippet-driven match (Rust async/await)
    c = _crown_signature(MOVEMENTS["Rust"], "async fn fetch() -> Result<String> { reqwest::get(url).await?.text().await }", language="Rust")
    matched_labels = [m["label"] for m in c["matched"]]
    check(any(label in matched_labels for label in ["async/await", "lifetime", "trait object", "macro", "const generics"]),
          "Rust snippet matches a known complication")

    # Snippet-driven match (Go channel)
    c = _crown_signature(MOVEMENTS["Go"], "ch := make(chan int); go func() { ch <- 42 }()", language="Go")
    matched_labels = [m["label"] for m in c["matched"]]
    check(any(label in matched_labels for label in ["goroutine", "channel", "select", "defer", "generics"]),
          "Go channel snippet matches")

    # Snippet-driven match (TS discriminated union)
    c = _crown_signature(MOVEMENTS["TypeScript"], "type Shape = { kind: 'circle' } | { kind: 'square' };", language="TypeScript")
    matched_labels = [m["label"] for m in c["matched"]]
    check(any(label in matched_labels for label in ["discriminated union", "mapped type", "conditional type", "template literal", "satisfies"]),
          "TS discriminated union snippet matches")

    print("  --- Dial Face Art ---")
    for lang in expected_langs:
        art = _dial_face_art(MOVEMENTS[lang])
        check(len(art) > 0, f"{lang} dial art non-empty")
        check("\n" in art, f"{lang} dial art is multi-line")
        check(art.startswith("┌") and art.endswith("┘"),
              f"{lang} dial art is framed")

    # Deterministic art
    art1 = _dial_face_art(MOVEMENTS["Rust"])
    art2 = _dial_face_art(MOVEMENTS["Rust"])
    check_eq(art1, art2, "dial art is deterministic per movement")

    print("  --- Movement Report ---")
    r = movement_report(language="Java", advance=False)
    for key in [
        "tool", "version", "generated_at", "current_language",
        "rotation_index", "next_language", "movement",
        "jewels", "bridges", "plates", "complications",
        "chronograph", "gear_train", "chronometric_rate",
        "power_reserve", "complication_dial", "crown_signature",
        "dial_art", "vitality",
    ]:
        check_in(key, r, f"report has key '{key}'")
    check_eq(r["tool"], "polyglot-horology", "tool name correct")
    check_eq(r["version"], "1.0.0", "version correct")
    check_eq(r["current_language"], "Java", "language override works")
    check_in("archetype", r["movement"], "report.movement.archetype present")
    check_in("dial_face", r["movement"], "report.movement.dial_face present")

    print("  --- Movement Tour ---")
    tour = movement_tour()
    check_eq(len(tour["movements"]), 8, "tour covers all 8 movements")
    check_eq(tour["total_movements"], 8, "tour total is 8")
    for entry in tour["movements"]:
        check_in("language", entry, "tour entry has language")
        check_in("archetype", entry, "tour entry has archetype")
        check_in("emoji", entry, "tour entry has emoji")
        check_in("caliber", entry, "tour entry has caliber")
        check_in("dial_face", entry, "tour entry has dial_face")

    print("  --- Chronometer Comparison ---")
    c = chronometer_compare("Rust", "Go")
    check_eq(c["language_a"], "Rust", "comparison preserves language_a")
    check_eq(c["language_b"], "Go", "comparison preserves language_b")
    check_in("overall_distance", c, "comparison has overall_distance")
    check_in("classification", c, "comparison has classification")
    check(c["overall_distance"] >= 0, "comparison distance non-negative")
    check(c["rate_difference"] >= 0, "comparison rate_difference non-negative")
    check(c["jewel_difference"] >= 0, "comparison jewel_difference non-negative")
    check(c["power_difference_hr"] >= 0, "comparison power_difference non-negative")
    check(c["beat_rate_difference_vph"] >= 0, "comparison beat_rate diff non-negative")

    # Symmetry check
    c1 = chronometer_compare("Rust", "Go")
    c2 = chronometer_compare("Go", "Rust")
    check_eq(c1["overall_distance"], c2["overall_distance"],
             "comparison distance is symmetric")

    print("  --- Deterministic Snippet Digest ---")
    r1 = movement_report(language="Rust", advance=False, snippet="let v = vec![1, 2, 3];")
    r2 = movement_report(language="Rust", advance=False, snippet="let v = vec![1, 2, 3];")
    check_eq(r1["crown_signature"]["digest"], r2["crown_signature"]["digest"],
             "same snippet → same crown signature digest")

    print("  --- Rotation Advance ---")
    cfg_before = load_rotation()
    idx_before = cfg_before["current_index"]
    lang_before = cfg_before["languages"][idx_before]
    _ = movement_report(language=lang_before, advance=True)
    cfg_after = load_rotation()
    idx_after = cfg_after["current_index"]
    check_eq((idx_before + 1) % 8, idx_after,
             "rotation index advanced by 1")
    check_eq(cfg_after["last_language"], lang_before,
             "last_language recorded correctly")

    # Restore rotation file to its original state to avoid pollution
    save_rotation(cfg_before)

    print("  --- Rotation File Resilience ---")
    cfg = load_rotation()
    check_eq(len(cfg["languages"]), 8, "rotation has 8 languages after reload")
    check_in("Rust", cfg["languages"], "Rust in rotation languages")
    check_in("C/C++", cfg["languages"], "C/C++ in rotation languages")

    print("  --- Vitality Score Range ---")
    for lang in expected_langs:
        r = movement_report(language=lang, advance=False)
        check(0.0 <= r["vitality"]["score"] <= 10.0,
              f"{lang} vitality score in [0,10]")
        check_in("classification", r["vitality"],
                 f"{lang} vitality classification present")

    print("  --- All 8 Languages (full reports) ---")
    for lang in expected_langs:
        r = movement_report(language=lang, advance=False)
        check_eq(r["current_language"], lang, f"{lang} full report works")

    print()
    print(f"  Total: {passed} passed, {len(failures)} failed")
    return failures


__all__ = [
    "TOOL_NAME", "TOOL_VERSION", "MOVEMENTS", "ROTATION_FILE",
    "load_rotation", "save_rotation", "get_current_language",
    "movement_report", "movement_tour", "chronometer_compare", "run_tests",
]


if __name__ == "__main__":
    # Allow `python polyglot_horology/__init__.py` to also work
    print("polyglot_horology is a package; use `python -m polyglot_horology` instead.")
