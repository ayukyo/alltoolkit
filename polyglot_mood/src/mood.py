"""Core mood analysis engine for Polyglot Mood."""

from dataclasses import dataclass, field
from pathlib import Path
import json
from datetime import datetime, timezone, timedelta
from typing import Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[2]
ROTATION_FILE = _REPO_ROOT / "language_rotation.json"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class MoodSpectrum:
    """Five-axis emotional fingerprint for a language."""
    intensity: float      # 0.0–1.0  calm → energetic
    warmth: float         # 0.0–1.0  cold/clinical → warm/friendly
    discipline: float     # 0.0–1.0  chaotic → disciplined
    creativity: float     # 0.0–1.0  pragmatic → creative
    confidence: float    # 0.0–1.0  uncertain → bold


@dataclass
class MoodProfile:
    """Full personality profile for a language."""
    language: str
    archetype: str
    tagline: str
    spectrum: MoodSpectrum
    haiku: str
    coding_tips: list
    emotional_terrain: str   # one-liner description of dev experience


@dataclass
class VibeCheck:
    """Comparison report between two consecutive languages."""
    from_language: str
    to_language: str
    mood_shift: str           # e.g., "disciplined → expressive"
    advice: str               # how to "feel" the transition
    contrast_score: float    # 0.0 = identical vibes, 1.0 = completely different


# ---------------------------------------------------------------------------
# Language personality database
# ---------------------------------------------------------------------------

LANGUAGE_MOODS = {
    "Rust": {
        "archetype": "The Perfectionist",
        "tagline": "If it compiles, it works. If it doesn't, you're learning.",
        "spectrum": MoodSpectrum(
            intensity=0.65,
            warmth=0.55,
            discipline=0.95,
            creativity=0.70,
            confidence=0.80,
        ),
        "haiku": (
            "The borrow checker counts,\n"
            "every lifetime, every breath—\n"
            "memory sleeps in peace."
        ),
        "coding_tips": [
            "Embrace the compiler's feedback as a mentor, not a critic.",
            "Ownership isn't restriction — it's freedom from bugs.",
            "Start with a working mess, then refactor toward ownership correctness.",
            "Pattern matching is your friend; lean into match expressions.",
            "The stdlib is a treasure chest — explore it before reaching for crates.io.",
        ],
        "emotional_terrain": "Exacting but deeply rewarding — like solving a puzzle that was designed just for you.",
    },
    "Go": {
        "archetype": "The Pragmatist",
        "tagline": "Simple is hard. Hard is simple.",
        "spectrum": MoodSpectrum(
            intensity=0.70,
            warmth=0.80,
            discipline=0.75,
            creativity=0.50,
            confidence=0.85,
        ),
        "haiku": (
            "Goroutines flow,\n"
            "channels of quiet thought—\n"
            "concurrency sings."
        ),
        "coding_tips": [
            "Write the happy path first, then handle errors — don't pre-optimize error handling.",
            "Interfaces are implicit; design for what you need, not what you declare.",
            "gofmt is not a suggestion — let it format your code automatically.",
            "Keep it simple: one package, one responsibility, clean boundaries.",
            "Defer cleanup: use defer for resource teardown, always.",
        ],
        "emotional_terrain": "Cheerful and surprisingly deep — a language that rewards clarity over cleverness.",
    },
    "Swift": {
        "archetype": "The Elegant Expressive",
        "tagline": "Clarity at the speed of thought.",
        "spectrum": MoodSpectrum(
            intensity=0.60,
            warmth=0.85,
            discipline=0.75,
            creativity=0.90,
            confidence=0.75,
        ),
        "haiku": (
            "Optionals unwrap,\n"
            "safety weaves through the code—\n"
            "iOS dreams in Swift."
        ),
        "coding_tips": [
            "Let Swift infer types — let the compiler do the work.",
            "Use guard early and often for early exit and optional unwrapping.",
            "Structs for values, classes for identity — this single rule solves most design questions.",
            "Protocols are first-class — think in protocol composition, not inheritance.",
            "Embrace the standard library: map, filter, reduce are your artistic tools.",
        ],
        "emotional_terrain": "Refined and empowering — coding feels like composing a poem that actually runs.",
    },
    "Kotlin": {
        "archetype": "The Pragmatic Poet",
        "tagline": "Concision without sacrifice. Safety without ceremony.",
        "spectrum": MoodSpectrum(
            intensity=0.55,
            warmth=0.80,
            discipline=0.80,
            creativity=0.75,
            confidence=0.80,
        ),
        "haiku": (
            "Extension functions bloom,\n"
            "null safety guides the way—\n"
            "JVM dances light."
        ),
        "coding_tips": [
            "Use extension functions liberally — they make APIs read like natural speech.",
            "data classes replace POJOs; datacopy replaces builders.",
            "Coroutines are not async callbacks — think in sequential code that happens to suspend.",
            "Sealed classes are your friend for modeling exhaustive state.",
            "Prefer expression syntax: if/when/try are expressions, not statements.",
        ],
        "emotional_terrain": "Sophisticated yet approachable — Java's power with Scala's elegance and none of the complexity tax.",
    },
    "TypeScript": {
        "archetype": "The Type Defender",
        "tagline": "Catch the bug before it hatches.",
        "spectrum": MoodSpectrum(
            intensity=0.75,
            warmth=0.70,
            discipline=0.70,
            creativity=0.65,
            confidence=0.75,
        ),
        "haiku": (
            "Types guard the code,\n"
            "generics flow like river—\n"
            "JavaScript grows up."
        ),
        "coding_tips": [
            "Enable strict mode on day one — it's the only way to fly.",
            "Define interfaces for objects, type aliases for primitives and unions.",
            "Utility types (Partial, Required, Pick, Omit) are productivity superpowers.",
            "Don't any — if you need flexibility, use unknown and narrow it.",
            "Generic constraints are more valuable than generics themselves.",
        ],
        "emotional_terrain": "Empowering and slightly demanding — the type system feels like a safety net that asks you to be precise.",
    },
    "JavaScript": {
        "archetype": "The Free Spirit",
        "tagline": "If it works, it works. Let's ship it.",
        "spectrum": MoodSpectrum(
            intensity=0.90,
            warmth=0.75,
            discipline=0.45,
            creativity=0.85,
            confidence=0.70,
        ),
        "haiku": (
            "Callbacks cascade,\n"
            "async/await simplifies—\n"
            "the web breathes in JS."
        ),
        "coding_tips": [
            "Embrace the dynamic nature — use typeof and instanceof for type narrowing.",
            "Array methods (map, filter, reduce) are more expressive than for-loops.",
            "const over let over var — make immutability your default.",
            "Template literals and destructuring are life-changing — use them always.",
            "The event loop is your mental model — understand it before debugging async.",
        ],
        "emotional_terrain": "Exhilaratingly free and occasionally bewildering — the language that teaches you to adapt.",
    },
    "Java": {
        "archetype": "The Enterprise Architect",
        "tagline": "Built to last. Built to scale.",
        "spectrum": MoodSpectrum(
            intensity=0.50,
            warmth=0.55,
            discipline=0.90,
            creativity=0.40,
            confidence=0.85,
        ),
        "haiku": (
            "Classes load and wait,\n"
            "JVM hums beneath the surface—\n"
            "enterprise wakes."
        ),
        "coding_tips": [
            "Favor composition over inheritance — it's not a guideline, it's a necessity.",
            "Streams are powerful but don't overuse them — readable > clever.",
            "Checked exceptions are a mixed blessing — use them judiciously.",
            "Optional is for library return types, not fields — don't box primitive fields.",
            "Immutability by default — use final fields and builder patterns.",
        ],
        "emotional_terrain": "Serious and reliable — the language that means business and gets things done at scale.",
    },
    "C/C++": {
        "archetype": "The Control Magician",
        "tagline": "You are the memory manager now.",
        "spectrum": MoodSpectrum(
            intensity=0.80,
            warmth=0.40,
            discipline=0.85,
            creativity=0.75,
            confidence=0.90,
        ),
        "haiku": (
            "Pointers and the stack,\n"
            "manual memory whispers—\n"
            "control is absolute."
        ),
        "coding_tips": [
            "Every malloc needs a free — RAII and smart pointers when possible.",
            "Understand the value categories: lvalue, xvalue, prvalue — this unlocks everything.",
            "const correctness is not optional — it's the foundation of safe code.",
            "Templates enable zero-cost abstractions — learn them deeply.",
            "Debug with gdb/lldb的心态 — printf debugging is a stepping stone, not a destination.",
        ],
        "emotional_terrain": "Exhilaratingly powerful and unforgiving — every line demands intention.",
    },
}


# ---------------------------------------------------------------------------
# Mood analysis
# ---------------------------------------------------------------------------

def _load_rotation() -> dict:
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_rotation(data: dict) -> None:
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _compute_mood_shift(from_spectrum: MoodSpectrum, to_spectrum: MoodSpectrum) -> str:
    """Generate a human-readable mood shift description."""
    shifts = []
    axes = [
        ("intensity", "intensity"),
        ("warmth", "warmth"),
        ("discipline", "discipline"),
        ("creativity", "creativity"),
        ("confidence", "confidence"),
    ]
    for attr, label in axes:
        from_val = getattr(from_spectrum, attr)
        to_val = getattr(to_spectrum, attr)
        delta = to_val - from_val
        if abs(delta) >= 0.3:
            direction = "↑" if delta > 0 else "↓"
            shifts.append(f"{label} {direction}")
    if not shifts:
        return "subtle emotional shift"
    return ", ".join(shifts)


def _compute_contrast(from_spectrum: MoodSpectrum, to_spectrum: MoodSpectrum) -> float:
    """Compute contrast score between two mood spectra (0.0 = identical, 1.0 = maximally different)."""
    axes = ["intensity", "warmth", "discipline", "creativity", "confidence"]
    total_diff = sum(
        abs(getattr(from_spectrum, ax) - getattr(to_spectrum, ax))
        for ax in axes
    )
    return total_diff / len(axes)


def _build_transition_advice(from_lang: str, to_lang: str, contrast: float) -> str:
    """Generate advice for navigating the emotional transition between languages."""
    if contrast < 0.15:
        return (
            f"The mood is similar between {from_lang} and {to_lang}. "
            f"Carry forward your energy — the emotional shift is gentle."
        )
    elif contrast < 0.30:
        return (
            f"You're transitioning from {from_lang} to {to_lang}. "
            f"Let go of {from_lang}'s habits and embrace the new emotional register."
        )
    else:
        return (
            f"Buckle up — {from_lang} to {to_lang} is a significant mood shift. "
            f"Give yourself permission to feel like a beginner again."
        )


def get_mood_profile(language: str, rotate: bool = True) -> MoodProfile:
    """Get the mood profile for a language.

    Args:
        language: Language name (e.g., "Rust", "Go").
        rotate: If True, advance current_index in language_rotation.json.

    Returns:
        MoodProfile for the language.

    Raises:
        ValueError: If language is not in LANGUAGE_MOODS.
    """
    if language not in LANGUAGE_MOODS:
        raise ValueError(f"Unknown language: {language!r}")

    data = LANGUAGE_MOODS[language]
    spectrum_dict = data["spectrum"]

    profile = MoodProfile(
        language=language,
        archetype=data["archetype"],
        tagline=data["tagline"],
        spectrum=MoodSpectrum(
            intensity=spectrum_dict.intensity,
            warmth=spectrum_dict.warmth,
            discipline=spectrum_dict.discipline,
            creativity=spectrum_dict.creativity,
            confidence=spectrum_dict.confidence,
        ),
        haiku=data["haiku"],
        coding_tips=data["coding_tips"],
        emotional_terrain=data["emotional_terrain"],
    )

    if rotate:
        config = _load_rotation()
        languages = config["languages"]
        if language in languages:
            current_idx = languages.index(language)
            next_idx = (current_idx + 1) % len(languages)
            config["current_index"] = next_idx
            config["last_language"] = language
            config["updated_at"] = datetime.now(timezone.utc).isoformat()
            _save_rotation(config)

    return profile


def get_consecutive_mood(rotate: bool = True) -> tuple:
    """Get mood profiles for the current and next language in rotation.

    Args:
        rotate: If True, advance the rotation index.

    Returns:
        Tuple of (current_mood, vibe_check). vibe_check is None if rotation is empty.
    """
    config = _load_rotation()
    languages = config["languages"]
    current_idx = config.get("current_index", 0) % len(languages)

    current_lang = languages[current_idx]
    next_idx = (current_idx + 1) % len(languages)
    next_lang = languages[next_idx]

    current_mood = get_mood_profile(current_lang, rotate=False)

    if not rotate:
        return current_mood, None

    # Advance rotation
    config["current_index"] = next_idx
    config["last_language"] = next_lang
    config["updated_at"] = datetime.now(timezone.utc).isoformat()
    _save_rotation(config)

    # Build vibe check
    next_mood_data = LANGUAGE_MOODS[next_lang]
    next_spectrum_dict = next_mood_data["spectrum"]
    next_spectrum = MoodSpectrum(
        intensity=next_spectrum_dict.intensity,
        warmth=next_spectrum_dict.warmth,
        discipline=next_spectrum_dict.discipline,
        creativity=next_spectrum_dict.creativity,
        confidence=next_spectrum_dict.confidence,
    )

    shift = _compute_mood_shift(current_mood.spectrum, next_spectrum)
    contrast = _compute_contrast(current_mood.spectrum, next_spectrum)
    advice = _build_transition_advice(current_lang, next_lang, contrast)

    vibe_check = VibeCheck(
        from_language=current_lang,
        to_language=next_lang,
        mood_shift=shift,
        advice=advice,
        contrast_score=contrast,
    )

    return current_mood, vibe_check