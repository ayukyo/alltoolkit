#!/usr/bin/env python3
"""
🌟 Language Sage v1.0
An AI mentor that dispenses wisdom, idioms, and pro tips for the selected language.
Creative language-learning companion that rotates through languages and delivers
personalized insights, idioms, common pitfalls, and mentorship quotes.
"""

import json
import random
import os
from datetime import datetime

TOOL_NAME = "language-sage"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "language_rotation.json")


def load_rotation():
    """Load language rotation config."""
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data):
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


# Language-specific wisdom databases
LANGUAGE_DATA = {
    "Rust": {
        "idioms": [
            "Borrow checker says NO — and it's right.",
            "If it doesn't compile, you didn't deserve it.",
            "Ownership isn't hoarding; it's stewardship.",
            "Match your way to correctness.",
            "Lifetime annotations: the compiler's love letters.",
        ],
        "pitfalls": [
            "Don't fight the borrow checker — listen to it.",
            "Arc<Mutex<T>> isn't a silver bullet for shared state.",
            "Unwrap in production is a meditation on risk.",
            "Trait objects need 'dyn' — don't forget the dance.",
        ],
        "pro_tips": [
            "Run `cargo build` daily — small compiles are happy compiles.",
            "Use `cargo clippy --fix` for auto-fixable warnings.",
            "Document with `///` for doc comments — they're searchable.",
            "Start with `rustlings` exercises to build muscle memory.",
        ],
        "mentor_quote": "\"The Rust compiler is your strict but brilliant professor who never gives up on you.\"",
        "resource": "The Rust Programming Language (rust-book.toml)",
    },
    "Go": {
        "idioms": [
            "Don't communicate by sharing memory; share memory by communicating.",
            "If a function returns an error, handle it or propagate it — never ignore it.",
            "Make the zero value useful.",
            "Gofmt your code — arguments end where style begins.",
            "Interfaces are implicit; implement by existing.",
        ],
        "pitfalls": [
            "Goroutines leak if you never close channels they send to.",
            "Slices are references — modifying them can affect 'copies'.",
            "defer runs LIFO but evaluate immediately at call time.",
            "nil slices serialize to 'null' in JSON — use empty slices instead.",
        ],
        "pro_tips": [
            "Use `go vet` before committing — it catches real bugs.",
            "Context should flow through your call stack like water.",
            "Keep interfaces small; io.Reader/Writer is the gold standard.",
            "Profile with `pprof` — optimization without data is guessing.",
        ],
        "mentor_quote": "\"Simplicity is hard to build and easy to understand; complexity is easy to build and hard to understand.\"",
        "resource": "Effective Go (golang.org/doc/effective_go)",
    },
    "Swift": {
        "idioms": [
            "Let the type system work — don't fight inference.",
            "Optionals are not nullable pointers; they're the absence or presence of a value.",
            "Protocols over inheritance; composition over class hierarchies.",
            "If it's worth doing in a loop, it's worth doing with map/filter/reduce.",
            "guard else is your friend for early exits.",
        ],
        "pitfalls": [
            "Structs are value types — mutating requires 'var', not 'let'.",
            "Avoid retain cycles: weak and unowned are your lifelines.",
            "DispatchQueue.main.async from main thread causes deadlocks.",
            "JSON decoder fails silently on type mismatches — validate first.",
        ],
        "pro_tips": [
            "Use `@escaping` explicitly — Swift won't guess for you.",
            "Build protocols first, then implement.",
            "swiftlint and swiftformat keep your codebase sane.",
            "XCTest for everything — TDD is your safety net.",
        ],
        "mentor_quote": "\"Swift is what Objective-C wanted to be: safe, modern, and expressive.\"",
        "resource": "The Swift Programming Language (swift.org/documentation)",
    },
    "Kotlin": {
        "idioms": [
            "Null safety isn't a burden; it's a gift that prevents NullPointerException.",
            "Data classes auto-generate equals, hashCode, toString, copy.",
            "Extension functions let you add methods to closed classes.",
            "Coroutines turn async code into sequential code.",
            "When expression replaces switch — and it's better in every way.",
        ],
        "pitfalls": [
            "Lateinit vars can be uninitialized — check with isInitialized.",
            "Sequence vs List: sequences are lazy, Lists are eager.",
            "Companion object fields aren't truly static — use @JvmStatic.",
            "Scoped functions (let/also/apply/run) can obscure logs.",
        ],
        "pro_tips": [
            "Use `sealed classes` for exhaustive when expressions.",
            "Dependency injection with Koin or Hilt keeps code testable.",
            "Flow for reactive streams; Channel for one-shot events.",
            "Kotlin Multiplatform shares code across JVM/JS/Native.",
        ],
        "mentor_quote": "\"Kotlin doesn't just interoperate with Java — it improves on it.\"",
        "resource": "Kotlinlang.org documentation",
    },
    "TypeScript": {
        "idioms": [
            "TypeScript is JavaScript with a college education.",
            "The 'unknown' type is 'any' with a conscience.",
            "Discriminated unions model state like a boss.",
            "Generic constraints are the grammar of reusable types.",
            "Utility types (Partial, Pick, Omit) are free power-ups.",
        ],
        "pitfalls": [
            "'as' casts are escape hatches — use sparingly.",
            "Structural typing means extra fields are silently tolerated.",
            "Type inference breaks down with complex nested generics.",
            "tsconfig 'strict' flag catches real bugs — always enable it.",
        ],
        "pro_tips": [
            "Use Zod or Yup for runtime type validation.",
            "Template literal types unlock string manipulation at the type level.",
            "never type is great for exhaustive checks in switch statements.",
            "Prefer interfaces for object shapes, types for unions/primitives.",
        ],
        "mentor_quote": "\"TypeScript's type system is Turing complete — use that power wisely.\"",
        "resource": "TypeScript Handbook (typescriptlang.org/docs)",
    },
    "JavaScript": {
        "idioms": [
            "Async/await is promises with a nicer face.",
            "Destructuring with defaults handles missing properties gracefully.",
            "Array methods (map, filter, reduce) replace most loops.",
            "Event loop: don't block the main thread.",
            "null == undefined but null !== undefined — know the difference.",
        ],
        "pitfalls": [
            "== coerces types; === compares without coercion — always ===.",
            "Closures capture references, not values — loop beware.",
            "Mutation of objects you don't own causes bugs and broken hearts.",
            "NaN is a number and !== NaN — use Number.isNaN instead.",
        ],
        "pro_tips": [
            "ES modules (import/export) replace require/module.exports.",
            "Optional chaining (?.) replaces deep null checks.",
            "Nullish coalescing (??) distinguishes false from undefined.",
            "Use a linter (ESLint) and formatter (Prettier) — always.",
        ],
        "mentor_quote": "\"JavaScript is the language that runs the world's most dynamic applications.\"",
        "resource": "MDN Web Docs (developer.mozilla.org)",
    },
    "Java": {
        "idioms": [
            "Favor composition over inheritance.",
            "Immutability is a feature, not a limitation.",
            "Streams are lazy — nothing runs until a terminal operation triggers.",
            "A lambda is an anonymous function; a method reference is a name tag.",
            "Optional is a box — don't unwrap it unless you must.",
        ],
        "pitfalls": [
            "String literal pool doesn't include new String() objects.",
            "ConcurrentHashMap is not a drop-in replacement for HashMap.",
            "Date/Time API (java.time) replaces the broken legacy Date.",
            "Autoboxing hides performance costs in tight loops.",
        ],
        "pro_tips": [
            "Use JShell to experiment with Java snippets instantly.",
            "Records (Java 16+) eliminate boilerplate for data carriers.",
            "Virtual threads (Java 21+) make concurrency cheap.",
            "Reactive streams (Flow API) handle backpressure elegantly.",
        ],
        "mentor_quote": "\"Write once, run anywhere — Java's promise that shaped an ecosystem.\"",
        "resource": "Oracle Java Tutorials (docs.oracle.com/javase/tutorial)",
    },
    "C/C++": {
        "idioms": [
            "C: you are your own memory manager — own it.",
            "C++: RAII ties resource lifetime to object lifetime.",
            "Prefer constexpr for compile-time computation.",
            "Move semantics eliminate unnecessary copies.",
            "Templates are compile-time polymorphism.",
        ],
        "pitfalls": [
            "Buffer overflows are the root of most security exploits.",
            "Double-free and use-after-free are the twin terrors.",
            "Uninitialized variables: the gift that keeps on giving bugs.",
            "Casting away const invites undefined behavior.",
        ],
        "pro_tips": [
            "C++20 modules replace header files — embrace the future.",
            "Use smart pointers (unique_ptr, shared_ptr) — never raw new/delete.",
            "Static analysis (clang-tidy) catches bugs before they bite.",
            "Sanitizers (ASAN, MSAN) find memory bugs in seconds.",
        ],
        "mentor_quote": "\"C gives you enough rope to hang yourself; C++ gives you enough rope to build a suspension bridge.\"",
        "resource": "cppreference.com and isocpp.org",
    },
}


WISDOM_TEMPLATES = [
    "The wise developer knows that {language} rewards patience and practice.",
    "Remember: every {language} expert was once a beginner who refused to give up.",
    "In {language}, the path to mastery is paved with compiler errors — each one a lesson.",
    "Today's bug is tomorrow's deep understanding. Debug with curiosity, not frustration.",
    "The best code is written when you understand the language's philosophy, not just its syntax.",
]

SEASONAL_VIBES = {
    "morning": "Rise and code! ☀️",
    "afternoon": "Keep the momentum going! ⚡",
    "evening": "Wind down with some clean code. 🌙",
    "night": "The quiet hours are for deep focus. 🌌",
}


def get_time_vibe():
    """Get greeting based on time of day."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return SEASONAL_VIBES["morning"]
    elif 12 <= hour < 18:
        return SEASONAL_VIBES["afternoon"]
    elif 18 <= hour < 22:
        return SEASONAL_VIBES["evening"]
    else:
        return SEASONAL_VIBES["night"]


def select_wisdom(language):
    """Select a random wisdom template and fill it."""
    template = random.choice(WISDOM_TEMPLATES)
    return template.format(language=language)


def dispense(language):
    """
    Main dispense function — deliver sage wisdom for the selected language.
    This is the core of Language Sage: it loads the rotation config,
    validates the language, serves wisdom, and advances the rotation.
    """
    config = load_rotation()

    if language not in config["languages"]:
        raise ValueError(
            f"Language '{language}' not in rotation. "
            f"Available: {', '.join(config['languages'])}"
        )

    # Get language-specific data
    lang_data = LANGUAGE_DATA.get(language, {})

    # Build the wisdom response
    idiom = random.choice(lang_data.get("idioms", ["No idiom available."]))
    pitfall = random.choice(lang_data.get("pitfalls", ["No pitfalls listed."]))
    pro_tip = random.choice(lang_data.get("pro_tips", ["No tips available."]))
    wisdom = select_wisdom(language)

    # Prepare response
    current_idx = config["languages"].index(language)
    next_idx = (current_idx + 1) % len(config["languages"])

    # Update rotation: advance to next language
    config["current_index"] = next_idx
    config["last_language"] = language
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "mentor_quote": lang_data.get("mentor_quote", ""),
        "idiom_of_the_session": idiom,
        "pitfall_to_avoid": pitfall,
        "pro_tip_of_the_day": pro_tip,
        "wisdom": wisdom,
        "resource": lang_data.get("resource", ""),
        "time_vibe": get_time_vibe(),
        "next_language": config["languages"][next_idx],
        "rotation": config["languages"],
        "timestamp": datetime.now().isoformat(),
    }


def run_tests():
    """Run tests to validate the tool."""
    tests_passed = 0
    tests_failed = 0

    def assert_eq(a, b, msg=""):
        nonlocal tests_passed, tests_failed
        if a == b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — expected {b!r}, got {a!r}")

    print("Testing Language Sage...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_eq(0, config["current_index"], "Index starts at 0 (Rust)")

    print("  Testing dispense for Rust...")
    result = dispense("Rust")
    expected_keys = [
        "tool", "version", "selected_language", "mentor_quote",
        "idiom_of_the_session", "pitfall_to_avoid", "pro_tip_of_the_day",
        "wisdom", "resource", "time_vibe", "next_language", "rotation", "timestamp"
    ]
    for key in expected_keys:
        assert_eq(True, key in result, f"Key '{key}' present in response")

    assert_eq("Rust", result["selected_language"], "Rust is selected")
    assert_eq("Go", result["next_language"], "Next language is Go")
    assert_eq("language-sage", result["tool"], "Correct tool name")

    print("  Verifying rotation update...")
    config2 = load_rotation()
    assert_eq(1, config2["current_index"], "Index advanced to 1 (Go)")
    assert_eq("Rust", config2["last_language"], "Last language recorded as Rust")

    print("  Testing dispense for Go (next in rotation)...")
    result2 = dispense("Go")
    assert_eq("Go", result2["selected_language"], "Go is selected")
    assert_eq("Swift", result2["next_language"], "Next language is Swift")

    print("  Testing invalid language handling...")
    try:
        dispense("Python")
        tests_failed += 1
        print("  ❌ FAIL: No error raised for invalid language")
    except ValueError as e:
        tests_passed += 1
        print(f"  ✅ PASS: ValueError raised for invalid language")
        assert_eq(True, "not in rotation" in str(e), "Error mentions rotation")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ FAIL: Wrong exception: {e}")

    print("  Testing all languages are covered...")
    for lang in config["languages"]:
        data = LANGUAGE_DATA.get(lang)
        assert_eq(True, data is not None, f"Data exists for {lang}")
        assert_eq(True, len(data.get("idioms", [])) >= 3, f"{lang} has idioms")
        assert_eq(True, len(data.get("pitfalls", [])) >= 3, f"{lang} has pitfalls")
        assert_eq(True, len(data.get("pro_tips", [])) >= 3, f"{lang} has pro tips")

    print(f"\n{'='*50}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("🎉 All tests passed! The Sage is wise.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)
