#! /usr/bin/env python3
"""
🔮 Polyglot Tarot — Core Oracle Engine v1.0
"""

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-tarot"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent
_WORKSPACE_ROOT = _MODULE_DIR.parent
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ─────────────────────────────────────────────────────────────────────────────
# The 22-Card Major Arcana — each card is a programming archetype
# ─────────────────────────────────────────────────────────────────────────────

MAJOR_ARCANA: List[Dict[str, Any]] = [
    {
        "id": 0,
        "name": "The Fool",
        "symbol": "🃏",
        "archetype": "NULL_HANDLING",
        "upright": {
            "fortune": "Beginning. New territory. The compiler says nothing yet.",
            "warning": "Ignoring the null check leads to runtime chaos.",
            "language": {
                "Rust": "Option<T> is the Fool's enlightened path — None is a valid state, not an error.",
                "Go": "The Fool trusts nil. In Go, nil is a valid zero-value for pointers and interfaces — until it isn't.",
                "Swift": "Optional<T> is the Fool dressed as a gentle guardian — nil is possible, handle it.",
                "Kotlin": "The Fool in Kotlin sees ? everywhere — nullable types are first-class citizens.",
                "TypeScript": "The Fool says '?.?' — optional chaining lets you walk through null without looking.",
                "JavaScript": "The Fool dances between undefined and null, unsure which void to trust.",
                "Java": "null is the Fool's abyss. Optional<T> is the enlightenment path.",
                "C/C++": "nullptr is a sober Fool — at least it knows its type. But dereference is still a leap of faith.",
            },
        },
        "reversed": {
            "fortune": "Naivety. Blind faith in type safety without null checks.",
            "warning": "The Fool reversed: assume_non_null leads to segfaults.",
            "language": {
                "Rust": "The Fool reversed: .unwrap() on None — panic instead of grace.",
                "Go": "The Fool reversed: dereferencing nil interface — a hidden trap with no stack trace.",
                "Swift": "The Fool reversed: forced unwrap of nil — crash with style.",
                "Kotlin": "The Fool reversed: !! operator — forcing null into submission backfires.",
                "TypeScript": "The Fool reversed: non-null assertion — the compiler believes you, but reality doesn't.",
                "JavaScript": "The Fool reversed: typeof null === 'object' — even the language is confused.",
                "Java": "The Fool reversed: NPE — the billion-dollar mistake, alive and well.",
                "C/C++": "The Fool reversed: NULL macro expansion — 0 in disguise,UB when dereferenced.",
            },
        },
    },
    {
        "id": 1,
        "name": "The Magician",
        "symbol": "🎩",
        "archetype": "METAPROGRAMMING",
        "upright": {
            "fortune": "Transformation. Abstractions at your command.",
            "warning": "Too much magic makes the codebase unreadable.",
            "language": {
                "Rust": "Macros by example — the Magician conjures code from tokens without evaluating it.",
                "Go": "The Magician is restrained — Go has no generics, no macros, no tricks. Simplicity is the magic.",
                "Swift": "Macros as the Magician's wand — #string interpolation, #available, #selector.",
                "Kotlin": "Reified generics on inline functions — the Magician knows the type at runtime.",
                "TypeScript": "Conditional types and template literals — TypeScript's Magician rewrites your types.",
                "JavaScript": "eval() and Proxy — the dark Magician. Works, but at what cost?",
                "Java": "Reflection as the Magician's mirror — seeing all, even private fields.",
                "C/C++": "Templates are compile-time Magicians — SFINAE, constexpr if, concepts.",
            },
        },
        "reversed": {
            "fortune": "Stunted magic. Metaprogramming that obscures rather than reveals.",
            "warning": "The abstraction layers have consumed the original intent.",
            "language": {
                "Rust": "Macro soup — the Magician reversed, conjuring tokens without clarity.",
                "Go": "Code generation as a crutch — the Magician hides in go generate.",
                "Swift": "Opaque return types that hide too much — the magician's curtain.",
                "Kotlin": "DSL builders with receiver overload — the magic is impressive but the code is unreadable.",
                "TypeScript": "Type-level programming that defeats TypeScript's own inference.",
                "JavaScript": "Minified bundles as black magic — the original spell is lost.",
                "Java": "Reflection used at runtime for what should be compile-time.",
                "C/C++": "Preprocessor macros — the Magician's oldest, darkest spell.",
            },
        },
    },
    {
        "id": 2,
        "name": "The High Priestess",
        "symbol": "🌙",
        "archetype": "IMPLICIT_BEHAVIOR",
        "upright": {
            "fortune": "Intuition. The hidden rules that govern the system.",
            "warning": "What happens in the dark (runtime) matters.",
            "language": {
                "Rust": "The borrow checker is the High Priestess — invisible rules enforce safety.",
                "Go": "Goroutines die silently when main exits — the Priestess cleans up after you.",
                "Swift": "Copy-on-write semantics — the Priestess copies only when necessary.",
                "Kotlin": "Coroutines suspend in silence — the Priestess knows where execution paused.",
                "TypeScript": "Type erasure at runtime — the Priestess knows types but keeps them hidden.",
                "JavaScript": "Hoisting and the temporal dead zone — the Priestess moves things before you look.",
                "Java": "Type erasure — the Priestess removes generics before runtime.",
                "C/C++": "Copy elision and NRVO — the Priestess eliminates copies you never saw.",
            },
        },
        "reversed": {
            "fortune": "Confusion. Implicit behavior that bites back.",
            "warning": "The hidden rules have changed and you didn't notice.",
            "language": {
                "Rust": "Auto-deref and the Deref trait — coercion you didn't ask for.",
                "Go": "nil vs zero-value ambiguity — the Priestess reversed hides the difference.",
                "Swift": "Implicit conversion of String to NSString — two worlds collide.",
                "Kotlin": "Smart cast cancellation after null check — the Priestess reversed.",
                "TypeScript": " widening number types — 3 becomes 3.0 and you didn't ask.",
                "JavaScript": " + '' coercion — the Priestess turns numbers into strings silently.",
                "Java": "Auto-boxing Integer cache — 127 is cached but 128 is not.",
                "C/C++": "Integer promotion rules — the Priestess makes chars into ints unexpectedly.",
            },
        },
    },
    {
        "id": 3,
        "name": "The Empress",
        "symbol": "🌿",
        "archetype": "MEMORY_MANAGEMENT",
        "upright": {
            "fortune": "Abundance. Resources flow freely and are reclaimed naturally.",
            "warning": "Abundance can become waste if not managed.",
            "language": {
                "Rust": "Ownership and the borrow checker — the Empress rules with a firm hand. Memory is yours, then returned.",
                "Go": "The Empress of Go is generous — GC reclaims everything eventually.",
                "Swift": "ARC — Automatic Reference Counting. The Empress counts every retain.",
                "Kotlin": "JVM heap — the Empress tends a garden the GC tends.",
                "TypeScript": "JS heap — managed, invisible, sometimes surprising.",
                "JavaScript": "GC in the background — the Empress reclaims when she chooses.",
                "Java": "HotSpot GC — generational Empress, prioritising young objects.",
                "C/C++": "Manual memory — no Empress here. You are your own caretaker.",
            },
        },
        "reversed": {
            "fortune": "Exhaustion. Memory leaks, fragmentation, GC pauses.",
            "warning": "The Empress is overwhelmed — resources are not being reclaimed.",
            "language": {
                "Rust": "Rc<T> cycles — the Empress can't break them, memory leaks by design.",
                "Go": "GC pauses — the Empress sometimes takes a breath and stops the world.",
                "Swift": "Retain cycles with closures — the Empress counts endlessly.",
                "Kotlin": "Old-generation retention — the Empress holds onto objects too long.",
                "TypeScript": "Closures holding references — the Empress collects what you forgot.",
                "JavaScript": "Global object references — the Empress never lets go.",
                "Java": "PermGen / Metaspace — the Empress's long-term memory can fill.",
                "C/C++": "Double-free, use-after-free — the Empress reversed, chaos ensues.",
            },
        },
    },
    {
        "id": 4,
        "name": "The Emperor",
        "symbol": "⚔️",
        "archetype": "STRICT_TYPING",
        "upright": {
            "fortune": "Structure. Order imposed through types and contracts.",
            "warning": "Rigidity can crush flexibility and creativity.",
            "language": {
                "Rust": "The Emperor of Rust — types are laws. The compiler is the enforcement arm.",
                "Go": "The Emperor is lenient — structs are data, not classes. No inheritance.",
                "Swift": "Protocols over inheritance — the Emperor favours composition.",
                "Kotlin": "Classes with smart defaults — the Emperor rules with nullable grace.",
                "TypeScript": "Structural types — the Emperor cares what you do, not what you claim.",
                "JavaScript": "The Emperor is absent — duck typing reigns, anything goes.",
                "Java": "Nominal types and checked exceptions — the Emperor's laws are many.",
                "C/C++": "Static types and UB — the Emperor enforces some laws but not all.",
            },
        },
        "reversed": {
            "fortune": "Tyranny. Type systems that fight the programmer at every turn.",
            "warning": "The Emperor reversed: types become cages.",
            "language": {
                "Rust": "The borrow checker as tyrant — complex lifetimes defeat even the wise.",
                "Go": "The Emperor's limits: no generics, no union types, workarounds everywhere.",
                "Swift": "Protocol existentials — the Emperor reverses his decision at runtime.",
                "Kotlin": "Sealed classes and exhaustive when — the Emperor demands completeness.",
                "TypeScript": "Strict mode flags fighting legacy JS patterns.",
                "JavaScript": "TypeScript's strict mode — the Emperor finally arrives, but legacy code suffers.",
                "Java": "Checked exceptions — the Emperor makes callers responsible for everything.",
                "C/C++": "The Emperor's loopholes: const_cast, reinterpret_cast, void*.",
            },
        },
    },
    {
        "id": 5,
        "name": "The Hierophant",
        "symbol": "📜",
        "archetype": "STANDARD_LIBRARY",
        "upright": {
            "fortune": "Tradition. The canonical way to do things is proven and stable.",
            "warning": "The standard path is safe but may not be optimal.",
            "language": {
                "Rust": "The Hierophant speaks through std — batteries included, memory-safe by default.",
                "Go": "The stdlib is the Hierophant's gospel — fmt, net/http, encoding/json.",
                "Swift": "Foundation and the Hierophant's word — cross-platform consistency.",
                "Kotlin": "The Hierophant in Kotlin's stdlib — collections, coroutines, Kotlin-specific.",
                "TypeScript": "The DOM types and the Hierophant — @types packages fill the gaps.",
                "JavaScript": "The globalThis is the Hierophant's temple — built-ins everywhere.",
                "Java": "java.lang, java.util, java.io — the Hierophant's complete scripture.",
                "C/C++": "The STL — std::vector, std::map, algorithms. The Hierophant's modern form.",
            },
        },
        "reversed": {
            "fortune": "Heresy. The standard library is inadequate or outdated.",
            "warning": "Third-party libraries may be necessary where stdlib fails.",
            "language": {
                "Rust": "The Hierophant reversed: std is small. You need crates.io for much.",
                "Go": "The stdlib is conservative — some packages feel dated.",
                "Swift": "Foundation bridging inconsistencies — the Hierophant speaks two languages.",
                "Kotlin": "The Java interop gap — the Hierophant sometimes points to java.* instead.",
                "TypeScript": "lib.dom.d.ts drift — the Hierophant's scripture lags browser reality.",
                "JavaScript": "The standard library is famously small — Lodash is almost mandatory.",
                "Java": "Old APIs linger — the Hierophant doesn't retire old gods.",
                "C/C++": "The C++ standard library is incomplete — boost fills the gaps.",
            },
        },
    },
    {
        "id": 6,
        "name": "The Lovers",
        "symbol": "💘",
        "archetype": "INTEROPERABILITY",
        "upright": {
            "fortune": "Union. Two systems in harmony, bridging worlds.",
            "warning": "Love across boundaries requires translation.",
            "language": {
                "Rust": "FFI and the love for C — Rust speaks to C without translation needed.",
                "Go": "cgo — Go loves C, but the union is awkward and slow across the boundary.",
                "Swift": "Obj-C and Swift — two lovers reunited in Apple's ecosystem.",
                "Kotlin": "Kotlin/JVM and interop — loves Java deeply, can also speak JS via Kotlin/JS.",
                "TypeScript": "TypeScript and JavaScript — they ARE the same language, a perfect union.",
                "JavaScript": "WebAssembly bindings — JS's new lover from the native world.",
                "Java": "JNI — Java loves C/C++, but the union requires ceremony and ritual.",
                "C/C++": "C ABI as the universal lover — most languages can speak to C.",
            },
        },
        "reversed": {
            "fortune": "Mismatch. The boundary between systems causes friction.",
            "warning": "Data format mismatches, ABI incompatibilities, silent corruptions.",
            "language": {
                "Rust": "Unsafe {} at the boundary — the Lovers reversed, the unsafe union.",
                "Go": "cgo overhead — every call across the boundary has a cost.",
                "Swift": "ABI instability between versions — the Lovers forget each other.",
                "Kotlin": "Kotlin/JS type erasure on the JS side — the Lovers speak different dialects.",
                "TypeScript": "TypeScript + JS interoperability — types vanish at runtime.",
                "JavaScript": "JSON as the translator — lossy, but the universal lover's language.",
                "Java": "JNI memory leaks — the Lovers reversed, resources not returned.",
                "C/C++": "ABI compatibility across compilers — the Lovers can no longer understand each other.",
            },
        },
    },
    {
        "id": 7,
        "name": "The Chariot",
        "symbol": "🏎️",
        "archetype": "CONCURRENCY",
        "upright": {
            "fortune": "Victory through control. Parallel forces harnessed toward a goal.",
            "warning": "Control requires discipline — losing the reins means disaster.",
            "language": {
                "Rust": "Fearless concurrency via Send/Sync — the Chariot is armour-plated.",
                "Go": "Goroutines and channels — the Chariot rides with CSP, not threads.",
                "Swift": "async/await and actors — the Chariot with Swift 6's data-race safety.",
                "Kotlin": "Coroutines and Flow — structured concurrency, the disciplined Chariot.",
                "TypeScript": "async/await with Promise.all — the Chariot advances on one lane.",
                "JavaScript": "Event loop — single-threaded Chariot, but promises queue efficiently.",
                "Java": "Threads and virtual threads — the Chariot with many horses, old and new.",
                "C/C++": "std::thread and atomics — the Chariot with no seatbelt.",
            },
        },
        "reversed": {
            "fortune": "Loss of control. Data races, deadlocks, and chaos on the road.",
            "warning": "The Chariot has crashed — threads competing for the same resource.",
            "language": {
                "Rust": "Send/Sync violations caught at compile time — the Chariot almost never crashes.",
                "Go": "Goroutine leaks and deadlock — the Chariot reversed without select or context.",
                "Swift": "Actor re-entrancy surprises — the Chariot reversed when crossing actor boundaries.",
                "Kotlin": "Coroutine cancellation without cooperative check — the Chariot ignores the stop signal.",
                "TypeScript": "Unhandled promise rejections — the Chariot carries a silent bomb.",
                "JavaScript": "Event loop blocking — the Chariot stalls on synchronous heavy work.",
                "Java": "Thread pool starvation — too many goroutines (virtual threads) converge.",
                "C/C++": "Data races and UB — the Chariot reversed: no one is driving.",
            },
        },
    },
    {
        "id": 8,
        "name": "Strength",
        "symbol": "🦁",
        "archetype": "ERROR_HANDLING",
        "upright": {
            "fortune": "Courage. Facing failure directly with type-safe mechanisms.",
            "warning": "Strength without wisdom is brute force, not control.",
            "language": {
                "Rust": "Result<T, E> — Strength faces errors as first-class values. No exceptions.",
                "Go": "error interface — Strength returns errors, nil means success.",
                "Swift": "throws and do/catch — Strength names errors and forces handling.",
                "Kotlin": "Result<T> and runCatching — Kotlin's Strength is flexible about errors.",
                "TypeScript": "throw + try/catch — Strength throws values, TypeScript erases types.",
                "JavaScript": "throw as control flow — JS's Strength can become weakness easily.",
                "Java": "Checked + unchecked exceptions — the most rigorous Strength in the land.",
                "C/C++": "Return codes and errno — Strength is manual, no compiler assistance.",
            },
        },
        "reversed": {
            "fortune": "Weakness. Errors swallowed, ignored, or mishandled.",
            "warning": "Strength reversed: silent failures create invisible damage.",
            "language": {
                "Rust": ".unwrap() in production — Strength reversed: panic instead of graceful handling.",
                "Go": "Ignoring returned errors — _ = err — Strength left on the floor.",
                "Swift": "try? swallowing errors into optionals — Strength converted to silence.",
                "Kotlin": "throw in Kotlin — Strength outside its usual domain.",
                "TypeScript": "catch(e) {} — Strength reversed: the error disappears.",
                "JavaScript": "Error objects discarded — the weakest form of error handling.",
                "Java": "Empty catch blocks — the Emperor's Strength rendered void.",
                "C/C++": "Return code ignored — the weakest link in the chain.",
            },
        },
    },
    {
        "id": 9,
        "name": "The Hermit",
        "symbol": "🔦",
        "archetype": "INFORMATION_HIDING",
        "upright": {
            "fortune": "Wisdom through solitude. Internal details stay hidden.",
            "warning": "Too much isolation makes the Hermit unapproachable.",
            "language": {
                "Rust": "Privacy at module level — the Hermit reveals only the public API.",
                "Go": "Exported vs unexported — the Hermit uses capital letters to choose.",
                "Swift": "Access control: private, fileprivate, internal, public, open.",
                "Kotlin": "visibility modifiers — the Hermit controls visibility precisely.",
                "TypeScript": "export and internal — the Hermit decides what TypeScript exposes.",
                "JavaScript": "Closures and IIFEs — the Hermit hides state in function scope.",
                "Java": "private, package-private, protected, public — four levels of Hermit.",
                "C/C++": "Opaque pointers and pImpl — the Hermit hides implementation details.",
            },
        },
        "reversed": {
            "fortune": "Exposure. The Hermit has revealed too much.",
            "warning": "Implementation details leak, breaking encapsulation.",
            "language": {
                "Rust": "pub(crate) leaking — the Hermit opens doors to the whole crate.",
                "Go": "Exported fields in structs — the Hermit left a gate open.",
                "Swift": "Internal being the default — the Hermit is more open than expected.",
                "Kotlin": "data class exposing all fields — the Hermit has no secrets.",
                "TypeScript": "Everything is exposed by default — the Hermit forgot to hide.",
                "JavaScript": "Prototype chain exposure — the Hermit cannot truly hide.",
                "Java": "Reflection breaking privacy — the Hermit can be forced to speak.",
                "C/C++": "Header files exposing everything — the Hermit's walls have windows.",
            },
        },
    },
    {
        "id": 10,
        "name": "Wheel of Fortune",
        "symbol": "🎡",
        "archetype": "RUNTIME_DISPATCH",
        "upright": {
            "fortune": "Fate. Dynamic behaviour resolved at the moment of execution.",
            "warning": "What the wheel decides cannot be known until runtime.",
            "language": {
                "Rust": "Dynamic dispatch via dyn Trait — the wheel spins at runtime for erased types.",
                "Go": "Interface method resolution — the wheel decides which implementation at runtime.",
                "Swift": "Witness tables and vtables — the wheel spins at runtime for protocol dispatch.",
                "Kotlin": "Virtual method dispatch on open classes — the wheel turns per instance.",
                "TypeScript": "typeof and instanceof at runtime — the wheel decides by checking types.",
                "JavaScript": "typeof null === 'object', the wheel decides 10 kinds of things.",
                "Java": "Virtual machine dispatch — the JVM wheel spins for every method call.",
                "C/C++": "Virtual functions and vtables — the wheel of polymorphism at runtime.",
            },
        },
        "reversed": {
            "fortune": "Bad luck. The wheel landed on UB — undefined behaviour.",
            "warning": "Runtime dispatch that went wrong, or type information lost.",
            "language": {
                "Rust": "dyn Trait object with wrong vtable — the wheel falls off.",
                "Go": "nil interface with value — the wheel spins into nil pointer panic.",
                "Swift": "objc_msgSend on deallocated object — the wheel does not stop.",
                "Kotlin": "Reified type erasure — the wheel forgot which type it held.",
                "TypeScript": "Type narrowing lost on assignment — the wheel reverses.",
                "JavaScript": "Instanceof failing across frames — the wheel has no memory.",
                "Java": "ClassCastException — the wheel landed on the wrong type.",
                "C/C++": "Virtual call on deleted object — UB, the wheel crashes completely.",
            },
        },
    },
    {
        "id": 11,
        "name": "Justice",
        "symbol": "⚖️",
        "archetype": "CONST_CORRECTNESS",
        "upright": {
            "fortune": "Balance. What is immutable is protected. What is mutable is intentional.",
            "warning": "Justice demands consistency — mutability must be deliberate.",
            "language": {
                "Rust": "const and mut — Justice demands you declare intent. Default is immutability.",
                "Go": "const for literals, immutability via absence — Justice is gentle here.",
                "Swift": "let vs var — Justice distinguishes the constant from the variable.",
                "Kotlin": "val vs var — Justice applies to references. Collections can still mutate.",
                "TypeScript": "const assertions — Justice locks literal types. Objects remain mutable.",
                "JavaScript": "const objects can be mutated — Justice is incomplete.",
                "Java": "final on references — Justice prevents reassignment, not mutation.",
                "C/C++": "const and constexpr — Justice at compile time and runtime.",
            },
        },
        "reversed": {
            "fortune": "Injustice. The balance is broken — mutable state spreads unchecked.",
            "warning": "State changed when it should not have been.",
            "language": {
                "Rust": "Interior mutability (Cell, RefCell) — Justice reversed: mutation through shared references.",
                "Go": "Slices sharing backing arrays — Justice misses the mutation.",
                "Swift": "inout parameters — Justice passes through the side door.",
                "Kotlin": "Mutable collections in val containers — Justice doesn't deep-freeze.",
                "TypeScript": "Object.assign and spread — Justice is not deep.",
                "JavaScript": "Mutation of const objects — the scales are broken.",
                "Java": "Collections.unmodifiableList() with a cast — Justice is pretended.",
                "C/C++": "const_cast — Justice reversed: the compiler is bypassed.",
            },
        },
    },
    {
        "id": 12,
        "name": "The Hanged Man",
        "symbol": "🌀",
        "archetype": "LAZY_EVALUATION",
        "upright": {
            "fortune": "Surrender. Defer computation until the result is truly needed.",
            "warning": "Suspension can become avoidance — the result may never come.",
            "language": {
                "Rust": "Iterators and lazy .iter() — the Hanged Man suspends evaluation forever.",
                "Go": "Channels — the Hanged Man blocks until the value arrives.",
                "Swift": "lazy properties — evaluation deferred until first access.",
                "Kotlin": "Sequences and lazy sequences — the Hanged Man defers computation.",
                "TypeScript": "Generator functions (function*) — the Hanged Man yields and waits.",
                "JavaScript": "Closures and thunks — the Hanged Man defers by wrapping.",
                "Java": "Supplier<T> and lazy initialization — the Hanged Man suspends intent.",
                "C/C++": "lambda captures — the Hanged Man defers by closing over scope.",
            },
        },
        "reversed": {
            "fortune": "Forced resolution. Evaluation forced before it was ready.",
            "warning": "Eager evaluation breaks the contract of deferral.",
            "language": {
                "Rust": "collect() forced too early — the Hanged Man reversed: memory allocated before needed.",
                "Go": "Buffered channel capacity confusion — the Hanged Man reversed: blocks or drops.",
                "Swift": "force unwrap of lazy — the Hanged Man is forced to speak early.",
                "Kotlin": "Eager collection of sequences — the Hanged Man reversed: no deferral.",
                "TypeScript": "await in top-level — the Hanged Man cannot suspend at the top level.",
                "JavaScript": "IIFEs forcing thunks — the Hanged Man reversed: immediate evaluation.",
                "Java": "Eager static initializers — the Hanged Man has no patience.",
                "C/C++": "Eager template instantiation — the Hanged Man reversed: all choices made at compile.",
            },
        },
    },
    {
        "id": 13,
        "name": "Death",
        "symbol": "💀",
        "archetype": "RESOURCE_CLEANUP",
        "upright": {
            "fortune": "Transformation. Resources returned, connections closed, memory freed.",
            "warning": "Death must come — deferred cleanup leads to zombie resources.",
            "language": {
                "Rust": "Drop trait — deterministic resource destruction. The Drop order is the Death process.",
                "Go": "defer — Death is the last statement executed before the function returns.",
                "Swift": "deinit — Death in class instances. ARC handles the rest.",
                "Kotlin": "use {} extension on Closeable — Death with a scope guard.",
                "TypeScript": "finally blocks — Death runs cleanup even after exceptions.",
                "JavaScript": "try/finally and WeakRef — Death can be deferred but not avoided.",
                "Java": "try-with-resources — Death is automatic and certain.",
                "C/C++": "RAII — destructors as Death's angels. Deterministic and reliable.",
            },
        },
        "reversed": {
            "fortune": "Zombies. Resources that refuse to die, leaks that persist.",
            "warning": "Death reversed: cleanup code that never runs, finalizers that hang.",
            "language": {
                "Rust": "Memory leaks via Rc cycles or mem::forget — Death reversed.",
                "Go": "Goroutines without done channels — Death cannot find them.",
                "Swift": "Retain cycles in closures — Death waits forever.",
                "Kotlin": "Closeable not used in use {} — Death is skipped.",
                "TypeScript": "Unhandled promise rejections — Death silently leaves the scene.",
                "JavaScript": "Event listeners not removed — Death accumulates in the DOM.",
                "Java": "Finalizers that are never called — Death delayed indefinitely.",
                "C/C++": "Missing virtual destructor — Death incomplete, UB on polymorphic delete.",
            },
        },
    },
    {
        "id": 14,
        "name": "Temperance",
        "symbol": "🧪",
        "archetype": "TYPE_COERCION",
        "upright": {
            "fortune": "Balance through blending. Values transform between types safely.",
            "warning": "Too much coercion blurs the boundary between types.",
            "language": {
                "Rust": "From/Into/TryFrom/TryInto — Temperance coordinates between types systematically.",
                "Go": "Implicit numeric conversions absent — Temperance is strict. Explicit casting required.",
                "Swift": "Numeric protocol conversions — Temperance converts Int to Double with .init().",
                "Kotlin": "Smart casts after type checks — Temperance narrows types automatically.",
                "TypeScript": "Widening and literal type widening — Temperance blends silently.",
                "JavaScript": "Type coercion is Temperance at its most chaotic — + '', ==, Number().",
                "Java": "Boxing/unboxing and widening — Temperance blends primitives and objects.",
                "C/C++": "Implicit conversions and user-defined conversions — Temperance can be hidden.",
            },
        },
        "reversed": {
            "fortune": "Confusion. Implicit coercions that corrupt data silently.",
            "warning": "Temperance reversed: the blend has no measure — precision is lost.",
            "language": {
                "Rust": " Deref coercion — Temperance crosses type boundaries invisibly.",
                "Go": "nil interface comparison — Temperance reversed: equal? no? confusing.",
                "Swift": "Any and AnyObject — Temperance loses all type information.",
                "Kotlin": "Generics with star projection — Temperance knows nothing.",
                "TypeScript": "Structural type compatibility — Temperance reverses when excess properties appear.",
                "JavaScript": "'5' + 3 = '53' — Temperance in chaos: number becomes string.",
                "Java": "Boxing comparisons: new Integer(127) == new Integer(127) — broken Temperance.",
                "C/C++": "Integer promotions and floating point conversions — Temperance can be lossy.",
            },
        },
    },
    {
        "id": 15,
        "name": "The Devil",
        "symbol": "😈",
        "archetype": "UNSAFE_OPERATIONS",
        "upright": {
            "fortune": "Power. Breaking the rules when necessary and knowing the cost.",
            "warning": "The Devil's power always has a price. Use sparingly.",
            "language": {
                "Rust": "unsafe {} — the Devil's pact: raw pointers, volatile, transmute, inline assembly.",
                "Go": "unsafe.Pointer — the Devil in Go's clothing, bypassing the type system.",
                "Swift": "unsafeBitCast and unmanaged — the Devil knows memory directly.",
                "Kotlin": "Intrinsics and Kotlin/Native unsafe — the Devil calls native code.",
                "TypeScript": "eval() and the Function constructor — the Devil speaks JavaScript.",
                "JavaScript": "with statement — the Devil's own syntax for scope manipulation.",
                "Java": "sun.misc.Unsafe — the Devil's private API in Java's basement.",
                "C/C++": "Everything is unsafe — the Devil IS C/C++. Raw pointers, no bounds.",
            },
        },
        "reversed": {
            "fortune": "Temptation misused. Unsafe operations where safe alternatives exist.",
            "warning": "The Devil reversed: unnecessary danger invited unnecessarily.",
            "language": {
                "Rust": "unsafe without justification — the Devil is loose for no reason.",
                "Go": "unsafe used for performance where it wasn't needed.",
                "Swift": "UnsafeMutablePointer in hot paths — the Devil invited where not needed.",
                "Kotlin": "Kotlin/Native memory management bypassing safety.",
                "TypeScript": "eval() for trivial parsing — the Devil for a one-liner.",
                "JavaScript": "Function() constructor and new Function() — the Devil on the loose.",
                "Java": "Reflection used to bypass visibility — the Devil breaks the contract.",
                "C/C++": "Buffer overflows, format string attacks — the Devil's playground.",
            },
        },
    },
    {
        "id": 16,
        "name": "The Tower",
        "symbol": "🗼",
        "archetype": "BREAKING_CHANGE",
        "upright": {
            "fortune": "Destruction of the old. Necessary collapse to rebuild stronger.",
            "warning": "The Tower falls — old assumptions are proven wrong at speed.",
            "language": {
                "Rust": "Edition migrations and async traits — the Tower sometimes must fall.",
                "Go": "Go 1 compatibility promise — the Tower rarely falls. But generics were a quake.",
                "Swift": "ABI stability arrival — the Tower was built in layers over years.",
                "Kotlin": "Kotlin 2.0 — the Tower of Kotlin/JS collapsed into IR.",
                "TypeScript": "Major version jumps — the Tower falls when old syntax is deprecated.",
                "JavaScript": "ES6+ migration — the Tower of callbacks collapsed, replaced by promises/async.",
                "Java": "Java 8 streams breaking Java 7 code — a controlled Tower collapse.",
                "C/C++": "C++11, C++20 — the Tower keeps being rebuilt, never quite finished.",
            },
        },
        "reversed": {
            "fortune": "Collapse avoided. The warning signs were ignored.",
            "warning": "The Tower falls anyway — deferred breaking changes hit harder.",
            "language": {
                "Rust": "Compiler breaking changes across editions — the deferred Tower.",
                "Go": "Go 2 proposals hanging — the Tower that hasn't fallen yet.",
                "Swift": "Swift 6 concurrency model — the delayed Tower collapse.",
                "Kotlin": "Deprecation without removal — the Tower stands despite cracks.",
                "TypeScript": "tsconfig strict flag deferred — the Tower accumulates risk.",
                "JavaScript": "Old code still on ES5 — the Tower still standing by inertia.",
                "Java": "Deprecated APIs never removed — the Tower accumulates scaffolding.",
                "C/C++": "Legacy codebases on C89 — the Tower has no renovation plan.",
            },
        },
    },
    {
        "id": 17,
        "name": "The Star",
        "symbol": "⭐",
        "archetype": "IDEA_EXPRESSION",
        "upright": {
            "fortune": "Inspiration. The language expresses ideas with clarity and elegance.",
            "warning": "The Star can be distant — beauty without practicality.",
            "language": {
                "Rust": "Pattern matching and Result — the Star shines in error-rich code.",
                "Go": "goroutines as the Star — concurrency expressed simply and beautifully.",
                "Swift": "Result builders and trailing closures — the Star writes like prose.",
                "Kotlin": "Extension functions and DSL builders — the Star decorates existing types.",
                "TypeScript": "Mapped types and template literal types — the Star at the type level.",
                "JavaScript": "Arrow functions and destructuring — the Star simplified JS.",
                "Java": "Streams and lambdas (Java 8) — the Star arrived late but brightly.",
                "C/C++": "Range-based for and auto — the Star in C++20 ranges.",
            },
        },
        "reversed": {
            "fortune": "Burnout. The language's expressiveness is exhausted.",
            "warning": "The Star reversed: verbose workarounds where elegance should exist.",
            "language": {
                "Rust": "Lifetime annotations in complex cases — the Star is dimmed.",
                "Go": "Error handling repetition: if err != nil — the Star is obscured.",
                "Swift": "Combine framework verbosity — the Star needs too much ceremony.",
                "Kotlin": "Complex generic bounds — the Star's light bends through complexity.",
                "TypeScript": "Complex conditional types — the Star is only visible to the initiated.",
                "JavaScript": "Callback hell and async waterfall — the Star was missing.",
                "Java": "Checked exception propagation — the Star struggles through the call stack.",
                "C/C++": "Template error messages — the Star's beauty is buried in noise.",
            },
        },
    },
    {
        "id": 18,
        "name": "The Moon",
        "symbol": "🌙",
        "archetype": "AMBIGUITY",
        "upright": {
            "fortune": "Mystery. Things that work but cannot be fully explained.",
            "warning": "The Moon hides as much as it reveals.",
            "language": {
                "Rust": "Polonius borrow checker — the Moon illuminates complex aliasing.",
                "Go": "Goroutine scheduler mysteries — the Moon governs the hidden M:N threading.",
                "Swift": "SIL and MIR — the Moon shows different views at each compilation stage.",
                "Kotlin": "Inline function reification — the Moon makes types real at runtime.",
                "TypeScript": "Structural typing with excess property checks — the Moon's inconsistency.",
                "JavaScript": "this binding — the Moon moves depending on call-site context.",
                "Java": "JIT compilation — the Moon optimises invisibly at runtime.",
                "C/C++": "Compiler optimisations and UB — the Moon reveals different behaviour.",
            },
        },
        "reversed": {
            "fortune": "Delirium. Behaviour that makes no sense and has no explanation.",
            "warning": "The Moon reversed: something is wrong but you cannot see it.",
            "language": {
                "Rust": "Miri catching UB in unsafe — the Moon reversed is caught.",
                "Go": "Data races — the Moon reversed: two goroutines see different memory.",
                "Swift": "Unspecified evaluation order in SwiftUI — the Moon reversed.",
                "Kotlin": "Coroutines and structured concurrency violations — the Moon sets wrong.",
                "TypeScript": "Type inference failing silently — the Moon reversed retreats.",
                "JavaScript": "NaN !== NaN — the Moon is fully reversed: a value is not itself.",
                "Java": "Escape analysis decisions — the Moon decides stack vs heap invisibly.",
                "C/C++": "Undefined behaviour — the Moon reversed is pure chaos.",
            },
        },
    },
    {
        "id": 19,
        "name": "The Sun",
        "symbol": "☀️",
        "archetype": "OPTIMISATION",
        "upright": {
            "fortune": "Radiance. Code that runs fast and clear, optimised by the compiler.",
            "warning": "The Sun can bleach colour — over-optimisation loses readability.",
            "language": {
                "Rust": "LLVM's optimiser + monomorphisation — the Sun illuminates with zero cost.",
                "Go": "Compiler is simple, not aggressive — the Sun is warm but not blinding.",
                "Swift": "Whole-module optimisation — the Sun sees across all files.",
                "Kotlin": "JIT warm-up and inline functions — the Sun grows brighter with use.",
                "TypeScript": "V8's JIT and Crankshaft/Turbofan — the Sun optimises at runtime.",
                "JavaScript": "JIT compilation in V8 — the Sun runs faster as it learns.",
                "Java": "HotSpot JIT — the Sun identifies hot paths and accelerates them.",
                "C/C++": "Aggressive optimisations (-O3, LTO, IPO) — the Sun at full power.",
            },
        },
        "reversed": {
            "fortune": "Blindness. Premature optimisation or compiler tricks backfire.",
            "warning": "The Sun reversed: optimisation at the cost of correctness.",
            "language": {
                "Rust": "Monomorphisation bloat — the Sun produces too many copies.",
                "Go": "escape analysis surprises — the Sun puts things on the heap unexpectedly.",
                "Swift": "Whole-module optimisation time — the Sun takes too long to rise.",
                "Kotlin": "Inline at call site — the Sun reverses: bytecode grows, not shrinks.",
                "TypeScript": "Minifier mangling — the Sun's names are lost, debugging is darkness.",
                "JavaScript": "V8 deoptimisation — the Sun reversed: optimised code becomes slow.",
                "Java": "Escape analysis failures — the Sun allocates on the heap instead of stack.",
                "C/C++": "UB under optimisation — the Sun reveals the code was wrong all along.",
            },
        },
    },
    {
        "id": 20,
        "name": "Judgement",
        "symbol": "🎺",
        "archetype": "CODE_GENERATION",
        "upright": {
            "fortune": "Resurrection. Code that generates more code, patterns that replicate.",
            "warning": "Judgement is final — the generated code is the final word.",
            "language": {
                "Rust": "proc_macro, derive macros — Judgement speaks through annotations.",
                "Go": "go generate and stringer — Judgement produces boilerplate automatically.",
                "Swift": "@resultBuilder, property wrappers — Judgement builds from components.",
                "Kotlin": "kapt, KSP — Judgement generates code before compilation.",
                "TypeScript": "tsc --generateDeclarations and plugins — Judgement from types.",
                "JavaScript": "Babel and transpilation — Judgement translates the old into the new.",
                "Java": "Annotation processors and Lombok — Judgement fills in the boilerplate.",
                "C/C++": "Templates and constexpr — Judgement generates at compile time.",
            },
        },
        "reversed": {
            "fortune": "Misjudgement. Generated code that diverges from intent.",
            "warning": "The generated code was wrong and propagated everywhere.",
            "language": {
                "Rust": "Derive macros generating wrong impls — Judgement reversed: the compiler agrees with wrong code.",
                "Go": "stringer breaks on new constants — Judgement missed the update.",
                "Swift": "@auto_closure conflicts with newer Swift — Judgement reversed.",
                "Kotlin": "KAPT-generated code out of sync — Judgement is confused.",
                "TypeScript": "Declaration emit failing — Judgement cannot write what it promised.",
                "JavaScript": "Babel transpiling modern features to wrong ES5 output.",
                "Java": "Lombok's AST manipulation — Judgement is invisible and breaks tools.",
                "C/C++": "Template instantiation explosion — Judgement generates too much.",
            },
        },
    },
    {
        "id": 21,
        "name": "The World",
        "symbol": "🌍",
        "archetype": "ECOSYSTEM_COMPLETENESS",
        "upright": {
            "fortune": "Completion. A rich ecosystem where all needs are served.",
            "warning": "The World can be inward-looking — the ecosystem is vast but insular.",
            "language": {
                "Rust": "crates.io — a curated World of 100k+ crates, Rust's global village.",
                "Go": "The Go module mirror — the World of Go packages is simpler but growing.",
                "Swift": "Swift Package Manager + Apple's ecosystem — the World is well-integrated.",
                "Kotlin": "Maven Central + jcenter legacy — the World of JVM libraries.",
                "TypeScript": "npm — the largest package ecosystem in the World.",
                "JavaScript": "npm/yarn/pnpm — JavaScript's World is the largest ecosystem on Earth.",
                "Java": "Maven Central and Gradle — the World of enterprise Java is mature.",
                "C/C++": "Conan, vcpkg — the World of C++ has many package managers, none dominant.",
            },
        },
        "reversed": {
            "fortune": "Isolation. The ecosystem is inadequate or fractured.",
            "warning": "The World reversed: packages exist but nothing works together.",
            "language": {
                "Rust": "Crate version conflicts — the World has many villages with different dialects.",
                "Go": "Go's module proxy politics — the World has governance issues.",
                "Swift": "SPM and CocoaPods tension — two Worlds on the same Apple platform.",
                "Kotlin": "Kotlin/JS and Kotlin/Native ecosystems are smaller — the World is incomplete.",
                "TypeScript": "@types DefinitelyTyped lag — the TypeScript World depends on a volunteer library.",
                "JavaScript": "npm dependency hell — the World is too large to navigate safely.",
                "Java": "JAR hell and classpath ordering — the old World of Java.",
                "C/C++": "ABI incompatibilities across compilers — there is no single World.",
            },
        },
    },
]

# Reading archetypes — the types of questions the Oracle can answer
READING_ARCHETYPES: List[Dict[str, Any]] = [
    {"id": "null_handling", "name": "The Void", "emoji": "🌑", "question": "What does {lang} say about absence?"},
    {"id": "error_recovery", "name": "The Chasm", "emoji": "⚡", "question": "How does {lang} face failure?"},
    {"id": "concurrency", "name": "The River", "emoji": "🧵", "question": "How does {lang} handle parallel waters?"},
    {"id": "memory", "name": "The Garden", "emoji": "🌿", "question": "What grows in {lang}'s memory garden?"},
    {"id": "typing", "name": "The Mirror", "emoji": "🪞", "question": "What does {lang}'s type system reveal?"},
    {"id": "metaprogramming", "name": "The Mirror Gate", "emoji": "🌀", "question": "How does {lang} rewrite itself?"},
    {"id": "interop", "name": "The Bridge", "emoji": "🌉", "question": "What boundaries does {lang} cross?"},
    {"id": "design", "name": "The Compass", "emoji": "🧭", "question": "What path does {lang} chart for design?"},
]

SPREAD_POSITIONS = [
    ("past", "The Foundation"),
    ("present", "The Current"),
    ("challenge", "The Obstacle"),
    ("root", "The Root Cause"),
    ("goal", "The Aspiration"),
    ("outcome", "The Verdict"),
]


# ─────────────────────────────────────────────────────────────────────────────
# Rotation helpers
# ─────────────────────────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def get_current_language() -> str:
    data = load_rotation()
    idx = data.get("current_index", 0)
    return data["languages"][idx % len(data["languages"])]


def advance_rotation() -> None:
    data = load_rotation()
    old_idx = data["current_index"]
    current = data["languages"][old_idx]
    data["current_index"] = (old_idx + 1) % len(data["languages"])
    data["last_language"] = current
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation(data)


# ─────────────────────────────────────────────────────────────────────────────
# Deterministic card drawing
# ─────────────────────────────────────────────────────────────────────────────

def _compute_seed(language: str, archetype_id: str, counter: int = 0) -> int:
    """Compute a deterministic seed from language + archetype + counter."""
    raw = f"{language}:{archetype_id}:{counter}"
    h = hashlib.sha256(raw.encode()).digest()
    return int.from_bytes(h[:4], "big")


def draw_card(language: str, archetype_id: str, counter: int = 0) -> Dict[str, Any]:
    """Draw a single card deterministically for the given seed."""
    seed = _compute_seed(language, archetype_id, counter)
    card_idx = seed % len(MAJOR_ARCANA)
    card = MAJOR_ARCANA[card_idx]

    # Reversal: based on seed's second byte — roughly half the time
    reversed_flag = (seed >> 8) & 1 == 1

    return {"card": card, "reversed": reversed_flag}


def interpret_card(card_data: Dict[str, Any], language: str) -> Dict[str, Any]:
    """Extract the language-specific interpretation from a card."""
    card = card_data["card"]
    reversed_flag = card_data["reversed"]
    position = card["reversed" if reversed_flag else "upright"]
    lang_interp = position["language"].get(language, "The Oracle has no voice for this language.")
    return {
        "id": card["id"],
        "name": card["name"],
        "symbol": card["symbol"],
        "archetype": card["archetype"],
        "position": "reversed" if reversed_flag else "upright",
        "fortune": position["fortune"],
        "warning": position["warning"],
        "language_interpretation": lang_interp,
    }


def build_spread(language: str, archetype_id: str) -> List[Dict[str, Any]]:
    """Build a 6-position Celtic-inspired spread for a language + archetype."""
    spread = []
    for i, (pos_id, pos_name) in enumerate(SPREAD_POSITIONS):
        card_data = draw_card(language, archetype_id, counter=i)
        interp = interpret_card(card_data, language)
        spread.append({
            "position_id": pos_id,
            "position_name": pos_name,
            "card": interp,
        })
    return spread


# ─────────────────────────────────────────────────────────────────────────────
# Core API
# ─────────────────────────────────────────────────────────────────────────────

def tarot(archetype_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Perform a tarot reading for the current rotation language.

    1. Load rotation, get current language, advance index.
    2. Pick an archetype (by index or given).
    3. Build a 6-card Celtic spread.
    4. Return the full reading.
    """
    config = load_rotation()
    languages = config.get("languages", ROTATION_ORDER)
    current_index = config.get("current_index", 0)
    current_language = languages[current_index % len(languages)]

    # Advance rotation for next run
    advance_rotation()

    # Pick archetype
    if archetype_id is None:
        archetype_idx = current_index % len(READING_ARCHETYPES)
        archetype = READING_ARCHETYPES[archetype_idx]
    else:
        archetype = next(
            (a for a in READING_ARCHETYPES if a["id"] == archetype_id),
            READING_ARCHETYPES[current_index % len(READING_ARCHETYPES)],
        )

    # Build spread
    spread = build_spread(current_language, archetype["id"])

    # Draw the "signature card" (first card of spread)
    sig_card_data = draw_card(current_language, archetype["id"], counter=0)
    sig_interp = interpret_card(sig_card_data, current_language)

    next_lang_idx = current_index + 1
    next_language = languages[next_lang_idx % len(languages)]

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": current_language,
        "language_index": current_index,
        "archetype": archetype,
        "signature_card": sig_card_data,
        "signature_interpretation": sig_interp,
        "spread": spread,
        "rotation_advanced": True,
        "next_language": next_language,
        "next_index": next_lang_idx % len(languages),
        "rotation_order": ROTATION_ORDER,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Formatting
# ─────────────────────────────────────────────────────────────────────────────

def format_card(interp: Dict[str, Any]) -> str:
    """Format a single card interpretation as a string."""
    pos_emoji = "🔴" if interp["position"] == "reversed" else "🟢"
    return (
        f"  {interp['symbol']} **{interp['name']}** [{interp['position'].upper()}] — {interp['archetype']}\n"
        f"       📜 {interp['fortune']}\n"
        f"       ⚠️  {interp['warning']}\n"
        f"       💬 {interp['language_interpretation']}"
    )


def format_tarot_reading(m: Dict[str, Any]) -> str:
    """Format a full tarot reading as a human-readable string."""
    lang = m["language"]
    archetype = m["archetype"]
    sig = m["signature_interpretation"]
    spread = m["spread"]

    lines = [
        "╔═══════════════════════════════════════════════════════════════════╗",
        "║  🔮 POLYGLOT TAROT — The Programming Oracle                     ║",
        "╠═══════════════════════════════════════════════════════════════════╣",
        f"║  Language   : {lang:<48}║",
        f"║  Archetype  : {archetype['emoji']} {archetype['name']} — {archetype['question'].format(lang=''):<30}║",
        "╠═══════════════════════════════════════════════════════════════════╣",
        "║  ✦ SIGNATURE CARD                                               ║",
    ]

    pos_emoji = "🔴 REVERSED" if sig["position"] == "reversed" else "🟢 UPRIGHT"
    lines += [
        f"║  {sig['symbol']} {sig['name']} — {pos_emoji:<40}║",
        f"║  Archetype  : {sig['archetype']:<44}║",
        f"║  📜 {sig['fortune']:<47}║",
        f"║  ⚠️  {sig['warning']:<47}║",
        f"║  💬 {sig['language_interpretation']:<47}║",
        "╠═══════════════════════════════════════════════════════════════════╣",
        "║  🃏 THE CELTIC SPREAD — 6 Positions                            ║",
    ]

    for i, pos in enumerate(spread):
        interp = pos["card"]
        pos_emoji = "🔴" if interp["position"] == "reversed" else "🟢"
        lines.append(
            f"║  {i+1}. [{pos['position_name']}] "
            f"{pos_emoji} {interp['symbol']} {interp['name']:<18} "
            f"{interp['archetype']:<15}  ║"
        )
        lines.append(
            f"║     📜 {interp['fortune']:<44}  ║"
        )
        lines.append(
            f"║     💬 {interp['language_interpretation']:<44}  ║"
        )
        if i < len(spread) - 1:
            lines.append("║     ──────────────────────────────────────────────  ║")

    lines += [
        "╠═══════════════════════════════════════════════════════════════════╣",
        "║  🔮 CODA — The Oracle's Verdict                                 ║",
    ]

    outcome_card = spread[-1]["card"]
    coda = (
        f"When {lang} faces {archetype['name'].lower()} matters, "
        f"the {outcome_card['name']} appears {outcome_card['position']}. "
        f"{outcome_card['fortune']}"
    )
    lines.append(f"║  {coda:<57}  ║")

    lines += [
        "╠═══════════════════════════════════════════════════════════════════╣",
        "║  🔄 NEXT LANGUAGE                                               ║",
        f"║  ➜ {m['next_language']:<56}║",
        "║  🔁 Rotation: Rust → Go → Swift → Kotlin → TS → JS → Java → C/C++║",
        "╚═══════════════════════════════════════════════════════════════════╝",
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────────────

def run_tests() -> None:
    """Run all tests for the Polyglot Tarot module."""
    import sys

    errors: List[str] = []
    passed = 0

    def t(name: str, cond: bool, msg: str = "") -> None:
        nonlocal passed, errors
        if cond:
            print(f"  ✅ {name}")
            passed += 1
        else:
            print(f"  ❌ {name}: {msg}")
            errors.append(name)

    print("🔮 Polyglot Tarot — Running Tests\n")

    # ── Files ─────────────────────────────────────────────────────────────────
    try:
        t("ROTATION_FILE exists", os.path.exists(ROTATION_FILE))
    except Exception as e:
        t("ROTATION_FILE accessible", False, str(e))

    # ── Module constants ────────────────────────────────────────────────────────
    t("TOOL_NAME is 'polyglot-tarot'", TOOL_NAME == "polyglot-tarot")
    t("TOOL_VERSION is '1.0.0'", TOOL_VERSION == "1.0.0")
    t("ROTATION_ORDER has 8 languages", len(ROTATION_ORDER) == 8)
    t("ROTATION_ORDER matches expected sequence",
      ROTATION_ORDER == ["Rust","Go","Swift","Kotlin","TypeScript","JavaScript","Java","C/C++"])

    # ── MAJOR_ARCANA ──────────────────────────────────────────────────────────
    t("MAJOR_ARCANA has 22 cards", len(MAJOR_ARCANA) == 22)
    ids = [c["id"] for c in MAJOR_ARCANA]
    t("MAJOR_ARCANA IDs are 0-21", ids == list(range(22)))
    for card in MAJOR_ARCANA:
        t(f"  Card {card['id']} '{card['name']}' has upright/reversed",
          "upright" in card and "reversed" in card)
        t(f"  Card {card['id']} has all 8 language interpretations",
          all(lang in card["upright"]["language"] for lang in ROTATION_ORDER))
        t(f"  Card {card['id']} reversed has all 8 language interpretations",
          all(lang in card["reversed"]["language"] for lang in ROTATION_ORDER))

    # ── READING_ARCHETYPES ─────────────────────────────────────────────────────
    t("READING_ARCHETYPES has 8 entries", len(READING_ARCHETYPES) == 8)
    for arch in READING_ARCHETYPES:
        t(f"  Archetype '{arch['id']}' has id/name/emoji/question",
          all(k in arch for k in ("id", "name", "emoji", "question")))

    # ── SPREAD_POSITIONS ───────────────────────────────────────────────────────
    t("SPREAD_POSITIONS has 6 entries", len(SPREAD_POSITIONS) == 6)

    # ── Determinism: same seed → same card ────────────────────────────────────
    card1 = draw_card("Rust", "null_handling", counter=0)
    card2 = draw_card("Rust", "null_handling", counter=0)
    t("draw_card is deterministic (same seed)", card1["card"]["id"] == card2["card"]["id"])
    t("draw_card is deterministic (same seed, same reversal)",
      card1["reversed"] == card2["reversed"])

    # ── Different seeds → different results ───────────────────────────────────
    card_rust = draw_card("Rust", "null_handling", counter=0)
    card_go   = draw_card("Go",   "null_handling", counter=0)
    t("draw_card differs between languages", card_rust["card"]["id"] != card_go["card"]["id"])

    card_null = draw_card("Rust", "null_handling", counter=0)
    card_err  = draw_card("Rust", "error_recovery", counter=0)
    t("draw_card differs between archetypes", card_null["card"]["id"] != card_err["card"]["id"])

    # ── interpret_card ─────────────────────────────────────────────────────────
    card_data = draw_card("Rust", "null_handling", counter=0)
    interp = interpret_card(card_data, "Rust")
    t("interpret_card returns required fields",
      all(k in interp for k in ("id", "name", "symbol", "archetype",
                                 "position", "fortune", "warning", "language_interpretation")))
    t("interpret_card has language_interpretation", isinstance(interp["language_interpretation"], str))

    # ── build_spread ──────────────────────────────────────────────────────────
    spread = build_spread("JavaScript", "concurrency")
    t("build_spread returns 6 positions", len(spread) == 6)
    t("build_spread positions have required fields",
      all(all(k in p for k in ("position_id", "position_name", "card")) for p in spread))
    t("build_spread position IDs are unique", len(set(p["position_id"] for p in spread)) == 6)

    # ── load_rotation / save_rotation ────────────────────────────────────────
    try:
        cfg = load_rotation()
        t("load_rotation returns dict", isinstance(cfg, dict))
        t("rotation has 'languages' key", "languages" in cfg)
        t("rotation has 'current_index' key", "current_index" in cfg)
        t("rotation languages match ROTATION_ORDER", cfg["languages"] == ROTATION_ORDER)
    except Exception as e:
        t("load_rotation succeeds", False, str(e))

    # ── tarot() rotation advancement ───────────────────────────────────────────
    # Save rotation state so tests don't permanently advance the index
    _saved_cfg = load_rotation()
    try:
        cfg_before = load_rotation()
        idx_before = cfg_before["current_index"]
        lang_before = cfg_before["languages"][idx_before % len(cfg_before["languages"])]
        result = tarot()
        cfg_after = load_rotation()
        idx_after = cfg_after["current_index"]
        t("tarot() advances current_index",
          idx_after == (idx_before + 1) % len(cfg_before["languages"]))
        t("tarot() returns the correct language", result["language"] == lang_before)
        t("tarot() returns rotation_advanced=True", result.get("rotation_advanced") is True)
        t("tarot() returns next_language", "next_language" in result)
        t("tarot() returns archetype", "archetype" in result)
        t("tarot() returns signature_card", "signature_card" in result)
        t("tarot() returns spread with 6 positions", len(result["spread"]) == 6)
    except Exception as e:
        t("tarot() rotation advancement", False, str(e))
    finally:
        save_rotation(_saved_cfg)

    # ── format_tarot_reading ──────────────────────────────────────────────────
    _saved_cfg2 = load_rotation()
    try:
        result = tarot()
        formatted = format_tarot_reading(result)
        t("format_tarot_reading returns a string", isinstance(formatted, str))
        t("format_tarot_reading starts with box char", formatted.startswith("╔"))
        t("format_tarot_reading ends with box char", formatted.rstrip().endswith("╝"))
        t("format_tarot_reading contains the language", result["language"] in formatted)
        t("format_tarot_reading contains signature card name",
          result["signature_interpretation"]["name"] in formatted)
    except Exception as e:
        t("format_tarot_reading", False, str(e))
    finally:
        save_rotation(_saved_cfg2)

    # ── All cards have language interpretations ────────────────────────────────
    for card in MAJOR_ARCANA:
        for lang in ROTATION_ORDER:
            t(f"Card {card['id']} upright has '{lang}' interp",
              lang in card["upright"]["language"])
            t(f"Card {card['id']} reversed has '{lang}' interp",
              lang in card["reversed"]["language"])

    # ── All archetypes cover all languages ────────────────────────────────────
    # The 8 archetypes cover all languages in each card interpretation

    print(f"\n{'='*60}")
    if errors:
        print(f"❌ {len(errors)} test(s) failed: {', '.join(errors)}")
        sys.exit(1)
    else:
        print(f"✅ All {passed} tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        result = tarot()
        print(format_tarot_reading(result))
