#!/usr/bin/env python3
"""
🏛️ Language Archaeology v1.0
A creative tool that digs into the historical roots, design philosophy,
and evolutionary lineage of programming languages.

Creative concept: "Every language has a story. This tool tells it."
Each language is examined through the lens of:
  - Origins & Creators
  - Design Philosophy (the "why")
  - Ancestral DNA (ideas borrowed from predecessors)
  - Philosophical Signature (the core ethos)
  - Archaeological Finds (landmarks/version milestones)
  - Cross-pollination (which languages it influenced)

Distinct from existing tools:
  - language_compass: learning journey maps (milestones)
  - language_ecohub: package ecosystem field guide
  - language_sage: idioms, pro tips, pitfalls
  - language_mastery: XP/level progress tracking

Archaeology is about TIME and HISTORY — a different dimension entirely.
"""

import json
import os
from datetime import datetime

TOOL_NAME = "language-archaeology"
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


# ── Archaeology data per language ─────────────────────────────────────────────
ARCHAEOLOGY_DATA = {
    "Rust": {
        "origins": {
            "created_by": "Graydon Hoare (Mozilla)",
            "year_born": 2006,
            "first_release": "May 2010 (0.1)",
            "inspired_by": ["ML", "Haskell", "C++", "Newsqueak", "Axiom"],
            "born_from_question": "What if you could have memory safety without a garbage collector?",
        },
        "philosophy": {
            "tagline": "Fearless concurrency.",
            "core_ethos": "Zero-cost abstractions, memory safety without GC, and fearless concurrency.",
            "design_principles": [
                "Memory safety without garbage collection through ownership & borrowing",
                "Abstractions that cost nothing (zero-cost principle)",
                "Fearless concurrency — no data races at compile time",
                "Explicit over implicit (lifetimes are visible)",
                "Prefer composition over inheritance",
            ],
            "philosophical_signature": "The borrow checker is not your enemy — it's a formal proof of correctness.",
        },
        "ancestral_dna": [
            {"concept": "Ownership & Borrowing", "ancestor": "ML family (1973)", "description": "Linear types and region-based memory management"},
            {"concept": "Zero-cost Abstractions", "ancestor": "C++ (Stroustrup, 1983)", "description": "Abstractions that compile to equivalent machine code"},
            {"concept": "Type Inference", "ancestor": "ML (1973)", "description": "Hindley-Milner type inference, finally done right in a systems language"},
            {"concept": "Pattern Matching", "ancestor": "ML / Prolog", "description": "Exhaustive pattern matching as a correctness tool"},
            {"concept": "Async/Await via Futures", "ancestor": "Futures in LISP / Kahn Networks", "description": "Composable asynchronous programming"},
        ],
        "landmarks": [
            {"version": "1.0", "year": 2015, "event": "First stable release — 'Rust is ready for production'"},
            {"version": "2018 Edition", "year": 2018, "event": "Ownership system simplified; async/await stabilized in 2019"},
            {"version": "1.56", "year": 2021, "event": "Edition 2021: panic in Drop, const generics stable"},
            {"version": "Rust 2024 Edition", "year": 2024, "event": "Async closures, refined borrow checker (polonius)"},
        ],
        "cross_pollination": {
            "influenced": ["Carbon", "Zig", "Swift (memory model)", "C++ (concepts borrowing from traits)", "Vale"],
            "ideas_taken_from_others": [
                ("Haskell", "Algebraic data types, trait system, pure functions"),
                ("C++", "RAII, zero-cost abstractions, move semantics"),
                ("Erlang", "Message-passing concurrency model"),
            ],
        },
        "archaeological_finds": [
            "The 'triangle of death' problem (reference cycles) led to Arc<Mutex<T>> as a solution",
            "Rust's trait system is like Haskell's typeclasses — but with coherence rules",
            "The first Rust compiler was written in OCaml, not Rust itself",
            "Rust holds the title for 'most loved language' on StackOverflow for 9+ consecutive years",
        ],
        "dig_quote": "To understand Rust is to understand why memory safety must be a compile-time property, not a runtime convention.",
    },
    "Go": {
        "origins": {
            "created_by": "Robert Griesemer, Rob Pike, Ken Thompson (Google)",
            "year_born": 2009,
            "first_release": "March 2012 (Go 1.0)",
            "inspired_by": ["C", "Pascal", "Newsqueak", "Alef", "Python", "Smalltalk"],
            "born_from_question": "Can a language for large-scale Google services be both expressive and compile fast?",
        },
        "philosophy": {
            "tagline": "Simple, reliable, efficient.",
            "core_ethos": "Go was designed to solve Google's internal scaling problems: thousands of engineers, massive codebases, fast builds.",
            "design_principles": [
                "Simplicity — one way to do things, not many",
                "Composition over inheritance — no classes, only interfaces",
                "Concurrency built into the language (goroutines + channels)",
                "Fast compilation as a first-class goal",
                "Garbage collection — but with low latency (sub-1ms pauses)",
            ],
            "philosophical_signature": "C's spirit in a modern syntax, with concurrency that makes parallelism trivial.",
        },
        "ancestral_dna": [
            {"concept": "Goroutines & Channels", "ancestor": "CSP (Hoare, 1978) / Newsqueak (Pike, 1988)", "description": "Communicating Sequential Processes — processes that communicate, not share memory"},
            {"concept": "Interfaces (implicit)", "ancestor": "Plan 9 / Alef", "description": "No explicit declaration needed — satisfaction is implicit"},
            {"concept": "defer statement", "ancestor": "Lisp (unwind-protect) / Pascal (finally)", "description": "Postponed execution for guaranteed cleanup"},
            {"concept": "Fast compilation", "ancestor": "C (single-pass design)", "description": "Go's compiler was designed to never be a bottleneck"},
            {"concept": "Error values (not exceptions)", "ancestor": "C (error return codes)", "description": "Errors are values — handle them explicitly"},
        ],
        "landmarks": [
            {"version": "Go 1.0", "year": 2012, "event": "First stable release. Compatibility promise born."},
            {"version": "Go 1.5", "year": 2015, "event": "Compiler rewritten in Go (self-hosting). GC latency improved dramatically."},
            {"version": "Go 1.18", "year": 2022, "event": "Generics finally shipped — the most requested feature in Go history"},
            {"version": "Go 1.22", "year": 2024, "event": "Improved range-over-func, routing pattern matching in net/http"},
        ],
        "cross_pollination": {
            "influenced": ["Gleam", "Zig (comptime)", "Cloudflare's Pingora", "Caddy"],
            "ideas_taken_from_others": [
                ("C", "Syntax roots, fast compilation philosophy, error-as-value"),
                ("Python", "Lightweight syntax, quick scripting"),
                ("Smalltalk", "Message-passing object model (via Newsqueak lineage)"),
            ],
        },
        "archaeological_finds": [
            "Go's interfaces were inspired by Plan 9's灵活的接口 concept — types just declare what they implement",
            "The original Go compiler was written in C; the current one (gc) is written in Go itself",
            "Rob Pike famously said: 'Go is a language for people who take programming seriously but not language design seriously'",
            "goroutines were inspired by 'processes as communication' — not threads or coroutines",
        ],
        "dig_quote": "Go is the archaeological dig site where C's pragmatism meets CSP's elegance — and neither was supposed to win.",
    },
    "Swift": {
        "origins": {
            "created_by": "Chris Lattner & Apple (with influence from Objective-C, Rust, Python, C#)",
            "year_born": 2010,
            "first_release": "June 2014 (Swift 1.0 for iOS/Mac developers)",
            "inspired_by": ["Objective-C", "Rust", "Python", "C#", "Haskell", "Ruby"],
            "born_from_question": "Can we have the safety of a modern language and the power of Objective-C, without the legacy baggage?",
        },
        "philosophy": {
            "tagline": "Safe, fast, expressive.",
            "core_ethos": "Swift was designed to replace Objective-C for Apple platform development, offering memory safety without a runtime overhead.",
            "design_principles": [
                "Safe by default — no uninitialized variables, no nil without Optional",
                "Fast — compiles to native code, comparable to C",
                "Expressive — modern syntax that reads like pseudocode",
                "Protocol-oriented — protocols over class inheritance",
                "Memory-safe — ARC without the cycle problems of manual retain/release",
            ],
            "philosophical_signature": "Protocols are the architecture; classes are a detail.",
        },
        "ancestral_dna": [
            {"concept": "Optionals", "ancestor": "Haskell Maybe / Rust Option", "description": "Making null explicit rather than a hidden trapdoor"},
            {"concept": "Protocol-Oriented Programming", "ancestor": "Go interfaces + CLU (Liskov, 1975)", "description": "Behavior defined by what you can do, not what you inherit"},
            {"concept": "ARC Memory Management", "ancestor": "Objective-C (manual retain/release)", "description": "Automatic Reference Counting — compile-time, not runtime overhead"},
            {"concept": "Generics", "ancestor": "C++ templates / Haskell typeclasses", "description": "Powerful generic programming with constraints"},
            {"concept": "Async/Await", "ancestor": "C# async/await (2007)", "description": "Sequential-looking async code without callback hell"},
        ],
        "landmarks": [
            {"version": "Swift 1.0", "year": 2014, "event": "First public release — iOS 8 and OS X Yosemite"},
            {"version": "Swift 2.0", "year": 2015, "event": "Error handling with try/catch/throw, protocol extensions"},
            {"version": "Swift 5.0", "year": 2019, "event": "ABI stability, async/await, result builders"},
            {"version": "Swift 6.0", "year": 2024, "event": "Complete concurrency checking, typed throws, noncopyable types"},
        ],
        "cross_pollination": {
            "influenced": ["SwiftUI (declarative UI)", "Rust (async/await design)", "Kotlin (result builders inspiration)", "Python (syntactic sugar for ergonomics)"],
            "ideas_taken_from_others": [
                ("Rust", "Ownership model, borrowing, memory safety philosophy"),
                ("Python", "Clean syntax, list comprehensions, named parameters"),
                ("C#", "Async/await pattern, LINQ-like collection methods"),
            ],
        },
        "archaeological_finds": [
            "Swift's earliest prototype was written in C++ — and it showed in early syntax",
            "Chris Lattner originally pitched the Swift design to Apple as a 'safer Objective-C' in 2010",
            "Swift's protocol extensions came from the CLU language by Barbara Liskov (1975) — decades before Swift existed",
            "Swift is the first mainstream language to combine ARC (safety), async/await (ergonomics), and native performance",
        ],
        "dig_quote": "Swift is what Objective-C would have become if it had been redesigned in 2010 with Rust's safety philosophy.",
    },
    "Kotlin": {
        "origins": {
            "created_by": "JetBrains (Dmitry Jemerov, Andrey Breslav)",
            "year_born": 2011,
            "first_release": "February 2016 (Kotlin 1.0)",
            "inspired_by": ["Java", "Scala", "Groovy", "C#", "Python", " Gosu"],
            "born_from_question": "Can we have a JVM language that's more concise than Java, safer than Scala, and compiles as fast as Java?",
        },
        "philosophy": {
            "tagline": "Concise, safe, interoperable.",
            "core_ethos": "Kotlin was built to be a better Java — pragmatic, concise, null-safe, and fully interoperable with existing Java code.",
            "design_principles": [
                "100% interoperable with Java — call Java from Kotlin and vice versa seamlessly",
                "Null safety at the type system level (Nullable vs non-null types)",
                "Coroutines for async — structured concurrency without callback hell",
                "Smart casts — the compiler tracks type narrowing within blocks",
                "Extension functions — add methods to existing classes without inheritance",
            ],
            "philosophical_signature": "Pragmatic modern features on the JVM, with Java interoperability as a non-negotiable constraint.",
        },
        "ancestral_dna": [
            {"concept": "Extension Functions", "ancestor": "C# extension methods (2007)", "description": "Adding methods to closed classes without inheritance"},
            {"concept": "Coroutines", "ancestor": "Google's Go / Python asyncio / C# async", "description": "Structured concurrency with suspend functions"},
            {"concept": "Data Classes", "ancestor": "Scala case classes / Python dataclasses", "description": "Auto-generate equals, hashCode, toString, copy"},
            {"concept": "Null Safety", "ancestor": "Scala Option / Haskell Maybe", "description": "Type系统在编译时区分可空和不可空"},
            {"concept": "Sealed Classes", "ancestor": "F# discriminated unions / Scala sealed traits", "description": "Exhaustive when expressions without default branches"},
        ],
        "landmarks": [
            {"version": "Kotlin 1.0", "year": 2016, "event": "First stable release — JetBrains commits to backward compatibility"},
            {"version": "Kotlin 1.3", "year": 2018, "event": "Coroutines for async — stable, production-ready"},
            {"version": "Kotlin 1.5", "year": 2021, "event": "Stable inline classes, improvements to JVM IR backend"},
            {"version": "Kotlin 2.0", "year": 2024, "event": "K2 compiler (new frontend), Compose Multiplatform GA"},
        ],
        "cross_pollination": {
            "influenced": ["Kotlin Multiplatform (shared business logic)", "Compose Multiplatform", "Ktor (web framework)", "Fuel (HTTP client)"],
            "ideas_taken_from_others": [
                ("Scala", "Implicit conversions, lazy vals, traits"),
                ("C#", "Extension methods, null-conditional operator (?.)"),
                ("Python", "String templates, named parameters with defaults"),
            ],
        },
        "archaeological_finds": [
            "Kotlin was originally designed to run on the JVM, but also targets JavaScript and native (LLVM)",
            "The name 'Kotlin' comes from Kotlin Island near St. Petersburg — inspired by Java's island naming",
            "JetBrains originally tried to use Scala but found compilation too slow — so they built Kotlin",
            "Kotlin's null safety was influenced by the billion-dollar mistake (Tony Hoare's null reference)",
        ],
        "dig_quote": "Kotlin is the archaeological record of what Java could have become if the language had a decade of reflection.",
    },
    "TypeScript": {
        "origins": {
            "created_by": "Microsoft (Anders Hejlsberg, creator of C# and Delphi)",
            "year_born": 2012,
            "first_release": "October 2012 (TypeScript 0.8)",
            "inspired_by": ["JavaScript", "C#", "Java", "ML", "Haskell"],
            "born_from_question": "Can we add a powerful type system to JavaScript without breaking the web?",
        },
        "philosophy": {
            "tagline": "JavaScript that scales.",
            "core_ethos": "TypeScript is a syntactic superset of JavaScript that adds optional static typing and class-based object-oriented programming.",
            "design_principles": [
                "Valid JavaScript is valid TypeScript — gradual adoption is the key",
                "Optional static types that disappear at runtime",
                "Compiles to plain JavaScript (ES3+), works in any browser",
                "Class-based OOP with interfaces, inheritance, access modifiers",
                "Structural typing — compatibility is based on shape, not name",
            ],
            "philosophical_signature": "Types are documentation that the compiler verifies — they never lie and never go stale.",
        },
        "ancestral_dna": [
            {"concept": "Static Typing", "ancestor": "C# / Java", "description": "Types checked at compile time, not runtime"},
            {"concept": "Type Inference", "ancestor": "ML / Haskell", "description": "Hindley-Milner inference, adapted for JavaScript's dynamic roots"},
            {"concept": "Structural Typing", "ancestor": "Go interfaces / OCaml polymorphic variants", "description": "Types are compatible if shapes match, not nominal names"},
            {"concept": "Decorators", "ancestor": "Python decorators / Java annotations", "description": "Meta-programming via function composition on declarations"},
            {"concept": "Generics", "ancestor": "C++ templates / Java generics", "description": "Parametric polymorphism with constraint support"},
        ],
        "landmarks": [
            {"version": "TypeScript 0.9", "year": 2013, "event": "Generics introduced — the type system grows teeth"},
            {"version": "TypeScript 2.0", "year": 2016, "event": "Non-nullable types, control flow analysis, tagged union types"},
            {"version": "TypeScript 4.0", "year": 2020, "event": "Variadic tuple types, labeled tuple elements, class property inference"},
            {"version": "TypeScript 5.0", "year": 2023, "event": "Decorators (ES2022 stage 3), const type parameters, speed improvements"},
        ],
        "cross_pollination": {
            "influenced": ["Angular (adopted TypeScript)", "Vue 3", "Microsoft's own VS Code", "tsx/bun", "OxC (Rust-powered TypeScript compiler)"],
            "ideas_taken_from_others": [
                ("C#", "Namespaces, enums, async/await (which C# borrowed from F#)"),
                ("Haskell", "Type inference, algebraic data types via union types"),
                ("JavaScript", "Prototype inheritance, dynamic typing, runtime evaluation"),
            ],
        },
        "archaeological_finds": [
            "Anders Hejlsberg created TypeScript after working on C# — his first major work was Turbo Pascal",
            "TypeScript's structural typing was chosen over nominal typing (like C#/Java) for JavaScript compatibility",
            "TypeScript's type system is Turing complete — you can compute at the type level",
            "Before TypeScript, Microsoft tried a different approach called 'AtScript' which included type annotations",
        ],
        "dig_quote": "TypeScript is the archaeological evidence that JavaScript could have been designed with types from the beginning — and that the web would have been safer for it.",
    },
    "JavaScript": {
        "origins": {
            "created_by": "Brendan Eich (Netscape)",
            "year_born": 1995,
            "first_release": "December 1995 (JavaScript 1.0 in Netscape Navigator 2.0)",
            "inspired_by": ["Self", "Scheme", "Perl", "AWK", "Java"],
            "born_from_question": "Can we make a scripting language that designers and non-programmers can use in web pages?",
        },
        "philosophy": {
            "tagline": "The language of the web.",
            "core_ethos": "JavaScript was written in 10 days in 1995. It was meant to be a simple scripting language for non-programmers. It accidentally became the world's most widely deployed runtime.",
            "design_principles": [
                "Prototype-based inheritance — objects inherit directly from other objects",
                "First-class functions — functions are values, passed around like any other",
                "Dynamic typing — no compile-time checks, everything resolves at runtime",
                "Event loop & non-blocking I/O — single-threaded but asynchronous",
                "Function scoping (not block scoping) — var declarations are hoisted",
            ],
            "philosophical_signature": "JavaScript was designed to be understood by humans, not machines — which is why it has quirks.",
        },
        "ancestral_dna": [
            {"concept": "Prototypal Inheritance", "ancestor": "Self (1994)", "description": "Objects inherit directly from other objects, not from classes"},
            {"concept": "First-Class Functions", "ancestor": "Scheme (1975)", "description": "Functions as values — stored, passed, returned"},
            {"concept": "Closures", "ancestor": "Scheme / Lisp", "description": "Functions capture their lexical environment"},
            {"concept": "RegExp", "ancestor": "Perl (1987)", "description": "JavaScript borrowed Perl's regular expression syntax almost wholesale"},
            {"concept": "JSON (as a data format)", "ancestor": "Java (primitive types) + JavaScript object literals", "description": "JSON was born from JavaScript object literal syntax, now universal"},
        ],
        "landmarks": [
            {"version": "ES3 (ECMAScript 3)", "year": 1999, "event": "try/catch,正则表达式, try/catch, in/dynamic evaluation — the language stabilizes"},
            {"version": "ES5", "year": 2009, "event": "Strict mode, JSON built-in, array extras — jQuery era"},
            {"version": "ES6/ES2015", "year": 2015, "event": "Classes, arrow functions, Promises, let/const, generators — the modern era begins"},
            {"version": "ES2020+", "year": 2020, "event": "Optional chaining, nullish coalescing, BigInt, top-level await — JavaScript grows up"},
        ],
        "cross_pollination": {
            "influenced": ["Node.js", "Deno", "Bun (all JS runtimes)", "TypeScript (superset)", "Webpack/Bundlers", "React/Vue/Angular"],
            "ideas_taken_from_others": [
                ("Self", "Prototype chain, object literals"),
                ("Perl", "Regular expressions, string interpolation"),
                ("Scheme", "First-class functions, closures, read-evaluate-print loop"),
            ],
        },
        "archaeological_finds": [
            "Brendan Eich created JavaScript in 10 days in September 1995 — originally called 'Mocha', then 'LiveScript'",
            "Java and JavaScript share only the first 4 letters — they're completely unrelated languages",
            "The 'this' keyword in JavaScript was modeled after Java's — but with a fundamentally different runtime semantics",
            "NaN in JavaScript is actually a number (typeof NaN === 'number') and NaN !== NaN — by design",
        ],
        "dig_quote": "JavaScript is a dig site where Scheme's elegance meets Self's prototype inheritance, buried under layers of web history.",
    },
    "Java": {
        "origins": {
            "created_by": "James Gosling & Sun Microsystems",
            "year_born": 1995,
            "first_release": "January 1996 (JDK 1.0)",
            "inspired_by": ["C++", "Objective-C", "Smalltalk", "Ada", "Modula-3"],
            "born_from_question": "Can we build a language that's 'write once, run anywhere' — without recompiling for each platform?",
        },
        "philosophy": {
            "tagline": "Write once, run anywhere.",
            "core_ethos": "Java was designed to be a consumer electronics language — simple, object-oriented, and platform-independent via the JVM.",
            "design_principles": [
                "Simple — no pointer arithmetic, automatic memory management",
                "Object-oriented — everything is an object (except primitives)",
                "Platform-independent — compiled to bytecode, run on any JVM",
                "Strongly typed — no implicit casts that lose precision",
                "Multithreaded — built-in concurrency support from day one",
            ],
            "philosophical_signature": "The JVM is the great equalizer — one bytecode, every platform.",
        },
        "ancestral_dna": [
            {"concept": "Garbage Collection", "ancestor": "Lisp (1958)", "description": "Automatic memory management — no explicit free()"},
            {"concept": "JVM Bytecode", "ancestor": "UCSD Pascal P-System", "description": "Compile to intermediate code, interpret on any platform"},
            {"concept": "Class-based OOP", "ancestor": "C++ / Smalltalk", "description": "Everything is an object (except primitives), classes as blueprints"},
            {"concept": "Interfaces", "ancestor": "Objective-C protocols", "description": "Pure abstraction — no implementation, multiple inheritance of type"},
            {"concept": "Checked Exceptions", "ancestor": "Modula-3", "description": "Compile-time enforcement of exception handling — a controversial choice"},
        ],
        "landmarks": [
            {"version": "Java 1.0", "year": 1996, "event": "First public release. Applets bring Java to web browsers."},
            {"version": "Java 5.0 (Tiger)", "year": 2004, "event": "Generics, annotations, autoboxing, enums, for-each loop — the language modernizes"},
            {"version": "Java 8", "year": 2014, "event": "Lambda expressions, Stream API, Optional, Nashorn JS engine — functional Java"},
            {"version": "Java 21 (LTS)", "year": 2023, "event": "Virtual threads (GA), pattern matching for switch, record patterns"},
        ],
        "cross_pollination": {
            "influenced": ["Kotlin", "Scala", "Clojure", "Groovy", "Android (official language)", "Spring ecosystem"],
            "ideas_taken_from_others": [
                ("C++", "Syntax roots, class concept, operator overloading"),
                ("Smalltalk", "Pure OOP message-passing model (Java simplified it)"),
                ("Ada", "Checked exceptions (a design decision still debated today)"),
            ],
        },
        "archaeological_finds": [
            "Java was originally called 'Oak' — after the oak tree outside James Gosling's office",
            "The 'Green project' at Sun was meant to control set-top boxes — Java went a different direction",
            "Java's checked exceptions were controversial from day one — even James Gosling has said he'd drop them if he could",
            "The JVM was so well-designed that it now runs dozens of languages — Kotlin, Scala, Clojure, Groovy, JRuby",
        ],
        "dig_quote": "Java's archaeological dig reveals that 'write once, run anywhere' was not just a slogan — it was a vision that changed software distribution forever.",
    },
    "C/C++": {
        "origins": {
            "created_by": "Dennis Ritchie (C, 1972) + Bjarne Stroustrup (C++, 1979)",
            "year_born": 1972,
            "first_release": "C: 1978 (K&R book) / C++: 1985 (first commercial release)",
            "inspired_by": ["BCPL (C's ancestor)", "Simula (C++'s ancestor)", "ALGOL", "COBOL"],
            "born_from_question": "C: 'How do we write an OS in a high-level language without losing performance?' / C++: 'How do we add OOP to C without losing C's speed?'",
        },
        "philosophy": {
            "tagline": "C: 'Trust the programmer.' C++: 'Provide zero-overhead abstractions.'",
            "core_ethos": "C is a low-level systems language where you are always in control. C++ adds abstractions that compile away to nothing if you don't use them.",
            "design_principles": [
                "C: 'Trust the programmer' — no safety nets, maximum control",
                "C++: 'You don't pay for what you don't use' — zero-cost abstractions",
                "Prefer value semantics where possible, heap allocation when needed",
                "RAII (Resource Acquisition Is Initialization) — resource management tied to object lifetime",
                "Template metaprogramming — Turing-complete compile-time computation",
            ],
            "philosophical_signature": "In C++, the compiler is a partner, not a babysitter.",
        },
        "ancestral_dna": [
            {"concept": "Pointers & Manual Memory", "ancestor": "BCPL (1971)", "description": "Pointer arithmetic, direct memory access — both C's power and its danger"},
            {"concept": "Classes & Inheritance", "ancestor": "Simula 67 (1967)", "description": "Stroustrup's 'C with Classes' borrowed Simula's class concept"},
            {"concept": "RAII", "ancestor": "C++ original design", "description": "Tying resource management (file handles, locks) to object lifetime via destructors"},
            {"concept": "Templates & Generics", "ancestor": "Ada generics (1983)", "description": "Parametric polymorphism via compile-time code generation"},
            {"concept": "Move Semantics", "ancestor": "C++11 (influenced by Rust's earlier design)", "description": "Avoiding unnecessary copies by transferring ownership of resources"},
        ],
        "landmarks": [
            {"version": "C89/ANSI C", "year": 1989, "event": "First standardized C — the language that built UNIX and Linux"},
            {"version": "C++98 (ISO)", "year": 1998, "event": "First ISO standard — STL, templates, exceptions fully standardized"},
            {"version": "C++11 (Modern C++)", "year": 2011, "event": "Move semantics, smart pointers, lambda, auto, nullptr, threading — renaissance"},
            {"version": "C++20/23", "year": 2020, "event": "Concepts, Ranges, Coroutines, Modules — C++ grows up again"},
        ],
        "cross_pollination": {
            "influenced": ["Rust", "Go (syntax roots)", "Carbon", "Zig", "Swift (value semantics)", "D", "Objective-C"],
            "ideas_taken_from_others": [
                ("Simula 67", "Classes, inheritance, virtual methods"),
                ("BCPL", "Pointer model, expression syntax, block structure"),
                ("ALGOL 68", "Reference parameters, separate compilation"),
            ],
        },
        "archaeological_finds": [
            "C was written to rewrite UNIX in a high-level language — UNIX was originally written in assembly",
            "Dennis Ritchie designed C to be a 'portable assembly' — it worked so well that UNIX became portable",
            "Bjarne Stroustrup created 'C with Classes' in 1979, adding OOP to C — it was later renamed C++",
            "The C preprocessor (macros) was borrowed from ALGOL 68 — it's the most powerful and dangerous tool in C",
        ],
        "dig_quote": "The C/C++ dig site is the deepest in computing history — from this soil, every modern language has grown roots.",
    },
}


def dig(language):
    """
    Main dig function — uncover the archaeological record for the selected language.
    Loads rotation config, builds the archaeological report, advances rotation.
    """
    config = load_rotation()

    if language not in config["languages"]:
        raise ValueError(
            f"Language '{language}' not in rotation. "
            f"Available: {', '.join(config['languages'])}"
        )

    data = ARCHAEOLOGY_DATA.get(language)
    if not data:
        raise ValueError(f"No archaeological data for '{language}'")

    # Build the report
    origins = data["origins"]
    philosophy = data["philosophy"]

    # Calculate language age
    age_years = datetime.now().year - origins["year_born"]

    # Build ancestral DNA chain
    dna_chain = []
    for dna in data["ancestral_dna"]:
        dna_chain.append({
            "concept": dna["concept"],
            "inherited_from": dna["ancestor"],
            "description": dna["description"],
            "generations": f"~{datetime.now().year - 1970 + (origins['year_born'] - 1970)} generations" if origins["year_born"] < 1980 else f"~{datetime.now().year - origins['year_born']} years of refinement"
        })

    # Build cross-pollination summary
    cross = data["cross_pollination"]
    pollination = {
        "languages_this_influenced": cross["influenced"],
        "ideas_borrowed_summary": [
            f"From {source}: {ideas}"
            for source, ideas in cross["ideas_taken_from_others"]
        ],
    }

    # Build milestone timeline
    timeline = [
        f"{lm['year']}: {lm['version']} — {lm['event']}"
        for lm in data["landmarks"]
    ]

    # Build findings
    findings = [
        f"📍 {finding}" for finding in data["archaeological_finds"]
    ]

    # Prepare response
    current_idx = config["languages"].index(language)
    next_idx = (current_idx + 1) % len(config["languages"])

    # Advance rotation: next run selects Go
    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now().isoformat()
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "age_years": age_years,
        "origins": {
            "created_by": origins["created_by"],
            "year_born": origins["year_born"],
            "first_release": origins["first_release"],
            "inspired_by": origins["inspired_by"],
            "born_from_question": origins["born_from_question"],
        },
        "philosophy": {
            "tagline": philosophy["tagline"],
            "core_ethos": philosophy["core_ethos"],
            "design_principles": philosophy["design_principles"],
            "philosophical_signature": philosophy["philosophical_signature"],
        },
        "ancestral_dna": dna_chain,
        "timeline": timeline,
        "cross_pollination": pollination,
        "archaeological_finds": findings,
        "dig_quote": data["dig_quote"],
        "next_language": config["languages"][next_idx],
        "rotation": config["languages"],
        "timestamp": datetime.now().isoformat(),
    }


def run_tests():
    """Run tests to validate the Language Archaeology module."""
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

    print("Testing Language Archaeology...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_eq(True, 0 <= config["current_index"] < 8, "current_index in valid range")
    assert_eq("Rust", config["languages"][0], "Rust is first language")

    print("  Testing dig for Rust...")
    result = dig("Rust")
    expected_keys = [
        "tool", "version", "selected_language", "age_years",
        "origins", "philosophy", "ancestral_dna", "timeline",
        "cross_pollination", "archaeological_finds", "dig_quote",
        "next_language", "rotation", "timestamp"
    ]
    for key in expected_keys:
        assert_eq(True, key in result, f"Key '{key}' present in response")

    assert_eq("Rust", result["selected_language"], "Rust is selected")
    assert_eq("Go", result["next_language"], "Next language is Go")
    assert_eq(TOOL_NAME, result["tool"], "Correct tool name")

    print("  Verifying origins structure...")
    origins = result["origins"]
    assert_true("created_by" in origins, "origins has created_by")
    assert_true("year_born" in origins, "origins has year_born")
    assert_true("first_release" in origins, "origins has first_release")
    assert_true("inspired_by" in origins, "origins has inspired_by")
    assert_true("born_from_question" in origins, "origins has born_from_question")

    print("  Verifying philosophy structure...")
    phil = result["philosophy"]
    assert_true("tagline" in phil, "philosophy has tagline")
    assert_true("core_ethos" in phil, "philosophy has core_ethos")
    assert_true("design_principles" in phil, "philosophy has design_principles")
    assert_true("philosophical_signature" in phil, "philosophy has philosophical_signature")

    print("  Verifying ancestral_dna structure...")
    dna = result["ancestral_dna"]
    assert_true(len(dna) >= 4, f"ancestral_dna has {len(dna)} entries (>= 4)")
    for entry in dna:
        assert_true("concept" in entry, "DNA entry has concept")
        assert_true("inherited_from" in entry, "DNA entry has inherited_from")
        assert_true("description" in entry, "DNA entry has description")

    print("  Verifying Rust-specific content...")
    assert_eq("Graydon Hoare (Mozilla)", result["origins"]["created_by"], "Rust creator is Graydon Hoare")
    assert_eq(2006, result["origins"]["year_born"], "Rust born in 2006")
    assert_true(result["age_years"] >= 18, "Rust is at least 18 years old")
    assert_true(any("Ownership" in d["concept"] for d in dna), "Ownership concept in Rust DNA")
    assert_true(len(result["timeline"]) >= 3, "Rust has >= 3 timeline entries")

    print("  Verifying rotation update...")
    config2 = load_rotation()
    assert_eq(1, config2["current_index"], "Index advanced to 1 (Go)")
    assert_eq("Rust", config2["last_language"], "Last language recorded as Rust")

    print("  Testing dig for Go (next in rotation)...")
    result2 = dig("Go")
    assert_eq("Go", result2["selected_language"], "Go is selected")
    assert_eq("Swift", result2["next_language"], "Next language is Swift")
    assert_eq("Robert Griesemer, Rob Pike, Ken Thompson (Google)", result2["origins"]["created_by"], "Go creators verified")
    assert_eq(2009, result2["origins"]["year_born"], "Go born in 2009")

    print("  Testing all languages have complete archaeology data...")
    for lang in config["languages"]:
        r = dig(lang)
        assert_eq(lang, r["selected_language"], f"{lang} selected correctly")
        assert_true(r["age_years"] >= 0, f"{lang} has valid age")
        assert_true(len(r["origins"]["inspired_by"]) >= 3, f"{lang} has >= 3 inspirations")
        assert_true(len(r["philosophy"]["design_principles"]) >= 4, f"{lang} has >= 4 design principles")
        assert_true(len(r["ancestral_dna"]) >= 4, f"{lang} has >= 4 ancestral DNA entries")
        assert_true(len(r["timeline"]) >= 3, f"{lang} has >= 3 timeline entries")
        assert_true(len(r["archaeological_finds"]) >= 3, f"{lang} has >= 3 archaeological finds")

    print("  Verifying cross_pollination structure...")
    cross = result["cross_pollination"]
    assert_true("languages_this_influenced" in cross, "cross_pollination has languages_this_influenced")
    assert_true("ideas_borrowed_summary" in cross, "cross_pollination has ideas_borrowed_summary")
    assert_true(len(cross["languages_this_influenced"]) >= 3, "influenced list >= 3")

    print("  Testing invalid language handling...")
    try:
        dig("Python")
        tests_failed += 1
        print("  ❌ FAIL: No error raised for invalid language")
    except ValueError as e:
        tests_passed += 1
        print("  ✅ PASS: ValueError raised for invalid language")
        assert_in("not in rotation", str(e), "Error mentions rotation")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ FAIL: Wrong exception: {e}")

    print("  Testing timeline and archaeological_finds format...")
    assert_true(all(isinstance(t, str) for t in result["timeline"]), "All timeline entries are strings")
    assert_true(all(isinstance(f, str) for f in result["archaeological_finds"]), "All finds are strings")

    print("  Testing dig_quote is non-empty...")
    assert_true(len(result["dig_quote"]) > 10, "dig_quote is meaningful")

    print(f"\n{'='*55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("🏛️ All Archaeology tests passed! The dig is complete.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--dig":
        language = sys.argv[2] if len(sys.argv) > 2 else "Rust"
        result = dig(language)
        print(json.dumps(result, indent=2))
    else:
        print(f"Language Archaeology v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m language_archaeology --test   # Run tests")
        print("  python -m language_archaeology --dig [lang]  # Dig up language history")
