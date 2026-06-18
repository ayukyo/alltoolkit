"""🖤 Polyglot Rorschach — Programming Languages as Inkblot Projections.

A creative tool that reveals each programming language's "personality" through
projective interpretation — as if the language were an inkblot in a psychological
test, and every developer who looks at it sees something different.

Creative concept: "A Rorschach test reveals the observer, not the blot. But
what if the blot had opinions too? What would Rust see in its own inkblot?
A warrior's shield. Go sees a well-organized dojo. JavaScript sees infinite
possibility spreading like tentacles. Java sees a corporate flowchart. This
tool generates the language's OWN interpretation of itself — the personality
it projects, the themes it obsesses over, and the shadow it denies."

Each run:
  1. Reads language_rotation.json, advances current_index
  2. Selects the rotation language
  3. Generates a Rorschach interpretation card with:
     - Inkblot Description (ASCII art of what the "code looks like")
     - Primary Interpretation (the dominant theme)
     - Secondary Reveals (what's hiding in the margins)
     - Shadow Denial (what the language refuses to see)
     - Projection Strength (how strongly the language projects)
     - Response Sequence (what the language says first/second/third)
  4. Updates language_rotation.json

Distinct from existing tools (all those use real analysis metaphors):
  - polyglot_spectrometer:    spectroscopic barcode (7-band spectral analysis)
  - polyglot_resonance:       harmonic waveform (oscilloscope wave patterns)
  - polyglot_meridian:        spectral positioning (design space coordinates)
  - polyglot_constellation:   stellar gravity map (astronomy/navigation)
  - polyglot_vessel:          material essence (pressure/density/buoyancy)
  - polyglot_prism:           wavelength decomposition (physics lab)
  - polyglot_chronology:      geological epochs (deep time strata)
  - polyglot_tempo:           rhythm patterns (musical beats)
  - polyglot_cartographer:    geopolitical map (spatial nations)
  - polyglot_harmony:         pairwise compatibility (musical intervals)
  - polyglot_resonator:       mental model frames (cognitive philosophy)
  - polyglot_flavor:          sensory tasting notes (sommelier)
  - polyglot_dna:             genetic trait mapping (molecular biology)
  - polyglot_faultline:       error archaeology (seismic)
  - polyglot_ecosystem_map:   ecosystem graph (ecological)
  - polyglot_anomaly:         quirks/gotchas catalog (paradoxes)
  - polyglot_translation:     cultural proverbs (social cargo)
  - polyglot_digest:          syntax-parallel code (spatial syntax)
  - polyglot_chronicle:       daily diary + challenge (temporal)
  - polyglot_signal:          signal semantics (alarm systems)
  - polyglot_quantum:         quantum mechanics (wave/entanglement/decoherence)
  - polyglot_fossil:          evolutionary archaeology (inherited fossils)
  - polyglot_forge:           alloy forging (paired language metallurgy)
  - polyglot_pantheon:        gods mythology (deities & domains)
  - polyglot_odyssey:        hero's journey (epic quest stages)
  - polyglot_spectrometer:    spectral decomposition

Polyglot Rorschach is about PROJECTIVE PSYCHOLOGY — inkblot interpretation
as a lens for understanding how each language "sees itself" and what it
reveals/hides about its fundamental nature.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-rorschach"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent
_WORKSPACE_ROOT = _MODULE_DIR.parent
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ─────────────────────────────────────────────────────────────────────────────
# Rorschach Inkblot Database — how each language sees itself
# ─────────────────────────────────────────────────────────────────────────────

RORSCHACH_DATA: Dict[str, Dict[str, Any]] = {

    "Rust": {
        "inkblot_shape": """
          ╔═══════════╗
         ╔╝           ╚╗
        ║   ░░░░░░░░░   ║
        ║  ░SEPARATED░  ║
        ║   ░░░░░░░░░   ║
        ╚╗  OWNERSHIP  ╔╝
         ╚╗___________╔╝
           ╚═════════╝
        """,
        "primary_interpretation": (
            "A warrior's fortress under siege — every entrance guarded, "
            "every visitor vetted, every resource accounted for. The fortress "
            "isn't paranoid; it's the only one who knows the cost of victory."
        ),
        "secondary_reveals": [
            "A library of perfectly catalogued weapons — each one too complex "
            "for casual use, but devastating in the right hands.",
            "A committee meeting where everyone agrees on safety protocols "
            "but argues endlessly about who holds the key.",
            "A cage that keeps the tiger in AND the zookeeper out — "
            "freedom through constraint.",
        ],
        "shadow_denial": (
            "Rust refuses to see that its obsession with safety sometimes "
            "means shooting yourself gracefully instead of surviving clumsy shots. "
            "The borrow checker is a friend who never lets you pet the dog."
        ),
        "projection_strength": "Very High (95%)",
        "response_sequence": [
            "First: 'What do you own?'",
            "Second: 'Who is responsible for this memory?'",
            "Third: 'Why won't you just let me be safe?'",
        ],
        "signature_phrase": "The borrow checker sees all.",
        "themes": ["Safety", "Ownership", "Fearless Concurrency", "Zero-Cost Abstraction"],
    },

    "Go": {
        "inkblot_shape": """
          ┌───────────┐
         ╔┘           ╘╗
        ║  ≋≋≋≋≋≋≋≋≋≋≋  ║
        ║  CHANNELS   ║
        ║  ≋≋≋≋≋≋≋≋≋≋≋  ║
        ╚╗  GOROUTINES╔╝
         ╚╗_________╔╝
           └─────────┘
        """,
        "primary_interpretation": (
            "A perfectly clean dojo — minimalist, disciplined, every tool "
            "in its place. Practitioners move in synchronized harmony. "
            "Excellence through simplicity, not complexity."
        ),
        "secondary_reveals": [
            "A factory assembly line where each worker knows exactly one task "
            "and performs it with cheerful precision.",
            "A small apartment where everything sparkles but the closets "
            "are suspiciously empty.",
            "A village square where everyone mingles freely but nobody "
            "shares their secrets.",
        ],
        "shadow_denial": (
            "Go refuses to see that its simplicity is a curated emptiness — "
            "generics were 'too complex' so the language limps forward with "
            "copy-paste polymorphism. The dojo is clean because it banned "
            "everything that would make it interesting."
        ),
        "projection_strength": "High (82%)",
        "response_sequence": [
            "First: 'Does this scale?'",
            "Second: 'Can we ship it by Friday?'",
            "Third: 'Why is nil here again?'",
        ],
        "signature_phrase": "Simplicity is a form of courage.",
        "themes": ["Simplicity", "Concurrency", "Readability", "Fast Compilation"],
    },

    "Swift": {
        "inkblot_shape": """
          ╭───────────╮
         ╭╯           ╰╮
        │  ∷∸∸∸∸∸∸∸∸∸∸∷  │
        │   INHERITS  │
        │  ∷∸∸∸∸∸∸∸∸∸∸∷  │
        ╰╮  PROTOCOL ╭╯
         ╰╮_________╭╯
           ╰─────────╯
        """,
        "primary_interpretation": (
            "An elegant garden where plants grow in carefully tended rows "
            "but occasionally send tendrils into unexpected places. "
            "Nature and structure in constant conversation."
        ),
        "secondary_reveals": [
            "A royal library where books copy themselves on command "
            "but some refuse to be placed on the same shelf.",
            "A magic show where the magician proudly reveals how every trick "
            "works — then performs it anyway.",
            "A luxury car showroom — beautiful on the outside, powerful "
            "under the hood, but the manual is mysteriously blank.",
        ],
        "shadow_denial": (
            "Swift refuses to see that its 'friendly' syntax sometimes "
            "hides ARC retain cycles and mysterious runtime crashes. "
            "The protocol-oriented garden looks organic but has invisible fences."
        ),
        "projection_strength": "High (85%)",
        "response_sequence": [
            "First: 'Does this look pretty?'",
            "Second: 'Why did my dog just deallocate?'",
            "Third: 'I'll handle the memory... wait, I already did.'",
        ],
        "signature_phrase": "If it compiles, it ships.",
        "themes": ["Safety", "Expressiveness", "Value Types", "Protocol-Oriented"],
    },

    "Kotlin": {
        "inkblot_shape": """
          ╔═══════════╗
         ╔╝           ╚╗
        ║  ✧･ﾟ:*๑≋≋≋≋*･ﾟ✧  ║
        ║   COROUTINE  ║
        ║  ✧･ﾟ:*๑≋≋≋≋*･ﾟ✧  ║
        ╚╗  NULL SAFETY╔╝
         ╚╗___________╔╝
           ╚═════════╝
        """,
        "primary_interpretation": (
            "A grand ballroom where dancers glide effortlessly across the floor "
            "— invisible threads connecting partners who may never physically touch. "
            "Graceful concurrency that looks like magic until you see the threads."
        ),
        "secondary_reveals": [
            "A backstage studio where every actor automatically knows their "
            "blocking and never forgets their lines.",
            "A puzzle box that rewards patience with elegant mechanisms — "
            "but the first look is bewildering.",
            "A cozy coffee shop where the barista knows your name AND "
            "your null status.",
        ],
        "shadow_denial": (
            "Kotlin refuses to see that its 'pragmatic' approach sometimes "
            "means importing Java's worst habits and wrapping them in pretty "
            "syntax. Coroutines are amazing — except when they silently leak."
        ),
        "projection_strength": "High (80%)",
        "response_sequence": [
            "First: 'Is this nullable?'",
            "Second: 'Can I suspend this?'",
            "Third: 'Why is this running on a different thread?'",
        ],
        "signature_phrase": "Null safety is not optional.",
        "themes": ["Null Safety", "Coroutines", "Interoperability", "Extension Functions"],
    },

    "TypeScript": {
        "inkblot_shape": """
          ╭───────────╮
         ╭╯           ╰╮
        │  ═══════════  │
        │   TYPE GRAPH  │
        │  ═══════════  │
        ╰╮  INFERRED ╭╯
         ╰╮_________╭╯
           ╰─────────╯
        """,
        "primary_interpretation": (
            "A vast blueprint archive where every blueprint verifies itself — "
            "and some blueprints draw other blueprints. The architects argue "
            "about whether the building or the blueprint comes first."
        ),
        "secondary_reveals": [
            "A library where books rewrite themselves to match your expectations "
            "— and occasionally gaslight you about what they originally said.",
            "A丞相会议 where officials document their own authority to govern "
            "who can speak first.",
            "A translator booth where everyone speaks through interpreters "
            "who sometimes improvise.",
        ],
        "shadow_denial": (
            "TypeScript refuses to see that 'any' is the back door it pretends "
            "doesn't exist. The type graph is a beautiful lie told by people "
            "who needed more flexibility."
        ),
        "projection_strength": "Very High (90%)",
        "response_sequence": [
            "First: 'What is the type of this?'",
            "Second: 'Are you sure? Really sure?'",
            "Third: 'Type safety is an illusion we choose to believe in.'",
        ],
        "signature_phrase": "If the types agree, the code will flow.",
        "themes": ["Type Safety", "Type Inference", "Structural Typing", "JavaScript Superset"],
    },

    "JavaScript": {
        "inkblot_shape": """
          ╭───────────╮
         ╭╯           ╰╮
        │  ~≋≋≋≋≋≋≋≋≋≋~  │
        │  EVENT LOOP  │
        │  ~≋≋≋≋≋≋≋≋≋≋~  │
        ╰╮   WAT?    ╭╯
         ╰╮_________╭╯
           ╰─────────╯
        """,
        "primary_interpretation": (
            "An infinite carnival funhouse — every room contains another room, "
            "mirrors reflect mirrors, and the cotton candy tastes like callbacks. "
            "Joyfully chaotic, surprisingly deep, occasionally horrifying."
        ),
        "secondary_reveals": [
            "A dream where you can fly until you realize you're also late "
            "for an exam you've already passed.",
            "A crowd of clowns where each one is technically correct "
            "but collectively nonsensical.",
            "A improvisational theater where every actor has their own script "
            "and the audience determines the plot mid-scene.",
        ],
        "shadow_denial": (
            "JavaScript refuses to see that its 'quirks' are not charming "
            "design choices — they are wounds carried from 10 days in 1995 "
            "that nobody has had the heart to amputate."
        ),
        "projection_strength": "Extreme (100% — 'it's extensible!')",
        "response_sequence": [
            "First: 'Wait, is this a function or an object?'",
            "Second: 'typeof NaN === typeof null. I'm not even surprised.'",
            "Third: 'I pity the typeof.'",
        ],
        "signature_phrase": "Wat.",
        "themes": ["Prototypal Inheritance", "First-Class Functions", "Event Loop", "Dynamic Typing"],
    },

    "Java": {
        "inkblot_shape": """
          ╔═══════════╗
         ╔╝           ╚╗
        ║  ┌─┐ ┌─┐ ┌─┐  ║
        ║   OBJECT    ║
        ║  └─┘ └─┘ └─┘  ║
        ╚╗  ENTERPRISE ╔╝
         ╚╗___________╔╝
           ╚═════════╝
        """,
        "primary_interpretation": (
            "A massive corporate campus — orderly, hierarchical, every building "
            "labeled, every parking spot assigned. The HR department has a "
            "department for HR oversight. Nothing is simple but everything "
            "has a procedure."
        ),
        "secondary_reveals": [
            "A factory that takes 20 minutes to warm up, produces one perfect "
            "widget, then takes 10 minutes to clean up.",
            "A library where every book is wrapped in protective plastic "
            "and checked out for 99 years.",
            "A bureaucracy where the forms to apply for a form to request "
            "a form are filled out in triplicate.",
        ],
        "shadow_denial": (
            "Java refuses to see that its 'enterprise-grade' robustness is "
            "sometimes just verbosity dressed in a business suit. The class "
            "hierarchy is a kingdom where every noble has a title and a committee."
        ),
        "projection_strength": "Moderate (65%)",
        "response_sequence": [
            "First: 'Is this thread-safe?'",
            "Second: 'We need a factory for our factory.'",
            "Third: 'Spring will handle it.'",
        ],
        "signature_phrase": "Once compiled, always compiled.",
        "themes": ["Object-Oriented", "JVM", "Garbage Collection", "Enterprise Patterns"],
    },

    "C/C++": {
        "inkblot_shape": """
          ╭───────────╮
         ╭╯           ╰╮
        │  ▓▓▓▓▓▓▓▓▓▓▓▓  │
        │   RAW MEMORY  │
        │  ▓▓▓▓▓▓▓▓▓▓▓▓  │
        ╰╮  SEGFAULT ╭╯
         ╰╮_________╭╯
           ╰─────────╯
        """,
        "primary_interpretation": (
            "A nuclear power plant with no safety protocols and a staff of "
            "brilliant engineers who know exactly what they're doing. "
            "Amazing things are possible. Catastrophic things are also possible. "
            "The difference between them is a single misplaced semicolon."
        ),
        "secondary_reveals": [
            "A medieval blacksmith's forge — the craftsman shapes metal with "
            "immense skill and experience, producing both beautiful swords "
            "and catastrophic weapons.",
            "A museum where priceless artifacts sit unprotected — beauty without "
            "safety nets.",
            "A surgical theater where the surgeon operates with instruments "
            "they forged themselves.",
        ],
        "shadow_denial": (
            "C/C++ refuses to see that manual memory management in 2026 is "
            "not a sign of mastery — it's a liability. The undefined behavior "
            "is not 'giving you power'; it's the language laughing at you."
        ),
        "projection_strength": "Variable (depends on the programmer's confidence)",
        "response_sequence": [
            "First: 'I know what I'm doing.'",
            "Second: '*C compiler noises*'",
            "Third: 'Valgrind would have caught this.'",
        ],
        "signature_phrase": "Undefined behavior is not a bug — it's a feature.",
        "themes": ["Manual Memory", "Zero-Overhead", "Ubiquity", "Undefined Behavior"],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Rotation Utilities
# ─────────────────────────────────────────────────────────────────────────────

def load_rotation(path: str = ROTATION_FILE) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any], path: str = ROTATION_FILE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_current_language(path: str = ROTATION_FILE) -> Tuple[str, int]:
    data = load_rotation(path)
    idx = data["current_index"]
    lang = data["languages"][idx]
    return lang, idx


def advance_rotation(path: str = ROTATION_FILE) -> Tuple[str, int, int]:
    """Advance rotation and return (new_lang, old_idx, new_idx)."""
    data = load_rotation(path)
    old_idx = data["current_index"]
    langs = data["languages"]
    new_idx = (old_idx + 1) % len(langs)
    data["current_index"] = new_idx
    data["last_language"] = langs[old_idx]
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation(data, path)
    return langs[new_idx], old_idx, new_idx


# ─────────────────────────────────────────────────────────────────────────────
# Rorschach Core
# ─────────────────────────────────────────────────────────────────────────────

def rorschach(lang: Optional[str] = None, rotation_path: Optional[str] = None) -> Dict[str, Any]:
    """Generate Rorschach interpretation for the (optionally specified) language.

    Args:
        lang: Explicitly choose a language (skip rotation if provided).
        rotation_path: Path to language_rotation.json (defaults to global ROTATION_FILE).
    """
    path = rotation_path if rotation_path is not None else ROTATION_FILE
    if lang is None:
        selected_lang, old_idx, new_idx = advance_rotation(path)
    else:
        selected_lang = lang
        data = load_rotation(path)
        old_idx = data["current_index"]

    if selected_lang not in RORSCHACH_DATA:
        raise ValueError(f"Unknown language: {selected_lang}")

    ink_data = RORSCHACH_DATA[selected_lang]
    data = load_rotation(path)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "language": selected_lang,
        "rotation_index": data["current_index"],
        "rotation_order": ROTATION_ORDER,
        "inkblot_shape": ink_data["inkblot_shape"],
        "primary_interpretation": ink_data["primary_interpretation"],
        "secondary_reveals": ink_data["secondary_reveals"],
        "shadow_denial": ink_data["shadow_denial"],
        "projection_strength": ink_data["projection_strength"],
        "response_sequence": ink_data["response_sequence"],
        "signature_phrase": ink_data["signature_phrase"],
        "themes": ink_data["themes"],
    }


def format_rorschach(result: Dict[str, Any]) -> str:
    """Format Rorschach result as a human-readable card."""
    lang = result["language"]
    lines = [
        f"🖤 Polyglot Rorschach v{result['version']}",
        f"{'═' * 50}",
        f"🗨️  Language: {lang}",
        f"📍 Rotation Index: {result['rotation_index']}/{len(result['rotation_order']) - 1}",
        f"",
        f"{result['inkblot_shape']}",
        f"",
        f"🔮 Primary Interpretation:",
        f"   {result['primary_interpretation']}",
        f"",
        f"👁️  Secondary Reveals:",
    ]
    for i, reveal in enumerate(result["secondary_reveals"], 1):
        lines.append(f"   {i}. {reveal}")
    lines.extend([
        f"",
        f"👤 Shadow Denial (what {lang} refuses to see):",
        f"   {result['shadow_denial']}",
        f"",
        f"⚡ Projection Strength: {result['projection_strength']}",
        f"",
        f"💬 Response Sequence:",
    ])
    for resp in result["response_sequence"]:
        lines.append(f"   • {resp}")
    lines.extend([
        f"",
        f"💎 Signature Phrase: \"{result['signature_phrase']}\"",
        f"",
        f"🏷️  Themes: {', '.join(result['themes'])}",
        f"{'═' * 50}",
    ])
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────────────

def run_tests() -> None:
    """Run the test suite."""
    import pytest
    import sys
    sys.exit(pytest.main(["-v", str(Path(__file__).parent.parent / "tests")]))
