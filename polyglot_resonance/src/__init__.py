#! /usr/bin/env python3
"""
🎵 Polyglot Resonance v1.0
A creative tool that maps how programming concepts "resonate" differently
across the language spectrum — as harmonic frequency shifts and phase distortions.

Creative concept: "Every language vibrates at a different frequency. When you
translate the same concept between languages, each step introduces a 'frequency
shift' — a subtle distortion of the original signal. Polyglot Resonance maps
these shifts as harmonic overtones on an oscilloscope-style display, revealing
which languages are 'in tune' with each other and which create dissonance."

Each run selects the current rotation language and maps a "resonance theme"
(a universal programming concept) as:
  1. A "fundamental frequency" — how this language handles the concept
  2. Harmonic overtones — how the same concept sounds in other languages
  3. An ASCII oscilloscope visualization — the "waveform" of that concept
  4. In-tune / Dissonant classification

Distinct from existing tools:
  - polyglot_dna:           genetic trait mapping (static molecular traits)
  - polyglot_meridian:      spectral positioning (coordinates in design space)
  - polyglot_resonator:     thinking philosophy (mental models & cognitive frames)
  - polyglot_signal:        signal semantics (alarm systems for conditions)
  - polyglot_craft:         practical skill cards (patterns, gotchas, exercises)
  - polyglot_harmony:       pairwise compatibility scores
  - language_archaeology:   historical lineage (temporal origin)
  - language_compass:       learning journey maps (future milestones)
  - polyglot_chronicle:     daily diary + today's challenge (temporal today)
  - polyglot_digest:        syntax-parallel code snippets (spatial syntax)

Polyglot Resonance is about CONCEPTUAL FREQUENCY SHIFT — how the same
universal programming concept vibrates at different frequencies in each
language, visualized as harmonic waveforms and phase distortions.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import math
import random
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-resonance"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
    "language_rotation.json"
)

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ─────────────────────────────────────────────────────────────────────────────
# Resonance Themes — each is a universal programming concept
# ─────────────────────────────────────────────────────────────────────────────
# Each theme has:
#   - id / name / emoji
#   - fundamental: what "perfect" resonance (no shift) looks like
#   - per-language "frequency" and "phase" characterizing how that language
#     vibrates on this concept
#   - overtone_series: how the concept's expression differs across languages
#   - dissonance_triggers: specific language pairs that create dissonance on this theme

RESONANCE_THEMES: List[Dict[str, Any]] = [
    {
        "id": "state_mutation",
        "name": "State Mutation",
        "emoji": "🔄",
        "question": "How does the language handle changing state?",
        "fundamental_hz": 440.0,  # A4 — "perfect" mutable state reference
        "languages": {
            "Rust":       {"hz": 432.0, "phase": 0.0,  "wave": "sine",     "description": "Ownership-guarded mutation — must borrow or move"},
            "Go":         {"hz": 438.0, "phase": 0.05, "wave": "triangle", "description": "Shared mutation via pointers — mutex for sync"},
            "Swift":      {"hz": 436.0, "phase": 0.02, "wave": "sine",     "description": "Copy-on-write structs — mutation via explicit mutating"},
            "Kotlin":     {"hz": 437.0, "phase": 0.03, "wave": "triangle", "description": "var/val distinction — val is immutable reference"},
            "TypeScript": {"hz": 439.0, "phase": 0.06, "wave": "sawtooth", "description": "Objects are always mutable — const guard only the reference"},
            "JavaScript": {"hz": 440.0, "phase": 0.08, "wave": "sawtooth", "description": "Everything mutable by default — no guard"},
            "Java":       {"hz": 435.0, "phase": 0.04, "wave": "square",   "description": "References are mutable; primitives are immutable values"},
            "C/C++":      {"hz": 428.0, "phase": 0.10, "wave": "sawtooth", "description": "Raw pointers allow unrestricted mutation — UB on aliasing"},
        },
        "dissonance_pairs": [
            ("Rust", "JavaScript", "Rust's ownership vs JS's unbridled mutation — maximum dissonance"),
            ("C/C++", "Kotlin",    "C++ pointers bypass all aliasing rules; Kotlin's immutability is compile-time enforced"),
        ],
    },
    {
        "id": "null_handling",
        "name": "Absence / Null",
        "emoji": "🌑",
        "question": "How does the language represent the absence of a value?",
        "fundamental_hz": 264.0,  # C4 — the "null" note (silence)
        "languages": {
            "Rust":       {"hz": 256.0, "phase": 0.0,  "wave": "sine",     "description": "Option<T> — Some(T) or None. Compile-time enforced exhaustive matching."},
            "Go":         {"hz": 260.0, "phase": 0.12, "wave": "triangle", "description": "(T, ok) map pattern + nil for pointers/interfaces — zero-value ambiguity"},
            "Swift":      {"hz": 258.0, "phase": 0.02, "wave": "sine",     "description": "Optional<T> — nil is distinct from a value. if let / guard let."},
            "Kotlin":     {"hz": 259.0, "phase": 0.03, "wave": "triangle", "description": "Nullable T? — null-safe calls (?.) and elvis (?:). Non-null by default."},
            "TypeScript": {"hz": 263.0, "phase": 0.07, "wave": "sawtooth", "description": "undefined | null — optional chaining (?.) + nullish coalescing (??)."},
            "JavaScript": {"hz": 264.0, "phase": 0.09, "wave": "sawtooth", "description": "undefined vs null — two distinct absence values. typeof lies about null."},
            "Java":       {"hz": 262.0, "phase": 0.05, "wave": "square",   "description": "null as absence (unsafe) + Optional<T> (Java 8+) for typesafe alternative."},
            "C/C++":      {"hz": 240.0, "phase": 0.15, "wave": "sawtooth", "description": "NULL (0) / nullptr (C++11) — no Option type, no compile-time enforcement."},
        },
        "dissonance_pairs": [
            ("Rust", "JavaScript", "Rust's Option<T> vs JS's undefined — one is compile-time proven, the other is a runtime footgun"),
            ("C/C++", "Swift",      "C++ nullptr vs Swift's Optional — no safe navigation in C++"),
        ],
    },
    {
        "id": "error_recovery",
        "name": "Error Recovery",
        "emoji": "⚡",
        "question": "How does the language signal and recover from failure?",
        "fundamental_hz": 528.0,  # C5 — "love" frequency for healing
        "languages": {
            "Rust":       {"hz": 520.0, "phase": 0.0,  "wave": "sine",     "description": "Result<T, E> — no exceptions. ? propagates. Exhaustive matching."},
            "Go":         {"hz": 526.0, "phase": 0.06, "wave": "triangle", "description": "error interface — returned as last value. nil = no error."},
            "Swift":      {"hz": 522.0, "phase": 0.02, "wave": "sine",     "description": "throws + Error protocol — try/catch with exhaustive catch blocks."},
            "Kotlin":     {"hz": 524.0, "phase": 0.03, "wave": "triangle", "description": "No checked exceptions. runCatching { } returns Result<T>. "},
            "TypeScript": {"hz": 527.0, "phase": 0.08, "wave": "sawtooth", "description": "throw + try/catch — throw any type, types erased at runtime."},
            "JavaScript": {"hz": 528.0, "phase": 0.10, "wave": "sawtooth", "description": "throw + try/catch — unhandled promise rejections are silent failures."},
            "Java":       {"hz": 518.0, "phase": 0.05, "wave": "square",   "description": "Checked + unchecked exceptions — compiler enforces throws clause."},
            "C/C++":      {"hz": 500.0, "phase": 0.14, "wave": "sawtooth", "description": "Return codes + errno (C) | exceptions (C++, opt-in) — no type safety."},
        },
        "dissonance_pairs": [
            ("Rust", "JavaScript", "Rust's Result<T,E> vs JS's throw — one is a value, the other is a control flow jump"),
            ("Java", "Kotlin",     "Java's checked exceptions vs Kotlin's un-checked — callers must handle differently"),
        ],
    },
    {
        "id": "concurrency_model",
        "name": "Concurrency Model",
        "emoji": "🧵",
        "question": "How does the language handle parallel work?",
        "fundamental_hz": 880.0,  # A5 — high-energy parallel processing
        "languages": {
            "Rust":       {"hz": 872.0, "phase": 0.0,  "wave": "sine",     "description": "Send/Sync traits — compile-time data race prevention. async/await."},
            "Go":         {"hz": 878.0, "phase": 0.04, "wave": "triangle", "description": "Goroutines + channels — CSP model, cheap threads, select."},
            "Swift":      {"hz": 876.0, "phase": 0.02, "wave": "sine",     "description": "async/await + actors (Swift 6) — data race safety by construction."},
            "Kotlin":     {"hz": 877.0, "phase": 0.03, "wave": "triangle", "description": "Coroutines (suspend) + Flow — structured concurrency."},
            "TypeScript": {"hz": 879.0, "phase": 0.07, "wave": "sawtooth", "description": "async/await + Promise.all — single-threaded event loop."},
            "JavaScript": {"hz": 880.0, "phase": 0.09, "wave": "sawtooth", "description": "Single-threaded event loop. Promises queue microtasks."},
            "Java":       {"hz": 874.0, "phase": 0.05, "wave": "square",   "description": "Threads + CompletableFuture + virtual threads (Java 21+)."},
            "C/C++":      {"hz": 860.0, "phase": 0.12, "wave": "sawtooth", "description": "std::thread + std::async + atomics — manual thread lifecycle."},
        },
        "dissonance_pairs": [
            ("Go", "JavaScript", "Goroutines are cheap parallel threads; JS event loop is single-threaded — fundamentally different concurrency models"),
            ("Rust", "C/C++",    "Rust's Send/Sync enforce memory safety at compile time; C++ threads have no such guarantees"),
        ],
    },
    {
        "id": "generics_polymorphism",
        "name": "Generics / Polymorphism",
        "emoji": "🎭",
        "question": "How does the language achieve code reuse across types?",
        "fundamental_hz": 639.0,  # D5 — polymorphic versatility
        "languages": {
            "Rust":       {"hz": 630.0, "phase": 0.0,  "wave": "sine",     "description": "Traits as bounds — T: Trait. Homogeneous generic monomorphization."},
            "Go":         {"hz": 636.0, "phase": 0.10, "wave": "triangle", "description": "No generics pre-1.18. interfaces for duck typing. Generics are limited."},
            "Swift":      {"hz": 633.0, "phase": 0.02, "wave": "sine",     "description": "Generics with protocol constraints. Homogeneous via type parameters."},
            "Kotlin":     {"hz": 634.0, "phase": 0.03, "wave": "triangle", "description": "Declaration-site variance (out/in). Reified generics via inline."},
            "TypeScript": {"hz": 637.0, "phase": 0.06, "wave": "sawtooth", "description": "Structural typing + conditional types — erasure at runtime."},
            "JavaScript": {"hz": 639.0, "phase": 0.08, "wave": "sawtooth", "description": "No compile-time types. Duck typing via objects. No monomorphization."},
            "Java":       {"hz": 632.0, "phase": 0.05, "wave": "square",   "description": "Type erasure + bounded wildcards (? extends T). Homogeneous."},
            "C/C++":      {"hz": 618.0, "phase": 0.14, "wave": "sawtooth", "description": "Templates with SFINAE + concepts (C++20). Monomorphization at compile."},
        },
        "dissonance_pairs": [
            ("C/C++", "JavaScript", "C++ templates vs JS duck typing — one is compile-time, the other is runtime-only"),
            ("Rust", "Go",           "Rust traits vs Go interfaces — Rust has bounds and associated types; Go's interfaces are structural"),
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Waveform generators
# ─────────────────────────────────────────────────────────────────────────────

def _sine(t: float) -> float:
    return math.sin(2 * math.pi * t)


def _triangle(t: float) -> float:
    v = 2 * (t % 1.0)
    return 2 * v - 1.0 if v < 1.0 else 2 * (2 - v) - 1.0


def _square(t: float) -> float:
    return 1.0 if (t % 1.0) < 0.5 else -1.0


def _sawtooth(t: float) -> float:
    return 2 * (t % 1.0) - 1.0


WAVE_FUNCTIONS = {
    "sine":     _sine,
    "triangle": _triangle,
    "square":   _square,
    "sawtooth": _sawtooth,
}


def _build_waveform(
    hz: float,
    phase: float,
    wave: str,
    fundamental_hz: float,
    width: int = 60,
    amplitude: int = 10,
) -> str:
    """
    Build a horizontal ASCII waveform string.

    The waveform is a superposition of the fundamental + the language's frequency
    (creating harmonic overtones). The phase offset shifts the waveform.
    """
    fundamental_amp = amplitude * 0.6
    overtone_amp   = amplitude * 0.3
    noise_amp      = amplitude * 0.1

    wave_fn = WAVE_FUNCTIONS.get(wave, _sine)
    lines: List[str] = []

    # One full cycle at the language's frequency
    # We show multiple cycles across the width
    cycles = 2  # show 2 full cycles
    steps = width
    chars = [" "] * width

    # Track max/min for normalisation
    vals: List[float] = []
    for i in range(steps):
        t = (i / steps) * cycles
        # Fundamental frequency component
        f_t = t * fundamental_hz + phase * 0.0
        # Language frequency component (creates overtones when different)
        l_t = t * hz + phase
        # Mix them (beats/interference pattern)
        f_val = math.sin(2 * math.pi * f_t)
        l_val = wave_fn(t * (hz / fundamental_hz) + phase)
        val = fundamental_amp * f_val + overtone_amp * l_val
        # Add slight noise for realism
        noise = (hash((i, int(hz))) % 1000) / 1000.0 - 0.5
        val += noise_amp * noise * 0.3
        vals.append(val)

    min_v, max_v = min(vals), max(vals)
    span = max_v - min_v if max_v > min_v else 1.0

    # Centre line index (amplitude from centre)
    centre = amplitude

    for i in range(steps):
        t = (i / steps) * cycles
        f_t = t * fundamental_hz + phase * 0.0
        l_t = t * hz + phase
        f_val = math.sin(2 * math.pi * f_t)
        l_val = wave_fn(t * (hz / fundamental_hz) + phase)
        val = fundamental_amp * f_val + overtone_amp * l_val
        noise = (hash((i, int(hz))) % 1000) / 1000.0 - 0.5
        val += noise_amp * noise * 0.3

        # Map to character row
        # amplitude maps from centre, so row = centre - val
        row_float = centre - (val / span) * amplitude
        row = max(0, min(amplitude * 2, int(round(row_float))))

        for j in range(amplitude * 2 + 1):
            mark = " "
            if j == centre:
                mark = "─"
            elif j == row:
                mark = "●"
            elif j > centre and j == centre + 1 and row > centre:
                mark = "│"
            elif j < centre and j == centre - 1 and row < centre:
                mark = "│"
            if j == amplitude * 2:
                mark = " "
            if mark != " ":
                chars[i] = mark
                break

    # Re-do more carefully: just draw the wave line
    chars = [" "] * width
    for i in range(steps):
        t = (i / steps) * cycles
        f_val = math.sin(2 * math.pi * t * fundamental_hz / fundamental_hz)
        l_val = wave_fn(t * (hz / fundamental_hz) + phase)
        val = fundamental_amp * f_val + overtone_amp * l_val
        row_float = centre - (val / span) * amplitude
        row = max(0, min(amplitude * 2, int(round(row_float))))
        chars[i] = "█" if row == centre else ("╿" if row < centre and abs(row - centre) < 3 else ("╽" if row > centre and abs(row - centre) < 3 else " "))
        # Actually just use simple dot on wave
    # Better approach: centre-line with wave peaks
    chars = [" "] * width
    for i in range(steps):
        t = (i / steps) * cycles
        f_val = math.sin(2 * math.pi * t)
        l_val = wave_fn(t * (hz / fundamental_hz) + phase)
        val = fundamental_amp * f_val + overtone_amp * l_val
        row_float = centre - (val / span) * amplitude
        row = max(0, min(amplitude * 2, int(round(row_float))))
        chars[i] = "│" if row == centre else ("●" if row != centre else "─")

    return "".join(chars)


def _draw_oscilloscope(
    fund_hz: float,
    lang_hz: float,
    lang_phase: float,
    wave: str,
    width: int = 60,
    height: int = 9,
) -> List[str]:
    """
    Draw a multi-line oscilloscope display with the waveform centered.
    """
    wave_fn = WAVE_FUNCTIONS.get(wave, _sine)
    cycles = 2
    rows: List[List[str]] = [[" "] * width for _ in range(height)]
    centre_row = height // 2

    for i in range(width):
        t = (i / width) * cycles
        f_val = math.sin(2 * math.pi * t)
        l_val = wave_fn(t * (lang_hz / fund_hz) + lang_phase)
        val = 0.6 * f_val + 0.4 * l_val  # blend fundamental + overtone

        # Map val [-1, 1] to row indices
        row_float = centre_row - val * (centre_row - 1)
        row = max(0, min(height - 1, int(round(row_float))))

        for r in range(height):
            if r == centre_row:
                rows[r][i] = "─"
            elif r == row:
                rows[r][i] = "●"
            elif r > row and r == row + 1:
                rows[r][i] = "│"
            elif r < row and r == row - 1:
                rows[r][i] = "│"
            else:
                rows[r][i] = " "

    # Clean up: remove isolated dots that aren't part of wave
    for r in range(height):
        for i in range(width):
            if rows[r][i] == "●":
                # Check if adjacent to another ● or to centre
                left  = rows[r][i-1] if i > 0 else " "
                right = rows[r][i+1] if i < width-1 else " "
                if left not in ("●", "─", "│") and right not in ("●", "─", "│"):
                    rows[r][i] = " "

    return ["".join(row) for row in rows]


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

def resonance() -> Dict[str, Any]:
    """
    Main entry point: advance rotation, pick a resonance theme,
    and return the full resonance analysis.
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

    # Pick a theme — cycle through them deterministically
    theme_idx = current_index % len(RESONANCE_THEMES)
    theme = RESONANCE_THEMES[theme_idx]

    result = generate_resonance_analysis(current_language, theme, languages)
    result["rotation_advanced"] = True
    result["next_language"] = languages[next_index]
    result["next_index"] = next_index
    return result


def generate_resonance_analysis(
    language: str,
    theme: Dict[str, Any],
    languages: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Generate resonance analysis for a language + theme combination."""
    langs = languages or ROTATION_ORDER
    theme_langs = theme.get("languages", {})

    if language not in theme_langs:
        raise ValueError(f"Language '{language}' not in theme '{theme['id']}'")

    lang_info = theme_langs[language]
    fund_hz = theme.get("fundamental_hz", 440.0)

    # Build waveform
    wave_rows = _draw_oscilloscope(
        fund_hz=fund_hz,
        lang_hz=lang_info["hz"],
        lang_phase=lang_info["phase"],
        wave=lang_info["wave"],
    )

    # Build overtone series for all languages on this theme
    overtones: List[Dict[str, Any]] = []
    for lang in langs:
        if lang not in theme_langs:
            continue
        info = theme_langs[lang]
        freq_ratio = round(info["hz"] / fund_hz, 4)
        # Classify as in-tune / dissonant
        phase_diff = abs(info["phase"] - lang_info["phase"])
        hz_diff = abs(info["hz"] - lang_info["hz"])
        if hz_diff < 3.0 and phase_diff < 0.05:
            resonance_type = "in_tune"
        elif hz_diff > 15.0 or phase_diff > 0.10:
            resonance_type = "dissonant"
        else:
            resonance_type = "harmonic"
        overtones.append({
            "language": lang,
            "frequency_hz": info["hz"],
            "frequency_ratio": freq_ratio,
            "phase_offset": info["phase"],
            "wave_type": info["wave"],
            "description": info["description"],
            "resonance_type": resonance_type,
        })

    # Build dissonance pairs for this theme
    dissonances: List[Dict[str, Any]] = []
    for a, b, reason in theme.get("dissonance_pairs", []):
        if a == language or b == language:
            dissonances.append({
                "pair": [a, b],
                "reason": reason,
            })

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": language,
        "theme": {
            "id": theme["id"],
            "name": theme["name"],
            "emoji": theme["emoji"],
            "question": theme["question"],
            "fundamental_hz": fund_hz,
        },
        "language_resonance": {
            "frequency_hz": lang_info["hz"],
            "frequency_ratio": round(lang_info["hz"] / fund_hz, 4),
            "phase_offset": lang_info["phase"],
            "wave_type": lang_info["wave"],
            "description": lang_info["description"],
        },
        "waveform_display": wave_rows,
        "overtones": overtones,
        "dissonance_pairs": dissonances,
        "rotation_order": ROTATION_ORDER,
    }


def format_resonance(m: Dict[str, Any]) -> str:
    """Format the resonance analysis as a human-readable string."""
    lang = m["language"]
    theme = m["theme"]
    lang_res = m["language_resonance"]
    wave_rows = m["waveform_display"]

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  🎵 POLYGLOT RESONANCE — Concept Frequency Cartography           ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Language     : {lang:<48}║",
        f"║  Theme        : {theme['emoji']} {theme['name']:<44}║",
        f"║  Question     : {theme['question']:<45}║",
        f"║  Fundamental  : {theme['fundamental_hz']} Hz{' ' * 38}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  📡 WAVEFORM DISPLAY                                            ║",
    ]

    for row in wave_rows:
        lines.append(f"║  {row} ║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🎼 LANGUAGE RESONANCE                                          ║",
        f"║  Frequency   : {lang_res['frequency_hz']} Hz (ratio {lang_res['frequency_ratio']}){' ' * 20}║",
        f"║  Wave type   : {lang_res['wave_type']:<44}║",
        f"║  Phase offset: {lang_res['phase_offset']:<44}║",
        f"║  Description : {lang_res['description']:<45}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🎵 OVERTONE SERIES                                            ║",
    ]

    for ot in m["overtones"]:
        emoji = {"in_tune": "🎶", "harmonic": "🎵", "dissonant": "💥"}.get(ot["resonance_type"], "🎵")
        lines.append(
            f"║  {emoji} {ot['language']:<12} {ot['frequency_hz']}Hz "
            f"(×{ot['frequency_ratio']}) phase={ot['phase_offset']:.2f} [{ot['resonance_type']}]"
        )
        lines.append(f"║         {ot['description']:<50}║")

    if m["dissonance_pairs"]:
        lines += [
            "╠══════════════════════════════════════════════════════════════════╣",
            "║  💥 DISSONANCE TRIGGERS                                         ║",
        ]
        for dp in m["dissonance_pairs"]:
            lines.append(f"║  {dp['pair'][0]} ↔ {dp['pair'][1]}: {dp['reason']:<37}║")

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
    """Run all tests for the polyglot_resonance module."""
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

    print("🎵 Polyglot Resonance — Running Tests\n")

    # ── Rotation file ─────────────────────────────────────────────────────────
    try:
        config = load_rotation()
        t("load_rotation() returns valid dict", isinstance(config, dict))
        t("rotation has 'languages' key", "languages" in config)
        t("rotation has 'current_index' key", "current_index" in config)
    except Exception as e:
        t("load_rotation() succeeds", False, str(e))

    # ── ROTATION_ORDER ────────────────────────────────────────────────────────
    for lang in ROTATION_ORDER:
        t(f"ROTATION_ORDER contains '{lang}'", lang in ROTATION_ORDER)

    # ── RESONANCE_THEMES ─────────────────────────────────────────────────────
    t("RESONANCE_THEMES has 5 themes", len(RESONANCE_THEMES) == 5)
    for theme in RESONANCE_THEMES:
        t(f"  Theme '{theme['id']}' has 'languages'", "languages" in theme)
        t(f"  Theme '{theme['id']}' has 'fundamental_hz'", "fundamental_hz" in theme)
        t(f"  Theme '{theme['id']}' has 'dissonance_pairs'", "dissonance_pairs" in theme)
        for lang, info in theme["languages"].items():
            t(f"    '{lang}' has hz/phase/wave/description",
              all(k in info for k in ("hz", "phase", "wave", "description")))

    # ── Waveform generators ───────────────────────────────────────────────────
    for wave_name, fn in WAVE_FUNCTIONS.items():
        t(f"Wave function '{wave_name}' defined", callable(fn))

    # ── _draw_oscilloscope ────────────────────────────────────────────────────
    try:
        rows = _draw_oscilloscope(440.0, 432.0, 0.0, "sine", width=60, height=9)
        t("_draw_oscilloscope returns 9 rows", len(rows) == 9)
        t("_draw_oscilloscope rows are 60 chars wide", all(len(r) == 60 for r in rows))
    except Exception as e:
        t("_draw_oscilloscope succeeds", False, str(e))

    # ── generate_resonance_analysis ───────────────────────────────────────────
    for theme in RESONANCE_THEMES:
        for lang in theme["languages"]:
            try:
                result = generate_resonance_analysis(lang, theme)
                t(f"generate_resonance_analysis('{lang}', '{theme['id']}') succeeds", True)
                t(f"  - has 'theme'", "theme" in result)
                t(f"  - has 'language_resonance'", "language_resonance" in result)
                t(f"  - has 'waveform_display'", "waveform_display" in result)
                t(f"  - has 'overtones'", "overtones" in result)
                t(f"  - waveform_display is list of 9 strings", len(result["waveform_display"]) == 9)
                t(f"  - overtones is non-empty list", len(result["overtones"]) > 0)
                # All overtones should have required fields
                for ot in result["overtones"]:
                    t(f"  - overtone has required fields",
                      all(k in ot for k in ("language", "frequency_hz", "resonance_type")))
            except Exception as e:
                t(f"generate_resonance_analysis('{lang}', '{theme['id']}')", False, str(e))

    # ── resonance() advances rotation ────────────────────────────────────────
    try:
        cfg_before = load_rotation()
        idx_before = cfg_before["current_index"]
        lang_before = cfg_before["languages"][idx_before % len(cfg_before["languages"])]
        result = resonance()
        cfg_after = load_rotation()
        idx_after = cfg_after["current_index"]
        t("resonance() advances current_index",
          idx_after == (idx_before + 1) % len(cfg_before["languages"]))
        t("resonance() returns rotation_advanced=True",
          result.get("rotation_advanced") is True)
        t("resonance() returns the selected language",
          result.get("language") == lang_before)
        t("resonance() returns next_language",
          "next_language" in result)
        t("resonance() returns next_index",
          "next_index" in result)
    except Exception as e:
        t("resonance() rotation advancement", False, str(e))

    # ── format_resonance ──────────────────────────────────────────────────────
    try:
        theme = RESONANCE_THEMES[0]
        lang = list(theme["languages"].keys())[0]
        m = generate_resonance_analysis(lang, theme)
        formatted = format_resonance(m)
        t("format_resonance() returns a string", isinstance(formatted, str))
        t("format_resonance() starts with box-drawing char", formatted.startswith("╔"))
        t("format_resonance() ends with box-drawing char", formatted.rstrip().endswith("╝"))
        t("format_resonance() contains the language name", lang in formatted)
    except Exception as e:
        t("format_resonance()", False, str(e))

    # ── Unknown language raises ValueError ────────────────────────────────────
    try:
        generate_resonance_analysis("Brainfuck", RESONANCE_THEMES[0])
        t("Unknown language raises ValueError", False, "did not raise")
    except ValueError:
        t("Unknown language raises ValueError", True)
    except Exception as e:
        t("Unknown language raises ValueError", False, f"wrong exception: {e}")

    # ── Rotation index wraps correctly ───────────────────────────────────────
    try:
        cfg = load_rotation()
        langs = cfg["languages"]
        idx = cfg["current_index"]
        # Simulate advancing until we wrap
        for _ in range(len(langs) + 1):
            cfg = load_rotation()
            idx = cfg["current_index"]
            lang = cfg["languages"][idx % len(langs)]
            cfg["current_index"] = (idx + 1) % len(langs)
            cfg["last_language"] = lang
            cfg["updated_at"] = datetime.now(timezone.utc).isoformat()
            save_rotation(cfg)
        cfg_final = load_rotation()
        t("Rotation wraps after full cycle",
          cfg_final["current_index"] == (idx + len(langs) + 1) % len(langs))
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
        result = resonance()
        print(format_resonance(result))
