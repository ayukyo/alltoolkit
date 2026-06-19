#! /usr/bin/env python3
"""
🚀 Polyglot Odyssey v1.0

A time-travel journey through programming language history. Each rotation
language appears as a historical "waypoint era" with ASCII timeline maps,
archaeological artifacts, and a journey narrative for the current language.

Creative concept: "Programming languages are epochs in the grand story of
computation. Polyglot Odyssey generates an ASCII timeline journey — each
language is a destination with its own era, landmarks, cultural artifacts,
and a forward/backward path through the history of languages. The current
rotation language becomes your travel destination, with contextual travel
advice on what to pack (mental model), how to navigate (syntax patterns),
and what to see (signature features)."

Unlike other tools:
  - polyglot_chronology: macro timeline of ALL languages through deep time
  - polyglot_cartographer: geopolitical world map metaphor
  - polyglot_chef: kitchen brigade metaphor
  - polyglot_tarot: mystical card readings per session
  - polyglot_oracle: philosophical counsel from one language's perspective

Odyssey is a JOURNEY NARRATIVE — a travel itinerary through language history,
with each destination (language) having landmarks, cultural notes, travel
warnings, and a "souvenir" (code artifact) you bring back.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import random
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-odyssey"
TOOL_VERSION = "1.0.0"

# ─────────────────────────────────────────────────────────────────────────────
# File paths
# ─────────────────────────────────────────────────────────────────────────────
_MODULE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # polyglot_odyssey/
_WORKSPACE_ROOT = os.path.dirname(_MODULE_DIR)                              # AllToolkit/ -> workspace/
_ROTATION_FILE = os.path.join(_WORKSPACE_ROOT, "language_rotation.json")

# ─────────────────────────────────────────────────────────────────────────────
# Language waypoint eras — each language is a historical time period
# ─────────────────────────────────────────────────────────────────────────────
# Each era has:
#   - era_year: fictional historical date string
#   - era_subtitle: poetic subtitle for the era
#   - birthplace: where the language originated
#   - founding_rationale: why it was created
#   - landmarks: ASCII-art featured sites
#   - cultural_artifacts: notable syntax/code patterns as "museum exhibits"
#   - travel_warnings: pitfalls for visitors
#   - local_customs: idiomatic patterns
#   - era_treasures: signature features as collectible items
#   - visit_summary: short description of what makes this era notable

LANGUAGE_ERAS: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "era_year": "2015 ERA — The Safety Reformation",
        "era_subtitle": "Where Memory Becomes Law",
        "birthplace": "Mozilla Research, Mountain View",
        "founding_rationale": "A rebellion against memory unsafety — the Safety Reformation established "
                               "compile-time ownership as the supreme law. The borrow checker became "
                               "the great auditor of every memory transaction.",
        "landmarks": [
            {
                "name": "The Ownership Citadel",
                "ascii": [
                    "              ▲",
                    "             ╱ ╲",
                    "            ╱   ╲",
                    "           ╱ BORROW╲",
                    "          ╱ CHECKER ╲",
                    "         ╱___________╲",
                    "        ║  [CORE]    ║",
                    "        ║ ═══════════║",
                    "       ═╝             ╚═",
                    "      ═╝   [STACK]       ╚═",
                    "     ═╝      [HEAP]        ╚═",
                ],
            },
            {
                "name": "The Zero-Cost Abstraction Bazaar",
                "ascii": [
                    " ╔══════════════════════════════╗",
                    " ║  ZERO-COST ABSTRACTION BAZAAR ║",
                    " ╠══════════════════════════════╣",
                    " ║ [iter()]  [Box<T>]  [Arc<T>] ║",
                    " ║  no tax      heap     shared  ║",
                    " ╠══════════════════════════════╣",
                    " ║      COMPILE-TIME PROOF       ║",
                    " ╚══════════════════════════════╝",
                ],
            },
            {
                "name": "The Pattern Matching Cathedral",
                "ascii": [
                    "         ▲▲▲",
                    "        ╱   ╲",
                    "       ╱ match╲",
                    "      ╱  arm   ╲",
                    "     ╱__________╲",
                    "     ║          ║",
                    "     ║  Some(v) ║ => v + 1",
                    "     ║  None    ║ => 0",
                    "     ╚══════════╝",
                ],
            },
        ],
        "cultural_artifacts": [
            {
                "artifact_id": "ownership_contract",
                "name": "Ownership Transfer Contract",
                "description": "The founding document of Rust — proves that exactly one entity "
                               "owns a resource at any time. Transfer is explicit, no silent copies.",
                "code_example": "let s1 = String::from(\"hello\");\nlet s2 = s1; // s1 moved, s2 now owns",
            },
            {
                "artifact_id": "borrow_check_scroll",
                "name": "Borrow Checker Scroll",
                "description": "The ancient scroll that defines the rules of borrowing — "
                               "either many immutable references OR one mutable, never both.",
                "code_example": "let mut v = vec![1, 2, 3];\nlet r1 = &v;\nlet r2 = &v; // OK\nlet rm = &mut v; // NOT OK — can't have & and &mut",
            },
            {
                "artifact_id": "result_monad",
                "name": "Result Monad Shrine",
                "description": "Where errors are typed citizens. No exceptions — every fallible "
                               "operation returns Result<T, E> and the ? operator propagates.",
                "code_example": "fn read() -> Result<String, io::Error> {\n    let mut f = File::open(\"foo\")?;\n    let mut s = String::new();\n    f.read_to_string(&mut s)?;\n    Ok(s)\n}",
            },
        ],
        "travel_warnings": [
            "⚠️ The Borrow Checker is strict — fight it and lose. Redesign instead.",
            "⚠️ Lifetime annotations are cryptic at first — they're the language's memory of where references live.",
            "⚠️ No garbage collector means YOU own the correctness — the compiler just verifies your proof.",
            "⚠️ Async is powerful but the learning curve is real — start with sync Rust first.",
        ],
        "local_customs": [
            "Greet with `let` declarations — everything starts with binding",
            "Use `match` for exhaustive control flow — if you can think it, the compiler will demand it",
            "Return types go last: `fn add(a: i32, b: i32) -> i32 { a + b }`",
            "Semicolons mean 'discard the value'; no semicolon means 'return this'",
            "`unwrap()` is considered rude in polite company — handle the Result",
        ],
        "era_treasures": [
            "🏆 The Ownership Algebra — proof of exclusive access, statically verified",
            "🏆 The Zero-Cost Abstraction Gem — high-level code, machine speed",
            "🏆 The Fearless Concurrency Talisman — Send + Sync let the compiler catch races",
            "🏆 Pattern Matching Relic — exhaustive, declarative, elegant",
            "🏆 Algebraic Data Types — enums that hold values, Option<T>, Result<T, E>",
        ],
        "visit_summary": "Rust's era is defined by the Safety Reformation — a radical proposition "
                         "that memory safety is not a runtime feature but a compile-time proof. "
                         "The borrow checker is demanding, but it keeps the peace.",
    },
    "Go": {
        "era_year": "2009 ERA — The Simplicity Uprising",
        "era_subtitle": "Against Complexity, With Channels",
        "birthplace": "Google, Menlo Park",
        "founding_rationale": "The Simplicity Uprising arose from frustration with C++ complexity. "
                               "Go's founders wanted a language for the modern cloud — goroutines as "
                               "first-class citizens, interfaces without ceremony, and a tool that "
                               "ships in minutes, not hours.",
        "landmarks": [
            {
                "name": "The Goroutine Highway",
                "ascii": [
                    " ═══════════════════════════════════",
                    " ═══>  goroutine  ═══>  goroutine  ═══>",
                    " ═══════════════════════════════════",
                    "    [CHAN]        [CHAN]       [CHAN]",
                    " ═══════════════════════════════════",
                    " ═══>  goroutine  ═══>  goroutine  ═══>",
                    " ═══════════════════════════════════",
                    "          [select] intersection",
                ],
            },
            {
                "name": "The Interface Theatre",
                "ascii": [
                    " ┌─────────────────────────────────┐",
                    " │     INTERFACE THEATRE           │",
                    " ├─────────────────────────────────┤",
                    " │  ╭───────╮   ╭───────────╮      │",
                    " │  │Reader│───│ io.Reader │      │",
                    " │  ╰───────╯   ╰───────────╯      │",
                    " │  ╭───────╮   ╭───────────╮      │",
                    " │  │Writer│───│ io.Writer │      │",
                    " │  ╰───────╯   ╰───────────╯      │",
                    " └─────────────────────────────────┘",
                ],
            },
            {
                "name": "The Error Pager Station",
                "ascii": [
                    " ┌──────────────────────────────┐",
                    " │  ERROR PAGING STATION        │",
                    " ├──────────────────────────────┤",
                    " │  func() (Val, error) {       │",
                    " │    ...                        │",
                    " │    if err != nil {            │",
                    " │      return nil, err          │",
                    " │    }                          │",
                    " │    return val, nil            │",
                    " │  }                           │",
                    " └──────────────────────────────┘",
                ],
            },
        ],
        "cultural_artifacts": [
            {
                "artifact_id": "goroutine_spawn",
                "name": "Goroutine Spawn Scroll",
                "description": "The spell that conjures a goroutine — a lightweight thread managed "
                               "by the Go runtime, not the OS. Spawn thousands without flinching.",
                "code_example": "go func() {\n    fmt.Println(\"I run concurrently!\")\n}()\n// The 'go' keyword is the invocation",
            },
            {
                "artifact_id": "channel_comm",
                "name": "Channel Communication Tablet",
                "description": "CSP channels — pipes through which goroutines communicate. "
                               "'Share memory by communicating' is the founding doctrine.",
                "code_example": "ch := make(chan int)\ngo func() { ch <- 42 }()\nresult := <-ch // blocks until value available",
            },
            {
                "artifact_id": "defer_ritual",
                "name": "Defer Ritual Stone",
                "description": "The defer statement ensures cleanup runs when the function exits — "
                               "whether normally or via panic. Essential for resource management.",
                "code_example": "f, _ := os.Open(\"file\")\ndefer f.Close() // runs when surrounding function exits",
            },
        ],
        "travel_warnings": [
            "⚠️ No generics until Go 1.18 — if you need generic code, wait or use interface{}",
            "⚠️ Goroutine leaks are real — a blocked goroutine holding a channel lives forever",
            "⚠️ The nil interface is treacherous — a nil concrete type stored in an interface is not nil",
            "⚠️ Error handling is verbose — `if err != nil { return err }` is a ritual you perform often",
        ],
        "local_customs": [
            "Greet with `package main` at the entry point — every program is a package",
            "Import paths are URLs: `import \"github.com/user/repo\"`",
            "Opening brace `{` must be on the same line as the function declaration — this is enforced",
            "Use `:=` for short variable declarations, `var` for explicit types at package level",
            "Return multiple values freely — `(string, error)` is the Go idiom for fallible operations",
        ],
        "era_treasures": [
            "🏆 Goroutine — cheap concurrency for the cloud era",
            "🏆 Channel CSP — share memory by communicating",
            "🏆 The Toolchain — go build, go test, go fmt: everything you need in the box",
            "🏆 Defer — guaranteed cleanup, always",
            "🏆 Interface composition — implicit satisfaction, no ceremony",
        ],
        "visit_summary": "Go's era is defined by the Simplicity Uprising — a deliberate rejection of "
                         "complexity in favor of clarity. Goroutines and channels make concurrency "
                         "a first-class joy, not an afterthought.",
    },
    "Swift": {
        "era_year": "2014 ERA — The Safety & Elegance Renaissance",
        "era_subtitle": "Where Safety Meets Aesthetic",
        "birthplace": "Apple Inc., Cupertino",
        "founding_rationale": "The Elegance Renaissance aimed to do what Objective-C never could: "
                               "combine the power of a compiled systems language with the ergonomics "
                               "of a modern scripting language. Optionals, value types, and protocol "
                               "oriented programming defined a new aesthetic.",
        "landmarks": [
            {
                "name": "The Optional Chain Bridge",
                "ascii": [
                    "     ╭───────────╮",
                    "     │  person?  │",
                    "     │   .name   │",
                    "     │   .uppercased() │",
                    "     ╰───────────╯",
                    "         │ safe navigation",
                    "         ▼",
                    "     Optional<String>",
                    "         │",
                    "    ┌────┴────┐",
                    "    │  nil?   │",
                    "    │ unwrap  │",
                    "    │ orElse  │",
                    "    └─────────┘",
                ],
            },
            {
                "name": "The Copy-on-Write Library",
                "ascii": [
                    " ┌──────────────────────────────┐",
                    " │  COPY-ON-WRITE LIBRARY      │",
                    " ├──────────────────────────────┤",
                    " │                              │",
                    " │  [A]───copy───▶ [A]         │",
                    " │   │               │          │",
                    " │   │   shared ref   │          │",
                    " │   ▼               ▼          │",
                    " │  [A]�──write───▶ [A']         │",
                    " │          new copy           │",
                    " └──────────────────────────────┘",
                ],
            },
            {
                "name": "The Actor Isle",
                "ascii": [
                    "   ◎═══◎═══◎",
                    "   ║   ║   ║",
                    "   ║ ISOLATED ║",
                    "   ║  STATE   ║",
                    "   ◎═══◎═══◎",
                    "   ║   ║   ║",
                    "   async ferry",
                ],
            },
        ],
        "cultural_artifacts": [
            {
                "artifact_id": "optional_pattern",
                "name": "The Optional Safety Badge",
                "description": "The badge that marks nullable types — T? means 'T or nil'. "
                               "Forcing unwrap (!) is the reckless tourist move.",
                "code_example": "let name: String? = nil\nlet safe = name ?? \"Anonymous\"  // coalescing\nif let unwrapped = name {\n    print(unwrapped)  // only if non-nil\n}",
            },
            {
                "artifact_id": "protocol_ext",
                "name": "Protocol Extension Monument",
                "description": "Protocols with default implementations — define behavior once, "
                               "apply to all conforming types automatically.",
                "code_example": "protocol Drawable {\n    func draw()\n}\nextension Drawable {\n    func draw() { print(\"default\") } // default impl\n}",
            },
        ],
        "travel_warnings": [
            "⚠️ ARC is not garbage collection — reference cycles will leak memory",
            "⚠️ @StateObject vs @ObservedObject vs @EnvironmentObject — know which owns the data",
            "⚠️ Swift 6 makes data-race safety a compile error — migrate carefully",
            "⚠️ UIKit and SwiftUI coexist uneasily — bridging them requires care",
        ],
        "local_customs": [
            "Greet with `import Foundation` or `import SwiftUI` — name your imports",
            "Use `guard` for early exits — it's the Swift way of saying 'bail out now'",
            "Trailing closures: `array.map { $0 * 2 }` — the last arg can hang off the call",
            "`let` is the default — only use `var` when you truly need mutation",
            "Range operators: `..<` (half-open), `...` (closed) — know which you're using",
        ],
        "era_treasures": [
            "🏆 Optional — nil safety baked into the type system",
            "🏆 Copy-on-Write value semantics — efficient by default",
            "🏆 Protocol-oriented programming — composition over inheritance",
            "🏆 Actor model (Swift 6) — compile-time data-race safety",
            "🏆 Trailing closure syntax — functional elegance, readable code",
        ],
        "visit_summary": "Swift's era is the Safety & Elegance Renaissance — a proof that a language "
                         "can be both safe and beautiful. Optionals eliminate null pointer exceptions "
                         "by making absence a type-level concept.",
    },
    "Kotlin": {
        "era_year": "2011 ERA — The Pragmatic Modernization",
        "era_subtitle": "JVM Power With Half the Ceremony",
        "birthplace": "JetBrains, Prague",
        "founding_rationale": "The Pragmatic Modernization answered a simple question: what if we "
                               "took the JVM ecosystem we depend on and removed half the boilerplate? "
                               "Kotlin brought null safety, extension functions, and coroutines "
                               "without asking developers to abandon their libraries.",
        "landmarks": [
            {
                "name": "The Nullable Type Checkpoint",
                "ascii": [
                    "  ┌────────────────────────────┐",
                    "  │  NULLABLE TYPE CHECKPOINT  │",
                    "  ├────────────────────────────┤",
                    "  │                            │",
                    "  │  val a: String  = \"hi\"     │",
                    "  │  val b: String? = null     │",
                    "  │                            │",
                    "  │  a.length   ✓ no check     │",
                    "  │  b?.length  ✓ safe call    │",
                    "  │  b!!.length ⚠ crash       │",
                    "  │                            │",
                    "  └────────────────────────────┘",
                ],
            },
            {
                "name": "The Coroutine Ski Resort",
                "ascii": [
                    "      ║  ║  ║  ║",
                    "      ║  ║  ║  ║  ← suspend cable cars",
                    "      ║  ║  ║  ║",
                    "    ════════════════",
                    "    │  FLOW RIVER  │ ← streams",
                    "    ════════════════",
                    "    [COROUTINE RESORT OFFICE]",
                    "    scope: viewModelScope",
                ],
            },
            {
                "name": "The Extension Function Library",
                "ascii": [
                    "  ┌────────────────────────────────┐",
                    "  │  EXTENSION FUNCTION LIBRARY   │",
                    "  ├────────────────────────────────┤",
                    "  │                                │",
                    "  │  fun String.addExclamation()   │",
                    "  │      = this + \"!\"              │",
                    "  │                                │",
                    "  │  \"hello\".addExclamation()      │",
                    "  │  // = \"hello!\"                 │",
                    "  │                                │",
                    "  └────────────────────────────────┘",
                ],
            },
        ],
        "cultural_artifacts": [
            {
                "artifact_id": "data_class",
                "name": "Data Class Seal",
                "description": "The seal that auto-generates equals(), hashCode(), toString(), "
                               "copy(), and destructuring for a class. One keyword, full payload.",
                "code_example": "data class User(\n    val name: String,\n    val age: Int\n)\nval user = User(\"Alice\", 30)\nval copy = user.copy(name = \"Bob\")",
            },
            {
                "artifact_id": "scope_functions",
                "name": "Scope Function Gallery",
                "description": "let, run, with, apply, also — five functions that execute a block "
                               "in a specific context (it/this) and return a value. Master these and "
                               "your code flows like water.",
                "code_example": "val length = \"hello\"\n    .run { this.uppercase() }\n    .run { this.length }\n// = 5",
            },
        ],
        "travel_warnings": [
            "⚠️ Nullable types (T?) are not the same as platform types (T!) from Java interop",
            "⚠️ Coroutine cancellation is cooperative — if a coroutine doesn't check, it won't stop",
            "⚠️ Using lateinit var defeats null safety — use by lazy {} instead when possible",
            "⚠️ Kotlin's `==` is structural equality (equals()), `===` is identity — unlike Java",
        ],
        "local_customs": [
            "Greet with `fun` — functions are first-class citizens, declared with flair",
            "Semicolons are optional — whitespace carries meaning",
            "Use `val` by default, `var` only when necessary — immutable is the default",
            "Extension functions let you add methods to classes you don't own — use wisely",
            "When returning a value, the last expression is returned — no explicit 'return' needed",
        ],
        "era_treasures": [
            "🏆 Nullable types — T? makes absence a compile-time concept",
            "🏆 Coroutines — async/await without callback pyramids",
            "🏆 Data classes — one keyword, auto-generated boilerplate",
            "🏆 Extension functions — add methods to existing types without inheritance",
            "🏆 Smart casts — the compiler tracks your type checks and removes casts",
        ],
        "visit_summary": "Kotlin's era is pragmatic modernization — JetBrains took the best parts "
                         "of the JVM (libraries, tooling, ecosystem) and fixed the worst parts "
                         "(verbose types, null hazards, lack of coroutines). The result: a language "
                         "developers actually enjoy.",
    },
    "TypeScript": {
        "era_year": "2012 ERA — The Type Annotation Uprising",
        "era_subtitle": "JavaScript, But With Proofs",
        "birthplace": "Microsoft Research, Redmond",
        "founding_rationale": "The Type Annotation Uprising began as a simple question: what if "
                               "we could add a type system to JavaScript without losing the soul of "
                               "the language? TypeScript added optional types, interfaces, and "
                               "generics on top of ES5, creating a superset that compiles to "
                               "plain JavaScript.",
        "landmarks": [
            {
                "name": "The Structural Type Market",
                "ascii": [
                    "  ┌──────────────────────────────┐",
                    "  │  STRUCTURAL TYPE MARKET    │",
                    "  ├──────────────────────────────┤",
                    "  │                              │",
                    "  │  interface Drawable {        │",
                    "  │    draw(): void              │",
                    "  │  }                           │",
                    "  │                              │",
                    "  │  class Circle implements     │",
                    "  │    Drawable { draw() {...} }│",
                    "  │                              │",
                    "  │  if it HAS the shape,        │",
                    "  │  it FITS the interface       │",
                    "  └──────────────────────────────┘",
                ],
            },
            {
                "name": "The Union Type Crossroads",
                "ascii": [
                    "       ╱ A ╲",
                    "      ╱     ╲",
                    "  ───╱  A|B  ╲───",
                    "     ╲       ╱",
                    "      ╲  B  ╱",
                    "       ╲   ╱",
                    "    ┌───┴───┐",
                    "    │ switch │",
                    "    │  case  │",
                    "    │ exhaust│",
                    "    └────────┘",
                ],
            },
            {
                "name": "The Generic Forge",
                "ascii": [
                    "  ┌────────────────────────────────┐",
                    "  │  GENERIC FORGE                │",
                    "  ├────────────────────────────────┤",
                    "  │                                │",
                    "  │  function identity<T>(         │",
                    "  │    arg: T): T {                │",
                    "  │    return arg                  │",
                    "  │  }                            │",
                    "  │                                │",
                    "  │  identity<number>(42)         │",
                    "  │  // = 42 (typed!)             │",
                    "  └────────────────────────────────┘",
                ],
            },
        ],
        "cultural_artifacts": [
            {
                "artifact_id": "type_guard",
                "name": "Type Guard Scroll",
                "description": "Custom type predicates that narrow union types — the compiler "
                               "learns your type checks and applies them automatically.",
                "code_example": "function isString(x: unknown): x is string {\n    return typeof x === 'string'\n}\nif (isString(val)) {\n    console.log(val.toUpperCase()) // val is string here\n}",
            },
            {
                "artifact_id": "discriminated_union",
                "name": "Discriminated Union Banner",
                "description": "Union types with a common literal field — the 'kind' field lets "
                               "the compiler exhaustively check every case. Makes invalid states "
                               "unrepresentable.",
                "code_example": "type Result<T> =\n    | { kind: 'ok', value: T }\n    | { kind: 'err', error: Error }\nswitch (r.kind) {\n    case 'ok': return r.value\n    case 'err': return r.error\n}",
            },
        ],
        "travel_warnings": [
            "⚠️ `any` is the escape hatch — it defeats the type system's safety net",
            "⚠️ TypeScript compiles to JavaScript — runtime behavior is still JS behavior",
            "⚠️ `strict: true` is the safe mode — don't disable individual flags",
            "⚠️ Type assertions (`as`) are lies you tell the compiler — use sparingly",
        ],
        "local_customs": [
            "Greet with `interface` — name your contracts before using them",
            "Use `unknown` instead of `any` for truly unknown data — narrow before using",
            "Enums are old news — use `const enum` or union types instead",
            "Use `type` for aliases, `interface` for object shapes that may be extended",
            "The `?` operator: `obj.foo?.bar` — safe property access, returns undefined if any part is null",
        ],
        "era_treasures": [
            "🏆 Structural typing — if it quacks like a duck, it IS a duck (at compile time)",
            "🏆 Generics — code that works across types, with compile-time safety",
            "🏆 Discriminated unions — exhaustiveness checking makes invalid states unrepresentable",
            "🏆 Optional chaining & nullish coalescing — `?.` and `??` handle absence gracefully",
            "🏆 Compilation to JavaScript — runs everywhere JavaScript runs",
        ],
        "visit_summary": "TypeScript's era is the Type Annotation Uprising — Microsoft proved that "
                         "adding types to JavaScript could catch bugs at compile time without "
                         "changing the runtime. The result is the most widely-used language "
                         "for large-scale web applications.",
    },
    "JavaScript": {
        "era_year": "1995 ERA — The Prototypal Rebellion",
        "era_subtitle": "The Language That Ate the World",
        "birthplace": "Netscape Communications, Mountain View",
        "founding_rationale": "The Prototypal Rebellion started with a 10-day sprint. Brendan Eich "
                               "embedded a Scheme-like language into Netscape Navigator, called it "
                               "JavaScript as a marketing decision, and accidentally created the "
                               "world's most ubiquitous language. It runs in every browser, on every "
                               "server (Node), and increasingly on every device.",
        "landmarks": [
            {
                "name": "The Prototype Chain Tower",
                "ascii": [
                    "        Object.prototype",
                    "              │",
                    "        ┌─────┴─────┐",
                    "        │           │",
                    "   Array.prototype  String.prototype",
                    "        │           │",
                    "        │     ┌─────┴─────┐",
                    "        │     │           │",
                    "    [1,2,3].__proto__  \"hi\".__proto__",
                    "        │           │",
                    "    Array        String",
                ],
            },
            {
                "name": "The Closure Workshop",
                "ascii": [
                    "  ┌──────────────────────────────────┐",
                    "  │  CLOSURE WORKSHOP               │",
                     "  ├──────────────────────────────────┤",
                    "  │                                  │",
                    "  │  function outer() {              │",
                    "  │    let x = 10;                   │",
                    "  │    return function inner() {     │",
                    "  │      return x; // captures x     │",
                    "  │    }                             │",
                    "  │  }                               │",
                    "  │  const fn = outer()             │",
                    "  │  fn() // = 10, x lives on!       │",
                    "  │                                  │",
                    "  └──────────────────────────────────┘",
                ],
            },
            {
                "name": "The Event Loop Arena",
                "ascii": [
                    "       ○ Call Stack",
                    "       │",
                    "    ┌──┴──┐",
                    "    │ WEB │",
                    "    │  APIS│",
                    "    └──┬──┘",
                    "       │",
                    "    ┌──┴──┐",
                    "    │QUEUE│",
                    "    │micro│",
                    "    │task │",
                    "    └─────┘",
                ],
            },
        ],
        "cultural_artifacts": [
            {
                "artifact_id": "first_class_functions",
                "name": "First-Class Function Manifesto",
                "description": "Functions are values — stored in variables, passed as arguments, "
                               "returned from other functions. This single fact powers async/await, "
                               "map/filter/reduce, and every modern JS pattern.",
                "code_example": "const add = (a, b) => a + b\nconst double = (fn) => (x) => fn(x, x)\nconst quad = double(add)\nquad(2) // = 8",
            },
            {
                "artifact_id": "promise_pattern",
                "name": "Promise Chain Monument",
                "description": "Where async operations chain cleanly — no callback pyramid. "
                               "Then/catch/finally form a readable async narrative.",
                "code_example": "fetch('/api/user')\n  .then(r => r.json())\n  .then(user => updateUI(user))\n  .catch(err => showError(err))",
            },
        ],
        "travel_warnings": [
            "⚠️ `this` is context-sensitive — use arrow functions or `.bind()` in callbacks",
            "⚠️ `==` does type coercion, `===` does not — always use `===`",
            "⚠️ Hoisting moves declarations but not initializations — know what you're using",
            "⚠️ Prototypal inheritance is real — `class` syntax is syntactic sugar over it",
        ],
        "local_customs": [
            "Greet with `const` — let is for values that change, const is for bindings that don't",
            "Arrow functions: `const f = (x) => x * 2` — concise, lexically scoped `this`",
            "Use `async/await` over raw promises — it reads like synchronous code",
            "Template literals: `Hello ${name}` — no more string concatenation",
            "`undefined` is uninitialized; `null` is intentional absence — know the difference",
        ],
        "era_treasures": [
            "🏆 Prototype chain — objects inherit directly from objects, no classes required",
            "🏆 First-class functions — functions as values, callbacks as a design pattern",
            "🏆 Closures — functions that remember their scope",
            "🏆 Event loop — non-blocking async that powers the modern web",
            "🏆 The entire npm ecosystem — 2 million packages at your fingertips",
        ],
        "visit_summary": "JavaScript's era is the Prototypal Rebellion — the language that started "
                         "as a 10-day hack became the universal runtime. From browsers to servers "
                         "to embedded devices, JavaScript runs everywhere. Its quirks are famous, "
                         "but its reach is unmatched.",
    },
    "Java": {
        "era_year": "1995 ERA — The Object-Oriented Commonwealth",
        "era_subtitle": "Write Once, Run Anywhere (Almost)",
        "birthplace": "Sun Microsystems, Santa Clara",
        "founding_rationale": "The Object-Oriented Commonwealth unified the fragmented landscape "
                               "of platform-specific code. 'Write Once, Run Anywhere' was the battle "
                               "cry — the JVM was the great equalizer. Generics, checked exceptions, "
                               "and enterprise-grade tooling followed.",
        "landmarks": [
            {
                "name": "The Class Hierarchy Temple",
                "ascii": [
                    "           Object",
                    "          ╱      ╲",
                    "     Person    Animal",
                    "        │        │",
                    "     Employee  Dog",
                    "        │",
                    "     Manager",
                    "",
                    "    inheritance tree",
                ],
            },
            {
                "name": "The Generic Archive (Type Erasure Museum)",
                "ascii": [
                    "  ┌─────────────────────────────────┐",
                    "  │  TYPE ERASURE MUSEUM           │",
                    "  ├─────────────────────────────────┤",
                    "  │                                 │",
                    "  │  List<String>                   │",
                    "  │       │                         │",
                    "  │  compiled to                   │",
                    "  │       ▼                         │",
                    "  │  List     (erased!)             │",
                    "  │                                 │",
                    "  │  [T] becomes [Object]            │",
                    "  │                                 │",
                    "  └─────────────────────────────────┘",
                ],
            },
            {
                "name": "The Garbage Collection Garden",
                "ascii": [
                    "  ┌──────────────────────────────────┐",
                    "  │   GC GARDEN — WATCH GROW        │",
                    "  ├──────────────────────────────────┤",
                    "  │                                  │",
                    "  │  Eden    │  S0   │  S1  │ OldGen│",
                    "  │  ┌─────┐ │ ┌──┐ │ ┌──┐ │ ┌────┐ │",
                    "  │  │ obj │ │ │  │ │ │  │ │ │████│ │",
                    "  │  └─────┘ │ └──┘ │ └──┘ │ │████│ │",
                    "  │   ↓copy ↓  ↓    │    │copy│ old │",
                    "  │  ┌─────┐ │ ┌──┐ │    │ ┌──┐│    │",
                    "  │  │survivors│ │  │ │    │ │  ││    │",
                    "  │  └─────┘ │ └──┘ │    │ └──┘│    │",
                    "  └──────────────────────────────────┘",
                ],
            },
        ],
        "cultural_artifacts": [
            {
                "artifact_id": "interface_default",
                "name": "Interface Default Method Scroll",
                "description": "Java 8 added default methods to interfaces — previously immutable "
                               "contracts could now have implementations. The 'virtual extension "
                               "method' controversy, resolved.",
                "code_example": "interface Drawable {\n    void draw();\n    default void print() {\n        System.out.println(\"default\");\n    }\n}",
            },
            {
                "artifact_id": "lambda_manifesto",
                "name": "Lambda Expression Manifesto",
                "description": "Java 8 embraced functional programming — lambdas brought behavior "
                               "as values. `->` became the syntax for creating anonymous function "
                               "objects. Map/filter/reduce followed.",
                "code_example": "list.stream()\n    .filter(x -> x > 0)\n    .map(x -> x * 2)\n    .collect(Collectors.toList())",
            },
        ],
        "travel_warnings": [
            "⚠️ Type erasure removes generic type information at runtime — List<String> and List<Integer> "
                               "are both just List at runtime",
            "⚠️ Checked exceptions force you to declare or catch — don't swallow exceptions silently",
            "⚠️ Immutable strings (String is immutable) — concatenating in loops creates many temporaries",
            "⚠️ NullPointerException was the original plague — use Optional<T> since Java 8",
        ],
        "local_customs": [
            "Greet with `public static void main(String[] args)` — the entry point ritual",
            "Semicolons end every statement — no exceptions",
            "Class names start with capital letters, methods with lowercase — CamelCase convention",
            "Checked exceptions must be declared in the method signature — deal with it or propagate it",
            "Use `Optional<T>` for potentially absent values since Java 8 — stop returning null",
        ],
        "era_treasures": [
            "🏆 The JVM — run anywhere, optimize later, massive ecosystem",
            "🏆 Checked exceptions — compile-time enforcement of error handling contracts",
            "🏆 Generics (with erasure) — compile-time type safety at a runtime cost",
            "🏆 Virtual threads (Java 21) — millions on a single machine",
            "🏆 The enterprise ecosystem — Spring, Hibernate, Maven/Gradle: everything is included",
        ],
        "visit_summary": "Java's era is the Object-Oriented Commonwealth — the language that proved "
                         "OO principles could work at scale. The JVM became the universal runtime "
                         "for 'write once, run anywhere,' and the enterprise ecosystem that grew "
                         "around it is unmatched in size and maturity.",
    },
    "C/C++": {
        "era_year": "1972 ERA — The Mechanical Age",
        "era_subtitle": "Total Control, Total Responsibility",
        "birthplace": "Bell Labs, Murray Hill",
        "founding_rationale": "The Mechanical Age began when Dennis Ritchie created C as a "
                               "tool for writing the Unix operating system. It gave programmers "
                               "total control over memory, hardware, and performance — with "
                               "absolutely no safety net. C++ extended this with classes and "
                               "templates, creating the most powerful and most dangerous language "
                               "in common use.",
        "landmarks": [
            {
                "name": "The Pointer Mines",
                "ascii": [
                    "  ┌─────────────────────────────┐",
                    "  │      THE POINTER MINES      │",
                    "  ├─────────────────────────────┤",
                    "  │                              │",
                    "  │  int x = 10;                │",
                    "  │  int *p = &x;               │",
                    "  │                              │",
                    "  │  *p    → dereference         │",
                    "  │  p     → address value       │",
                    "  │  &x    → address of x        │",
                    "  │                              │",
                    "  │  ⚠️  NULL = segfault        │",
                    "  │  ⚠️  wild pointer = UB       │",
                    "  │                              │",
                    "  └─────────────────────────────┘",
                ],
            },
            {
                "name": "The RAII Fortress",
                "ascii": [
                    "  ╔══════════════════════════════╗",
                    "  ║     RAII FORTRESS            ║",
                    "  ╠══════════════════════════════╣",
                    "  ║                               ║",
                    "  ║  class FileGuard {            ║",
                    "  ║    FILE *f;                  ║",
                    "  ║  public:                     ║",
                    "  ║    FileGuard(name) {          ║",
                    "  ║      f = fopen(name);        ║",
                    "  ║    }                         ║",
                    "  ║    ~FileGuard() {             ║",
                    "  ║      fclose(f); // always!   ║",
                    "  ║    }                         ║",
                    "  ║  };                          ║",
                    "  ║                               ║",
                    "  ╚══════════════════════════════╝",
                ],
            },
            {
                "name": "The Template Metaprogram Lab",
                "ascii": [
                    "  ┌─────────────────────────────────┐",
                    "  │  TEMPLATE METAPROGRAM LAB      │",
                    "  ├─────────────────────────────────┤",
                    "  │                                  │",
                    "  │  template<int N>                 │",
                    "  │  struct Factorial {              │",
                    "  │    enum { value = N *            │",
                    "  │         Factorial<N-1>::value }; │",
                    "  │  };                             │",
                    "  │                                  │",
                    "  │  template<>                      │",
                    "  │  struct Factorial<0> {           │",
                    "  │    enum { value = 1 };           │",
                    "  │  };                             │",
                    "  │                                  │",
                    "  │  Factorial<5>::value // = 120   │",
                    "  │                                  │",
                    "  └─────────────────────────────────┘",
                ],
            },
        ],
        "cultural_artifacts": [
            {
                "artifact_id": "raw_allocation",
                "name": "Raw Allocation Tablet",
                "description": "The founding document of C memory management — malloc and free, "
                               "new and delete. Every allocation must be matched by a deallocation. "
                               "The programmer is the memory manager.",
                "code_example": "int *arr = (int *)malloc(n * sizeof(int));\n// ... use arr ...\nfree(arr); // or: delete[] arr",
            },
            {
                "artifact_id": "virtual_dispatch",
                "name": "Virtual Dispatch Mechanism",
                "description": "Virtual functions enable runtime polymorphism — the vtable "
                               "dispatches the correct method at runtime based on the actual "
                               "type of the object, not the pointer type.",
                "code_example": "class Shape {\npublic:\n    virtual void draw() = 0; // pure virtual",
            },
        ],
        "travel_warnings": [
            "⚠️ Buffer overflows are the #1 security vulnerability — never write past the end of an array",
            "⚠️ Use-after-free is a ghost that haunts production — use ASan or Valgrind to detect it",
            "⚠️ Undefined behavior means the compiler can do ANYTHING — including things that seem to work",
            "⚠️ Raw pointers have no ownership semantics — who deletes this? Document it or use smart pointers",
        ],
        "local_customs": [
            "Greet with `#include <header.h>` — the preprocessor sets the stage",
            "Header files (.h) declare; source files (.cpp/.c) define — separation of interface/implementation",
            "Always initialize variables — uninitialized memory contains garbage",
            "Use `std::vector` instead of raw arrays in C++ — bounds-checked access when using `.at()`",
            "Prefer `std::unique_ptr` and `std::shared_ptr` over raw `new`/`delete` — RAII is your friend",
        ],
        "era_treasures": [
            "🏆 Total hardware control — direct memory access, pointer arithmetic, inline assembly",
            "🏆 Zero overhead abstractions — templates are compile-time, no runtime cost",
            "🏆 RAII — resource management tied to object lifetime, exception-safe",
            "🏆 The STL — containers, algorithms, iterators: battle-tested standard library",
            "🏆 Deterministic resource management — you decide when everything is allocated/deallocated",
        ],
        "visit_summary": "C/C++'s era is the Mechanical Age — total control, total responsibility. "
                         "Every system that matters runs on C or C++: operating systems, databases, "
                         "browsers, game engines, embedded firmware. There is no safety net. "
                         "When you write in C/C++, you ARE the operating system.",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Timeline waypoints — for drawing the ASCII journey line
# ─────────────────────────────────────────────────────────────────────────────

TIMELINE_WAYPOINTS: List[str] = [
    "1972│ C is born at Bell Labs ─ Unix is written in C ─",
    "1983│ C++ arrives: 'C with Classes' → objects ───────",
    "1995│ Java: WORA • JavaScript: Netscape's 10-day hack",
    "2009│ Go: Google's simplicity uprising ───────────────",
    "2011│ Kotlin: JetBrains pragmatic modernization ───────",
    "2012│ TypeScript: MS adds types to JS ───────────────",
    "2014│ Swift: Apple safety + elegance renaissance ─────",
    "2015│ Rust: Mozilla's safety reformation ────────────",
]


# ─────────────────────────────────────────────────────────────────────────────
# Rotation helpers
# ─────────────────────────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    """Load language rotation config."""
    with open(_ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    """Save updated rotation config."""
    with open(_ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def get_current_language(config: Dict[str, Any]) -> Tuple[str, int]:
    """Return (language, index) for current rotation position."""
    languages = config["languages"]
    idx = config.get("current_index", 0)
    return languages[idx % len(languages)], idx


def advance_rotation(config: Dict[str, Any]) -> None:
    """Advance current_index by 1, wrapping at list length."""
    languages = config["languages"]
    config["current_index"] = (config.get("current_index", 0) + 1) % len(languages)


# ─────────────────────────────────────────────────────────────────────────────
# Core API
# ─────────────────────────────────────────────────────────────────────────────

def odyssey(rotate: bool = True, language: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate an odyssey journey report for the current rotation language.

    Args:
        rotate: if True, advance rotation after selecting (default behavior).
                If False, just report without advancing (for testing).
        language: override the language selection (for testing).

    Returns:
        dict with full journey report
    """
    config = load_rotation()
    languages = config.get("languages", [])
    if not languages:
        raise ValueError("No languages found in rotation config")

    if language is not None:
        # Override: don't rotate, just use specified language
        selected_lang = language
        lang_idx = languages.index(selected_lang)
        # Don't advance
    else:
        selected_lang, lang_idx = get_current_language(config)
        if rotate:
            advance_rotation(config)
            config["last_language"] = selected_lang
            config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
            save_rotation(config)

    era = LANGUAGE_ERAS.get(selected_lang, LANGUAGE_ERAS["Rust"])

    # Determine next language for the journey preview
    next_idx = (lang_idx + 1) % len(languages)
    next_lang = languages[next_idx]

    # Build result
    result = {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": selected_lang,
        "selected_era": era["era_year"],
        "era_subtitle": era["era_subtitle"],
        "birthplace": era["birthplace"],
        "founding_rationale": era["founding_rationale"],
        "landmarks": era["landmarks"],
        "cultural_artifacts": era["cultural_artifacts"],
        "travel_warnings": era["travel_warnings"],
        "local_customs": era["local_customs"],
        "era_treasures": era["era_treasures"],
        "visit_summary": era["visit_summary"],
        "timeline_waypoints": TIMELINE_WAYPOINTS,
        "current_position": lang_idx,
        "rotation_order": languages,
        "next_language": next_lang,
        "next_era": LANGUAGE_ERAS.get(next_lang, {}).get("era_year", "Unknown"),
        "rotation_updated": rotate,
    }
    return result


def format_odyssey_report(report: Dict[str, Any]) -> str:
    """Format the odyssey report as a readable ASCII travel journal."""
    lines: List[str] = []
    lang = report["selected_language"]
    era = report["selected_era"]
    subtitle = report["era_subtitle"]

    # Header
    lines.append("╔══════════════════════════════════════════════════════════════════╗")
    lines.append("║  🚀 POLYGLOT ODYSSEY — A Time-Travel Journey Through Language   ║")
    lines.append("╠══════════════════════════════════════════════════════════════════╣")
    lines.append(f"║  Destination: {lang:<52}║")
    lines.append(f"║  Era:         {era:<52}║")
    lines.append(f"║  Subtitle:    {subtitle:<52}║")
    lines.append("╠══════════════════════════════════════════════════════════════════╣")
    lines.append("║  📍 ORIGIN                                                   ║")
    lines.append(f"║  Birthplace: {report['birthplace']:<50}║")
    lines.append("╠══════════════════════════════════════════════════════════════════╣")
    lines.append("║  📜 FOUNDING RATIONALE                                        ║")
    rationale = report["founding_rationale"]
    # Wrap rationale at 60 chars
    words = rationale.split()
    line = "║  "
    for word in words:
        if len(line) + len(word) + 1 > 62:
            lines.append(line + " " * (62 - len(line)) + "║")
            line = "║  " + word
        else:
            line += " " + word if line != "║  " else word
    if line != "║  ":
        lines.append(line + " " * (62 - len(line)) + "║")
    lines.append("╠══════════════════════════════════════════════════════════════════╣")
    lines.append("║  🗺️  LANDMARKS                                               ║")
    for landmark in report["landmarks"]:
        lines.append(f"║  ── {landmark['name']} ──────────────────────────────║")
        for art_line in landmark["ascii"]:
            lines.append(f"║    {art_line:<57}║")
    lines.append("╠══════════════════════════════════════════════════════════════════╣")
    lines.append("║  🏛️  CULTURAL ARTIFACTS (Museum Exhibits)                      ║")
    for artifact in report["cultural_artifacts"]:
        lines.append(f"║  ── {artifact['name']} ────────────────────────────────║")
        desc_words = artifact["description"].split()
        line = "║    "
        for word in desc_words:
            if len(line) + len(word) + 1 > 62:
                lines.append(line + " " * (62 - len(line)) + "║")
                line = "║    " + word
            else:
                line += " " + word if line != "║    " else word
        if line != "║    ":
            lines.append(line + " " * (62 - len(line)) + "║")
        code_lines = artifact["code_example"].split("\n")
        for code_line in code_lines:
            lines.append(f"║      {code_line:<55}║")
    lines.append("╠══════════════════════════════════════════════════════════════════╣")
    lines.append("║  ⚠️  TRAVEL WARNINGS                                          ║")
    for warning in report["travel_warnings"]:
        lines.append(f"║  {warning:<59}║")
    lines.append("╠══════════════════════════════════════════════════════════════════╣")
    lines.append("║  🤝 LOCAL CUSTOMS                                             ║")
    for custom in report["local_customs"]:
        lines.append(f"║  • {custom:<56}║")
    lines.append("╠══════════════════════════════════════════════════════════════════╣")
    lines.append("║  💎 ERA TREASURES (Collect Them All!)                          ║")
    for treasure in report["era_treasures"]:
        lines.append(f"║  {treasure:<59}║")
    lines.append("╠══════════════════════════════════════════════════════════════════╣")
    lines.append("║  📖 VISIT SUMMARY                                              ║")
    summary_words = report["visit_summary"].split()
    line = "║  "
    for word in summary_words:
        if len(line) + len(word) + 1 > 62:
            lines.append(line + " " * (62 - len(line)) + "║")
            line = "║  " + word
        else:
            line += " " + word if line != "║  " else word
    if line != "║  ":
        lines.append(line + " " * (62 - len(line)) + "║")
    lines.append("╠══════════════════════════════════════════════════════════════════╣")
    lines.append("║  🕰️  TIMELINE WAYPOINTS                                        ║")
    for wp in report["timeline_waypoints"]:
        lines.append(f"║  • {wp:<57}║")
    lines.append("╠══════════════════════════════════════════════════════════════════╣")
    lines.append("║  🔄 ROTATION ORDER                                              ║")
    rotation_str = " → ".join(report["rotation_order"])
    lines.append(f"║  {rotation_str:<59}║")
    lines.append(f"║  Next up: {report['next_language']} ({report['next_era']}){' ' * max(0, 28 - len(report['next_language']))}║")
    lines.append("╚══════════════════════════════════════════════════════════════════╝")
    return "\n".join(lines)


def run_tests() -> None:
    """Run all tests for the polyglot_odyssey module."""
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

    print("🚀 Polyglot Odyssey — Running Tests\n")

    # ── Rotation file ─────────────────────────────────────────────────────────
    try:
        config = load_rotation()
        t("load_rotation() returns valid dict", isinstance(config, dict))
        t("rotation has 'languages' key", "languages" in config)
        t("rotation has 'current_index' key", "current_index" in config)
        t("rotation has exactly 8 languages", len(config["languages"]) == 8)
        expected = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
        t("rotation languages match expected order", config["languages"] == expected)
    except Exception as e:
        t("load_rotation() succeeds", False, str(e))

    # ── LANGUAGE_ERAS completeness ────────────────────────────────────────────
    for lang in ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]:
        t(f"LANGUAGE_ERAS has '{lang}'", lang in LANGUAGE_ERAS)
        era = LANGUAGE_ERAS[lang]
        t(f"  '{lang}' has era_year", "era_year" in era)
        t(f"  '{lang}' has era_subtitle", "era_subtitle" in era)
        t(f"  '{lang}' has birthplace", "birthplace" in era)
        t(f"  '{lang}' has founding_rationale", "founding_rationale" in era)
        t(f"  '{lang}' has landmarks", "landmarks" in era)
        t(f"  '{lang}' has cultural_artifacts", "cultural_artifacts" in era)
        t(f"  '{lang}' has travel_warnings", "travel_warnings" in era)
        t(f"  '{lang}' has local_customs", "local_customs" in era)
        t(f"  '{lang}' has era_treasures", "era_treasures" in era)
        t(f"  '{lang}' has visit_summary", "visit_summary" in era)
        t(f"  '{lang}' has at least 3 landmarks", len(era["landmarks"]) >= 3)
        t(f"  '{lang}' has at least 2 artifacts", len(era["cultural_artifacts"]) >= 2)
        t(f"  '{lang}' has at least 3 travel_warnings", len(era["travel_warnings"]) >= 3)
        t(f"  '{lang}' has at least 3 local_customs", len(era["local_customs"]) >= 3)
        t(f"  '{lang}' has at least 3 era_treasures", len(era["era_treasures"]) >= 3)
        for lm in era["landmarks"]:
            t(f"  '{lang}' landmark '{lm['name']}' has 'ascii' list", "ascii" in lm and isinstance(lm["ascii"], list))
            t(f"  '{lang}' landmark '{lm['name']}' has non-empty ascii", "ascii" in lm and len(lm["ascii"]) > 0)
        for art in era["cultural_artifacts"]:
            t(f"  '{lang}' artifact '{art['artifact_id']}' has code_example", "code_example" in art)
            t(f"  '{lang}' artifact '{art['artifact_id']}' has description", "description" in art)

    # ── TIMELINE_WAYPOINTS ────────────────────────────────────────────────────
    t("TIMELINE_WAYPOINTS is non-empty list", isinstance(TIMELINE_WAYPOINTS, list) and len(TIMELINE_WAYPOINTS) > 0)
    t("TIMELINE_WAYPOINTS has 8 entries (one per language)", len(TIMELINE_WAYPOINTS) == 8)

    # ── odyssey() rotation behavior ────────────────────────────────────────────
    try:
        config_before = load_rotation()
        idx_before = config_before["current_index"]
        lang_before = config_before["languages"][idx_before]

        result = odyssey(rotate=True)
        config_after = load_rotation()
        idx_after = config_after["current_index"]

        t("odyssey(rotate=True) advances current_index by 1",
          idx_after == (idx_before + 1) % 8)
        t("odyssey(rotate=True) returns selected_language", "selected_language" in result)
        t("odyssey(rotate=True) returns correct selected_language",
          result["selected_language"] == lang_before)
        t("odyssey(rotate=True) returns next_language", "next_language" in result)
        t("odyssey(rotate=True) returns era_treasures", "era_treasures" in result)
        t("odyssey(rotate=True) returns landmarks", "landmarks" in result)
        t("odyssey(rotate=True) returns cultural_artifacts", "cultural_artifacts" in result)
        t("odyssey(rotate=True) returns travel_warnings", "travel_warnings" in result)
        t("odyssey(rotate=True) returns local_customs", "local_customs" in result)
        t("odyssey(rotate=True) returns timeline_waypoints", "timeline_waypoints" in result)
    except Exception as e:
        t("odyssey(rotate=True) runs without error", False, str(e))

    # ── odyssey(rotate=False) does not advance ─────────────────────────────────
    try:
        config_before = load_rotation()
        idx_before = config_before["current_index"]
        result = odyssey(rotate=False, language="Rust")
        config_after = load_rotation()
        idx_after = config_after["current_index"]
        t("odyssey(rotate=False) does not advance current_index",
          idx_after == idx_before)
        t("odyssey(rotate=False, language=X) returns specified language",
          result["selected_language"] == "Rust")
    except Exception as e:
        t("odyssey(rotate=False) test", False, str(e))

    # ── All languages can be odysseyd ──────────────────────────────────────────
    for lang in config["languages"]:
        try:
            result = odyssey(rotate=False, language=lang)
            t(f"odyssey(language='{lang}') succeeds", True)
            t(f"  returns '{lang}' as selected_language",
              result["selected_language"] == lang)
            t(f"  has era_year", len(result["selected_era"]) > 0)
            t(f"  has era_subtitle", len(result["era_subtitle"]) > 0)
            t(f"  has founding_rationale", len(result["founding_rationale"]) > 10)
            t(f"  has visit_summary", len(result["visit_summary"]) > 10)
            t(f"  has at least 3 landmarks", len(result["landmarks"]) >= 3)
            t(f"  has at least 2 cultural_artifacts", len(result["cultural_artifacts"]) >= 2)
        except Exception as e:
            t(f"odyssey(language='{lang}')", False, str(e))

    # ── format_odyssey_report ──────────────────────────────────────────────────
    try:
        result = odyssey(rotate=False, language="Rust")
        formatted = format_odyssey_report(result)
        t("format_odyssey_report() returns a string", isinstance(formatted, str))
        t("format_odyssey_report() starts with box char", formatted.startswith("╔"))
        t("format_odyssey_report() ends with box char", formatted.rstrip().endswith("╝"))
        t("format_odyssey_report() contains 'Rust'", "Rust" in formatted)
        t("format_odyssey_report() contains 'ODYSSEY'", "ODYSSEY" in formatted)
        t("format_odyssey_report() contains 'TIMELINE'", "TIMELINE" in formatted)
        t("format_odyssey_report() contains 'TREASURES'", "TREASURES" in formatted)
        t("format_odyssey_report() contains 'WARNINGS'", "WARNINGS" in formatted)
    except Exception as e:
        t("format_odyssey_report()", False, str(e))

    # ── Tool name and version ──────────────────────────────────────────────────
    result = odyssey(rotate=False, language="Rust")
    t("TOOL_NAME is 'polyglot-odyssey'", TOOL_NAME == "polyglot-odyssey")
    t("TOOL_VERSION is '1.0.0'", TOOL_VERSION == "1.0.0")
    t("Result contains correct tool name", result["tool"] == "polyglot-odyssey")
    t("Result contains correct version", result["version"] == "1.0.0")

    # ── Rotation order in result ───────────────────────────────────────────────
    config = load_rotation()
    result = odyssey(rotate=False, language="Rust")
    t("Result contains rotation_order", "rotation_order" in result)
    t("rotation_order matches config", result["rotation_order"] == config["languages"])

    print(f"\n{'='*55}")
    if errors:
        print(f"❌ {len(errors)} test(s) failed:")
        for e in errors:
            print(f"   - {e}")
        sys.exit(1)
    else:
        print(f"✅ All {passed} tests passed! The odyssey awaits.")
        sys.exit(0)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        result = odyssey(rotate=True)
        print(format_odyssey_report(result))
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        result = odyssey(rotate=True)
        print(json.dumps(result, indent=2))
    else:
        print(f"🚀 Polyglot Odyssey v{TOOL_VERSION}")
        print("  A time-travel journey through programming language history.")
        print("")
        print("Usage:")
        print("  python -m polyglot_odyssey --test    # Run all tests")
        print("  python -m polyglot_odyssey --report  # Generate journey report")
        print("  python -m polyglot_odyssey --json    # JSON output")
