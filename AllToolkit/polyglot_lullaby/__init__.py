#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍼 Polyglot Lullaby v1.0.0
A creative tool that composes a "lullaby" for a programming language —
a soothing narrative recipe that pairs each language's anxiety points
with the comfort of idiomatic refactoring advice.

Concept: every language has its own bedtime worries. This tool reads
a code snippet (or a stress topic) and hums back a calm, structured
"lullaby": a verse list of stanzas (anxieties), refrains (idiomatic
relief), and a final benediction. Languages in the rotation get a
distinct musical key / bedtime motif.
"""

import json
import os
import re
import hashlib
from datetime import datetime
from pathlib import Path

TOOL_NAME = "polyglot-lullaby"
TOOL_VERSION = "1.0.0"

ROTATION_FILE = "language_rotation.json"

# Per-language lullaby "musical key" and short motif.
# These are *creative* choices, not technical — they give each language
# a distinct bedtime "feel" so the output is unique across the rotation.
LANGUAGE_KEY = {
    "Rust":        {"key": "D minor",  "motif": "ownership cradle",     "tempo": "andantino"},
    "Go":          {"key": "G major",  "motif": "goroutine lull",       "tempo": "moderato"},
    "Swift":       {"key": "A major",  "motif": "optional cocoon",      "tempo": "dolce"},
    "Kotlin":      {"key": "F# minor", "motif": "null-safe cradle",     "tempo": "espressivo"},
    "TypeScript":  {"key": "C major",  "motif": "typed whisper",        "tempo": "comodo"},
    "JavaScript":  {"key": "E minor",  "motif": "async hush",           "tempo": "rubato"},
    "Java":        {"key": "Bb major", "motif": "verbose blessing",     "tempo": "maestoso"},
    "C/C++":       {"key": "A minor",  "motif": "malloc midnight",      "tempo": "grave"},
}

# Verse library: anxieties + idiomatic relief per language.
# Each verse is a (anxiety_pattern, refactored_remedy) pair.
VERSE_LIBRARY = {
    "Rust": [
        ("borrow checker scolding you for a move",
         "clone only what you mean to own, and let the rest live in peace"),
        ("a lifetime longer than the program itself",
         "let the borrow checker tuck it in with a shorter scope"),
        ("an async tangle that won't unwind",
         "spawn it gently, await it patiently, and let it sleep when done"),
    ],
    "Go": [
        ("an if-else pyramid that never ends",
         "early return, so each goroutine can rest at the first signal"),
        ("a channel that's never closed",
         "close it from the sender side, the receiver will hum a thank-you"),
        ("error handling copy-pasted 400 times",
         "wrap it, name it, and let your IDE sing the refrain"),
    ],
    "Swift": [
        ("force-unwraps waiting to crash at 3am",
         "guard let, if let, or a calm nil-coalescing breath"),
        ("retain cycles looping in the night",
         "capture lists — weak, unowned — and the cycle will untie itself"),
        ("a delegate protocol that no one conforms to",
         "closures, dear friend, are sometimes the gentler path"),
    ],
    "Kotlin": [
        ("a platform type from Java haunting your null safety",
         "wrap it in let, apply, or a small `!!` of courage (sparingly)"),
        ("a coroutine that forgets to cancel",
         "structured concurrency — give it a scope, and a job, and a name"),
        ("extension functions growing into a forest",
         "group them by intent, and the forest becomes a garden"),
    ],
    "TypeScript": [
        ("any spreading like a cold through the codebase",
         "let unknown be the door, and the type guard be the key"),
        ("a generic so deep the IDE sighs",
         "name the type parameter — T is fine, Story is better"),
        ("a discriminated union that's not really discriminated",
         "add the tag, and TypeScript will sing the rest"),
    ],
    "JavaScript": [
        ("a callback pyramid from 2014",
         "async/await — the same dream, finally fluent"),
        ("a this that points somewhere unexpected",
         "arrow functions keep it close, or bind it gently by hand"),
        ("a promise that never resolves or rejects",
         "wrap it in Promise.race with a timeout — even dreams need limits"),
    ],
    "Java": [
        ("a try-catch that wraps a try-catch that wraps a try-catch",
         "try-with-resources, dear, and let AutoCloseable do the sighing"),
        ("a builder so verbose it builds itself a builder",
         "Lombok, records, or just a good old static factory — pick one and rest"),
        ("checked exceptions checked, doubled, and re-checked",
         "wrap them at the boundary, and let the business logic breathe"),
    ],
    "C/C++": [
        ("a malloc whose free is in another castle",
         "RAII — give every resource a guardian, and let the destructor hum"),
        ("a buffer that doesn't know its own size",
         "size_t at the door, capacity at the gate, length at the pillow"),
        ("undefined behavior knocking politely at midnight",
         "const, restrict, and a sanitizer — the holy trinity of bedtime"),
    ],
}

REFRAINS = [
    "hush little code, don't you cry,",
    "the compiler is a friend, not a foe,",
    "every bug is a bedtime story waiting to be told,",
    "sleep now, refactor in the morning,",
]

BENEDICTIONS = [
    "may your tests pass on the first run tomorrow.",
    "may your stack traces be short and your logs be kind.",
    "may your merge be clean and your CI be green.",
    "may your diffs be small and your coffee be warm.",
]


def _now_iso():
    """Return current local time in ISO format."""
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _digest(text):
    """Stable short hash of a string — used to pick a deterministic verse."""
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]


def _default_rotation_path():
    """Resolve language_rotation.json path: prefer workspace root, then module parent.

    Honors a patched ROTATION_FILE (used by tests to point at an explicit path).
    """
    # First honor a patched/customized ROTATION_FILE if it points to an existing file.
    rf = Path(ROTATION_FILE)
    if rf.is_absolute() and rf.exists():
        return rf
    candidates = [
        Path(__file__).parent.parent.parent / ROTATION_FILE,  # workspace root
        Path(__file__).parent.parent / ROTATION_FILE,         # AllToolkit/ sibling
        rf,                                                    # cwd / patched relative
    ]
    for c in candidates:
        if c.exists():
            return c
    # Default to workspace root if nothing exists
    return Path(__file__).parent.parent.parent / ROTATION_FILE


def load_rotation(path=None):
    """Load language_rotation.json. Resolve path relative to repo root when not given."""
    if path is None:
        path = _default_rotation_path()
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(config, path=None):
    """Persist updated rotation config back to disk."""
    if path is None:
        path = _default_rotation_path()
    path = Path(path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")


def pick_language(config, explicit=None):
    """Pick the language: explicit override, else current_index in the rotation."""
    if explicit:
        return explicit
    idx = config["current_index"] % len(config["languages"])
    return config["languages"][idx]


def detect_anxieties(snippet, language):
    """From a code snippet, detect which verses are most relevant.

    Heuristics: token-counting, common-syntactic-sugar sniffing, and a
    fallback to the language's first verse if nothing matches.
    """
    verses = VERSE_LIBRARY.get(language, [])
    if not snippet or not snippet.strip():
        # No snippet: deterministic rotation through verses via digest of "silent"
        chosen = [verses[0]] if verses else []
        return chosen

    text = snippet.lower()
    anxiety_keywords = {
        "Rust":       [("borrow", "move"), ("async", "await"), ("lifetime", "'a")],
        "Go":         [("if err", "error"), ("chan", "close"), ("go func", "goroutine")],
        "Swift":      [("!", "force"), ("self.", "delegate"), ("weak", "unowned")],
        "Kotlin":     [("platform", "!!"), ("launch", "async"), ("fun ", "extension")],
        "TypeScript": ["any", " as ", "<T", "type "],
        "JavaScript": ["function(", "=>", "this.", "promise"],
        "Java":       [("try {", "throws"), ("public class", "builder"), ("public static", "factory")],
        "C/C++":      ["malloc", "free(", "size_t", "char *"],
    }
    keys = anxiety_keywords.get(language, [])
    matched = []
    for verse in verses:
        anxiety_text = verse[0].lower()
        for k in keys:
            kw = k if isinstance(k, str) else k[0]
            if kw in text and kw in anxiety_text:
                matched.append(verse)
                break
    if not matched:
        # deterministic fallback: first verse (and maybe second, by digest parity)
        chosen = [verses[0]]
        if _digest(snippet)[-1] in "02468ace" and len(verses) > 1:
            chosen.append(verses[1])
        return chosen
    return matched


def compose_lullaby(language, snippet=""):
    """Compose the lullaby payload for a language (and optional snippet)."""
    meta = LANGUAGE_KEY.get(language, {"key": "C major", "motif": "neutral dream", "tempo": "adagio"})
    verses = detect_anxieties(snippet, language)
    if not verses:
        verses = VERSE_LIBRARY.get(language, [])[:1] or [("the unknown", "breathe, and try again")]

    # Deterministic refrain + benediction selection
    refrains = REFRAINS
    benedictions = BENEDICTIONS
    seed = _digest(language + "::" + (snippet or "silent"))
    refrain = refrains[int(seed[0], 16) % len(refrains)]
    benediction = benedictions[int(seed[1], 16) % len(benedictions)] if len(seed) > 1 else benedictions[0]

    stanza_lines = []
    for anxiety, remedy in verses:
        stanza_lines.append({"anxiety": anxiety, "remedy": remedy})

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": language,
        "key": meta["key"],
        "motif": meta["motif"],
        "tempo": meta["tempo"],
        "refrain": refrain,
        "stanzas": stanza_lines,
        "benediction": benediction,
        "composed_at": _now_iso(),
        "digest": seed,
    }


def advance_rotation(config, path=None):
    """Advance current_index in the rotation by 1 (wrapping), persist, and return new state."""
    n = len(config["languages"])
    config["current_index"] = (config["current_index"] + 1) % n
    config["last_language"] = config["languages"][(config["current_index"] - 1) % n]
    config["updated_at"] = _now_iso()
    save_rotation(config, path=path)
    return config


def run_tests():
    """Lightweight self-test runner (no pytest dependency)."""
    from polyglot_lullaby import (
        compose_lullaby, detect_anxieties, load_rotation, advance_rotation,
        LANGUAGE_KEY, VERSE_LIBRARY, REFRAINS, BENEDICTIONS,
    )
    failures = []
    for lang in ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]:
        if lang not in LANGUAGE_KEY:
            failures.append(f"missing key for {lang}")
        if lang not in VERSE_LIBRARY or not VERSE_LIBRARY[lang]:
            failures.append(f"missing verses for {lang}")
        out = compose_lullaby(lang)
        for k in ("language", "key", "motif", "tempo", "refrain", "stanzas", "benediction"):
            if k not in out:
                failures.append(f"{lang} output missing {k}")
        if not out["stanzas"]:
            failures.append(f"{lang} produced no stanzas")

    cfg = load_rotation()
    if not isinstance(cfg.get("languages"), list) or len(cfg["languages"]) < 2:
        failures.append("rotation config invalid")
    return failures


__all__ = [
    "TOOL_NAME", "TOOL_VERSION", "LANGUAGE_KEY", "VERSE_LIBRARY",
    "load_rotation", "save_rotation", "pick_language", "detect_anxieties",
    "compose_lullaby", "advance_rotation", "run_tests",
]
