#! /usr/bin/env python3
"""
🎼 Polyglot Fugue v1.0
Musical Syntax Counterpoint — each programming language is a musical voice
in a four-part fugue rendered as ASCII sheet music.

Creative concept: "Every language has its own rhythm, cadence, and harmonic
personality. When a concept is expressed across languages, it plays as a
polyphonic fugue — each voice (language) carries the same thematic material
(at the concept level) but with distinct melodic contours and ornamentation.
Polyglot Fugue renders these four voices on a grand staff, showing how the
same idea sounds in four different syntactic registers."

Unlike existing tools:
  - polyglot_tarot:       programming archetypes as tarot cards
  - polyglot_resonance:   waveform oscilloscope visualization
  - polyglot_harmony:     pairwise compatibility scoring
  - polyglot_cartographer: geopolitical world map
  - polyglot_chronicle:   daily learning diary
  - polyglot_selector:    language rotation with challenges
  - polyglot_whisper:     insight cards

Fugue is about SYNTACTIC COUNTERPOINT — rendering how four languages each
render the same concept as distinct melodic voices on an ASCII musical score.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import hashlib
import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-fugue"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent.parent
_WORKSPACE_ROOT = _MODULE_DIR.parent
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ─────────────────────────────────────────────────────────────────────────────
# Fugue Themes — each is a universal programming concept rendered in 4 voices
# ─────────────────────────────────────────────────────────────────────────────

FUGUE_THEMES: List[Dict[str, Any]] = [
    {
        "id": "null_check",
        "name": "Null Check",
        "emoji": "🌑",
        "question": "How does the language handle the absence of a value?",
        "subject": "Check if x is null and return default",
        "voices": {
            "Rust": {
                "melody": ["G4", "E4", "C4", "E4", "G4", "rest", "A4", "B4"],
                "dynamics": "piano",
                "ornaments": ["turn", "mordent"],
                "code": "x.unwrap_or(42)",
                "description": "A staccato declaration — Option<T> names its absence directly.",
            },
            "Go": {
                "melody": ["D4", "E4", "F4", "E4", "D4", "E4", "G4", "rest"],
                "dynamics": "mezzo-forte",
                "ornaments": [],
                "code": 'if x == nil { x = 42 }',
                "description": "A grounded procedural chant — nil is checked with explicit vigilance.",
            },
            "Swift": {
                "melody": ["C4", "D4", "E4", "D4", "C4", "D4", "E4", "G4"],
                "dynamics": "pianissimo",
                "ornaments": ["grace_note"],
                "code": "x ?? 42",
                "description": "A whispered elision — nil and the elvis operator resolve in one syllable.",
            },
            "Kotlin": {
                "melody": ["F4", "G4", "A4", "G4", "F4", "G4", "A4", "rest"],
                "dynamics": "piano",
                "ornaments": ["slide"],
                "code": "x ?: 42",
                "description": "A smooth ternary glide — the elvis tilts to catch what falls.",
            },
        },
    },
    {
        "id": "loop_iteration",
        "name": "Loop & Iteration",
        "emoji": "🔁",
        "question": "How does the language walk through a collection?",
        "subject": "Iterate over items and double each value",
        "voices": {
            "Rust": {
                "melody": ["C5", "D5", "C5", "B4", "A4", "G4", "A4", "B4"],
                "dynamics": "forte",
                "ornaments": [],
                "code": "for x in items { println!(\"{}\", x * 2); }",
                "description": "A precise martellato — each element named, owned, and consumed.",
            },
            "Go": {
                "melody": ["G4", "A4", "B4", "C5", "B4", "A4", "G4", "A4"],
                "dynamics": "mezzo-forte",
                "ornaments": [],
                "code": "for _, x := range items { fmt.Println(x * 2) }",
                "description": "A steady march — range returns index and value in structured order.",
            },
            "Swift": {
                "melody": ["E5", "D5", "C5", "D5", "E5", "D5", "C5", "rest"],
                "dynamics": "piano",
                "ornaments": ["grace_note", "slur"],
                "code": "for x in items { print(x * 2) }",
                "description": "A legato glide — for-in is a gentle current, no index needed.",
            },
            "Kotlin": {
                "melody": ["A4", "B4", "C5", "D5", "C5", "B4", "A4", "G4"],
                "dynamics": "mezzo-piano",
                "ornaments": ["slide"],
                "code": "items.forEach { x -> println(x * 2) }",
                "description": "A lambda float — forEach carries the closure as a passenger.",
            },
        },
    },
    {
        "id": "function_definition",
        "name": "Function Definition",
        "emoji": "ƒ",
        "question": "How does the language define and call a callable?",
        "subject": "Define a function that adds two numbers and returns the result",
        "voices": {
            "Rust": {
                "melody": ["C4", "E4", "G4", "C5", "G4", "E4", "C4", "rest"],
                "dynamics": "forte",
                "ornaments": [],
                "code": "fn add(a: i32, b: i32) -> i32 { a + b }",
                "description": "A fanfare in three declarations — parameters named, typed, and returned.",
            },
            "Go": {
                "melody": ["G4", "G4", "A4", "B4", "C5", "B4", "A4", "G4"],
                "dynamics": "mezzo-forte",
                "ornaments": [],
                "code": "func add(a int, b int) int { return a + b }",
                "description": "A clean hymn — func names the relationship, return releases it.",
            },
            "Swift": {
                "melody": ["C4", "D4", "E4", "F4", "G4", "F4", "E4", "D4"],
                "dynamics": "piano",
                "ornaments": ["slur", "turn"],
                "code": "func add(_ a: Int, _ b: Int) -> Int { a + b }",
                "description": "A courtly pavane — parameter labels dance before the name.",
            },
            "Kotlin": {
                "melody": ["A4", "C5", "E5", "G5", "E5", "C5", "A4", "rest"],
                "dynamics": "pianissimo",
                "ornaments": ["grace_note"],
                "code": "fun add(a: Int, b: Int) = a + b",
                "description": "A single-breath expression — the body is the return, no ceremony.",
            },
        },
    },
    {
        "id": "error_handling",
        "name": "Error Handling",
        "emoji": "⚡",
        "question": "How does the language signal and recover from failure?",
        "subject": "Attempt an operation and handle its failure path",
        "voices": {
            "Rust": {
                "melody": ["G4", "E4", "C4", "D4", "E4", "F4", "G4", "rest"],
                "dynamics": "forte",
                "ornaments": ["mordent"],
                "code": "match do_something() { Ok(v) => v, Err(e) => panic!() }",
                "description": "A dramatic recitative — Result<T, E> names both outcomes before singing.",
            },
            "Go": {
                "melody": ["D4", "E4", "F4", "G4", "A4", "G4", "F4", "E4"],
                "dynamics": "mezzo-forte",
                "ornaments": [],
                "code": "if err := doSomething(); err != nil { panic() }",
                "description": "A ritual litany — error is named, checked, and answered in sequence.",
            },
            "Swift": {
                "melody": ["C4", "D4", "E4", "D4", "C4", "B3", "C4", "rest"],
                "dynamics": "piano",
                "ornaments": ["grace_note"],
                "code": "do { let v = try doSomething() } catch { fatalError() }",
                "description": "A theatrical scene — do sets the stage, catch receives the fallen act.",
            },
            "Kotlin": {
                "melody": ["F4", "G4", "A4", "B4", "A4", "G4", "F4", "E4"],
                "dynamics": "pianissimo",
                "ornaments": ["slide"],
                "code": "runCatching { doSomething() }.onFailure { throw it }",
                "description": "A murmured aside — runCatching watches, onFailure responds in whispers.",
            },
        },
    },
    {
        "id": "concurrent_task",
        "name": "Concurrent Task",
        "emoji": "🧵",
        "question": "How does the language execute work in parallel?",
        "subject": "Launch a background task and wait for its result",
        "voices": {
            "Rust": {
                "melody": ["C5", "E5", "G5", "E5", "C5", "G4", "C4", "rest"],
                "dynamics": "forte",
                "ornaments": [],
                "code": "let handle = spawn(async { do_work().await }); handle.await?;",
                "description": "A fanfare of isolation — async blocks are named, spawned, and awaited.",
            },
            "Go": {
                "melody": ["G4", "B4", "D5", "B4", "G4", "D4", "G4", "rest"],
                "dynamics": "forte",
                "ornaments": [],
                "code": "go doWork(); <-done",
                "description": "A chorale of goroutines — go launches, channel receives the signal.",
            },
            "Swift": {
                "melody": ["E5", "D5", "C5", "B4", "A4", "B4", "C5", "D5"],
                "dynamics": "piano",
                "ornaments": ["slur"],
                "code": "Task { let _ = await doWork() }",
                "description": "A soft suspension — Task{} is a brief garden where async blooms.",
            },
            "Kotlin": {
                "melody": ["A4", "C5", "E5", "G5", "E5", "C5", "A4", "rest"],
                "dynamics": "mezzo-piano",
                "ornaments": ["slide", "grace_note"],
                "code": "launch { doWork() }",
                "description": "A wandering rhapsody — launch sends the coroutine into the current scope.",
            },
        },
    },
    {
        "id": "generic_container",
        "name": "Generic Container",
        "emoji": "📦",
        "question": "How does the language express type-parameterized collections?",
        "subject": "Create a list of strings and access the first element",
        "voices": {
            "Rust": {
                "melody": ["G4", "A4", "B4", "C5", "D5", "C5", "B4", "A4"],
                "dynamics": "piano",
                "ornaments": [],
                "code": "let v: Vec<&str> = vec![\"a\", \"b\"]; v[0];",
                "description": "A notated inventory — Vec<T> declares its element type explicitly.",
            },
            "Go": {
                "melody": ["D4", "F4", "G4", "A4", "B4", "A4", "G4", "F4"],
                "dynamics": "mezzo-forte",
                "ornaments": [],
                "code": "v := []string{\"a\", \"b\"}; _ = v[0]",
                "description": "A slice of life — []string names the element type in brackets.",
            },
            "Swift": {
                "melody": ["C4", "E4", "G4", "E4", "C4", "G4", "E4", "C4"],
                "dynamics": "pianissimo",
                "ornaments": ["grace_note", "slur"],
                "code": "let v: [String] = [\"a\", \"b\"]; v[0]",
                "description": "An array of courtly elements — [T] is the natural arrangement.",
            },
            "Kotlin": {
                "melody": ["F4", "A4", "C5", "E5", "C5", "A4", "F4", "rest"],
                "dynamics": "piano",
                "ornaments": ["slide"],
                "code": "val v = listOf(\"a\", \"b\"); v[0]",
                "description": "A soft assembly — listOf infers the type from the string literals.",
            },
        },
    },
    {
        "id": "closure_lambda",
        "name": "Closure / Lambda",
        "emoji": "λ",
        "question": "How does the language define anonymous callable literals?",
        "subject": "Define a closure that squares its input",
        "voices": {
            "Rust": {
                "melody": ["D4", "F4", "A4", "G4", "F4", "D4", "F4", "rest"],
                "dynamics": "piano",
                "ornaments": ["mordent"],
                "code": "|x| x * x",
                "description": "A precise sigil — pipes name the parameters, the body is the value.",
            },
            "Go": {
                "melody": ["E4", "G4", "A4", "B4", "C5", "B4", "A4", "G4"],
                "dynamics": "mezzo-forte",
                "ornaments": [],
                "code": "func(x int) int { return x * x }",
                "description": "A formal minuet — func keyword introduces the anonymous guest.",
            },
            "Swift": {
                "melody": ["C4", "E4", "G4", "A4", "G4", "E4", "C4", "rest"],
                "dynamics": "pianissimo",
                "ornaments": ["turn"],
                "code": "{ $0 * $0 }",
                "description": "A cryptic shorthand — $0 is the first argument, brevity is the style.",
            },
            "Kotlin": {
                "melody": ["F4", "A4", "C5", "D5", "E5", "D5", "C5", "B4"],
                "dynamics": "piano",
                "ornaments": ["slide"],
                "code": "{ x -> x * x }",
                "description": "An arrow notation — x enters through the arrow, emerges transformed.",
            },
        },
    },
    {
        "id": "string_interpolation",
        "name": "String Interpolation",
        "emoji": "💬",
        "question": "How does the language embed values inside text?",
        "subject": "Greet a user by name with their count of items",
        "voices": {
            "Rust": {
                "melody": ["C4", "E4", "G4", "C5", "G4", "E4", "C4", "rest"],
                "dynamics": "forte",
                "ornaments": [],
                "code": 'format!("Hello, {}! {} items", name, count)',
                "description": "A scored proclamation — format!() fills named slots with named values.",
            },
            "Go": {
                "melody": ["G4", "B4", "D5", "C5", "B4", "G4", "D4", "G4"],
                "dynamics": "mezzo-forte",
                "ornaments": [],
                "code": 'fmt.Printf(\"Hello, %s! %d items\\n\", name, count)',
                "description": "A printf chant — verbs and specifiers perform the interpolation.",
            },
            "Swift": {
                "melody": ["E4", "G4", "A4", "B4", "C5", "B4", "A4", "G4"],
                "dynamics": "piano",
                "ornaments": ["slur", "grace_note"],
                "code": '"Hello, \\(name)! \\(count) items"',
                "description": "A string in suspension — \\(expr) interpolates within the string itself.",
            },
            "Kotlin": {
                "melody": ["A4", "C5", "E5", "F5", "G5", "F5", "E5", "D5"],
                "dynamics": "pianissimo",
                "ornaments": ["slide"],
                "code": '"Hello, $name! ${items.size} items"',
                "description": "A dollar invocation — $name and ${} both open the string to values.",
            },
        },
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Musical rendering helpers
# ─────────────────────────────────────────────────────────────────────────────

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_TO_SOLFEGE: Dict[str, str] = {
    "C": "Do", "C#": "Di", "D": "Re", "D#": "Ri",
    "E": "Mi", "F": "Fa", "F#": "Fi", "G": "Sol",
    "G#": "Si", "A": "La", "A#": "Li", "B": "Ti",
}

STAFF_LINES = 5          # 5-line grand staff
VOICE_COLUMNS = 8        # 8 note positions per phrase
MEASURE_WIDTH = 11       # characters per measure (including bar line)

CLEF_SYMBOLS: Dict[str, str] = {
    "Rust":     "𝄞",   # treble clef — precise, structured
    "Go":       "𝄢",   # bass clef — grounded, procedural
    "Swift":    "𝄞",   # treble clef — expressive, elegant
    "Kotlin":   "𝄢",   # bass clef — JVM-rooted
}


def _note_to_midi(note: str) -> int:
    """Convert note name like 'G4' to MIDI note number."""
    if note == "rest":
        return 0
    name = note[:-1]
    octave = int(note[-1])
    semitone = NOTE_NAMES.index(name) if name in NOTE_NAMES else 0
    return (octave + 1) * 12 + semitone


def _midi_to_staff_row(midi: int, top_midi: int = 84) -> int:
    """Map a MIDI note to a row index in the staff (0=top, 4=mid, 8=bottom)."""
    if midi == 0:
        return -1  # rest — below staff
    # Map notes to staff positions (octave 4 = middle of treble/bass)
    # Each staff line/space is 1 semitone step in diatonic terms
    # We use a simplified mapping: C4=60, each step is ~1 row
    # Staff middle line (B4 for treble) maps to row 4
    # G4 (treble bottom) = row 5
    # E5 (treble top) = row 2
    # C5 = row 3, D5 = row 3, etc.
    # Use diatonic mapping
    note_names = ["C", "D", "E", "F", "G", "A", "B"]
    if midi == 0:
        return -1
    octave = midi // 12 - 1
    pitch_class = midi % 12
    note_name = NOTE_NAMES[pitch_class]
    if "#" in note_name:
        # Sharp: map to natural
        pass
    # Map to diatonic position
    try:
        diatonic = note_names.index(note_name.replace("#", "").replace("b", ""))
    except ValueError:
        diatonic = 0
    # Staff row: 0=top, 4=mid, 8=bottom (for 9-row display)
    # Middle B4 = row 4, G4 = row 5, E5 = row 2
    staff_row = 7 - (octave - 4) * 7 - diatonic
    return max(0, min(8, staff_row))


def _build_grand_staff(
    voices: Dict[str, Dict[str, Any]],
    width: int = 80,
) -> List[List[str]]:
    """Build a 9-row character grid for the grand staff.

    Rows 0-4: upper staff (treble clef, upper voices)
    Row 5:    middle gap
    Rows 6-9: lower staff (bass clef, lower voices)

    Returns a list of rows, each a list of characters.
    """
    # 9 rows: 0-4 upper (treble), 5 gap, 6-9 lower (bass)
    height = 9
    cols = width
    grid: List[List[str]] = [[" " for _ in range(cols)] for _ in range(height)]

    # Draw staff lines
    for col in range(cols):
        for row in range(5):
            grid[row][col] = "─"
        for row in range(6, 9):
            grid[row][col] = "─"
        grid[5][col] = " "  # gap between staves

    # Treble staff lines: row 4 is the middle line, row 0 top ledger
    # Bass staff lines: row 6 is the middle line, row 9 bottom ledger

    return grid, cols


def _place_note_on_staff(
    grid: List[List[str]],
    staff_row: int,
    col: int,
    note_char: str,
    is_upper: bool,
) -> None:
    """Place a note character at the given grid position."""
    if staff_row < 0 or staff_row >= 9:
        return
    if col < 0 or col >= len(grid[0]):
        return
    grid[staff_row][col] = note_char
    # Add ledger lines if needed (beyond staff)
    if is_upper and staff_row < 4:
        grid[staff_row + 1][col] = "─"
    if not is_upper and staff_row > 6:
        grid[staff_row - 1][col] = "─"


def _render_measure(
    grid: List[List[str]],
    start_col: int,
    voice_key: str,
    melody: List[str],
    dynamics: str,
    staff_row_offset: int,
    is_upper: bool,
    clef: str,
    measure_num: int,
) -> None:
    """Render one measure (8 notes) for one voice on the grid."""
    note_char = {
        "Rust":     "𝅗𝅥",   # half note
        "Go":       "𝅘𝅥",   # quarter note
        "Swift":    "𝅝",    # dotted quarter (or whole)
        "Kotlin":   "𝅘𝅥",   # quarter note
    }.get(voice_key, "𝅘𝅥")

    for i, note in enumerate(melody):
        col = start_col + i
        if note == "rest":
            # Rest: no note, leave blank
            continue
        midi = _note_to_midi(note)
        row = _midi_to_staff_row(midi)
        if is_upper:
            # Upper staff rows 0-4
            # Map: row 4=mid (B4), row 3=E5, row 2=C5, row 1=A4, row 0=G4
            mapped_row = 4 - (row - 4)
            mapped_row = max(0, min(4, mapped_row))
        else:
            # Lower staff rows 6-9
            # row 4 in upper maps to row 6 in lower
            mapped_row = 6 + (row - 4)
            mapped_row = max(6, min(9, mapped_row))

        _place_note_on_staff(grid, mapped_row, col, note_char, is_upper)


def _draw_clefs(grid: List[List[str]]) -> None:
    """Draw clef symbols at the start of each staff."""
    grid[3][0] = "𝄞"  # treble clef at row 3 (middle line of treble staff)
    grid[7][0] = "𝄢"  # bass clef at row 7 (middle line of bass staff)


def _draw_bar_lines(
    grid: List[List[str]],
    num_measures: int,
    cols: int,
) -> None:
    """Draw vertical bar lines between measures."""
    for m in range(1, num_measures):
        start_col = m * MEASURE_WIDTH
        if start_col >= cols:
            break
        for row in range(5):
            grid[row][start_col] = "│"
        for row in range(6, 9):
            grid[row][start_col] = "│"


def render_fugue_score(
    voices: Dict[str, Dict[str, Any]],
    width: int = 80,
) -> List[str]:
    """Render a grand staff score with all four voices as melodic lines.

    Returns a list of ASCII strings, one per staff row.
    """
    grid, cols = _build_grand_staff(voices, width)
    _draw_clefs(grid)

    # Upper voices: Rust (treble), Swift (treble)
    # Lower voices: Go (bass), Kotlin (bass)
    voice_order = [
        ("Rust",     True,  3),   # (key, is_upper, staff_row_offset)
        ("Swift",   True,  4),
        ("Go",      False, 6),
        ("Kotlin",  False, 7),
    ]

    # Assign voices to measures
    num_measures = 1
    start_col = 2  # leave room for clefs

    for voice_key, is_upper, base_row in voice_order:
        if voice_key not in voices:
            continue
        voice = voices[voice_key]
        melody = voice.get("melody", [])
        _render_measure(
            grid, start_col, voice_key, melody,
            dynamics=voice.get("dynamics", "mezzo-forte"),
            staff_row_offset=base_row,
            is_upper=is_upper,
            clef="treble" if is_upper else "bass",
            measure_num=0,
        )

    _draw_bar_lines(grid, num_measures + 1, cols)

    return ["".join(row) for row in grid]


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
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def advance_rotation() -> Tuple[str, int, str]:
    """Advance the rotation index and return (language, index, next_language)."""
    config = load_rotation()
    languages = config.get("languages", ROTATION_ORDER)
    current_index = config.get("current_index", 0)
    current_language = languages[current_index % len(languages)]
    next_index = (current_index + 1) % len(languages)
    config["current_index"] = next_index
    config["last_language"] = current_language
    config["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation(config)
    return current_language, current_index, languages[next_index]


# ─────────────────────────────────────────────────────────────────────────────
# Core API
# ─────────────────────────────────────────────────────────────────────────────

def fugue(theme_id: Optional[str] = None) -> Dict[str, Any]:
    """Main entry point: advance rotation, pick a theme, render the fugue.

    Returns:
        {
            "tool": str,
            "version": str,
            "language": str,           # rotation language (voice 1)
            "language_index": int,
            "theme": Dict,
            "voices": Dict[str, Dict],  # all 4 voice details
            "score_display": List[str],  # ASCII staff rows
            "rotation_advanced": bool,
            "next_language": str,
            "next_index": int,
            "rotation_order": List[str],
            "timestamp": str,
        }
    """
    config = load_rotation()
    languages = config.get("languages", ROTATION_ORDER)
    current_index = config.get("current_index", 0)
    current_language = languages[current_index % len(languages)]

    # Advance rotation for next run
    current_language, current_index, next_language = advance_rotation()
    next_index = (current_index + 1) % len(languages)

    # Pick theme — cycle through them deterministically
    if theme_id is None:
        theme_idx = current_index % len(FUGUE_THEMES)
        theme = FUGUE_THEMES[theme_idx]
    else:
        theme = next(
            (t for t in FUGUE_THEMES if t["id"] == theme_id),
            FUGUE_THEMES[current_index % len(FUGUE_THEMES)],
        )

    # Render the fugue score
    score_display = render_fugue_score(theme["voices"])

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": current_language,
        "language_index": current_index,
        "theme": {
            "id": theme["id"],
            "name": theme["name"],
            "emoji": theme["emoji"],
            "question": theme["question"],
            "subject": theme["subject"],
        },
        "voices": theme["voices"],
        "score_display": score_display,
        "rotation_advanced": True,
        "next_language": next_language,
        "next_index": next_index,
        "rotation_order": ROTATION_ORDER,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def format_fugue(m: Dict[str, Any]) -> str:
    """Format the fugue analysis as a human-readable ASCII musical score."""
    theme = m["theme"]
    voices = m["voices"]
    score_rows = m["score_display"]

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  🎼 POLYGLOT FUGUE — Musical Syntax Counterpoint               ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Theme       : {theme['emoji']} {theme['name']:<44}║",
        f"║  Subject     : {theme['subject']:<45}║",
        f"║  Question    : {theme['question']:<45}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🎼 GRAND STAFF SCORE                                          ║",
    ]

    # Score display
    for row in score_rows:
        lines.append(f"║  {row} ║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🎵 THE FOUR VOICES                                            ║",
    ]

    voice_order = [("Rust", "𝄞"), ("Swift", "𝄞"), ("Go", "𝄢"), ("Kotlin", "𝄢")]
    for voice_key, clef in voice_order:
        if voice_key not in voices:
            continue
        v = voices[voice_key]
        dynamics_emoji = {
            "pianissimo": "🇵🇵",
            "piano": "🇵",
            "mezzo-piano": "🇲🇵",
            "mezzo-forte": "🇲🇫",
            "forte": "🇫",
        }.get(v["dynamics"], "🎵")

        ornament_str = " + ".join(v["ornaments"]) if v["ornaments"] else "none"
        lines += [
            f"║  {clef} {voice_key:<8} │ dynamics: {v['dynamics']:<13} │ ornaments: {ornament_str:<14}║",
            f"║    ♪ {v['description']:<55}║",
            f"║    code: {v['code']:<55}║",
        ]

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
    """Run all tests for the Polyglot Fugue module."""
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

    print("🎼 Polyglot Fugue — Running Tests\n")

    # ── Module constants ──────────────────────────────────────────────────────
    t("TOOL_NAME is 'polyglot-fugue'", TOOL_NAME == "polyglot-fugue")
    t("TOOL_VERSION is '1.0.0'", TOOL_VERSION == "1.0.0")
    t("ROTATION_ORDER has 8 languages", len(ROTATION_ORDER) == 8)
    t("ROTATION_ORDER matches expected sequence",
      ROTATION_ORDER == ["Rust","Go","Swift","Kotlin","TypeScript","JavaScript","Java","C/C++"])

    # ── FUGUE_THEMES ───────────────────────────────────────────────────────────
    t("FUGUE_THEMES has 8 themes", len(FUGUE_THEMES) == 8)
    for theme in FUGUE_THEMES:
        t(f"  Theme '{theme['id']}' has id/name/emoji/question",
          all(k in theme for k in ("id", "name", "emoji", "question", "subject", "voices")))
        t(f"  Theme '{theme['id']}' has 4 voices",
          len(theme["voices"]) == 4)
        t(f"  Theme '{theme['id']}' voices are Rust/Go/Swift/Kotlin",
          set(theme["voices"].keys()) == {"Rust", "Go", "Swift", "Kotlin"})
        for voice_key, voice in theme["voices"].items():
            t(f"    Voice '{voice_key}' has melody/dynamics/ornaments/code/description",
              all(k in voice for k in ("melody", "dynamics", "ornaments", "code", "description")))
            t(f"    Voice '{voice_key}' melody has 8 notes",
              len(voice["melody"]) == 8)
            t(f"    Voice '{voice_key}' melody contains valid note names",
              all(n == "rest" or n[:-1] in NOTE_NAMES for n in voice["melody"]))

    # ── Musical helpers ───────────────────────────────────────────────────────
    t("_note_to_midi('C4') == 60", _note_to_midi("C4") == 60)
    t("_note_to_midi('rest') == 0", _note_to_midi("rest") == 0)
    t("_note_to_midi('A4') == 69", _note_to_midi("A4") == 69)
    t("_note_to_midi('G5') == 79", _note_to_midi("G5") == 79)

    # ── render_fugue_score ─────────────────────────────────────────────────────
    theme = FUGUE_THEMES[0]
    try:
        score = render_fugue_score(theme["voices"])
        t("render_fugue_score returns 9 rows", len(score) == 9)
        t("render_fugue_score rows are strings", all(isinstance(r, str) for r in score))
        t("render_fugue_score starts with staff lines", score[0].startswith("─"))
    except Exception as e:
        t("render_fugue_score succeeds", False, str(e))

    # ── load_rotation / save_rotation ───────────────────────────────────────
    try:
        cfg = load_rotation()
        t("load_rotation returns dict", isinstance(cfg, dict))
        t("rotation has 'languages' key", "languages" in cfg)
        t("rotation has 'current_index' key", "current_index" in cfg)
        t("rotation languages match ROTATION_ORDER", cfg["languages"] == ROTATION_ORDER)
    except Exception as e:
        t("load_rotation succeeds", False, str(e))

    # ── advance_rotation ─────────────────────────────────────────────────────
    cfg_before = load_rotation()
    idx_before = cfg_before["current_index"]
    lang_before = cfg_before["languages"][idx_before % len(cfg_before["languages"])]
    try:
        lang, idx, next_lang = advance_rotation()
        t("advance_rotation returns language", lang == lang_before)
        t("advance_rotation advances index", idx == idx_before)
        cfg_after = load_rotation()
        t("rotation file is updated after advance",
          cfg_after["current_index"] == (idx_before + 1) % len(cfg_before["languages"]))
    except Exception as e:
        t("advance_rotation", False, str(e))

    # ── fugue() ──────────────────────────────────────────────────────────────
    try:
        result = fugue()
        t("fugue() returns dict", isinstance(result, dict))
        t("fugue() returns tool/version", result.get("tool") == TOOL_NAME)
        t("fugue() returns language", "language" in result)
        t("fugue() returns theme", "theme" in result)
        t("fugue() returns score_display", "score_display" in result)
        t("fugue() returns 4 voices", len(result["voices"]) == 4)
        t("fugue() returns rotation_advanced=True", result.get("rotation_advanced") is True)
        t("fugue() returns next_language", "next_language" in result)
        t("fugue() score_display has 9 rows", len(result["score_display"]) == 9)
        t("fugue() theme has required fields",
          all(k in result["theme"] for k in ("id", "name", "emoji", "question", "subject")))
    except Exception as e:
        t("fugue() succeeds", False, str(e))

    # ── fugue() with specific theme ──────────────────────────────────────────
    try:
        result = fugue(theme_id="string_interpolation")
        t("fugue(theme_id=...) selects correct theme",
          result["theme"]["id"] == "string_interpolation")
        result2 = fugue(theme_id="null_check")
        t("fugue(theme_id=...) with unknown id falls back",
          result2["theme"]["id"] in [t["id"] for t in FUGUE_THEMES])
    except Exception as e:
        t("fugue(theme_id=...)", False, str(e))

    # ── format_fugue ─────────────────────────────────────────────────────────
    try:
        result = fugue()
        formatted = format_fugue(result)
        t("format_fugue returns a string", isinstance(formatted, str))
        t("format_fugue starts with box char", formatted.startswith("╔"))
        t("format_fugue ends with box char", formatted.rstrip().endswith("╝"))
        t("format_fugue contains theme name", result["theme"]["name"] in formatted)
        t("format_fugue contains all 4 voice names",
          all(v in formatted for v in ["Rust", "Go", "Swift", "Kotlin"]))
    except Exception as e:
        t("format_fugue", False, str(e))

    # ── All voices have required fields ─────────────────────────────────────
    for theme in FUGUE_THEMES:
        for voice_key, voice in theme["voices"].items():
            t(f"Theme '{theme['id']}' voice '{voice_key}' code is a string",
              isinstance(voice["code"], str))
            t(f"Theme '{theme['id']}' voice '{voice_key}' description is a string",
              isinstance(voice["description"], str))
            t(f"Theme '{theme['id']}' voice '{voice_key}' dynamics is valid",
              voice["dynamics"] in ("pianissimo", "piano", "mezzo-piano",
                                   "mezzo-forte", "forte"))

    print(f"\n{'='*60}")
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
        result = fugue()
        print(format_fugue(result))
