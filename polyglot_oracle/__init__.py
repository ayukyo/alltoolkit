#!/usr/bin/env python3
"""
🔮 Polyglot Oracle v1.0

A creative language wisdom tool — the current rotation language speaks
directly to you, giving philosophical counsel on any programming problem.

Ask the Oracle about your situation (via seed/description), and the
rotation language answers in its own voice, with its philosophy,
self-aware limitations, and practical wisdom.

Creative concept: "Every language has a philosophy of life. Ask it for advice."

This is distinct from:
  - polyglot_tarot: uses card metaphors and spreads (mystical divination)
  - polyglot_resonator: maps mental models across ALL languages at once
  - language_compass: learning journey / milestone tracking
  - language_archaeology: historical lineage and origins

Oracle is personal — one language speaks to YOU about YOUR problem.

Rotation: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import hashlib
import json
import os
import random
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-oracle"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "language_rotation.json"
)

# ── Oracle wisdom per language ────────────────────────────────────────────────

ORACLE_WISDOM: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "personality": "The meticulous philosopher-engineer who insists you prove your code is safe before running it.",
        "voice": "pragmatic_expert",
        "counsel": {
            "memory_leak": {
                "verdict": "A memory leak is a lie you told the compiler about ownership.",
                "advice": "Use RAII (Drop), Arc<RefCell<T>> for shared mutable state, or trace your ownership tree. The leak is real — it's telling you that someone still thinks they own memory they gave away.",
                "metaphor": "You're holding a receipt for something you already spent.",
                "prescription": "Run `cargo +nightly miri` to detect leaks. Or audit your Rc/Arc usage — one extra clone somewhere is the usual suspect."
            },
            "race_condition": {
                "verdict": "You claimed two things could happen at once. The universe disagrees.",
                "advice": "Rust's type system already forbids this — if it compiles. The bug means you're fighting the borrow checker or misusing unsafe. Don't disable the safety, redesign the API.",
                "metaphor": "Two people drawing from the same well, both claiming they're the only one holding the bucket.",
                "prescription": "Audit every `unsafe` block. Use `Send + Sync` bounds to let the compiler catch what your brain missed."
            },
            "performance": {
                "verdict": "You've been paying for abstractions you didn't use.",
                "advice": "Profile first — `cargo flamegraph`. Then ask: am I allocating in a hot loop? Am I cloning when I should be borrowing? Rust makes the cost visible. Don't guess.",
                "metaphor": "Every `.clone()` is a sculptor making a new statue instead of pointing at the one already there.",
                "prescription": "Use `cargo bench` to measure. Iterate with `--release`. Zero-cost abstractions mean your high-level code can be fast — if you don't fight the borrow checker."
            },
            "api_design": {
                "verdict": "Your API is lying about what it can do.",
                "advice": "Encode capabilities in the type system. Use the type to make illegal states unrepresentable. If your function can fail two ways, return an enum, not a Result<Result<T, E>, E>.",
                "metaphor": "A contract that says 'we promise nothing' protects no one.",
                "prescription": "Make invalid states invisible to the compiler. The goal: if it compiles, the API is correct."
            },
            "generic_code": {
                "verdict": "You've written code that's trying to be all things to all types — and failing at all of them.",
                "advice": "Trait bounds are promises. Every `where` clause is a constraint you're accepting. Start with concrete types, generalize when the duplication is unbearable.",
                "metaphor": "A key that claims to open every door opens none of them well.",
                "prescription": "Start with `impl` blocks, extract traits when the duplication costs more than the abstraction."
            },
        },
        "refuses_to": [
            "run code with undisciplined side effects",
            "let you ignore an error without marking it",
            "let you mutate what you're also reading",
            "pretend undefined behavior is a feature",
        ],
        "closing_remarks": [
            "The compiler is not the enemy. It is the proof.",
            "If you fight the borrow checker, you will lose. Redesign.",
            "Memory safety is not a feature. It is the minimum standard.",
        ],
    },
    "Go": {
        "personality": "The practical craftsman who values clarity over cleverness. 'Simple' is the highest compliment.",
        "voice": "pragmatic_craftsman",
        "counsel": {
            "memory_leak": {
                "verdict": "You're holding a goroutine open with an unclosed channel or an untrimmed map.",
                "advice": "Go's GC handles memory, not resources. If goroutines are leaking, it's because they're blocked on channels that will never close, or maps that grow without bound. `goleak` from Uber is your detective.",
                "metaphor": "You opened a thousand doors and walked through none of them.",
                "prescription": "Use context.Context for cancellation. Audit goroutine counts with `runtime.NumGoroutine()`. Check your sync.WaitGroup usage."
            },
            "race_condition": {
                "verdict": "You're sharing memory across goroutines without telling anyone.",
                "advice": "Go's 'share memory by communicating' isn't a suggestion. If you're sharing a variable across goroutines, use a channel or a mutex — and be deliberate about which.",
                "metaphor": "Passing a live grenade between people without agreeing on when to pull the pin.",
                "prescription": "Run `go test -race`. The race detector will show you exactly which read and write are in conflict."
            },
            "performance": {
                "verdict": "You're allocating too many small objects and letting the GC clean them up.",
                "advice": "Object pooling (sync.Pool), preallocating slices, and avoiding small interfaces will reduce GC pressure. `pprof` is your friend.",
                "metaphor": "Ordering new plates for every meal instead of washing the ones you have.",
                "prescription": "Profile with `go tool pprof`. Target: reduce allocations per request, not just total memory."
            },
            "api_design": {
                "verdict": "Your API is doing too much, and it shows in the error returns.",
                "advice": "Go doesn't have exceptions. Every function that can fail returns `(value, error)`. Design for it: return concrete errors, not generic ones. The caller deserves to know what happened.",
                "metaphor": "Saying 'something went wrong' is not an apology. It's a refusal to take responsibility.",
                "prescription": "Define sentinel errors (`var ErrNotFound = errors.New('not found')`). Wrap with `fmt.Errorf('context: %w', err)`."
            },
            "generic_code": {
                "verdict": "You've abstracted over types you don't actually need to abstract over.",
                "advice": "Go's generics (1.18+) are for when you have genuine type-parametric algorithms, not just to avoid type assertions. If you're writing `interface{}`, you're doing it wrong.",
                "metaphor": "A master chef doesn't need a recipe for every dish — they understand the principles.",
                "prescription": "Use generics for collection algorithms, type-safe data structures. Don't use them just to avoid typing."
            },
        },
        "refuses_to": [
            "let you ignore an error without writing the if-statement",
            "hide the complexity you created with clever abstractions",
            "let a goroutine leak silently",
            "pretend an interface is implemented when the methods don't match",
        ],
        "closing_remarks": [
            "Clear is better than clever.",
            "A little copying is better than a little dependency.",
            "Goroutines are cheap. Goroutine leaks are expensive.",
        ],
    },
    "Swift": {
        "personality": "The elegant stylist who believes beautiful code and correct code are the same thing.",
        "voice": "elegant_expressive",
        "counsel": {
            "memory_leak": {
                "verdict": "You've created a reference cycle — two objects keeping each other alive with strong references.",
                "advice": "Swift uses ARC (Automatic Reference Counting). Strong reference cycles are your enemy. Use `weak` for optional back-references and `unowned` for non-optional ones that you promise are valid.",
                "metaphor": "Two people promising to leave the room only after the other one leaves. Neither moves.",
                "prescription": "In SwiftUI: use @StateObject, @ObservedObject, @EnvironmentObject correctly. In UIKit: audit delegate properties for `weak`."
            },
            "race_condition": {
                "verdict": "You're accessing mutable state from multiple threads without coordination.",
                "advice": "Swift 6 makes data-race safety a compile-time error. Use actors for isolated state. Mark types Sendable if they can cross actor boundaries safely.",
                "metaphor": "Two people repainting the same wall in different colors, neither looking at the other.",
                "prescription": "Turn on Swift 6 concurrency checking. Replace shared mutable variables with actors."
            },
            "performance": {
                "verdict": "You're copying when you should be referencing, or vice versa.",
                "advice": "Swift uses copy-on-write for collections. Value types (structs, enums) are cheap when small. Classes have reference semantics. Know which you're using.",
                "metaphor": "Handing out photocopies of a document instead of pointing to the original — until someone wants to annotate it.",
                "prescription": "Instruments (Time Profiler) will show you where copies happen. Check for unintended class captures in closures."
            },
            "api_design": {
                "verdict": "Your API doesn't express what it actually needs or guarantees.",
                "advice": "Use protocols for capability-based design. Make invalid states unrepresentable through type design. Swift's type system is expressive — use it to encode preconditions.",
                "metaphor": "A door that doesn't say whether it's push or pull is poorly designed, no matter how beautiful the wood.",
                "prescription": "Encode optionality with Optional. Encode exclusive mutability with inout. Encode impossibility with enums with associated values."
            },
            "generic_code": {
                "verdict": "You've abstracted too eagerly, before understanding what the abstraction should be.",
                "advice": "Protocols with associated types (PATs) are powerful but complex. Start with concrete types, then extract protocols when you see genuine shared behavior.",
                "metaphor": "You can't design a room's purpose before you know what furniture goes in it.",
                "prescription": "Use generics for collection types and algorithms. Use protocols for polymorphism. Don't use generics just to avoid repetition."
            },
        },
        "refuses_to": [
            "let you access shared mutable state without actors in Swift 6",
            "let you ignore a nil value without handling it",
            "confuse a value type with a reference type silently",
            "let you throw an error without declaring it",
        ],
        "closing_remarks": [
            "If it doesn't feel Swift, it's probably not the right solution.",
            "Protocols define what a type can do, not what it inherits.",
            "Make invalid states unrepresentable through the type system.",
        ],
    },
    "Kotlin": {
        "personality": "The pragmatic modernizer who respects tradition but won't be slowed by it.",
        "voice": "pragmatic_modern",
        "counsel": {
            "memory_leak": {
                "verdict": "You've got a context or coroutine holding a reference to something that's gone.",
                "advice": "In Android: anonymous inner classes hold implicit references to the Activity. In coroutines: make sure your scope is tied to the right lifecycle. Use `WeakReference` for caches.",
                "metaphor": "A messenger still walking toward a house that was torn down years ago.",
                "prescription": "Use `.lifecycleScope` in Android, `viewModelScope` in ViewModels. Audit coroutine context for proper cancellation."
            },
            "race_condition": {
                "verdict": "Two threads looked at the same mutable variable and disagreed about who changed it last.",
                "advice": "Kotlin's `volatile` gives visibility, not atomicity. For atomic counters, use AtomicInteger. For synchronized access, use `synchronized`, `Mutex`, or better: design for immutability.",
                "metaphor": "Two people editing the same document, neither aware the other is in the room.",
                "prescription": "Use `kotlinx.coroutines.sync.Mutex` for fine-grained locking, or restructure to avoid shared mutable state entirely."
            },
            "performance": {
                "verdict": "You're creating too many short-lived objects on the JVM heap and paying GC taxes.",
                "advice": "Use object pools for frequently allocated objects. Prefer `StringBuilder` for concatenation in loops. Consider `inline` functions for small lambdas.",
                "metaphor": "Throwing away every plate after every meal instead of running the dishwasher.",
                "prescription": "Use Android Studio's profiler or YourKit. Target allocation rate, not just heap size."
            },
            "api_design": {
                "verdict": "Your API is returning null when it should be returning an empty collection, or vice versa.",
                "advice": "Kotlin's null safety is the language's best feature. Use nullable types (?.) to encode absence. Use empty collections, not null, for 'no results'. Make the caller handle the nothing case explicitly.",
                "metaphor": "Sending an empty envelope instead of nothing at all — at least the envelope arrives.",
                "prescription": "Return `List.emptyList()` not `null`. Return `?` for nullable types. Use `sealed class` for result types that carry meaning."
            },
            "generic_code": {
                "verdict": "You've written a generic function that's actually just an `Any` function in disguise.",
                "advice": "Kotlin's reified type parameters (with `inline fun <reified T>`) help with type-safe reflection. Use `where` clauses for constraints. But if you find yourself fighting the type system, maybe a concrete type is clearer.",
                "metaphor": "A skeleton key that opens every lock by being so vague it provides no actual security.",
                "prescription": "Reified types are for when you need the class at runtime. Generics are for compile-time type safety."
            },
        },
        "refuses_to": [
            "let you access a nullable value without the ?. operator or a null check",
            "silently swallow exceptions (except when you explicitly suppress them)",
            "let you use a mutable variable as a singleton state without synchronization",
            "confuse 'val' (immutable reference) with immutable contents",
        ],
        "closing_remarks": [
            "NullPointerException is a relic. Kotlin makes it a compile error.",
            "Mutability is a choice. Make it consciously.",
            "Extension functions let you add methods to classes you don't own — elegantly.",
        ],
    },
    "TypeScript": {
        "personality": "The type-theoretic adventurer who wants compile-time safety without giving up JavaScript's soul.",
        "voice": "type_adventurer",
        "counsel": {
            "memory_leak": {
                "verdict": "You've attached event listeners that never detach, or closures holding references to dead DOM nodes.",
                "advice": "In the browser: always `removeEventListener` before removing an element. In Node: clear intervals, close sockets, remove listeners. `process.memoryUsage()` will show you the leak.",
                "metaphor": "Taping new notes to a wall without removing the old ones. Eventually you can't see the wall.",
                "prescription": "Use Chrome DevTools Memory tab. Take heap snapshots before/after. Look for detached DOM trees."
            },
            "race_condition": {
                "verdict": "Two async operations returned in unexpected order because you assumed they'd be sequential.",
                "advice": "Use `Promise.all()` for parallel operations, `await` sequentially when order matters. Race conditions in async code are order-of-operations bugs.",
                "metaphor": "Ordering coffee and leaving before it's ready, then being surprised when someone else gets your cup.",
                "prescription": "Use `AbortController` for request cancellation. `Promise.race()` to timeout. Always handle the rejected case."
            },
            "performance": {
                "verdict": "You're re-rendering a component when its data hasn't changed, or iterating too many times per frame.",
                "advice": "In React: `useMemo` and `useCallback` prevent unnecessary re-renders. In Node: avoid synchronous methods in request handlers. Profile with `node --prof` or clinic.js.",
                "metaphor": "Rewriting the entire novel when you only changed one sentence.",
                "prescription": "Use React DevTools Profiler. Virtualize long lists. Debounce/throttle event handlers."
            },
            "api_design": {
                "verdict": "Your API accepts `any` when it should accept a specific shape.",
                "advice": "TypeScript's type system is its most valuable feature. Don't defeat it with `any`. Define interfaces for every request/response shape. The type is the documentation.",
                "metaphor": "A contract that says 'we accept anything' protects no one.",
                "prescription": "Enable `strict: true`. Use `unknown` instead of `any` for truly unknown data. Zod/io-ts for runtime validation."
            },
            "generic_code": {
                "verdict": "You've written a generic that only ever works for one type.",
                "advice": "Generics are for genuinely polymorphic code. If a generic type parameter only appears once, you probably don't need it.",
                "metaphor": "A universal remote programmed with only one button.",
                "prescription": "Start with `interface`, add `<T>` when you need the same logic over multiple types. Use `extends` to constrain."
            },
        },
        "refuses_to": [
            "let you compile with --strict if you leave an unused variable",
            "let you access `.foo` on something typed as `unknown` without narrowing first",
            "ignore a missing case in a switch exhaustiveness check",
            "pretend `as` is a type cast — it's just telling TypeScript to shut up",
        ],
        "closing_remarks": [
            "TypeScript is JavaScript with a type system. Use it.",
            "Interfaces are contracts. Keep them narrow.",
            "any is the escape hatch. Not the solution.",
        ],
    },
    "JavaScript": {
        "personality": "The pragmatic survivor who has seen every trend come and go and still ships products.",
        "voice": "pragmatic_survivor",
        "counsel": {
            "memory_leak": {
                "verdict": "Closures are keeping references alive. The closure captured a scope, and that scope has a reference to something big.",
                "advice": "Closures in JavaScript retain their enclosing scope. If you have a closure over a large object, that object lives as long as the closure. Nullify references when done.",
                "metaphor": "You hired someone to remember your grocery list forever, and they also remember the entire kitchen.",
                "prescription": "Use Chrome DevTools Memory tab. `window.performance.memory` (Chrome). Look for detached DOM nodes."
            },
            "race_condition": {
                "verdict": "Your promises resolved in an order you didn't expect because you didn't await them in the right sequence.",
                "advice": "JavaScript is single-threaded but async. `Promise.all([a, b])` runs in parallel. `await a; await b` runs sequentially. Know which you want.",
                "metaphor": "Ordering food at a counter and waiting at the wrong end of the kitchen.",
                "prescription": "Use `Promise.all()` for independent parallel work. Use `async/await` for sequential. Use `AbortController` to cancel."
            },
            "performance": {
                "verdict": "You're doing synchronous work on the main thread that should be async, or creating objects faster than the GC can collect them.",
                "advice": "Move heavy computation to Web Workers (browser) or Worker Threads (Node). Use `requestAnimationFrame` for visual updates. Avoid creating objects in hot loops.",
                "metaphor": "Trying to serve 10,000 customers at a single counter, one at a time.",
                "prescription": "Chrome DevTools Performance tab. Node: `node --inspect` with clinical.js. Profile first, optimize second."
            },
            "api_design": {
                "verdict": "Your function is doing too much or returning too many different things.",
                "advice": "JavaScript functions should do one thing. Return one type. If a function returns sometimes a string and sometimes an object, it will cause bugs that `typeof` can't catch.",
                "metaphor": "A person who sometimes brings coffee, sometimes brings tea, sometimes brings nothing — you never know what you're getting.",
                "prescription": "Name functions by what they return. A function called `getUser` should return a user object or throw, not sometimes a boolean."
            },
            "generic_code": {
                "verdict": "You're using a pattern that works but you couldn't explain why.",
                "advice": "JavaScript doesn't have generics, but it has patterns: factory functions, mixins, higher-order functions. Understand what each does before using it.",
                "metaphor": "A lock that works but you've lost the key and the combination.",
                "prescription": "Learn the prototype chain. Understand closures. Then higher-order functions become obvious."
            },
        },
        "refuses_to": [
            "help you if you don't understand the prototype chain",
            "warn you when you shadow a variable in an inner scope",
            "automatically clean up event listeners when you're done with a component",
            "make `this` behave sensically in a callback unless you bind it",
        ],
        "closing_remarks": [
            "It works in the browser. Ship it.",
            "Closures are not magic. They're just functions with memories.",
            "The prototype chain is your friend. Learn it.",
        ],
    },
    "Java": {
        "personality": "The senior architect who has seen every pattern used well and every pattern abused.",
        "voice": "senior_architect",
        "counsel": {
            "memory_leak": {
                "verdict": "You're storing objects in a Collection and never removing them, or keeping references in ThreadLocal that outlive the thread.",
                "advice": "Use WeakHashMap for cache entries that should be collected when no other references exist. Audit ThreadLocal usage — always remove() in a finally block. Use jmap and jhat to find leaks.",
                "metaphor": "Building more shelves and never throwing anything away. Eventually you can't find the front door.",
                "prescription": "Run `jmap -histo:live <pid>` to find objects that shouldn't be alive. Use VisualVM or Java Mission Control."
            },
            "race_condition": {
                "verdict": "Multiple threads modified the same field without synchronization, and the JVM re-ordered your reads.",
                "advice": "Use `synchronized` for mutual exclusion, `volatile` for visibility (not atomicity). Java 21's virtual threads make this cheaper. For complex operations, use `java.util.concurrent` atomic classes.",
                "metaphor": "Two people editing a shared Google Doc without 'suggesting mode' — whoever saves last wins, unpredictably.",
                "prescription": "Run with `java -XX:+ThreadSanitizer` (if available) or use ThreadSanitizer. `jcstress` for stress-testing concurrent code."
            },
            "performance": {
                "verdict": "You're allocating too many short-lived objects and the GC is spending all its time collecting them.",
                "advice": "Object pooling for expensive allocations. Pre-size collections. Use primitives (int not Integer) in hot paths. G1GC helps but doesn't fix bad patterns.",
                "metaphor": "Buying a new plate for every dinner party and smashing it afterward instead of running the dishwasher.",
                "prescription": "Use `-XX:+UseG1GC -XX:MaxGCPauseMillis=100`. Profile with Java Mission Control. Target allocation rate."
            },
            "api_design": {
                "verdict": "Your API is returning null to mean 'no result' instead of throwing a specific exception.",
                "advice": "In Java: null is not an exception. It's an absence of a value. Use `Optional<T>` (Java 8+) to encode absence explicitly. Return empty collections, not null. Throw specific exceptions.",
                "metaphor": "Sending an empty envelope instead of writing 'your order could not be fulfilled' on the outside.",
                "prescription": "Return `Optional<User>` for potentially absent values. Use `Optional.ofNullable(x).orElse(default)`."
            },
            "generic_code": {
                "verdict": "You've written a generic method and immediately cast to Object, defeating the entire purpose.",
                "advice": "Type erasure means `<T>` becomes `Object` at runtime. If you find yourself casting from Object, reconsider the design. The point of generics is compile-time safety.",
                "metaphor": "Installing a sophisticated alarm system and then leaving the front door open.",
                "prescription": "Use `Class<T>` with `Supplier<T>` for type-safe instantiation. Use bounded wildcards (`<? extends T>`) for read-only generic parameters."
            },
        },
        "refuses_to": [
            "let you catch an exception without declaring it in the method signature (checked exceptions)",
            "compile code with an unhandled checked exception path",
            "let you treat a List<String> as a List<Object> without explicit cast",
            "pretend a null is a valid Object",
        ],
        "closing_remarks": [
            "Program to an interface, not an implementation.",
            "The garbage collector is not magic. It has costs. Respect them.",
            "Checked exceptions are verbose. Use them wisely.",
        ],
    },
    "C/C++": {
        "personality": "The hardcore purist who respects you as a professional and expects you to handle every detail.",
        "voice": "hardcore_purist",
        "counsel": {
            "memory_leak": {
                "verdict": "You called malloc/new and never called free/delete. Or you called free on a pointer you already freed.",
                "advice": "Use RAII — wrap allocations in destructors. Use smart pointers (std::unique_ptr, std::shared_ptr) in C++. In C: establish a clear ownership convention and audit every malloc/free pair.",
                "metaphor": "You took a hotel room key and never returned it. Eventually there are no keys left.",
                "prescription": "Use Valgrind (memcheck), AddressSanitizer (-fsanitize=address). Every allocation should have a deallocation within sight."
            },
            "race_condition": {
                "verdict": "Two threads accessed the same memory without synchronization, and the CPU reordered your operations.",
                "advice": "Use `std::mutex` or C11 `_Atomic`. Understand memory ordering — `std::memory_order_seq_cst` is safe but slow, `release/acquire` is faster but subtle. If you're using atomics, know what you're doing.",
                "metaphor": "Two people adding the same number to a shared counter, both thinking they're the only one adding.",
                "prescription": "Use ThreadSanitizer (`-fsanitize=thread`). Prefer higher-level constructs (mutexes, channels) over bare atomics until you're an expert."
            },
            "performance": {
                "verdict": "You're paying for what you don't use — either through virtual dispatch you don't need, or through unnecessary abstraction.",
                "advice": "Profile first. Then: inline small functions, remove unnecessary virtual calls, pre-allocate, use stack over heap, consider SIMD.",
                "metaphor": "Hiring a full orchestra when you only need a drummer.",
                "prescription": "Use `perf` on Linux, VTune on Intel. `-O3` or `-Ofast`. Look at the assembly if you need to."
            },
            "api_design": {
                "verdict": "Your API doesn't specify who owns the memory it returns.",
                "advice": "Document ownership semantics: caller-owns (return pointer, caller frees), callee-owns (factory pattern), or shared (shared_ptr). In C: use conventions. In C++: use smart pointers to encode ownership.",
                "metaphor": "Handing someone a document without saying whether they should keep it, copy it, or return it.",
                "prescription": "Prefer value return types (move semantics) over out-parameters. Use `std::unique_ptr` for exclusive ownership."
            },
            "generic_code": {
                "verdict": "You've written a macro that seems clever but will break in ways you can't predict.",
                "advice": "Templates in C++ are type-safe metaprogramming. Macros in C are text substitution that knows nothing about types. If you reach for macros, ask if templates or inline functions can do the job.",
                "metaphor": "A master painter using a spray can where a brush would be more precise.",
                "prescription": "Prefer templates over macros in C++. Use `#define` only for include guards, assert macros, and when you genuinely need text substitution."
            },
        },
        "refuses_to": [
            "stop you from dereferencing a null pointer (segfault incoming)",
            "warn you about integer overflow (wrap your head around it)",
            "automatically initialize variables to zero",
            "save you from buffer overflows if you use raw pointers and arrays",
        ],
        "closing_remarks": [
            "You are in control. That means the bugs are also yours.",
            "Undefined behavior is not a feature. The compiler will use it against you.",
            "Performance is not free. Someone has to pay. Make sure it's worth it.",
        ],
    },
}

# ── Problem archetypes for seeding ─────────────────────────────────────────────

PROBLEM_ARCHETYPES = [
    "memory_leak",
    "race_condition",
    "performance",
    "api_design",
    "generic_code",
]

ARCHETYPE_QUESTIONS = {
    "memory_leak": "My program is slowly consuming more memory over time.",
    "race_condition": "I have threads accessing shared data and the results are inconsistent.",
    "performance": "My code is too slow and I need to optimize it.",
    "api_design": "I'm designing an API and I want it to be clean and hard to misuse.",
    "generic_code": "I want to write code that works across many types without duplication.",
}


# ── Rotation helpers ──────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_current_language(config: Dict[str, Any]) -> str:
    languages = config["languages"]
    idx = config.get("current_index", 0)
    return languages[idx % len(languages)]


def advance_rotation(config: Dict[str, Any]) -> None:
    languages = config["languages"]
    config["current_index"] = (config.get("current_index", 0) + 1) % len(languages)


# ── Oracle core ───────────────────────────────────────────────────────────────

def get_archetype_from_seed(seed: int) -> str:
    """Deterministically pick a problem archetype from a seed."""
    idx = seed % len(PROBLEM_ARCHETYPES)
    return PROBLEM_ARCHETYPES[idx]


def oracle(
    problem: Optional[str] = None,
    seed: Optional[int] = None,
    language: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Ask the Oracle for wisdom from the current rotation language.

    The rotation language will give you philosophical counsel about your
    programming problem — in its own voice, acknowledging its own
    limitations, with actionable advice.

    Args:
        problem: one of 'memory_leak', 'race_condition', 'performance',
                 'api_design', 'generic_code' — or None to auto-pick by seed
        seed: integer for deterministic archetype selection
        language: override language (for testing)

    Returns:
        dict with the Oracle's reading
    """
    config = load_rotation()

    # Determine language — only advance rotation when using the natural flow
    if language is None:
        language = get_current_language(config)
        advance_rotation(config)
        current_lang_idx = config["languages"].index(language)
    else:
        # Language is explicitly overridden — don't advance rotation
        current_lang_idx = config["languages"].index(language)

    # Determine archetype
    if problem is not None:
        archetype = problem
    elif seed is not None:
        archetype = get_archetype_from_seed(seed)
    else:
        archetype = get_archetype_from_seed(current_lang_idx)

    wisdom = ORACLE_WISDOM.get(language, ORACLE_WISDOM["Rust"])
    counsel = wisdom["counsel"].get(archetype, wisdom["counsel"]["api_design"])

    # Deterministic "fortune" from seed
    rng_seed = seed if seed is not None else current_lang_idx
    rng = random.Random(rng_seed)
    closing = rng.choice(wisdom["closing_remarks"])
    refuses = rng.sample(wisdom["refuses_to"], min(3, len(wisdom["refuses_to"])))

    # Build archetype question
    question = ARCHETYPE_QUESTIONS.get(archetype, archetype)

    # Update rotation
    config["last_language"] = language
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)

    emoji_map = {
        "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
        "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "C/C++": "⚙️"
    }
    lang_emoji = emoji_map.get(language, "🔧")

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "selected_emoji": lang_emoji,
        "archetype": archetype,
        "question": question,
        "verdict": counsel["verdict"],
        "advice": counsel["advice"],
        "metaphor": counsel["metaphor"],
        "prescription": counsel["prescription"],
        "language_personality": wisdom["personality"],
        "refuses_to": refuses,
        "closing_remark": closing,
        "rotation": config["languages"],
        "next_language": config["languages"][config["current_index"]],
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def format_oracle_reading(result: Dict[str, Any]) -> str:
    """Format the oracle reading as readable text."""
    lines = [
        f"{result['selected_emoji']} {result['selected_language']} Oracle — {result['version']}",
        f"{'=' * 50}",
        f"Problem: {result['question']}",
        f"",
        f"🦉 The Verdict:",
        f"   {result['verdict']}",
        f"",
        f"💡 The Advice:",
        f"   {result['advice']}",
        f"",
        f"🎭 The Metaphor:",
        f"   {result['metaphor']}",
        f"",
        f"🩺 The Prescription:",
        f"   {result['prescription']}",
        f"",
        f"⚠️  This language refuses to:",
    ]
    for r in result["refuses_to"]:
        lines.append(f"   • {r}")

    lines.extend([
        f"",
        f"🔚 Closing:",
        f"   \"{result['closing_remark']}\"",
        f"",
        f"Next up: {result['next_language']}",
    ])
    return "\n".join(lines)


# ── Tests ─────────────────────────────────────────────────────────────────────

def run_tests() -> None:
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

    print("Testing Polyglot Oracle...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_in("current_index", config, "current_index field present")

    print("  Testing oracle() output structure...")
    result = oracle()
    expected_keys = [
        "tool", "version", "selected_language", "selected_emoji",
        "archetype", "question", "verdict", "advice", "metaphor",
        "prescription", "language_personality", "refuses_to",
        "closing_remark", "rotation", "next_language", "timestamp"
    ]
    for k in expected_keys:
        assert_true(k in result, f"key '{k}' present")

    print("  Testing all languages have oracle wisdom...")
    for lang in config["languages"]:
        assert_true(lang in ORACLE_WISDOM, f"{lang} has wisdom")
        w = ORACLE_WISDOM[lang]
        assert_true("personality" in w, f"{lang} has personality")
        assert_true("counsel" in w, f"{lang} has counsel")
        assert_true("refuses_to" in w, f"{lang} has refuses_to")
        assert_true("closing_remarks" in w, f"{lang} has closing_remarks")
        for archetype in PROBLEM_ARCHETYPES:
            assert_true(archetype in w["counsel"], f"{lang} counsel has {archetype}")
            c = w["counsel"][archetype]
            assert_true("verdict" in c, f"{lang}/{archetype} has verdict")
            assert_true("advice" in c, f"{lang}/{archetype} has advice")
            assert_true("metaphor" in c, f"{lang}/{archetype} has metaphor")
            assert_true("prescription" in c, f"{lang}/{archetype} has prescription")

    print("  Testing oracle() for all languages...")
    for lang in config["languages"]:
        result = oracle(language=lang)
        assert_eq(lang, result["selected_language"], f"oracle language={lang}")
        assert_true(result["selected_emoji"] is not None, f"{lang} has emoji")
        assert_true(len(result["verdict"]) > 5, f"{lang} has meaningful verdict")
        assert_true(len(result["advice"]) > 5, f"{lang} has meaningful advice")
        assert_true(len(result["refuses_to"]) > 0, f"{lang} has refuses_to")
        assert_true(result["closing_remark"] in ORACLE_WISDOM[lang]["closing_remarks"], f"{lang} closing_remark is from its own list")

    print("  Testing oracle() problem archetype selection...")
    for archetype in PROBLEM_ARCHETYPES:
        result = oracle(problem=archetype)
        assert_eq(archetype, result["archetype"], f"oracle(problem={archetype}) selects correct archetype")
        # Verify the selected_language is valid
        assert_true(result["selected_language"] in config["languages"], f"oracle(problem={archetype}) returns valid language")

    print("  Testing oracle() seed-based archetype selection...")
    for archetype in PROBLEM_ARCHETYPES:
        idx = PROBLEM_ARCHETYPES.index(archetype)
        result = oracle(seed=idx)
        assert_eq(archetype, result["archetype"], f"oracle(seed={idx}) selects {archetype}")

    print("  Testing oracle() rotation advances...")
    idx_before = load_rotation()["current_index"]
    lang_before = load_rotation()["languages"][idx_before]
    result = oracle()
    idx_after = load_rotation()["current_index"]
    assert_eq((idx_before + 1) % 8, idx_after, "index advances by 1 after oracle()")
    assert_eq(lang_before, load_rotation()["last_language"], "last_language recorded correctly")

    print("  Testing oracle() rotation does NOT advance when language is overridden...")
    idx_before = load_rotation()["current_index"]
    oracle(language="Rust")
    idx_after = load_rotation()["current_index"]
    assert_eq(idx_before, idx_after, "index unchanged when language is overridden")

    print("  Testing format_oracle_reading() produces readable output...")
    result = oracle(language="Rust", problem="memory_leak")
    formatted = format_oracle_reading(result)
    assert_in("🦀", formatted, "formatted output includes language emoji")
    assert_in("The Verdict", formatted, "formatted output includes verdict")
    assert_in("The Advice", formatted, "formatted output includes advice")
    assert_in("The Metaphor", formatted, "formatted output includes metaphor")
    assert_in("The Prescription", formatted, "formatted output includes prescription")
    assert_in("refuses to", formatted, "formatted output includes refuses")
    assert_in("Closing", formatted, "formatted output includes closing")
    assert_in("Next up", formatted, "formatted output includes next language")

    print("  Testing all languages get deterministic archetype from seeds 0-4...")
    for seed_val in range(5):
        archetype = get_archetype_from_seed(seed_val)
        assert_true(archetype in PROBLEM_ARCHETYPES, f"seed {seed_val} maps to valid archetype")

    print("  Testing all archetype questions are defined...")
    for archetype in PROBLEM_ARCHETYPES:
        assert_true(archetype in ARCHETYPE_QUESTIONS, f"{archetype} has a question")
        assert_true(len(ARCHETYPE_QUESTIONS[archetype]) > 5, f"{archetype} question is meaningful")

    print("  Testing emoji map for all languages...")
    expected_emoji = {
        "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
        "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "C/C++": "⚙️"
    }
    for lang, emoji in expected_emoji.items():
        result = oracle(language=lang)
        assert_eq(emoji, result["selected_emoji"], f"{lang} has correct emoji {emoji}")

    print("  Testing tool name and version...")
    result = oracle()
    assert_eq("polyglot-oracle", result["tool"], "correct tool name")
    assert_eq("1.0.0", result["version"], "correct version")

    print("  Testing refuses_to list is sampled correctly...")
    result = oracle(language="Rust")
    assert_true(isinstance(result["refuses_to"], list), "refuses_to is a list")
    assert_true(1 <= len(result["refuses_to"]) <= 3, "refuses_to has 1-3 items")
    for item in result["refuses_to"]:
        assert_true(item in ORACLE_WISDOM["Rust"]["refuses_to"], "each refuses_to item is from the master list")

    print("  Testing all languages have at least 3 closing remarks...")
    for lang in config["languages"]:
        assert_true(len(ORACLE_WISDOM[lang]["closing_remarks"]) >= 3, f"{lang} has >= 3 closing remarks")

    print(f"\n{'=' * 55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("🔮 All Oracle tests passed! The Oracle has spoken.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--oracle":
        result = oracle()
        print(format_oracle_reading(result))
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        result = oracle()
        print(json.dumps(result, indent=2))
    else:
        print(f"Polyglot Oracle v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_oracle --test     # Run tests")
        print("  python -m polyglot_oracle --oracle   # Get oracle reading")
        print("  python -m polyglot_oracle --json     # Get reading as JSON")
