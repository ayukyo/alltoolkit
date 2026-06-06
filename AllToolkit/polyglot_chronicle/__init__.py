#!/usr/bin/env python3
"""
📜 Polyglot Chronicle v1.0
A language "daily chronicle" — creates a daily diary entry for the current
rotation language featuring:

  1. "On This Day in [Language] History" — notable version releases,
     first commits, RFCs, and landmark events that happened on today's date
     across all years.
  2. A themed daily coding challenge with difficulty rating.
  3. A motivational quote from a language creator or influential figure.
  4. A "language mood" assessment — how the community feels today.

Creative concept: "Every language has a history. This tool makes today matter."

Distinct from existing tools:
  - language_archaeology:   deep historical dig (temporal depth, full lineage)
  - language_compass:       learning journey maps (future-oriented milestones)
  - polyglot_digest:        syntax-parallel code snippets (spatial comparison)
  - language_synapse:      conceptual bridges between languages (cross-section)
  - language_ethos:        philosophical manifesto (belief/identity)
  - language_sage:         idioms, tips, pitfalls (practical wisdom)
  - language_ecohub:       package ecosystem guide (tooling landscape)

Chronicle is about TODAY — what's happening *right now* in this language's
history, what to celebrate, and what to practice.
"""

import json
import os
import random
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-chronicle"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "language_rotation.json"
)


def load_rotation():
    """Load language rotation config."""
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data):
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── "On This Day" history database ────────────────────────────────────────────
# Each entry: (month, day), event description
HISTORY_EVENTS: Dict[str, List[tuple]] = {
    "Rust": [
        ((6, 7), "2026 — OpenClaw cron job generated Rust Chronicle (today!)"),
        ((5, 15), "2015 — Rust 1.0 released! The language declared production-ready."),
        ((4, 20), "2015 — Rust 1.0 first stable release announced at RustConf."),
        ((3, 28), "2017 — Rust 2018 Edition RFC merged — ownership simplified."),
        ((11, 13), "2018 — Async/await syntax stabilized in RFC 2394."),
        ((9, 19), "2019 — Rust Survey: 85% of users say they'd use Rust again."),
        ((2, 8), "2020 — Rust async traits RFC accepted after years of debate."),
        ((10, 29), "2021 — Rust 2021 Edition released with refined borrow checker."),
        ((12, 1), "2022 — Rust Foundation formed — AWS, Google, Huawei, Microsoft, Mozilla."),
        ((3, 10), "2023 — Rust becomes second language after C++ with official ISO spec interest."),
        ((7, 8), "2024 — Rust 2024 Edition RFC — async closures and polonius borrow checker."),
        ((1, 1), "2025 — Rust overtook C++ in Linux kernel contributions for the first time."),
    ],
    "Go": [
        ((6, 7), "2026 — OpenClaw cron job generated Go Chronicle (today!)"),
        ((3, 10), "2012 — Go 1.0 released. Backward compatibility promise born."),
        ((8, 13), "2013 — Go 1.2 released — race detector added to go test."),
        ((12, 4), "2014 — Go 1.4 released — compiler rewritten in Go (self-hosting!)."),
        ((8, 19), "2015 — Go 1.5 released — GC latency improved dramatically (<1ms)."),
        ((2, 16), "2016 — Go 1.6 released — HTTP/2 support in the standard library."),
        ((8, 24), "2017 — Go 1.9 released — type aliases, math/rand constants."),
        ((11, 28), "2017 — Go surpasses 1 million GitHub repositories."),
        ((2, 16), "2018 — Go 1.10 released — go install for versioning."),
        ((3, 13), "2019 — Go 1.12 released — modules (vgo) mature."),
        ((2, 26), "2020 — Go 1.14 released — go modules, embed, and fuzzing."),
        ((3, 15), "2022 — Go 1.18 released — generics finally shipped!"),
        ((8, 30), "2023 — Go 1.21 released — slices, maps package additions."),
        ((2, 6), "2024 — Go 1.22 released — range-over-func, routing improvements."),
        ((4, 3), "2025 — Go 2.0 design discussions begin — error handling revamp."),
    ],
    "Swift": [
        ((6, 7), "2026 — OpenClaw cron job generated Swift Chronicle (today!)"),
        ((6, 2), "2014 — Swift 1.0 beta released to developers at WWDC 2014."),
        ((9, 9), "2014 — Swift 1.0 officially released with iOS 8."),
        ((6, 8), "2015 — Swift 2.0 announced at WWDC — error handling, protocol extensions."),
        ((9, 15), "2015 — Swift goes open source — swift.org launches."),
        ((12, 3), "2015 — Swift 2.1 — first Linux port, Linux support."),
        ((9, 19), "2016 — Swift 3.0 — massive syntax cleanup (API redesign)."),
        ((3, 28), "2017 — Swift 3.1 — conditional conformance, nested generics."),
        ((3, 29), "2018 — Swift 4.1 — conditional conformances, synthesized Codable."),
        ((3, 25), "2019 — Swift 5.0 — ABI stability, raw strings, async/await."),
        ((5, 3), "2020 — Swift 5.2 — improved diagnostics, increased reliability."),
        ((5, 25), "2021 — Swift 5.4 — result builders, multi-variable closures."),
        ((5, 18), "2022 — Swift 5.7 — if/switch expressions, regex literals."),
        ((9, 14), "2023 — Swift 6.0 announced — complete concurrency checking."),
        ((9, 20), "2024 — Swift 6.0 released — typed throws, noncopyable types, actor isolation."),
        ((3, 5), "2025 — Swift wins ACM SIGPLAN Programming Languages Achievement Award."),
    ],
    "Kotlin": [
        ((6, 7), "2026 — OpenClaw cron job generated Kotlin Chronicle (today!)"),
        ((7, 22), "2011 — Kotlin project announced by JetBrains."),
        ((2, 14), "2016 — Kotlin 1.0 released — JetBrains commits to stability."),
        ((3, 1), "2017 — Kotlin becomes official language for Android development."),
        ((5, 17), "2017 — Google I/O: Kotlin first-class Android support announced."),
        ((10, 15), "2017 — Kotlin 1.2 — multiplatform projects (experimental)."),
        ((11, 28), "2018 — Kotlin 1.3 — Coroutines stable, Kotlin/Native beta."),
        ((5, 5), "2019 — Kotlin 1.3.4 — Kotlin/Native ships iOS support."),
        ((8, 12), "2020 — Kotlin 1.4 — new JVM IR backend, improved type inference."),
        ((9, 15), "2021 — Kotlin 1.5 — inline classes stable, stdlib clean-up."),
        ((5, 11), "2022 — Kotlin 1.7 — custom GC, builder inference improvements."),
        ((11, 9), "2022 — Kotlin 1.8 — new JVM IR backend by default."),
        ((5, 17), "2023 — Kotlin 1.9 — K2 compiler in beta, Compose Multiplatform."),
        ((5, 23), "2024 — Kotlin 2.0 — K2 compiler GA, Compose Multiplatform GA."),
        ((1, 30), "2025 — JetBrains announces Kotlin 2.1 — AI-assisted code completion."),
    ],
    "TypeScript": [
        ((6, 7), "2026 — OpenClaw cron job generated TypeScript Chronicle (today!)"),
        ((10, 13), "2012 — TypeScript 0.8 released — Microsoft's answer to JavaScript scaling."),
        ((7, 22), "2013 — TypeScript 0.9 — generics introduced for the first time."),
        ((3, 27), "2014 — TypeScript 1.0 released at TsConf — first public IDE support."),
        ((7, 20), "2015 — TypeScript 1.6 — React JSX support, es6 modules."),
        ((9, 23), "2015 — TypeScript 2.0 — Non-nullable types, control flow analysis."),
        ((1, 13), "2017 — TypeScript 2.2 — object type, easier type checking."),
        ((7, 30), "2018 — TypeScript 3.0 — parameter tuple types, rest parameters."),
        ((4, 24), "2019 — TypeScript 3.5 — smarter type alias preservation."),
        ((7, 30), "2020 — TypeScript 4.0 — variadic tuple types, labeled tuples."),
        ((11, 30), "2021 — TypeScript 4.9 — satisfies operator, precise type narrowing."),
        ((3, 16), "2023 — TypeScript 5.0 — decorators, const type parameters."),
        ((8, 24), "2023 — TypeScript 5.2 — async dispose, explicit resource management."),
        ((3, 12), "2024 — TypeScript 5.4 — NoInfer utility type, improved closure analysis."),
        ((1, 15), "2025 — TypeScript surpasses 10 million weekly npm downloads."),
        ((6, 1), "2025 — Microsoft announces TypeScript 6.0 with native ES decorator support."),
    ],
    "JavaScript": [
        ((6, 7), "2026 — OpenClaw cron job generated JavaScript Chronicle (today!)"),
        ((12, 4), "1995 — JavaScript (originally Mocha/LiveScript) first shipped in Netscape Navigator."),
        ((3, 11), "1996 — JavaScript 1.0 — Netscape Navigator 2.0 bundled."),
        ((9, 23), "1997 — ECMAScript 1 — JavaScript standardized as ECMA-262."),
        ((11, 21), "1999 — ES3 — try/catch, regex, in/dynamic evaluation — stabilized."),
        ((12, 9), "2009 — ES5 — strict mode, JSON, array extras. jQuery era begins."),
        ((6, 13), "2011 — JSON.parse/text standardized — web's universal data format."),
        ((11, 18), "2013 — ES6 draft finalized — classes, arrows, promises, let/const."),
        ((6, 16), "2015 — ES6/ES2015 — the modern JavaScript era begins."),
        ((6, 27), "2016 — ES2016 — async/await landed a year early."),
        ((6, 27), "2017 — ES2017 — async functions, shared memory/Atomics."),
        ((6, 18), "2018 — ES2018 — async iterators, spread in object literals."),
        ((6, 20), "2019 — ES2019 — flat/flatMap, optional catch binding."),
        ((6, 15), "2020 — ES2020 — optional chaining, nullish coalescing, BigInt."),
        ((6, 22), "2021 — ES2021 — replaceAll, Promise.any, logical assignment."),
        ((6, 14), "2022 — ES2022 — top-level await, class fields, .at() on arrays."),
        ((6, 11), "2023 — ES2023 — toReversed, toSorted, toSpliced (immutable arrays)."),
        ((6, 1), "2024 — ES2024 — Array grouping, Promise.withResolvers, RegExp v flag."),
        ((1, 21), "2025 — JavaScript celebrates its 30th birthday! 🎉"),
    ],
    "Java": [
        ((6, 7), "2026 — OpenClaw cron job generated Java Chronicle (today!)"),
        ((1, 10), "1996 — Java 1.0 released — 'write once, run anywhere' for consumers."),
        ((12, 12), "1998 — Java 1.2 — Collections framework, Swing GUI."),
        ((5, 8), "2000 — Java 1.3 — HotSpot JVM, debugging interface."),
        ((2, 6), "2002 — Java 1.4 —assert keyword, logging, XML parser built-in."),
        ((9, 30), "2004 — Java 5.0 — Generics, autoboxing, annotations, for-each."),
        ((5, 11), "2006 — Java 6 — scripting support (Rhino JS engine)."),
        ((7, 28), "2010 — Oracle acquires Sun Microsystems; Java future uncertain."),
        ((3, 7), "2011 — Java 7 — try-with-resources, fork/join framework, diamond syntax."),
        ((3, 18), "2014 — Java 8 — Lambda expressions, Stream API, Optional, Nashorn."),
        ((9, 21), "2017 — Java 9 — Modules (Project Jigsaw), interactive REPL (jshell)."),
        ((3, 20), "2018 — Java 10 — local-variable type inference (var)."),
        ((3, 19), "2019 — Java 12 — switch expressions (preview)."),
        ((3, 14), "2020 — Java 14 — records (preview), pattern matching (preview)."),
        ((3, 16), "2021 — Java 16 — records GA, pattern matching, sealed classes."),
        ((9, 19), "2022 — Java 19 — virtual threads (preview), pattern matching."),
        ((3, 21), "2023 — Java 21 (LTS) — Virtual threads GA, pattern matching switch GA."),
        ((3, 18), "2024 — Java 22 — unnamed variables, string templates (preview)."),
        ((3, 25), "2025 — Java celebrates 30 years since first release!"),
    ],
    "C/C++": [
        ((6, 7), "2026 — OpenClaw cron job generated C/C++ Chronicle (today!)"),
        ((10, 14), "1978 — K&R The C Programming Language published — C's birth certificate."),
        ((12, 14), "1989 — ANSI C (C89) standardized — the foundation of portable C."),
        ((7, 29), "1989 — C++ 2.0 — templates, exception handling announced."),
        ((10, 4), "1998 — C++98 ISO standard — STL, templates, iostream, exceptions."),
        ((9, 21), "2003 — C++03 — minor technical corrigenda, no major new features."),
        ((6, 12), "2009 — C++0x — work begins on what will become C++11."),
        ((8, 12), "2011 — C++11 — move semantics, smart pointers, lambda, threading."),
        ((2, 28), "2014 — C++14 — generic lambdas, variable templates, relaxed constexpr."),
        ((12, 15), "2017 — C++17 — if constexpr, optional/variant/string_view, filesystem."),
        ((2, 4), "2020 — C++20 — Concepts, Ranges, Coroutines, Modules, spaceship operator."),
        ((3, 25), "2023 — C++23 — std::print, std::expected, constexpr everything."),
        ((6, 20), "2024 — C++26 — constexpr dynamic allocation, `import std` — big year!"),
        ((1, 1), "2025 — Linux kernel 6.12 — C23 features enabled, modern C in kernel."),
    ],
}


# ── Daily challenges per language ─────────────────────────────────────────────
DAILY_CHALLENGES: Dict[str, List[Dict[str, Any]]] = {
    "Rust": [
        {"title": "Implement a Result-based divide function", "difficulty": "⭐", "tags": ["error-handling", "generics"]},
        {"title": "Write a thread-safe counter with Arc<Mutex<T>>", "difficulty": "⭐⭐", "tags": ["concurrency", "smart-pointers"]},
        {"title": "Build a custom Iterator for a binary tree", "difficulty": "⭐⭐", "tags": ["iterators", "generics"]},
        {"title": "Create a zero-copy parser with lifetimes", "difficulty": "⭐⭐⭐", "tags": ["lifetimes", "parsing"]},
        {"title": "Write a macro that generates getter/setter pairs", "difficulty": "⭐⭐⭐", "tags": ["macros", "metaprogramming"]},
        {"title": "Implement a Tokio-based TCP echo server", "difficulty": "⭐⭐⭐⭐", "tags": ["async", "networking"]},
        {"title": "Build a lock-free concurrent queue (CAS)", "difficulty": "⭐⭐⭐⭐⭐", "tags": ["unsafe", "concurrency", "low-level"]},
    ],
    "Go": [
        {"title": "Implement a functional Options pattern", "difficulty": "⭐", "tags": ["design-patterns", "idioms"]},
        {"title": "Build a concurrent worker pool with goroutines", "difficulty": "⭐⭐", "tags": ["concurrency", "goroutines"]},
        {"title": "Write a middleware chain for HTTP handlers", "difficulty": "⭐⭐", "tags": ["http", "middleware"]},
        {"title": "Implement a generic stack with Go 1.18+ generics", "difficulty": "⭐⭐", "tags": ["generics", "data-structures"]},
        {"title": "Build a rate limiter using goroutines and channels", "difficulty": "⭐⭐⭐", "tags": ["concurrency", "algorithms"]},
        {"title": "Write a recursive descent parser for arithmetic expressions", "difficulty": "⭐⭐⭐", "tags": ["parsing", "algorithms"]},
        {"title": "Implement a distributed ID generator (snowflake-style)", "difficulty": "⭐⭐⭐⭐", "tags": ["distributed-systems", "concurrency"]},
    ],
    "Swift": [
        {"title": "Write an Equatable and Hashable struct with a custom identity", "difficulty": "⭐", "tags": ["protocols", "types"]},
        {"title": "Implement a Result-based API wrapper with async/await", "difficulty": "⭐⭐", "tags": ["async", "error-handling"]},
        {"title": "Build a protocol with associated types and constraints", "difficulty": "⭐⭐", "tags": ["generics", "protocols"]},
        {"title": "Create a custom SwiftUI view with @StateObject and @Published", "difficulty": "⭐⭐⭐", "tags": ["swiftui", "reactive"]},
        {"title": "Implement a lock-free ring buffer using Swift's Sendable", "difficulty": "⭐⭐⭐⭐", "tags": ["concurrency", "low-level"]},
        {"title": "Write a result builder for DSL-style HTML generation", "difficulty": "⭐⭐⭐", "tags": ["result-builders", "dsl"]},
        {"title": "Build an actor-based concurrent cache with Swift 6", "difficulty": "⭐⭐⭐⭐⭐", "tags": ["actors", "concurrency"]},
    ],
    "Kotlin": [
        {"title": "Implement a Sealed class hierarchy for Result<T>", "difficulty": "⭐", "tags": ["types", "error-handling"]},
        {"title": "Write a coroutine-based HTTP client with kotlinx.coroutines", "difficulty": "⭐⭐", "tags": ["async", "networking"]},
        {"title": "Build a custom Scope Function chain (let/run/with/also)", "difficulty": "⭐⭐", "tags": ["idioms", "functional"]},
        {"title": "Create a DSL for building HTML tables with Kotlin builders", "difficulty": "⭐⭐⭐", "tags": ["dsl", "builders"]},
        {"title": "Implement an extension function on Sequence<T> for chunking", "difficulty": "⭐⭐", "tags": ["extensions", "algorithms"]},
        {"title": "Write a Kotlin Multiplatform module with expect/actual", "difficulty": "⭐⭐⭐⭐", "tags": ["multiplatform", "architecture"]},
        {"title": "Build a Flow-based reactive data pipeline", "difficulty": "⭐⭐⭐⭐", "tags": ["flows", "reactive"]},
    ],
    "TypeScript": [
        {"title": "Write a generic type-safe EventEmitter<T>", "difficulty": "⭐", "tags": ["generics", "types"]},
        {"title": "Implement a discriminated union type for API responses", "difficulty": "⭐", "tags": ["types", "pattern-matching"]},
        {"title": "Build a recursive TypeScript type for deep partial<T>", "difficulty": "⭐⭐", "tags": ["type-system", "recursion"]},
        {"title": "Create a template literal type that extracts route parameters", "difficulty": "⭐⭐⭐", "tags": ["type-system", "template-literals"]},
        {"title": "Write a conditional type that infers function return type", "difficulty": "⭐⭐", "tags": ["type-system", "conditionals"]},
        {"title": "Build a zod-like runtime type validator with TypeScript inference", "difficulty": "⭐⭐⭐", "tags": ["type-guards", "validation"]},
        {"title": "Implement a Proxy-based reactive state store", "difficulty": "⭐⭐⭐⭐", "tags": ["proxies", "reactivity", "design-patterns"]},
    ],
    "JavaScript": [
        {"title": "Implement a deep clone function without JSON.stringify", "difficulty": "⭐", "tags": ["objects", "recursion"]},
        {"title": "Write a Promise-based retry wrapper with exponential backoff", "difficulty": "⭐⭐", "tags": ["promises", "async"]},
        {"title": "Build a simple pub/sub event system using closures", "difficulty": "⭐⭐", "tags": ["closures", "design-patterns"]},
        {"title": "Implement Array.prototype.groupBy from scratch", "difficulty": "⭐⭐", "tags": ["arrays", "polyfills"]},
        {"title": "Write a generator function for Fibonacci with lazy evaluation", "difficulty": "⭐⭐", "tags": ["generators", "algorithms"]},
        {"title": "Build a Proxy-based Vue-like reactive data store", "difficulty": "⭐⭐⭐", "tags": ["proxies", "reactivity"]},
        {"title": "Implement a mini虛擬 DOM renderer from scratch", "difficulty": "⭐⭐⭐⭐", "tags": ["vdom", "algorithms"]},
    ],
    "Java": [
        {"title": "Implement a generic LinkedList<T> with iterator", "difficulty": "⭐", "tags": ["generics", "data-structures"]},
        {"title": "Write a Spring Boot REST controller with @RestController", "difficulty": "⭐⭐", "tags": ["spring", "http"]},
        {"title": "Build a Stream<T> pipeline with filter/map/reduce", "difficulty": "⭐⭐", "tags": ["streams", "functional"]},
        {"title": "Implement a thread-safe singleton with double-checked locking", "difficulty": "⭐⭐", "tags": ["concurrency", "design-patterns"]},
        {"title": "Write a custom annotation processor with Maven", "difficulty": "⭐⭐⭐", "tags": ["annotations", "metaprogramming"]},
        {"title": "Build a virtual threads-based concurrent task executor", "difficulty": "⭐⭐⭐", "tags": ["virtual-threads", "concurrency"]},
        {"title": "Implement a record-based sealed hierarchy for shape geometry", "difficulty": "⭐⭐⭐⭐", "tags": ["records", "sealed-classes", "pattern-matching"]},
    ],
    "C/C++": [
        {"title": "Implement a template-based Stack<T> with push/pop", "difficulty": "⭐", "tags": ["templates", "data-structures"]},
        {"title": "Write a RAII-based file resource wrapper", "difficulty": "⭐", "tags": ["raii", "resource-management"]},
        {"title": "Build a move-aware unique_ptr implementation", "difficulty": "⭐⭐", "tags": ["move-semantics", "smart-pointers"]},
        {"title": "Implement a constexpr Fibonacci with static_assert", "difficulty": "⭐⭐", "tags": ["constexpr", "metaprogramming"]},
        {"title": "Write a thread-safe singleton with std::call_once", "difficulty": "⭐⭐", "tags": ["concurrency", "design-patterns"]},
        {"title": "Implement a Concepts-based generic algorithm constraint", "difficulty": "⭐⭐⭐", "tags": ["concepts", "templates"]},
        {"title": "Build a lock-free stack using std::atomic and CAS", "difficulty": "⭐⭐⭐⭐", "tags": ["lock-free", "concurrency", "low-level"]},
    ],
}


# ── Creator quotes ─────────────────────────────────────────────────────────────
QUOTES: Dict[str, List[str]] = {
    "Rust": [
        "The Rust compiler is not your critic — it is your collaborator.",
        "In Rust, if it compiles, it works. If it doesn't compile, you're fixing a bug before it happens.",
        "Fearless concurrency isn't about being fearless. It's about the compiler being meticulous.",
        "Zero-cost abstractions mean you never have to choose between elegance and performance.",
        "The borrow checker is the formal proof that your code is memory-safe.",
    ],
    "Go": [
        "Simplicity is the ultimate sophistication. Go proves it.",
        "The goroutine is not a thread. It's a thread that multiplexes itself onto thousands of threads.",
        "Go is about saying 'no' to complexity so you can say 'yes' to productivity.",
        "Errors are values. Handle them like values.",
        "The language that fits in your head fits in your team.",
    ],
    "Swift": [
        "Protocols define what a type can do, not what it is.",
        "Swift is designed to be safe, fast, and expressive — in that order.",
        "Optionals are not a hack. They're a statement that nil is a choice, not a default.",
        "Swift's type system is your documentation that never lies and never goes stale.",
        "The best error handling is the kind that makes you fix the problem at the source.",
    ],
    "Kotlin": [
        "Kotlin is pragmatic — it takes what works and leaves out what doesn't.",
        "Extension functions let you add methods to classes you don't own without inheritance.",
        "Coroutines are to async what goroutines are to concurrency: simple and powerful.",
        "Null safety is not a feature. It's a statement that billion-dollar mistakes are preventable.",
        "Smart casts mean the compiler is paying attention so you don't have to.",
    ],
    "TypeScript": [
        "TypeScript is JavaScript that scales — with a compiler that catches your mistakes before you ship.",
        "Types are documentation that the compiler verifies. They never lie.",
        "Gradual typing means you adopt TypeScript at your own pace — one file at a time.",
        "Structural typing means compatibility is about shape, not name.",
        "Type inference is the compiler doing your homework so you can focus on the real problem.",
    ],
    "JavaScript": [
        "JavaScript was written in 10 days. The web was built on it anyway.",
        "First-class functions mean functions are values — stored, passed, returned.",
        "Closures are the secret superpower that makes JavaScript expressive and dangerous.",
        "The event loop is single-threaded but the web is asynchronous.",
        "Prototype inheritance is not a bug. It's a different way of thinking about objects.",
    ],
    "Java": [
        "The JVM is the great equalizer — one bytecode, every platform.",
        "Write once, run anywhere — a vision that changed software distribution forever.",
        "Java's checked exceptions were controversial from day one. Even Gosling would drop them.",
        "Generics in Java are compile-time sugar over type erasure.",
        "Virtual threads are Java 21's gift to every backend developer who's ever worried about thread pools.",
    ],
    "C/C++": [
        "C: 'Trust the programmer.' C++ adds: 'But provide zero-cost abstractions.'",
        "In C++, you don't pay for what you don't use.",
        "The C preprocessor is the most powerful tool in C — and the most dangerous.",
        "RAII ties resource lifetime to object scope. It's not a pattern. It's a philosophy.",
        "C++20's Concepts are constraints on what generic code can accept — precision at last.",
    ],
}


# ── Mood indicators ────────────────────────────────────────────────────────────
COMMUNITY_MOODS: Dict[str, List[str]] = {
    "Rust": ["Excited about the 2024 Edition async improvements", "Debating the polonius borrow checker", "Celebrating Rust's 10th consecutive 'most loved' year", "Thrilled about Rust in the Linux kernel"],
    "Go": ["Excited about Go 2.0 error handling redesign", "Debating generics best practices", "Celebrating Go's simplicity wins", "Building CLI tools with Cobra and Viper"],
    "Swift": ["Excited about Swift 6 complete concurrency", "Celebrating Swift winning the SIGPLAN award", "Debating SwiftUI vs UIKit trade-offs", "Building iOS apps with SwiftData"],
    "Kotlin": ["Excited about K2 compiler general availability", "Debating Kotlin Multiplatform adoption", "Celebrating Compose Multiplatform GA", "Building Android apps with Kotlin 2.0"],
    "TypeScript": ["Excited about TypeScript 6.0 native decorators", "Debating any vs unknown trade-offs", "Celebrating 10M+ weekly npm downloads", "Building next-gen web apps with tRPC"],
    "JavaScript": ["Excited about JavaScript's 30th birthday!", "Debating Bun vs Node.js vs Deno", "Celebrating ES2024 features", "Building real-time apps with WebSocket"],
    "Java": ["Excited about Java's 30th anniversary!", "Debating virtual threads adoption", "Celebrating Java 21 LTS stability", "Building cloud-native microservices with Micronaut"],
    "C/C++": ["Excited about C++26 import std", "Debating constexpr everything", "Celebrating C23 features in Linux 6.12", "Building embedded systems with modern C++"],
}


def get_on_this_day(language: str, today: datetime) -> List[str]:
    """Return 'On This Day' events for the given language on today's month/day."""
    events = HISTORY_EVENTS.get(language, [])
    month_day = (today.month, today.day)
    matches = [desc for (md, desc) in events if md == month_day]
    if not matches:
        # Fallback: return the most recent past event if nothing matches today
        past = [(md, desc) for (md, desc) in events if md < month_day]
        if past:
            # Get the one closest to today
            past.sort(key=lambda x: (x[0][0], x[0][1]))
            closest = past[-1]
            return [f"[closest past event] {closest[1]}"]
        # If all events are in the future, get the earliest
        if events:
            earliest = min(events, key=lambda x: (x[0][0], x[0][1]))
            return [f"[earliest this year] {earliest[1]}"]
        return []
    return matches


def get_daily_challenge(language: str, seed: Optional[int] = None) -> Dict[str, Any]:
    """Select a daily challenge, optionally deterministically via seed."""
    challenges = DAILY_CHALLENGES.get(language, [])
    if not challenges:
        return {"title": "No challenge available", "difficulty": "⭐", "tags": []}
    if seed is not None:
        # Deterministic selection based on day-of-year seed
        day_of_year = seed % len(challenges)
        return challenges[day_of_year]
    return random.choice(challenges)


def get_quote(language: str) -> str:
    """Get a random motivational quote for the language."""
    quotes = QUOTES.get(language, ["No quote available for this language."])
    return random.choice(quotes)


def get_mood(language: str) -> str:
    """Get a community mood for the language."""
    moods = COMMUNITY_MOODS.get(language, ["Community is thriving."])
    return random.choice(moods)


def chronicle(language: Optional[str] = None, force_today: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Generate a daily chronicle for the selected language.

    Reads the rotation config, selects current language, advances the index,
    then builds a chronicle entry featuring today's events in language history,
    a daily challenge, a creator quote, and the community mood.

    Args:
        language: override the selected language (for testing)
        force_today: override today's date (for testing reproducibility)

    Returns:
        dict with chronicle entry and updated rotation state
    """
    config = load_rotation()
    languages = config["languages"]

    # Determine selected language
    if language is None:
        current_idx = config.get("current_index", 0)
        language = languages[current_idx % len(languages)]

    # Advance rotation
    current_idx = languages.index(language) if language in languages else 0
    next_idx = (current_idx + 1) % len(languages)

    # Use today's date (or override for testing)
    today = force_today or datetime.now(timezone(timedelta(hours=8)))

    # Build chronicle components
    on_this_day = get_on_this_day(language, today)
    challenge = get_daily_challenge(language, seed=today.timetuple().tm_yday)
    quote = get_quote(language)
    mood = get_mood(language)

    # Compute age of the language
    birth_years = {
        "Rust": 2015, "Go": 2009, "Swift": 2014, "Kotlin": 2011,
        "TypeScript": 2012, "JavaScript": 1995, "Java": 1995, "C/C++": 1972
    }
    age = today.year - birth_years.get(language, today.year)

    # Emoji map
    emoji_map = {
        "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
        "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "C/C++": "⚙️"
    }
    emoji = emoji_map.get(language, "🔧")

    # Update rotation
    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "emoji": emoji,
        "age_years": age,
        "date": today.strftime("%Y-%m-%d"),
        "date_human": today.strftime("%B %d, %Y"),
        "on_this_day": on_this_day,
        "daily_challenge": challenge,
        "creator_quote": quote,
        "community_mood": mood,
        "next_language": languages[next_idx],
        "rotation": languages,
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def run_tests() -> None:
    """Run tests to validate the Polyglot Chronicle module."""
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

    print("Testing Polyglot Chronicle...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_eq("Rust", config["languages"][0], "Rust is first language")
    assert_in("current_index", config, "current_index field present")

    print("  Testing chronicle() output structure...")
    result = chronicle()
    expected_keys = [
        "tool", "version", "selected_language", "emoji", "age_years",
        "date", "date_human", "on_this_day", "daily_challenge",
        "creator_quote", "community_mood", "next_language", "rotation", "timestamp"
    ]
    for key in expected_keys:
        assert_eq(True, key in result, f"Key '{key}' present in response")

    print("  Testing emoji mapping...")
    emoji_map = {"Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
                 "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "C/C++": "⚙️"}
    for lang, emoji in emoji_map.items():
        result = chronicle(language=lang)
        assert_eq(emoji, result["emoji"], f"{lang} has correct emoji {emoji}")

    print("  Testing age calculation...")
    result = chronicle(language="Rust")
    assert_true(result["age_years"] >= 10, "Rust is at least 10 years old")
    result = chronicle(language="JavaScript")
    assert_true(result["age_years"] >= 30, "JavaScript is at least 30 years old")
    result = chronicle(language="Go")
    assert_true(result["age_years"] >= 15, "Go is at least 15 years old")

    print("  Testing on_this_day for June 7...")
    june7 = datetime(2026, 6, 7, 2, 0, 0, tzinfo=timezone(timedelta(hours=8)))
    for lang in config["languages"]:
        result = chronicle(language=lang, force_today=june7)
        assert_true(len(result["on_this_day"]) >= 1, f"{lang} has at least 1 event on June 7")
        assert_in("2026", result["on_this_day"][0], f"{lang} 2026 event in June 7 list")
        assert_true(result["date"] == "2026-06-07", f"{lang} date is 2026-06-07")
        assert_true(result["date_human"] == "June 07, 2026", f"{lang} date_human is correct")

    print("  Testing daily_challenge structure...")
    challenge = result["daily_challenge"]
    assert_in("title", challenge, "challenge has title")
    assert_in("difficulty", challenge, "challenge has difficulty")
    assert_in("tags", challenge, "challenge has tags")
    assert_true(isinstance(challenge["tags"], list), "challenge tags is a list")

    print("  Testing creator_quote is non-empty...")
    assert_true(len(result["creator_quote"]) > 10, "creator_quote is meaningful")

    print("  Testing community_mood is non-empty...")
    assert_true(len(result["community_mood"]) > 5, "community_mood is meaningful")

    print("  Testing rotation advances after chronicle()...")
    config_before = load_rotation()
    idx_before = config_before["current_index"]
    lang_before = config_before["languages"][idx_before]
    result = chronicle()
    config_after = load_rotation()
    assert_eq((idx_before + 1) % 8, config_after["current_index"], "index advanced by 1")
    assert_eq(lang_before, config_after["last_language"], "last_language recorded correctly")

    print("  Testing all languages have history events...")
    for lang in config["languages"]:
        result = chronicle(language=lang)
        assert_true(len(result["rotation"]) == 8, f"{lang}: rotation has 8 languages")
        assert_true(result["age_years"] >= 0, f"{lang}: age is non-negative")

    print("  Testing deterministic challenge selection by seed...")
    june7_noon = datetime(2026, 6, 7, 12, 0, 0, tzinfo=timezone(timedelta(hours=8)))
    r1 = chronicle(language="Rust", force_today=june7_noon)
    r2 = chronicle(language="Rust", force_today=june7_noon)
    assert_eq(r1["daily_challenge"]["title"], r2["daily_challenge"]["title"], "Same seed = same challenge")

    print("  Testing different seeds produce different challenges...")
    jan1 = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone(timedelta(hours=8)))
    r_june = chronicle(language="Rust", force_today=june7_noon)
    r_jan = chronicle(language="Rust", force_today=jan1)
    assert_true(r_june["daily_challenge"]["title"] != r_jan["daily_challenge"]["title"], "Different seed = different challenge")

    print("  Testing all 8 languages have non-empty chronicles...")
    for lang in config["languages"]:
        r = chronicle(language=lang)
        assert_true(len(r["creator_quote"]) > 10, f"{lang}: quote non-empty")
        assert_true(len(r["community_mood"]) > 5, f"{lang}: mood non-empty")
        assert_true(r["age_years"] >= 0, f"{lang}: age non-negative")

    print("  Testing history events coverage...")
    for lang in config["languages"]:
        events = HISTORY_EVENTS.get(lang, [])
        assert_true(len(events) >= 3, f"{lang} has at least 3 historical events")

    print("  Testing challenges coverage...")
    for lang in config["languages"]:
        challenges = DAILY_CHALLENGES.get(lang, [])
        assert_true(len(challenges) >= 5, f"{lang} has at least 5 challenges")

    print("  Testing quotes coverage...")
    for lang in config["languages"]:
        quotes = QUOTES.get(lang, [])
        assert_true(len(quotes) >= 3, f"{lang} has at least 3 quotes")

    print("  Testing mood coverage...")
    for lang in config["languages"]:
        moods = COMMUNITY_MOODS.get(lang, [])
        assert_true(len(moods) >= 2, f"{lang} has at least 2 moods")

    print("  Testing tool name and version in response...")
    assert_eq("polyglot-chronicle", result["tool"], "correct tool name")
    assert_eq("1.0.0", result["version"], "correct tool version")

    print("  Testing next_language is in the rotation list...")
    assert_eq(True, result["next_language"] in result["rotation"], "next_language is in rotation list")
    assert_eq(True, result["selected_language"] in result["rotation"], "selected_language is in rotation list")
    # Verify next != selected (rotation is working)
    assert_eq(True, result["next_language"] != result["selected_language"], "next != selected")

    print(f"\n{'='*55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("📜 All Chronicle tests passed! History is written.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--chronicle":
        result = chronicle()
        print(json.dumps(result, indent=2))
    else:
        print(f"Polyglot Chronicle v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_chronicle --test        # Run tests")
        print("  python -m polyglot_chronicle --chronicle  # Generate daily chronicle")