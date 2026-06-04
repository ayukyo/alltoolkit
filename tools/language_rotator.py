#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Language Rotator — Creative Tool Module
Rotates through: Rust -> Go -> Swift -> Kotlin -> TypeScript -> JavaScript -> Java -> C/C++ -> Rust (cycle)

Each rotation generates a "Language Challenge Card" — a creative daily coding challenge
uniquely tailored to the target language's paradigm, syntax personality, and ecosystem.

This tool is distinct from:
  - language_codex:       hidden syntax quirks / Easter eggs
  - language_archaeology:  historical/linguistic roots
  - language_compass:       learning journey maps
  - language_sage:          idioms, pro tips, pitfalls
  - language_mastery:       XP / level progress

This module focuses on: ROTATION LOGIC + CREATIVE DAILY CHALLENGE GENERATION.
"""

from __future__ import print_function

import json
import os
import random as random_module
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── Constants ───────────────────────────────────────────────────────────────────
TOOL_NAME = "language-rotator"
TOOL_VERSION = "1.1.0"

# Rotation order (deterministic sequence — not random)
LANGUAGES = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]

# Canonical path to the shared rotation config at workspace root
ROTATION_FILE = Path.home() / ".openclaw" / "workspace" / "language_rotation.json"

# ── Challenge Template Database ──────────────────────────────────────────────
# Each language has 4 unique challenge categories that rotate daily.
# These are generative — values are combined dynamically per challenge.

_CHALLENGE_TEMPLATES = {
    "Rust": [
        {
            "category": "Ownership Lab",
            "emoji": "\U0001f980",
            "hook": "Prove that the borrow checker is smarter than you think.",
            "task": "Write a function that demonstrates a *complex ownership transfer* "
                   "— something that trips up most Rust newcomers.",
            "constraints": ["No Arc<Mutex>", "Must not compile with `unsafe`"],
            "paradigm_focus": "Ownership & Borrowing",
        },
        {
            "category": "Trait Force",
            "emoji": "\U0001f980",
            "hook": "Traits are Rust's answer to interfaces — but with superpowers.",
            "task": "Implement a composite trait that combines Iterator + IntoIterator "
                   "with a custom type, then use it in a generic function.",
            "constraints": ["Must use at least 2 trait bounds with `+`", "No `where` clause"],
            "paradigm_focus": "Trait Bounds & Generics",
        },
        {
            "category": "Concurrency Quest",
            "emoji": "\U0001f980",
            "hook": "Fearless concurrency — but are YOU fearless enough?",
            "task": "Build a thread-safe producer-consumer channel from scratch using only "
                   "std::thread and std::sync::mpsc.",
            "constraints": ["No external crates", "Maximum 3 channels", "No Mutex"],
            "paradigm_focus": "Fearless Concurrency",
        },
        {
            "category": "Result Revenge",
            "emoji": "\U0001f980",
            "hook": "unwrap() in production is a meditation on risk. Don't do it.",
            "task": "Write a small parser that returns Result<T, E> for all error paths, "
                   "then chain it with the `?` operator.",
            "constraints": ["Every error variant must be typed", "No expect() or unwrap()"],
            "paradigm_focus": "Error Handling",
        },
    ],
    "Go": [
        {
            "category": "Goroutine Garden",
            "emoji": "\U0001f43b",
            "hook": "Concurrency is cheap, but not free. Use it wisely.",
            "task": "Build a fan-out / fan-in pattern: spawn N goroutines that each do "
                   "a computation, collect results via a shared channel.",
            "constraints": ["Use sync.WaitGroup", "No mutex for result collection"],
            "paradigm_focus": "Goroutines & Channels",
        },
        {
            "category": "Interface Ink",
            "emoji": "\U0001f43b",
            "hook": "In Go, interfaces are implicit — no declaration, no ceremony.",
            "task": "Design a small plugin system using io.Reader/io.Writer as the "
                   "core interfaces. Implement for a custom type.",
            "constraints": ["Define at least 1 custom interface", "Use embedding"],
            "paradigm_focus": "Interfaces & Composition",
        },
        {
            "category": "Context Crucible",
            "emoji": "\U0001f43b",
            "hook": "Context should flow through your program like water.",
            "task": "Write a tree of functions where cancellation propagates correctly "
                   "from a root context, and each leaf prints its depth on cancellation.",
            "constraints": ["Must handle DeadlineExceeded", "No global state"],
            "paradigm_focus": "Context & Cancellation",
        },
        {
            "category": "Defer Dilemma",
            "emoji": "\U0001f43b",
            "hook": "defer runs LIFO — but arguments are evaluated immediately.",
            "task": "Create a scenario where understanding defer's argument-evaluation "
                   "timing causes a subtle bug, then fix it.",
            "constraints": ["Must involve a loop", "Print execution trace to prove understanding"],
            "paradigm_focus": "Defer, Panic, Recover",
        },
    ],
    "Swift": [
        {
            "category": "Optional Odyssey",
            "emoji": "\U0001f985",
            "hook": "nil is not absence — it's a first-class concept.",
            "task": "Chain at least 4 optional values using `if let` and `guard let`, "
                   "then refactor the same logic using optional map/flatMap.",
            "constraints": ["Both versions must exist in the same file", "No `!` force-unwrap"],
            "paradigm_focus": "Optionals & Pattern Matching",
        },
        {
            "category": "Protocol Playground",
            "emoji": "\U0001f985",
            "hook": "Protocols over inheritance. Always.",
            "task": "Design a protocol hierarchy (at least 3 protocols, 1 with inheritance) "
                   "for a Shape system, then implement for enums with associated values.",
            "constraints": ["At least one protocol has a static method", "Use extension for default impl"],
            "paradigm_focus": "Protocol-Oriented Programming",
        },
        {
            "category": "Generics Gateway",
            "emoji": "\U0001f985",
            "hook": "Generics in Swift are more powerful than they look.",
            "task": "Write a generic function that uses `where` clauses to constrain a "
                   "type to be both Hashable and Comparable, then call it with 2 different types.",
            "constraints": ["At least one custom type in a generic call", "No type erasure"],
            "paradigm_focus": "Generics & Type Constraints",
        },
        {
            "category": "Actor Adventure",
            "emoji": "\U0001f985",
            "hook": "Swift concurrency: actors protect their state.",
            "task": "Implement a simple bank account actor with deposit/withdraw/transfer "
                   "methods, demonstrating isolation guarantee.",
            "constraints": ["Must use `actor` keyword", "No `@MainActor`", "Transfer must be atomic"],
            "paradigm_focus": "Swift Concurrency (Actors)",
        },
    ],
    "Kotlin": [
        {
            "category": "Coroutine Canyon",
            "emoji": "\U0001f9c3",
            "hook": "Lightweight concurrency that reads like synchronous code.",
            "task": "Write a multi-step async pipeline using suspend functions: fetch -> "
                   "transform -> save, with proper error handling at each stage.",
            "constraints": ["Use withContext for thread switching", "No blocking in coroutine"],
            "paradigm_focus": "Coroutines & Structured Concurrency",
        },
        {
            "category": "Extension Expedition",
            "emoji": "\U0001f9c3",
            "hook": "Extend any class without touching its source.",
            "task": "Create 3+ extension functions on String that form a DSL for "
                   "validating and transforming user input.",
            "constraints": ["At least 1 must use inline + reified", "Chain 2+ extensions together"],
            "paradigm_focus": "Extension Functions & DSL",
        },
        {
            "category": "Sealed Quest",
            "emoji": "\U0001f9c3",
            "hook": "Sealed classes: exhaustiveness made enforceable.",
            "task": "Model a state machine for a game using sealed classes and an "
                   "exhaustive `when` expression, then show what breaks if you add a new state.",
            "constraints": ["Must show compiler exhaustiveness check", "At least 4 states"],
            "paradigm_focus": "Sealed Classes & Algebraic Types",
        },
        {
            "category": "Sequence Sprint",
            "emoji": "\U0001f9c3",
            "hook": "Sequences are lazy. Know when to use them over lists.",
            "task": "Build a pipeline that processes 1,000,000 elements using Sequence "
                   "operators (not List), demonstrating lazy evaluation.",
            "constraints": ["No intermediate collections", "Time both Sequence and List paths"],
            "paradigm_focus": "Lazy Sequences & Streams",
        },
    ],
    "TypeScript": [
        {
            "category": "Type Tetris",
            "emoji": "\U0001f4d8",
            "hook": "TypeScript's type system is a Turing-complete puzzle.",
            "task": "Write a recursive conditional type that flattens a nested array type "
                   "of arbitrary depth to a flat tuple — then test it.",
            "constraints": ["Must handle depth 0, 1, 2, 3+", "No `any` in the type itself"],
            "paradigm_focus": "Conditional Types & Mapped Types",
        },
        {
            "category": "Infer Investigation",
            "emoji": "\U0001f4d8",
            "hook": "infer is TypeScript's type-level pattern matching.",
            "task": "Implement a `ReturnType<T>` utility from scratch using `infer`, "
                   "then use it in a wrapper function type declaration.",
            "constraints": ["Must work for sync and async functions", "No built-in utility"],
            "paradigm_focus": "infer Keyword & Type Inference",
        },
        {
            "category": "Decorator Dungeon",
            "emoji": "\U0001f4d8",
            "hook": "Decorators reveal metadata about your code at runtime.",
            "task": "Create a class decorator that measures method execution time "
                   "and a parameter decorator that logs argument shapes.",
            "constraints": ["Must support both class and method decorators", "No external deps"],
            "paradigm_focus": "Decorators & Metadata Reflection",
        },
        {
            "category": "Narrowing Lab",
            "emoji": "\U0001f4d8",
            "hook": "Type narrowing makes your code safer, one branch at a time.",
            "task": "Write a discriminated union type for an API response with loading/success/error "
                   "states, then demonstrate all narrowing paths.",
            "constraints": ["Use `in` operator narrowing", "Exhaustive switch must compile"],
            "paradigm_focus": "Type Narrowing & Discriminated Unions",
        },
    ],
    "JavaScript": [
        {
            "category": "Proxy Paradox",
            "emoji": "\U0001f31f",
            "hook": "Meta-programming without touching the original object.",
            "task": "Build a reactive state object using Proxy that intercepts reads/writes "
                   "and notifies subscribers, with no Proxy polyfill.",
            "constraints": ["Must trap get, set, and deleteProperty", "No Object.defineProperty"],
            "paradigm_focus": "Proxy & Metaprogramming",
        },
        {
            "category": "Async Abyss",
            "emoji": "\U0001f31f",
            "hook": "Promises are not optional in modern JS — they're inevitable.",
            "task": "Implement a Promise.allSettled equivalent from scratch (no built-in), "
                   "then use it to handle mixed success/failure API calls.",
            "constraints": ["Cannot use Promise.allSettled", "Must handle rejection"],
            "paradigm_focus": "Promises & Async/Await",
        },
        {
            "category": "Closure Cavern",
            "emoji": "\U0001f31f",
            "hook": "Closures remember what the world looked like when they were born.",
            "task": "Create a memoize decorator that closes over a cache, demonstrating "
                   "closure with multiple execution contexts.",
            "constraints": ["Must work with functions of any arity", "Must clear cache on demand"],
            "paradigm_focus": "Closures & Higher-Order Functions",
        },
        {
            "category": "Prototype Puzzle",
            "emoji": "\U0001f31f",
            "hook": "Classical inheritance is dead. Long live prototypal inheritance.",
            "task": "Build a mini OOP hierarchy using Object.create() and "
                   "Reflect.construct — no class keyword, no new.",
            "constraints": ["Must demonstrate prototype chain traversal", "At least 3 levels"],
            "paradigm_focus": "Prototypes & Object Composition",
        },
    ],
    "Java": [
        {
            "category": "Generic Gauntlet",
            "emoji": "\u2615",
            "hook": "Type erasure is Java's dirty little secret.",
            "task": "Write a generic class that demonstrates type erasure effects, then "
                   "use Class<T> to recover type information at runtime.",
            "constraints": ["Must show raw type vs generic at runtime", "Use TypeToken pattern"],
            "paradigm_focus": "Generics & Type Erasure",
        },
        {
            "category": "Stream Saga",
            "emoji": "\u2615",
            "hook": "Streams aren't loops — they're data pipeline descriptions.",
            "task": "Build a stream pipeline that processes a list of transactions: filter "
                   "by date, group by category, sum amounts, and sort descending.",
            "constraints": ["Must use collect() with a custom Collector", "No mutating the input list"],
            "paradigm_focus": "Streams & Lambda Expressions",
        },
        {
            "category": "Pattern Saga",
            "emoji": "\u2615",
            "hook": "Pattern matching in Java — finally, after 25 years.",
            "task": "Use sealed interfaces + pattern matching (Java 21+) to model a "
                   "type hierarchy and show exhaustive switch compilation.",
            "constraints": ["Requires Java 21+ features", "Must show compiler exhaustiveness"],
            "paradigm_focus": "Pattern Matching for Switch",
        },
        {
            "category": "Concurrency Cave",
            "emoji": "\u2615",
            "hook": "Virtual threads: the biggest JVM change in a decade.",
            "task": "Implement a simple thread-per-request web server using virtual threads "
                   "(Java 21+), compare with classic thread pool approach.",
            "constraints": ["Must use Executors.newVirtualThreadPerTaskExecutor()", "Benchmark both"],
            "paradigm_focus": "Virtual Threads (Project Loom)",
        },
    ],
    "C/C++": [
        {
            "category": "Template Tomfoolery",
            "emoji": "\u2699",
            "hook": "C++ templates: compile-time computation with no runtime cost.",
            "task": "Write a template metaprogram that computes the Nth Fibonacci number "
                   "at compile time using template specialization.",
            "constraints": ["Must compute at compile time (static_assert)", "No recursion depth warnings"],
            "paradigm_focus": "Template Metaprogramming",
        },
        {
            "category": "Move Mastery",
            "emoji": "\u2699",
            "hook": "Move semantics: the most important C++11 feature you probably misuse.",
            "task": "Implement a class with a move constructor and move assignment operator "
                   "that correctly handles a dynamically allocated buffer.",
            "constraints": ["Rule of 5 must be satisfied", "No std::move in the class itself"],
            "paradigm_focus": "Move Semantics & Rvalue References",
        },
        {
            "category": "Memory Maze",
            "emoji": "\u2699",
            "hook": "Memory leaks are not bugs — they're design failures.",
            "task": "Use valgrind-observable patterns to demonstrate a memory leak, "
                   "then fix it using RAII (Resource Acquisition Is Initialization).",
            "constraints": ["Must run under valgrind", "Use unique_ptr for the fix"],
            "paradigm_focus": "RAII & Smart Pointers",
        },
        {
            "category": "Coroutine Canyon",
            "emoji": "\u2699",
            "hook": "C++20 coroutines: async/await for C++.",
            "task": "Write a minimal coroutine that suspends and resumes, tracking "
                   "the number of active coroutine frames.",
            "constraints": ["Must use co_await / co_return", "Track frame count without global state"],
            "paradigm_focus": "C++20 Coroutines",
        },
    ],
}

# Difficulty labels by modulo-4 index
_DIFFICULTY_LEVELS = ["\u2605\u2606\u2606\u2606\u2606", "\u2605\u2605\u2606\u2606\u2606",
                      "\u2605\u2605\u2605\u2606\u2606", "\u2605\u2605\u2605\u2605\u2606"]

_BONUS_MODIFIERS = [
    "Add a hidden time limit.",
    "Solve it in under 20 lines of code.",
    "Write it without any third-party imports.",
    "Make it single-file with zero dependencies.",
    "Use it to teach someone new to the language in 5 minutes.",
    "Make it work in a REPL or playground environment.",
]


# ── Rotation Logic ─────────────────────────────────────────────────────────────

def load_rotation():
    # type: () -> Dict[str, Any]
    """Load rotation config from the canonical workspace path."""
    if not ROTATION_FILE.exists():
        return {
            "languages": LANGUAGES,
            "current_index": 0,
            "last_language": None,
            "updated_at": None,
        }
    with open(ROTATION_FILE) as f:
        return json.load(f)


def save_rotation(config):
    # type: (Dict[str, Any]) -> None
    """Persist updated rotation config."""
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    with open(ROTATION_FILE, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_language_at_index(languages, index):
    # type: (List[str], int) -> str
    """Safely resolve language by index with wrap-around."""
    return languages[index % len(languages)]


def advance_rotation(config):
    # type: (Dict[str, Any]) -> Dict[str, Any]
    """Advance current_index to next position and update last_language."""
    languages = config.get("languages", LANGUAGES)
    current_idx = config.get("current_index", 0)
    selected = languages[current_idx % len(languages)]
    next_idx = (current_idx + 1) % len(languages)
    config["current_index"] = next_idx
    config["last_language"] = selected
    return config


# ── Challenge Card Generator ──────────────────────────────────────────────────

def generate_challenge_card(language, day_seed):
    # type: (str, int) -> Dict[str, Any]
    """Generate a unique daily challenge card for the given language."""
    templates = _CHALLENGE_TEMPLATES.get(language, _CHALLENGE_TEMPLATES["JavaScript"])
    challenge_index = day_seed % len(templates)
    challenge = templates[challenge_index]
    modifier = _BONUS_MODIFIERS[day_seed % len(_BONUS_MODIFIERS)]
    diff_index = day_seed % 4

    return {
        "language": language,
        "emoji": challenge["emoji"],
        "category": challenge["category"],
        "day_difficulty": _DIFFICULTY_LEVELS[diff_index],
        "hook": challenge["hook"],
        "task": challenge["task"],
        "constraints": challenge["constraints"],
        "paradigm_focus": challenge["paradigm_focus"],
        "bonus_modifier": modifier,
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def build_rotation_summary(config):
    # type: (Dict[str, Any]) -> Dict[str, Any]
    """Build a complete status summary of the current rotation state."""
    languages = config.get("languages", LANGUAGES)
    current_idx = config.get("current_index", 0)
    last = config.get("last_language")
    return {
        "rotation_order": languages,
        "current_index": current_idx,
        "current_language": languages[current_idx % len(languages)],
        "last_language": last,
        "cycle_position": "{}/{}".format(current_idx + 1, len(languages)),
        "cycle_progress_pct": round((float(current_idx) / len(languages)) * 100, 1),
        "is_wrapping": current_idx >= len(languages),
    }


# ── Main Entry Point ───────────────────────────────────────────────────────────

def rotate_and_build():
    # type: () -> Dict[str, Any]
    """
    Main entry: load config -> select current language -> generate challenge card
    -> advance rotation -> persist state -> return full result.
    """
    config = load_rotation()
    languages = config.get("languages", LANGUAGES)
    current_idx = config.get("current_index", 0)
    selected = languages[current_idx % len(languages)]

    # Deterministic day seed from today's date (same challenge all day)
    today = datetime.now(timezone(timedelta(hours=8))).date()
    day_seed = today.toordinal()  # ordinal integer = consistent per-day selection

    card = generate_challenge_card(selected, day_seed)
    config = advance_rotation(config)
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": selected,
        "challenge": card,
        "rotation_state": build_rotation_summary(config),
        "config_updated": True,
        "rotated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


# ── Public CLI Interface ────────────────────────────────────────────────────────

def main():
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--rotate":
        result = rotate_and_build()
        print("Language: {}".format(result["selected_language"]))
        print("Challenge: {} {}".format(result["challenge"]["category"],
                                       result["challenge"]["emoji"]))
        print("Hook: {}".format(result["challenge"]["hook"]))
        print("Task: {}".format(result["challenge"]["task"]))
        print("Constraints: {}".format(", ".join(result["challenge"]["constraints"])))
        print("Bonus: {}".format(result["challenge"]["bonus_modifier"]))
        print("Next: {}".format(result["rotation_state"]["current_language"]))
        print("Cycle: {} ({}%)".format(result["rotation_state"]["cycle_position"],
                                       result["rotation_state"]["cycle_progress_pct"]))
    elif len(sys.argv) > 1 and sys.argv[1] == "--status":
        config = load_rotation()
        summary = build_rotation_summary(config)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print("Language Rotator v{}".format(TOOL_VERSION))
        print("Usage:")
        print("  python language_rotator.py --rotate  # Rotate & generate challenge")
        print("  python language_rotator.py --status  # Show rotation state")


if __name__ == "__main__":
    main()