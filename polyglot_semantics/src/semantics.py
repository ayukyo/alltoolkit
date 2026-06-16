"""
Polyglot Semantics — Semantic Topology Engine
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-semantics"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent.parent
_WORKSPACE_ROOT = _MODULE_DIR.parent
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]


# ─────────────────────────────────────────────────────────────────────────────
# Semantic fingerprints per language
# Each language maps concepts to syntactic forms differently.
# We track: existence, action, state, relation, identity, control, abstraction.
# ─────────────────────────────────────────────────────────────────────────────

SEMANTIC_PROFILES: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "paradigm": "systems / memory-safety via ownership",
        "existence": {
            "keyword": "let / let mut / const",
            "semantic_difference": (
                "Binding vs binding-with-mutability vs compile-time constant. "
                "Rust splits 'existence' into three tiers, each with strict guarantees. "
                "Ownership is embedded in the binding itself — the variable IS the owner."
            ),
        },
        "action": {
            "keyword": "fn",
            "semantic_difference": (
                "Functions are declared with 'fn'. No methods 'inside' structs — "
                "only associated functions. The function is a standalone unit of "
                "action. First-class: functions can be passed as values."
            ),
        },
        "state": {
            "keyword": "struct / enum / tuple",
            "semantic_difference": (
                "Structs are named field aggregates; enums are tagged unions — "
                "NOT classes. State is expressed through types, not objects. "
                "The type system IS the state model. No classes, no inheritance, "
                "no 'this'. Composition over inheritance."
            ),
        },
        "relation": {
            "keyword": "impl Trait for Type / trait",
            "semantic_difference": (
                "Relations are expressed via traits — Rust's ad-hoc polymorphism. "
                "A trait says what a type CAN do (interface-equivalent) but the "
                "implementation lives separately. No subtyping hierarchy by default. "
                "Impl blocks are the only way to attach behavior."
            ),
        },
        "identity": {
            "keyword": "&T / &mut T / T (owned)",
            "semantic_difference": (
                "Identity is split across borrowing levels: shared reference, "
                "mutable reference, or owned value. Two owned values are ALWAYS "
                "independent. Two references to the same data cannot coexist "
                "if one is mutable. Identity is BORROW-based."
            ),
        },
        "control": {
            "keyword": "match / if let / loop",
            "semantic_difference": (
                "Pattern matching (match) is exhaustive — the compiler forces "
                "you to handle all cases. Control flow is algebraic: match "
                "expressions produce values. No fall-through, no switch."
            ),
        },
        "abstraction": {
            "keyword": "generics<T> /trait bounds",
            "semantic_difference": (
                "Generics are monomorphized at compile time — zero runtime cost. "
                "Trait bounds express constraints. No erasure, no boxing. "
                "The abstraction barrier is the trait system."
            ),
        },
        "notable_divergence": (
            "Rust's borrow checker enforces aliasing XOR mutability at compile time. "
            "There is no garbage collector — memory is freed when owners go out of scope. "
            "Rust's 'self' is explicit (self, &self, &mut self). No hidden receivers."
        ),
    },
    "Go": {
        "paradigm": "concurrency-first / procedural with interfaces",
        "existence": {
            "keyword": "var / const / :=",
            "semantic_difference": (
                "Variables are explicitly declared or inferred with :=. "
                "No let/const distinction — mutability is by convention. "
                "Constants must be compile-time known. Existence is flexible."
            ),
        },
        "action": {
            "keyword": "func",
            "semantic_difference": (
                "Functions are first-class; can return multiple values (tuple-like). "
                "No classes — only functions attached to structs (methods). "
                "The receiver syntax (func (r Receiver) Method()) attaches behavior "
                "to types without inheritance."
            ),
        },
        "state": {
            "keyword": "struct / interface",
            "semantic_difference": (
                "Structs are field aggregates — like Rust's struct but with tags "
                "for reflection. Interfaces are implicit — a type satisfies an "
                "interface by implementing its methods. No explicit declaration. "
                "State lives in structs; behavior in methods."
            ),
        },
        "relation": {
            "keyword": "interface / composition",
            "semantic_difference": (
                "Interfaces are structural (nominal), not nominal like Java. "
                "Any type with the right methods satisfies any interface. "
                "Composition via embedding (struct inside struct), not inheritance. "
                "No subtyping hierarchy — flat interface world."
            ),
        },
        "identity": {
            "keyword": "pointers / values",
            "semantic_difference": (
                "Everything can be a pointer (*T) or a value (T). "
                "No borrowing — you pass pointers or copies explicitly. "
                "Maps and slices are reference types under the hood. "
                "Identity is explicit via & operator."
            ),
        },
        "control": {
            "keyword": "if / for / switch",
            "semantic_difference": (
                "Go has ONE loop keyword: for. if and switch have optional "
                "initializer. No while, no do-while. switch does NOT fall-through "
                "by default (break is implicit). Control flow is minimal and uniform."
            ),
        },
        "abstraction": {
            "keyword": "generics (2022) / interface{}",
            "semantic_difference": (
                "Generics added in Go 1.18 — compile-time erasure model (like Java). "
                "interface{} was the pre-generics abstraction (void* equivalent). "
                "Abstraction is interface-based."
            ),
        },
        "notable_divergence": (
            "Go's concurrency model (goroutines + channels) is built into the language, "
            "not a library. Goroutines are cheap threads, channels are typed pipes. "
            "CSP (Communicating Sequential Processes) is a first-class language concept. "
            "No classes, no inheritance, no generics before 1.18."
        ),
    },
    "Swift": {
        "paradigm": "safe / protocol-oriented / value-semantics",
        "existence": {
            "keyword": "var / let / func",
            "semantic_difference": (
                "var = mutable binding, let = immutable binding. "
                "Swift distinguishes binding mutability like Rust, but without "
                "separate const keyword. Functions are first-class (function values)."
            ),
        },
        "action": {
            "keyword": "func",
            "semantic_difference": (
                "Functions declared with func. Methods are functions attached "
                "to a type (self as receiver). No static methods in the Java sense — "
                "type methods via static func. Functions are first-class values."
            ),
        },
        "state": {
            "keyword": "struct / class / enum",
            "semantic_difference": (
                "Structs: value types (copied on assignment). Classes: reference types "
                "(heap-allocated, ARC). Enums: tagged unions with associated values. "
                "State semantics are EXPLICITLY chosen per type — value vs reference."
            ),
        },
        "relation": {
            "keyword": "protocol / extension",
            "semantic_difference": (
                "Protocols are structural interfaces (like Go). Extensions add "
                "functionality to existing types without inheritance. A type can "
                "conform to multiple protocols. No class hierarchy required."
            ),
        },
        "identity": {
            "keyword": "reference semantics (class) vs value semantics (struct)",
            "semantic_difference": (
                "Two structs with identical contents are equal AND independent. "
                "Two class instances with identical contents are the SAME object "
                "(reference identity). Swift makes the choice explicit per type."
            ),
        },
        "control": {
            "keyword": "if / guard / switch / for-in",
            "semantic_difference": (
                "guard unwraps optionals early-exit style. switch is exhaustive "
                "with pattern matching. for-in iterates over sequences. "
                "No while-do. Optional chaining (?.) is a control flow mechanism."
            ),
        },
        "abstraction": {
            "keyword": "generics<T> / protocol constraints",
            "semantic_difference": (
                "Generics with protocol constraints. Protocol compositions via &. "
                "Existentials via 'any Protocol'. Associated types in protocols. "
                "Abstraction is protocol and generic-based."
            ),
        },
        "notable_divergence": (
            "Swift's String is a value type (Unicode grapheme clusters, "
            "copied on assignment). Unlike most languages where strings are "
            "reference types. Swift's optionals (? and !) are a type-level "
            "null-safety system — the type system itself encodes absence."
        ),
    },
    "Kotlin": {
        "paradigm": "pragmatic JVM / null-safe / interoperable",
        "existence": {
            "keyword": "val / var",
            "semantic_difference": (
                "val = read-only binding (like Rust's let), var = mutable. "
                "No separate const — val is the only immutability guarantee. "
                "Variables must be explicitly typed or inferred."
            ),
        },
        "action": {
            "keyword": "fun",
            "semantic_difference": (
                "Functions are declared with fun. Can be top-level, inside a class "
                "(methods), or in a file (extension functions). Functions are first-class. "
                "Named parameters, default parameters, and infix functions exist."
            ),
        },
        "state": {
            "keyword": "class / data class / object",
            "semantic_difference": (
                "Regular classes. Data classes auto-generate equals/hashCode/toString. "
                "Object is a singleton class. Sealed classes restrict inheritance. "
                "No structs — everything is a reference type on the JVM (unless val var)."
            ),
        },
        "relation": {
            "keyword": "interface / inheritance (:)",
            "semantic_difference": (
                "Interfaces define contracts. Classes inherit via : syntax. "
                "Single inheritance of classes, multiple interfaces. "
                "Composition via delegation (by keyword)."
            ),
        },
        "identity": {
            "keyword": "references (JVM) / == (structural equality)",
            "semantic_difference": (
                "== is structural equality (equals()), === is reference equality. "
                "On JVM: reference equality is pointer comparison. "
                "Data classes get structural equality for free."
            ),
        },
        "control": {
            "keyword": "if / when / try / for / while",
            "semantic_difference": (
                "when is switch + pattern matching (exhaustive). if and when "
                "are expressions (produce values). No fall-through. "
                "try-catch-finally also an expression."
            ),
        },
        "abstraction": {
            "keyword": "generics<T> / reified (inline only)",
            "semantic_difference": (
                "Generics with type erasure (JVM). Inline functions can use "
                "reified generics (type preserved at runtime). Variance annotations "
                "(out/in) control subtype relationships."
            ),
        },
        "notable_divergence": (
            "Kotlin's null safety (?, !!, let, safe call) is built into the type system. "
            "The compiler enforces null checks at compile time. "
            "Coroutines (async/await) are library-level, not syntax. "
            "Extension functions let any type gain methods without inheritance."
        ),
    },
    "TypeScript": {
        "paradigm": "gradual typing / structural / transpiled",
        "existence": {
            "keyword": "let / const / var",
            "semantic_difference": (
                "const = immutable binding (like Kotlin's val), let = mutable. "
                "var is function-scoped (legacy). Block-scoping is the norm. "
                "TypeScript adds compile-time type annotations."
            ),
        },
        "action": {
            "keyword": "function / arrow function",
            "semantic_difference": (
                "Two function syntaxes: function keyword and arrow functions (=>). "
                "Arrow functions have lexical this (no binding required). "
                "Functions are first-class values. Methods are properties on objects."
            ),
        },
        "state": {
            "keyword": "class / interface / type",
            "semantic_difference": (
                "class: traditional prototype-based inheritance. "
                "interface: structural type contract (like Go). "
                "type: type alias or union/intersection types. "
                "All three can express state — each with different semantics."
            ),
        },
        "relation": {
            "keyword": "extends (class) / implements (interface) / interface merging",
            "semantic_difference": (
                "Classes extend single classes. Interfaces merge across declarations "
                "(declaration merging). No multiple inheritance — multiple interfaces OK. "
                "Duck typing: structural compatibility determines relation."
            ),
        },
        "identity": {
            "keyword": "reference identity / === (strict equality)",
            "semantic_difference": (
                "Objects are references. === checks value equality for primitives, "
                "reference equality for objects. No built-in deep equality. "
                "Identity is heap-pointer based for objects."
            ),
        },
        "control": {
            "keyword": "if / switch / try-catch / for / while / do-while",
            "semantic_difference": (
                "Standard C-style control flow. switch does NOT fall-through by default. "
                "try-catch-finally. for-of (iterables), for-in (enumerable keys). "
                "Async/await is syntax sugar over Promises."
            ),
        },
        "abstraction": {
            "keyword": "generics<T> / union types / conditional types",
            "semantic_difference": (
                "Generics with type inference. Union types (|) and intersection types (&). "
                "Mapped types, conditional types, template literal types. "
                "TypeScript types are erased — no runtime type info (by default)."
            ),
        },
        "notable_divergence": (
            "TypeScript's 'as' cast is a runtime assertion (type erasure). "
            "The 'unknown' type is the type-safe counterpart of 'any' — "
            "you must narrow unknown before using it. "
            "Decorators are experimental (proposal-driven). "
            "TypeScript compiles to JavaScript — the runtime is JavaScript."
        ),
    },
    "JavaScript": {
        "paradigm": "prototype-based / dynamic / event-loop",
        "existence": {
            "keyword": "let / const / var",
            "semantic_difference": (
                "const = immutable binding (reference immutability, not deep). "
                "let = mutable, block-scoped. var = mutable, function-scoped. "
                "No type annotations — everything is dynamic."
            ),
        },
        "action": {
            "keyword": "function / arrow function",
            "semantic_difference": (
                "Two function forms. Arrow functions have lexical this (no dynamic binding). "
                "Functions are first-class values. Closures capture their environment. "
                "No multi-return — return a plain object for multiple values."
            ),
        },
        "state": {
            "keyword": "object / class (ES6+) / prototype chain",
            "semantic_difference": (
                "Objects are dynamic key-value maps. Class syntax (ES6) is sugar "
                "over prototypes. Inheritance via prototype chain — not class hierarchy "
                "in the traditional OOP sense. No interfaces (TypeScript adds them)."
            ),
        },
        "relation": {
            "keyword": "prototype / extends / super",
            "semantic_difference": (
                "Relation via prototype chain: [[Prototype]] link. "
                "class extends sets the prototype. "
                "Object.create() creates objects with explicit prototypes. "
                "No static typing — relation is dynamic at runtime."
            ),
        },
        "identity": {
            "keyword": "Object.is() / === / Object.assign (clone)",
            "semantic_difference": (
                "=== is strict equality (NaN !== NaN, +0 === -0). "
                "Object.is() fixes === quirks (NaN === NaN, +0 !== -0). "
                "No built-in deep clone — need structured cloning or libraries."
            ),
        },
        "control": {
            "keyword": "if / switch / try-catch / for / while / do-while",
            "semantic_difference": (
                "Standard C-style. switch does not fall-through. "
                "try-catch-finally. Async patterns via callbacks → Promises → async/await. "
                "No built-in generators in the language (but iterators exist)."
            ),
        },
        "abstraction": {
            "keyword": "Closures / prototypes / WeakMap",
            "semantic_difference": (
                "Abstraction via closures (encapsulation), prototypes (inheritance), "
                "and Symbol (unique property keys). No generics. "
                "Proxy and Reflect objects provide meta-programming."
            ),
        },
        "notable_divergence": (
            "JavaScript's typeof null === 'object' — a historical quirk. "
            "JavaScript has no classes in the traditional sense — only prototypes. "
            "The event loop (libuv) handles async I/O without threads. "
            "Array.sort() is not stable by default (V8 used TimSort historically, now stable). "
            "NaN is the only value that is not equal to itself (NaN !== NaN)."
        ),
    },
    "Java": {
        "paradigm": "class-based OOP / JVM / static typing",
        "existence": {
            "keyword": "variables / final",
            "semantic_difference": (
                "All variables hold references (except primitives). "
                "final makes a reference immutable — the referred object can still change. "
                "No let/const — mutability is via convention and final."
            ),
        },
        "action": {
            "keyword": "method (void or return type)",
            "semantic_difference": (
                "Methods belong to classes. static methods are class methods. "
                "Instance methods require an object. Methods cannot be first-class values "
                "directly (method references introduced in Java 8). No multi-return — "
                "return objects or use out-parameters (rarely)."
            ),
        },
        "state": {
            "keyword": "class / record (Java 16+) / enum",
            "semantic_difference": (
                "Classes are the primary state unit. record is a shallow-immutable data "
                "carrier (auto-generates equals, hashCode, toString). "
                "enum is a fixed set of constants with optional state. "
                "Static state belongs to the class, instance state to the object."
            ),
        },
        "relation": {
            "keyword": "extends (single) / implements (multiple)",
            "semantic_difference": (
                "Single class inheritance. Multiple interface implementation. "
                "An interface can have default methods (Java 8+). "
                "No composition-based relation by default — use delegation patterns."
            ),
        },
        "identity": {
            "keyword": "== (reference) / .equals() (content)",
            "semantic_difference": (
                "== compares references (pointer equality). equals() is the content "
                "comparison (must be overridden). String pool for interned strings. "
                "Identity is heap-pointer based for objects."
            ),
        },
        "control": {
            "keyword": "if / else / switch (pattern matching Java 17+) / for / while / do-while",
            "semantic_difference": (
                "Standard C-style. switch with pattern matching (Java 17+). "
                "Enhanced for (for-each). No goto. "
                "Checked exceptions must be declared or caught."
            ),
        },
        "abstraction": {
            "keyword": "generics (type erasure) / wildcard (? super T / ? extends T)",
            "semantic_difference": (
                "Generics with type erasure (runtime type info erased). "
                "Wildcards express covariance (? extends T) and contravariance (? super T). "
                "No primitive generics (use wrapper types). "
                "Abstract classes and interfaces are abstraction boundaries."
            ),
        },
        "notable_divergence": (
            "Java has checked exceptions — methods must declare what they throw. "
            "The JVM has a strong memory model (happen-before guarantees). "
            "Garbage collection is a runtime concern — not visible to the programmer. "
            "Covariance in arrays is unsound (Integer[] can be cast to Number[] at runtime "
            "but ArrayStoreException guards it)."
        ),
    },
    "C/C++": {
        "paradigm": "systems / zero-overhead / manual memory",
        "existence": {
            "keyword": "variables / const / constexpr",
            "semantic_difference": (
                "Variables are typed storage locations. const = read-only at compile time. "
                "constexpr = evaluated at compile time (C++11). "
                "No garbage collection — memory is explicitly managed. "
                "Pointers (*), references (&), and values are distinct identity modes."
            ),
        },
        "action": {
            "keyword": "function",
            "semantic_difference": (
                "Functions are code pointers. No method vs function distinction — "
                "C++ member functions have an implicit this pointer. "
                "Functions are not values in C (function pointers exist). "
                "C++ has function objects (functors) and lambdas."
            ),
        },
        "state": {
            "keyword": "struct / class / union",
            "semantic_difference": (
                "struct: public by default (C), both public/private (C++). "
                "class: private by default (C++). "
                "union: overlapping memory for distinct types. "
                "No built-in inheritance — composition and manual vtable management."
            ),
        },
        "relation": {
            "keyword": "inheritance (public/protected/private) / composition / templates",
            "semantic_difference": (
                "C++ supports multiple inheritance. Virtual functions use vtable dispatch. "
                "Templates provide compile-time polymorphism. "
                "No interface keyword — use abstract classes or concepts (C++20)."
            ),
        },
        "identity": {
            "keyword": "address-of (&) / pointer (*) / value",
            "semantic_difference": (
                "Identity modes: value (T), pointer (T*), reference (T&). "
                "References are aliases (not separate objects). "
                "Two pointers can point to the same address. "
                "Identity is fully explicit — no hidden references."
            ),
        },
        "control": {
            "keyword": "if / switch / for / while / do-while / goto",
            "semantic_difference": (
                "Standard C control flow. goto exists (rarely used). "
                "switch does NOT fall-through unless explicitly written. "
                "C++11 added range-based for. "
                "No exceptions in C; C++ has try/catch (exceptions disabled in some codebases)."
            ),
        },
        "abstraction": {
            "keyword": "templates / concepts (C++20) / virtual dispatch",
            "semantic_difference": (
                "Templates: compile-time generic programming (zero overhead). "
                "Concepts: constraints on template arguments (C++20). "
                "Virtual dispatch: runtime polymorphism via vtable. "
                "Abstraction cost is explicit — you choose what you pay for."
            ),
        },
        "notable_divergence": (
            "C/C++ has no garbage collector — memory leaks are the programmer's responsibility. "
            "Buffer overflows and use-after-free are undefined behavior (compiler can assume they don't happen). "
            "C++ move semantics (rvalue references) separate identity from copyability. "
            "C++'s constexpr has evolved: C++20 constexpr virtual functions. "
            "The type system is opt-in — casts are explicit and lossy."
        ),
    },
}


def get_current_language() -> Dict[str, Any]:
    """
    Read language_rotation.json, return the current language and
    advance the index to the next one (round-robin).
    """
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    langs = data["languages"]
    idx = data["current_index"]
    current_lang = langs[idx]

    next_idx = (idx + 1) % len(langs)
    data["current_index"] = next_idx
    data["last_language"] = current_lang
    data["updated_at"] = datetime.now(timezone.utc).isoformat()

    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return {
        "current_language": current_lang,
        "index": idx,
        "next_language": langs[next_idx],
    }


def analyze_semantics(language: str) -> Dict[str, Any]:
    """Return the semantic profile for the given language."""
    if language not in SEMANTIC_PROFILES:
        raise ValueError(f"Unknown language: {language}")
    return SEMANTIC_PROFILES[language]


def format_semantic_fingerprint(lang_info: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format the semantic fingerprint as a readable report."""
    lang = lang_info["current_language"]
    next_lang = lang_info["next_language"]

    lines = [
        "=" * 60,
        f"  🌌 POLYGLOT SEMANTICS — Semantic Fingerprint",
        f"  Language: {lang}",
        f"  Paradigm: {profile['paradigm']}",
        "=" * 60,
        "",
    ]

    sections = [
        ("existence", "🧬 Existence — How does the language express 'being'?"),
        ("action",    "⚡ Action — How does the language express 'doing'?"),
        ("state",     "📦 State — How does the language express 'having'?"),
        ("relation",  "🔗 Relation — How does the language express 'connecting'?"),
        ("identity",  "🪞 Identity — How does the language handle 'self-ness'?"),
        ("control",   "🔄 Control — How does the language direct 'flow'?"),
        ("abstraction","🏗️ Abstraction — How does the language build 'higher worlds'?"),
    ]

    for key, heading in sections:
        entry = profile[key]
        lines.append(heading)
        lines.append(f"  Keyword  : {entry['keyword']}")
        lines.append(f"  Semantics:")
        for word in entry["semantic_difference"].split(". "):
            word = word.strip()
            if word:
                lines.append(f"    · {word}.")
        lines.append("")

    lines.append("─" * 60)
    lines.append(f"  📌 Notable Semantic Divergence")
    for word in profile["notable_divergence"].split(". "):
        word = word.strip()
        if word:
            lines.append(f"    · {word}.")
    lines.append("")
    lines.append("─" * 60)
    lines.append(f"  Next in rotation → {next_lang}")
    lines.append("=" * 60)

    return "\n".join(lines)


def run_tests() -> None:
    """Run basic sanity tests."""
    import traceback

    failures = []

    # Test: rotation advances correctly
    try:
        with open(ROTATION_FILE, "r") as f:
            before = json.load(f)
        lang_info = get_current_language()
        with open(ROTATION_FILE, "r") as f:
            after = json.load(f)

        assert lang_info["current_language"] in ROTATION_ORDER, (
            f"Got unexpected language: {lang_info['current_language']}"
        )
        assert after["current_index"] == (before["current_index"] + 1) % len(before["languages"]), (
            "Index not advanced correctly"
        )
        print("✅ test_rotation_advances")
    except Exception as e:
        failures.append(f"❌ test_rotation_advances: {e}")
        traceback.print_exc()

    # Test: each language has a profile
    try:
        for lang in ROTATION_ORDER:
            profile = analyze_semantics(lang)
            assert "paradigm" in profile
            assert "notable_divergence" in profile
            for key in ["existence", "action", "state", "relation", "identity", "control", "abstraction"]:
                assert key in profile, f"Missing key {key} in {lang}"
                assert "keyword" in profile[key]
                assert "semantic_difference" in profile[key]
        print("✅ test_all_languages_have_profiles")
    except Exception as e:
        failures.append(f"❌ test_all_languages_have_profiles: {e}")
        traceback.print_exc()

    # Test: unknown language raises
    try:
        analyze_semantics("NonExistentLanguage")
        failures.append("❌ test_unknown_language_raises: no exception raised")
    except ValueError:
        print("✅ test_unknown_language_raises")
    except Exception as e:
        failures.append(f"❌ test_unknown_language_raises: {e}")

    # Test: fingerprint output is non-empty
    try:
        lang_info = get_current_language()
        profile = analyze_semantics(lang_info["current_language"])
        fp = format_semantic_fingerprint(lang_info, profile)
        assert len(fp) > 200, f"Fingerprint too short: {len(fp)} chars"
        assert lang_info["current_language"] in fp
        print("✅ test_fingerprint_format")
    except Exception as e:
        failures.append(f"❌ test_fingerprint_format: {e}")
        traceback.print_exc()

    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(f)
        raise SystemExit(1)
    print(f"\n🎉 All tests passed!")