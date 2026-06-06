#!/usr/bin/env python3
"""
⚡ Language Ethos v1.0
A creative tool that distills each programming language into a single
philosophical manifesto — its ethos card.

Creative concept: "Every language has a soul. This tool reveals it."
Each language's ethos card contains:
  - Guiding motto (the one-liner)
  - Philosophical signature (the core belief)
  - Paradigm fingerprint (what programming paradigm it embraces)
  - Design dogmas (the non-negotiable principles)
  - Anti-patterns (what this language actively discourages)
  - Philosophical twin (which human philosophy it mirrors)

Distinct from existing tools:
  - language_archaeology: historical dig through time (temporal)
  - language_compass: learning journey and milestones (progress)
  - language_sage: idioms, tips, and common pitfalls (usage)
  - language_ecohub: package ecosystem field guide (tooling)
  - language_synapse: conceptual bridges between languages (connections)

Ethos is about PHILOSOPHY and BELIEF — the soul of each language.
"""

import json
import os
from datetime import datetime

TOOL_NAME = "language-ethos"
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


# ── Ethos data per language ───────────────────────────────────────────────────
ETHOS_DATA = {
    "Rust": {
        "guiding_motto": "Fearless concurrency. Zero-cost abstractions.",
        "philosophical_signature": (
            "The compiler is not your critic — it is a formal proof. "
            "Through ownership and borrowing rules, Rust enforces memory safety "
            "at compile time. If it compiles, it is provably correct."
        ),
        "paradigm_fingerprint": [
            "Systems programming with zero-cost abstractions",
            "Ownership & borrowing as compile-time correctness proofs",
            "Algebraic data types via enums with payloads",
            "Traits as ad-hoc polymorphism (typeclasses done in OOP style)",
            "Async/await as escalation, not a fundamental feature",
        ],
        "design_dogmas": [
            "Memory safety is non-negotiable — the type system enforces it",
            "You never pay for what you don't use (zero-cost principle)",
            "Concurrency bugs are caught at compile time, not runtime",
            "Explicit is better than implicit (lifetimes are visible)",
            "Composition over inheritance — traits over classes",
        ],
        "anti_patterns": [
            "No garbage collector — memory is managed by the ownership system",
            "No null — use Option<T> explicitly",
            "No unchecked exceptions — use Result<T, E> for recoverable errors",
            "No inheritance-based polymorphism — use traits instead",
            "No reference cycles without Arc<Mutex<T>> — the compiler forbids them",
        ],
        "philosophical_twin": (
            "Stoicism — a philosophy of discipline, reason, and control. "
            "Rust demands you master its rules not to suffer from them, "
            "but to become truly fearless in what you build."
        ),
        "ethos_quote": (
            "The borrow checker is not a gatekeeper — it is a guide "
            "to the safest path through complexity."
        ),
    },
    "Go": {
        "guiding_motto": "Simple, reliable, efficient — at scale.",
        "philosophical_signature": (
            "Complexity is the enemy of reliability. "
            "Go's simplicity is a deliberate philosophical choice: "
            "one way to do things, expressed clearly and read once."
        ),
        "paradigm_fingerprint": [
            "Concurrent by design — goroutines + channels as first-class citizens",
            "CSP-inspired message passing (communicate, don't share memory)",
            "Interfaces as implicit contracts (no explicit declaration needed)",
            "defer for guaranteed resource cleanup",
            "Errors as values — handle them explicitly, don't suppress them",
        ],
        "design_dogmas": [
            "One way to do it — orthogonality over flexibility",
            "Fast compilation is a feature — never wait for the compiler",
            "Concurrency is cheap and built-in — use goroutines liberally",
            "Errors are values — handle them, don't panic for recoverable cases",
            "Pragmatism over theory — if it works and is readable, it's right",
        ],
        "anti_patterns": [
            "No generics until Go 1.18 — and still intentionally limited",
            "No inheritance — use composition and interfaces instead",
            "No exceptions — use error returns, not try/throw",
            "No operator overloading — no surprise arithmetic",
            "No try/catch — errors are return values, handled at call site",
        ],
        "philosophical_twin": (
            "Pragmatism (William James) — truth is what works, "
            "meaningful progress over perfect theory. "
            "Go was built by practitioners who got tired of waiting."
        ),
        "ethos_quote": (
            "Go doesn't ask you to learn a language — "
            "it asks you to write a program that humans can read."
        ),
    },
    "Swift": {
        "guiding_motto": "Safe, fast, expressive — without the legacy baggage.",
        "philosophical_signature": (
            "Protocols are the architecture; classes are a detail. "
            "Swift's protocol-oriented design means you're building behavior "
            "from the outside in — what you can do, not what you inherit."
        ),
        "paradigm_fingerprint": [
            "Protocol-oriented programming — behavior defined by protocols, not classes",
            "Value types by default — structs over classes where possible",
            "Optionals as explicit null — no nil without Optional",
            "Async/await for structured asynchronous programming",
            "Result builders for declarative domain-specific language construction",
        ],
        "design_dogmas": [
            "Safe by default — uninitialized variables don't exist",
            "Pure performance — compiles to native machine code",
            "Protocols over inheritance — composable, not hierarchical",
            "Memory-safe — ARC without manual retain/release",
            "Expressive syntax that reads like pseudocode",
        ],
        "anti_patterns": [
            "No nil without Optional — optional chaining is explicit",
            "No raw pointers — memory is managed by ARC",
            "No inheritance for shared behavior — use protocols",
            "No checked exceptions — use throws, handle at call site",
            "No implicit conversions — types are strict",
        ],
        "philosophical_twin": (
            "Humanism — the belief in human reason and potential. "
            "Swift was designed to free developers from the constraints "
            "of legacy systems, trusting them to build beautiful software."
        ),
        "ethos_quote": (
            "Swift code should read like poetry written for machines — "
            "elegant, precise, and understandable at first glance."
        ),
    },
    "Kotlin": {
        "guiding_motto": "Concise, safe, interoperable — pragmatic modern development.",
        "philosophical_signature": (
            "Pragmatism is the Kotlin philosophy. "
            "It takes the best ideas from Java, Scala, and Groovy "
            "and removes the ceremony — null safety, coroutines, extension functions — "
            "without requiring you to rewrite your entire Java codebase."
        ),
        "paradigm_fingerprint": [
            "Object-oriented with functional extensions (lambdas, higher-order functions)",
            "Coroutines for async — structured concurrency without callbacks",
            "Extension functions — add methods to existing classes without inheritance",
            "Smart casts — compiler tracks type narrowing within blocks",
            "Null safety at the type level — Nullable vs non-null distinguished",
        ],
        "design_dogmas": [
            "100% interoperable with Java — call Java from Kotlin, Kotlin from Java",
            "Pragmatism over purity — use whatever paradigm fits best",
            "Null safety is mandatory — the type system enforces it",
            "Conciseness — data classes, single-expression functions, type inference",
            "Coroutines for async — structured, not callback-based",
        ],
        "anti_patterns": [
            "No more NullPointerException — nullable types are explicit",
            "No checked exceptions — Kotlin doesn't have them",
            "No raw types — generics are always typed",
            "No checked exceptions — errors flow through Result type",
            "No operator overloading without explicit overloads",
        ],
        "philosophical_twin": (
            "Existentialism (Jean-Paul Sartre) — existence precedes essence. "
            "Kotlin says: don't wait for the perfect language. "
            "Build with what works, evolve as you go."
        ),
        "ethos_quote": (
            "Kotlin doesn't argue about programming paradigms — "
            "it asks: what do you need to build, and how can we help?"
        ),
    },
    "TypeScript": {
        "guiding_motto": "JavaScript that scales — types as living documentation.",
        "philosophical_signature": (
            "Types are documentation that the compiler verifies. "
            "They never lie, never go stale, and never need a comment. "
            "TypeScript's structural typing means compatibility is based on shape, not name."
        ),
        "paradigm_fingerprint": [
            "Static typing with optional type annotations (gradual typing)",
            "Structural typing — compatibility by shape, not nominal name",
            "Class-based OOP with interfaces, inheritance, access modifiers",
            "Generics with constraint support (parametric polymorphism)",
            "Decorators for meta-programming (stage 3 ES proposal)",
        ],
        "design_dogmas": [
            "Valid JavaScript is valid TypeScript — gradual adoption is the key",
            "Types are a superset of JavaScript — they erase at runtime",
            "Structural typing enables flexibility — shape defines compatibility",
            "Compiles to plain JavaScript (ES3+) — works in any browser",
            "The type system is Turing complete — compute at the type level",
        ],
        "anti_patterns": [
            "No any without explicit opt-in — use unknown for truly unknown types",
            "No runtime type checking (types erase) — types are compile-time only",
            "No nominal typing — structural typing means names don't matter",
            "No private fields without # prefix — use explicit access modifiers",
            "No undefined by default — strict null checks are recommended",
        ],
        "philosophical_twin": (
            "Empiricism — knowledge derived from experience and evidence. "
            "TypeScript trusts types as evidence of correctness, "
            "verified by the compiler (the empiricist's instrument)."
        ),
        "ethos_quote": (
            "TypeScript turns JavaScript's 'anything goes' into "
            "'show me the types, and I'll show you the bugs.'"
        ),
    },
    "JavaScript": {
        "guiding_motto": "The world's runtime — running everywhere, everything.",
        "philosophical_signature": (
            "JavaScript was written for humans, not machines. "
            "It prioritizes expressiveness over rigidity, "
            "functions as first-class values, and prototype inheritance "
            "over class hierarchies — a language that bends rather than breaks."
        ),
        "paradigm_fingerprint": [
            "Prototype-based OOP — objects inherit directly from other objects",
            "First-class functions — functions as values, passed around like data",
            "Dynamic typing — no compile-time enforcement",
            "Event loop with non-blocking I/O — single-threaded but async",
            "Closures as fundamental building blocks",
        ],
        "design_dogmas": [
            "Everything is an object (primitives are auto-boxed)",
            "Functions are values — stored, passed, returned, composed",
            "Prototype chain — inheritance without classes",
            "Dynamic typing — types resolved at runtime",
            "Event-driven, non-blocking — I/O doesn't block the thread",
        ],
        "anti_patterns": [
            "No static typing — rely on JSDoc or TypeScript for safety",
            "No block scoping with var — var is function-scoped, hoisted",
            "No class-based inheritance by default — use prototypes or ES6 classes",
            "No const enforcement for objects — const prevents reassignment, not mutation",
            "Avoid == (loose equality) — always use === (strict equality)",
        ],
        "philosophical_twin": (
            "Existentialism — freedom, choice, and responsibility for creating meaning. "
            "JavaScript gives you no safety nets, no enforced rules — "
            "you define your own structure, and own your own mistakes."
        ),
        "ethos_quote": (
            "JavaScript is the wild west of languages — no fences, "
            "but if you know what you're doing, you can build anything."
        ),
    },
    "Java": {
        "guiding_motto": "Write once, run anywhere — enterprise-trusted, platform-independent.",
        "philosophical_signature": (
            "The JVM is the great equalizer. "
            "Java's philosophy is simple: compile once to bytecode, "
            "run on any platform with a JVM. "
            "Strong typing and explicit contracts mean large teams can collaborate safely."
        ),
        "paradigm_fingerprint": [
            "Class-based OOP — everything is an object (except primitives)",
            "Strong static typing — no implicit narrowing casts",
            "JVM bytecode — platform independence via intermediate representation",
            "Checked exceptions — compiler enforces exception handling",
            "Multithreaded from day one — built-in concurrency support",
        ],
        "design_dogmas": [
            "Strong typing — if it compiles, types are consistent",
            "Platform independence — JVM as the universal runtime",
            "Checked exceptions — recoverable errors must be declared or caught",
            "No operator overloading — no surprise semantics",
            "Garbage collection — memory management is automatic",
        ],
        "anti_patterns": [
            "No checked exceptions in modern Java (deprecated in Java 21+)",
            "No multiple inheritance of classes — use interfaces instead",
            "No pointer arithmetic — no unsafe memory access",
            "No unsigned types (until Java 8+ for some) — integers are signed",
            "No struct types — everything is an object on the heap or stack as value",
        ],
        "philosophical_twin": (
            "Legalism (Han Feizi) — rules and structures create order. "
            "Java brought discipline to enterprise software, "
            "standardizing behavior across teams, codebases, and decades."
        ),
        "ethos_quote": (
            "Java doesn't care what you think you meant — "
            "it cares what you said. Compile first, trust the bytecode."
        ),
    },
    "C/C++": {
        "guiding_motto": "Trust the programmer — control everything, pay for only what you use.",
        "philosophical_signature": (
            "In C/C++, you are always in control. "
            "The compiler is a partner, not a babysitter. "
            "Zero-cost abstractions mean the compiler generates equivalent machine code — "
            "what you write is what runs. No hidden overhead, no surprises."
        ),
        "paradigm_fingerprint": [
            "Procedural programming (C) — you manage memory and control flow",
            "Object-oriented programming (C++) — classes, inheritance, RAII",
            "Template metaprogramming — Turing-complete compile-time computation",
            "Value semantics by default — heap allocation when you ask for it",
            "Move semantics (C++11+) — avoid unnecessary copies",
        ],
        "design_dogmas": [
            "You are in control — no safety nets unless you opt in",
            "Zero-cost abstractions — no runtime overhead for abstractions you don't use",
            "RAII (Resource Acquisition Is Initialization) — resource management via lifetimes",
            "Prefer value semantics — stack over heap unless necessary",
            "No hidden costs — if you didn't write it, it doesn't run",
        ],
        "anti_patterns": [
            "No bounds checking — buffer overflows are your problem",
            "No garbage collection — manual memory management via malloc/free or new/delete",
            "No runtime type safety — raw pointers are the default",
            "No safe array decay — pointer decay loses size information",
            "No guaranteed initialization — uninitialized variables contain garbage",
        ],
        "philosophical_twin": (
            "Epicureanism — mastery of pleasure requires discipline and control. "
            "C/C++ gives you the raw power to build anything, "
            "but demands deep understanding of what you're doing. "
            "Power without wisdom is destruction."
        ),
        "ethos_quote": (
            "C/C++ is the language of architects — "
            "you design every room, lay every brick, and own every crack."
        ),
    },
}


def ethos(language=None):
    """
    Main ethos function — distill a language's philosophical manifesto.

    Args:
        language: Optional. Language name. If None, reads current_index from
                  language_rotation.json and selects accordingly.

    Returns:
        A complete ethos card dict with motto, signature, paradigms, dogmas,
        anti-patterns, philosophical twin, and quote.
        Advances current_index in language_rotation.json.
    """
    config = load_rotation()
    languages = config["languages"]

    if language is None:
        idx = config["current_index"]
        language = languages[idx]
    elif language not in languages:
        raise ValueError(
            f"Language '{language}' not in rotation. "
            f"Available: {', '.join(languages)}"
        )

    data = ETHOS_DATA.get(language)
    if not data:
        raise ValueError(f"No ethos data for '{language}'")

    # Advance rotation
    idx = languages.index(language)
    next_idx = (idx + 1) % len(languages)
    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now().isoformat()
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "guiding_motto": data["guiding_motto"],
        "philosophical_signature": data["philosophical_signature"],
        "paradigm_fingerprint": data["paradigm_fingerprint"],
        "design_dogmas": data["design_dogmas"],
        "anti_patterns": data["anti_patterns"],
        "philosophical_twin": data["philosophical_twin"],
        "ethos_quote": data["ethos_quote"],
        "next_language": languages[next_idx],
        "rotation_order": languages,
        "timestamp": datetime.now().astimezone().isoformat(),
    }


def run_tests():
    """Run comprehensive tests for the Language Ethos module."""
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
            print(f"  ❌ FAIL: {msg}")

    def assert_true(a, msg=""):
        nonlocal tests_passed, tests_failed
        if a:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg}")

    print("Testing Language Ethos...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_eq(True, 0 <= config["current_index"] < 8, "current_index in valid range")

    print("  Testing ethos() for Rust...")
    result = ethos("Rust")
    expected_keys = [
        "tool", "version", "selected_language", "guiding_motto",
        "philosophical_signature", "paradigm_fingerprint", "design_dogmas",
        "anti_patterns", "philosophical_twin", "ethos_quote",
        "next_language", "rotation_order", "timestamp"
    ]
    for key in expected_keys:
        assert_eq(True, key in result, f"Key '{key}' present in response")

    assert_eq("Rust", result["selected_language"], "Rust is selected")
    assert_eq("Go", result["next_language"], "Next language is Go")
    assert_eq(TOOL_NAME, result["tool"], "Correct tool name")

    print("  Verifying motto and signature...")
    assert_true(len(result["guiding_motto"]) > 5, "guiding_motto is non-empty")
    assert_true(len(result["philosophical_signature"]) > 20, "philosophical_signature is substantial")
    assert_true(len(result["ethos_quote"]) > 10, "ethos_quote is meaningful")

    print("  Verifying paradigm_fingerprint structure...")
    pf = result["paradigm_fingerprint"]
    assert_true(isinstance(pf, list), "paradigm_fingerprint is a list")
    assert_true(len(pf) >= 4, f"paradigm_fingerprint has {len(pf)} entries (>= 4)")
    assert_true(all(isinstance(p, str) for p in pf), "all paradigm entries are strings")

    print("  Verifying design_dogmas structure...")
    dd = result["design_dogmas"]
    assert_true(isinstance(dd, list), "design_dogmas is a list")
    assert_true(len(dd) >= 4, f"design_dogmas has {len(dd)} entries (>= 4)")
    assert_true(all(isinstance(d, str) for d in dd), "all dogma entries are strings")

    print("  Verifying anti_patterns structure...")
    ap = result["anti_patterns"]
    assert_true(isinstance(ap, list), "anti_patterns is a list")
    assert_true(len(ap) >= 4, f"anti_patterns has {len(ap)} entries (>= 4)")
    assert_true(all(isinstance(a, str) for a in ap), "all anti-pattern entries are strings")

    print("  Verifying philosophical_twin...")
    twin = result["philosophical_twin"]
    assert_true(len(twin) > 20, "philosophical_twin is substantial")

    print("  Verifying Rust-specific content...")
    assert_true("ownership" in result["philosophical_signature"].lower() or "borrow" in result["philosophical_signature"].lower(), "Rust signature mentions ownership or borrowing")
    assert_true("fearless" in result["guiding_motto"].lower() or "zero-cost" in result["guiding_motto"].lower(), "Rust motto mentions core principles")
    assert_true("stoicism" in result["philosophical_twin"].lower() or "stoic" in result["philosophical_twin"].lower(), "Rust philosophical twin is stoicism")

    print("  Testing rotation update after ethos('Rust')...")
    config2 = load_rotation()
    assert_eq(1, config2["current_index"], "Index advanced to 1 (Go)")
    assert_eq("Rust", config2["last_language"], "Last language recorded as Rust")

    print("  Testing ethos() for Go (next in rotation)...")
    result2 = ethos("Go")
    assert_eq("Go", result2["selected_language"], "Go is selected")
    assert_eq("Swift", result2["next_language"], "Next language is Swift")
    assert_true("simplicity" in result2["guiding_motto"].lower() or "simple" in result2["guiding_motto"].lower(), "Go motto mentions simplicity")
    assert_true("pragmatism" in result2["philosophical_twin"].lower() or "pragmat" in result2["philosophical_twin"].lower(), "Go philosophical twin is pragmatism")

    print("  Testing all languages have complete ethos data...")
    for lang in config["languages"]:
        r = ethos(lang)
        assert_eq(lang, r["selected_language"], f"{lang} selected correctly")
        assert_true(len(r["guiding_motto"]) > 5, f"{lang} has non-empty motto")
        assert_true(len(r["philosophical_signature"]) > 20, f"{lang} has substantial signature")
        assert_true(len(r["paradigm_fingerprint"]) >= 4, f"{lang} has >= 4 paradigm entries")
        assert_true(len(r["design_dogmas"]) >= 4, f"{lang} has >= 4 design dogmas")
        assert_true(len(r["anti_patterns"]) >= 4, f"{lang} has >= 4 anti-patterns")
        assert_true(len(r["philosophical_twin"]) > 20, f"{lang} has substantial philosophical twin")
        assert_true(len(r["ethos_quote"]) > 10, f"{lang} has meaningful ethos quote")
        assert_eq(TOOL_NAME, r["tool"], f"{lang} tool name correct")
        assert_eq(TOOL_VERSION, r["version"], f"{lang} version correct")

    print("  Testing invalid language handling...")
    try:
        ethos("Python")
        tests_failed += 1
        print("  ❌ FAIL: No error raised for invalid language")
    except ValueError as e:
        tests_passed += 1
        print("  ✅ PASS: ValueError raised for invalid language")
        assert_in("not in rotation", str(e), "Error mentions rotation")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ FAIL: Wrong exception: {e}")

    print("  Testing rotation_order structure...")
    ro = result["rotation_order"]
    assert_true(isinstance(ro, list), "rotation_order is a list")
    assert_eq(8, len(ro), "rotation_order has 8 entries")
    assert_eq("Rust", ro[0], "Rust is first in rotation_order")
    assert_eq("C/C++", ro[-1], "C/C++ is last in rotation_order")

    print("  Verifying timestamp format...")
    ts = result["timestamp"]
    assert_true("T" in ts, "timestamp has ISO format with T separator")
    assert_true("+" in ts or "Z" in ts or (len(ts) > 20 and ts[-6:-5] in ["+", "-"]), "timestamp has timezone info")

    print("  Testing ethos() with None (auto-select from rotation)...")
    current_idx = load_rotation()["current_index"]
    current_lang = load_rotation()["languages"][current_idx]
    result_auto = ethos()
    assert_eq(current_lang, result_auto["selected_language"], f"Auto-selected language is correct (current_index={current_idx})")

    print(f"\n{'='*55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("⚡ All Ethos tests passed! Every language's soul has been distilled.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--ethos":
        language = sys.argv[2] if len(sys.argv) > 2 else None
        result = ethos(language)
        print(json.dumps(result, indent=2))
    else:
        print(f"Language Ethos v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m language_ethos --test        # Run tests")
        print("  python -m language_ethos --ethos [lang]  # Distill language ethos")
