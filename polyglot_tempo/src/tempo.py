#!/usr/bin/env python3
"""
🎵 Polyglot Tempo v1.0

Rhythm Pattern Generator — maps each programming language to its
"natural rhythm" based on syntax cadence, compilation model, and
execution personality, then generates beat patterns and percussion
arrangements that embody each language's tempo.

Creative concept: "Every language has a rhythm. Rust is staccato —
precise, ownership-checked beats. Go is a clean 4/4 — simple,
goroutine-parallel percussion. JavaScript is syncopated funk —
prototype chaos, event-loop swing. This tool translates languages
into playable rhythm notation."

Each language is mapped to:
  - BPM (beats per minute) — the "heart rate" of compilation/execution
  - Time Signature — the structural feel (4/4, 6/8, etc.)
  - Primary Pattern — main percussion rhythm
  - Accent Map — which beats get emphasis
  - Fill Pattern — the transitional phrase between operations
  - Groove Tag — funk, metal, jazz, minimal, etc.
  - Notation — a text-based rhythm notation (MIDI-like or ASCII)

The tool generates a full rhythm arrangement for the current
rotation language, showing the "beat" of compilation, the "swing"
of type checking, and the "fill" of error handling.

Distinct from existing tools:
  - polyglot_signal:    signal vocabulary (error/null/warning semantics)
  - polyglot_digest:    syntax-parallel code (same code, different syntax)
  - polyglot_translation: cultural idioms/proverbs (social cargo)
  - polyglot_chronology:  geological/evolutionary timeline (deep time)
  - polyglot_harmony:     pair compatibility analysis
  - polyglot_resonator:   mental model differences

Tempo is about the FEEL and CADENCE of languages — the rhythm and
groove that makes each language feel different when you write it.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-tempo"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent  # polyglot_tempo/src/ -> polyglot_tempo/
_WORKSPACE_ROOT = _MODULE_DIR.parent  # polyglot_tempo/ -> workspace/
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]


# ─────────────────────────────────────────────────────────────────────────────
# Rhythm Database — language tempo characteristics
# ─────────────────────────────────────────────────────────────────────────────

RHYTHM_DB: Dict[str, Dict[str, Any]] = {

    "Rust": {
        "bpm": 120,
        "time_signature": "4/4",
        "groove_tag": "Staccato Precision Metal",
        "feel": "tight, ownership-locked, every beat exact",
        "primary_pattern": "Kick·Snare·Kick-Snare",
        "pattern_desc": "Exact one-liners, no wasted notes. Every beat is proven.",
        "beat_notation": "♩ ▌  ♩ ▌  ♩ ▌  ♩ ▌",  # quarter + eighth
        "fill_pattern": "rapid 16th-note arpeggios on the & of 4",
        "fill_desc": "The borrow checker runs a 16th-note fill — checking every reference.",
        "kick": "hard and immediate (compile success)",
        "snare": "crisp error-stop (compile failure)",
        "hihat": "soldering-iron sizzle (warning tick)",
        "crash": "dramatic panic (panic! macro)",
        "swing_factor": 0.0,  # no swing — perfectly quantized
        "percussion_emoji": "⚡",
        "cadence": "measured · precise · zero-tolerance",
        "rhythm_quote": "The borrow checker is a metronome — it never misses a beat.",
        "tempo_desc": "Rust feels like a drum solo where every hit is mathematically proven.",
        "loop_symbol": "⟦⟩",
        "rest_symbol": "··",
        "accent_symbol": "▶",
        "ascii_notation": [
            " 1 ♩ · · · 2 ♩ · · · 3 ♩ · · · 4 ♩ · · · ",
            " K · · · S · · · K · · · S · · · K · · · ",
            " H ▌ ▌ ▌ H ▌ ▌ ▌ H ▌ ▌ ▌ H ▌ ▌ ▌ ",
            " F · · · · · · · · · · · · F · · · · · · ",
        ],
    },

    "Go": {
        "bpm": 130,
        "time_signature": "4/4",
        "groove_tag": "Clean 4/4 Funk",
        "feel": "lightweight goroutines, easy concurrency, no fuss",
        "primary_pattern": "Kick-Snare·Kick·Kick-Snare",
        "pattern_desc": "Simple and balanced, the gopher keeps steady time.",
        "beat_notation": "♩♩ ♩♩ ♩♩ ♩♩",  # pairs of quarters
        "fill_pattern": "8th-note ghost notes on the hi-hat",
        "fill_desc": "Goroutine spawns are ghost notes — they appear without disrupting the beat.",
        "kick": "clean and punchy",
        "snare": "backbeat on 2 and 4",
        "hihat": "continuous 8ths (scheduler ticks)",
        "crash": "panic crash — rare and dramatic",
        "swing_factor": 0.1,
        "percussion_emoji": "🥟",
        "cadence": "steady · relaxed · goroutine-parallel",
        "rhythm_quote": "Goroutines are ghost notes — the beat goes on even when they land.",
        "tempo_desc": "Go feels like a relaxed funk groove — simple syntax, steady time.",
        "loop_symbol": "⟦⟩",
        "rest_symbol": "··",
        "accent_symbol": "▶",
        "ascii_notation": [
            " 1 ♩♩ · 2 ♩♩ · 3 ♩♩ · 4 ♩♩ · ",
            " K S · K · · S · K S · K · · S · ",
            " H ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ",
            " F · · · · · · G · · · · · · · F · ",
        ],
    },

    "Swift": {
        "bpm": 110,
        "time_signature": "4/4",
        "groove_tag": "Smooth Protocol Jazz",
        "feel": "expressive, protocol-oriented, graceful optional handling",
        "primary_pattern": "Kick··Snare··Kick·Snare",
        "pattern_desc": "Smooth and lyrical — optionals are rests between beats.",
        "beat_notation": "♩ · ♩ · ♩ · ♩ ·",  # syncopated quarters
        "fill_pattern": "triplet feel on the & of 2 and 4",
        "fill_desc": "Optional unwrapping is a triplet fill — graceful descent.",
        "kick": "soft and warm (successful unwrap)",
        "snare": "light brush (protocol conformance)",
        "hihat": "closed-open pair (guard statement)",
        "crash": "fatalError crash — dramatic curtain fall",
        "swing_factor": 0.2,
        "percussion_emoji": "🦅",
        "cadence": "smooth · lyrical · protocol-harmonic",
        "rhythm_quote": "Swift optionals are rests in a smooth jazz solo.",
        "tempo_desc": "Swift feels like smooth jazz — graceful, expressive, and safe.",
        "loop_symbol": "⟲",
        "rest_symbol": "···",
        "accent_symbol": "▶",
        "ascii_notation": [
            " 1 ♩ · · 2 · ♩ 3 ♩ · · 4 · ♩ ",
            " K · · · · · S · K · · · · S · ",
            " H ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ",
            " F · · · · T · · · · · · · F · · ",
        ],
    },

    "Kotlin": {
        "bpm": 115,
        "time_signature": "4/4",
        "groove_tag": "Coroutines Flow",
        "feel": "null-safe flows, concise chains, suspend rhythm",
        "primary_pattern": "Kick·Snare·Kick·Snare-Fill",
        "pattern_desc": "Extension chains build like a rolling percussion wave.",
        "beat_notation": "♩ ▌ ♩ ▌ ♩ ▌ ♩ ▌♩",  # quarter + 8th pairs
        "fill_pattern": "coroutine suspend is a 3-beat fill across bar lines",
        "fill_desc": "suspend functions suspend the beat — async fills that cross measure boundaries.",
        "kick": "firm and immediate",
        "snare": "crisp backbeat",
        "hihat": "flowing 16ths (sequence operations)",
        "crash": "KotlinNullPointerException — rare but sharp",
        "swing_factor": 0.1,
        "percussion_emoji": "🟣",
        "cadence": "flowing · chain-reactive · null-safe",
        "rhythm_quote": "Kotlin coroutines are async fills that cross the bar line.",
        "tempo_desc": "Kotlin feels like a flowing jam — chain operators are rolling toms.",
        "loop_symbol": "⟦⟩",
        "rest_symbol": "··",
        "accent_symbol": "▶",
        "ascii_notation": [
            " 1 ♩ ▌ 2 ♩ ▌ 3 ♩ ▌ 4 ♩ ▌♩ ",
            " K · S · K · S · K · S · · · F ",
            " H ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ",
            " F · · · · · · · · · · · F · · · ",
        ],
    },

    "TypeScript": {
        "bpm": 140,
        "time_signature": "4/4",
        "groove_tag": "Type Error Funk",
        "feel": "fast iteration, compile-time type jazz, runtime js chaos",
        "primary_pattern": "Kick·Kick-Snare·Kick-Snare",
        "pattern_desc": "Double-time kick on type checks, syncopated runtime.",
        "beat_notation": "♩♩ ♩♩ ♩♩ ♩♩",  # double-time
        "fill_pattern": "interface declaration is a 2-beat rest-then-accent",
        "fill_desc": "Type annotations are rests — the beat pauses while types are checked.",
        "kick": "hard type assertion",
        "snare": "runtime error snap",
        "hihat": "rapid type inference ticks",
        "crash": "TypeError at runtime — the funk breaks down",
        "swing_factor": 0.15,
        "percussion_emoji": "📘",
        "cadence": "double-time · type-checked · runtime-funky",
        "rhythm_quote": "TypeScript's type checker is a syncopated jazz solo over JavaScript's funk.",
        "tempo_desc": "TypeScript feels like double-time funk — type checks are syncopated fills.",
        "loop_symbol": "⟦⟩",
        "rest_symbol": "··",
        "accent_symbol": "▶",
        "ascii_notation": [
            " 1 ♩♩ 2 ♩♩ 3 ♩♩ 4 ♩♩ ",
            " K K S · K S · K S · · ",
            " H ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ",
            " F · · · · · · · · T · T · · · · F · ",
        ],
    },

    "JavaScript": {
        "bpm": 135,
        "time_signature": "4/4",
        "groove_tag": "Event-Loop Funk",
        "feel": "prototype chaos, callback fills, async swing",
        "primary_pattern": "Kick··Snare·Kick·Snare",
        "pattern_desc": "Event loop drives the groove — callbacks are swing fills.",
        "beat_notation": "♩ · ♩ · ♩♩ ♩♩",  # quarter + double-time ending
        "fill_pattern": "callback hell is a 4-beat crescendo fill",
        "fill_desc": "Nested callbacks build like a jazz crescendo — messy but exciting.",
        "kick": "synchronous execution",
        "snare": "event dispatch snap",
        "hihat": "setTimeout hi-hat ticks",
        "crash": "ReferenceError — funk breaks hard",
        "swing_factor": 0.25,
        "percussion_emoji": "💛",
        "cadence": "funky · prototype-swing · event-driven",
        "rhythm_quote": "JavaScript's event loop is a perpetual swing fill.",
        "tempo_desc": "JavaScript feels like funk — prototype chaos, callback swing, event-loop groove.",
        "loop_symbol": "⟲",
        "rest_symbol": "···",
        "accent_symbol": "▶",
        "ascii_notation": [
            " 1 ♩ · · 2 ♩ · · 3 ♩♩ 4 ♩♩ ",
            " K · · · S · K · S · · · · · · ",
            " H ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ",
            " F · · · · · C · · · · · · F · · ",
        ],
    },

    "Java": {
        "bpm": 100,
        "time_signature": "4/4",
        "groove_tag": "Enterprise March",
        "feel": "ceremonial, checked exceptions, stable enterprise march",
        "primary_pattern": "Kick·Snare·Kick·Snare",
        "pattern_desc": "Steady and ceremonial — checked exceptions are formal drum roasts.",
        "beat_notation": "♩ ♩ ♩ ♩",  # straight quarters
        "fill_pattern": "try-catch-finally is a 3-beat building fill",
        "fill_desc": "Exception handling builds like a ceremonial march — structured and formal.",
        "kick": "strong and ceremonial",
        "snare": "formal backbeat",
        "hihat": "JVM tick — steady metronome of the JVM",
        "crash": "RuntimeException — enterprise drama",
        "swing_factor": 0.0,
        "percussion_emoji": "☕",
        "cadence": "ceremonial · checked · enterprise-stable",
        "rhythm_quote": "Java is an enterprise march — checked exceptions are drum roasts.",
        "tempo_desc": "Java feels like a ceremonial march — structured, stable, and formal.",
        "loop_symbol": "⟦⟩",
        "rest_symbol": "··",
        "accent_symbol": "▶",
        "ascii_notation": [
            " 1 ♩ 2 ♩ 3 ♩ 4 ♩ ",
            " K S K S K S K S ",
            " H ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ",
            " F · · · · · · T C F · · · · · · · ",
        ],
    },

    "C/C++": {
        "bpm": 150,
        "time_signature": "4/4",
        "groove_tag": "Death Metal Precision",
        "feel": "raw power, manual memory, buffer overflow breakdowns",
        "primary_pattern": "Kick-Snare-Kick-Snare-Kick-Fill",
        "pattern_desc": "Aggressive and precise — manual memory is a double-kick pedal.",
        "beat_notation": "♩♩♩ ♩♩♩ ♩♩♩ ♩♩♩♩",  # relentless 16ths
        "fill_pattern": "buffer overflow is a 4-beat blast beat fill",
        "fill_desc": "Memory violations trigger a blast-beat fill — chaotic and loud.",
        "kick": "sub-kick bass drum (manual memory access)",
        "snare": "snare crack (pointer dereference)",
        "hihat": "segfault sizzle",
        "crash": "segfault — total system crash",
        "swing_factor": 0.0,
        "percussion_emoji": "⚙️",
        "cadence": "aggressive · raw · manual-power",
        "rhythm_quote": "C/C++ is death metal — manual memory is a double-kick pedal.",
        "tempo_desc": "C/C++ feels like death metal — raw power, zero safety nets.",
        "loop_symbol": "⟦⟩",
        "rest_symbol": "··",
        "accent_symbol": "▶",
        "ascii_notation": [
            " 1 ♩♩♩ 2 ♩♩♩ 3 ♩♩♩ 4 ♩♩♩♩ ",
            " K S K S K S K S K F · · · · ",
            " H ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ▌ ",
            " F · · · · · · · · · · · · F · · · ",
        ],
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


def _render_ascii_bar(bpm: int, pattern: List[str], swing: float) -> str:
    """Render a single bar of ASCII beat notation."""
    beats = int(bpm / 30)  # rough scaling
    return f"[{bpm} BPM | swing={swing:.0%}] {' '.join(pattern[:4])}"


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def get_current_language(config_path: Optional[str] = None) -> str:
    """Return the current language from rotation config (no rotation)."""
    data = _load_rotation(config_path)
    idx = data["current_index"]
    return data["languages"][idx]


def get_tempo_for_language(language: str) -> Optional[Dict[str, Any]]:
    """Return the tempo/rhythm data for a given language, or None if unknown."""
    return RHYTHM_DB.get(language)


def generate_tempo_map(rotate: bool = True,
                       config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate a rhythm pattern report for the current rotation language.

    Args:
        rotate: If True, advance the rotation index after generating the report.
        config_path: Optional path to language_rotation.json (defaults to workspace).

    Returns:
        {
            "current_language": str,
            "current_index": int,
            "bpm": int,
            "time_signature": str,
            "groove_tag": str,
            "feel": str,
            "primary_pattern": str,
            "pattern_desc": str,
            "beat_notation": str,
            "fill_pattern": str,
            "fill_desc": str,
            "percussion_emoji": str,
            "cadence": str,
            "rhythm_quote": str,
            "tempo_desc": str,
            "ascii_notation": List[str],
            "kick": str,
            "snare": str,
            "hihat": str,
            "crash": str,
            "swing_factor": float,
            "rotated": bool,
            "new_index": Optional[int],
        }
    """
    data = _load_rotation(config_path)
    languages = data["languages"]
    current_index = data["current_index"]

    current_language = languages[current_index]
    rhythm_data = RHYTHM_DB.get(current_language)

    new_index = _compute_next_index(current_index, languages)
    if rotate:
        data["current_index"] = new_index
        data["last_language"] = current_language
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        _save_rotation(data, config_path)

    if rhythm_data is None:
        return {
            "current_language": current_language,
            "current_index": current_index,
            "bpm": 0,
            "time_signature": "Unknown",
            "groove_tag": "Unknown Groove",
            "feel": "Unknown feel.",
            "primary_pattern": "",
            "pattern_desc": "",
            "beat_notation": "",
            "fill_pattern": "",
            "fill_desc": "",
            "percussion_emoji": "❓",
            "cadence": "",
            "rhythm_quote": "",
            "tempo_desc": "No rhythm data available for this language.",
            "ascii_notation": [],
            "kick": "",
            "snare": "",
            "hihat": "",
            "crash": "",
            "swing_factor": 0.0,
            "rotated": rotate,
            "new_index": new_index if rotate else None,
        }

    return {
        "current_language": current_language,
        "current_index": current_index,
        **rhythm_data,
        "rotated": rotate,
        "new_index": new_index if rotate else None,
    }


def format_tempo_card(m: Dict[str, Any]) -> str:
    """
    Format the tempo map result as a human-readable rhythm card.
    """
    notation = "\n".join(f"  ║  {line}" for line in m.get("ascii_notation", []))

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  🎵  POLYGLOT TEMPO — Rhythm Pattern Generator                   ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Language         : {m['current_language']:<47}║",
        f"║  Groove Tag        : {m['groove_tag']:<47}║",
        f"║  BPM / Time        : {m['bpm']} BPM / {m['time_signature']:<40}║",
        f"║  Feel              : {m['feel']:<47}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🥁  PRIMARY RHYTHM PATTERN                                     ║",
        f"║  {m['primary_pattern']:<64}║",
        f"║  {m['pattern_desc']:<64}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🎶  BEAT NOTATION                                               ║",
        f"║  {m['beat_notation']:<64}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  📝  ASCII RHYTHM NOTATION (16th-note grid)                      ║",
        f"  ║{notation}",
        "║       ────────────────────────────────────────────────          ║",
        "║       K=Kick  S=Snare  H=Hi-Hat  F=Fill  T=Type-check            ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🔥  FILL PATTERN                                                ║",
        f"║  {m['fill_pattern']:<64}║",
        f"║  {m['fill_desc']:<64}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🥁  PERCUSSION SEMANTICS                                        ║",
        f"║  Kick   : {m['kick']:<54}║",
        f"║  Snare  : {m['snare']:<54}║",
        f"║  Hi-Hat : {m['hihat']:<54}║",
        f"║  Crash  : {m['crash']:<54}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🎤  CADENCE & QUOTE                                             ║",
        f"║  Cadence : {m['cadence']:<51}║",
        f"║  Quote   : \"{m['rhythm_quote']:<59}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Swing Factor    : {m['swing_factor']:.0%} ({'swing' if m['swing_factor'] > 0 else 'straight':<41}║",
        f"║  Rotated         : {str(m['rotated']):<47}║",
        f"║  New Index       : {str(m.get('new_index', '')):<47}║",
        "╚══════════════════════════════════════════════════════════════════╝",
    ]
    return "\n".join(lines)


def run_tests() -> None:
    """Run all tests and exit."""
    import pytest
    import sys
    sys.exit(pytest.main([str(Path(__file__).parent.parent / "tests"), "-v"]))