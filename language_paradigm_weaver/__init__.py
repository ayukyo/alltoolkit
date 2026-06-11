#!/usr/bin/env python3
"""
🕸️ Language Paradigm Weaver v1.0

A creative tool that exposes the hidden paradigm assumptions in each language —
the unstated "world view" each language embeds in its syntax, type system,
and standard library design.

For the selected rotation language, this tool:
  1. Identifies the language's dominant paradigm (OOP, functional, procedural, multi-paradigm)
  2. Reveals the paradigm's hidden assumptions — what it makes easy, what it makes hard
  3. Shows how the same code would look in each paradigm the language supports
  4. Generates a "paradigm tension map" — where the language fights against itself
  5. Provides a paradigm fitness recommendation: when this language IS the right tool

Creative concept: "Every language has a worldview baked into its syntax.
This tool maps the invisible assumptions — and shows where paradigms clash."

Distinct from existing tools:
  - polyglot_bridges:     problem→solution semantic maps (WHAT each language does)
  - polyglot_resonator:   mental model frames (HOW each language thinks)
  - polyglot_dna:         genetic trait mapping (WHAT traits each has)
  - polyglot_chronicle:   daily history/challenge (temporal today)
  - polyglot_digest:      syntax-parallel snippets (same code, different syntax)
  - polyglot_wire:        FFI and interop (cross-language wire)
  - language_compass:    learning journey maps (milestones, stages)
  - language_archaeology: historical lineage (temporal depth)
  - language_synapse:    conceptual bridges between concepts
  - language_ethos:      philosophical manifesto (belief/identity)
  - language_sage:       idioms, tips, pitfalls (practical wisdom)
  - language_ecohub:     package ecosystem guide (tooling)

Paradigm Weaver is about PARADIGM ASSUMPTIONS — the invisible worldview
each language carries, and where paradigm clashes create friction.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

TOOL_NAME = "language-paradigm-weaver"
TOOL_VERSION = "1.0.0"

# The 8 languages this tool manages — matches the rotation order
TOOL_LANGUAGES = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]

ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
    "language_rotation.json"
)


def load_rotation():
    """Load language rotation config."""
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data):
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Paradigm definitions ───────────────────────────────────────────────────────
PARADIGMS = {
    "procedural": {
        "name": "Procedural",
        "emoji": "📋",
        "description": "Code as a sequence of statements that mutate state. Think: C, early Fortran.",
        "core_idea": "Do this, then do that, then do this.",
        "hidden_assumptions": [
            "Sequential execution is the natural order",
            "Global state is acceptable",
            "Mutation is the primary way to model change",
            "Side effects are normal and expected",
        ],
        "makes_easy": ["Step-by-step algorithms", "Direct hardware access", "Simple scripts"],
        "makes_hard": ["Concurrency", "Reasoning about state", "Large-scale composition"],
    },
    "object_oriented": {
        "name": "Object-Oriented",
        "emoji": "🎭",
        "description": "Code organized around objects that bundle state and behavior. Think: Java, Python.",
        "core_idea": "Objects send messages to each other.",
        "hidden_assumptions": [
            "Everything is an object (or should be)",
            "Inheritance is a good reuse mechanism",
            "Encapsulation is the primary decomposition unit",
            "Methods belong to classes",
        ],
        "makes_easy": ["Modeling real-world entities", "Inheritance hierarchies", "Polymorphism via interfaces"],
        "makes_hard": ["Concurrency", "Composition over inheritance", "First-class functions"],
    },
    "functional": {
        "name": "Functional",
        "emoji": "λ",
        "description": "Code as composition of pure functions with no side effects. Think: Haskell, Lisp.",
        "core_idea": "Given X, always produce Y. No mutation, no surprises.",
        "hidden_assumptions": [
            "Immutability is the default",
            "Functions are values",
            "Composition is preferred over inheritance",
            "Side effects should be explicit (monads)",
        ],
        "makes_easy": ["Concurrency", "Reasoning about code", "Parallel computation"],
        "makes_hard": ["I/O", "State that changes", "Debugging lazy evaluation"],
    },
    "multi_paradigm": {
        "name": "Multi-Paradigm",
        "emoji": "🔀",
        "description": "Language supports multiple paradigms without mandating any. Think: Python, JavaScript.",
        "core_idea": "Pick the right tool for the job — the language won't stop you.",
        "hidden_assumptions": [
            "No single 'right' way to solve problems",
            "Programmer knows best",
            "Pragmatism over purity",
            "Paradigm choice is a project-level decision",
        ],
        "makes_easy": ["Rapid prototyping", "Incremental adoption of new patterns", "Team autonomy"],
        "makes_hard": ["Enforcing consistency", "Onboarding new developers", "Large-scale architecture"],
    },
    "actor_based": {
        "name": "Actor-Based",
        "emoji": "🎪",
        "description": "Computation via isolated actors that communicate via message passing. Think: Erlang, Elixir.",
        "core_idea": "Everything is an actor. Mailbox inbox. Process mail. Send mail.",
        "hidden_assumptions": [
            "Isolation is the primary unit of reliability",
            "Message passing is safer than shared memory",
            "Failure is normal, not exceptional",
            "Supervision hierarchies handle errors",
        ],
        "makes_easy": ["Fault tolerance", "Distributed systems", "Concurrency without locks"],
        "makes_hard": ["Debugging race conditions", "Transactions across actors", "Type-safe message contracts"],
    },
    "systems": {
        "name": "Systems",
        "emoji": "⚙️",
        "description": "Low-level control over memory, threads, and hardware. Think: Rust, C.",
        "core_idea": "You are in charge. The language gives you power and expects responsibility.",
        "hidden_assumptions": [
            "Programmer is always right (no safety net)",
            "Performance is paramount",
            "Memory layout is your responsibility",
            "Undefined behavior is acceptable if you know what you're doing",
        ],
        "makes_easy": ["Maximum performance", "Direct hardware access", "Predictable memory usage"],
        "makes_hard": ["Productivity", "Safety", "Concurrency without data races"],
    },
    "concurrent": {
        "name": "Concurrent",
        "emoji": "⚡",
        "description": "Built-in concurrency primitives as a core language feature. Think: Go goroutines, Erlang actors.",
        "core_idea": "Concurrency is a first-class citizen, not an afterthought.",
        "hidden_assumptions": [
            "Concurrency should be cheap and abundant",
            "Message passing is safer than shared memory",
            "Parallelism is the default for I/O-bound tasks",
            "Goroutines/actors are the unit of concurrency",
        ],
        "makes_easy": ["Network servers", "I/O-bound parallelism", "Highly concurrent services"],
        "makes_hard": ["CPU-bound parallelism", "Debugging race conditions", "Deterministic testing"],
    },
}

# ── Language paradigm profiles ───────────────────────────────────────────────
LANGUAGE_PROFILES: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "primary_paradigm": "systems",
        "secondary_paradigms": ["functional"],
        "dominant_ideology": "Safety without garbage collection. Power without undefined behavior.",
        "paradigm_tension": [
            {
                "tension": "Ownership (systems) vs. Borrow Checking (runtime safety)",
                "description": "Rust has a systems-level view of memory but a Haskell-style borrow checker. The borrow checker is compile-time-only — but ownership IS runtime behavior (destructors).",
                "where_it_fires": "When you need shared mutation across threads — Arc<Mutex<T>> is the escape hatch, and it's verbose.",
                "verdict": "Rust wins — the tension is productive. Ownership enforces correctness, borrow checker enforces safety.",
            },
            {
                "tension": "Zero-cost abstractions (systems) vs. High-level ergonomics (functional)",
                "description": "Rust's iterators, closures, and Option/Result are zero-cost abstractions — but they require learning a new mental model for loops (for vs. iterators).",
                "where_it_fires": "When a Rustacean coming from Python tries to use a for loop instead of .map().filter().sum() — and gets told to use iterators for performance.",
                "verdict": "Rust wins — zero-cost abstractions are the point. The ergonomics are the price.",
            },
            {
                "tension": "Pattern matching (functional) vs. Exhaustiveness checking (OOP-adjacent)",
                "description": "Rust's match is algebraic (like Haskell) but also enforces exhaustiveness (like a type checker). This means adding a new enum variant BREAKS all match arms.",
                "where_it_fires": "When adding a new language feature (new enum variant), the compiler forces you to handle all cases — which is good, but requires updating ALL match statements.",
                "verdict": "Rust wins — exhaustiveness is a feature, not a bug. The breakage is compile-time safety.",
            },
        ],
        "hidden_assumptions": [
            "You care about memory layout",
            "You want the compiler to prove your code is safe",
            "Runtime costs should be visible in the code (no hidden GC)",
            "Fearless concurrency is achievable",
        ],
        "what_it_makes_easy": [
            "Fearless concurrency (data race prevention at compile time)",
            "Zero-cost abstractions",
            "Deterministic resource cleanup (RAII)",
            "Writing correct code by construction",
        ],
        "what_it_makes_hard": [
            "Shared mutable state across threads",
            "Rapid prototyping (ownership is a learning curve)",
            "Dynamic loading / plugin systems (lack of runtime reflection)",
        ],
        "fitness": {
            "excellent": ["Systems programming", "WebAssembly", "Embedded", "Performance-critical services", "CLI tools"],
            "poor": ["Rapid scripting", "Quick data analysis", "Mobile development", "Dynamic plugin systems"],
        },
        "paradigm_evolution": {
            "2015": "Pure systems language — no async, no stable abstractions",
            "2018": "Rust 2018: non-lexical lifetimes, async/await preview",
            "2021": "Rust 2021: closure capture, await syntax, improved error messages",
            "2024": "Rust 2024: async closures stabilized, polonius borrow checker in progress",
            "2026": "Ownership is still the core — no paradigm shift, but the ecosystem has grown around it",
        },
        "idiomatic_code_comparison": {
            "mutation": {
                "paradigm": "systems / ownership",
                "code": '''let mut x = 5;
x = 10; // explicit mut required — mutation is visible''',
            },
            "abstraction": {
                "paradigm": "functional / algebraic",
                "code": '''let result = [1, 2, 3]
    .iter()
    .map(|x| x * 2)
    .filter(|x| *x > 3)
    .sum::<i32>(); // zero-cost chain''',
            },
            "concurrency": {
                "paradigm": "actor / message passing",
                "code": '''let counter = Arc::new(Mutex::new(0));
let c = counter.clone();
tokio::spawn(async move {
    *c.lock().unwrap() += 1;
});''',
            },
        },
    },
    "Go": {
        "primary_paradigm": "procedural",
        "secondary_paradigms": ["object_oriented", "concurrent"],
        "dominant_ideology": "Simple is better than complex. Concurrency is built in. Formatting is automatic.",
        "paradigm_tension": [
            {
                "tension": "Simplicity (procedural) vs. Expressiveness (functional)",
                "description": "Go has no generics before 1.18, no exceptions, no try/catch. This keeps the language simple — but makes some code verbose or repetitive.",
                "where_it_fires": "When you need a generic data structure — before Go 1.18, you had to use interface{} or code-generate. After 1.18, you have generics but no higher-kinded types.",
                "verdict": "Go wins on simplicity — but loses on expressiveness. The tension is real.",
            },
            {
                "tension": "Concurrency built-in (goroutines) vs. Sequential thinking (procedural)",
                "description": "Goroutines are the best concurrency model for most use cases — cheap, simple, composable. But Go programs are often written as if concurrency doesn't exist.",
                "where_it_fires": "When a Go programmer writes a sequential loop calling an API 1000 times instead of using goroutines + channels.",
                "verdict": "Go wins — goroutines are cheap enough that you CAN use them, even if idiomatic Go sometimes forgets.",
            },
            {
                "tension": "Interfaces (duck typing) vs. Structs (concrete types)",
                "description": "Go's interfaces are structural (if it has the methods, it satisfies the interface). But Go has no inheritance — only struct embedding.",
                "where_it_fires": "When you want to 'extend' a type — Go uses embedding (composition), not inheritance. This is a paradigm shift for OOP programmers.",
                "verdict": "Go wins — composition over inheritance is the right call. But it requires unlearning OOP habits.",
            },
        ],
        "hidden_assumptions": [
            "Simplicity is more important than expressiveness",
            "Goroutines solve concurrency problems",
            "Errors should be handled at every call site (not thrown)",
            "Formatting should be automatic (gofmt)",
        ],
        "what_it_makes_easy": [
            "Network servers and microservices",
            "Concurrency with goroutines and channels",
            "Large team collaboration (simple syntax, enforced formatting)",
            "Fast compilation",
        ],
        "what_it_makes_hard": [
            "Generic algorithms (pre-1.18)",
            "Error handling verbosity (every error must be checked)",
            "Expression-based functional patterns",
        ],
        "fitness": {
            "excellent": ["Network services", "CLI tools", "Cloud infrastructure", "Microservices", "DevOps tooling"],
            "poor": ["Embedded systems", "Real-time systems", "Heavy computation (no SIMD abstractions)"],
        },
        "paradigm_evolution": {
            "2009": "Go announced — simple procedural language with concurrency",
            "2012": "Go 1.0 — stable, backward compatible",
            "2014": "vendor/ directory for dependency management",
            "2016": "Go 1.7 — context package for cancellation and timeouts",
            "2018": "Go 1.11 — modules, go mod",
            "2022": "Go 1.18 — generics! Finally!",
            "2024": "Go 1.23 — range-over-func iterators",
            "2026": "Generics are now idiomatic — the tension is resolving",
        },
        "idiomatic_code_comparison": {
            "mutation": {
                "paradigm": "procedural",
                "code": '''x := 5
x = 10 // no mut keyword — all variables are mutable by default''',
            },
            "abstraction": {
                "paradigm": "generic / procedural",
                "code": '''func Map[T, U any](s []T, f func(T) U) []U {
    result := make([]U, len(s))
    for i, v := range s {
        result[i] = f(v)
    }
    return result
}''',
            },
            "concurrency": {
                "paradigm": "CSP / actor",
                "code": '''ch := make(chan int)
go func() { ch <- 42 }()
result := <-ch''',
            },
        },
    },
    "Swift": {
        "primary_paradigm": "object_oriented",
        "secondary_paradigms": ["functional", "procedural"],
        "dominant_ideology": "Safe, fast, expressive. Types are your friend. Protocols over inheritance.",
        "paradigm_tension": [
            {
                "tension": "Value types (functional) vs. Reference types (OOP)",
                "description": "Swift's structs are value types (copied), classes are reference types (shared). This is a design choice — not an assumption. But it means Swift programmers must think about when to use which.",
                "where_it_fires": "When you pass a class to a function and it gets mutated — or when you pass a struct and it doesn't get mutated because it was copied.",
                "verdict": "Swift wins — the programmer chooses. But the choice matters and has consequences.",
            },
            {
                "tension": "Protocols (composition) vs. Inheritance (OOP)",
                "description": "Swift's answer to polymorphism is protocols — like interfaces. You can add protocols to existing types (extension + protocol). This is more composable than single inheritance.",
                "where_it_fires": "When an OOP programmer tries to use multiple inheritance — Swift doesn't have it. Use protocols + extensions instead.",
                "verdict": "Swift wins — protocols are more flexible than inheritance. But it requires unlearning the 'inheritance hierarchy' mental model.",
            },
            {
                "tension": "Optional (null safety) vs. Force unwrap (crash risk)",
                "description": "Swift's Optional<T> is a first-class type (like Rust's Option). But ! (force unwrap) exists and crashes at runtime. The tension is between safety and ergonomics.",
                "where_it_fires": "When a programmer uses ! everywhere to avoid if let — and gets runtime crashes.",
                "verdict": "Swift wins — Optional is the right default. ! is the escape hatch. The tension is productive.",
            },
        ],
        "hidden_assumptions": [
            "Types should be explicit where they matter",
            "Mutability should be explicit (let vs. var)",
            "Protocols are better than inheritance",
            "Safety is more important than performance (except in hot paths)",
        ],
        "what_it_makes_easy": [
            "iOS/macOS development (first-class)",
            "Protocol-oriented programming",
            "Safe null handling",
            "Value semantics for data structures",
        ],
        "what_it_makes_hard": [
            "Cross-platform development (until Swift 6)",
            "Metaprogramming",
            "Interfacing with C libraries (manually bridged)",
        ],
        "fitness": {
            "excellent": ["iOS/macOS development", "Server-side (via SwiftNIO)", "Systems with safety requirements"],
            "poor": ["Android development", "Windows", "Embedded (no standard embedded story)"],
        },
        "paradigm_evolution": {
            "2014": "Swift announced — replacement for Objective-C",
            "2015": "Swift 2.0 — error handling, protocol extensions",
            "2016": "Swift 3.0 — massive API redesign, SE-0002",
            "2019": "Swift 5.0 — async/await, result builders",
            "2023": "Swift 5.9 — macro system, existential types",
            "2024": "Swift 6.0 — complete data-race safety, typed throws",
            "2026": "Swift 6 is the most advanced Swift ever — actor model is first-class",
        },
        "idiomatic_code_comparison": {
            "mutation": {
                "paradigm": "value semantics",
                "code": '''let x = 5 // immutable
var y = 10 // mutable
y = 20 // OK''',
            },
            "abstraction": {
                "paradigm": "protocol-oriented",
                "code": '''protocol Drawable {
    func draw()
}
struct Circle: Drawable {
    func draw() { print("circle") }
}''',
            },
            "concurrency": {
                "paradigm": "structured concurrency / actor",
                "code": '''actor Counter {
    private var count = 0
    func increment() { count += 1 }
}''',
            },
        },
    },
    "Kotlin": {
        "primary_paradigm": "object_oriented",
        "secondary_paradigms": ["functional"],
        "dominant_ideology": "Pragmatic JVM language. Null safety built in. Coroutines for async. Extension functions for DSLs.",
        "paradigm_tension": [
            {
                "tension": "OOP (classes) vs. Functional (functions as values)",
                "description": "Kotlin is a hybrid — it has classes and objects (OOP) but also first-class functions (functional). The tension is which to reach for.",
                "where_it_fires": "When a Kotlin programmer writes everything as a class method vs. when they use top-level functions and lambda expressions.",
                "verdict": "Kotlin wins — both are valid. The tension is resolved by style guides (JetBrains recommends top-level functions).",
            },
            {
                "tension": "JVM (Java interop) vs. Kotlin-native (coroutines, extension functions)",
                "description": "Kotlin compiles to JVM bytecode and interoperates with Java. But Kotlin has coroutines and extension functions that Java doesn't. The tension is when to use each.",
                "where_it_fires": "When you need to call Java from Kotlin and get null safety (use @Nullable/@NonNull), or when you use Kotlin extension functions on Java types.",
                "verdict": "Kotlin wins — the interop is good enough. But you need to know both worlds.",
            },
            {
                "tension": "Immutability (data classes) vs. Mutable state (var)",
                "description": "Kotlin's val is read-only, var is mutable. Data classes are typically immutable (all vals). But you can still write mutable code.",
                "where_it_fires": "When a Kotlin programmer uses var everywhere instead of val + immutable data classes.",
                "verdict": "Kotlin wins — the tooling encourages immutability. But the programmer can ignore it.",
            },
        ],
        "hidden_assumptions": [
            "JVM is the target platform (for Android/server)",
            "Null safety is non-negotiable",
            "Coroutines are the right async model",
            "Extension functions are a good idea",
        ],
        "what_it_makes_easy": [
            "Android development",
            "DSL construction (extension functions)",
            "Safe null handling",
            "Coroutines for async",
        ],
        "what_it_makes_hard": [
            "Native compilation (Kotlin/Native is maturing)",
            "Metaprogramming (no macros like Rust)",
            "Compile time reflection (limited compared to Java)",
        ],
        "fitness": {
            "excellent": ["Android development", "JVM backend services", "DSL construction", "Coroutines-heavy async"],
            "poor": ["Native compilation (Kotlin/Native)", "iOS development", "Low-level systems"],
        },
        "paradigm_evolution": {
            "2011": "Kotlin announced by JetBrains",
            "2016": "Kotlin 1.0 — production ready",
            "2017": "Google I/O — Kotlin is official Android language",
            "2018": "Kotlin 1.3 — coroutines stable",
            "2019": "Kotlin 1.4 — SAM conversions, new type inference",
            "2021": "Kotlin 1.5 — sealed interfaces, inline classes",
            "2023": "Kotlin 2.0 — K2 compiler, new frontend",
            "2026": "Kotlin multiplatform is maturing — iOS, JVM, JS, Native all in one language",
        },
        "idiomatic_code_comparison": {
            "mutation": {
                "paradigm": "data class / immutability",
                "code": '''data class User(val name: String, val age: Int)
// copy() creates modified version:
val updated = user.copy(age = 26)''',
            },
            "abstraction": {
                "paradigm": "extension functions",
                "code": '''fun String.addExclamation() = this + "!"
val greeting = "hello".addExclamation() // "hello!"''',
            },
            "concurrency": {
                "paradigm": "coroutines / structured concurrency",
                "code": '''suspend fun fetchUser(id: Long): User =
    withContext(Dispatchers.IO) { userApi.get(id) }''',
            },
        },
    },
    "TypeScript": {
        "primary_paradigm": "multi_paradigm",
        "secondary_paradigms": ["object_oriented", "functional"],
        "dominant_ideology": "JavaScript with types. The type system is the feature. If it compiles, it probably works.",
        "paradigm_tension": [
            {
                "tension": "Dynamic (JavaScript) vs. Static (TypeScript)",
                "description": "TypeScript adds compile-time types to JavaScript. But at runtime, it's still JavaScript. The type system is erased — there's no runtime type safety.",
                "where_it_fires": "When TypeScript compiles 'as' casts that fail at runtime, or when strict: false means null checks are skipped.",
                "verdict": "TypeScript wins on safety — but the tension is real. You need strict mode and discipline.",
            },
            {
                "tension": "Structural typing (TS) vs. Nominal typing (Java)",
                "description": "TypeScript uses structural typing: if it has the right shape, it's the right type. This is different from Java's nominal typing.",
                "where_it_fires": "When a TypeScript programmer expects private fields to be enforced (they're not in structural typing — 'private' is just naming convention).",
                "verdict": "TypeScript wins — structural typing is more flexible. But you need to know the difference.",
            },
            {
                "tension": "JavaScript ecosystem (dynamic) vs. TypeScript tooling (static)",
                "description": "TypeScript has great tooling (autocomplete, refactoring) but JavaScript has the npm ecosystem. The tension is when to use which.",
                "where_it_fires": "When you want to use a JavaScript library in TypeScript — you need .d.ts type declarations, which may be incomplete or outdated.",
                "verdict": "TypeScript wins — the ecosystem is catching up. But the tension is real in mature codebases.",
            },
        ],
        "hidden_assumptions": [
            "Runtime types are not enforced (types are compile-time only)",
            "any is always one keystroke away",
            "null and undefined are both 'absent'",
            "The type system is Turing-complete (you can encode anything)",
        ],
        "what_it_makes_easy": [
            "Large JavaScript codebases (gradual typing)",
            "Web development (Node.js, browser)",
            "Complex domain modeling (type-level computation)",
        ],
        "what_it_makes_hard": [
            "Runtime type safety (must use zod/runtypes)",
            "Performance-critical code (no low-level control)",
            "Compiler performance (large projects can be slow)",
        ],
        "fitness": {
            "excellent": ["Web development (frontend + backend)", "Large JS codebases", "Complex domain modeling"],
            "poor": ["Embedded systems", "Real-time systems", "Low-level systems"],
        },
        "paradigm_evolution": {
            "2012": "TypeScript 0.8 — Microsoft internal use",
            "2014": "TypeScript 1.0 — public release",
            "2016": "TypeScript 2.0 — strict null checks, control flow analysis",
            "2018": "TypeScript 2.7 — definite assignment assertions, const assertions",
            "2020": "TypeScript 4.0 — variadic tuple types, labeled tuple elements",
            "2023": "TypeScript 5.0 — decorators, const type parameters",
            "2025": "TypeScript 6.0 — inferred type variables, better variance handling",
            "2026": "TypeScript is the dominant typed JavaScript — and the type system is more advanced than most languages",
        },
        "idiomatic_code_comparison": {
            "mutation": {
                "paradigm": "multi-paradigm",
                "code": '''const x = 5; // immutable binding
let y = 10; // mutable
y = 20; // OK — but y is still a const binding to a mutable number (primitives are immutable)''',
            },
            "abstraction": {
                "paradigm": "structural / generic",
                "code": '''type Result<T, E> =
    | { kind: "ok"; value: T }
    | { kind: "err"; error: E };
// discriminated union — exhaustiveness enforced''',
            },
            "concurrency": {
                "paradigm": "async / functional",
                "code": '''const [a, b] = await Promise.all([
    fetch(url1),
    fetch(url2)
]); // parallel async, structured''',
            },
        },
    },
    "JavaScript": {
        "primary_paradigm": "multi_paradigm",
        "secondary_paradigms": ["object_oriented", "functional", "procedural"],
        "dominant_ideology": "The world's most widely deployed runtime. Everything is an object (except primitives). Async is cooperative.",
        "paradigm_tension": [
            {
                "tension": "Prototype inheritance (OOP) vs. Class syntax (ES2015)",
                "description": "JavaScript has two object systems: prototype chains (original) and class syntax (ES2015 sugar over prototypes). The tension is which to use.",
                "where_it_fires": "When you use class inheritance and hit the 'method overriding' gotcha with 'this' binding, or when you use prototypes and need to understand the prototype chain.",
                "verdict": "JavaScript wins — classes are idiomatic now. But understanding prototypes is still important for debugging.",
            },
            {
                "tension": "Synchronous (procedural) vs. Asynchronous (callback/promise/async)",
                "description": "JavaScript is single-threaded with an event loop. All I/O is async. But you can write synchronous-looking code with async/await.",
                "where_it_fires": "When a programmer writes blocking code (sync fs operations) inside an async function — and blocks the event loop.",
                "verdict": "JavaScript wins — async/await is the right model. But the event loop is a footgun.",
            },
            {
                "tension": "Dynamic typing (flexible) vs. Debugging (hard)",
                "description": "JavaScript has no compile-time type checking. Type errors happen at runtime. This makes debugging harder.",
                "where_it_fires": "When a runtime type error crashes production — because there was no compile-time check.",
                "verdict": "JavaScript loses — use TypeScript. The tension is real and TypeScript solves it.",
            },
        ],
        "hidden_assumptions": [
            "Runtime errors are acceptable",
            "Async is cooperative (no preemption)",
            "Everything can throw",
            "this is bound at call time",
        ],
        "what_it_makes_easy": [
            "Web development (browser)",
            "Rapid prototyping",
            "Full-stack (Node.js)",
        ],
        "what_it_makes_hard": [
            "Type safety (use TypeScript)",
            "Concurrency (event loop is single-threaded)",
            "Large codebases (without TypeScript)",
        ],
        "fitness": {
            "excellent": ["Web development", "CLI scripts", "Rapid prototyping", "Full-stack JS"],
            "poor": ["Safety-critical systems", "Embedded", "High-performance computing"],
        },
        "paradigm_evolution": {
            "1997": "JavaScript standardized as ECMAScript 1",
            "2009": "Node.js — JavaScript on the server",
            "2015": "ES2015 (ES6) — classes, promises, arrow functions, let/const",
            "2017": "async/await — structured async",
            "2020": "ES2020 — optional chaining, nullish coalescing",
            "2023": "ES2023 — array find last, toSorted",
            "2026": "JavaScript has the largest ecosystem in the world — npm has 2M+ packages",
        },
        "idiomatic_code_comparison": {
            "mutation": {
                "paradigm": "prototype / object",
                "code": '''const obj = { x: 5 };
obj.x = 10; // mutation is fine — no const for objects prevents reassignment, not mutation''',
            },
            "abstraction": {
                "paradigm": "closure / functional",
                "code": '''const add = (a) => (b) => a + b;
const increment = add(1);
increment(5); // 6 — currying''',
            },
            "concurrency": {
                "paradigm": "async / cooperative",
                "code": '''async function fetchAll(urls) {
    return Promise.all(urls.map(fetch));
}''',
            },
        },
    },
    "Java": {
        "primary_paradigm": "object_oriented",
        "secondary_paradigms": ["procedural", "functional"],
        "dominant_ideology": "Write once, run anywhere. Strong typing, checked exceptions, class hierarchy. The language that made OOP mainstream.",
        "paradigm_tension": [
            {
                "tension": "Class inheritance (OOP) vs. Composition (functional)",
                "description": "Java is fundamentally class-based. But modern Java has lambdas, streams, and functional programming constructs. The tension is when to use class hierarchies vs. composition.",
                "where_it_fires": "When a Java programmer overuses inheritance ('extends' everywhere) instead of composition + interfaces.",
                "verdict": "Java wins — effective Java says 'prefer composition over inheritance'. The tension is cultural.",
            },
            {
                "tension": "Checked exceptions (verbose) vs. Unchecked exceptions (silent)",
                "description": "Java has checked exceptions (compiler enforces handling) and unchecked exceptions (RuntimeException hierarchy). The tension is when to use which.",
                "where_it_fires": "When a Java programmer uses checked exceptions for everything (verbose) or unchecked for everything (silent failures).",
                "verdict": "Java loses — checked exceptions were a mistake. Use Result<T> or don't throw checked exceptions.",
            },
            {
                "tension": "Generics (type erasure) vs. Reified types (Kotlin)",
                "description": "Java's generics use type erasure at runtime (List<String> and List<Integer> are the same class). Kotlin has reified generics (inline functions).",
                "where_it_fires": "When a Java programmer tries to do List<String>.class — it doesn't exist because of type erasure.",
                "verdict": "Java loses — type erasure was a JVM compatibility trade-off. It's a real limitation.",
            },
        ],
        "hidden_assumptions": [
            "Everything is a class",
            "Inheritance is a good reuse mechanism",
            "Checked exceptions are a good idea",
            "GC is the right memory model",
        ],
        "what_it_makes_easy": [
            "Enterprise development",
            "Android development",
            "Large team collaboration",
            "Cross-platform deployment",
        ],
        "what_it_makes_hard": [
            "Functional programming (lambdas help but not enough)",
            "Low-level control",
            "Value types (until record classes, still limited)",
        ],
        "fitness": {
            "excellent": ["Enterprise software", "Android development", "Backend services", "Large-scale systems"],
            "poor": ["Embedded systems", "Low-level systems", "Functional-first domains"],
        },
        "paradigm_evolution": {
            "1995": "Java announced by Sun — 'applets in the browser'",
            "1998": "Java 1.2 — collections framework, Swing",
            "2004": "Java 5 — generics, annotations, enums, autoboxing",
            "2014": "Java 8 — lambdas, streams, Optional, default methods",
            "2017": "Java 9 — modules (JPMS), reactive streams",
            "2018": "Java 11 — removes Java EE / CORBA modules, LTS",
            "2021": "Java 17 — sealed classes, pattern matching (preview)",
            "2023": "Java 21 — virtual threads (ga), pattern matching (ga), record classes",
            "2026": "Java 25 — virtual threads are standard, records are idiomatic, modern Java has closed the gap",
        },
        "idiomatic_code_comparison": {
            "mutation": {
                "paradigm": "immutable by design",
                "code": '''final int x = 5; // final binding
// For objects: don't expose setters, use immutable design
public class User {
    private final String name;
    public User(String name) { this.name = name; }
    public String getName() { return name; }
}''',
            },
            "abstraction": {
                "paradigm": "interface / polymorphism",
                "code": '''interface Comparator<T> {
    int compare(T a, T b);
}
// Lambda:
Comparator<String> byLen = (a, b) -> Integer.compare(a.length(), b.length());''',
            },
            "concurrency": {
                "paradigm": "virtual threads / structured concurrency",
                "code": '''try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> f = scope.fork(() -> api.call());
    scope.join();
}''',
            },
        },
    },
    "C/C++": {
        "primary_paradigm": "systems",
        "secondary_paradigms": ["procedural", "object_oriented"],
        "dominant_ideology": "You are in charge. Performance is paramount. No safety net. If you don't manage it, it doesn't get managed.",
        "paradigm_tension": [
            {
                "tension": "C (procedural) vs. C++ (OOP + functional + generic)",
                "description": "C++ is a multi-paradigm language that includes C. But using C++ as 'C with classes' wastes its power. Using it as pure template metaprogramming is hard to read.",
                "where_it_fires": "When a C++ programmer writes C-style code (malloc, raw pointers) instead of using RAII, smart pointers, and STL.",
                "verdict": "C++ wins — use modern C++. But the tension is real in legacy codebases.",
            },
            {
                "tension": "Performance (manual) vs. Safety (automatic)",
                "description": "C++ gives you manual memory management, raw pointers, and undefined behavior. It also gives you RAII, smart pointers, and type-safe abstractions. The tension is which to use.",
                "where_it_fires": "When a C++ programmer uses raw pointers and manual memory management for 'performance' — and introduces memory leaks or buffer overflows.",
                "verdict": "C++ wins — modern C++ (RAII + smart pointers) is as safe as garbage-collected languages while maintaining performance. But the old habits die hard.",
            },
            {
                "tension": "Templates (generic) vs. Concepts (readable constraints)",
                "description": "C++ templates are Turing-complete at compile time (metaprogramming). C++20 Concepts make them readable. The tension is expressiveness vs. readability.",
                "where_it_fires": "When a C++ programmer writes a 200-line template error message — because the compiler is trying to instantiate a template with the wrong type.",
                "verdict": "C++ wins — C++20 Concepts are the right answer. But legacy code still uses raw templates.",
            },
        ],
        "hidden_assumptions": [
            "Programmer is always right",
            "Performance is more important than safety",
            "Manual memory management is acceptable",
            "Undefined behavior is acceptable if you know what you're doing",
        ],
        "what_it_makes_easy": [
            "Maximum performance",
            "Direct hardware access",
            "Zero-overhead abstractions",
            "Predictable memory layout",
        ],
        "what_it_makes_hard": [
            "Productivity",
            "Concurrency (no safe shared mutation)",
            "Large teams (undefined behavior is a footgun)",
        ],
        "fitness": {
            "excellent": ["Operating systems", "Embedded systems", "Game engines", "High-frequency trading", "Compiler toolchains"],
            "poor": ["Web development", "Rapid prototyping", "Scripting", "Large team collaboration"],
        },
        "paradigm_evolution": {
            "1978": "C — 'The C Programming Language' book",
            "1985": "C++ — 'The C++ Programming Language' book, classes, constructors/destructors",
            "1998": "C++98 — standard library, STL, templates",
            "2011": "C++11 — auto, lambdas, smart pointers, move semantics, nullptr",
            "2014": "C++14 — generic lambdas, return type deduction",
            "2017": "C++17 — if constexpr, optional/variant, filesystem",
            "2020": "C++20 — Concepts, ranges, coroutines, modules",
            "2023": "C++23 — std::expected, constexpr everything, import std",
            "2026": "C++26 — static constexpr, improved coroutines, reflection (preview)",
        },
        "idiomatic_code_comparison": {
            "mutation": {
                "paradigm": "manual / RAII",
                "code": '''auto file = std::make_unique<File>("data.txt");
// file is automatically closed when it goes out of scope
// RAII — the destructor runs automatically''',
            },
            "abstraction": {
                "paradigm": "template / generic",
                "code": '''template<std::integral T>
T square(T x) { return x * x; }
// C++20 Concepts constrain T to integral types only''',
            },
            "concurrency": {
                "paradigm": "thread / atomic",
                "code": '''std::atomic<int> counter{0};
counter.fetch_add(1, std::memory_order_relaxed);
// Lock-free counter — no mutex needed''',
            },
        },
    },
}


def build_weave(language: str) -> Dict[str, Any]:
    """
    Build a paradigm weave for the selected language.

    Reveals hidden paradigm assumptions, tension maps, and fitness ratings.
    """
    config = load_rotation()
    languages = TOOL_LANGUAGES

    if language not in languages:
        raise ValueError(
            f"Language '{language}' not in this tool's rotation. "
            f"Available: {', '.join(languages)}"
        )

    profile = LANGUAGE_PROFILES[language]
    primary_p = profile["primary_paradigm"]
    paradigm_data = PARADIGMS[primary_p]

    # Build tension map
    tension_map = []
    for tension in profile.get("paradigm_tension", []):
        tension_map.append({
            "tension": tension["tension"],
            "description": tension["description"],
            "where_it_fires": tension["where_it_fires"],
            "verdict": tension["verdict"],
        })

    # Build hidden assumptions map
    hidden_assumptions = []
    for assumption in profile.get("hidden_assumptions", []):
        hidden_assumptions.append(assumption)

    # Build paradigm comparison (how this language's paradigm compares to others)
    paradigm_comparison = {}
    for lang in languages:
        other_profile = LANGUAGE_PROFILES[lang]
        other_primary = other_profile["primary_paradigm"]
        if other_primary == primary_p:
            comparison_type = "same_family"
        elif primary_p in other_profile.get("secondary_paradigms", []):
            comparison_type = "secondary_match"
        else:
            comparison_type = "different"
        paradigm_comparison[lang] = {
            "primary_paradigm": other_primary,
            "comparison": comparison_type,
            "emoji": PARADIGMS[other_primary]["emoji"],
        }

    # Fitness radar dimensions
    fitness_dimensions = ["Systems", "Web", "Mobile", "Concurrency", "Safety", "Productivity", "Abstraction"]
    fitness_values = _compute_fitness(profile, fitness_dimensions)

    # Paradigm signature (how this language's paradigm scores on each dimension)
    paradigm_signature = {}
    for dim in fitness_dimensions:
        paradigm_signature[dim] = _paradigm_score(primary_p, dim)

    # Determine next language
    current_idx = languages.index(language)
    next_idx = (current_idx + 1) % len(languages)
    next_lang = languages[next_idx]

    # Advance rotation
    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "primary_paradigm": {
            "id": primary_p,
            "name": paradigm_data["name"],
            "emoji": paradigm_data["emoji"],
            "description": paradigm_data["description"],
            "core_idea": paradigm_data["core_idea"],
        },
        "secondary_paradigms": [
            {"id": p, "name": PARADIGMS[p]["name"], "emoji": PARADIGMS[p]["emoji"]}
            for p in profile.get("secondary_paradigms", [])
        ],
        "dominant_ideology": profile["dominant_ideology"],
        "hidden_assumptions": hidden_assumptions,
        "paradigm_tension_map": tension_map,
        "paradigm_comparison": paradigm_comparison,
        "fitness": {
            "dimensions": fitness_dimensions,
            "radar": fitness_values,
            "excellent_for": profile["fitness"]["excellent"],
            "poor_for": profile["fitness"]["poor"],
        },
        "paradigm_signature": paradigm_signature,
        "paradigm_evolution": profile["paradigm_evolution"],
        "idiomatic_code_comparison": profile["idiomatic_code_comparison"],
        "next_language": next_lang,
        "rotation_order": languages,
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def _paradigm_score(paradigm_id: str, dimension: str) -> int:
    """Score a paradigm on a dimension (1-10)."""
    scores = {
        "systems": {"Systems": 10, "Web": 2, "Mobile": 3, "Concurrency": 7, "Safety": 4, "Productivity": 3, "Abstraction": 5},
        "procedural": {"Systems": 7, "Web": 4, "Mobile": 2, "Concurrency": 3, "Safety": 3, "Productivity": 6, "Abstraction": 3},
        "object_oriented": {"Systems": 4, "Web": 7, "Mobile": 8, "Concurrency": 4, "Safety": 5, "Productivity": 7, "Abstraction": 8},
        "functional": {"Systems": 5, "Web": 6, "Mobile": 4, "Concurrency": 9, "Safety": 8, "Productivity": 5, "Abstraction": 10},
        "multi_paradigm": {"Systems": 4, "Web": 9, "Mobile": 6, "Concurrency": 5, "Safety": 5, "Productivity": 9, "Abstraction": 7},
        "actor_based": {"Systems": 6, "Web": 7, "Mobile": 3, "Concurrency": 10, "Safety": 8, "Productivity": 6, "Abstraction": 6},
        "concurrent": {"Systems": 5, "Web": 8, "Mobile": 3, "Concurrency": 10, "Safety": 6, "Productivity": 8, "Abstraction": 6},
    }
    return scores.get(paradigm_id, {}).get(dimension, 5)


def _compute_fitness(profile: Dict, dimensions: List[str]) -> Dict[str, int]:
    """Compute fitness values for a language across dimensions."""
    paradigm = profile["primary_paradigm"]
    scores = {}
    for dim in dimensions:
        base = _paradigm_score(paradigm, dim)
        # Adjust for secondary paradigms
        for sp in profile.get("secondary_paradigms", []):
            sp_score = _paradigm_score(sp, dim)
            base = max(base, sp_score)
        scores[dim] = min(10, base)
    return scores


def paradigm_weaver(language: Optional[str] = None) -> Dict[str, Any]:
    """
    Main entry point: build a paradigm weave for the selected language.
    If language is None, uses the current rotation index.
    """
    config = load_rotation()
    languages = TOOL_LANGUAGES

    if language is None:
        current_idx = config.get("current_index", 0) % len(languages)
        language = languages[current_idx]

    return build_weave(language)


def run_tests():
    """Run tests to validate the Language Paradigm Weaver module."""
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

    print("Testing Language Paradigm Weaver...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(TOOL_LANGUAGES), "Tool manages 8 languages")
    assert_eq(True, 0 <= config["current_index"] < len(TOOL_LANGUAGES), "current_index in valid range")
    assert_eq("Rust", TOOL_LANGUAGES[0], "Rust is first language")

    print("  Testing build_weave for Rust...")
    result = build_weave("Rust")
    expected_keys = [
        "tool", "version", "selected_language", "primary_paradigm",
        "secondary_paradigms", "dominant_ideology", "hidden_assumptions",
        "paradigm_tension_map", "paradigm_comparison", "fitness",
        "paradigm_signature", "paradigm_evolution", "idiomatic_code_comparison",
        "next_language", "rotation_order", "timestamp"
    ]
    for key in expected_keys:
        assert_eq(True, key in result, f"Key '{key}' present in response")

    print("  Verifying primary paradigm structure...")
    pp = result["primary_paradigm"]
    assert_eq(True, "id" in pp, "primary_paradigm has id")
    assert_eq(True, "name" in pp, "primary_paradigm has name")
    assert_eq(True, "emoji" in pp, "primary_paradigm has emoji")
    assert_eq(True, "description" in pp, "primary_paradigm has description")
    assert_eq(True, "core_idea" in pp, "primary_paradigm has core_idea")
    assert_true(len(pp["description"]) > 10, "paradigm description is non-empty")
    assert_true(len(pp["core_idea"]) > 5, "paradigm core_idea is non-empty")

    print("  Verifying secondary paradigms...")
    sp = result["secondary_paradigms"]
    assert_true(isinstance(sp, list), "secondary_paradigms is a list")
    assert_true(len(sp) >= 1, "has at least one secondary paradigm")
    for p in sp:
        assert_eq(True, "id" in p, "secondary paradigm has id")
        assert_eq(True, "name" in p, "secondary paradigm has name")
        assert_eq(True, "emoji" in p, "secondary paradigm has emoji")

    print("  Verifying hidden assumptions...")
    ha = result["hidden_assumptions"]
    assert_true(isinstance(ha, list), "hidden_assumptions is a list")
    assert_true(len(ha) >= 2, "has at least 2 hidden assumptions")
    for assumption in ha:
        assert_true(len(assumption) > 5, "assumption is non-empty")

    print("  Verifying paradigm tension map...")
    tm = result["paradigm_tension_map"]
    assert_true(isinstance(tm, list), "paradigm_tension_map is a list")
    assert_true(len(tm) >= 1, "has at least 1 tension entry")
    for tension in tm:
        assert_eq(True, "tension" in tension, "tension has tension field")
        assert_eq(True, "description" in tension, "tension has description field")
        assert_eq(True, "where_it_fires" in tension, "tension has where_it_fires")
        assert_eq(True, "verdict" in tension, "tension has verdict")
        assert_true(len(tension["tension"]) > 5, "tension name is non-empty")
        assert_true(len(tension["verdict"]) > 5, "verdict is non-empty")

    print("  Verifying paradigm comparison...")
    pc = result["paradigm_comparison"]
    assert_eq(8, len(pc), "paradigm_comparison has entries for all 8 languages")
    for lang in TOOL_LANGUAGES:
        assert_eq(True, lang in pc, f"comparison has entry for {lang}")
        assert_eq(True, "primary_paradigm" in pc[lang], f"{lang} has primary_paradigm")
        assert_eq(True, "comparison" in pc[lang], f"{lang} has comparison")
        assert_eq(True, "emoji" in pc[lang], f"{lang} has emoji")

    print("  Verifying fitness...")
    fit = result["fitness"]
    assert_eq(True, "dimensions" in fit, "fitness has dimensions")
    assert_eq(True, "radar" in fit, "fitness has radar")
    assert_eq(True, "excellent_for" in fit, "fitness has excellent_for")
    assert_eq(True, "poor_for" in fit, "fitness has poor_for")
    assert_true(len(fit["dimensions"]) == 7, "fitness has 7 dimensions")
    assert_true(len(fit["radar"]) == 7, "fitness has 7 radar values")
    assert_true(isinstance(fit["excellent_for"], list), "excellent_for is a list")
    assert_true(isinstance(fit["poor_for"], list), "poor_for is a list")

    print("  Verifying paradigm signature...")
    ps = result["paradigm_signature"]
    assert_eq(7, len(ps), "paradigm_signature has 7 entries")
    for dim, score in ps.items():
        assert_true(1 <= score <= 10, f"{dim} score {score} is in range 1-10")

    print("  Verifying paradigm evolution...")
    pe = result["paradigm_evolution"]
    assert_true(isinstance(pe, dict), "paradigm_evolution is a dict")
    assert_true(len(pe) >= 3, "has at least 3 evolution entries")

    print("  Verifying idiomatic code comparison...")
    ic = result["idiomatic_code_comparison"]
    assert_true(isinstance(ic, dict), "idiomatic_code_comparison is a dict")
    assert_true(len(ic) >= 2, "has at least 2 code comparison entries")
    for key, entry in ic.items():
        assert_eq(True, "paradigm" in entry, f"{key} has paradigm")
        assert_eq(True, "code" in entry, f"{key} has code")
        assert_true(len(entry["code"]) > 10, f"{key} code is non-empty")

    print("  Verifying rotation update...")
    config2 = load_rotation()
    assert_eq(1, config2["current_index"], "Index advanced to 1 (Go)")
    assert_eq("Rust", config2["last_language"], "Last language recorded as Rust")

    print("  Resetting rotation for next test phase...")
    config = load_rotation()
    config["current_index"] = 1
    config["last_language"] = "Rust"
    save_rotation(config)

    print("  Testing build_weave for Go (next in rotation)...")
    result2 = build_weave("Go")
    assert_eq("Go", result2["selected_language"], "Go is selected")
    assert_eq("Swift", result2["next_language"], "Next language is Swift")

    print("  Testing all 8 languages have valid weaves...")
    for lang in TOOL_LANGUAGES:
        r = build_weave(lang)
        assert_eq(lang, r["selected_language"], f"{lang} selected correctly")
        assert_eq(8, len(r["paradigm_comparison"]), f"{lang}: comparison has 8 entries")
        assert_eq(True, "primary_paradigm" in r, f"{lang}: result has primary_paradigm")
        assert_eq(True, "paradigm_tension_map" in r, f"{lang}: result has paradigm_tension_map")
        assert_true(len(r["dominant_ideology"]) > 10, f"{lang}: dominant_ideology is non-empty")
        assert_true(len(r["hidden_assumptions"]) >= 2, f"{lang}: has at least 2 hidden assumptions")

    print("  Testing next_language is different from selected...")
    for lang in TOOL_LANGUAGES:
        r = build_weave(lang)
        assert_true(r["next_language"] != lang, f"{lang}: next_language differs from selected")

    print("  Testing all paradigms are represented...")
    seen_paradigms = set()
    for lang in TOOL_LANGUAGES:
        r = build_weave(lang)
        seen_paradigms.add(r["primary_paradigm"]["id"])
    assert_true(len(seen_paradigms) >= 2, f"Multiple paradigms found: {seen_paradigms}")

    print("  Testing invalid language handling...")
    try:
        build_weave("Python")
        tests_failed += 1
        print("  ❌ FAIL: No error raised for invalid language")
    except ValueError as e:
        tests_passed += 1
        print("  ✅ PASS: ValueError raised for invalid language")
        assert_in("not in this tool's rotation", str(e), "Error mentions rotation")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ FAIL: Wrong exception: {e}")

    print("  Testing paradigm_weaver() with None (auto-select)...")
    current_idx = load_rotation()["current_index"] % len(TOOL_LANGUAGES)
    current_lang = TOOL_LANGUAGES[current_idx]
    result_auto = paradigm_weaver()
    assert_eq(current_lang, result_auto["selected_language"], f"Auto-selected: {current_lang}")

    print("  Testing timestamp format...")
    ts = result["timestamp"]
    assert_true("T" in ts, "timestamp has ISO format with T separator")

    print("  Testing tension verdicts are non-empty...")
    for lang in TOOL_LANGUAGES:
        r = build_weave(lang)
        for tension in r["paradigm_tension_map"]:
            assert_true(len(tension["verdict"]) > 5, f"{lang}: verdict is non-empty")
            assert_true(len(tension["where_it_fires"]) > 5, f"{lang}: where_it_fires is non-empty")

    print("  Testing fitness radar values are integers in range...")
    for lang in TOOL_LANGUAGES:
        r = build_weave(lang)
        for dim, val in r["fitness"]["radar"].items():
            assert_true(isinstance(val, int), f"{lang}/{dim}: value is int")
            assert_true(1 <= val <= 10, f"{lang}/{dim}: value {val} in range 1-10")

    print(f"\n{'='*55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("🕸️ All Paradigm Weaver tests passed! Every language reveals its hidden assumptions.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--weave":
        language = sys.argv[2] if len(sys.argv) > 2 else None
        result = paradigm_weaver(language)
        print(json.dumps(result, indent=2))
    else:
        print(f"Language Paradigm Weaver v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m language_paradigm_weaver --test      # Run tests")
        print("  python -m language_paradigm_weaver --weave [lang]  # Build paradigm weave")