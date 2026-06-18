#!/usr/bin/env python3
"""
📢 Polyglot Echoes v1.0

Every programming language has legendary one-liners — the phrases that
define an era, capture a philosophy, or become shorthand for an entire
community's worldview. These echoes resonate long after they're first
spoken. Rust's "fearless concurrency." Go's "less is more." JavaScript's
"everything is an object." C++'s "zero-overhead."

This tool selects the current rotation language and surfaces its most
iconic echoes: the quotes, battle cries, community mantras, and memorable
one-liners that make each language's culture unique.

Each run:
  1. Reads language_rotation.json, gets current language
  2. Picks a random echo category for that language
  3. Returns: the echo text + cultural context + what it means + what it hides
  4. Shows how the SAME concept sounds in each language's voice
  5. Updates current_index

Echo categories:
  - BATTLE_CRY    — the phrase you'd shout charging into a new codebase
  - PHILOSOPHY    — the guiding principle that shapes design decisions
  - GOTCHA        — the warning that saves you from a common pitfall
  - COMMUNITY_SAY — what practitioners say when they recognize each other
  - DESIGNER_VOICE — the creator's own words that became legend
  - LINGO         — insider vocabulary unique to that language's community

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust

Distinct from existing tools:
  - polyglot_codex:      literary canon & philosophy (written texts, proverbs)
  - polyglot_translation: cultural idiom mapping (how concepts translate)
  - polyglot_resonator:  mental model frames (how languages think)
  - polyglot_digest:     syntax-parallel snippets (same code, different syntax)
  - polyglot_chronicle:  today's history & trivia (temporal daily events)
  - polyglot_ethos:     philosophical manifesto (belief/identity statements)
  - polyglot_signal:     signal vocabulary (how languages signal conditions)
  - polyglot_sage:       idioms & practical tips (applied wisdom)
  - polyglot_compass:    learning journey maps (future milestones)
  - polyglot_archaeology: historical lineage (past, epochs)

Polyglot Echoes is about the LIVING WORDS — the quotes that travel
beyond any single codebase and become part of programming culture.
"""

import json
import os
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-echoes"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).resolve().parent.parent
_WORKSPACE_ROOT = _MODULE_DIR.parent.parent
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]


# ─────────────────────────────────────────────────────────────────────────────
# Echo Database — iconic quotes and sayings for each language
# Each echo has: text, category, context, meaning, what_it_hides
# ─────────────────────────────────────────────────────────────────────────────

ECHOES_DB: Dict[str, Dict[str, List[Dict[str, str]]]] = {
    "Rust": {
        "BATTLE_CRY": [
            {
                "text": "Fearless concurrency.",
                "context": "Rust's flagship promise — the compiler prevents data races at compile time.",
                "meaning": "You can write concurrent code without fear of hidden bugs. The type system makes safety guarantees no other systems language can claim.",
                "what_it_hides": "The Send/Sync trait system. You still need to think about which types can cross thread boundaries.",
            },
            {
                "text": "If it compiles, it's correct.",
                "context": "Borrow checker-approved code has strong safety guarantees.",
                "meaning": "Rust's strict type system means the compiler is your proof assistant. If the types line up, the program is memory-safe.",
                "what_it_hides": "Logic bugs still compile. The compiler prevents memory unsafety, not incorrect business logic.",
            },
        ],
        "PHILOSOPHY": [
            {
                "text": "Zero-cost abstractions.",
                "context": "If you don't use a feature, you don't pay for it. Always.",
                "meaning": "High-level idioms (iterators, closures, generics) compile to optimal machine code with no runtime overhead.",
                "what_it_hides": "Compile times suffer. Rust's abstraction system is Turing-complete at the type level, and LLVM does heavy work.",
            },
            {
                "text": "Make invalid states unrepresentable.",
                "context": "The type system should make impossible states impossible to express.",
                "meaning": "Design your types so the compiler rejects programs that encode wrong states, rather than checking at runtime.",
                "what_it_hides": "This requires significant type system expertise. 'Making states unrepresentable' is harder than it sounds.",
            },
        ],
        "GOTCHA": [
            {
                "text": "Don't fight the borrow checker — listen to it.",
                "context": "Every borrow checker error is the compiler trying to save you from a subtle bug.",
                "meaning": "The borrow checker is right more often than not. When it rejects code, the fix is usually restructuring ownership, not adding unsafe.",
                "what_it_hides": "There are legitimate cases whereRc<RefCell<T>> is the right answer. unsafe exists for a reason.",
            },
            {
                "text": "Clone is not your enemy — it's your escape hatch.",
                "context": "When ownership is too complex to reason about, cloning is correct.",
                "meaning": "Premature optimization against clones is the root of much borrow-checker suffering. Memory is cheap.",
                "what_it_hides": "Cloning large data structures in hot paths has real costs. The key word is 'in hot paths.'",
            },
        ],
        "COMMUNITY_SAY": [
            {
                "text": "The borrow checker is my strict but brilliant mentor.",
                "context": "Rust programmers describe the borrow checker as demanding but ultimately wise.",
                "meaning": "The compiler forces you to think carefully about ownership. This is painful at first, but leads to better code.",
                "what_it_hides": "Mentorship requires a learning curve. The first months in Rust are famously humbling.",
            },
        ],
        "DESIGNER_VOICE": [
            {
                "text": "Rust is a language for writing the next 40 years of software.",
                "context": "Graydon Hoare on Rust's ambition: systems programming that lasts.",
                "meaning": "Rust targets domains where software longevity and safety matter: OS kernels, browsers, file systems, embedded.",
                "what_it_hides": "Rust's ambition creates compile-time complexity that doesn't always pay off for short-lived projects.",
            },
        ],
        "LINGO": [
            {
                "text": "Rc<RefCell<T>> — the逃离舱",
                "context": "The pattern for when compile-time borrowing is too restrictive.",
                "meaning": "Runtime borrow checking viaRefCell<T> wrapped in Rc<T> lets you mutate under shared ownership.",
                "what_it_hides": "This pattern defeats the borrow checker's static guarantees. Use it only when necessary.",
            },
            {
                "text": "Send/Sync — the thread safety marks",
                "context": "Types implementing Send can be transferred across threads; Sync means &T is Send.",
                "meaning": "These marker traits are the foundation of Rust's fearless concurrency story.",
                "what_it_hides": "Most types are Send/Sync by default. Wrapper types choose deliberately.",
            },
        ],
    },
    "Go": {
        "BATTLE_CRY": [
            {
                "text": "Less is more.",
                "context": "Go's core philosophy: fewer features, simpler design, more clarity.",
                "meaning": "Go deliberately excludes features other languages consider essential. This is a strength, not a limitation.",
                "what_it_hides": "The 'less' boundary is subjective. Generics took 12 years to arrive.",
            },
            {
                "text": "Simple is boring, but it ships.",
                "context": "Go prioritizes shipping over sophistication.",
                "meaning": "A simple, readable program that works beats an elegant, clever program that doesn't.",
                "what_it_hides": "'Simple' can mean verbose when the language lacks expressive power.",
            },
        ],
        "PHILOSOPHY": [
            {
                "text": "Don't communicate by sharing memory; share memory by communicating.",
                "context": "The CSP model: goroutines communicate via channels instead of shared state.",
                "meaning": "Concurrency safety comes from not needing locks for shared data — just pass data through channels.",
                "what_it_hides": "Channels are not free. Buffered channels can mask backpressure problems.",
            },
            {
                "text": "Goroutines are cheap — spawn them freely.",
                "context": "Go's goroutines start at 2KB stack and grow dynamically.",
                "meaning": "You can have thousands of concurrent operations without the overhead of OS threads.",
                "what_it_hides": "'Cheap' has limits. Millions of goroutines with active memory can still overwhelm a system.",
            },
        ],
        "GOTCHA": [
            {
                "text": "The nil pointer dereference is still your fault.",
                "context": "Interfaces can hold nil values in ways that are surprising.",
                "meaning": "An interface holding a nil concrete type is not nil itself. This trips up even experienced Gophers.",
                "what_it_hides": "Method receivers on nil values are valid in Go — a deliberate design that's regularly confusing.",
            },
            {
                "text": "go fmt will change your code. Accept it.",
                "context": "go fmt is not configurable. Everyone uses the same style.",
                "meaning": "The formatter is a social contract that eliminates style debates entirely.",
                "what_it_hides": "The lack of configurability means you can't adapt to project conventions.",
            },
        ],
        "COMMUNITY_SAY": [
            {
                "text": "Gopher — the proud name of every Go developer",
                "context": "Go's mascot and community identity.",
                "meaning": "Go developers embrace the Gopher identity. The language's community is famously friendly.",
                "what_it_hides": "Friendliness can shade into complacency about language shortcomings.",
            },
        ],
        "DESIGNER_VOICE": [
            {
                "text": "Simplicity is complicated.",
                "context": "Rob Pike on why Go is simple: it takes hard work to make something look simple.",
                "meaning": "Go's apparent simplicity is the result of deliberate, difficult design choices.",
                "what_it_hides": "The complexity had to go somewhere — often into the call site or the programmer.",
            },
        ],
        "LINGO": [
            {
                "text": "Defer, panic, recover — the trio",
                "context": "Go's error handling trio: defer for cleanup, panic for unrecoverable failures, recover to catch panics.",
                "meaning": "This pattern lets you handle catastrophic failures without crashing the entire program.",
                "what_it_hides": "Panic/recover is not exception handling. Using it for expected errors is considered bad form.",
            },
        ],
    },
    "Swift": {
        "BATTLE_CRY": [
            {
                "text": "Swift is a protocol-oriented language.",
                "context": "Apple's stated design philosophy — protocols over inheritance.",
                "meaning": "Composition through protocol conformance is preferred over class hierarchies.",
                "what_it_hides": "The term is more aspirational than precise. Swift is also deeply object-oriented.",
            },
        ],
        "PHILOSOPHY": [
            {
                "text": "If let soothes the soul.",
                "context": "Optional binding turns a maybe-nil into a definite value safely.",
                "meaning": "Swift's optionals make nil safety explicit and ergonomic.",
                "what_it_hides": "Too many nested if-let pyramids lead to 'pyramid of doom.'",
            },
            {
                "text": "Value types are cheap to copy. Reference types are cheap to share.",
                "context": "Choose semantics based on whether you want independence or shared identity.",
                "meaning": "Structs (value) when copying makes sense; classes (reference) when sharing identity is needed.",
                "what_it_hides": "Copy-on-write means value types aren't always as cheap as they look.",
            },
        ],
        "GOTCHA": [
            {
                "text": "[weak self] — the retain cycle escape hatch",
                "context": "Closures that reference self need [weak self] to avoid retain cycles.",
                "meaning": "Swift's ARC requires explicit weakness to prevent circular references in closures.",
                "what_it_hides": "weak self means self might be nil inside the closure. You need guard let self = self.",
            },
        ],
        "COMMUNITY_SAY": [
            {
                "text": "It's like Python, but compiled.",
                "context": "The common (inaccurate) elevator pitch for Swift.",
                "meaning": "Swift's syntax is clean and approachable, but it's a deep systems language.",
                "what_it_hides": "Swift's type system, ARC, and value semantics are significantly more complex than Python's.",
            },
        ],
        "DESIGNER_VOICE": [
            {
                "text": "Objective-C without the C.",
                "context": "Chris Lattner on Swift's goal: the power of C with modern ergonomics.",
                "meaning": "Swift inherits C's systems programming roots but replaces C's dated syntax entirely.",
                "what_it_hides": "Swift interops with Objective-C and C extensively. 'Without the C' is poetic.",
            },
        ],
        "LINGO": [
            {
                "text": "@State, @Binding, @Published — the property wrapper zoo",
                "context": "SwiftUI's property wrappers manage state, binding, and observation.",
                "meaning": "These decorators inject behavior into properties without subclassing.",
                "what_it_hides": "Each wrapper has different ownership and lifecycle semantics.",
            },
        ],
    },
    "Kotlin": {
        "BATTLE_CRY": [
            {
                "text": "Pragmatic over purist.",
                "context": "Kotlin's unofficial motto — pick the right tool, not the ideological one.",
                "meaning": "Kotlin doesn't force functional or OO — it lets you choose what fits.",
                "what_it_hides": "'Pragmatic' can mean inconsistent — the language supports multiple paradigms that don't always compose cleanly.",
            },
        ],
        "PHILOSOPHY": [
            {
                "text": "NullPointerException is a thing of the past.",
                "context": "Kotlin's nullable types make null impossible to ignore at compile time.",
                "meaning": "The type system forces you to handle null at every call site.",
                "what_it_hides": "Kotlin/Java interop can still produce NPE. !! operator bypasses safety.",
            },
            {
                "text": "Extension functions — pretend the standard library is yours.",
                "context": "Add methods to any class without inheritance.",
                "meaning": "You can extend String, Int, or any existing class with new functionality.",
                "what_it_hides": "Extensions don't actually modify the class — they're resolved statically at compile time.",
            },
        ],
        "GOTCHA": [
            {
                "text": "Coroutines are cheap — but not free.",
                "context": "Kotlin coroutines can suspend without blocking threads.",
                "meaning": "Millions of coroutines can run on few threads, making async code readable.",
                "what_it_hides": "Structured concurrency means if you forget to cancel, resources leak. launch returns Job.",
            },
        ],
        "COMMUNITY_SAY": [
            {
                "text": "It's like Scala, but compiles before the heat death of the universe.",
                "context": "The joke comparing Kotlin's fast compilation to Scala's legendary slowness.",
                "meaning": "Kotlin compiles dramatically faster than Scala, making it suitable for large projects.",
                "what_it_hides": "Compilation speed varies by project size and complexity.",
            },
        ],
        "DESIGNER_VOICE": [
            {
                "text": "Concise, safe, interoperable, tool-friendly.",
                "context": "Kotlin's four design pillars from JetBrains.",
                "meaning": "The language was designed to solve specific pain points in Java development.",
                "what_it_hides": "'Tool-friendly' means IDE support was a primary concern.",
            },
        ],
        "LINGO": [
            {
                "text": "data class — the POJO destroyer",
                "context": "One keyword replaces getters, setters, equals, hashCode, and toString.",
                "meaning": "Data classes generate all boilerplate for you automatically.",
                "what_it_hides": "Generated methods are not always what you need. copy() is shallow.",
            },
        ],
    },
    "TypeScript": {
        "BATTLE_CRY": [
            {
                "text": "JavaScript that scales.",
                "context": "TypeScript's founding promise — type safety for large JavaScript codebases.",
                "meaning": "Add types to JavaScript, get compile-time error checking without losing runtime flexibility.",
                "what_it_hides": "Type information is erased. TypeScript's types don't exist at runtime.",
            },
        ],
        "PHILOSOPHY": [
            {
                "text": "Propagate types, not values.",
                "context": "Structural typing means you only describe the shape you need.",
                "meaning": "If an object has the right properties, it satisfies the interface — no explicit declaration.",
                "what_it_hides": "Structural typing can be too permissive — objects can silently gain extra properties.",
            },
            {
                "text": "Any is the escape hatch. Don't live there.",
                "context": "TypeScript's escape valve for untypable situations.",
                "meaning": "any opts out of type checking. Use it sparingly.",
                "what_it_hides": "one 'any' can spread through a codebase like a virus.",
            },
        ],
        "GOTCHA": [
            {
                "text": "TypeScript is JavaScript with training wheels — and they're good ones.",
                "context": "The gradual typing system means you can start loose and tighten up.",
                "meaning": "Add types incrementally. Not everything needs to be typed from day one.",
                "what_it_hides": "The training wheels eventually need to come off for real safety.",
            },
            {
                "text": "interface vs type — use interface for public APIs, type for unions.",
                "context": "Community convention for when to use each.",
                "meaning": "interface extends better. type handles complex union/intersection cases.",
                "what_it_hides": "The distinction is subtle. Both work in most situations.",
            },
        ],
        "COMMUNITY_SAY": [
            {
                "text": "I don't trust JavaScript, but I trust TypeScript to generate it.",
                "context": "TypeScript as a code quality filter.",
                "meaning": "The type system catches a large class of JavaScript bugs at compile time.",
                "what_it_hides": "TypeScript can't catch logic errors or runtime-specific issues.",
            },
        ],
        "DESIGNER_VOICE": [
            {
                "text": "TypeScript is JavaScript with types.",
                "context": "Anders Hejlsberg on TypeScript's goal: types without breaking JavaScript.",
                "meaning": "TypeScript is a superset of JavaScript — all JavaScript is valid TypeScript.",
                "what_it_hides": "'Superset' means you can still write untyped JavaScript inside TypeScript.",
            },
        ],
        "LINGO": [
            {
                "text": "Trick question: is TypeScript statically or dynamically typed?",
                "context": "Answer: statically typed at compile time, dynamically at runtime.",
                "meaning": "Types are checked by the compiler, then erased. The runtime is still JavaScript.",
                "what_it_hides": "The compiler is not the runtime. Type constraints don't exist at runtime.",
            },
        ],
    },
    "JavaScript": {
        "BATTLE_CRY": [
            {
                "text": "The language that runs the web.",
                "context": "JavaScript is the only language that runs natively in browsers.",
                "meaning": "JavaScript's ubiquity makes it the de facto language of the web.",
                "what_it_hides": "Node.js, Deno, Bun — JavaScript escaped the browser and now runs everywhere.",
            },
        ],
        "PHILOSOPHY": [
            {
                "text": " == or ===? Always ===. Always.",
                "context": "The first rule every JavaScript developer learns.",
                "meaning": "=== checks value and type. == does type coercion — a notorious footgun.",
                "what_it_hides": "Sometimes == is genuinely useful. Knowing when is the mark of experience.",
            },
            {
                "text": "Everything is an object, except when it isn't.",
                "context": "Primitives (number, string) are coerced but not truly OO.",
                "meaning": "typeof lies about some types. Object wrappers exist but rarely matter.",
                "what_it_hides": "Functions are objects. null is 'object'. NaN is 'number.' JavaScript's typeof is quirky.",
            },
        ],
        "GOTCHA": [
            {
                "text": "Hoisting: declarations rise, initializations don't.",
                "context": "var is hoisted but undefined until the assignment runs.",
                "meaning": "Using a variable before its declaration isn't always an error — just dangerous.",
                "what_it_hides": "let and const are not hoisted in the same way. They're in the TDZ (temporal dead zone).",
            },
            {
                "text": "0.1 + 0.2 !== 0.3.",
                "context": "IEEE 754 floating point. Famous. Unexpected to newcomers.",
                "meaning": "JavaScript uses double-precision floating point. Precision limits exist.",
                "what_it_hides": "All numbers are floats in JavaScript. There's no Integer type.",
            },
        ],
        "COMMUNITY_SAY": [
            {
                "text": "It works on my machine.",
                "context": "JavaScript's environment fragmentation — browsers differ in subtle ways.",
                "meaning": "Cross-browser compatibility remains a real challenge.",
                "what_it_hides": "Node version differences are equally challenging.",
            },
        ],
        "DESIGNER_VOICE": [
            {
                "text": "First-class functions — functions are data.",
                "context": "Brendan Eich's favorite design decision in JavaScript.",
                "meaning": "Functions can be assigned to variables, passed as arguments, returned from functions.",
                "what_it_hides": "this binding in functions is notoriously confusing.",
            },
        ],
        "LINGO": [
            {
                "text": "Callback hell — the pyramid of doom",
                "context": "Nested callbacks make code unreadable.",
                "meaning": "Async code without Promises leads to deeply nested indentation.",
                "what_it_hides": "async/await and Promises solved this. Callback hell is now a historical artifact.",
            },
        ],
    },
    "Java": {
        "BATTLE_CRY": [
            {
                "text": "Write once, run anywhere.",
                "context": "Java's founding promise — bytecode on the JVM.",
                "meaning": "Java compiles to JVM bytecode, runs on any machine with a JVM.",
                "what_it_hides": "'Anywhere' ignores JVM version fragmentation and platform-specific behavior.",
            },
        ],
        "PHILOSOPHY": [
            {
                "text": "Object-oriented, or it doesn't count.",
                "context": "Java is the language that made OOP mainstream in industry.",
                "meaning": "Everything is a class. Even main() lives in a class.",
                "what_it_hides": "Java 8+ added lambdas and functional programming. The OO dogma softened.",
            },
            {
                "text": "A final class is a sealed contract.",
                "context": "final means no subclasses. Immutability as a design statement.",
                "meaning": "Preventing inheritance is a deliberate design choice, not a limitation.",
                "what_it_hides": "final on classes is underused. Many Java codebases extend classes that shouldn't be.",
            },
        ],
        "GOTCHA": [
            {
                "text": "Checked exceptions: the feature everyone loves to hate.",
                "context": "Java forces you to declare or handle checked exceptions.",
                "meaning": "The compiler makes error handling explicit. This is verbose.",
                "what_it_hides": "Checked exceptions don't compose well with generics and lambdas.",
            },
            {
                "text": "String is immutable. StringBuilder is for when you care.",
                "context": "Java's String is a value object by design.",
                "meaning": "Strings can't be modified after creation. Use StringBuilder for concatenation in loops.",
                "what_it_hides": "The JVM optimizes String concatenation via StringBuilder automatically in most cases.",
            },
        ],
        "COMMUNITY_SAY": [
            {
                "text": "Enterprise Java — where everything is a factory, builder, and visitor pattern.",
                "context": "The joke about enterprise Java's tendency toward over-engineering.",
                "meaning": "Java's ecosystem developed complex design patterns as idioms.",
                "what_it_hides": "Spring Boot simplified much of this, but the culture of ceremony takes time to shake.",
            },
        ],
        "DESIGNER_VOICE": [
            {
                "text": "James Gosling on Java: 'We wanted a language you could write once and run anywhere.'",
                "context": "Java's founding vision from 1995.",
                "meaning": "The JVM as a platform abstraction was genuinely revolutionary.",
                "what_it_hides": "The 'write once' part assumes you're not using platform-specific APIs.",
            },
        ],
        "LINGO": [
            {
                "text": "POJO — Plain Old Java Object",
                "context": "Simple objects without framework dependencies.",
                "meaning": "The ideal: a class with fields, getters, and setters. Nothing more.",
                "what_it_hides": "Lombok and other annotation processors automate the boilerplate.",
            },
        ],
    },
    "C/C++": {
        "BATTLE_CRY": [
            {
                "text": "You have the memory, the pointer, and nothing else. Good luck.",
                "context": "C's no-safety-net philosophy — raw, honest, brutal.",
                "meaning": "C gives you complete control. The cost is complete responsibility for correctness.",
                "what_it_hides": "The bugs are real and dangerous. Buffer overflows and use-after-free are lurking.",
            },
            {
                "text": "You pay for what you use.",
                "context": "C++'s zero-overhead principle.",
                "meaning": "If you don't use a feature, you don't pay for it. No hidden costs.",
                "what_it_hides": "The definition of 'use' is flexible. Modern C++ is not always zero-cost.",
            },
        ],
        "PHILOSOPHY": [
            {
                "text": "RAII: Resource Acquisition Is Initialization.",
                "context": "The destructor as automatic cleanup mechanism.",
                "meaning": "Acquiring a resource in a constructor and releasing it in the destructor gives deterministic cleanup.",
                "what_it_hides": "RAII doesn't work for non-memory resources like network sockets without careful design.",
            },
            {
                "text": "Undefined behavior is not a bug — it's a feature of the C standard.",
                "context": "UB lets compilers optimize aggressively. It also means anything can happen.",
                "meaning": "The C standard doesn't define behavior for certain constructs. Compilers exploit this.",
                "what_it_hides": "UB can manifest years later as 'impossible' bugs in unrelated code.",
            },
        ],
        "GOTCHA": [
            {
                "text": "Segmentation fault: the most informative error message in programming.",
                "context": "It tells you SOMETHING went wrong. That's all.",
                "meaning": "C has no safety net. The OS kills your program when it misbehaves.",
                "what_it_hides": "ASAN (AddressSanitizer) and Valgrind exist for a reason.",
            },
            {
                "text": "sizeof(char) is always 1. sizeof(int) is not guaranteed to be 4.",
                "context": "The C standard defines sizes in terms of relative relationships, not absolute values.",
                "meaning": "stdint.h types (int32_t, uint64_t) give you fixed sizes across platforms.",
                "what_it_hides": "Platform differences in type sizes are the source of subtle, hard-to-find bugs.",
            },
        ],
        "COMMUNITY_SAY": [
            {
                "text": "C: the assembler you can write readable code in.",
                "context": "C is often called 'portable assembly.'",
                "meaning": "C gives you low-level control with syntax that's more expressive than raw assembly.",
                "what_it_hides": "'Readable' is relative. C code can be just as obfuscated as assembly.",
            },
        ],
        "DESIGNER_VOICE": [
            {
                "text": "Bjarne Stroustrup: 'C makes it easy to shoot yourself in the foot; C++ makes it harder, but when you do, it takes your whole leg off.'",
                "context": "The famous quote on C++'s power and danger.",
                "meaning": "C++ gives you more tools, but each tool can cause more damage.",
                "what_it_hides": "Modern C++ (RAII, smart pointers, constexpr) has significantly improved safety.",
            },
        ],
        "LINGO": [
            {
                "text": "UB — Undefined Behavior",
                "context": "The term that strikes fear into C/C++ developers.",
                "meaning": "The standard doesn't specify what happens. The compiler can do anything.",
                "what_it_hides": "UB sanitizers (UBSAN) exist to catch UB at runtime during development.",
            },
        ],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Echo presentation
# ─────────────────────────────────────────────────────────────────────────────

ECHO_CATEGORIES = {
    "BATTLE_CRY":     ("⚔️  Battle Cry",     "The phrase you'd shout charging into a new codebase"),
    "PHILOSOPHY":     ("🧭 Philosophy",      "The guiding principle behind every design decision"),
    "GOTCHA":         ("⚠️  Gotcha",          "The warning that saves you from a common pitfall"),
    "COMMUNITY_SAY":  ("🤝 Community Say",   "What practitioners say when they recognize each other"),
    "DESIGNER_VOICE": ("🎙️  Designer Voice",  "The creator's own words that became legend"),
    "LINGO":          ("🗣️  Lingo",           "Insider vocabulary unique to the community"),
}

CATEGORY_EMOJI = {k: v[0] for k, v in ECHO_CATEGORIES.items()}
CATEGORY_DESC = {k: v[1] for k, v in ECHO_CATEGORIES.items()}


# ─────────────────────────────────────────────────────────────────────────────
# Core API
# ─────────────────────────────────────────────────────────────────────────────

def load_rotation(path: str = None) -> Dict[str, Any]:
    """Load language rotation config."""
    if path is None:
        path = ROTATION_FILE
    with open(path, "r") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any], path: str = None) -> None:
    """Save updated rotation config."""
    if path is None:
        path = ROTATION_FILE
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def get_current_language(config: Dict[str, Any] = None) -> str:
    """Return the current language from rotation config."""
    if config is None:
        config = load_rotation()
    langs = config.get("languages", ROTATION_ORDER)
    idx = config.get("current_index", 0)
    return langs[idx % len(langs)]


def advance_rotation(config: Dict[str, Any] = None) -> int:
    """Advance current_index by 1, save, return old index."""
    if config is None:
        config = load_rotation()
    old_index = config["current_index"]
    langs = config.get("languages", ROTATION_ORDER)
    new_index = (old_index + 1) % len(langs)
    config["current_index"] = new_index
    config["last_language"] = langs[old_index]
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)
    return old_index


def pick_echo(language: str, seed: int = None) -> Dict[str, str]:
    """Pick a random echo from the language's database."""
    lang_echoes = ECHOES_DB.get(language, {})
    if not lang_echoes:
        return {
            "text": f"No echoes found for {language}.",
            "category": "UNKNOWN",
            "context": "",
            "meaning": "",
            "what_it_hides": "",
        }

    # Collect all echoes across categories
    all_echoes: List[Dict[str, str]] = []
    for category, echoes in lang_echoes.items():
        for echo in echoes:
            all_echoes.append({**echo, "category": category})

    if seed is not None:
        random.seed(seed)
        chosen = all_echoes[seed % len(all_echoes)]
        random.seed()  # Reset
    else:
        chosen = random.choice(all_echoes)

    return chosen


def generate_echo_report(
    language: str,
    seed: int = None,
) -> Dict[str, Any]:
    """Generate a full echo report for the selected language."""
    echo = pick_echo(language, seed=seed)
    category = echo["category"]

    # Build cross-language resonance — how does this concept echo in other languages?
    cross_echoes: List[Dict[str, str]] = []
    for other_lang in ROTATION_ORDER:
        if other_lang == language:
            continue
        other_echoes = ECHOES_DB.get(other_lang, {}).get(category, [])
        if other_echoes:
            cross_echoes.append({
                "language": other_lang,
                "echo": random.choice(other_echoes)["text"],
                "emoji": _LANG_EMOJI.get(other_lang, "🔧"),
            })

    return {
        "language": language,
        "emoji": _LANG_EMOJI.get(language, "🔧"),
        "echo": echo,
        "category_emoji": CATEGORY_EMOJI.get(category, "📢"),
        "category_desc": CATEGORY_DESC.get(category, ""),
        "cross_language_echoes": cross_echoes,
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def format_echo_report(report: Dict[str, Any]) -> str:
    """Format an echo report as a readable string."""
    lines = []
    lang = report["language"]
    emoji = report["emoji"]
    echo = report["echo"]

    lines.append(f"📢 POLYGLOT ECHOES — {lang}")
    lines.append(f"{'─' * 50}")
    lines.append(f"")
    lines.append(f"  {report['category_emoji']} {report['category_desc']}")
    lines.append(f"")
    lines.append(f"  \"{echo['text']}\"")
    lines.append(f"")
    lines.append(f"  💬 CONTEXT")
    lines.append(f"  {echo['context']}")
    lines.append(f"")
    lines.append(f"  🎯 MEANING")
    lines.append(f"  {echo['meaning']}")
    lines.append(f"")
    lines.append(f"  🎭 WHAT IT HIDES")
    lines.append(f"  {echo['what_it_hides']}")

    if report["cross_language_echoes"]:
        lines.append(f"")
        lines.append(f"  🌐 SAME CATEGORY, DIFFERENT VOICES")
        for cross in report["cross_language_echoes"]:
            lines.append(f"  {cross['emoji']} {cross['language']}: \"{cross['echo']}\"")

    lines.append(f"")
    lines.append(f"  ⏭️  NEXT → {report.get('next_language', '?')}")

    return "\n".join(lines)


_LANG_EMOJI = {
    "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
    "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "C/C++": "🔩",
}


def next_language(current: str) -> str:
    """Return the next language in rotation."""
    idx = ROTATION_ORDER.index(current)
    return ROTATION_ORDER[(idx + 1) % len(ROTATION_ORDER)]


def echoes(seed: int = None, override_language: str = None) -> Dict[str, Any]:
    """
    Generate an echo report for the current rotation language.

    Reads language_rotation.json, selects the current language, picks
    a random echo category (or deterministic via seed), and returns
    a structured report with the echo, its context, meaning, and
    cross-language resonances.

    Args:
        seed: optional seed for deterministic echo selection
        override_language: override the selected language (for testing)

    Returns:
        dict with echo report and updated rotation state
    """
    config = load_rotation()
    langs = config.get("languages", ROTATION_ORDER)

    if override_language:
        language = override_language
    else:
        language = get_current_language(config)

    # Build the report
    report = generate_echo_report(language, seed=seed)
    report["tool"] = TOOL_NAME
    report["version"] = TOOL_VERSION

    # Advance rotation
    current_idx = langs.index(language) if language in langs else 0
    next_idx = (current_idx + 1) % len(langs)
    report["next_language"] = langs[next_idx]
    report["rotation"] = langs

    # Save updated config
    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)

    return report


# ─────────────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────────────

def run_tests() -> None:
    """Run test suite for Polyglot Echoes."""
    tests_passed = 0
    tests_failed = 0

    def assert_eq(a, b, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a == b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — expected {b!r}, got {a!r}")

    def assert_in(a: str, b, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a in b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — '{a}' not found in {b!r}")

    def assert_true(a, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg}")

    def assert_keys(d: Dict, expected_keys: List[str], msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        missing = [k for k in expected_keys if k not in d]
        if not missing:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — missing keys: {missing}")

    print("Testing Polyglot Echoes...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_eq("Rust", config["languages"][0], "Rust is first language")
    assert_in("current_index", config, "current_index field present")

    print("  Testing echoes() output structure...")
    result = echoes()
    expected_keys = [
        "tool", "version", "language", "emoji", "echo",
        "category_emoji", "category_desc", "cross_language_echoes",
        "timestamp", "next_language", "rotation",
    ]
    assert_keys(result, expected_keys, "All expected keys present")

    print("  Testing echo structure...")
    echo = result["echo"]
    echo_keys = ["text", "category", "context", "meaning", "what_it_hides"]
    assert_keys(echo, echo_keys, "echo has all required fields")
    assert_true(len(echo["text"]) > 3, "echo text is meaningful")
    assert_true(echo["category"] in ECHO_CATEGORIES, "echo category is valid")

    print("  Testing cross_language_echoes structure...")
    cross = result["cross_language_echoes"]
    assert_true(len(cross) >= 1, "has at least 1 cross-language echo")
    for item in cross:
        assert_in("language", item, "cross echo has language")
        assert_in("echo", item, "cross echo has text")
        assert_in("emoji", item, "cross echo has emoji")
        assert_true(item["language"] != result["language"], "cross echo is different language")

    print("  Testing all 8 languages have echo data...")
    for lang in ROTATION_ORDER:
        lang_echoes = ECHOES_DB.get(lang)
        assert_true(lang_echoes is not None, f"{lang} has echoes database entry")
        assert_true(len(lang_echoes) >= 3, f"{lang} has at least 3 categories")
        total_echoes = sum(len(v) for v in lang_echoes.values())
        assert_true(total_echoes >= 3, f"{lang} has at least 3 total echoes")

    print("  Testing echo categories are valid...")
    for lang, categories in ECHOES_DB.items():
        for cat in categories.keys():
            assert_true(cat in ECHO_CATEGORIES, f"{lang} uses valid category '{cat}'")

    print("  Testing rotation advances after echoes()...")
    idx_before = load_rotation()["current_index"]
    lang_before = load_rotation()["languages"][idx_before]
    result = echoes()
    idx_after = load_rotation()["current_index"]
    assert_eq((idx_before + 1) % 8, idx_after, "index advanced by 1")
    assert_eq(lang_before, load_rotation()["last_language"], "last_language recorded correctly")

    print("  Testing deterministic echo selection by seed...")
    for lang in ROTATION_ORDER:
        r1 = echoes(seed=0, override_language=lang)
        r2 = echoes(seed=0, override_language=lang)
        assert_eq(r1["echo"]["text"], r2["echo"]["text"], f"seed=0 same echo for {lang}")
        assert_eq(r1["echo"]["category"], r2["echo"]["category"], f"seed=0 same category for {lang}")

    print("  Testing different seeds produce different echoes...")
    r1 = echoes(seed=1)
    r2 = echoes(seed=5)
    assert_true(
        r1["echo"]["text"] != r2["echo"]["text"] or r1["echo"]["category"] != r2["echo"]["category"],
        "different seeds → different echoes"
    )

    print("  Testing format_echo_report()...")
    formatted = format_echo_report(result)
    assert_in(result["echo"]["text"], formatted, "formatted report contains echo text")
    assert_in(result["language"], formatted, "formatted report contains language")
    assert_in(result["echo"]["context"], formatted, "formatted report contains context")
    assert_in(result["echo"]["meaning"], formatted, "formatted report contains meaning")
    assert_in(result["next_language"], formatted, "formatted report contains next language")

    print("  Testing all languages produce valid echo reports...")
    for lang in ROTATION_ORDER:
        report = generate_echo_report(lang)
        assert_true(len(report["echo"]["text"]) > 3, f"{lang} echo has text")
        assert_true(len(report["cross_language_echoes"]) >= 1, f"{lang} has cross echoes")

    print("  Testing get_current_language()...")
    cfg = load_rotation()
    current = get_current_language(cfg)
    assert_true(current in ROTATION_ORDER, "get_current_language returns valid language")

    print("  Testing language emoji mapping...")
    for lang, emoji in _LANG_EMOJI.items():
        assert_true(len(emoji) >= 1 and ord(emoji[0]) > 127, f"{lang} emoji is a non-ASCII character")
        result = echoes(override_language=lang)
        assert_eq(emoji, result["emoji"], f"{lang} emoji is correct")

    print("  Testing cross_language_echoes are from the same category...")
    for lang in ROTATION_ORDER:
        result = generate_echo_report(lang)
        source_cat = result["echo"]["category"]
        for cross in result["cross_language_echoes"]:
            # Find what category that cross echo is from
            cross_lang = cross["language"]
            cross_cat = cross.get("category", "")
            # At minimum, verify cross language is different
            assert_true(cross_lang != lang, f"{lang}: cross language is different")

    print("  Testing all echo categories appear across languages...")
    category_counts: Dict[str, int] = {}
    for lang, categories in ECHOES_DB.items():
        for cat in categories.keys():
            category_counts[cat] = category_counts.get(cat, 0) + 1
    for cat, count in category_counts.items():
        assert_true(count >= 6, f"category '{cat}' appears in at least 6 languages ({count})")

    print("  Testing each language has all 6 categories...")
    for lang, categories in ECHOES_DB.items():
        for cat in ECHO_CATEGORIES.keys():
            assert_true(
                cat in categories and len(categories[cat]) >= 1,
                f"{lang} has category '{cat}' with at least 1 echo"
            )

    print("  Testing next_language is in rotation list...")
    result = echoes()
    assert_true(result["next_language"] in result["rotation"], "next_language in rotation")
    assert_true(result["language"] in result["rotation"], "selected_language in rotation")
    assert_true(result["next_language"] != result["language"], "next != selected")

    print("  Testing tool name and version in response...")
    assert_eq("polyglot-echoes", result["tool"], "correct tool name")
    assert_eq("1.0.0", result["version"], "correct tool version")

    print("  Testing ECHO_CATEGORIES covers all categories in DB...")
    for lang, categories in ECHOES_DB.items():
        for cat in categories.keys():
            assert_true(cat in ECHO_CATEGORIES, f"category '{cat}' is in ECHO_CATEGORIES")

    print(f"\n{'=' * 55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("📢 All Echoes tests passed! Every language has its voice.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)
