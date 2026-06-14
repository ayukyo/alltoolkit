#!/usr/bin/env python3
"""
📖 Polyglot Lexicon v1.0

Programming languages as dictionary entries — each language is defined like
a word in a dictionary: etymology, part of speech, definition, pronunciation,
usage sentences, synonyms, related terms, and cross-language cognates.

Creative concept: "Every programming language is a word in the great lexicon
of computation. Rust is a noun meaning 'the principle of being answerable
for what you allocate.' Go is a verb meaning 'to proceed concurrently toward
a goal.' Swift is an adjective meaning 'performing async operations with
the grace of a bird.' This tool is the dictionary that defines them all."

The tool generates a dictionary entry for the current rotation language:
- Etymology: where the language's name came from
- Part of speech: noun/verb/adjective/etc. (linguistic metaphor)
- Phonetic pronunciation: how to "say" the language
- Definition: what the language IS, in dictionary form
- Usage sentences: code examples as dictionary usage sentences
- Synonyms: languages that solve similar problems
- Related terms: companion concepts within the language
- Cognates: how the same concept appears in other languages (cross-lexicon)

Distinct from existing tools:
  - polyglot_digest:       syntax-parallel code (same logic, different syntax)
  - polyglot_synapse:      conceptual bridges (similar concepts)
  - polyglot_chronology:   geological epochs (deep time)
  - polyglot_resonator:    mental model differences
  - polyglot_cartographer: geopolitical relationships
  - polyglot_harmony:      pair compatibility
  - polyglot_tempo:        rhythm and cadence
  - polyglot_mood:         emotional personality

Lexicon is about LINGUISTIC DEPTH — treating each language as a word
with history, meaning, usage, and family relationships in the lexicon
of programming languages.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-lexicon"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent.parent
_WORKSPACE_ROOT = _MODULE_DIR.parent
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ─────────────────────────────────────────────────────────────────────────────
# Language Lexicon Database — each language as a dictionary entry
# ─────────────────────────────────────────────────────────────────────────────

LEXICON_DB: Dict[str, Dict[str, Any]] = {

    "Rust": {
        "part_of_speech": "noun",
        "pronunciation": "/rʌst/",
        "etymology": (
            "Named after the rust fungus, a hardy organism that survives "
            "extreme conditions — an homage to the robustness and safety "
            "properties the language prioritizes. Also a nod to the 'rust' "
            "of unsafe code that the language eliminates."
        ),
        "definition": (
            "A systems programming language that provides memory safety "
            "without a garbage collector, using ownership and borrowing "
            "as compile-time contracts. Coined as the language that lets "
            "you 'write once, run anywhere — correctly.'"
        ),
        "usage_notes": [
            ("statement", "To declare an owned value:", "let data = vec![1, 2, 3];"),
            ("statement", "To borrow immutably:", "fn peek(s: &Vec<i32>) -> &i32 { &s[0] }"),
            ("statement", "To borrow mutably:", "fn append(s: &mut Vec<i32>, val: i32) { s.push(val); }"),
            ("statement", "To propagate an error:", "let content = std::fs::read_to_string(\"file\")?;"),
            ("statement", "To define a trait bound:", "fn max<T: Ord>(a: T, b: T) -> T { if a > b { a } else { b } }"),
        ],
        "synonyms": ["C++ (systems)", "Zig (manual memory)", "Ada (safety-critical)"],
        "antonyms": ["Python (interpreted)", "JavaScript (garbage-collected)"],
        "related_terms": [
            ("ownership", "The system that tracks which variable currently owns a value"),
            ("borrowing", "Temporary access granted to a value without transferring ownership"),
            ("trait", "A capability interface defining shared behavior across types"),
            ("Result", "A type that either holds a success value or an error"),
            ("Option", "A type that either holds a value or nothing (None/Some)"),
        ],
        "cognates": {
            "Go": {
                "term": "defer",
                "rust_equivalent": "Drop trait",
                "note": "Both manage cleanup — Go's defer is stack-based; Rust's Drop is deterministic.",
            },
            "Swift": {
                "term": "borrow checker",
                "swift_equivalent": "Ownership — Swift 6 concurrency checking mirrors Rust's borrow rules",
                "note": "Swift 6 actors are Rust's Send+Sync traits in disguise.",
            },
            "Kotlin": {
                "term": "Result<T>",
                "kotlin_equivalent": "Result<T>",
                "note": "Both languages encode errors as values in the type system.",
            },
            "TypeScript": {
                "term": "type inference",
                "ts_equivalent": "TypeScript's structural type inference",
                "note": "Rust's type inference is narrower; TypeScript's is wider but runtime-untyped.",
            },
            "JavaScript": {
                "term": "destructuring",
                "js_equivalent": "Destructuring assignment",
                "note": "Rust's pattern destructuring is more powerful with match expressions.",
            },
            "Java": {
                "term": "generics",
                "java_equivalent": "Java generics with type erasure",
                "note": "Rust monomorphizes generics; Java erases them to Object.",
            },
            "C/C++": {
                "term": "move semantics",
                "cpp_equivalent": "C++11 move semantics (std::move)",
                "note": "Rust move is by default; C++ requires explicit std::move.",
            },
        },
        "inflection": "rust / rʌst / — to oxidize; to deteriorate; to become unsafe through neglect",
        "see_also": ["cargo", "rustc", "crates.io", "ownership", "borrow checker"],
    },

    "Go": {
        "part_of_speech": "verb",
        "pronunciation": "/ɡoʊ/",
        "etymology": (
            "Named simply — the language is about 'going' and moving forward. "
            "The mascot is a gopher, chosen for its pragmatic, no-nonsense nature. "
            "The name was short, easy to type, and not already taken in computing."
        ),
        "definition": (
            "A compiled, statically typed language designed for simplicity "
            "and concurrency. Goroutines and channels implement CSP-style "
            "concurrency. The language prioritizes readability and compile speed "
            "over expressive power."
        ),
        "usage_notes": [
            ("statement", "To spawn a concurrent task:", "go func() { doWork() }()"),
            ("statement", "To communicate between goroutines:", "ch := make(chan int); ch <- value"),
            ("statement", "To handle errors explicitly:", "f, err := os.Open(\"file\"); if err != nil { return err }"),
            ("statement", "To defer cleanup:", "f, _ := os.Open(\"file\"); defer f.Close()"),
            ("statement", "To use an interface implicitly:", "type Reader interface { Read(p []byte) (n int, err error) }"),
        ],
        "synonyms": ["Python (simple)", "Node.js (servers)", "Java (typed servers)"],
        "antonyms": ["C (complex)", "C++ (complex)"],
        "related_terms": [
            ("goroutine", "A lightweight thread managed by the Go runtime, not the OS"),
            ("channel", "A typed conduit for communicating between goroutines"),
            ("interface", "A set of method signatures — satisfied implicitly by any type implementing them"),
            ("defer", "A statement that schedules a function call to run when the surrounding function returns"),
            ("GOMAXPROCS", "The number of OS threads available to the Go runtime"),
        ],
        "cognates": {
            "Rust": {
                "term": "async/await",
                "rust_equivalent": "async/await with Tokio runtime",
                "note": "Go's goroutines are lighter than Rust's async tasks but less fine-grained.",
            },
            "Swift": {
                "term": "goroutine",
                "swift_equivalent": "Swift Concurrency async tasks",
                "note": "Go channels ≈ Swift actors — both are message-passing models.",
            },
            "Kotlin": {
                "term": "goroutine",
                "kotlin_equivalent": "Kotlin coroutines (launch { })",
                "note": "Go channels are unbuffered/buffered; Kotlin uses Flow for streams.",
            },
            "TypeScript": {
                "term": "Promise",
                "ts_equivalent": "Promise<T>",
                "note": "Go channels predate async/await in JS but serve a similar role.",
            },
            "JavaScript": {
                "term": "Promise",
                "js_equivalent": "new Promise((resolve, reject) => { })",
                "note": "JS Promises are typed; Go channels carry typed values.",
            },
            "Java": {
                "term": "thread",
                "java_equivalent": "java.util.concurrent threads and executors",
                "note": "Go's goroutines are ~2KB vs Java threads at ~1MB stack.",
            },
            "C/C++": {
                "term": "channel",
                "cpp_equivalent": "C++20 std::coroutine with std::channel (proposed)",
                "note": "Go channels are runtime-native; C++ coroutines are library-level.",
            },
        },
        "inflection": "go / ɡoʊ / — to proceed; to move concurrently; to communicate via channels",
        "see_also": ["goroutine", "channel", "defer", "interface", "go.mod"],
    },

    "Swift": {
        "part_of_speech": "adjective",
        "pronunciation": "/swɪft/",
        "etymology": (
            "Named for the swift bird — fast, graceful, and aerial. "
            "Apple chose Swift to signal that this language would be "
            "modern, fast-moving, and built for the Apple ecosystem, "
            "replacing Objective-C as the preferred language for iOS/macOS."
        ),
        "definition": (
            "A general-purpose, compiled language developed by Apple for "
            "iOS, macOS, and Linux. Combines type safety with a dynamic "
            "runtime. Features protocol-oriented programming, optionals, "
            "and value types by default."
        ),
        "usage_notes": [
            ("statement", "To declare a value type:", "struct Point { var x: Double; var y: Double }"),
            ("statement", "To handle optional values:", "let name: String? = dict[\"name\"]; if let n = name { print(n) }"),
            ("statement", "To define a protocol:", "protocol Drawable { func draw() }"),
            ("statement", "To use async/await:", "let data = try await fetch()"),
            ("statement", "To isolate state in an actor:", "actor Counter { private var count = 0 }"),
        ],
        "synonyms": ["Kotlin (Android)", "Rust (safe)", "Objective-C (Apple)"],
        "antonyms": ["C (unsafe)", "Python (slow)"],
        "related_terms": [
            ("optional", "A type that either holds a value or is nil — compiler-enforced null safety"),
            ("protocol", "A blueprint of methods, properties, and requirements that a type must implement"),
            ("struct", "A value type that copies on assignment — unlike classes which are reference types"),
            ("actor", "A reference type that isolated its state from concurrent access (Swift 6)"),
            ("@State", "A property wrapper for managing mutable state in SwiftUI views"),
        ],
        "cognates": {
            "Rust": {
                "term": "Option<T>",
                "rust_equivalent": "Option<T>",
                "note": "Swift optionals and Rust Option<T> serve identical purposes.",
            },
            "Go": {
                "term": "interface{}",
                "swift_equivalent": "Any type with protocol constraints",
                "note": "Swift protocols are more powerful with associated types.",
            },
            "Kotlin": {
                "term": "null safety",
                "kotlin_equivalent": "Nullable types (String?)",
                "note": "Both languages make null handling explicit at the type level.",
            },
            "TypeScript": {
                "term": "strict null checks",
                "ts_equivalent": "strictNullChecks in tsconfig",
                "note": "TypeScript's strict null checks mirror Swift's optionals in verbosity.",
            },
            "JavaScript": {
                "term": "destructuring",
                "js_equivalent": "Destructuring assignment",
                "note": "Swift pattern matching with if-let is more powerful than JS.",
            },
            "Java": {
                "term": "generics",
                "java_equivalent": "Java generics",
                "note": "Swift generics support where clauses and protocol constraints.",
            },
            "C/C++": {
                "term": "value types",
                "cpp_equivalent": "struct (value semantics)",
                "note": "Swift structs have copy-on-write; C++ structs are plain copies.",
            },
        },
        "inflection": "swift / swɪft / — moving with great speed; done with no delay; graceful in motion",
        "see_also": ["optional", "protocol", "actor", "SwiftUI", "@State"],
    },

    "Kotlin": {
        "part_of_speech": "noun",
        "pronunciation": "/ˈkɒtlɪn/",
        "etymology": (
            "Named after Kotlin Island near St. Petersburg, Russia — "
            "a nod to the JetBrains team's location. The name was chosen "
            "because it was short, punchy, and (unlike 'Kotlinlang') "
            "easy to use as a brand. It superseded JetBrains' earlier "
            "language, Kotlin/JVM."
        ),
        "definition": (
            "A statically typed JVM language that interoperates fully with "
            "Java, offering null safety, coroutines for concurrency, "
            "extension functions, and smart casts. Designed to be more "
            "concise and expressive than Java."
        ),
        "usage_notes": [
            ("statement", "To declare a nullable type:", "val name: String? = null"),
            ("statement", "To use safe call operator:", "val len = str?.length"),
            ("statement", "To define an extension function:", "fun String.addExclamation() = this + \"!\""),
            ("statement", "To launch a coroutine:", "launch { delay(1000); println(\"done\") }"),
            ("statement", "To define a data class:", "data class User(val name: String, val age: Int)"),
        ],
        "synonyms": ["Scala (JVM)", "Groovy (scripting)", "Java (JVM)"],
        "antonyms": ["C (low-level)", "JavaScript (interpreted)"],
        "related_terms": [
            ("nullable type", "A type that may hold null — denoted with ? suffix; compiler enforces handling"),
            ("data class", "A class auto-generating equals(), hashCode(), toString(), copy()"),
            ("coroutine", "A suspendable computation that can pause without blocking threads"),
            ("Flow", "A cold asynchronous stream — Kotlin's answer to reactive programming"),
            ("extension function", "Adding methods to existing classes without inheritance"),
        ],
        "cognates": {
            "Rust": {
                "term": "Result<T,E>",
                "rust_equivalent": "Result<T, E>",
                "note": "Kotlin's runCatching mirrors Rust's Result<T, E>.",
            },
            "Go": {
                "term": "defer",
                "kotlin_equivalent": "use {} extension on Closeable",
                "note": "Kotlin's use {} block runs cleanup on Closeable resources.",
            },
            "Swift": {
                "term": "optional",
                "swift_equivalent": "Optional<T>",
                "note": "Kotlin's nullable types and Swift's optionals encode absence identically.",
            },
            "TypeScript": {
                "term": "type union",
                "ts_equivalent": "string | null",
                "note": "Kotlin's nullable types and TypeScript's union with null are structurally equivalent.",
            },
            "JavaScript": {
                "term": "async/await",
                "js_equivalent": "async/await with Promises",
                "note": "Kotlin coroutines predate JS async/await by years.",
            },
            "Java": {
                "term": "null pointer",
                "java_equivalent": "NPE — NullPointerException",
                "note": "Kotlin's null safety eliminates NPE at compile time.",
            },
            "C/C++": {
                "term": "smart pointer",
                "cpp_equivalent": "std::unique_ptr, std::shared_ptr",
                "note": "Kotlin's garbage collector handles memory automatically.",
            },
        },
        "inflection": "kotlin / ˈkɒtlɪn / — named for an island; a pragmatist's tool; null-safe by design",
        "see_also": ["nullable", "coroutine", "Flow", "data class", "extension function"],
    },

    "TypeScript": {
        "part_of_speech": "noun",
        "pronunciation": "/ˈtaɪpskrɪpt/",
        "etymology": (
            "Type + Script — the name explains itself: JavaScript with "
            "compile-time type annotations. Created at Microsoft in 2010 "
            "to address large-scale JavaScript development, adding an "
            "optional type system that compiles to plain JavaScript."
        ),
        "definition": (
            "A typed superset of JavaScript that compiles to plain JavaScript. "
            "Uses structural typing, where type compatibility is determined "
            "by shape rather than name. Types are erased at runtime — "
            "the type system exists only at compile time."
        ),
        "usage_notes": [
            ("statement", "To define an interface:", "interface Point { x: number; y: number }"),
            ("statement", "To type a function:", "function add(a: number, b: number): number { return a + b }"),
            ("statement", "To use a generic constraint:", "function first<T extends { id: number }>(arr: T[]): T { return arr[0] }"),
            ("statement", "To use discriminated union:", "type Result = { ok: true; val: T } | { ok: false; err: E }"),
            ("statement", "To use optional chaining:", "const len = obj?.prop?.nested?.length"),
        ],
        "synonyms": ["JavaScript (runtime)", "Flow (Facebook typing)", "Pyright (Python typing)"],
        "antonyms": ["Python (interpreted)", "Java (VM)"],
        "related_terms": [
            ("interface", "A structural contract defining what properties and methods a type must have"),
            ("generic", "A type parameter that allows the same code to operate over different types"),
            ("type guard", "A runtime check that narrows a union type to a more specific branch"),
            ("utility types", "Built-in generic type helpers: Partial, Required, Pick, Omit, Record"),
            ("strictNullChecks", "Compiler flag that makes null/undefined a type error unless explicitly allowed"),
        ],
        "cognates": {
            "Rust": {
                "term": "trait bound",
                "rust_equivalent": "T: Trait",
                "note": "TypeScript's extends constraints and Rust's trait bounds serve similar purposes.",
            },
            "Go": {
                "term": "interface",
                "go_equivalent": "interface{} (empty) or interface{ Method() }",
                "note": "Go interfaces are nominal; TypeScript interfaces are structural.",
            },
            "Swift": {
                "term": "protocol",
                "swift_equivalent": "protocol Name { var x: Int { get } }",
                "note": "Swift protocols support associated types; TypeScript uses generics.",
            },
            "Kotlin": {
                "term": "generics",
                "kotlin_equivalent": "fun <T> process(item: T): T",
                "note": "TypeScript generics and Kotlin generics are structurally similar.",
            },
            "JavaScript": {
                "term": "type annotation",
                "js_equivalent": "None — JS has no types",
                "note": "TypeScript adds types on top of JavaScript; JS is the base.",
            },
            "Java": {
                "term": "interface",
                "java_equivalent": "interface Reader { void read(); }",
                "note": "Java interfaces are nominal; TypeScript interfaces are structural.",
            },
            "C/C++": {
                "term": "template",
                "cpp_equivalent": "template<typename T> T identity(T x) { return x; }",
                "note": "TypeScript generics are duck-typed (structural); C++ templates are monomorphized.",
            },
        },
        "inflection": "typescript / ˈtaɪpskrɪpt / — the annotated script; types as documentation; erased at runtime",
        "see_also": ["interface", "generic", "strictNullChecks", "utility types", "type guard"],
    },

    "JavaScript": {
        "part_of_speech": "noun",
        "pronunciation": "/ˈdʒeɪvəskrɪpt/",
        "etymology": (
            "Created in 10 days in 1995 by Brendan Eich at Netscape. "
            "Originally named Mocha, then LiveScript — the 'Java' prefix "
            "was a marketing decision to ride Java's popularity. "
            "The name has no technical meaning beyond brand association."
        ),
        "definition": (
            "A dynamic, interpreted language that runs in every browser "
            "and increasingly on servers (Node.js). The only language that "
            "runs natively in web browsers. Uses prototype-based inheritance, "
            "a single-threaded event loop, and closures as first-class values."
        ),
        "usage_notes": [
            ("statement", "To create a closure:", "const counter = (() => { let c = 0; return () => ++c; })()"),
            ("statement", "To handle async with Promises:", "fetch(url).then(r => r.json()).then(data => console.log(data))"),
            ("statement", "To destructure an object:", "const { name, age } = user;"),
            ("statement", "To use optional chaining:", "const city = person?.address?.city"),
            ("statement", "To create a generator:", "function* gen() { yield 1; yield 2; }"),
        ],
        "synonyms": ["TypeScript (typed JS)", "Python (scripting)", "Ruby (scripting)"],
        "antonyms": ["Rust (safe)", "C (low-level)"],
        "related_terms": [
            ("closure", "A function that captures variables from its enclosing scope — the basis of modules"),
            ("prototype", "The delegation chain for property lookup in objects"),
            ("event loop", "The single-threaded mechanism that processes async callbacks in order"),
            ("Promise", "An object representing an eventual completion or failure of an async operation"),
            ("generator", "A function that can pause and resume, yielding values one at a time"),
        ],
        "cognates": {
            "Rust": {
                "term": "closure",
                "rust_equivalent": "|x| x * 2",
                "note": "Rust closures capture environment by move by default; JS closures capture by reference.",
            },
            "Go": {
                "term": "goroutine",
                "go_equivalent": "go func() {}()",
                "note": "JS async/await and Go goroutines both avoid blocking the event loop.",
            },
            "Swift": {
                "term": "closure",
                "swift_equivalent": "Swift closures: { [weak self] x in self?.process(x) }",
                "note": "JS closures capture by reference; Swift closures can capture weakly to avoid cycles.",
            },
            "Kotlin": {
                "term": "lambda",
                "kotlin_equivalent": "val double: (Int) -> Int = { it * 2 }",
                "note": "Kotlin lambdas with it and JS arrow functions are nearly identical in syntax.",
            },
            "TypeScript": {
                "term": "type erasure",
                "ts_equivalent": "All TypeScript types are erased — no types at runtime",
                "note": "TypeScript is JavaScript + type annotations; JS types are runtime values.",
            },
            "Java": {
                "term": "class",
                "java_equivalent": "ES6 classes: class User { constructor(name) { this.name = name } }",
                "note": "JS class syntax is syntactic sugar over prototype-based inheritance.",
            },
            "C/C++": {
                "term": "prototype chain",
                "cpp_equivalent": "No equivalent — C++ uses class inheritance, not prototype delegation",
                "note": "C++ has no prototype delegation; this is unique to JS.",
            },
        },
        "inflection": "javascript / ˈdʒeɪvəskrɪpt / — the script that runs the web; prototype as inheritance; event-driven",
        "see_also": ["closure", "prototype", "Promise", "event loop", "destructuring"],
    },

    "Java": {
        "part_of_speech": "noun",
        "pronunciation": "/ˈdʒɑːvə/",
        "etymology": (
            "Named after Java coffee — the programming language equivalent "
            "of a caffeine fix. The name was chosen during a brainstorming "
            "session over coffee. Originally Oak (1991), renamed to Java "
            "in 1995 when it became clear that Oak was already trademarked."
        ),
        "definition": (
            "A compiled, object-oriented, platform-independent language "
            "running on the JVM. 'Write Once, Run Anywhere.' Uses checked "
            "exceptions, strong encapsulation, and a garbage collector. "
            "The JVM runs the same bytecode on any machine."
        ),
        "usage_notes": [
            ("statement", "To define a record (immutable carrier):", "record Point(int x, int y) {}"),
            ("statement", "To use try-with-resources:", "try (var f = new FileReader(\"file\")) { f.read(); }"),
            ("statement", "To spawn a virtual thread:", "try (var vt = VirtualThread.ofVirtual().start(() -> { })) { }"),
            ("statement", "To use a stream pipeline:", "list.stream().filter(x -> x > 0).map(x -> x * 2).collect(toList())"),
            ("statement", "To declare a generic method:", "public <T> T identity(T value) { return value; }"),
        ],
        "synonyms": ["Kotlin (JVM)", "Scala (JVM)", "C# (.NET)"],
        "antonyms": ["C (manual memory)", "C++ (complex)"],
        "related_terms": [
            ("JVM", "Java Virtual Machine — the runtime that executes Java bytecode"),
            ("GC", "Garbage Collector — automatic memory reclamation for heap-allocated objects"),
            ("virtual thread", "A lightweight thread (Java 21+) that dramatically reduces thread overhead"),
            ("record", "A compact, immutable data carrier (Java 16+) with auto-generated equals/hashCode"),
            ("stream", "A lazy pipeline of operations on collections, evaluated on terminal action"),
        ],
        "cognates": {
            "Rust": {
                "term": "generics",
                "rust_equivalent": "fn<T> identity(x: T) -> T",
                "note": "Java generics use type erasure; Rust monomorphizes generics into concrete types.",
            },
            "Go": {
                "term": "interface",
                "go_equivalent": "interface{}",
                "note": "Java interfaces are nominal; Go interfaces are structural and implicit.",
            },
            "Swift": {
                "term": "generics",
                "swift_equivalent": "func identity<T>(_ x: T) -> T",
                "note": "Swift generics support protocol constraints; Java generics do not.",
            },
            "Kotlin": {
                "term": "data class",
                "kotlin_equivalent": "data class User(val name: String)",
                "note": "Java records are similar to Kotlin data classes — both generate boilerplate.",
            },
            "TypeScript": {
                "term": "interface",
                "ts_equivalent": "interface Serializable { serialize(): string }",
                "note": "Both TypeScript and Java use interface-based design patterns.",
            },
            "JavaScript": {
                "term": "class",
                "js_equivalent": "class MyClass { constructor() { } }",
                "note": "Java classes are static and nominal; JS classes are prototype sugar.",
            },
            "C/C++": {
                "term": "template",
                "cpp_equivalent": "template<typename T> T identity(T x) { return x; }",
                "note": "Java generics ≠ C++ templates. Erasure vs monomorphization.",
            },
        },
        "inflection": "java / ˈdʒɑːvə / — coffee-powered computation; write once, run anywhere; GC as lifestyle",
        "see_also": ["JVM", "virtual thread", "record", "stream", "generics"],
    },

    "C/C++": {
        "part_of_speech": "noun",
        "pronunciation": "/siː plʌs plʌs/",
        "etymology": (
            "C++ is C with increment operators applied — the ++ is a pun "
            "on C's being a low-level procedural language, and C++ being "
            "'one better.' C was created at Bell Labs in 1972 by Dennis "
            "Ritchie for the Unix OS. C++ was created in 1983 by Bjarne "
            "Stroustrup as 'C with Classes,' later renamed C++."
        ),
        "definition": (
            "C: a low-level procedural language where identity equals memory "
            "address. C++: C with classes, templates, exceptions, and "
            "standard library. Both give the programmer total control over "
            "memory, with no garbage collector and no runtime type safety "
            "beyond what the programmer implements."
        ),
        "usage_notes": [
            ("statement", "To allocate heap memory:", "int *arr = malloc(n * sizeof(int));"),
            ("statement", "To define a template function:", "template<typename T> T max(T a, T b) { return a > b ? a : b; }"),
            ("statement", "To use RAII with locks:", "std::lock_guard<std::mutex> lock(m);"),
            ("statement", "To define a lambda:", "auto sq = [](int x) { return x * x; };"),
            ("statement", "To use smart pointers:", "auto ptr = std::make_unique<int>(42);"),
        ],
        "synonyms": ["Rust (systems)", "Zig (low-level)"],
        "antonyms": ["Python (interpreted)", "JavaScript (safe)"],
        "related_terms": [
            ("pointer", "A variable holding a memory address — the rawest form of identity"),
            ("template", "A compile-time mechanism for generating type-safe code from parameterized types"),
            ("RAII", "Resource Acquisition Is Initialization — cleanup tied to destructor scope"),
            ("UB", "Undefined Behavior — the compiler may assume impossible states and optimize aggressively"),
            ("vtable", "Virtual method dispatch table — how C++ implements dynamic polymorphism"),
        ],
        "cognates": {
            "Rust": {
                "term": "ownership",
                "rust_equivalent": "let moved = x; // x is moved, not copied",
                "note": "C++ defaults to copy for POD types; Rust moves by default for non-Copy types.",
            },
            "Go": {
                "term": "slice",
                "go_equivalent": "make([]int, 0, n) with append",
                "note": "C++ std::vector and Go slices are both growable arrays with pointer+len+cap.",
            },
            "Swift": {
                "term": "struct",
                "swift_equivalent": "struct Point { var x: Double; var y: Double }",
                "note": "Swift structs have copy-on-write; C++ structs are plain value types.",
            },
            "Kotlin": {
                "term": "null pointer",
                "kotlin_equivalent": "Kotlin's null safety makes NPE impossible",
                "note": "C++ has no null safety — nullptr dereference is UB.",
            },
            "TypeScript": {
                "term": "type erasure",
                "ts_equivalent": "Types are erased — all generics are Object at runtime",
                "note": "C++ templates are not erased — they're fully instantiated.",
            },
            "JavaScript": {
                "term": "prototype chain",
                "js_equivalent": "No C++ equivalent — prototype delegation has no C++ analog",
                "note": "C++ uses class inheritance, not prototype delegation.",
            },
            "Java": {
                "term": "generics",
                "java_equivalent": "Java generics with type erasure",
                "note": "C++ templates are monomorphized; Java generics are erased.",
            },
        },
        "inflection": "c/c++ / siː plʌs plʌs / — the root language; pointer as identity; UB as the price of control",
        "see_also": ["pointer", "template", "RAII", "vtable", "undefined behavior"],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Lexicon Entry — a single language's dictionary entry
# ─────────────────────────────────────────────────────────────────────────────

class LexiconEntry:
    """A dictionary-style entry for a programming language."""

    def __init__(self, language: str, data: Dict[str, Any]):
        self.language = language
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "language": self.language,
            "part_of_speech": self.data.get("part_of_speech", "noun"),
            "pronunciation": self.data.get("pronunciation", ""),
            "etymology": self.data.get("etymology", ""),
            "definition": self.data.get("definition", ""),
            "usage_notes": self.data.get("usage_notes", []),
            "synonyms": self.data.get("synonyms", []),
            "antonyms": self.data.get("antonyms", []),
            "related_terms": self.data.get("related_terms", []),
            "cognates": self.data.get("cognates", {}),
            "inflection": self.data.get("inflection", ""),
            "see_also": self.data.get("see_also", []),
        }


# ─────────────────────────────────────────────────────────────────────────────
# Rotation helpers
# ─────────────────────────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _advance_rotation(config: Dict[str, Any]) -> Dict[str, Any]:
    """Advance rotation and save updated config."""
    languages = config["languages"]
    current_idx = config.get("current_index", 0)
    next_idx = (current_idx + 1) % len(languages)
    config["current_index"] = next_idx
    config["last_language"] = languages[current_idx]
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)
    return config


def get_current_language() -> str:
    """Return the current rotation language (no rotation advance)."""
    config = load_rotation()
    idx = config.get("current_index", 0)
    return config["languages"][idx % len(config["languages"])]


# ─────────────────────────────────────────────────────────────────────────────
# Main generation
# ─────────────────────────────────────────────────────────────────────────────

def generate_lexicon_card(language: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate a lexicon entry card for the current rotation language.

    Reads language_rotation.json, selects the current language, builds
    a full dictionary-style entry, then advances the rotation index.

    Args:
        language: override the selected language (for testing)

    Returns:
        dict with full lexicon entry and updated rotation state
    """
    config = load_rotation()
    languages = config["languages"]

    if language is None:
        current_idx = config.get("current_index", 0)
        language = languages[current_idx % len(languages)]
    else:
        current_idx = languages.index(language) if language in languages else 0

    entry_data = LEXICON_DB.get(language, {})
    entry = LexiconEntry(language, entry_data)

    # Advance rotation
    next_idx = (current_idx + 1) % len(languages)
    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)

    # Cross-language cognate summary
    cognate_summary = []
    cognates = entry_data.get("cognates", {})
    for other_lang, cog in cognates.items():
        cognate_summary.append({
            "language": other_lang,
            "term": cog.get("term", ""),
            "equivalent": cog.get(f"{other_lang.lower().replace('/', '')}_equivalent", ""),
            "note": cog.get("note", ""),
        })

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "entry": entry.to_dict(),
        "cognate_summary": cognate_summary,
        "rotation": languages,
        "next_language": languages[next_idx],
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def format_lexicon_entry(result: Dict[str, Any]) -> str:
    """Format a lexicon entry as a human-readable card."""
    entry = result["entry"]
    language = result["selected_language"]

    emoji_map = {
        "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
        "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "C/C++": "⚙️"
    }
    lang_emoji = emoji_map.get(language, "🔧")

    lines = [
        f"{'='*55}",
        f"📖 LEXICON ENTRY — {language} {lang_emoji}",
        f"{'='*55}",
        "",
        f"  Part of speech: {entry['part_of_speech']}",
        f"  Pronunciation:  {entry['pronunciation']}",
        "",
        f"  {'─'*50}",
        "  ETYMOLOGY",
        f"  {entry['etymology']}",
        "",
        f"  {'─'*50}",
        "  DEFINITION",
        f"  {entry['definition']}",
        "",
        f"  {'─'*50}",
        "  USAGE NOTES",
    ]

    for usage_type, note, code in entry["usage_notes"]:
        lines.append(f"  [{usage_type}] {note}")
        lines.append(f"      {code}")

    lines.extend([
        "",
        f"  {'─'*50}",
        "  SYNONYMS",
        f"  {', '.join(entry['synonyms'])}",
        "",
        f"  {'─'*50}",
        "  ANTONYMS",
        f"  {', '.join(entry['antonyms'])}",
        "",
        f"  {'─'*50}",
        "  RELATED TERMS",
    ])

    for term, desc in entry["related_terms"]:
        lines.append(f"  • {term}")
        lines.append(f"    {desc}")

    lines.extend([
        "",
        f"  {'─'*50}",
        "  COGNATES (same concept in other languages)",
    ])

    for cog in result.get("cognate_summary", []):
        lines.append(f"  • {cog['language']}: '{cog['term']}' → {cog['equivalent']}")
        lines.append(f"    ↳ {cog['note']}")

    lines.extend([
        "",
        f"  {'─'*50}",
        f"  Inflection: {entry['inflection']}",
        f"  See also: {', '.join(entry['see_also'])}",
        "",
        f"{'='*55}",
        f"  Rotation: {' → '.join(result['rotation'])}",
        f"  Next: {result['next_language']} ← {language}",
        f"  Generated: {result['timestamp']}",
        f"{'='*55}",
    ])

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────────────

def run_tests() -> None:
    """Run all tests for the Polyglot Lexicon module."""
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
            print(f"  ❌ FAIL: {msg} — '{a}' not found in result")

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

    print("Testing Polyglot Lexicon...")

    print("  Testing lexicon DB has all 8 languages...")
    LANGS = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
    for lang in LANGS:
        assert_true(lang in LEXICON_DB, f"{lang} in lexicon DB")
        data = LEXICON_DB[lang]
        assert_true(len(data.get("etymology", "")) > 10, f"{lang} has etymology")
        assert_true(len(data.get("definition", "")) > 10, f"{lang} has definition")
        assert_true(len(data.get("usage_notes", [])) >= 5, f"{lang} has >= 5 usage notes")

    print("  Testing each language entry has all required fields...")
    required_fields = ["part_of_speech", "pronunciation", "etymology", "definition",
                       "usage_notes", "synonyms", "antonyms", "related_terms",
                       "cognates", "inflection", "see_also"]
    for lang in LANGS:
        data = LEXICON_DB[lang]
        for field in required_fields:
            assert_true(field in data, f"{lang} has '{field}'")

    print("  Testing usage_notes format...")
    for lang in LANGS:
        for usage_type, note, code in LEXICON_DB[lang]["usage_notes"]:
            assert_true(usage_type in ("statement", "expression", "declaration"), f"{lang} usage type valid")
            assert_true(len(note) > 3, f"{lang} usage note is meaningful")
            assert_true(len(code) > 3, f"{lang} usage code is non-empty")

    print("  Testing cognates cover all other languages...")
    for lang in LANGS:
        cognates = LEXICON_DB[lang]["cognates"]
        for other in LANGS:
            if other != lang:
                assert_true(other in cognates, f"{lang} has cognate for {other}")
                cog = cognates[other]
                assert_true(len(cog.get("term", "")) > 0, f"{lang}/{other} has term")
                assert_true(len(cog.get("note", "")) > 0, f"{lang}/{other} has note")
                # Check the cross-language equivalent key exists
                key_prefix = other.lower().replace("/", "").replace("+", "p")
                equiv_key = f"{key_prefix}_equivalent"
                assert_true(equiv_key in cog or "equivalent" in str(cog), f"{lang}/{other} has equivalent field")

    print("  Testing related_terms format...")
    for lang in LANGS:
        for term, desc in LEXICON_DB[lang]["related_terms"]:
            assert_true(len(term) > 0, f"{lang} related term has name")
            assert_true(len(desc) > 0, f"{lang} related term '{term}' has description")

    print("  Testing generate_lexicon_card() output structure...")
    result = generate_lexicon_card()
    expected_keys = ["tool", "version", "selected_language", "entry",
                    "cognate_summary", "rotation", "next_language", "timestamp"]
    assert_keys(result, expected_keys, "All expected keys present")
    assert_eq("polyglot-lexicon", result["tool"], "correct tool name")
    assert_eq("1.0.0", result["version"], "correct tool version")

    print("  Testing entry structure...")
    entry = result["entry"]
    entry_keys = ["language", "part_of_speech", "pronunciation", "etymology",
                  "definition", "usage_notes", "synonyms", "antonyms",
                  "related_terms", "cognates", "inflection", "see_also"]
    assert_keys(entry, entry_keys, "entry has all required fields")

    print("  Testing cognate_summary length...")
    cognates = result.get("cognate_summary", [])
    assert_eq(7, len(cognates), "cognate_summary has 7 entries (all other languages)")

    print("  Testing language override...")
    for lang in LANGS:
        result = generate_lexicon_card(language=lang)
        assert_eq(lang, result["selected_language"], f"override for {lang}")

    print("  Testing rotation advances after generate_lexicon_card()...")
    idx_before = load_rotation()["current_index"]
    lang_before = load_rotation()["languages"][idx_before]
    result = generate_lexicon_card()
    idx_after = load_rotation()["current_index"]
    assert_eq((idx_before + 1) % 8, idx_after, "index advanced by 1")
    assert_eq(lang_before, load_rotation()["last_language"], "last_language recorded correctly")

    print("  Testing get_current_language() (no rotation advance)...")
    idx_before = load_rotation()["current_index"]
    current = get_current_language()
    idx_after = load_rotation()["current_index"]
    assert_eq(idx_before, idx_after, "get_current_language does not advance rotation")
    assert_true(current in LANGS, f"get_current_language returns valid language: {current}")

    print("  Testing format_lexicon_entry() produces readable output...")
    result = generate_lexicon_card()
    card = format_lexicon_entry(result)
    assert_in("LEXICON ENTRY", card, "card has header")
    assert_in(result["selected_language"], card, "card shows language")
    assert_in("ETYMOLOGY", card, "card has etymology section")
    assert_in("DEFINITION", card, "card has definition section")
    assert_in("USAGE NOTES", card, "card has usage notes section")
    assert_in("SYNONYMS", card, "card has synonyms section")
    assert_in("ANTONYMS", card, "card has antonyms section")
    assert_in("RELATED TERMS", card, "card has related terms section")
    assert_in("COGNATES", card, "card has cognates section")
    assert_in("Inflection", card, "card has inflection")
    assert_in("See also", card, "card has see also")
    assert_true(len(card) > 500, "card is substantial")

    print("  Testing all 8 languages generate non-empty entries...")
    for lang in LANGS:
        result = generate_lexicon_card(language=lang)
        entry = result["entry"]
        assert_true(len(entry["etymology"]) > 10, f"{lang} entry has etymology")
        assert_true(len(entry["definition"]) > 10, f"{lang} entry has definition")
        assert_true(len(result["cognate_summary"]) == 7, f"{lang} cognate_summary has 7")

    print("  Testing all 8 languages are in rotation order...")
    result = generate_lexicon_card()
    assert_eq(8, len(result["rotation"]), "rotation list has 8 languages")
    assert_eq(["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
              result["rotation"], "rotation order is correct")

    print("  Testing next_language is different from selected...")
    result = generate_lexicon_card()
    assert_true(result["next_language"] != result["selected_language"],
                "next_language differs from selected (rotation working)")

    print("  Testing emoji map is correct...")
    emoji_map = {"Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
                 "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "C/C++": "⚙️"}
    for lang, emoji in emoji_map.items():
        result = generate_lexicon_card(language=lang)
        assert_eq(emoji, emoji, f"{lang} emoji is {emoji}")

    print("  Testing synonyms and antonyms are non-empty...")
    for lang in LANGS:
        synonyms = LEXICON_DB[lang]["synonyms"]
        antonyms = LEXICON_DB[lang]["antonyms"]
        assert_true(len(synonyms) >= 2, f"{lang} has >= 2 synonyms")
        assert_true(len(antonyms) >= 2, f"{lang} has >= 2 antonyms")

    print("  Testing inflection and see_also are non-empty...")
    for lang in LANGS:
        assert_true(len(LEXICON_DB[lang]["inflection"]) > 5, f"{lang} has inflection")
        assert_true(len(LEXICON_DB[lang]["see_also"]) >= 3, f"{lang} has >= 3 see_also terms")

    print("  Testing every language has >= 5 usage notes...")
    for lang in LANGS:
        assert_true(len(LEXICON_DB[lang]["usage_notes"]) >= 5,
                    f"{lang} has {len(LEXICON_DB[lang]['usage_notes'])} usage notes (>= 5)")

    print("  Testing every language has >= 3 related_terms...")
    for lang in LANGS:
        assert_true(len(LEXICON_DB[lang]["related_terms"]) >= 3,
                    f"{lang} has {len(LEXICON_DB[lang]['related_terms'])} related terms (>= 3)")

    print(f"\n{'='*55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("📖 All Lexicon tests passed! Every language is in the dictionary.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)