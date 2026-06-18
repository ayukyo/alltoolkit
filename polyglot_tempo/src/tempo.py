#!/usr/bin/env python3
"""
🎵 Polyglot Tempo v1.0
Rhythm Pattern Generator — maps programming languages as musical rhythms.

Creative concept: "Every language has a rhythm. Rust clicks with precision —
each borrow check a metronome tick. Go flows like jazz swing — loose yet
disciplined. JavaScript improvises like free jazz — prototype chains are
spontaneous solos. This tool maps the tempo, time signature, and rhythmic
personality of each language as a musical performance."

Each language is characterized by:
  - BPM (beats per minute): perceived compilation/execution speed
  - Time Signature: how the language structures complexity
  - Genre: musical genre that matches the language's personality
  - Rhythm Pattern: ASCII drum-grid showing the language's characteristic beat
  - Signature Groove: the distinctive rhythmic feel
  - Syncopation Level: how much the language disrupts the beat
  - Common Rhythms: typical code patterns as rhythmic figures
  - Tempo Transition: how it feels to move from the previous language

Distinct from existing tools:
  - polyglot_harmony:       pairwise interval compatibility (musical intervals)
  - polyglot_resonance:     harmonic frequency shifts (oscilloscope overtones)
  - polyglot_chronology:    geological deep-time epochs (macro-scale history)
  - polyglot_quantum:       quantum mechanics (wave functions, entanglement)
  - polyglot_archetype_canvas: mythic archetypes (god-like personalities)
  - polyglot_epic_saga:     epic narrative storytelling (hero's journey)
  - polyglot_vessel:        material essence (pressure/density/buoyancy)
  - polyglot_cartographer: geospatial mapping (latitude/longitude coordinates)
  - language_compass:       learning journey milestones (future path)

Tempo is about RHYTHM and GROOVE — the feel of a language in your fingers
when you code, expressed as musical rhythm.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-tempo"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent
_WORKSPACE_ROOT = _MODULE_DIR.parent
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ─────────────────────────────────────────────────────────────────────────────
# Rhythm Database — each language as a musical rhythm/beat profile
# ─────────────────────────────────────────────────────────────────────────────

RHYTHM_DATA: Dict[str, Dict[str, Any]] = {

    "Rust": {
        "bpm": 120,
        "time_signature": "4/4",
        "genre": "Electronic Precision (Techno/Drum Machine)",
        "genre_emoji": "🎛️",
        "tempo_label": "Moderato — deliberate and exact",
        "description": (
            "Rust coding feels like a drum machine: each keystroke triggers a precise, "
            "predictable event. The borrow checker is the metronome — unforgiving, "
            "but once you lock into its groove, you feel invincible. It's tight "
            "4-on-the-floor techno: no swing, no blur, just precise quantization."
        ),
        "signature_groove": "Clockwork Click",
        "groove_description": (
            "Every operation lands exactly on the grid. No ghost notes, no swing — "
            "just pure quantized precision. The closest comparison: a Roland TR-808 "
            "kick on every beat with hi-hats at 16th notes, every hit perfectly timed."
        ),
        "syncopation_level": 1,  # 1-10, where 10 is highly syncopated
        "drum_pattern": [
            ("Kick",    "█   │   │   │   │   │   │   │   │"),
            ("Snare",   "│   │   │ ░ │   │   │   │ ░ │   │"),
            ("Hi-Hat",  "┄┄┄│┄┄│┄┄│┄┄│┄┄│┄┄│┄┄│┄┄│"),
            ("Shaker",  "┄┄┄│▒▒│┄┄│▒▒│┄┄┄│▒▒│┄┄│▒▒│"),
        ],
        "common_rhythms": [
            {"name": "Ownership Transfer", "pattern": "█ → █ (ownership moves, not copied)", "bpm_factor": 1.0},
            {"name": "Match Expression", "pattern": "░ │ ░ │ (binary decision on beat)", "bpm_factor": 1.0},
            {"name": "Result Propagation", "pattern": "▓?▓?▓? (early return on error)", "bpm_factor": 1.2},
            {"name": "Iterator Chain", "pattern": "┄┄┄┄ (fluid, continuous stream)", "bpm_factor": 0.9},
        ],
        "transition_from": {
            "C/C++": "C's raw freedom now has a metronome — the borrow checker adds structure without killing the groove. It feels like adding a drum machine to a rock band.",
            "Go": "Go's goroutine jazz feels chaotic compared to Rust's quantized precision. The shift is from swing to straight.",
            "default": "Every language feels looser after Rust's strict grid.",
        },
        "rhythm_quote": "In Rust, the rhythm is not in the code — it's in the compiler's clock. You learn to code on the beat or you don't code at all.",
        "beat_strength": 10,  # How strong/emphasis the downbeat is
        "ghost_note_frequency": 1,  # How often ghost notes appear (1=never, 10=very often)
        "swing_percentage": 0,  # 0 = straight, 50 = shuffle
        "polyrhythm_depth": 1,  # How many layers of independent rhythms
    },

    "Go": {
        "bpm": 130,
        "time_signature": "4/4",
        "genre": "Jazz Fusion (Groove-Oriented)",
        "genre_emoji": "🎷",
        "tempo_label": "Vivace — lively and loose",
        "description": (
            "Go coding feels like playing in a jazz combo: the goroutines are "
            "improvisational solos, the channels are call-and-response between "
            "musicians, and the GC is the bassist laying down a steady groove. "
            "There's intentional imperfection — `go fmt` is the gentle nudge "
            "to stay in pocket, not a rigid metronome."
        ),
        "signature_groove": "Jazz Pocket",
        "groove_description": (
            "Go code feels like being in the pocket — that magical jazz state where "
            "everyone is slightly behind the beat, creating a deep, laid-back groove. "
            "Goroutines swing, channels breathe. The GC pause is like a fermata: "
            "a moment of held time before continuing."
        ),
        "syncopation_level": 6,
        "drum_pattern": [
            ("Kick",    "█   │   │ ░ │   │█   │   │ ░ │   │"),
            ("Snare",   "│   │   │ █ │   ││   │   │ █ │   │"),
            ("Hi-Hat",  "┄┄┄│┄┄│░░░│┄┄│┄┄┄│┄┄│░░░│┄┄│"),
            ("Shaker",  "░░░│░░░│░░░│░░░│░░░│░░░│░░░│░░░│"),
        ],
        "common_rhythms": [
            {"name": "Goroutine Spawn", "pattern": "◐ + ◌ (async fire and forget)", "bpm_factor": 1.3},
            {"name": "Channel Send/Recv", "pattern": "← → (bidirectional call-response)", "bpm_factor": 1.0},
            {"name": "defer Cleanup", "pattern": "└ ┐ (postponed, guaranteed)", "bpm_factor": 0.95},
            {"name": "Error Return", "pattern": "_, _ = f() (ignore and continue)", "bpm_factor": 1.1},
        ],
        "transition_from": {
            "Rust": "Rust's rigid grid now has breathing room. Goroutines swing where Rust forced straight 16ths.",
            "Java": "Java's orchestra feels heavy. Go's jazz combo is leaner, each musician (goroutine) essential.",
            "default": "Go brings groove where others only have beats.",
        },
        "rhythm_quote": "Go's rhythm is not in the code structure — it's in the collaboration. Channels are conversations, goroutines are solos, and the GC keeps the bass line going.",
        "beat_strength": 7,
        "ghost_note_frequency": 5,
        "swing_percentage": 15,
        "polyrhythm_depth": 3,
    },

    "Swift": {
        "bpm": 126,
        "time_signature": "4/4",
        "genre": "Chamber Pop (Elegant & Refined)",
        "genre_emoji": "🎻",
        "tempo_label": "Andante — graceful and measured",
        "description": (
            "Swift coding feels like playing in a string quartet: every gesture "
            "is deliberate, every optional nil a rest in the music, every protocol "
            "extension a new voice joining the ensemble. ARC (Automatic Reference "
            "Counting) is like a conductor tracking every musician's breath — "
            "precise but invisible to the audience."
        ),
        "signature_groove": "Elegant Legato",
        "groove_description": (
            "Swift code flows in long, connected phrases — legato lines where "
            "types flow into each other. Optional unwrapping is a breath before "
            "continuing the melody. The Swift compiler is like a patient conductor: "
            "it lets you play, only stepping in when you're truly lost."
        ),
        "syncopation_level": 4,
        "drum_pattern": [
            ("Kick",    "█   │   │   │   │ ░ │   │   │   │"),
            ("Snare",   "│   │ ░ │   │   ││   │ ░ │   │   │"),
            ("Cello",   "▓▓▓▓│▓▓▓▓│▓▓▓▓│▓▓▓▓│▓▓▓▓│▓▓▓▓│▓▓▓▓│▓▓▓▓│"),
            ("Violin",  "~~~~│~~~~│~~~~│~~~~│~~~~│~~~~│~~~~│~~~~│"),
        ],
        "common_rhythms": [
            {"name": "Optional Unwrap", "pattern": "▓ ? ▓ (safe nil check, continue or halt)", "bpm_factor": 1.0},
            {"name": "Protocol Extension", "pattern": "▓ + ▓ (adding behavior to existing types)", "bpm_factor": 0.9},
            {"name": "Async/Await", "pattern": "▓ → ▓ (sequential but non-blocking)", "bpm_factor": 1.1},
            {"name": "Result Builder", "pattern": "▓▓▓▓ (composing nested structures declaratively)", "bpm_factor": 0.85},
        ],
        "transition_from": {
            "Kotlin": "Kotlin's pragmatic tempo shifts to Swift's refined chamber aesthetic. Extensions feel like adding instruments to an existing ensemble.",
            "Rust": "Rust's rigid techno softens into Swift's legato elegance — safety without the machine click.",
            "default": "Swift brings graceful phrasing where others play in figures.",
        },
        "rhythm_quote": "Swift's rhythm is a chamber piece — intimate, refined, every voice purposeful. The protocol is the score; the compiler is the conductor.",
        "beat_strength": 6,
        "ghost_note_frequency": 4,
        "swing_percentage": 5,
        "polyrhythm_depth": 2,
    },

    "Kotlin": {
        "bpm": 132,
        "time_signature": "4/4",
        "genre": "Electronic House (Infectious & Practical)",
        "genre_emoji": "🪩",
        "tempo_label": "Allegro — fast, bright, and upbeat",
        "description": (
            "Kotlin coding feels like a DJ set at a dance club: the coroutines "
            "are layered tracks mixing seamlessly, the extension functions are "
            "remixes of existing tracks, and the null safety is the crowd control "
            "keeping the dance floor safe. It's designed to keep the energy up — "
            "pragmatic EDM that knows its audience wants to move."
        ),
        "signature_groove": "Club Four-On-The-Floor",
        "groove_description": (
            "Kotlin code is pure 4/4 house: kick on every beat, energy never drops. "
            "The bass line (JVM) is deep and reliable. Extension functions add "
            "layers without changing the track. Coroutines mix in new rhythmic "
            "patterns without stopping the main groove. The dance floor (thread) "
            "is always moving."
        ),
        "syncopation_level": 5,
        "drum_pattern": [
            ("Kick",    "█   │   │   │   │█   │   │   │   │"),
            ("Clap",    "│ ░ │ ░ │ ░ │ │ ░ │ ░ │ ░ │ │"),
            ("Hi-Hat",  "┄┄┄│┄┄│┄┄│┄▒│┄┄┄│┄┄│┄▒│┄▒│"),
            ("Bass",    "▓▓▓▓│▓▓▓▓│▓▓▓▓│▓▓▓▓│▓▓▓▓│▓▓▓▓│▓▓▓▓│▓▓▓▓│"),
        ],
        "common_rhythms": [
            {"name": "Extension Function", "pattern": "▓ + ○ = ▓ (adding methods to closed classes)", "bpm_factor": 1.0},
            {"name": "Coroutine Flow", "pattern": "▓ → ▓ → ▓ (stream of data, non-blocking)", "bpm_factor": 1.15},
            {"name": "Smart Cast", "pattern": "▓ ▓ ▓ (type narrows automatically within blocks)", "bpm_factor": 0.9},
            {"name": "Scope Function", "pattern": "let │ also │ apply │ run (four flavors)", "bpm_factor": 1.05},
        ],
        "transition_from": {
            "Swift": "Swift's chamber elegance becomes a club banger. Extensions are DJ remixes.",
            "Java": "Java's orchestral formality simplifies into Kotlin's club energy — same bass, better party.",
            "default": "Kotlin turns Java's enterprise jazz into a dance club.",
        },
        "rhythm_quote": "Kotlin's rhythm is a club night: the bass (JVM) never stops, extensions remix the playlist, and everyone dances in null safety.",
        "beat_strength": 8,
        "ghost_note_frequency": 3,
        "swing_percentage": 0,
        "polyrhythm_depth": 3,
    },

    "TypeScript": {
        "bpm": 138,
        "time_signature": "4/4",
        "genre": "Synthwave (Retro-Futuristic Digital)",
        "genre_emoji": "🌆",
        "tempo_label": "Presto — rapid and fluid",
        "description": (
            "TypeScript coding feels like driving a neon-lit highway at night: "
            "the types are lane markings keeping you from crashing, the IDE is "
            "the dashboard display, and JavaScript underneath is the engine you "
            "never see but always feel. It's synthesizer-driven coding: the "
            "analog warmth of JS with digital type safety painted over it."
        ),
        "signature_groove": "Retrowave Pulse",
        "groove_description": (
            "TypeScript code pulses with a retrofuturist beat: arpeggiated "
            "type hierarchies building like synthesizer pads, the compiler "
            "checking types like a drum machine laying down a steady kick. "
            "undefined is silence; null is a rest. The type system is the "
            "lead synth — complex, layered, sometimes overwhelming."
        ),
        "syncopation_level": 5,
        "drum_pattern": [
            ("Kick",    "█   │   │   │ ░ │█   │   │   │ ░ │"),
            ("Synth",   "░░░░│░░░░│▓▓▓▓│░░░░│░░░░│░░░░│▓▓▓▓│░░░░│"),
            ("Arp",     "◐ ◑ │ ◐ ◑ │ ◐ ◑ │ ◐ ◑ │"),
            ("Bass",    "▓▓▓▓│▓▓░░│▓▓▓▓│▓▓░░│▓▓▓▓│▓▓░░│▓▓▓▓│▓▓░░│"),
        ],
        "common_rhythms": [
            {"name": "Generic Constraint", "pattern": "<T extends ▓> (bounded polymorphism)", "bpm_factor": 1.0},
            {"name": "Union Type Match", "pattern": "▓ | ▓ | ▓ (exhaustive case handling)", "bpm_factor": 1.1},
            {"name": "Optional Chaining", "pattern": "▓?.▓?.▓ (safe deep property access)", "bpm_factor": 0.95},
            {"name": "Utility Types", "pattern": "Partial│Pick│Omit (type transformations)", "bpm_factor": 0.9},
        ],
        "transition_from": {
            "JavaScript": "JS's free jazz gets lane markings and a dashboard. The engine is the same, the ride is safer.",
            "Kotlin": "Kotlin's club energy shifts to synthwave — same BPM, different aesthetic.",
            "default": "TypeScript paints neon over JavaScript's analog warmth.",
        },
        "rhythm_quote": "TypeScript's rhythm is a retrofuture highway: types are lane markings, generics are overpasses, and the compiler is the speedometer keeping you safe.",
        "beat_strength": 7,
        "ghost_note_frequency": 4,
        "swing_percentage": 0,
        "polyrhythm_depth": 2,
    },

    "JavaScript": {
        "bpm": 144,
        "time_signature": "4/4",
        "genre": "Free Jazz / Experimental Electronic",
        "genre_emoji": "🎹",
        "tempo_label": "Molto Vivace — wild and improvisational",
        "description": (
            "JavaScript coding feels like a late-night free jazz session: "
            "everything is in flux, prototypes are spontaneous compositions, "
            "callbacks are circular breathing, and the event loop is the drummer "
            "who never stops. It is the most alive, most unpredictable, most "
            "exhilarating language to work with — if you can handle the chaos."
        ),
        "signature_groove": "Free Improvisation",
        "groove_description": (
            "JavaScript code has no fixed grid — it breathes, expands, contracts. "
            "Prototype chains link objects in real-time like musicians calling "
            "to each other across the stage. Closures capture the session's "
            "memory like a recording. The event loop is relentless — a polyrhythmic "
            "percussion layer that never stops, even when you're not playing."
        ),
        "syncopation_level": 9,
        "drum_pattern": [
            ("Kick",    "█   │ ░ │ ▓ │   │█ ░ │ ░ │ ▓ │ ░ │"),
            ("Snare",   "░ │ █ │ ░ │ ▓ │ ░ │ █ │ ░ │ ▓ │"),
            ("Keys",    "◐ ◑ ◐ │◑ ◐ ◑ │◐ ◑ ◐ │◑ ◐ ◑ │"),
            ("Loop",    "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│"),
        ],
        "common_rhythms": [
            {"name": "Callback Hell", "pattern": "f(g(h(i()))) (nesting like counterpoint)", "bpm_factor": 1.4},
            {"name": "Prototype Chain", "pattern": ".__proto__ → .__proto__ → Object", "bpm_factor": 1.0},
            {"name": "Closure Capture", "pattern": "[▓] → (▓) → [▓] (captured state)", "bpm_factor": 1.1},
            {"name": "Event Loop", "pattern": "▓ ▓ ▓ ▓ ▓ (never stops, always callbacks)", "bpm_factor": 1.5},
        ],
        "transition_from": {
            "TypeScript": "The safety net dissolves. Free jazz replaces the synthesizer — more dangerous, more alive.",
            "Python": "Python's zen simplicity explodes into JavaScript's free-form expression.",
            "default": "JavaScript removes the grid — are you ready to improvise?",
        },
        "rhythm_quote": "JavaScript's rhythm is a free jazz session — no sheet music, no rules, just the event loop as an endless polyrhythmic groove. The best musicians play without a net.",
        "beat_strength": 5,
        "ghost_note_frequency": 9,
        "swing_percentage": 25,
        "polyrhythm_depth": 5,
    },

    "Java": {
        "bpm": 108,
        "time_signature": "4/4",
        "genre": "Symphonic Jazz (Large Ensemble, Structured)",
        "genre_emoji": "🎼",
        "tempo_label": "Moderato con moto — moderate but with forward motion",
        "description": (
            "Java coding feels like conducting a jazz symphony: every instrument "
            "(thread) has a part, the conductor (JVM) keeps everyone in sync, "
            "and the music is composed well in advance (compiled). The orchestra "
            "is large, the music is complex, and everything has its place. "
            "Virtual threads (Java 21) add more musicians without more sheet music."
        ),
        "signature_groove": "Symphonic Structure",
        "groove_description": (
            "Java code is structured jazz: the composition is set, the musicians "
            "are numerous, the conductor (JVM) is experienced. Every section plays "
            "its part in lockstep when needed, improvises when allowed. The "
            "type system is the musical score — verbose but unambiguous. "
            "Checked exceptions are sheet music markings: this section may "
            "require a solo adjustment."
        ),
        "syncopation_level": 3,
        "drum_pattern": [
            ("Kick",    "█   │   │   │   │█   │   │   │   │"),
            ("Snare",   "│   │ █ │   │   ││   │ █ │   │   │"),
            ("Cymbals", "─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─"),
            ("Toms",    "▓▓  │  ▓▓│  ▓▓│  ▓▓│▓▓  │  ▓▓│  ▓▓│  ▓▓│"),
        ],
        "common_rhythms": [
            {"name": "Thread Pool", "pattern": "[▓▓▓▓] → executor → [▓▓▓▓] (concurrent workers)", "bpm_factor": 1.0},
            {"name": "Stream Pipeline", "pattern": "▓ │ ▓ │ ▓ │ ▓ (chained transformation)", "bpm_factor": 0.95},
            {"name": "Virtual Thread", "pattern": "[▓][▓][▓][▓] (lightweight, millions possible)", "bpm_factor": 1.3},
            {"name": "Lambda Expression", "pattern": "(▓) → ▓ (concise behavior passed as argument)", "bpm_factor": 1.0},
        ],
        "transition_from": {
            "JavaScript": "Free jazz becomes a symphony. Every musician has a seat, a part, and a conductor.",
            "Kotlin": "Kotlin's club energy formalizes into Java's concert hall — same jazz DNA, more formal venue.",
            "default": "Java brings symphonic structure — larger ensemble, longer composition.",
        },
        "rhythm_quote": "Java's rhythm is a symphonic jazz ensemble: the JVM is the conductor, threads are musicians, and the composition (bytecode) plays on every stage.",
        "beat_strength": 8,
        "ghost_note_frequency": 2,
        "swing_percentage": 10,
        "polyrhythm_depth": 4,
    },

    "C/C++": {
        "bpm": 160,
        "time_signature": "5/4 & 7/8 (odd meters)",
        "genre": "Progressive Metal / Math Rock",
        "genre_emoji": "🎸",
        "tempo_label": "Prestissimo — extremely fast and complex",
        "description": (
            "C/C++ coding feels like playing progressive metal: you have "
            "absolute control over every parameter, the time signatures "
            "change without warning (pointer arithmetic), and the consequences "
            "of a mistake are severe (segfault = faceplant). Templates are "
            "sweeping guitar arpeggios; RAII is the drummer hitting every "
            "accent perfectly. It's the most technically demanding genre."
        ),
        "signature_groove": "Polyrhythmic Assault",
        "groove_description": (
            "C/C++ code shifts time signatures constantly: 4/4 for simple loops, "
            "then sudden 7/8 for template metaprogramming, 5/4 for class hierarchies. "
            "Pointers are silence — rests between notes that hold meaning. "
            "The preprocessor is a DJ remixing the track at compile time. "
            "Memory management is performing the music while tuning the instrument."
        ),
        "syncopation_level": 8,
        "drum_pattern": [
            ("Kick",    "█   │   │ █ │   │█   │   │   │ █ │"),
            ("Snare",   "│   │ █ │   │ █ ││   │ █ │   │ █ │"),
            ("Guitar",  "▓▓▓▓▓│▓▓▓▓▓│▓▓▓▓▓│▓▓▓▓▓│▓▓▓▓▓│▓▓▓▓▓│"),
            ("Poly",    "3 vs 2 vs 4 ││ 5 vs 3 vs 7 ││"),
        ],
        "common_rhythms": [
            {"name": "Pointer Arithmetic", "pattern": "*p → *(p+n) → *(p+n+m) (address walking)", "bpm_factor": 1.5},
            {"name": "Template Metaprogramming", "pattern": "⟨T⟩⟨U⟩⟨V⟩ (compile-time computation)", "bpm_factor": 1.2},
            {"name": "RAII Pattern", "pattern": "[acquire] → ░░░ → [dispose] (resource tied to lifetime)", "bpm_factor": 1.0},
            {"name": "Move Semantics", "pattern": "▓ → ∅ (ownership transfer, not copy)", "bpm_factor": 0.9},
        ],
        "transition_from": {
            "Java": "Java's symphonic structure fragments into progressive metal — same complexity, rawer power.",
            "Rust": "Rust's drum machine gains guitar distortion and odd time signatures.",
            "default": "C/C++ takes back the control rod — you're the conductor now.",
        },
        "rhythm_quote": "C/C++'s rhythm is progressive metal: every time signature is allowed, every sound is possible, and the audience doesn't forgive a missed note.",
        "beat_strength": 9,
        "ghost_note_frequency": 8,
        "swing_percentage": 0,
        "polyrhythm_depth": 5,
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    """Load language rotation config."""
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_current_language() -> str:
    """Get current language from rotation without advancing."""
    config = load_rotation()
    idx = config["current_index"] % len(config["languages"])
    return config["languages"][idx]


def advance_rotation() -> Tuple[str, int]:
    """Advance rotation and return (language, new_index)."""
    config = load_rotation()
    idx = config["current_index"]
    lang = config["languages"][idx]
    new_idx = (idx + 1) % len(config["languages"])
    config["current_index"] = new_idx
    config["last_language"] = lang
    config["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation(config)
    return lang, new_idx


def get_previous_language() -> Optional[str]:
    """Get the previous language from the rotation."""
    config = load_rotation()
    return config.get("last_language")


def build_drum_grid(drum_rows: List[tuple]) -> str:
    """Build a visual ASCII drum grid from drum pattern rows."""
    lines = []
    # Header with beat numbers
    beats = "│".join(str(i + 1).rjust(3) for i in range(8))
    lines.append("     " + beats)
    lines.append("     " + "─" * 41)

    for instrument, pattern in drum_rows:
        # The pattern already has beat separators
        lines.append(f"  {instrument:<8} {pattern}")

    return "\n".join(lines)


def build_syncopation_bar(level: int) -> str:
    """Build a syncopation visualization bar."""
    filled = "█" * level
    empty = "░" * (10 - level)
    return f"[{filled}{empty}] {level}/10"


def compute_transition_feel(from_lang: str, to_lang: str) -> Dict[str, str]:
    """Describe what the transition between two languages feels like rhythmically."""
    to_data = RHYTHM_DATA.get(to_lang, {})
    transitions = to_data.get("transition_from", {})
    feel = transitions.get(from_lang, transitions.get("default", ""))
    return {
        "from": from_lang,
        "to": to_lang,
        "feel": feel,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Main Tempo Function
# ─────────────────────────────────────────────────────────────────────────────

def tempo(rotate: bool = True) -> Dict[str, Any]:
    """
    Generate a rhythm profile for the current rotation language.
    Reads language_rotation.json, selects the current language,
    and generates a full musical rhythm analysis.

    Args:
        rotate: If True, advance the rotation index after selecting.

    Returns:
        A dictionary containing the full rhythm profile.
    """
    config = load_rotation()
    languages = config["languages"]

    if rotate:
        current_lang, new_idx = advance_rotation()
    else:
        idx = config["current_index"]
        current_lang = languages[idx]
        new_idx = idx

    prev_lang = get_previous_language()
    data = RHYTHM_DATA.get(current_lang)

    if not data:
        raise ValueError(f"No rhythm data for language: {current_lang}")

    # Build drum grid visualization
    drum_grid = build_drum_grid(data["drum_pattern"])

    # Build rhythm patterns display
    rhythm_patterns = []
    for rhythm in data["common_rhythms"]:
        rhythm_patterns.append({
            "name": rhythm["name"],
            "pattern": rhythm["pattern"],
            "bpm_factor": rhythm["bpm_factor"],
            "effective_bpm": round(data["bpm"] * rhythm["bpm_factor"]),
        })

    # Compute transition
    transition = None
    if prev_lang:
        transition = compute_transition_feel(prev_lang, current_lang)

    # Get next language
    next_lang = languages[(new_idx) % len(languages)]

    # Build polyrhythm visualization
    polyrhythm_vis = " × ".join(str(i + 1) for i in range(data["polyrhythm_depth"]))

    # Build swing/syncopation summary
    swing_label = (
        "Straight (0%)" if data["swing_percentage"] == 0 else
        f"Shuffle ({data['swing_percentage']}%)" if data["swing_percentage"] < 50 else
        f"Swung ({data['swing_percentage']}%)"
    )

    result = {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": current_lang,
        "previous_language": prev_lang,
        "next_language": next_lang,
        "rotation": languages,
        "rhythm_profile": {
            "bpm": data["bpm"],
            "tempo_label": data["tempo_label"],
            "time_signature": data["time_signature"],
            "genre": data["genre"],
            "genre_emoji": data["genre_emoji"],
            "description": data["description"],
            "signature_groove": data["signature_groove"],
            "groove_description": data["groove_description"],
        },
        "drum_grid": drum_grid,
        "syncopation": {
            "level": data["syncopation_level"],
            "bar": build_syncopation_bar(data["syncopation_level"]),
            "label": (
                "Rigid grid — every hit on the beat" if data["syncopation_level"] <= 2 else
                "Slight groove — occasional ghost notes" if data["syncopation_level"] <= 5 else
                "Heavy syncopation — off-beat emphasis throughout" if data["syncopation_level"] <= 8 else
                "Maximum syncopation — chaos groove"
            ),
        },
        "swing": {
            "percentage": data["swing_percentage"],
            "label": swing_label,
        },
        "beat_characteristics": {
            "beat_strength": data["beat_strength"],
            "ghost_note_frequency": data["ghost_note_frequency"],
            "polyrhythm_depth": data["polyrhythm_depth"],
            "polyrhythm_vis": polyrhythm_vis,
        },
        "common_rhythms": rhythm_patterns,
        "rhythm_quote": data["rhythm_quote"],
        "transition": transition,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    return result


def generate_rhythm_report(rotate: bool = True) -> Dict[str, Any]:
    """Alias for tempo() for API consistency."""
    return tempo(rotate=rotate)


def format_rhythm_card(result: Dict[str, Any]) -> str:
    """Format the rhythm result as a human-readable card."""
    rp = result["rhythm_profile"]
    sync = result["syncopation"]
    sw = result["swing"]
    bc = result["beat_characteristics"]

    lines = [
        "═" * 60,
        f"  🎵 {result['selected_language']} — Rhythm Profile",
        "═" * 60,
        f"  BPM: {rp['bpm']} {rp['genre_emoji']} {rp['tempo_label']}",
        f"  Time Signature: {rp['time_signature']}   Genre: {rp['genre']}",
        f"  Signature Groove: {rp['signature_groove']}",
        "─" * 60,
        f"  {rp['description'][:80]}",
        f"  {rp['description'][80:160]}" if len(rp['description']) > 80 else "",
        "─" * 60,
        "  🥁 DRUM GRID (8 beats)",
        "  " + result["drum_grid"].replace("\n", "\n  "),
        "─" * 60,
        f"  Syncopation: {sync['bar']} — {sync['label']}",
        f"  Swing: {sw['label']}   Polyrhythm: {bc['polyrhythm_vis']}",
        f"  Beat Strength: {bc['beat_strength']}/10   Ghost Notes: {bc['ghost_note_frequency']}/10",
        "─" * 60,
        "  🎶 COMMON RHYTHMS",
    ]

    for i, rhythm in enumerate(result["common_rhythms"], 1):
        lines.append(f"    {i}. {rhythm['name']}: {rhythm['pattern']} "
                     f"(×{rhythm['bpm_factor']} → ~{rhythm['effective_bpm']} BPM)")

    lines += [
        "─" * 60,
        f"  💬 \"{result['rhythm_quote']}\"",
    ]

    if result.get("transition"):
        t = result["transition"]
        lines += [
            "─" * 60,
            f"  🔄 TRANSITION: {t['from']} → {t['to']}",
            f"     {t['feel']}",
        ]

    lines += [
        "─" * 60,
        f"  Next in rotation: {result['next_language']}",
        f"  Rotation: {' → '.join(result['rotation'])} → {result['rotation'][0]}",
        "═" * 60,
    ]

    return "\n".join(line for line in lines if line)


# ─────────────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────────────

def run_tests() -> None:
    """Run tests to validate the Polyglot Tempo module."""
    tests_passed = 0
    tests_failed = 0

    def assert_eq(a: Any, b: Any, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a == b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — expected {b!r}, got {a!r}")

    def assert_in(a: str, b: str, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a in b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — '{a}' not in '{b}'")

    def assert_true(a: Any, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg}")

    def assert_keys(d: Dict, keys: List[str], msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        missing = [k for k in keys if k not in d]
        if not missing:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — missing keys: {missing}")

    print("🎵 Testing Polyglot Tempo...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_true(0 <= config["current_index"] < 8, "current_index in valid range")
    assert_eq("Rust", config["languages"][0], "Rust is first language")

    print("  Testing tempo() function...")
    result = tempo(rotate=False)

    required_keys = [
        "tool", "version", "selected_language", "previous_language",
        "next_language", "rotation", "rhythm_profile", "drum_grid",
        "syncopation", "swing", "beat_characteristics", "common_rhythms",
        "rhythm_quote", "transition", "timestamp"
    ]
    assert_keys(result, required_keys, "All required keys present in result")

    assert_eq(TOOL_NAME, result["tool"], "Correct tool name")
    assert_eq(TOOL_VERSION, result["version"], "Correct version")

    print("  Verifying rhythm_profile structure...")
    rp = result["rhythm_profile"]
    rp_keys = ["bpm", "tempo_label", "time_signature", "genre", "genre_emoji",
               "description", "signature_groove", "groove_description"]
    assert_keys(rp, rp_keys, "rhythm_profile has all required fields")
    assert_true(60 <= rp["bpm"] <= 200, "BPM in reasonable musical range (60-200)")
    assert_true("/" in rp["time_signature"], "Time signature contains '/'")

    print("  Verifying drum_grid is non-empty and multi-line...")
    assert_true(len(result["drum_grid"]) > 50, "drum_grid is substantial")
    assert_true(result["drum_grid"].count("\n") >= 3, "drum_grid has multiple rows")

    print("  Verifying syncopation structure...")
    sync = result["syncopation"]
    assert_true(1 <= sync["level"] <= 10, "syncopation level is 1-10")
    assert_true("[" in sync["bar"] and "]" in sync["bar"], "syncopation bar is formatted")
    assert_true(len(sync["label"]) > 10, "syncopation label is meaningful")

    print("  Verifying swing structure...")
    sw = result["swing"]
    assert_true(0 <= sw["percentage"] <= 100, "swing percentage 0-100")
    assert_true(len(sw["label"]) > 0, "swing label is non-empty")

    print("  Verifying beat_characteristics...")
    bc = result["beat_characteristics"]
    assert_true(1 <= bc["beat_strength"] <= 10, "beat_strength 1-10")
    assert_true(1 <= bc["ghost_note_frequency"] <= 10, "ghost_note_frequency 1-10")
    assert_true(1 <= bc["polyrhythm_depth"] <= 5, "polyrhythm_depth 1-5")
    assert_true("×" in bc["polyrhythm_vis"], "polyrhythm_vis shows multiplication")

    print("  Verifying common_rhythms...")
    rhythms = result["common_rhythms"]
    assert_true(len(rhythms) >= 3, f"common_rhythms has {len(rhythms)} entries (>= 3)")
    for rhythm in rhythms:
        assert_true("name" in rhythm, "rhythm has name")
        assert_true("pattern" in rhythm, "rhythm has pattern")
        assert_true("bpm_factor" in rhythm, "rhythm has bpm_factor")
        assert_true("effective_bpm" in rhythm, "rhythm has effective_bpm")
        assert_true(0.5 <= rhythm["bpm_factor"] <= 2.0, "bpm_factor is reasonable")

    print("  Verifying all languages have rhythm data...")
    for lang in config["languages"]:
        data = RHYTHM_DATA.get(lang)
        assert_true(data is not None, f"Rhythm data exists for {lang}")
        assert_true("bpm" in data, f"{lang} has bpm")
        assert_true("genre" in data, f"{lang} has genre")
        assert_true("drum_pattern" in data, f"{lang} has drum_pattern")
        assert_true(len(data["drum_pattern"]) >= 3, f"{lang} drum_pattern has >= 3 rows")
        assert_true("common_rhythms" in data, f"{lang} has common_rhythms")
        assert_true(len(data["common_rhythms"]) >= 3, f"{lang} has >= 3 common rhythms")
        assert_true("rhythm_quote" in data, f"{lang} has rhythm_quote")

    print("  Verifying rotation advances correctly...")
    initial_config = load_rotation()
    initial_idx = initial_config["current_index"]

    result1 = tempo(rotate=True)
    config_after = load_rotation()
    expected_idx = (initial_idx + 1) % len(config["languages"])
    assert_eq(expected_idx, config_after["current_index"], "Rotation advanced by 1")
    assert_eq(initial_config["languages"][initial_idx], config_after["last_language"],
              "last_language updated correctly")

    print("  Verifying tempo with rotation=False does NOT advance...")
    idx_before = load_rotation()["current_index"]
    result_norotate = tempo(rotate=False)
    idx_after = load_rotation()["current_index"]
    assert_eq(idx_before, idx_after, "Index unchanged when rotate=False")

    print("  Verifying get_current_language()...")
    lang = get_current_language()
    assert_true(lang in config["languages"], f"get_current_language returns valid language: {lang}")

    print("  Verifying compute_transition_feel()...")
    trans = compute_transition_feel("Rust", "Go")
    assert_true("from" in trans and "to" in trans and "feel" in trans,
                "transition has from/to/feel")
    assert_eq("Rust", trans["from"], "transition from Rust")
    assert_eq("Go", trans["to"], "transition to Go")
    assert_true(len(trans["feel"]) > 20, "transition feel is meaningful")

    print("  Testing transition between all language pairs...")
    for lang in config["languages"]:
        for prev_lang in config["languages"]:
            if lang != prev_lang:
                t = compute_transition_feel(prev_lang, lang)
                assert_eq(lang, t["to"], f"transition to {lang} from {prev_lang} is valid")

    print("  Verifying format_rhythm_card()...")
    card = format_rhythm_card(result)
    assert_true("DRUM GRID" in card, "Card contains DRUM GRID section")
    assert_true("COMMON RHYTHMS" in card, "Card contains COMMON RHYTHMS section")
    assert_true("Syncopation" in card, "Card contains Syncopation")
    assert_true("Transition" in card or "Next in rotation" in card,
                "Card contains transition or rotation info")

    print("  Testing BPM range across languages...")
    bpm_values = [RHYTHM_DATA[lang]["bpm"] for lang in config["languages"]]
    assert_true(min(bpm_values) >= 100, f"Fastest language BPM: {min(bpm_values)} (Rust should be ~120)")
    assert_true(max(bpm_values) <= 165, f"Slowest language BPM: {max(bpm_values)} (C/C++ should be ~160)")

    print("  Testing time signatures...")
    for lang in config["languages"]:
        ts = RHYTHM_DATA[lang]["time_signature"]
        assert_true("/" in ts, f"{lang} has valid time signature: {ts}")

    print("  Testing genre emojis...")
    for lang in config["languages"]:
        emoji = RHYTHM_DATA[lang]["genre_emoji"]
        assert_true(len(emoji) > 0, f"{lang} has genre emoji: {emoji}")

    print(f"\n{'=' * 55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("🎵 All Tempo tests passed! The rhythm is undeniable.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)
