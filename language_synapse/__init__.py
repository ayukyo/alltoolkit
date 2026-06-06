#!/usr/bin/env python3
"""
🧠 Language Synapse v1.0
A creative tool that maps neural pathways between programming languages —
finding conceptual bridges, semantic overlaps, and surprising connections.

Creative concept: "Every language is a different way to think.
This tool maps the thoughts that connect them."

Every language solves similar problems (state, flow, abstraction, types).
This tool discovers HOW each language conceptualizes these problems differently
and finds the conceptual "synapses" — bridges between languages.

Distinct from existing tools:
  - language_archaeology: history and origins (temporal dimension)
  - language_compass: learning journey maps (progress dimension)
  - language_sage: idioms and best practices (usage dimension)
  - language_ecohub: package ecosystems (tooling dimension)

Synapse is about CONCEPTUAL CONNECTIONS — how thinking in one language
maps to thinking in another.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

TOOL_NAME = "language-synapse"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "language_rotation.json"
)


def load_rotation():
    """Load language rotation config."""
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data):
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Core concepts that all languages grapple with ──────────────────────────────
# Each concept has a "thought pattern" — how that language approaches the problem
CORE_CONCEPTS = {
    "state": {
        "description": "How does the language model and manage state?",
        "patterns": {
            "Rust": "Ownership + borrowing: state has a single owner; sharing requires Arc<Mutex<T>>. No shared mutation without explicit coordination.",
            "Go": "Shared memory via channels (CSP): 'Don't communicate by sharing memory; share memory by communicating.' Data races are prevented by design.",
            "Swift": "Value semantics by default (structs), reference semantics (classes) when needed. ARC for reference types, no shared mutable state by default.",
            "Kotlin": "Null safety built into the type system. Coroutines provide structured state concurrency. Data classes for immutable-by-default state.",
            "TypeScript": "Objects as dictionaries of properties. No null safety — but strict null checks available. State often external (Redux-like).",
            "JavaScript": "Prototype chain for inheritance. Dynamic object properties. Closures capture state. `this` binding is the source of bugs.",
            "Java": "Class instances on the heap. Immutable objects (String, BigDecimal) for thread safety. Virtual threads for massive concurrency.",
            "C/C++": "Raw pointers, manual allocation. const correctness for immutability. RAII ties resource lifetime to scope. Undefined behavior lurks.",
        },
        "synapse_brief": "All languages manage state — but the MECHANISM differs: ownership (Rust), message-passing (Go), value semantics (Swift), null-tracking (Kotlin), prototype chain (JS), GC heap (Java), raw pointers (C)."
    },
    "abstraction": {
        "description": "How does the language create reusable, composable abstractions?",
        "patterns": {
            "Rust": "Traits + generics: 'traits as contracts, generics as compile-time polymorphism.' Zero-cost abstractions — the compiler erases them.",
            "Go": "Interfaces + functions: 'interfaces are implicit satisfaction.' Composition via embedding. Functions are first-class values.",
            "Swift": "Protocols + extensions: 'protocols define what a type CAN do, not what it IS.' Extensions add behavior to existing types.",
            "Kotlin": "Classes + extension functions: add methods to closed classes. Sealed classes for exhaustive matching. Delegation built-in.",
            "TypeScript": "Interfaces + type aliases + generics: structural typing, shape-based compatibility. Type inference reduces verbosity.",
            "JavaScript": "Functions + closures + prototype chain: classical inheritance is sugar over prototypes. ES6 classes added syntactic familiarity.",
            "Java": "Classes + interfaces + abstract classes: nominal typing. Generics via erasure (runtime loses type info). Annotations for meta-programming.",
            "C/C++": "Templates + inheritance + operator overloading: C++ templates are Turing-complete (metaprogramming). RAII for resource abstraction.",
        },
        "synapse_brief": "Abstraction in all languages means 'hide complexity behind a simpler interface.' The difference is WHEN (compile-time vs runtime) and HOW (inheritance vs composition vs traits)."
    },
    "flow_control": {
        "description": "How does the language model computation and control flow?",
        "patterns": {
            "Rust": "Pattern matching + Option/Result: exhaustive matching forces handling all cases. No exceptions — errors are values.",
            "Go": "Goroutines + channels + select: concurrent flow via CSP. select for multiplexing. defer for guaranteed cleanup.",
            "Swift": "do/catch + async/await + Result<T>: typed errors. Actors for thread-safe state. async/await for sequential-looking async.",
            "Kotlin": "Exceptions + coroutines: checked exceptions (controversial). Flow for async streams. Sequence for lazy evaluation.",
            "TypeScript": "Promises + async/await + union types: errors as rejected promises. Discriminated unions for state machines.",
            "JavaScript": "Callbacks → Promises → async/await: evolution of async patterns. Event loop is single-threaded, non-blocking.",
            "Java": "Checked exceptions + virtual threads (Java 21+): exceptions force caller to handle errors. Structured concurrency withScopedValue.",
            "C/C++": "goto, exceptions, longjmp: multiple flow mechanisms. RAII for deterministic cleanup. Coroutines (C++20) for async.",
        },
        "synapse_brief": "Every language has ways to: (1) branch (if/switch/match), (2) loop (for/while), (3) handle errors, (4) do async work. The synapse: the STYLE of these mechanisms reveals the language's philosophy on safety vs. control."
    },
    "type_system": {
        "description": "How does the language approach types and type safety?",
        "patterns": {
            "Rust": "Algebraic data types (enum with data), trait bounds, lifetime annotations. The compiler proves correctness.",
            "Go": "Structural typing, interfaces implicit, generics (2022). No sum types — use interfaces for variant handling.",
            "Swift": "Protocol composition, associated types, existential types (any). Generics with clause constraints.",
            "Kotlin": "Nullable types (?.) vs non-nullable, reified generics (JVM), inline classes for type aliases.",
            "TypeScript": "Structural typing, generics, conditional types, mapped types. Type-level computation is Turing-complete.",
            "JavaScript": "Dynamic types, no compile-time checks. typeof is limited. Proxy for meta-object protocol.",
            "Java": "Nominal typing, type erasure for generics. Primitive types vs reference types. Records (Java 16+) for data.",
            "C/C++": "Static typing with templates. auto type deduction. constexpr for compile-time computation. undefined behavior is a type hazard.",
        },
        "synapse_brief": "Type systems range from 'everything is an object' (JS) to 'the compiler proves memory safety' (Rust). The synapse: stronger type systems catch more bugs at compile time, but demand more from the programmer."
    },
    "concurrency": {
        "description": "How does the language handle parallel and concurrent computation?",
        "patterns": {
            "Rust": "Fearless concurrency: Arc<Mutex<T>>, Send + Sync traits. No data races possible at compile time. async/await with Tokio.",
            "Go": "Goroutines are cheap (2KB stacks). CSP via channels. select for I/O multiplexing. GC pauses minimized.",
            "Swift": "Actors (Swift 6) guarantee no data races. @MainActor for UI. async/await. Sendable checking at compile time.",
            "Kotlin": "Coroutines (structured concurrency), Flows for streams. Dispatchers control thread pools. StructuredTaskScope for hierarchy.",
            "TypeScript": "Web Workers for parallelism. async/await for I/O concurrency. SharedArrayBuffer for true parallelism (requires SAB).",
            "JavaScript": "Event loop, microtasks vs macrotasks. Web Workers for parallelism. Promises chain async work.",
            "Java": "Virtual threads (Java 21) for massive concurrency. ExecutorService thread pools. Happens-before memory model.",
            "C/C++": "Threads (C++11), atomics, mutexes. Memory model withsequentially-consistent ordering. Data races undefined behavior.",
        },
        "synapse_brief": "Concurrency paradigms: message-passing (Go, Erlang), actor model (Swift 6, Akka), shared-memory with locks (Java, C++), compile-time proof (Rust). The synapse: more explicit coordination = more control, but more verbosity."
    },
    "memory_model": {
        "description": "How does the language manage memory and resources?",
        "patterns": {
            "Rust": "Ownership (linear type), borrowing, lifetime annotations. Drop + Arc<Mutex<T>> for shared ownership. No GC.",
            "Go": "Concurrent GC (sub-1ms pauses). Escape analysis moves stack-allocatable objects. Pointers but no pointer arithmetic.",
            "Swift": "ARC (Automatic Reference Counting): compile-time reference counting, no GC pauses. weak/unowned for cycles.",
            "Kotlin": "JVM GC (G1, ZGC, Shenandoah). Escape analysis for stack allocation. No explicit memory management.",
            "TypeScript": "No memory management — JS engine (V8) handles GC. TypedArrays for manual buffer management.",
            "JavaScript": "V8 GC: generational, concurrent, incremental. Memory pressure signals trigger collection cycles.",
            "Java": "JVM GC: ZGC (<1ms pause), G1 (throughput), Shenandoah (no-pause). Heap tuning is a discipline.",
            "C/C++": "Manual malloc/free, RAII. Smart pointers (C++11): unique_ptr, shared_ptr. No safety net — UB is possible.",
        },
        "synapse_brief": "Memory models range from 'you own it' (Rust: ownership) to 'the runtime owns it' (JS: GC) with intermediate approaches (ARC in Swift, JVM GC in Java/Kotlin). The synapse: who is responsible for freeing memory? Manual vs. automatic vs. compile-time proof."
    },
    "error_handling": {
        "description": "How does the language represent and handle errors?",
        "patterns": {
            "Rust": "Result<T, E> and Option<T>: errors are values, returned like any other. No exceptions — exhaustive matching required.",
            "Go": "Errors are values: returned explicitly, checked at every call site. No exceptions. Error wrapping preserves stack.",
            "Swift": "do/catch with typed throws. Result<T, Error>. Never ignore errors by default.",
            "Kotlin": "Exceptions (checked in Java interop, unchecked by default). try/catch/finally. Kotlin Result for explicit handling.",
            "TypeScript": "Exceptions + union types for error states. throw is rarely used in Node.js — errors as values preferred.",
            "JavaScript": "throw is exceptional — errors as values preferred. try/catch/finally. Unhandled rejections are silent failures.",
            "Java": "Checked exceptions (enforced at compile time) — controversial. Unchecked exceptions (RuntimeException). Throwable hierarchy.",
            "C/C++": "errno, return codes, exceptions. RAII for cleanup. C++ exceptions have overhead. No memory-safe error handling.",
        },
        "synapse_brief": "Two philosophies: 'errors as values' (Rust, Go, functional) vs. 'errors as exceptions' (Java, JS, traditional). The synapse: explicit error handling (Result) catches more bugs but is verbose; exceptions are ergonomic but invisible at call sites."
    },
}

# ── Cross-language conceptual bridges ────────────────────────────────────────
# These are "aha!" connections — things that click when you see them
CROSS_LANGUAGE_INSIGHTS = [
    {
        "bridge": "Rust's ownership ↔ Swift's ARC",
        "insight": "Both are compile-time memory management — Rust uses linear types, Swift uses reference counting. Neither requires a GC. The difference: Rust's borrow checker prevents invalid states; Swift's ARC requires weak/unowned to break cycles.",
        "languages": ["Rust", "Swift"],
        "category": "memory_model"
    },
    {
        "bridge": "Go's goroutines ↔ JavaScript's async/await",
        "insight": "Goroutines are cheap green threads (2KB stacks); async/await in JS is syntax sugar over Promises. Both make concurrency feel sequential. The difference: Go's scheduler is cooperative; JS uses the event loop.",
        "languages": ["Go", "JavaScript"],
        "category": "concurrency"
    },
    {
        "bridge": "TypeScript's structural typing ↔ Go's implicit interfaces",
        "insight": "Both check 'does this shape match?' rather than 'was this explicitly declared?' TypeScript structural typing means you can extend a type without modifying it. Go interfaces are satisfied implicitly — if you have the methods, you implement the interface.",
        "languages": ["TypeScript", "Go"],
        "category": "type_system"
    },
    {
        "bridge": "Rust's Option<T> ↔ Kotlin's nullable types",
        "insight": "Rust's Option<T> and Kotlin's nullable T? are the same concept: a type that may or may not have a value. The difference: Rust uses match/if let for exhaustive handling; Kotlin uses ?. and let blocks.",
        "languages": ["Rust", "Kotlin"],
        "category": "state"
    },
    {
        "bridge": "Swift's protocols ↔ Go's interfaces",
        "insight": "Both are about 'what can this do?' rather than 'what is this?'. The difference: Swift protocols can have default implementations via extensions; Go interfaces are implicit and have no implementation.",
        "languages": ["Swift", "Go"],
        "category": "abstraction"
    },
    {
        "bridge": "Java's checked exceptions ↔ TypeScript's union types for errors",
        "insight": "Java's checked exceptions FORCE the caller to handle errors at compile time. TypeScript's discriminated union types make error states explicit in the type. Both are compile-time safety mechanisms for errors.",
        "languages": ["Java", "TypeScript"],
        "category": "error_handling"
    },
    {
        "bridge": "C++ templates ↔ TypeScript generics",
        "insight": "Both are compile-time code generation: C++ templates produce type-safe machine code at compile time; TypeScript generics work at the type level. Both support constraints (where clauses / extends).",
        "languages": ["C/C++", "TypeScript"],
        "category": "type_system"
    },
    {
        "bridge": "Rust's Result<T, E> ↔ Go's (T, error) pattern",
        "insight": "Rust: return Result<T, E> and use ? operator to propagate. Go: return (value, error) and check if error is nil. Both make errors explicit return values. The difference: Rust's type system forces exhaustive handling; Go relies on convention.",
        "languages": ["Rust", "Go"],
        "category": "error_handling"
    },
    {
        "bridge": "Kotlin's coroutines ↔ JavaScript's Promises",
        "insight": "Both are about async code that reads like sync code. Kotlin uses suspend functions; JS uses async functions. The difference: Kotlin's Flow is lazy (like a generator); JS Promises are eager (like a one-shot).",
        "languages": ["Kotlin", "JavaScript"],
        "category": "concurrency"
    },
    {
        "bridge": "Swift's Result<T, Error> ↔ Rust's Result<T, E>",
        "insight": "Identical concepts with different syntax. Swift: Result.success(.value), Result.failure(.error). Rust: Ok(value), Err(error). Both support map, flatMap, and pattern matching.",
        "languages": ["Swift", "Rust"],
        "category": "error_handling"
    },
    {
        "bridge": "Rust's trait system ↔ Haskell's typeclasses",
        "insight": "Rust traits are like Haskell typeclasses: they define a contract that types can implement. Both support default implementations, associated types, and orphan rules (in Rust: coherence).",
        "languages": ["Rust"],
        "category": "abstraction"
    },
    {
        "bridge": "Go's defer ↔ C++ RAII",
        "insight": "Both guarantee cleanup: Go's defer runs on scope exit; C++ destructors run when an object goes out of scope. The difference: defer is a statement; RAII is tied to object lifetime. Both prevent resource leaks.",
        "languages": ["Go", "C/C++"],
        "category": "flow_control"
    },
    {
        "bridge": "Kotlin's data classes ↔ Python's dataclasses",
        "insight": "Both auto-generate boilerplate: equals, hashCode, toString, copy. The difference: Kotlin data classes are nominal (name matters); Python dataclasses are essentially syntactic sugar over typed dicts with named fields.",
        "languages": ["Kotlin"],
        "category": "state"
    },
    {
        "bridge": "TypeScript's readonly ↔ Swift's let (immutability)",
        "insight": "readonly arrays in TS can't be modified; let in Swift creates immutable bindings. Both prevent accidental mutation. The difference: TS readonly is shallow; Swift let is deep (value types copy on assignment).",
        "languages": ["TypeScript", "Swift"],
        "category": "state"
    },
    {
        "bridge": "Java's Optional ↔ Swift's Optional",
        "insight": "Both represent 'value that may be absent.' Java Optional (Java 8+) has map/flatMap/filter; Swift Optional has map/flatMap/compactMap. The difference: Swift's ? syntax is built into the type system; Java's Optional is a wrapper class.",
        "languages": ["Java", "Swift"],
        "category": "state"
    },
]


def find_synapses(language: str) -> Dict[str, Any]:
    """
    Find all conceptual synapses for a given language.
    Returns neural pathway data, concept patterns, and cross-language insights.
    """
    config = load_rotation()

    if language not in config["languages"]:
        raise ValueError(
            f"Language '{language}' not in rotation. "
            f"Available: {', '.join(config['languages'])}"
        )

    # Build concept neural map for this language
    concept_map = {}
    for concept, data in CORE_CONCEPTS.items():
        pattern = data["patterns"].get(language, "No pattern recorded.")
        synapse_brief = data["synapse_brief"]
        concept_map[concept] = {
            "description": data["description"],
            "thought_pattern": pattern,
            "synapse_brief": synapse_brief,
        }

    # Find cross-language bridges that involve this language
    bridges = []
    for insight in CROSS_LANGUAGE_INSIGHTS:
        if language in insight["languages"]:
            bridges.append({
                "bridge": insight["bridge"],
                "insight": insight["insight"],
                "connected_to": [l for l in insight["languages"] if l != language],
                "category": insight["category"],
            })

    # Build a "thought summary" for this language
    thought_summary = _build_thought_summary(language, concept_map)

    # Advance rotation
    current_idx = config["languages"].index(language)
    next_idx = (current_idx + 1) % len(config["languages"])
    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now().isoformat()
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "thought_summary": thought_summary,
        "concepts": concept_map,
        "concept_count": len(concept_map),
        "bridges": bridges,
        "bridge_count": len(bridges),
        "next_language": config["languages"][next_idx],
        "rotation": config["languages"],
        "timestamp": datetime.now().isoformat(),
    }


def _build_thought_summary(language: str, concept_map: Dict) -> str:
    """Build a one-sentence philosophical summary of how this language thinks."""
    summaries = {
        "Rust": "Rust thinks in OWNERSHIP — every value has exactly one owner, and the compiler verifies the rules at compile time, making memory safety a mathematical guarantee rather than a runtime convention.",
        "Go": "Go thinks in CHANNELS — concurrency is communication, not shared memory. Simplicity is a feature: one way to do things, fast compilation, and readable code that scales across thousands of engineers.",
        "Swift": "Swift thinks in PROTOCOLS — define what something CAN do, not what it IS. Safety isn't a feature you add; it's the default: no nil without Optional, no uninitialized values, and memory safety via ARC.",
        "Kotlin": "Kotlin thinks in PRAGMATISM — null safety, extension functions, and coroutines are designed to solve real problems without breaking Java interoperability.",
        "TypeScript": "TypeScript thinks in SHAPES — types describe the structure of data, not the name of a class. If it has the right shape, it's the right type — and the compiler ensures you never misuse it.",
        "JavaScript": "JavaScript thinks in FUNCTIONS — first-class functions, closures, and prototype inheritance create a flexible, expressive language where 'everything is possible' sometimes means 'nothing is obvious.'",
        "Java": "Java thinks in CLASSES — everything is an object (except primitives), the JVM is the great equalizer, and 'write once, run anywhere' made it the enterprise backbone of the modern world.",
        "C/C++": "C/C++ thinks in CONTROL — memory layout, pointer arithmetic, and zero-overhead abstractions give you total control. The programmer is always right — and the price is undefined behavior.",
    }
    return summaries.get(language, "Unknown language.")


def synapse(language: str) -> Dict[str, Any]:
    """
    Main entry point: find neural pathways for the selected language.
    Wrapper around find_synapses for compatibility.
    """
    return find_synapses(language)


def run_tests():
    """Run tests to validate the Language Synapse module."""
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

    def assert_in(a, b, msg=""):
        nonlocal tests_passed, tests_failed
        if a in b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — '{a}' not found in target")

    def assert_true(a, msg=""):
        nonlocal tests_passed, tests_failed
        if a:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg}")

    print("Testing Language Synapse...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_eq(True, 0 <= config["current_index"] < 8, "current_index in valid range")
    assert_eq("Rust", config["languages"][0], "Rust is first language")

    print("  Testing find_synapses for Rust...")
    result = find_synapses("Rust")
    expected_keys = [
        "tool", "version", "selected_language", "thought_summary",
        "concepts", "concept_count", "bridges", "bridge_count",
        "next_language", "rotation", "timestamp"
    ]
    for key in expected_keys:
        assert_eq(True, key in result, f"Key '{key}' present in response")

    assert_eq("Rust", result["selected_language"], "Rust is selected")
    assert_eq("Go", result["next_language"], "Next language is Go")
    assert_eq(TOOL_NAME, result["tool"], "Correct tool name")
    assert_eq(7, result["concept_count"], "Rust has all 7 core concepts")

    print("  Verifying concept structure...")
    concepts = result["concepts"]
    required_concepts = ["state", "abstraction", "flow_control", "type_system",
                         "concurrency", "memory_model", "error_handling"]
    for concept in required_concepts:
        assert_eq(True, concept in concepts, f"Concept '{concept}' present")
        assert_eq(True, "description" in concepts[concept], f"{concept} has description")
        assert_eq(True, "thought_pattern" in concepts[concept], f"{concept} has thought_pattern")
        assert_eq(True, "synapse_brief" in concepts[concept], f"{concept} has synapse_brief")
        # Each thought_pattern should be non-empty and substantive
        assert_true(len(concepts[concept]["thought_pattern"]) > 30, f"{concept} pattern is substantive")

    print("  Verifying thought_summary...")
    assert_true(len(result["thought_summary"]) > 50, "Thought summary is meaningful")
    assert_in("ownership", result["thought_summary"].lower(), "Thought summary mentions ownership")

    print("  Verifying bridges structure...")
    bridges = result["bridges"]
    assert_true(len(bridges) >= 3, f"Rust has at least 3 bridges ({len(bridges)} found)")
    for bridge in bridges:
        assert_eq(True, "bridge" in bridge, "Bridge has name")
        assert_eq(True, "insight" in bridge, "Bridge has insight text")
        assert_eq(True, "connected_to" in bridge, "Bridge has connected_to list")
        assert_eq(True, "category" in bridge, "Bridge has category")
        assert_true(len(bridge["insight"]) > 30, "Bridge insight is substantive")

    print("  Verifying rotation update...")
    config2 = load_rotation()
    assert_eq(1, config2["current_index"], "Index advanced to 1 (Go)")
    assert_eq("Rust", config2["last_language"], "Last language recorded as Rust")

    print("  Testing find_synapses for Go (next in rotation)...")
    result2 = find_synapses("Go")
    assert_eq("Go", result2["selected_language"], "Go is selected")
    assert_eq("Swift", result2["next_language"], "Next language is Swift")
    assert_true(len(result2["thought_summary"]) > 50, "Go thought summary is meaningful")

    print("  Testing all languages have complete synapse data...")
    for lang in config["languages"]:
        r = find_synapses(lang)
        assert_eq(lang, r["selected_language"], f"{lang} selected correctly")
        assert_eq(7, r["concept_count"], f"{lang} has all 7 concepts")
        assert_true(len(r["thought_summary"]) > 30, f"{lang} has meaningful thought summary")
        # Check thought pattern for each concept is substantive
        for concept in required_concepts:
            pattern = r["concepts"][concept]["thought_pattern"]
            assert_true(len(pattern) > 30, f"{lang} has substantive pattern for {concept}")

    print("  Testing bridge count is reasonable...")
    for lang in config["languages"]:
        r = find_synapses(lang)
        # Each language should have at least 2 bridges
        assert_true(r["bridge_count"] >= 2, f"{lang} has >= 2 bridges ({r['bridge_count']})")

    print("  Verifying cross-language insights within each language...")
    for lang in config["languages"]:
        r = find_synapses(lang)
        seen = set()
        for bridge in r["bridges"]:
            # Within a single language, bridges should be unique
            assert_true(bridge["bridge"] not in seen, f"Unique bridge in {lang}: {bridge['bridge']}")
            seen.add(bridge["bridge"])
        # Verify total bridge count is reasonable
        assert_true(r["bridge_count"] >= 1, f"{lang} has at least 1 bridge")

    print("  Testing invalid language handling...")
    try:
        find_synapses("Python")
        tests_failed += 1
        print("  ❌ FAIL: No error raised for invalid language")
    except ValueError as e:
        tests_passed += 1
        print(f"  ✅ PASS: ValueError raised for invalid language")
        assert_in("not in rotation", str(e), "Error mentions rotation")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ FAIL: Wrong exception: {e}")

    print("  Testing thought_summary for all languages...")
    all_thoughts = {}
    for lang in config["languages"]:
        r = find_synapses(lang)
        assert_true(len(r["thought_summary"]) > 30, f"{lang} thought_summary not empty")
        # Each language should have a unique thought summary
        assert_true(r["thought_summary"] not in all_thoughts.values(), f"{lang} thought_summary is unique")
        all_thoughts[lang] = r["thought_summary"]

    print("  Verifying CORE_CONCEPTS has all required concepts...")
    for concept in required_concepts:
        assert_true(concept in CORE_CONCEPTS, f"{concept} in CORE_CONCEPTS")
        assert_true("description" in CORE_CONCEPTS[concept], f"{concept} has description")
        assert_true("patterns" in CORE_CONCEPTS[concept], f"{concept} has patterns dict")
        # Each concept should have patterns for all languages
        for lang in config["languages"]:
            assert_true(lang in CORE_CONCEPTS[concept]["patterns"], f"{concept} has pattern for {lang}")

    print("  Testing timestamp format...")
    assert_true("timestamp" in result, "Result has timestamp")
    # Timestamp should be ISO format
    ts = result["timestamp"]
    assert_true(len(ts) > 20, "Timestamp is non-empty")
    assert_true("T" in ts, "Timestamp is ISO format (has T separator)")

    print(f"\n{'='*55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("🧠 All Synapse tests passed! The neural pathways are connected.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--synapse":
        language = sys.argv[2] if len(sys.argv) > 2 else "Rust"
        result = find_synapses(language)
        print(json.dumps(result, indent=2))
    else:
        print(f"Language Synapse v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m language_synapse --test        # Run tests")
        print("  python -m language_synapse --synapse [lang]  # Map neural pathways")