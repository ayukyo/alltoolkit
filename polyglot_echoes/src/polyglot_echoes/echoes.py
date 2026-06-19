#!/usr/bin/env python3
"""
⚡ Polyglot Echoes v1.0

A creative tool that maps each programming language as a temporal
reverberation system — echoes of past innovations that shaped it,
the current resonance it produces, and the shadow it casts into
future possibilities. Every language is a bell struck in the
computation of history: its sound carries forward from predecessors
and reverberates into what comes after.

Creative concept: "When a language is born, it rings with echoes of
all languages that came before it — C's pointer arithmetic, Lisp's
lambda calculus, Smalltalk's message passing. But every language also
casts a shadow forward: the future languages and paradigms it makes
inevitable. Rust echoes C's systems power but with memory safety as
the reverb that removes danger. JavaScript echoes Scheme's functional
roots but amplifies them through the browser's global resonance.
This tool maps those temporal echoes — the past that shaped each
language, the present it occupies, and the future shadow it casts."

Each run:
  1. Reads language_rotation.json, advances current_index
  2. Selects the rotation language
  3. Generates an echo system report:
     - Past Echoes: ancestors and influences (signal sources)
     - Present Resonance: current footprint and strength
     - Future Shadow: what the language makes possible/impossible
     - Reverb Time: how long the language's influence persists
     - Echo Waveform: visual representation of the signal
     - Frequency Spectrum: dominant paradigm frequencies
     - Acoustic Impedance: how easily the language interfaces with others
  4. Updates language_rotation.json

Distinct from existing tools:
  - polyglot_quantum:         quantum mechanics (superposition/entanglement)
  - polyglot_spectrometer:    spectral decomposition (7 bands, barcode)
  - polyglot_resonance:        harmonic relationships (oscilloscope waves)
  - polyglot_meridian:         spectral positioning (design space coordinates)
  - polyglot_constellation:    stellar gravity map (astronomy/navigation)
  - polyglot_vessel:           material essence (pressure/density/buoyancy)
  - polyglot_prism:             wavelength decomposition (physics lab)
  - polyglot_chronology:       geological epochs (deep time)
  - polyglot_tempo:            rhythm patterns (musical beats)
  - polyglot_cartographer:     geopolitical map (spatial/nations)
  - polyglot_harmony:          pairwise compatibility scores (musical intervals)
  - polyglot_resonator:        mental model frames (cognitive philosophy)
  - polyglot_flavor:           sensory tasting notes (sommelier)
  - polyglot_dna:              genetic trait mapping (molecular biology)
  - polyglot_faultline:        error archaeology (seismic)
  - polyglot_ecosystem_map:    ecosystem graph (ecological)
  - polyglot_anomaly:          quirks/gotchas catalog (paradoxes)
  - polyglot_translation:      cultural proverbs (social cargo)
  - polyglot_digest:            syntax-parallel code (spatial syntax)
  - polyglot_chronicle:        daily diary + challenge (temporal)
  - polyglot_signal:            signal semantics (alarm systems)

Polyglot Echoes is about TEMPORAL ACOUSTICS — echoes, reverberation,
frequency response, and acoustic shadow as a lens for understanding
how programming languages carry forward from the past and cast
shadows into the future.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import math
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-echoes"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent
_WORKSPACE_ROOT = _MODULE_DIR.parent
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]


# ─────────────────────────────────────────────────────────────────────────────
# Echo System Database — each language as a temporal echo system
# ─────────────────────────────────────────────────────────────────────────────

ECHO_SYSTEMS: Dict[str, Dict[str, Any]] = {

    "Rust": {
        "past_echoes": [
            ("C/C++",    0.30, "Systems programming, pointer arithmetic, manual memory"),
            ("ML",       0.20, "Algebraic data types, pattern matching, type inference"),
            ("Haskell",  0.15, "Pure functions, monads, lazy evaluation"),
            ("C++ RAII", 0.15, "Resource acquisition is initialization"),
            ("Erlang",   0.10, "Fearless concurrency, message passing"),
            ("Swift",    0.10, "Protocol-oriented programming, Option<T>"),
        ],
        "present_resonance": 8.7,
        "future_shadow": [
            ("Safe Systems",      "Makes systems programming without GC inevitable"),
            ("Linear Types",      "Opens door to affine type systems in mainstream"),
            ("Wasm Native",       "Browser and serverless become one runtime"),
            ("Ownership Economy", "Resource tracking becomes a first-class concern"),
        ],
        "reverb_time": 12.0,
        "frequency_bands": {
            "safety":      0.87,
            "performance": 0.92,
            "expressiveness": 0.78,
            "concurrency": 0.85,
            "abstraction": 0.80,
        },
        "acoustic_impedance": 0.95,
        "echo_description": "Rust rings like a forged steel bell — dense, controlled, every vibration intentional. Its echo carries the weight of C's power without C's danger, the precision of ML's type system without ML's academic distance. The reverb is long and clean: safety that doesn't compromise performance.",
        "echo_glyph": "🔩",
        "waveform_peaks": [1.0, 0.82, 0.91, 0.74, 0.88, 0.65, 0.79, 0.58, 0.83],
        "impedance_materials": ["steel", "iron", "carbon fiber"],
        "shadow_wavelength": "long (decades-scale influence)",
    },

    "Go": {
        "past_echoes": [
            ("C",          0.25, "Procedural style,编译 model, pointers"),
            ("Python",     0.20, "Readability, quick development cycles"),
            ("CSP",        0.20, "Communicating Sequential Processes (Hoare, 1978)"),
            ("Pascal",     0.15, "Declarations, const/immutable philosophy"),
            ("Newsqueak",  0.10, "Concurrent messaging, Squeak origins"),
            ("Limbo",      0.10, "Statically typed, channel-based concurrency"),
        ],
        "present_resonance": 9.1,
        "future_shadow": [
            ("Cloud Native",     "Defines the default language for distributed systems"),
            ("Generics v2",      "Type parameters finally arrive, reshape libraries"),
            ("Go Wasm",          "Browser becomes a valid Go deployment target"),
            ("Structured Logs",  "Standardized structured logging reshapes observability"),
        ],
        "reverb_time": 8.5,
        "frequency_bands": {
            "safety":      0.72,
            "performance": 0.85,
            "expressiveness": 0.75,
            "concurrency": 0.95,
            "abstraction": 0.68,
        },
        "acoustic_impedance": 0.45,
        "echo_description": "Go resonates like a warm brass horn — open, bright, inviting. Its echo is the sound of simplicity amplified: no noise, no excess, just a clear tone that carries far. The reverb is short and clean, the kind of sound that fills a room without overwhelming it. It's the audible expression of goroutines humming in harmony.",
        "echo_glyph": "🐹",
        "waveform_peaks": [1.0, 0.90, 0.85, 0.78, 0.92, 0.88, 0.75, 0.82, 0.70],
        "impedance_materials": ["brass", "copper", "silver"],
        "shadow_wavelength": "medium (cloud-native era, ~10 years)",
    },

    "Swift": {
        "past_echoes": [
            ("Objective-C", 0.30, "Message passing, dynamic dispatch, categories"),
            ("Python",     0.20, "Readability, trailing closures, scriptability"),
            ("Rust",       0.15, "Memory safety, ownership, Option<T>"),
            ("Haskell",    0.12, "Algebraic data types, lazy collections"),
            ("C#",         0.10, "Async/await, generics, LINQ-inspired features"),
            ("Ruby",       0.08, "Blocks and iterators, human-first design"),
            ("D",          0.05, "Compile-time function execution, templates"),
        ],
        "present_resonance": 7.8,
        "future_shadow": [
            ("Swift Wasm",       "Cross-platform without platform-specific toolchains"),
            ("Swift Server",      "Server-side ecosystem matures, compete with Go"),
            ("Embedded Swift",    "Microcontroller programming becomes idiomatic"),
            ("Ownership Syntax",  "Rust-like borrow checker may arrive in Swift 7"),
        ],
        "reverb_time": 7.0,
        "frequency_bands": {
            "safety":      0.88,
            "performance": 0.82,
            "expressiveness": 0.92,
            "concurrency": 0.80,
            "abstraction": 0.90,
        },
        "acoustic_impedance": 0.55,
        "echo_description": "Swift echoes like a crystal glass — bright, clear, resonant with harmonics. Its sound carries Objective-C's bass warmth (the low-frequency rumble of dynamic messaging) but refracted through Python's mid-range clarity. The result is a tone with surprising overtones: protocol-oriented, optional-chained, closure-captured. Each reverb decays gracefully.",
        "echo_glyph": "🦅",
        "waveform_peaks": [1.0, 0.88, 0.76, 0.95, 0.82, 0.70, 0.91, 0.65, 0.78],
        "impedance_materials": ["crystal", "glass", "diamond"],
        "shadow_wavelength": "medium (Apple + cross-platform, ~8 years)",
    },

    "Kotlin": {
        "past_echoes": [
            ("Java",       0.30, "JVM foundation, object orientation, checked exceptions"),
            ("Scala",      0.25, "Pattern matching, implicit conversions, actor model"),
            ("Groovy",     0.15, "Dynamic scripting, DSL builder syntax"),
            ("C#",         0.15, "Extension methods, async/await, null-conditional"),
            ("Python",     0.10, "Readability over ceremony, list comprehensions"),
            (" Gosu",      0.05, "Practical extensibility, configuration-oriented"),
        ],
        "present_resonance": 8.4,
        "future_shadow": [
            ("Kotlin Multiplatform", "Shared code across iOS/Android/Web/Native"),
            ("Ktor Futures",         "Reactive server-side competes with Spring"),
            ("Wasm/Js Target",       "Browser and native blur further"),
            ("Value Classes",        "Performance without boxing reshapes API design"),
        ],
        "reverb_time": 9.0,
        "frequency_bands": {
            "safety":      0.85,
            "performance": 0.80,
            "expressiveness": 0.88,
            "concurrency": 0.82,
            "abstraction": 0.90,
        },
        "acoustic_impedance": 0.50,
        "echo_description": "Kotlin reverberates like a tuned drum — warm, balanced, with a deep bass note grounded in Java's foundation and shimmering overtones from Scala's functional grace. Its echo fills the JVM space with something more expressive, more playful, but still professional. The reverb is medium-long, settling slowly.",
        "echo_glyph": "🟣",
        "waveform_peaks": [1.0, 0.85, 0.92, 0.78, 0.88, 0.80, 0.73, 0.90, 0.68],
        "impedance_materials": ["bronze", "ceramic", "walnut"],
        "shadow_wavelength": "long (multiplatform vision, ~15 years)",
    },

    "TypeScript": {
        "past_echoes": [
            ("JavaScript", 0.35, "Prototype inheritance, dynamic typing, event loop"),
            ("Java",       0.20, "Static types, classes, interfaces, generics"),
            ("C#",         0.15, "TypeScript's original design heavily C#-inspired"),
            ("Python",     0.10, "Duck typing philosophy, readability"),
            ("Haskell",   0.10, "Type inference, discriminated unions"),
            ("Ruby",       0.10, "Symbol literals, method conventions"),
        ],
        "present_resonance": 9.5,
        "future_shadow": [
            ("TypeScript 6.x",   "Validates runtime behavior via static types more deeply"),
            ("WebAssembly",      "TS compiles natively to Wasm, browser becomes optional"),
            ("Server TS",        "Deno/Bun make TS a first-class server runtime"),
            ("AI-Assisted Types", "LLMs write the types; humans write the logic"),
        ],
        "reverb_time": 10.0,
        "frequency_bands": {
            "safety":      0.82,
            "performance": 0.75,
            "expressiveness": 0.88,
            "concurrency": 0.78,
            "abstraction": 0.92,
        },
        "acoustic_impedance": 0.35,
        "echo_description": "TypeScript's echo is the sound of a vast concert hall — thousands of instruments (JavaScript's ecosystem) resonating together under a precise conductor (the type system). The echo is massive, layered, constantly growing. New harmonics emerge as more libraries ship .d.ts files. The reverb is very long and deeply layered.",
        "echo_glyph": "🎓",
        "waveform_peaks": [1.0, 0.95, 0.88, 0.92, 0.85, 0.90, 0.78, 0.88, 0.82],
        "impedance_materials": ["acoustic wood", "cork", "felt"],
        "shadow_wavelength": "very long (web standard, generational)",
    },

    "JavaScript": {
        "past_echoes": [
            ("Scheme",     0.30, "First-class functions, lambda, lexical scope"),
            ("Java",       0.20, "Syntax inspiration, applet-era naming"),
            ("Perl",       0.15, "Regular expressions, string manipulation"),
            ("AWK",        0.10, "Text processing, associative arrays"),
            ("HyperTalk",  0.15, "Natural language style, event-driven scripting"),
            ("Self",       0.10, "Prototype-based objects, morphing behavior"),
        ],
        "present_resonance": 9.8,
        "future_shadow": [
            ("Wasm Runtime",   "JS becomes one of many Wasm-source languages"),
            ("Temporal API",    "Dates and times done right, at last"),
            ("Signal/React",   "Fine-grained reactivity changes framework paradigm"),
            ("WebAssembly",    "JS and Wasm co-exist, JS orchestrates Wasm modules"),
        ],
        "reverb_time": 15.0,
        "frequency_bands": {
            "safety":      0.50,
            "performance": 0.78,
            "expressiveness": 0.90,
            "concurrency": 0.72,
            "abstraction": 0.85,
        },
        "acoustic_impedance": 0.20,
        "echo_description": "JavaScript's echo is the roar of the ocean — deep, continuous, primordial. Born from Scheme's pure water (first-class functions) mixed with Java's sediment (syntax) and HyperTalk's strange tide (natural language events), the result is a sound that fills every beach on Earth. Its echo is everywhere, impossible to ignore, constantly reshaping itself. The reverb is effectively infinite.",
        "echo_glyph": "🌊",
        "waveform_peaks": [1.0, 0.98, 0.95, 0.92, 0.88, 0.94, 0.85, 0.90, 0.87],
        "impedance_materials": ["ocean", "air", "silicon"],
        "shadow_wavelength": "infinite (runs everywhere humans compute)",
    },

    "Java": {
        "past_echoes": [
            ("C/C++",      0.35, "Curly braces, statement syntax, primitive types"),
            ("Objective-C", 0.20, "Message passing syntax (historically), interface philosophy"),
            ("Ada",        0.15, "Strong typing, checked exceptions, package concept"),
            ("Modula-3",   0.15, "Interfaces, primitives, safe concurrency"),
            (" Mesa",      0.10, "X Window System origins, Berkeley/Caldera ties"),
            ("Pascal",    0.05, "Strong typing, structured programming discipline"),
        ],
        "present_resonance": 8.0,
        "future_shadow": [
            ("Project Loom",   "Virtual threads reshape concurrency model entirely"),
            ("Project Valhalla","Value types bring performance close to raw structs"),
            ("Java 25+",       "Pattern matching completes, records become normal"),
            ("GraalVM Native", "AOT compilation enables truly standalone binaries"),
        ],
        "reverb_time": 11.0,
        "frequency_bands": {
            "safety":      0.80,
            "performance": 0.82,
            "expressiveness": 0.70,
            "concurrency": 0.78,
            "abstraction": 0.85,
        },
        "acoustic_impedance": 0.60,
        "echo_description": "Java's echo fills the grand canyon — massive, authoritative, with a long reverb that bounces between canyon walls of enterprise infrastructure. It was the sound that defined 'write once, run anywhere', filling the valley with warm, round tones. The echo carries C's sharp edges but softened by a layer of safety. Generations of software have grown up inside its resonance.",
        "echo_glyph": "☕",
        "waveform_peaks": [1.0, 0.88, 0.80, 0.85, 0.75, 0.82, 0.78, 0.70, 0.84],
        "impedance_materials": ["canyon stone", "granite", "concrete"],
        "shadow_wavelength": "very long (enterprise backbone, generational)",
    },

    "C/C++": {
        "past_echoes": [
            ("C",           0.40, "Procedural programming, manual memory, pointers"),
            ("Simula",      0.20, "Classes, objects, inheritance (the first OOP)"),
            ("BCPL",        0.15, "Curly braces, expression syntax, type system"),
            ("ALGOL",       0.12, "Block structure, lexical scope, grammar"),
            ("Ada",         0.08, "Strong typing, compilation discipline"),
            ("Smalltalk",   0.05, "Object message passing, late binding"),
        ],
        "present_resonance": 9.3,
        "future_shadow": [
            ("C++26 Modules",  "Module system finally arrives, rebuilds compilation model"),
            ("Carbon",         "C++ successor experiment influences direction"),
            ("C/*future*/",    "Undefined behavior boundaries get sharper std"),
            ("HPC Renaissance","Exascale computing keeps C++ relevant at the frontier"),
        ],
        "reverb_time": 20.0,
        "frequency_bands": {
            "safety":      0.40,
            "performance": 0.99,
            "expressiveness": 0.85,
            "concurrency": 0.65,
            "abstraction": 0.88,
        },
        "acoustic_impedance": 0.98,
        "echo_description": "C/C++ is the deepest, most complex echo in computing — a cathedral of sound built over fifty years. Every note ever struck in systems programming echoes within it. C is the bass note: raw, powerful, unfiltered. C++ adds harmonics of abstraction that layer over the fundamental. The reverb is effectively permanent, a sound that will resonate as long as machines execute code.",
        "echo_glyph": "⚙️",
        "waveform_peaks": [1.0, 0.85, 0.78, 0.92, 0.70, 0.88, 0.65, 0.80, 0.75],
        "impedance_materials": ["iron", "stone", "concrete", "lead"],
        "shadow_wavelength": "permanent (foundational infrastructure)",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Echo Analysis Functions
# ─────────────────────────────────────────────────────────────────────────────

def compute_reverb_time(language: str) -> float:
    """Calculate the effective reverb time considering past and future."""
    sys = ECHO_SYSTEMS[language]
    base = sys["reverb_time"]
    present = sys["present_resonance"]
    # Languages with high resonance and long shadows have compounding reverb
    compound = (present / 10.0) * (len(sys["future_shadow"]) / 4.0)
    return round(base * (1.0 + compound * 0.1), 1)


def build_echo_waveform(language: str) -> str:
    """Build an ASCII waveform visualization of the language's echo."""
    sys = ECHO_SYSTEMS[language]
    peaks = sys["waveform_peaks"]
    glyph = sys["echo_glyph"]

    lines = []
    for amplitude in peaks:
        bar_len = int(amplitude * 28)
        bar = "█" * bar_len
        lines.append(f"{bar} {glyph} {amplitude:.2f}")

    return "\n".join(lines)


def load_rotation(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load the language rotation configuration."""
    path = config_path or ROTATION_FILE
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any], config_path: Optional[str] = None) -> None:
    """Save the language rotation configuration."""
    path = config_path or ROTATION_FILE
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────────────────────────────────────
# Core Echo Generation
# ─────────────────────────────────────────────────────────────────────────────

def _select_language(data: Dict[str, Any]) -> str:
    """Select and advance the language based on rotation state."""
    languages: List[str] = data["languages"]
    index: int = data["current_index"]
    selected = languages[index]
    next_index = (index + 1) % len(languages)
    data["current_index"] = next_index
    data["last_language"] = selected
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    return selected


def _build_frequency_spectrum(freq_bands: Dict[str, float]) -> str:
    """Build a frequency band visualization."""
    lines = []
    for band_name, value in sorted(freq_bands.items()):
        filled = int(value * 20)
        bar = "▓" * filled + "░" * (20 - filled)
        lines.append(f"  {band_name:<18} [{bar}] {value:.2f}")
    return "\n".join(lines)


def _build_acoustic_report(sys: Dict[str, Any]) -> str:
    """Build the acoustic impedance and material report."""
    impedance = sys["acoustic_impedance"]
    materials = sys["impedance_materials"]

    impedance_desc = (
        "Very Low" if impedance < 0.3 else
        "Low" if impedance < 0.5 else
        "Medium" if impedance < 0.7 else
        "High" if impedance < 0.85 else
        "Very High"
    )

    lines = [
        f"  Acoustic Impedance: {impedance:.2f} ({impedance_desc})",
        f"  Primary Materials:  {', '.join(materials)}",
        f"  Shadow Wavelength:  {sys['shadow_wavelength']}",
    ]
    return "\n".join(lines)


def _build_echo_summary(language: str, selected: str, data: Dict[str, Any]) -> str:
    """Build the echo analysis summary for the selected language."""
    sys = ECHO_SYSTEMS[selected]
    reverb = compute_reverb_time(selected)
    waveform = build_echo_waveform(selected)
    freq_spectrum = _build_frequency_spectrum(sys["frequency_bands"])
    acoustic_report = _build_acoustic_report(sys)

    past_lines = []
    for source, weight, desc in sys["past_echoes"]:
        bar = "▓" * int(weight * 20) + "░" * (20 - int(weight * 20))
        past_lines.append("    {:<15} {}  {}".format(source, bar, desc))

    future_lines = []
    for concept, future_desc in sys["future_shadow"]:
        future_lines.append("    \u2192 {}: {}".format(concept, future_desc))

    past_echoes_text = "\n".join(past_lines)
    future_shadow_text = "\n".join(future_lines)

    stars = "\u2b50" * int(sys["present_resonance"])
    next_idx = data["current_index"]
    next_lang = ROTATION_ORDER[next_idx] if next_idx < len(ROTATION_ORDER) else ROTATION_ORDER[0]

    report = """
╔══════════════════════════════════════════════════════════════╗
║  \u26a1 POLYGLOT ECHOES \u2014 Language Temporal Reverberation       ║
╠══════════════════════════════════════════════════════════════╣
║  Language:      {:<38}  ║
║  Glyph:          {:<38}  ║
║  Present Power:  {:<38}  ║
╚══════════════════════════════════════════════════════════════╝

🌊 PAST ECHOES
  These ancestors shaped {}'s sound:
{}

💫 PRESENT RESONANCE
  Current Strength: {}/10
  Effective Reverb: {}s

  Frequency Spectrum:
{}

🌑 FUTURE SHADOW
  The influence {} casts forward:
{}

🎵 ECHO CHARACTER
{}

  "{}"

📊 ECHO WAVEFORM
  Visualizing {}'s temporal signal:
{}

🔄 ROTATION STATUS
  Current Index:   {} → {} (next)
  Last Language:   {}
  Updated:         {}
""".format(
        selected, selected,
        sys["echo_glyph"], sys["echo_glyph"],
        stars, stars,
        past_echoes_text,
        selected, past_echoes_text,
        sys["present_resonance"], reverb,
        freq_spectrum,
        selected, future_shadow_text,
        acoustic_report,
        sys["echo_description"],
        selected, waveform,
        data["current_index"], next_lang,
        data["last_language"],
        data["updated_at"],
    )
    return report


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def echoes(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Run the Polyglot Echoes analysis."""
    data = load_rotation(config_path)
    selected = _select_language(data)
    save_rotation(data, config_path)

    sys = ECHO_SYSTEMS[selected]
    reverb = compute_reverb_time(selected)

    past_echoes_out = [
        {"source": src, "weight": w, "description": desc}
        for src, w, desc in sys["past_echoes"]
    ]

    future_shadow_out = [
        {"concept": c, "implication": i}
        for c, i in sys["future_shadow"]
    ]

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": selected,
        "echo_glyph": sys["echo_glyph"],
        "past_echoes": past_echoes_out,
        "present_resonance": sys["present_resonance"],
        "future_shadow": future_shadow_out,
        "reverb_time_seconds": reverb,
        "frequency_bands": sys["frequency_bands"],
        "acoustic_impedance": sys["acoustic_impedance"],
        "impedance_description": (
            "Very Low" if sys["acoustic_impedance"] < 0.3 else
            "Low" if sys["acoustic_impedance"] < 0.5 else
            "Medium" if sys["acoustic_impedance"] < 0.7 else
            "High" if sys["acoustic_impedance"] < 0.85 else
            "Very High"
        ),
        "impedance_materials": sys["impedance_materials"],
        "shadow_wavelength": sys["shadow_wavelength"],
        "echo_description": sys["echo_description"],
        "waveform_peaks": sys["waveform_peaks"],
        "rotation": {
            "current_index": data["current_index"],
            "next_language": ROTATION_ORDER[data["current_index"]] if data["current_index"] < len(ROTATION_ORDER) else ROTATION_ORDER[0],
            "last_language": data["last_language"],
            "updated_at": data["updated_at"],
        },
    }


def run_tests() -> None:
    """Run all tests."""
    import subprocess
    result = subprocess.run(
        ["python3", "-m", "pytest", str(Path(__file__).parent.parent / "tests"), "-v", "--tb=short"],
        capture_output=False,
    )
    raise SystemExit(result.returncode)
