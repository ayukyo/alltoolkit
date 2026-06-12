#!/usr/bin/env python3
"""
🌋 Polyglot Faultline v1.0
An "error archaeology" tool — digs into the historical, cultural, and
linguistic roots of error messages across programming languages.

For the selected rotation language, this tool:
  1. Reveals the "fault line" — the syntactic/semantic weak points where
     developers most often stumble
  2. Excavates the "error stratigraphy" — how an error message has evolved
     across language versions (what changed, what stayed the same)
  3. Generates a "seismic risk map" — which language features are most
     likely to cause earthquakes in developer productivity
  4. Translates cryptic error codes into human-readable "aftershock reports"
  5. Provides "fault zone survival guides" — how to navigate dangerous areas

Creative concept: "Every language has fault lines — historical seams where
design decisions from different eras collide. This tool maps the trembling."

Distinct from existing tools:
  - polyglot_weather:     atmospheric dynamics (pressure, fronts, storms)
  - polyglot_chronicle:   daily history (what happened on this day)
  - polyglot_digest:      syntax parallel snippets (same code, different syntax)
  - polyglot_resonator:   harmonic relationships (frequency lens)
  - polyglot_dna:         genetic trait mapping (trait lens)
  - polyglot_bridges:     problem→solution maps (conceptual)
  - language_archaeology: historical lineage (deep temporal dig)
  - language_compass:     learning journey maps (future milestones)
  - language_ethos:       philosophical manifesto (belief/identity)
  - language_sage:        idioms, tips, pitfalls (practical wisdom)
  - language_paradigm_weaver: paradigm assumptions (worldview lens)

Faultline is about ERROR ARCHAEOLOGY — the trembling seams where languages
break down, how errors have evolved, and how to survive the aftershocks.
"""

import json
import os
import random
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-faultline"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = str(
    Path(__file__).parent.parent.parent / "language_rotation.json"
)

# The 8-language rotation sequence
ROTATION_ORDER = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]


def load_rotation():
    """Load language rotation config."""
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data):
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Error archaeology data ───────────────────────────────────────────────────

FAULT_ZONES = {
    "Rust": {
        "emoji": "🦀",
        "seismic_risk": 6,
        "danger_zones": [
            {"zone": "borrow_checker", "risk_level": 9,
             "description": "The borrow checker is Rust's most feared and respected boundary. "
                            "It enforces memory safety at compile time, which means a whole class "
                            "of bugs simply cannot compile. But it also means the error messages "
                            "can be long, complex, and intimidating to newcomers.",
             "common_patterns": ["use after move", "mutable borrow conflict", "lifetime mismatch",
                                "cannot borrow as mutable", "does not live long enough"],
             "survival_guide": [
                 "Read the error from bottom to top — the root cause is usually at the end",
                 "The 'help:' suggestions are gold — read every one",
                 "If stuck, add type annotations to help the compiler narrow down the issue",
                 "rustc --explain Exxxx gives detailed explanations",
                 "Try rust-analyzer in your IDE — it gives inline error explanations",
             ]},
            {"zone": "lifetime_annotations", "risk_level": 8,
             "description": "Lifetimes are Rust's way of ensuring memory safety without "
                            "garbage collection. They can feel like a foreign language within "
                            "a foreign language — abstract, underdocumented, and subtle.",
             "common_patterns": ["missing lifetime specifier", "lifetime parameter not found",
                                "could not infer appropriate lifetime", "returns a value "
                                "borrowed from `x`"],
             "survival_guide": [
                 "Start with 'a and 'static — most simple cases use these",
                 "Lifetimes don't change how long data lives — they describe relationships",
                 "Elided lifetimes (implicit) work for simple functions — don't force them",
                 "When in doubt, add more explicit lifetimes to narrow down the issue",
             ]},
            {"zone": "ownership_moves", "risk_level": 7,
             "description": "Rust's ownership model means values can only have one owner. "
                            "Moving a value transfers ownership, and the original becomes invalid. "
                            "This trips up developers from GC languages.",
             "common_patterns": ["value borrowed here after move", "move occurs because "
                                "x has type", "cannot move out of x which is behind a shared reference"],
             "survival_guide": [
                 "Clone (.clone()) when you need multiple owners — it's always safe",
                 "Use references (&) when you just need to read data",
                 "Use Arc<T> for shared ownership across threads",
                 "Rc<T> is for single-threaded shared ownership",
             ]},
            {"zone": "pattern_matching_exhaustiveness", "risk_level": 5,
             "description": "Rust requires all enum variants to be handled in match expressions. "
                            "This is a feature (catches bugs) but can be annoying when adding new variants.",
             "common_patterns": ["non-exhaustive patterns", "missing match arms", "wildcard arm",
                                "unreachable pattern"],
             "survival_guide": [
                 "The _ => arm catches everything — use it as a fallback during development",
                 "#[derive(Debug)] on enums gives better error messages",
                 "Use ..= for catch-all patterns in complex enums",
             ]},
            {"zone": "async_await", "risk_level": 7,
             "description": "Rust's async/await is powerful but the error messages can be cryptic. "
                            "Send + Sync errors are particularly dreaded.",
             "common_patterns": ["future cannot be sent between threads", "future created by async "
                                "block is not Future: Send", "error future must be Send",
                                " Trait 'Send' is not implemented"],
             "survival_guide": [
                 "Add + Send to your async return types when you see Send errors",
                 "tokio::spawn expects Send futures",
                 "Use .await inside async blocks rather than blocking",
             ]},
        ],
        "error_stratigraphy": {
            "rustc_1.0": "Error messages were blunt and unhelpful — 'expected x, found y' was the norm. "
                        "No suggestions, no 'did you mean', no help text.",
            "rustc_1.12": "The 'self-configuring' compiler era began. Error messages improved "
                         "dramatically with the arrival of the modern error reporting system.",
            "rustc_1.39": "async/await landed, and with it came a new class of opaque Send/Sync errors "
                         "that haunted developers for years.",
            "rustc_1.56": "The 'precise' edition brought more accurate lifetime errors — "
                         "less confusing, more actionable.",
            "rustc_1.71": "Stabilized std::any::Provider APIs with clearer trait bound errors.",
            "rustc_1.77": "Improved stack overflow messages with more context.",
            "rustc_2024": "Modern Rust has some of the best error messages in compiled languages, "
                         "with color-coded output, suggestions, and 'did you mean x' corrections.",
        },
        "iconic_errors": [
            {"code": "E0502", "message": "borrow checker抗议：cannot borrow x as mutable because "
                     "it is also borrowed as immutable",
             "seismic_magnitude": 7,
             "description": "The classic 'two borrowers' error — one of the first errors new "
                           "Rustaceans encounter and remember forever."},
            {"code": "E0507", "message": "value borrowed here after move",
             "seismic_magnitude": 6,
             "description": "Moved values can't be used again. A fundamental Rust concept that "
                           "catches real bugs but confuses newcomers."},
            {"code": "E0277", "message": "the trait bound `T: Foo` is not satisfied",
             "seismic_magnitude": 5,
             "description": "Trait bound errors — often the result of missing a derive macro "
                           "or a required trait implementation."},
        ],
    },
    "Go": {
        "emoji": "🐹",
        "seismic_risk": 4,
        "danger_zones": [
            {"zone": "goroutine_leaks", "risk_level": 8,
             "description": "Go's concurrency model is simple (goroutines + channels) but "
                            "goroutine leaks are silent killers. A leaked goroutine consumes "
                            "memory and CPU forever with no error, no warning.",
             "common_patterns": ["goroutine not exiting", "channel blocking forever",
                                "select with no cases", "infinite channel send"],
             "survival_guide": [
                 "Use context.WithCancel to enable clean goroutine shutdown",
                 "Track goroutine count in tests — runtime.NumGoroutine()",
                 "Use goleak (uber/goleak) in tests to detect goroutine leaks",
                 "Buffered channels prevent blocking on send until buffer is full",
                 "Never start a goroutine without a shutdown plan",
             ]},
            {"zone": "nil_pointer_dereference", "risk_level": 7,
             "description": "Go will panic with 'nil pointer dereference' at runtime. "
                            "Unlike Java, Go has no null safety net at compile time.",
             "common_patterns": ["nil pointer dereference", "index out of range [0] with nil slice",
                                "cannot call nil function", "nil interface"],
             "survival_guide": [
                 "Use pointer receivers only when necessary — value receivers are safer",
                 "Check for nil explicitly before dereferencing",
                 "Use errors.Is() to check error values rather than string matching",
                 "Initialize maps and slices with make() — nil maps panic on write",
             ]},
            {"zone": "interface_confusion", "risk_level": 6,
             "description": "Go's interfaces are implicit (no 'implements' keyword). "
                            "This makes duck typing work but can lead to subtle type confusion.",
             "common_patterns": ["cannot use x as type y", "interface conversion panic",
                                "concurrent map iteration", "map concurrent read and write"],
             "survival_guide": [
                 "Keep interfaces small — one or two methods max",
                 "Define interfaces where you USE them, not where you IMPLEMENT them",
                 "Accept interfaces, return structs (Crocker's rule)",
                 "Use sync.Map for concurrent map access",
             ]},
            {"zone": "defer_evaluation", "risk_level": 5,
             "description": "Deferred functions run LIFO (last-in-first-out) after the surrounding "
                            "function returns. This sounds simple but leads to subtle bugs.",
             "common_patterns": ["defer with named return values", "defer in loops",
                                "defer function literal captures loop variable"],
             "survival_guide": [
                 "Deferred functions run in LIFO order — the last defer runs first",
                 "Never name return values in functions with defer",
                 "Avoid defers in loops — each iteration adds to the defer stack",
                 "Loop variables captured by defer closures should be passed as parameters",
             ]},
            {"zone": "slices_maps_growth", "risk_level": 5,
             "description": "Slices and maps are reference types. Append can cause unexpected "
                            "behavior if not understanding copy-on-write semantics.",
             "common_patterns": ["slice bounds out of range", "cannot assign to map index",
                                "grows beyond capacity", "append reallocates underlying array"],
             "survival_guide": [
                 "Use make([]T, 0, expected_size) to pre-allocate when size is known",
                 "append() returns a new slice — always capture the return value",
                 "Slices share underlying arrays — copying can cause aliasing bugs",
                 "copy() is explicit — use it when you need independent copies",
             ]},
        ],
        "error_stratigraphy": {
            "go1.0": "Error messages were sparse and technical. Stack traces were long but "
                    "not always helpful. No error wrapping.",
            "go1.4": "The 'go fund' era — build times improved, but error messages remained basic.",
            "go1.13": "Error wrapping landed with fmt.Errorf and %w — this was a watershed moment. "
                     "For the first time, errors could carry context without losing the original error.",
            "go1.20": "Multiple error wrapping with errors.Join, and improved panic recovery messages.",
            "go1.22": "Improved range loop semantics — loop variables are now per-iteration, "
                     "fixing a long-standing gotcha.",
            "go1.23": "Iterators (range over functions) added, with new iteration-related error patterns.",
        },
        "iconic_errors": [
            {"code": "runtime.error: goroutine stack", "message": "stack memory limit exceeded",
             "seismic_magnitude": 8,
             "description": "Infinite goroutine recursion — a goroutine used up all stack memory "
                           "and the runtime panics with a stack overflow."},
            {"code": "sync: unlock of unlocked mutex", "message": "unlock of unlocked mutex",
             "seismic_magnitude": 7,
             "description": "Go's mutexes are not reentrant. Unlocking an unlocked mutex causes a panic."},
            {"code": "all goroutines are asleep — deadlock", "message": "all goroutines are asleep — deadlock",
             "seismic_magnitude": 7,
             "description": "The runtime detected that all goroutines are blocked — a deadlock. "
                           "Classic sign of a channel or mutex misuse."},
        ],
    },
    "Swift": {
        "emoji": "🦅",
        "seismic_risk": 5,
        "danger_zones": [
            {"zone": "optional_chains", "risk_level": 7,
             "description": "Swift's optional system is powerful but the 'optional chain broke' "
                            "errors can be confusing when chaining many optionals.",
             "common_patterns": ["optional type 'T?' has no member 'x'", "value of type 'T?'",
                                "unwrap a nil", "nil coalescing error", "optional chaining result"],
             "survival_guide": [
                 "Use if let or guard let to safely unwrap before use",
                 "nil coalescing operator (??) provides a default value",
                 "XCTUnwrap() in tests to assert optionals have values",
                 "Implicitly unwrapped optionals (!) should be used sparingly",
             ]},
            {"zone": "copy_on_write", "risk_level": 6,
             "description": "Swift uses copy-on-write for collections and some types. "
                            "Understanding when copies happen is key to performance and correctness.",
             "common_patterns": ["modifying shared state", "copy on write triggered",
                                "value type semantics issue", "mutating a copy"],
             "survival_guide": [
                 "Structs are value types — mutation creates a copy",
                 "Classes are reference types — mutation affects all references",
                 "Use inout to explicitly mutate a value type in a function",
                 "Array and Dictionary are value types that use COW internally",
             ]},
            {"zone": "generic_constraints", "risk_level": 6,
             "description": "Swift generics are powerful but type constraint errors can be opaque.",
             "common_patterns": ["generic parameter 'T' could not be inferred", "protocol 'T' "
                                "only available on iOS", "type does not conform to protocol",
                                "same-type requirement conflict"],
             "survival_guide": [
                 "Use where clauses to add constraints to generic functions",
                 "Add explicit type annotations when inference fails",
                 "Protocol-associated types need default implementations",
                 "Check availability with #available() for platform-specific APIs",
             ]},
            {"zone": "arc_strong_reference_cycles", "risk_level": 8,
             "description": "Before ARC, reference counting was manual. With ARC, strong reference "
                            "cycles (retain cycles) are the new memory leak.",
             "common_patterns": ["memory leak", "strong reference cycle", "deinit not called",
                                "weak/unowned confusion"],
             "survival_guide": [
                 "Use weak for optional delegates (viewController.delegate = nil to break cycle)",
                 "Use unowned for non-optional references to self",
                 "In Swift 5, combine uses weak for its subscription management",
                 "Profile with Instruments to detect retain cycles",
             ]},
            {"zone": "actor_isolation", "risk_level": 7,
             "description": "Swift's actors (Swift 5.5+) enforce isolation — data isn't accessible "
                            "across actor boundaries without async/await.",
             "common_patterns": ["actor-isolated method can't be called", "capture of "
                                "non-sendable value", "MainActor isolation violations"],
             "survival_guide": [
                 "Mark cross-actor calls as async",
                 "Use @MainActor for UI-bound code",
                 "Implement Sendable conformance for custom types crossing actor boundaries",
                 "nonisolated keyword opts out of actor isolation for specific methods",
             ]},
        ],
        "error_stratigraphy": {
            "swift1.0": "Early Swift had helpful but verbose error messages. Type inference was limited.",
            "swift2.0": "Error handling with try/catch/throws was introduced, replacing NSError. "
                       "More expressive error handling.",
            "swift3.0": "API naming conventions changed. Many old error messages referred to "
                       "old-style method names that no longer existed.",
            "swift4.2": "Improved dictionary and collection error messages.",
            "swift5.5": "Actors and async/await introduced — a whole new class of isolation errors. "
                       "MainActor errors became common.",
            "swift5.9": "Macros introduced, with new macro-related error patterns.",
            "swift6.0": "Complete concurrency checking — Sendable errors are now enforced.",
        },
        "iconic_errors": [
            {"code": "EXC_BAD_ACCESS", "message": "Memory management failure — over-released object",
             "seismic_magnitude": 8,
             "description": "The classic 'message sent to deallocated object' crash. Swift "
                           "tries to prevent this but it can still happen with toll-free bridging."},
            {"code": "Swift/Optional.swift", "message": "unexpectedly found nil while unwrapping",
             "seismic_magnitude": 7,
             "description": "Force-unwrapping a nil optional (!) causes a runtime crash. "
                           "The infamous 'unexpectedly found nil' — a rite of passage."},
            {"code": "ActorIsolationViolation", "message": "actor-isolated method can't be called",
             "seismic_magnitude": 6,
             "description": "Swift 5.5+ concurrency violations — trying to access actor state "
                           "from the wrong isolation context."},
        ],
    },
    "Kotlin": {
        "emoji": "🤖",
        "seismic_risk": 4,
        "danger_zones": [
            {"zone": "null_safety", "risk_level": 7,
             "description": "Kotlin's type system distinguishes nullable (T?) from non-nullable (T). "
                            "The 'null pointer exception' is mostly eliminated at compile time, but "
                            "interoperability with Java code can reintroduce NPEs.",
             "common_patterns": ["NullPointerException", "null pointer on invoke",
                                "platform type null", "lateinit property has not been initialized"],
             "survival_guide": [
                 "Use ?. (safe call) and ?: (elvis operator) by default",
                 "Use !! only when you're certain the value is non-null",
                 "Use lateinit for properties initialized after construction",
                 "Use @Nullable/@NotNull annotations when interoperating with Java",
             ]},
            {"zone": "coroutines", "risk_level": 8,
             "description": "Kotlin coroutines are powerful but cancellation and structured "
                            "concurrency can trip up even experienced developers.",
             "common_patterns": ["CancellationException", "CoroutineScope leak", "blocking in async",
                                "Structured concurrency conflict", "Job not complete"],
             "survival_guide": [
                 "Never block in a coroutine — use suspend functions",
                 "Use withContext(Dispatchers.IO) for blocking operations",
                 "Handle CancellationException explicitly if needed",
                 "Use viewModelScope in Android, GlobalScope is almost never right",
                 "runBlocking is for tests only — never in production code",
             ]},
            {"zone": "generics_variance", "risk_level": 6,
             "description": "Kotlin's declaration-site variance (out/in) and type projections "
                            "can be confusing when crossing Java interop boundaries.",
             "common_patterns": ["type mismatch", "projected type", "star projection confusion",
                                "inconsistent type arguments", "variance conflict"],
             "survival_guide": [
                 "Use out for producer-only types (covariance)",
                 "Use in for consumer-only types (contravariance)",
                 "Use @UnsafeVariance to suppress warnings when you're sure",
                 "Understand PECS (Producer Extends, Consumer Super)",
             ]},
            {"zone": "extension_functions", "risk_level": 4,
             "description": "Extension functions look like methods but resolve statically. "
                            "They don't actually modify the class, which can be surprising.",
             "common_patterns": ["unresolved reference in extension", "extension on nullable",
                                "shadowing extension", "this in extension refers to receiver"],
             "survival_guide": [
                 "Extensions resolve statically — they don't support virtual dispatch",
                 "An extension with same name as a member wins the member",
                 "Nullable receivers (T?) allow calling on null values",
             ]},
            {"zone": "smart_cast", "risk_level": 5,
             "description": "Kotlin smart-casts variables after explicit checks, but this "
                            "can be invalidated by intervening code.",
             "common_patterns": ["smart cast to 'T' is impossible", "nullable type",
                                "smart cast target is not mutable", "assignment invalidates smart cast"],
             "survival_guide": [
                 "Smart casts work within the same basic block after is/as checks",
                 "Captured variables must be vals (immutable) for smart cast",
                 "Use explicit let { } transformation when smart cast fails",
                 "Abstract away mutability with val or read-only collections",
             ]},
        ],
        "error_stratigraphy": {
            "kotlin1.0": "Initial release. Basic null safety and extension functions. "
                         "Error messages were decent but not great.",
            "kotlin1.1": "Coroutines were experimental. Early adopters faced cryptic errors.",
            "kotlin1.3": "Coroutines became stable — but structured concurrency was still being figured out.",
            "kotlin1.5": "Sealed classes improvements and typealias. More precise type errors.",
            "kotlin1.7": "Gradual type inference improvements reduced 'type inference failed' errors.",
            "kotlin2.0": "Kotlin K2 compiler brought improved error messages and faster compilation.",
        },
        "iconic_errors": [
            {"code": "NullPointerException", "message": "null pointer — platform type not null-safed",
             "seismic_magnitude": 7,
             "description": "Usually from Java interop — a Java method returns a platform type "
                           "(T!) that Kotlin treats as potentially null."},
            {"code": "CancellationException", "message": "Job was cancelled",
             "seismic_magnitude": 6,
             "description": "Coroutine was cancelled — either explicitly or because "
                           "its scope was cancelled."},
            {"code": "KotlinNullPointerException", "message": "null pointer on invoke on non-null",
             "seismic_magnitude": 5,
             "description": "Attempting to invoke a non-null function on a null receiver. "
                           "Mostly eliminated but still occurs in edge cases."},
        ],
    },
    "TypeScript": {
        "emoji": "📘",
        "seismic_risk": 5,
        "danger_zones": [
            {"zone": "type_inference_limits", "risk_level": 7,
             "description": "TypeScript's type inference is good but complex generic chains "
                            "can cause 'type instantiation is excessively deep' errors.",
             "common_patterns": ["type instantiation is excessively deep", "generic type 'T' "
                                "could not be inferred", "type 'never'", "excessive type depth",
                                "type alias circular reference"],
             "survival_guide": [
                 "Use explicit type annotations when inference fails",
                 "Break complex generic types into smaller named types",
                 "Use satisfies to validate without widening",
                 "Avoid deeply nested conditional types",
             ]},
            {"zone": "any_vs_unknown", "risk_level": 6,
             "description": "any bypasses type checking entirely, while unknown requires "
                            "explicit type narrowing. The wrong choice creates bugs.",
             "common_patterns": ["object is of type 'unknown'", " Property 'x' does not "
                                "exist on type 'any'", "narrowing error after type check"],
             "survival_guide": [
                 "Use unknown instead of any — it forces type narrowing",
                 "Use type guards (typeof, instanceof, custom) to narrow unknown",
                 "Use satisfies operator to validate object shapes",
                 "Enable noImplicitAny in tsconfig",
             ]},
            {"zone": "strict_null_checks", "risk_level": 6,
             "description": "strictNullChecks makes null/undefined explicit. "
                            "Disabling it creates a minefield of potential NPEs.",
             "common_patterns": ["object is possibly undefined", "cannot assign null to x",
                                "value is possibly undefined", "undefined has no properties"],
             "survival_guide": [
                 "Always enable strictNullChecks in tsconfig",
                 "Use optional chaining (?.) and nullish coalescing (??)",
                 "Use non-null assertion (!) sparingly — only when truly certain",
                 "Define strict return types on functions",
             ]},
            {"zone": "decorator_standards", "risk_level": 5,
             "description": "TypeScript decorators (experimental) went through multiple "
                            "proposal stages. Different decorator syntaxes can conflict.",
             "common_patterns": ["decorator is not allowed here", "experimental decorators",
                                "decorator metadata not emitted", "multiple decorator contexts"],
             "survival_guide": [
                 "Use 'experimentalDecorators: true' for old-style decorators",
                 "New TC39 decorators are different — don't mix them",
                 "emitDecoratorMetadata is needed for DI frameworks like tsyringe",
             ]},
            {"zone": "module_resolution", "risk_level": 5,
             "description": "Node module resolution is complex. path mappings, baseUrls, "
                            "and different moduleResolution strategies cause many 'cannot find module' errors.",
             "common_patterns": ["cannot find module", "module not found", "relative import "
                                "in external module", "module resolution mismatch"],
             "survival_guide": [
                 "Use node moduleResolution where possible",
                 "Use path mappings sparingly — prefer relative imports",
                 "Check tsconfig paths match actual project structure",
                 "Use moduleSuffixes for .mjs/.cjs resolution issues",
             ]},
        ],
        "error_stratigraphy": {
            "typescript1.0": "Basic type checking. Errors were sometimes cryptic.",
            "typescript1.4": "Union types and type aliases introduced.",
            "typescript2.0": "strictNullChecks added — a major shift in error patterns. "
                             "Many existing codebases broke.",
            "typescript2.7": "Definite assignment assertions, strict property initialization.",
            "typescript4.0": "Variadic tuple types and improved inference — new error patterns emerged.",
            "typescript4.5": "Template literal type improvements.",
            "typescript5.0": "Decorators (TC39 stage 3) — new decorator error patterns.",
            "typescript5.5": "Inferred type predicates — better narrowing errors.",
        },
        "iconic_errors": [
            {"code": "TS2322", "message": "type 'X' is not assignable to type 'Y'",
             "seismic_magnitude": 6,
             "description": "The most common TypeScript error — type mismatch. Usually "
                           "from excess properties or wrong union members."},
            {"code": "TS18046", "message": "type is of unknown type — type inference failed",
             "seismic_magnitude": 6,
             "description": "'unknown' type encountered — usually in Promise.then() callbacks "
                           "without proper typing."},
            {"code": "TS7006", "message": "parameter 'x' implicitly has an 'any' type",
             "seismic_magnitude": 5,
             "description": "Parameter needs explicit typing when noImplicitAny is enabled "
                           "and inference can't determine the type."},
        ],
    },
    "JavaScript": {
        "emoji": "🟨",
        "seismic_risk": 6,
        "danger_zones": [
            {"zone": "hoisting_and_scope", "risk_level": 8,
             "description": "JavaScript hoists var declarations and function declarations "
                            "but not let/const. This creates a minefield of subtle bugs.",
             "common_patterns": ["undefined is not a function", "cannot access before initialization",
                                " Temporal Dead Zone", "hoisting confusion"],
             "survival_guide": [
                 "Use let/const instead of var — they have block scope",
                 "Declare variables at the top of their scope",
                 "Understand TDZ (Temporal Dead Zone) for let/const",
                 "Arrow functions don't have their own 'this' binding",
             ]},
            {"zone": "this_binding", "risk_level": 8,
             "description": "'this' in JavaScript is dynamically scoped, determined by "
                            "how a function is called, not where it's defined.",
             "common_patterns": ["this is undefined", "this is not defined", "losing this",
                                "arrow function can't be used as constructor"],
             "survival_guide": [
                 "Use arrow functions () => {} for callbacks — they inherit 'this'",
                 "Use .bind(this) or store this in a variable (const self = this)",
                 "Class fields auto-bind in constructor",
                 "Don't call object methods as callbacks without binding",
             ]},
            {"zone": "async_promise_confusion", "risk_level": 7,
             "description": "Callback hell has been replaced by promise confusion. "
                            "Unhandled promise rejections are silent killers.",
             "common_patterns": ["unhandled promise rejection", "promise is rejected with reason",
                                "async function without await", "then/catch chain break"],
             "survival_guide": [
                 "Always add .catch() or use try/catch with async/await",
                 "Use Promise.allSettled() to handle multiple promises gracefully",
                 "Never ignore the return value of a promise-returning function",
                 "Use AbortController for cancellable async operations",
             ]},
            {"zone": "closure_loop_traps", "risk_level": 7,
             "description": "Closures in loops are a classic JavaScript gotcha — loop variables "
                            "are captured by reference, not by value.",
             "common_patterns": ["all closures log the same value", "var in loop closure",
                                "setTimeout in loop captures wrong variable"],
             "survival_guide": [
                 "Use let instead of var in loops — let is block-scoped",
                 "Use an IIFE (immediately invoked function expression) to capture value",
                 "Pass the loop variable as a parameter to the closure",
                 "Use for...of which binds correctly with let",
             ]},
            {"zone": "type_coercion", "risk_level": 6,
             "description": "JavaScript coerces types automatically in many contexts, "
                            "leading to '+' doing concatenation instead of addition.",
             "common_patterns": ["NaN is not equal to itself", "false == 0 is true",
                                "'5' + 3 is '53'", "[] == false is true", "== vs ==="],
             "survival_guide": [
                 "Always use === instead of ==",
                 "Use Number() or parseInt() explicitly for type conversion",
                 "Use Object.is() for NaN and -0/+0 comparison",
                 "Be explicit about string concatenation vs addition",
             ]},
        ],
        "error_stratigraphy": {
            "js1.0": "Netscape era — errors were minimal. No class system, no modules.",
            "js1.5": "try/catch/finally, error objects, getter/setter. More structured errors.",
            "js1.8": "Generators and closures — new error patterns emerged.",
            "js1.9 (ES5)": "Strict mode introduced — 'use strict' revealed hidden errors. "
                           "Property getters/setters became more formal.",
            "js2015 (ES6)": "Classes, modules, let/const, arrow functions, promises. "
                             "A new era of errors: TDZ, const reassignment, module errors.",
            "js2020 (ES11)": "Optional chaining (?.) and nullish coalescing (??) — "
                             "reduced some null-check errors.",
            "js2024 (ES15)": "Promise.withResolvers, Array grouping — new APIs, new potential errors.",
        },
        "iconic_errors": [
            {"code": "TypeError", "message": "undefined is not a function",
             "seismic_magnitude": 8,
             "description": "The most iconic JavaScript error — usually from calling something "
                           "before it's defined, or losing 'this' context."},
            {"code": "ReferenceError", "message": "cannot access 'x' before initialization",
             "seismic_magnitude": 7,
             "description": "TDZ error with let/const — accessing a variable before it's initialized."},
            {"code": "UnhandledPromiseRejection", "message": "promise rejected with value",
             "seismic_magnitude": 7,
             "description": "A promise was rejected but there was no .catch() handler. "
                           "Silent failure in production."},
        ],
    },
    "Java": {
        "emoji": "☕",
        "seismic_risk": 4,
        "danger_zones": [
            {"zone": "null_pointer_exception", "risk_level": 8,
             "description": "The NullPointerException is Java's most infamous runtime error. "
                            "Despite Optional being available since Java 8, NPEs persist.",
             "common_patterns": ["NullPointerException", "java.lang.NullPointerException",
                                "invoking method on null object", "array access on null"],
             "survival_guide": [
                 "Use Optional<T> for methods that might not return a value",
                 "Use Objects.requireNonNull() to fail fast on null input",
                 "Enable null checks in your IDE (NullAway plugin)",
                 "Use @NonNull and @Nullable annotations",
                 "Prefer empty collections over null — Collections.emptyList()",
             ]},
            {"zone": "checked_exceptions", "risk_level": 6,
             "description": "Java's checked exceptions force error handling at compile time. "
                            "This is unique among modern languages and can lead to boilerplate.",
             "common_patterns": ["unhandled exception type X", "exception X must be caught "
                                "or declared to be thrown", "try without resources"],
             "survival_guide": [
                 "Wrap checked exceptions in unchecked ones (RuntimeException) for re-throwing",
                 "Use try-with-resources for AutoCloseable objects",
                 "Functional interfaces (Function, Supplier) can't throw checked exceptions directly",
                 "Consider a Result/Either type instead of checked exceptions",
             ]},
            {"zone": "generic_type_erasure", "risk_level": 7,
             "description": "Java generics are erased at runtime (type erasure). This means "
                            "no runtime type information, leading to cast errors and heap pollution.",
             "common_patterns": ["java.lang.ClassCastException", "generic array creation",
                                "heap pollution", "unchecked cast warning"],
             "survival_guide": [
                 "Use @SafeVarargs for varargs methods with generics",
                 "Don't create arrays of generic types (new T[])",
                 "Use instanceof with raw types, not with parameterized types",
                 "Class literal (MyClass.class) gives type info at runtime",
             ]},
            {"zone": "concurrency_liveness", "risk_level": 7,
             "description": "Java's threading model is low-level. Deadlock, race conditions, "
                            "and visibility issues are common in multithreaded code.",
             "common_patterns": ["deadlock detected", "race condition", "ConcurrentModificationException",
                                "happens-before violation", "starvation"],
             "survival_guide": [
                 "Use java.util.concurrent collections instead of synchronized ones",
                 "Use ExecutorService rather than raw threads",
                 "Use volatile for simple flag variables",
                 "Use ThreadLocal for thread-specific state",
                 "Prefer higher-level concurrency utilities (CountDownLatch, CyclicBarrier)",
             ]},
            {"zone": "class_loader", "risk_level": 5,
             "description": "Java's class loading system is complex. ClassNotFoundException, "
                            "NoClassDefFoundError, and LinkageError are common in large apps.",
             "common_patterns": ["ClassNotFoundException", "NoClassDefFoundError",
                                "ClassCircularityError", "IncompatibleClassChangeError"],
             "survival_guide": [
                 "ClassNotFoundException: the class wasn't on the classpath at all",
                 "NoClassDefFoundError: the class existed at compile time but not at runtime",
                 "Check for version mismatches between compile-time and runtime libraries",
                 "Use --verbose:class to debug class loading issues",
             ]},
        ],
        "error_stratigraphy": {
            "java1.0": "The beginning. Errors were basic, stack traces were long.",
            "java1.4": "Chained exceptions (Throwable.initCause) added.",
            "java1.5": "Generics (type erasure) introduced — new type-system error patterns.",
            "java1.7": "Try-with-resources (AutoCloseable) improved exception handling.",
            "java1.8": "Lambdas and streams — new errors around type inference and stream operations.",
            "java9": "Module system (JPMS) introduced — a whole new class of module-related errors.",
            "java17": "Sealed classes and pattern matching — new type pattern errors.",
            "java21": "Virtual threads — new concurrency error patterns.",
        },
        "iconic_errors": [
            {"code": "NullPointerException", "message": "null pointer — the eternal enemy",
             "seismic_magnitude": 8,
             "description": "Java's most famous exception. NullPointerException at line X — "
                           "one of the most common errors in all of programming."},
            {"code": "ClassCastException", "message": "cannot cast X to Y — type erasure strikes",
             "seismic_magnitude": 7,
             "description": "At runtime, Java generics are erased, so a ClassCastException "
                           "means you tried to cast something that wasn't the right type."},
            {"code": "ConcurrentModificationException", "message": "modifying collection while iterating",
             "seismic_magnitude": 7,
             "description": "You modified a collection (list/set/map) while iterating over it. "
                           "Use iterator.remove() or copy the collection first."},
        ],
    },
    "C/C++": {
        "emoji": "⚙️",
        "seismic_risk": 9,
        "danger_zones": [
            {"zone": "use_after_free", "risk_level": 10,
             "description": "The most dangerous fault line in C/C++. Memory is freed, then "
                            "accessed — causing crashes, security vulnerabilities, and "
                            "unpredictable behavior.",
             "common_patterns": ["heap corruption", "double free", "use after free",
                                "invalid read/write", "buffer overflow", "stack smashing"],
             "survival_guide": [
                 "Use RAII (Resource Acquisition Is Initialization) — wrap resources in classes",
                 "Use smart pointers (unique_ptr, shared_ptr, weak_ptr)",
                 "Enable AddressSanitizer (-fsanitize=address) in development",
                 "Use Valgrind to detect memory errors in old code",
                 "Never call free/delete on memory you've already freed",
             ]},
            {"zone": "undefined_behavior", "risk_level": 10,
             "description": "C/C++ has many forms of undefined behavior — code that appears "
                            "to work but can break in mysterious ways. This is the language's "
                            "most feared fault line.",
             "common_patterns": ["signed integer overflow", "dereferencing null pointer",
                                "shift by too many bits", "reading uninitialized memory",
                                "strict aliasing violation", "sequence point violation"],
             "survival_guide": [
                 "Use -Wall -Wextra -Werror to catch UB at compile time",
                 "Use -fsanitize=undefined for runtime UB detection",
                 "Never assume signed integers don't overflow",
                 "Don't cast away const and then modify",
                 "Use clang-tidy and static analysis tools",
             ]},
            {"zone": "buffer_overflow", "risk_level": 9,
             "description": "Writing past the end of an array corrupts adjacent memory. "
                            "A classic exploit vector for security vulnerabilities.",
             "common_patterns": ["buffer overflow", "stack buffer overflow", "heap overflow",
                                "off-by-one", "string.h overflow", "format string vulnerability"],
             "survival_guide": [
                 "Use std::vector or std::string instead of raw arrays where possible",
                 "Always bounds-check before array access",
                 "Use safe alternatives: strncpy instead of strcpy, snprintf instead of sprintf",
                 "Enable stack canaries (-fstack-protector)",
                 "Use ASLR (Address Space Layout Randomization) at the OS level",
             ]},
            {"zone": "template_instantiation_errors", "risk_level": 7,
             "description": "C++ template errors produce massive, incomprehensible error messages "
                            "that can scroll for thousands of lines.",
             "common_patterns": ["template instantiation depth", "no matching overload",
                                "SFINAE failure", "dependent base class", "ambiguous overload"],
             "survival_guide": [
                 "Use concepts (C++20) to constrain templates and get cleaner errors",
                 "Use static_assert for better error messages",
                 "Break large templates into smaller pieces",
                 "Use the 'note:' suggestions in error messages",
                 "clang's error messages are often more readable than gcc's",
             ]},
            {"zone": "thread_safety", "risk_level": 8,
             "description": "C++11 threads introduced new concurrency issues. Race conditions, "
                            "deadlocks, and data races are harder to detect than in managed languages.",
             "common_patterns": ["data race", "deadlock", "mutex lock ordering violation",
                                "atomic operations on non-atomic types", "lock_guard scope issue"],
             "survival_guide": [
                 "Use std::atomic for simple shared state",
                 "Use std::lock for multiple mutex acquisition (avoids deadlock)",
                 "Use thread-safe data structures from std::",
                 "Use ThreadSanitizer (-fsanitize=thread) in development",
                 "Prefer std::async and futures over raw threads",
             ]},
        ],
        "error_stratigraphy": {
            "c89/c90": "Ancient era — cryptic diagnostics, no stdbool, implicit int returns. "
                       "Errors were barely helpful.",
            "c99": "Variable-length arrays, inline functions, C99-style comments. "
                   "Compiler diagnostics improved.",
            "c11": "Unicode support, multi-threading, bounds-checking interfaces. "
                   "Static analyzers started emerging.",
            "c++98": "STL era — template errors were enormous and cryptic. "
                     "Error messages could be thousands of lines.",
            "c++11": "Move semantics, smart pointers, nullptr — new class of ownership errors. "
                     "unique_ptr without move = dangling.",
            "c++17": "optional, variant, string_view — new lifetime/error patterns. "
                     "string_view doesn't own its data — easy use-after-free.",
            "c++20": "Concepts gave better template errors. Coroutines introduced "
                     "new resource management challenges.",
            "c++23": "std::expected, static operator(), improvements to coroutines.",
        },
        "iconic_errors": [
            {"code": "SIGSEGV", "message": "segmentation fault — memory access violation",
             "seismic_magnitude": 10,
             "description": "The most feared runtime error — accessing memory you shouldn't. "
                           "Could be null pointer, buffer overflow, or use-after-free."},
            {"code": "heap corruption", "message": "glibc detected ... corrupted double-linked list",
             "seismic_magnitude": 9,
             "description": "You wrote past the end of a heap allocation, corrupting malloc's "
                           "internal bookkeeping. A double-free is a common cause."},
            {"code": "undefined behavior", "message": "this may be used uninitialized",
             "seismic_magnitude": 8,
             "description": "The compiler is warning about undefined behavior — the code might "
                           "appear to work but the result is unpredictable."},
        ],
    },
}


# ── Core faultline functions ──────────────────────────────────────────────────

def rotate_and_update():
    """
    Read language_rotation.json, select the current language,
    advance the index (wrapping to 0 at end), save, and return result.
    """
    config = load_rotation()
    languages = config["languages"]
    idx = config["current_index"]

    lang = languages[idx]
    next_idx = (idx + 1) % len(languages)
    next_lang = languages[next_idx]

    config["current_index"] = next_idx
    config["last_language"] = lang
    config["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation(config)

    return {
        "language": lang,
        "next_language": next_lang,
        "current_index": idx,
        "next_index": next_idx,
        "timestamp": config["updated_at"],
    }


def excavate_faultline(language: Optional[str] = None) -> Dict[str, Any]:
    """
    Main entry point: select language, generate full faultline report.
    """
    if language is None:
        rotation = rotate_and_update()
        lang = rotation["language"]
    else:
        rotation = None
        lang = language
        if lang not in FAULT_ZONES:
            raise ValueError(
                f"'{lang}' is not in this tool's rotation: "
                f"{', '.join(FAULT_ZONES.keys())}"
            )

    data = FAULT_ZONES[lang]
    risk = data["seismic_risk"]
    total_danger = sum(z["risk_level"] for z in data["danger_zones"])
    avg_danger = total_danger / len(data["danger_zones"])

    # Generate aftershock reports for iconic errors
    aftershock_reports = []
    for err in data["iconic_errors"]:
        aftershock_reports.append({
            "code": err["code"],
            "message": err["message"],
            "magnitude": err["seismic_magnitude"],
            "human_readable": _translate_error_to_survival_guide(lang, err, data),
        })

    # Risk heatmap across danger zones
    risk_heatmap = {
        z["zone"]: {
            "level": z["risk_level"],
            "zone_class": _risk_class(z["risk_level"]),
        }
        for z in data["danger_zones"]
    }

    result = {
        "language": lang,
        "emoji": data["emoji"],
        "seismic_risk": risk,
        "risk_class": _risk_class(risk),
        "danger_zones": data["danger_zones"],
        "risk_heatmap": risk_heatmap,
        "error_stratigraphy": data["error_stratigraphy"],
        "iconic_errors": data["iconic_errors"],
        "aftershock_reports": aftershock_reports,
        "fault_zone_summary": {
            "total_zones": len(data["danger_zones"]),
            "highest_risk_zone": max(data["danger_zones"], key=lambda z: z["risk_level"])["zone"],
            "avg_zone_risk": round(avg_danger, 2),
            "total_risk_score": total_danger,
        },
    }

    if rotation:
        result["rotation_info"] = rotation

    return result


def _translate_error_to_survival_guide(
    language: str, error: Dict, data: Dict
) -> str:
    """Translate an iconic error into an actionable aftershock survival guide."""
    zone_map = {z["zone"]: z for z in data["danger_zones"]}

    # Find the most relevant danger zone for this error
    relevant_zone = None
    for zone_name, zone_data in zone_map.items():
        for pattern in zone_data["common_patterns"]:
            if pattern.lower() in error["message"].lower():
                relevant_zone = zone_data
                break
        if relevant_zone:
            break

    if relevant_zone:
        return (
            f"When you encounter '{error['code']}' ({error['message']}), "
            f"check the {relevant_zone['zone']} fault zone. "
            f"Solutions: {'; '.join(relevant_zone['survival_guide'][:2])}"
        )

    return (
        f"Error '{error['code']}' in {language} requires careful debugging. "
        f"Check the language documentation and search for this specific error code."
    )


def _risk_class(level: int) -> str:
    """Map numeric risk level to severity class."""
    if level >= 9:
        return "critical"
    elif level >= 7:
        return "high"
    elif level >= 5:
        return "medium"
    else:
        return "low"


# ── Tests ─────────────────────────────────────────────────────────────────────

def run_tests():
    """Run the test suite."""
    import unittest

    # Save original rotation file for restoration
    with open(ROTATION_FILE, "r") as f:
        original_config = json.load(f)

    class TestRotationLogic(unittest.TestCase):
        def test_rotation_advances(self):
            """Index advances by 1 each call, wraps at end."""
            with open(ROTATION_FILE, "r") as f:
                before = json.load(f)
            idx_before = before["current_index"]

            result = rotate_and_update()

            with open(ROTATION_FILE, "r") as f:
                after = json.load(f)

            if idx_before == 7:  # Last language
                self.assertEqual(after["current_index"], 0, "Should wrap to 0")
            else:
                self.assertEqual(after["current_index"], idx_before + 1, "Should advance by 1")

            self.assertEqual(result["language"], before["languages"][idx_before])
            self.assertIn("timestamp", result)

        def test_full_rotation_cycle(self):
            """All 8 languages are selected across 8 consecutive calls."""
            seen = []
            for _ in range(8):
                result = rotate_and_update()
                seen.append(result["language"])

            self.assertEqual(len(set(seen)), 8, "All 8 languages should appear once")

    class TestFaultlineContent(unittest.TestCase):
        def test_all_languages_have_fault_zones(self):
            for lang in ROTATION_ORDER:
                data = FAULT_ZONES[lang]
                self.assertIn("danger_zones", data)
                self.assertGreaterEqual(len(data["danger_zones"]), 4)
                self.assertIn("emoji", data)

        def test_all_languages_have_stratigraphy(self):
            for lang in ROTATION_ORDER:
                data = FAULT_ZONES[lang]
                self.assertIn("error_stratigraphy", data)
                self.assertGreaterEqual(len(data["error_stratigraphy"]), 4)

        def test_all_languages_have_iconic_errors(self):
            for lang in ROTATION_ORDER:
                data = FAULT_ZONES[lang]
                self.assertIn("iconic_errors", data)
                self.assertGreaterEqual(len(data["iconic_errors"]), 3)
                for err in data["iconic_errors"]:
                    self.assertIn("code", err)
                    self.assertIn("message", err)
                    self.assertIn("seismic_magnitude", err)

        def test_seismic_risk_in_range(self):
            for lang, data in FAULT_ZONES.items():
                self.assertIn("seismic_risk", data)
                self.assertIsInstance(data["seismic_risk"], int)
                self.assertGreaterEqual(data["seismic_risk"], 1)
                self.assertLessEqual(data["seismic_risk"], 10)

        def test_danger_zones_have_survival_guides(self):
            for lang, data in FAULT_ZONES.items():
                for zone in data["danger_zones"]:
                    self.assertIn("survival_guide", zone)
                    self.assertIsInstance(zone["survival_guide"], list)
                    self.assertGreaterEqual(len(zone["survival_guide"]), 2)

    class TestExcavation(unittest.TestCase):
        def test_excavate_auto_selects_language(self):
            result = excavate_faultline()
            self.assertIn("language", result)
            self.assertIn("danger_zones", result)
            self.assertIn("error_stratigraphy", result)
            self.assertIn("iconic_errors", result)
            self.assertIn("rotation_info", result)
            self.assertIn("aftershock_reports", result)
            self.assertIn("fault_zone_summary", result)

        def test_excavate_with_explicit_language(self):
            result = excavate_faultline("Rust")
            self.assertEqual(result["language"], "Rust")
            self.assertNotIn("rotation_info", result)

        def test_invalid_language_raises(self):
            with self.assertRaises(ValueError) as ctx:
                excavate_faultline("Python")
            self.assertIn("not in this tool's rotation", str(ctx.exception))

        def test_aftershock_reports_have_translation(self):
            for lang in ROTATION_ORDER:
                result = excavate_faultline(lang)
                for report in result["aftershock_reports"]:
                    self.assertIn("human_readable", report)
                    self.assertGreater(len(report["human_readable"]), 10)

        def test_risk_heatmap_structure(self):
            for lang in ROTATION_ORDER:
                result = excavate_faultline(lang)
                heatmap = result["risk_heatmap"]
                self.assertGreaterEqual(len(heatmap), 4)
                for zone, info in heatmap.items():
                    self.assertIn("level", info)
                    self.assertIn("zone_class", info)
                    self.assertGreaterEqual(info["level"], 1)
                    self.assertLessEqual(info["level"], 10)

        def test_fault_zone_summary_fields(self):
            for lang in ROTATION_ORDER:
                result = excavate_faultline(lang)
                summary = result["fault_zone_summary"]
                self.assertIn("total_zones", summary)
                self.assertIn("highest_risk_zone", summary)
                self.assertIn("avg_zone_risk", summary)
                self.assertIn("total_risk_score", summary)
                self.assertEqual(summary["total_zones"], len(result["danger_zones"]))

    class TestRiskClassification(unittest.TestCase):
        def test_risk_classes(self):
            self.assertEqual(_risk_class(10), "critical")
            self.assertEqual(_risk_class(9), "critical")
            self.assertEqual(_risk_class(7), "high")
            self.assertEqual(_risk_class(5), "medium")
            self.assertEqual(_risk_class(4), "low")
            self.assertEqual(_risk_class(1), "low")

    # Run tests
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRotationLogic))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestFaultlineContent))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestExcavation))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRiskClassification))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Restore original rotation config
    with open(ROTATION_FILE, "w") as f:
        json.dump(original_config, f, indent=2)

    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()