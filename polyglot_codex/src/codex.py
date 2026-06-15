#!/usr/bin/env python3
"""
📜 Polyglot Codex v1.0

Literary Traditions of Programming Languages — each language is an
ancient codex with its own literary canon: proverbs, philosophy
quotes from language designers, famous maxims, Easter eggs hidden
in compilers/interpreters, and aphorisms that capture its soul.

Creative concept: "Every programming language is an ancient codex
carrying the wisdom of its creators. Rust's codex contains Graydon
Hoare's axioms of ownership. Go's codex holds Rob Pike's pragmatic
sayings. JavaScript's codex preserves Brendan Eich's philosophical
quips about first-class functions. This tool opens the codex for the
current rotation language, revealing its literary soul."

The tool generates a literary report for the current rotation language:
  - Ancient proverb (signature wisdom)
  - Designer's maxim (quote from creator/design team)
  - Famous saying (community wisdom)
  - Hidden Easter egg (compiler/interpreter secret)
  - Philosophical haiku (5-7-5 syllable meditation)
  - Literary theme (what kind of book the language would be)
  - Codex age and origin story
  - Epigraph (opening inscription)

Distinct from existing tools:
  - polyglot_signal:     signal vocabulary (how languages signal conditions)
  - polyglot_digest:     syntax-parallel code (same code, different syntax)
  - polyglot_translation: cultural idioms/proverbs (social cargo)
  - polyglot_chronology: geological timeline (deep time, epochs)
  - polyglot_harmony:    pair compatibility analysis
  - polyglot_resonator:  mental model differences
  - polyglot_tempo:      rhythm patterns (feel and cadence)
  - polyglot_mood:      emotional personality profiles
  - polyglot_craft:      practical signature patterns
  - polyglot_cartographer: geopolitical world map (spatial relationships)

Codex is about the LITERARY AND PHILOSOPHICAL soul of languages —
what wisdom they carry, who shaped their thinking, and what
aphorisms their practitioners live by. It's a library of living
wisdom from the PL world.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-codex"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent.parent
_WORKSPACE_ROOT = _MODULE_DIR.parent
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ─────────────────────────────────────────────────────────────────────────────
# Codex Database — literary canon for each language
# ─────────────────────────────────────────────────────────────────────────────

CODEX_DB: Dict[str, Dict[str, Any]] = {

    "Rust": {
        "literary_theme": "The Stoic's Codex — Discipline, Precision, and the Art of Memory",
        "codex_age": "Born 2010 (Graydon Hoare's personal project at Mozilla)",
        "origin_story": (
            "Graydon Hoare created Rust after being frustrated by C++ segfaults. "
            "The language was named after the 'rust fungus' — a resilient organism. "
            "It is the codex of the disciplined warrior who checks every resource twice."
        ),
        "epigraph": (
            "\"The Rust philosophy is: don't be sorry for the borrow checker. "
            "It is trying to save your program.\" — Graydon Hoare"
        ),
        "ancient_proverb": (
            "A resource borrowed is a resource protected; "
            "a resource owned is a resource honored."
        ),
        "designers_maxim": (
            "\"The purpose of akrepository is to make you think about ownership. "
            "If the borrow checker approves, your program is already half-correct.\" "
            "— Graydon Hoare"
        ),
        "famous_saying": (
            "In Rust, the borrow checker does not forgive — "
            "but what it approves, it protects for eternity."
        ),
        "hidden_easter_egg": (
            "Compiling Rust with --crate-type=lib produces a library so precise "
            "that the LLVM backend once rejected code that violated the One Mutable "
            "Reference rule — a rule that exists in no documentation, yet is absolute law."
        ),
        "philosophical_haiku": (
            "Ownership is truth\nBorrowed, but never forgotten\nLifetime ends clean"
        ),
        "signature_works": [
            "The Book (rust-lang.org/book) — the definitive scripture",
            "Rust RFCs — the council deliberations",
            "rustc compiler源码 — the living text",
        ],
        "literary_tone": "stoic, precise, meditative, uncompromising",
        "codex_color": "🔶",
    },

    "Go": {
        "literary_theme": "The Pragmatist's Digest — Clarity, Simplicity, and Service",
        "codex_age": "Born 2009 (Google internal project by Robert Griesemer, Rob Pike, Ken Thompson)",
        "origin_story": (
            "Robert Griesemer, Rob Pike, and Ken Thompson at Google created Go out "
            "of frustration with C++ compile times and Java's verbosity. "
            "It is the codex of the pragmatic craftsman who values clean tools."
        ),
        "epigraph": (
            "\"Go is not meant to impress. It is meant to solve problems. "
            "Simplicity is not a feature — it is the point.\" — Rob Pike"
        ),
        "ancient_proverb": (
            "Do not complicate what can be simple; "
            "do not abstract what can be clear."
        ),
        "designers_maxim": (
            "\"Less magic is better than more magic. "
            "If you need a feature to be clever, your language is failing.\" "
            "— Rob Pike"
        ),
        "famous_saying": (
            "A thousand goroutines may walk a single channel; "
            "none shall deadlock, for the channel is fair."
        ),
        "hidden_easter_egg": (
            "The Go playground at play.golang.org has a secret: the 'hello, world' "
            "program is always wrapped in a main package, but if you write 'package main' "
            "and compile with -ldflags '-s -w', the resulting binary is exactly 1.5MB "
            "smaller than the equivalent C binary — Go's runtime is minimal by design."
        ),
        "philosophical_haiku": (
            "Goroutines rise\nChannels carry, never drown\nSimplicity wins"
        ),
        "signature_works": [
            "Effective Go — the book of proper conduct",
            "The Go Blog — living wisdom",
            "go/src — the source as scripture",
        ],
        "literary_tone": "pragmatic, clear, humble, practical",
        "codex_color": "🟦",
    },

    "Swift": {
        "literary_theme": "The Poet's Anthology — Grace, Safety, and Expressive Elegance",
        "codex_age": "Born 2014 (Apple's Chris Lattner, rebuilt from Ruby & Python influences)",
        "origin_story": (
            "Chris Lattner created Swift as a replacement for Objective-C, "
            "blending Python's readability with Rust's safety and Ruby's dynamism. "
            "It is the codex of the graceful writer who values clarity above all."
        ),
        "epigraph": (
            "\"Swift is designed to be safe, fast, and expressive. "
            "Safety is not optional.\" — Chris Lattner"
        ),
        "ancient_proverb": (
            "The optional path may be nil; "
            "but the wise programmer always checks the bridge."
        ),
        "designers_maxim": (
            "\"Swift is not about what the compiler can infer — "
            "it is about what the programmer can read.\" "
            "— Chris Lattner"
        ),
        "famous_saying": (
            "In Swift, protocol composition is the art of being many things at once; "
            "in Java, you must choose your inheritance once and forever."
        ),
        "hidden_easter_egg": (
            "In Swift's REPL (swift REPL), you can type ':help' and see all REPL commands. "
            "But try ':ex' — an alias for 'expression' that is documented nowhere. "
            "It evaluates any Swift expression without a full declaration, "
            "a feature borrowed from the Lisp tradition."
        ),
        "philosophical_haiku": (
            "Protocols define\nNot what you are, but what you do\nCompose your nature"
        ),
        "signature_works": [
            "The Swift Programming Language (apple.com/swift) — the illuminated text",
            "Swift Evolution — community RFC process",
            "WWDC sessions — oral traditions",
        ],
        "literary_tone": "graceful, poetic, precise, expressive",
        "codex_color": "🟠",
    },

    "Kotlin": {
        "literary_theme": "The River Sagas — Flow, Null Safety, and Pragmatic Magic",
        "codex_age": "Born 2011 (JetBrains' Andrey Breslav, building on the JVM)",
        "origin_story": (
            "JetBrains' Andrey Breslav created Kotlin as a pragmatic alternative to Java — "
            "better syntax, null safety, and coroutines built in. "
            "Named after Kotlin Island near St. Petersburg, Russia. "
            "It is the codex of the river valley — always flowing, never overflowing."
        ),
        "epigraph": (
            "\"Kotlin is what Java would be if it were designed in 2011. "
            "Null safety is not a feature — it is a philosophy.\" — Andrey Breslav"
        ),
        "ancient_proverb": (
            "The null pointer is the source of ten thousand bugs; "
            "Kotlin makes it explicit, and the wise programmer respects it."
        ),
        "designers_maxim": (
            "\"Extension functions are not inheritance. "
            "They are adding behavior without changing lineage.\" "
            "— Andrey Breslav"
        ),
        "famous_saying": (
            "In Kotlin, the safe call operator (?.) whispers to the null: "
            "'You may pass, but only if you exist.'"
        ),
        "hidden_easter_egg": (
            "In Kotlin REPL, type 'fun main()= println(\"Hello\")' — a single-expression "
            "main function that compiles and runs. This compact syntax is valid Kotlin "
            "but not valid Java, and it reveals Kotlin's philosophy: "
            "minimal boilerplate, maximum meaning."
        ),
        "philosophical_haiku": (
            "Coroutines flow\nSuspend at the river's bend\nYield, never block"
        ),
        "signature_works": [
            "Kotlin in Action (Manning) — the complete scripture",
            "kotlinlang.org — living documentation",
            "Kotlin Coroutines design notes — the river philosophy",
        ],
        "literary_tone": "flowing, practical, modern, null-safe",
        "codex_color": "🟣",
    },

    "TypeScript": {
        "literary_theme": "The Type Guard's Chronicle — Discipline, Structure, and Transpiled Truth",
        "codex_age": "Born 2012 (Microsoft's Anders Hejlsberg, superset of JavaScript)",
        "origin_story": (
            "Anders Hejlsberg (creator of Turbo Pascal, Delphi, C#) at Microsoft "
            "created TypeScript to add static typing to JavaScript. "
            "Named 'TypeScript' because types are its defining feature. "
            "It is the codex of the careful scholar who checks documents before signing."
        ),
        "epigraph": (
            "\"TypeScript is JavaScript that scales. "
            "Types are not walls — they are contracts.\" — Anders Hejlsberg"
        ),
        "ancient_proverb": (
            "The interface is a promise; "
            "the type guard is its enforcer."
        ),
        "designers_maxim": (
            "\"TypeScript's type system is structural, not nominal. "
            "If it looks like a duck and quacks like a duck, it is a duck.\" "
            "— Anders Hejlsberg"
        ),
        "famous_saying": (
            "In TypeScript, any is the wilderness — dangerous, uncharted, "
            "but sometimes the only path through."
        ),
        "hidden_easter_egg": (
            "In TypeScript's tsconfig.json, setting 'strict: true' enables all strict "
            "type checks, but the flag 'noImplicitAny' is the most feared. "
            "Yet there is an undocumented behavior: when strict is true and a variable "
            "is inferred as 'any', the compiler does not error — it warns. "
            "Silence that warning with '// @ts-ignore' and the code compiles, "
            "revealing TypeScript's pragmatic philosophy: types guide, they do not imprison."
        ),
        "philosophical_haiku": (
            "Types as contracts\nErase at runtime's border\nYet truth remains"
        ),
        "signature_works": [
            "TypeScript Handbook — the illuminated guide",
            "TypeScript Deep Dive — the scholar's companion",
            " Definitely Typed — community scripture",
        ],
        "literary_tone": "structural, disciplined, contractual, practical",
        "codex_color": "📘",
    },

    "JavaScript": {
        "literary_theme": "The Nomad's Oral Tradition — Adaptability, First-Class Functions, and the Event Loop",
        "codex_age": "Born 1995 (Brendan Eich at Netscape, created in 10 days)",
        "origin_story": (
            "Brendan Eich at Netscape created JavaScript in 10 days in May 1995, "
            "initially named Mocha, then LiveScript, then JavaScript (a marketing decision). "
            "It is the codex of the nomadic trader — adaptable, creative, "
            "first-class functions as the universal currency."
        ),
        "epigraph": (
            "\"JavaScript is the only language that is both dangerously dynamic "
            "and universally ubiquitous.\" — Brendan Eich"
        ),
        "ancient_proverb": (
            "The function is first-class; "
            "it may travel, be stored, and be called upon at any moment."
        ),
        "designers_maxim": (
            "\"I wrote JavaScript in 10 days. If I had to do it again, "
            "I would change a few things — but not the first-class functions.\" "
            "— Brendan Eich"
        ),
        "famous_saying": (
            "In JavaScript, NaN === NaN is false — the only reflexive inequality in existence. "
            "Yet typeof null is 'object'. These are not bugs; they are history."
        ),
        "hidden_easter_egg": (
            "The JavaScript console command 'typeof (function(){})()' returns 'undefined' "
            "because the IIFE returns undefined. But 'typeof /regex/' returns 'object' — "
            "regex literals are objects in JavaScript. And in Chrome DevTools, "
            "typing '[] + []' gives '' (empty string), but '{} + []' gives '[object Object]'. "
            "These quirks are documented in the 'wat' talk — a living comedy tradition."
        ),
        "philosophical_haiku": (
            "First-class functions\nStored, passed, returned, and called\nPrototypes inherit"
        ),
        "signature_works": [
            "JavaScript: The Good Parts (Douglas Crockford) — the essential scripture",
            "You Don't Know JS (Kyle Simpson) — the deep texts",
            "MDN Web Docs — the living encyclopedia",
        ],
        "literary_tone": "nomadic, creative, paradoxical, universal",
        "codex_color": "💛",
    },

    "Java": {
        "literary_theme": "The Enterprise Annals — Institutional Memory, Durability, and the JVM Campus",
        "codex_age": "Born 1995 (James Gosling at Sun Microsystems)",
        "origin_story": (
            "James Gosling at Sun Microsystems created Java, originally called 'Oak'. "
            "The famous 'Duke' mascot was a hand gesture — waving. "
            "It is the codex of the institutional scholar — patient, durable, "
            "building monuments that outlive their architects."
        ),
        "epigraph": (
            "\"Java is not about coffee — it is about portability. "
            "Write once, run everywhere is not a slogan. It is a promise.\" — James Gosling"
        ),
        "ancient_proverb": (
            "The checked exception is a contract; "
            "ignoring it is a breach of the campus law."
        ),
        "designers_maxim": (
            "\"The checked exception mechanism in Java was my biggest mistake. "
            "Programmers catch too much, and the error handling becomes noise.\" "
            "— James Gosling"
        ),
        "famous_saying": (
            "In Java, a class without a package is homeless; "
            "in JavaScript, a function without a scope is also homeless."
        ),
        "hidden_easter_egg": (
            "In Java, the 'java' command has a hidden '-Xshare:off' option that disables "
            "class data sharing (CDS) — the internal archive that makes JVM startup fast. "
            "But more curious: Java has a 'clock' method in the standard library that "
            "was added for benchmarking and is accurate to nanoseconds, yet calling it "
            "in a loop can trigger JVM JIT recompilation that changes its own behavior — "
            "a self-modifying benchmark. Gosling called it 'a feature, not a bug'."
        ),
        "philosophical_haiku": (
            "Inheritance trees\nNoble classes pass their form\nEncapsulated truth"
        ),
        "signature_works": [
            "Effective Java (Joshua Bloch) — the enterprise bible",
            "Java Concurrency in Practice (Brian Goetz) — the concurrency scripture",
            "The Java Language Specification — the absolute law",
        ],
        "literary_tone": "institutional, durable, hierarchical, ceremonial",
        "codex_color": "☕",
    },

    "C/C++": {
        "literary_theme": "The Iron Epic — Raw Power, Ancient Wisdom, and the Manual of Control",
        "codex_age": "Born 1972 (Dennis Ritchie at Bell Labs, C); C++ born 1983 (Bjarne Stroustrup)",
        "origin_story": (
            "Dennis Ritchie at Bell Labs created C to write the Unix operating system. "
            "Bjarne Stroustrup at Bell Labs created 'C with Classes' in 1983, later renamed C++. "
            "It is the codex of the ironworker — powerful, unforgiving, "
            "building the infrastructure that holds the world together."
        ),
        "epigraph": (
            "\"C++ is a language for building abstractions that cost nothing. "
            "But if you make a mistake, you pay in segmentation faults.\" "
            "— Bjarne Stroustrup"
        ),
        "ancient_proverb": (
            "A pointer is not a promise; "
            "it may dangle, and the wise programmer checks before dereferencing."
        ),
        "designers_maxim": (
            "\"Within C++, there is a much smaller and cleaner language "
            "trying to get out.\" — Bjarne Stroustrup"
        ),
        "famous_saying": (
            "In C, you are responsible for everything. "
            "In Java, the JVM is responsible. In Rust, the borrow checker is responsible. "
            "In C++, you choose who is responsible."
        ),
        "hidden_easter_egg": (
            "The C preprocessor has a 'pragma' directive that was designed for compiler "
            "directives, but it can also be used for 'pragma once' — a non-standard "
            "but universally supported include guard. And in C++ compilers, "
            "compiling with '-std=c++17' enables the 'inline variables' feature — "
            "variables that can be defined in headers and instantiated once per translation unit. "
            "Bjarne called this 'the feature that took 30 years to standardize'."
        ),
        "philosophical_haiku": (
            "Pointers to memory\nManual allocation\nReturn the resource"
        ),
        "signature_works": [
            "The C Programming Language (Kernighan & Ritchie) — the original scripture",
            "The C++ Programming Language (Bjarne Stroustrup) — the modern epic",
            "ISO C++ Standard — the absolute law",
        ],
        "literary_tone": "powerful, raw, ancient, unforgiving",
        "codex_color": "⚙️",
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


def get_codex_data(language: str) -> Optional[Dict[str, Any]]:
    """Return the codex data for a given language, or None."""
    return CODEX_DB.get(language)


def generate_codex_report(
    rotate: bool = True,
    config_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a literary codex report for the current rotation language.

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
            "literary_theme": str,
            "codex_age": str,
            "origin_story": str,
            "epigraph": str,
            "ancient_proverb": str,
            "designers_maxim": str,
            "famous_saying": str,
            "hidden_easter_egg": str,
            "philosophical_haiku": str,
            "signature_works": List[str],
            "literary_tone": str,
            "codex_color": str,
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

    codex = CODEX_DB.get(current_language, {})

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": current_language,
        "current_index": old_idx,
        "new_index": new_idx if rotate else None,
        "rotated": rotate,
        "literary_theme": codex.get("literary_theme", "Unknown Theme"),
        "codex_age": codex.get("codex_age", "Unknown age"),
        "origin_story": codex.get("origin_story", "Unknown origin"),
        "epigraph": codex.get("epigraph", ""),
        "ancient_proverb": codex.get("ancient_proverb", ""),
        "designers_maxim": codex.get("designers_maxim", ""),
        "famous_saying": codex.get("famous_saying", ""),
        "hidden_easter_egg": codex.get("hidden_easter_egg", ""),
        "philosophical_haiku": codex.get("philosophical_haiku", ""),
        "signature_works": codex.get("signature_works", []),
        "literary_tone": codex.get("literary_tone", "Unknown"),
        "codex_color": codex.get("codex_color", "📜"),
        "rotation_order": ROTATION_ORDER,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def format_codex_report(m: Dict[str, Any]) -> str:
    """Format the codex report as a readable literary card."""

    works_lines = [f"  📚 {w}" for w in m["signature_works"]] if m["signature_works"] else ["  (no signature works recorded)"]

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  📜  POLYGLOT CODEX — Literary Traditions of Programming         ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Codex for       : {m['literary_theme']:<43}║",
        f"║  Language        : {m['language']:<43}║",
        f"║  Index           : {m['current_index']:<43}║",
        f"║  Rotated         : {str(m['rotated']):<43}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  📖  CODEX AGE & ORIGIN                                         ║",
        f"║  {m['codex_age']:<58}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  📜  ORIGIN STORY                                               ║",
    ]

    # Word-wrap the origin story
    origin_lines = _wrap_text(m["origin_story"], 56)
    for ol in origin_lines:
        lines.append(f"║  {ol:<57}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  ✒️  EPIGRAPH (Opening Inscription)                             ║",
    ]

    epigraph_lines = _wrap_text(m["epigraph"], 56)
    for el in epigraph_lines:
        lines.append(f"║  {el:<57}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🕯️  ANCIENT PROVERB                                            ║",
    ]

    proverb_lines = _wrap_text(m["ancient_proverb"], 56)
    for pl in proverb_lines:
        lines.append(f"║  {pl:<57}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  ⚡  DESIGNER'S MAXIM                                           ║",
    ]

    maxim_lines = _wrap_text(m["designers_maxim"], 56)
    for ml in maxim_lines:
        lines.append(f"║  {ml:<57}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🔮  FAMOUS SAYING                                              ║",
    ]

    saying_lines = _wrap_text(m["famous_saying"], 56)
    for sl in saying_lines:
        lines.append(f"║  {sl:<57}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🥚  HIDDEN EASTER EGG                                          ║",
    ]

    egg_lines = _wrap_text(m["hidden_easter_egg"], 56)
    for el in egg_lines:
        lines.append(f"║  {el:<57}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🎋  PHILOSOPHICAL HAIKU (5-7-5)                               ║",
    ]

    haiku_lines = _wrap_text(m["philosophical_haiku"], 56)
    for hl in haiku_lines:
        lines.append(f"║  {hl:<57}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  📚  SIGNATURE WORKS                                             ║",
    ]
    for wl in works_lines:
        lines.append(f"║{wl:<59}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🎭  LITERARY TONE                                              ║",
        f"║  {m['literary_tone']:<58}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🔄  ROTATION ORDER                                             ║",
        f"║  {' → '.join(ROTATION_ORDER):<58}║",
        "╚══════════════════════════════════════════════════════════════════╝",
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
        report = generate_codex_report()
        print(format_codex_report(report))
    else:
        print(f"Polyglot Codex v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_codex --test   # Run tests")
        print("  python -m polyglot_codex --report # Generate codex report")
