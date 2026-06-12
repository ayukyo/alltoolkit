#!/usr/bin/env python3
"""
🛰️ Polyglot Signal v1.0

Signal Semantics Cartography — maps how each programming language signals
conditions to the programmer: errors, warnings, absence, state, and
concurrency. Every language has a different "signal vocabulary."

Creative concept: "Every language has a different alarm system.
Rust has Result, Go has error values, Java has checked exceptions,
JavaScript has throw/try/catch, Swift has throws, Kotlin has Result,
TypeScript erases types at runtime... they're all signaling the same
universal conditions, just in different dialects."

This tool selects the current rotation language and maps its signal taxonomy:
- What does an ERROR signal look like?
- What does ABSENCE/NULL signal look like?
- What does a WARNING signal look like?
- What does a SUCCESS/OK signal look like?
- What does a CONCURRENCY/ASYNC signal look like?

Each signal category shows how the current language's approach compares
to all other languages in the rotation — creating a "signal vocabulary map."

Distinct from existing tools:
  - polyglot_resonator:  how each language THINKS (mental models)
  - polyglot_digest:      syntax-parallel code (same code, different syntax)
  - polyglot_translation: cultural idioms/proverbs (social cargo)
  - polyglot_chronology:  geological/evolutionary timeline (deep time)
  - polyglot_forge:       language alloy pairing (compatibility)

Signal is about HOW LANGUAGES COMMUNICATE with the programmer —
the signal vocabulary itself, what triggers each signal, and how
the programmer responds to it.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-signal"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent.parent  # polyglot_signal/
_WORKSPACE_ROOT = _MODULE_DIR.parent              # AllToolkit/ -> workspace/
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]


# ─────────────────────────────────────────────────────────────────────────────
# Signal Category Database
# ─────────────────────────────────────────────────────────────────────────────
# Each language has 5 signal categories:
#   error        — how the language signals failure/exceptional conditions
#   absence      — how the language signals "no value" / null / undefined
#   warning      — how the language signals "dangerous but allowed"
#   success      — how the language signals "everything is fine"
#   async        — how the language signals "happens later"

SIGNAL_DB: Dict[str, Dict[str, Dict[str, Any]]] = {

    "Rust": {
        "error": {
            "signal": "Result<T, E>",
            "mechanism": "Result<T, E> enum — Ok(T) or Err(E). No exceptions. The ? operator propagates.",
            "idiom": "let f = File::open(\"data\")?; // returns Err if failed, Ok if succeeded",
            "key_traits": ["compile-time checked", "no hidden exceptions", "exhaustive matching"],
            "signal_tag": "PROVEN",
            "emoji": "🛡️",
        },
        "absence": {
            "signal": "Option<T>",
            "mechanism": "Option<T> enum — Some(T) or None. Forces handling via match/if let.",
            "idiom": "let name: Option<String> = map.get(\"key\"); match name { Some(n) => ..., None => ... }",
            "key_traits": ["compile-time enforced", "no null pointer exception", "exhaustive"],
            "signal_tag": "PROVEN",
            "emoji": "🛡️",
        },
        "warning": {
            "signal": "Compiler warnings + #[deprecated]",
            "mechanism": "Compiler emits warnings for unused variables, incorrect types, deprecated APIs. Warnings are non-fatal.",
            "idiom": "#[deprecated(note = \"use new_api instead\")] fn old_api() {}",
            "key_traits": ["compile-time enforced", "non-fatal", "lint can promote to error"],
            "signal_tag": "PROVEN",
            "emoji": "🛡️",
        },
        "success": {
            "signal": "Ok(()) / unit type",
            "mechanism": "Operations that succeed return Ok(()) or just () — the unit type signals completion.",
            "idiom": "fn save() -> Result<(), io::Error> { write()?; Ok(()) }",
            "key_traits": ["explicit success type", "unit type = no meaningful value", "Result<Ok, Err>"],
            "signal_tag": "PROVEN",
            "emoji": "🛡️",
        },
        "async": {
            "signal": "async/await + Future<T>",
            "mechanism": "async fn returns a Future. .await suspends execution. No callback hell.",
            "idiom": "async fn fetch(url: &str) -> Result<String, reqwest::Error> { let resp = reqwest::get(url).await?; resp.text().await }",
            "key_traits": ["zero-cost abstraction", "native syntax", "no callback pyramid"],
            "signal_tag": "PROVEN",
            "emoji": "🛡️",
        },
    },

    "Go": {
        "error": {
            "signal": "error interface",
            "mechanism": "Multiple return values — last return is (error). nil means success, non-nil means failure.",
            "idiom": "f, err := os.Open(\"data\"); if err != nil { return err } // explicit nil check",
            "key_traits": ["explicit return value", "no exceptions", "error is a plain interface"],
            "signal_tag": "NOMINAL",
            "emoji": "⚡",
        },
        "absence": {
            "signal": "(T, ok) map lookup + nil for zero values",
            "mechanism": "Map returns (value, ok). Zero value for types (0, \"\", nil) is indistinguishable from absence without the ok check.",
            "idiom": "val, ok := myMap[key]; if !ok { /* key not present */ }",
            "key_traits": ["two-value map lookup", "zero value ambiguity", "explicit ok pattern"],
            "signal_tag": "NOMINAL",
            "emoji": "⚡",
        },
        "warning": {
            "signal": "Compiler warnings + golint",
            "mechanism": "Compiler warns on unreachable code, unused variables. golint enforces style + some safety.",
            "idiom": "//go:generate ./script.sh // directive for tooling, not a warning",
            "key_traits": ["compile-time warnings", "golint for style", "no implicit casts"],
            "signal_tag": "NOMINAL",
            "emoji": "⚡",
        },
        "success": {
            "signal": "nil error return",
            "mechanism": "A function succeeds by returning nil as the error. No special success type.",
            "idiom": "func save() error { if err := write(); err != nil { return err }; return nil }",
            "key_traits": ["nil = success", "error type is plain interface", "no Result wrapper"],
            "signal_tag": "NOMINAL",
            "emoji": "⚡",
        },
        "async": {
            "signal": "goroutines + channels",
            "mechanism": "go func() {} spawns a lightweight thread. Channels communicate. select waits on multiple channels.",
            "idiom": "ch := make(chan Result); go func() { ch <- doWork() }(); select { case r := <-ch: handle(r) }",
            "key_traits": ["cheap threads", "CSP communication", "no async keyword"],
            "signal_tag": "NOMINAL",
            "emoji": "⚡",
        },
    },

    "Swift": {
        "error": {
            "signal": "throws + Error protocol",
            "mechanism": "Functions marked throws produce errors conforming to Error protocol. try/catch handles them.",
            "idiom": "func read() throws { try FileManager.default.contents(atPath: \"data\") } do { try read() } catch { print(error) }",
            "key_traits": ["typed throws (Swift 5.20+)", "exhaustive catch blocks", "no unchecked exceptions"],
            "signal_tag": "PROVEN",
            "emoji": "🏔️",
        },
        "absence": {
            "signal": "Optional<T>",
            "mechanism": "Optional<T> — nil means absence. if let / guard let unwrap safely.",
            "idiom": "guard let name = user.name else { return } // name is String here",
            "key_traits": ["compile-time nil safety", "if let / guard let", "optional chaining (?.)"],
            "signal_tag": "PROVEN",
            "emoji": "🏔️",
        },
        "warning": {
            "signal": "Compiler warnings + #deprecated",
            "mechanism": "@available + #deprecated attribute. Lint can elevate warnings to errors.",
            "idiom": "@available(macOS 12.0, *) // gate API; #deprecated message shows in editor",
            "key_traits": ["platform availability gates", "deprecation attributes", "strict mode"],
            "signal_tag": "PROVEN",
            "emoji": "🏔️",
        },
        "success": {
            "signal": "Void / () — no error thrown",
            "mechanism": "A throws function succeeds by returning normally (no error thrown). No Result needed.",
            "idiom": "func save() throws { try writeSomething(); } // caller uses try (no catch = success path)",
            "key_traits": ["no thrown error = success", "Void return type", "Result<T, Error> available too"],
            "signal_tag": "PROVEN",
            "emoji": "🏔️",
        },
        "async": {
            "signal": "async/await + actors (Swift 6)",
            "mechanism": "async functions suspend without blocking threads. actors isolate state. Sendable marks safe transfers.",
            "idiom": "actor Counter { private var count = 0; func increment() async { count += 1 } }",
            "key_traits": ["structured concurrency", "actor isolation", "Swift 6: data race safety"],
            "signal_tag": "PROVEN",
            "emoji": "🏔️",
        },
    },

    "Kotlin": {
        "error": {
            "signal": "exceptions (unchecked) + Result<T>",
            "mechanism": "Kotlin has no checked exceptions. Exceptions are unchecked. Result<T> (or runCatching) for type-safe error handling.",
            "idiom": "val result = runCatching { riskyOperation() }; result.onFailure { println(it) }",
            "key_traits": ["no checked exceptions", "Result<T> for typed errors", "nullable Result"],
            "signal_tag": "ADAPTED",
            "emoji": "🟣",
        },
        "absence": {
            "signal": "Nullable type (T?)",
            "mechanism": "Type suffix ? means nullable. Elvis operator (?:) provides default. Safe call (?.) for chaining.",
            "idiom": "val len: Int? = str?.length ?: 0 // safe call + elvis default",
            "key_traits": ["compile-time null safety", "elvis operator", "not null assertion (!!)"],
            "signal_tag": "PROVEN",
            "emoji": "🟣",
        },
        "warning": {
            "signal": "Compiler warnings + @Deprecated annotation",
            "mechanism": "@Deprecated marks APIs that should not be used. Replacement API can be specified.",
            "idiom": "@Deprecated(\"Use newApi() instead\", ReplaceWith(\"newApi()\"))",
            "key_traits": ["replacement hint in annotation", "Warning as error possible", "lint via ktlint"],
            "signal_tag": "ADAPTED",
            "emoji": "🟣",
        },
        "success": {
            "signal": "Unit return or explicit Result.success",
            "mechanism": "Functions without a return type return Unit. Result<T> uses Result.success(value).",
            "idiom": "fun save(): Result<Unit> = runCatching { doStuff() }.onSuccess { println(\"OK\") }",
            "key_traits": ["Unit = void equivalent", "Result.success / Result.failure", "onSuccess callback"],
            "signal_tag": "ADAPTED",
            "emoji": "🟣",
        },
        "async": {
            "signal": "coroutines + Flow",
            "mechanism": "suspend functions pause without blocking threads. Channels and Flow for async streams.",
            "idiom": "launch { val data = async { fetch() }.await(); channel.send(data) }",
            "key_traits": ["structured concurrency", "Flow for reactive streams", "Dispatchers control threading"],
            "signal_tag": "ADAPTED",
            "emoji": "🟣",
        },
    },

    "TypeScript": {
        "error": {
            "signal": "throw + try/catch (type-erased)",
            "mechanism": "throw can throw any value. No type-safe error declarations. TypeScript types are erased at runtime.",
            "idiom": "try { JSON.parse(input) } catch (e: unknown) { if (e instanceof SyntaxError) handle(e) }",
            "key_traits": ["throw any type", "no typed throws", "unknown type forces narrowing"],
            "signal_tag": "ADAPTED",
            "emoji": "🔷",
        },
        "absence": {
            "signal": "undefined | null + optional chaining",
            "mechanism": "undefined and null are distinct. Optional chaining (?.) and nullish coalescing (??) handle absence.",
            "idiom": "const len: number | undefined = obj?.data?.length ?? 0",
            "key_traits": ["optional chaining (?.)", "nullish coalescing (??)", "strict null checks mode"],
            "signal_tag": "ADAPTED",
            "emoji": "🔷",
        },
        "warning": {
            "signal": "tsc warnings + eslint-disable comments",
            "mechanism": "TypeScript compiler warns on type mismatches. @ts-ignore / @ts-check control strictness.",
            "idiom": "// @ts-expect-error — suppress error for known incompatibility",
            "key_traits": ["tsconfig strict mode", "@ts-ignore for suppression", "no deprecated keyword"],
            "signal_tag": "ADAPTED",
            "emoji": "🔷",
        },
        "success": {
            "signal": "normal return (no exception thrown)",
            "mechanism": "A function succeeds by returning normally. No type distinguishes success from failure.",
            "idiom": "function parse(input: string): Record<string, number> { return JSON.parse(input) }",
            "key_traits": ["no success type", "runtime-only errors", "Promise resolves to success value"],
            "signal_tag": "ADAPTED",
            "emoji": "🔷",
        },
        "async": {
            "signal": "Promise + async/await",
            "mechanism": "async functions return Promise<T>. await suspends on the event loop. Promise.all for concurrency.",
            "idiom": "const [a, b] = await Promise.all([fetchA(), fetchB()])",
            "key_traits": ["single-threaded event loop", "Promise.all for parallel", "no true parallelism without Workers"],
            "signal_tag": "ADAPTED",
            "emoji": "🔷",
        },
    },

    "JavaScript": {
        "error": {
            "signal": "throw + try/catch",
            "mechanism": "throw can throw any value. Unhandled promise rejections are silent failures.",
            "idiom": "throw new Error('something went wrong'); // best practice — throw Error objects",
            "key_traits": ["throw any type", "unhandled rejection risk", "no compile-time checking"],
            "signal_tag": "RUNTIME",
            "emoji": "🟨",
        },
        "absence": {
            "signal": "undefined + null (two distinct absence values)",
            "mechanism": "undefined = uninitialized/missing. null = explicitly empty. typeof lies about null.",
            "idiom": "if (value === null || value === undefined) { /* absence */ }",
            "key_traits": ["typeof null === 'object' (historical bug)", "== vs === difference on null", "void 0 === undefined"],
            "signal_tag": "RUNTIME",
            "emoji": "🟨",
        },
        "warning": {
            "signal": "console.warn + runtime warnings",
            "mechanism": "console.warn is the warning mechanism. No compile-time warnings. Lint (ESLint) fills the gap.",
            "idiom": "console.warn('This API is deprecated: use newApi() instead')",
            "key_traits": ["runtime only", "ESLint for static analysis", "no first-class deprecated keyword"],
            "signal_tag": "RUNTIME",
            "emoji": "🟨",
        },
        "success": {
            "signal": "normal return (no exception thrown)",
            "mechanism": "A function succeeds by returning normally. No type distinguishes it.",
            "idiom": "function getData() { return fetchedData; } // success is implicit",
            "key_traits": ["implicit success", "Promise.resolve() for async", "no success type"],
            "signal_tag": "RUNTIME",
            "emoji": "🟨",
        },
        "async": {
            "signal": "Promise + event loop",
            "mechanism": "Single-threaded event loop. Promises queue microtasks. setTimeout queues macrotasks.",
            "idiom": "setTimeout(() => console.log('later'), 0); console.log('now'); // 'now' first",
            "key_traits": ["single-threaded", "microtask queue (Promise)", "macrotask queue (setTimeout)"],
            "signal_tag": "RUNTIME",
            "emoji": "🟨",
        },
    },

    "Java": {
        "error": {
            "signal": "checked + unchecked exceptions",
            "mechanism": "Checked exceptions are declared in method signature (throws). Compiler enforces handling.",
            "idiom": "public void read() throws IOException { ... } // caller MUST handle or propagate",
            "key_traits": ["compiler-enforced", "throws in signature", "checked = recoverable, unchecked = fatal"],
            "signal_tag": "PROVEN",
            "emoji": "☕",
        },
        "absence": {
            "signal": "null (no language-level null safety) + java.util.Optional",
            "mechanism": "null is the absence signal. No built-in null safety. Optional<T> (Java 8+) provides a typesafe alternative.",
            "idiom": "Optional<String> name = Optional.ofNullable(getName()); name.ifPresent(System.out::println)",
            "key_traits": ["null as absence (unsafe)", "Optional<T> as typesafe alternative", "null-check idiom"],
            "signal_tag": "ADAPTED",
            "emoji": "☕",
        },
        "warning": {
            "signal": "Compiler warnings (@Deprecated annotation)",
            "mechanism": "@Deprecated marks APIs for removal. @SuppressWarnings suppresses specific warnings.",
            "idiom": "@Deprecated(since = \"1.8\", forRemoval = true) // marked for future removal",
            "key_traits": ["@Deprecated annotation", "forRemoval=true flags eventual removal", "@SuppressWarnings"],
            "signal_tag": "PROVEN",
            "emoji": "☕",
        },
        "success": {
            "signal": "normal return (no exception thrown)",
            "mechanism": "A function succeeds by returning normally. No special success type.",
            "idiom": "public int add(int a, int b) { return a + b; } // success is implicit",
            "key_traits": ["implicit success", "void methods return nothing", "no Result wrapper"],
            "signal_tag": "PROVEN",
            "emoji": "☕",
        },
        "async": {
            "signal": "CompletableFuture + virtual threads (Java 21+)",
            "mechanism": "CompletableFuture for async pipelines. Virtual threads make threads cheap.",
            "idiom": "CompletableFuture.supplyAsync(() -> compute()).thenApply(x -> x * 2).join()",
            "key_traits": ["virtual threads (Java 21+)", "CompletableFuture composable", "ExecutorService for thread pools"],
            "signal_tag": "PROVEN",
            "emoji": "☕",
        },
    },

    "C/C++": {
        "error": {
            "signal": "return codes + errno (C) | exceptions (C++)",
            "mechanism": "C uses return codes + global errno. C++ adds exceptions (rarely used in performance code).",
            "idiom": "FILE *f = fopen(\"data\", \"r\"); if (!f) { perror(\"fopen\"); return errno; }",
            "key_traits": ["no exceptions in C", "errno is global state", "C++ exceptions are opt-in"],
            "signal_tag": "RUNTIME",
            "emoji": "⚙️",
        },
        "absence": {
            "signal": "NULL macro (0) / nullptr (C++11)",
            "mechanism": "NULL is (void*)0 in C (type-punned) or 0. nullptr is type-safe null in C++. No Option type.",
            "idiom": "if (ptr == nullptr) { /* null check */ } // C++11 nullptr is type-safe",
            "key_traits": ["nullptr (C++11) vs NULL macro", "no Option/Result", "no null safety enforcement"],
            "signal_tag": "RUNTIME",
            "emoji": "⚙️",
        },
        "warning": {
            "signal": "Compiler warnings (-Wall -Wextra) + #pragma warning",
            "mechanism": "Compiler warnings for type mismatches, unused variables. #pragma warning controls specific warnings.",
            "idiom": "#pragma warning(push); #pragma warning(disable: 4996); // suppress specific warning",
            "key_traits": ["-Wall -Wextra flags", "#pragma for targeted suppression", "undefined behavior triggers no warning"],
            "signal_tag": "RUNTIME",
            "emoji": "⚙️",
        },
        "success": {
            "signal": "return code 0 / normal exit",
            "mechanism": "C: main() returns 0 for success, non-zero for error. Library functions return 0 for success (e.g. strstr returns non-null pointer).",
            "idiom": "int main() { if (do_work()) return 0; else return 1; } // 0 = success convention",
            "key_traits": ["0 = success convention", "non-zero = error convention", "no Result type"],
            "signal_tag": "RUNTIME",
            "emoji": "⚙️",
        },
        "async": {
            "signal": "std::thread + std::async + atomics",
            "mechanism": "std::thread for explicit threads. std::async wraps callable in a future. Atomics for lock-free.",
            "idiom": "auto fut = std::async(std::launch::async, [](){ return compute(); }); fut.get()",
            "key_traits": ["manual thread lifecycle", "futures for result passing", "std::atomic for lock-free"],
            "signal_tag": "RUNTIME",
            "emoji": "⚙️",
        },
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Signal strength classification
# ─────────────────────────────────────────────────────────────────────────────

def classify_signal_strength(signal_tag: str) -> str:
    """Classify the rigor of a signal system."""
    if signal_tag == "PROVEN":
        return "compile-time proven signal — compiler enforces correctness"
    elif signal_tag == "NOMINAL":
        return "compile-time enforced signal — but uses nominal types"
    elif signal_tag == "ADAPTED":
        return "runtime signal with compile-time annotations — hybrid"
    else:
        return "runtime-only signal — no compile-time enforcement"


# ─────────────────────────────────────────────────────────────────────────────
# Core API
# ─────────────────────────────────────────────────────────────────────────────

def _load_rotation(config_path: Optional[str] = None) -> Dict[str, Any]:
    path = config_path if config_path is not None else ROTATION_FILE
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_rotation(data: Dict[str, Any], config_path: Optional[str] = None) -> None:
    path = config_path if config_path is not None else ROTATION_FILE
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def get_current_language(config_path: Optional[str] = None) -> str:
    """Return the language at current_index."""
    data = _load_rotation(config_path)
    idx = data.get("current_index", 0)
    return data["languages"][idx % len(data["languages"])]


def advance_rotation(config_path: Optional[str] = None) -> str:
    """Advance index, save, return the language we just finished with."""
    data = _load_rotation(config_path)
    langs = data["languages"]
    old_idx = data["current_index"]
    new_idx = (old_idx + 1) % len(langs)
    data["current_index"] = new_idx
    data["last_language"] = langs[old_idx]
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    _save_rotation(data, config_path)
    return langs[old_idx]


def get_signal_map(language: str) -> Dict[str, Dict[str, Any]]:
    """Return the full signal taxonomy for a language."""
    return SIGNAL_DB.get(language, {})


def get_signal_comparison(language: str) -> Dict[str, Any]:
    """Build a cross-language comparison of signal categories for a given language."""
    my_signals = SIGNAL_DB.get(language, {})

    comparison = {}
    for cat in ("error", "absence", "warning", "success", "async"):
        my_sig = my_signals.get(cat, {})
        row = {"source_language": language, "source_signal": my_sig.get("signal", "?"), "source_tag": my_sig.get("signal_tag", "?")}
        for other in ROTATION_ORDER:
            if other == language:
                continue
            other_sig = SIGNAL_DB.get(other, {}).get(cat, {})
            row[other] = {
                "signal": other_sig.get("signal", "?"),
                "tag": other_sig.get("signal_tag", "?"),
                "strength": classify_signal_strength(other_sig.get("signal_tag", "?")),
            }
        comparison[cat] = row
    return comparison


def generate_signal_report(
    rotate: bool = True,
    config_path: Optional[str] = None,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Generate a signal semantics report for the current rotation language.

    Args:
        rotate: advance rotation after generating
        config_path: optional path to language_rotation.json
        seed: optional seed for deterministic concept frame (unused here, for API compat)

    Returns:
        full signal report dict
    """
    data = _load_rotation(config_path)
    langs = data["languages"]
    old_idx = data["current_index"]

    current_language = langs[old_idx]
    new_idx = (old_idx + 1) % len(langs)

    if rotate:
        data["current_index"] = new_idx
        data["last_language"] = current_language
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        _save_rotation(data, config_path)

    signals = get_signal_map(current_language)
    comparison = get_signal_comparison(current_language)

    # Build category summaries
    categories = []
    for cat, sig in signals.items():
        categories.append({
            "category": cat,
            "signal": sig.get("signal", "?"),
            "mechanism": sig.get("mechanism", ""),
            "idiom": sig.get("idiom", ""),
            "key_traits": sig.get("key_traits", []),
            "signal_tag": sig.get("signal_tag", "?"),
            "emoji": sig.get("emoji", "🔧"),
            "strength": classify_signal_strength(sig.get("signal_tag", "?")),
        })

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": current_language,
        "current_index": old_idx,
        "new_index": new_idx if rotate else None,
        "rotated": rotate,
        "signal_categories": categories,
        "cross_language_comparison": comparison,
        "rotation_order": ROTATION_ORDER,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def format_signal_report(m: Dict[str, Any]) -> str:
    """Format the signal report as a human-readable string."""
    lang = m["language"]
    cats = m["signal_categories"]

    tag_legend = {
        "PROVEN":    "🛡️ PROVEN  — compile-time enforced",
        "NOMINAL":   "⚡ NOMINAL — compile-time checked",
        "ADAPTED":   "🟣 ADAPTED — runtime + annotations",
        "RUNTIME":   "⚙️ RUNTIME — runtime only",
    }

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  🛰️  POLYGLOT SIGNAL — Signal Semantics Cartography               ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Language : {lang:<48}║",
        f"║  Index    : {m['current_index']:<48}║",
        f"║  Rotated  : {str(m['rotated']):<48}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  SIGNAL TAXONOMY                                               ║",
    ]

    for cat in cats:
        lines.append(
            f"║  {cat['emoji']} {cat['category'].upper():8} : {cat['signal']:<38}║"
        )
        lines.append(
            f"║              [{cat['signal_tag']}] {classify_signal_strength(cat['signal_tag']):<35}║"
        )
        if cat["idiom"]:
            idiom_short = cat["idiom"][:42].replace("\n", " ")
            lines.append(f"║              💬 {idiom_short:<44}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  TAG LEGEND                                                    ║",
    ]
    for tag, desc in tag_legend.items():
        lines.append(f"║  {desc:<58}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  CROSS-LANGUAGE COMPARISON (this language vs others)            ║",
    ]

    cat_labels = {
        "error": "ERROR",
        "absence": "ABSENCE",
        "warning": "WARNING",
        "success": "SUCCESS",
        "async": "ASYNC",
    }

    for cat, row in m["cross_language_comparison"].items():
        lines.append(f"║  ── {cat_labels.get(cat, cat.upper()):<55}║")
        my_sig = row["source_signal"]
        lines.append(f"║    My signal: {my_sig:<46}║")
        others = [k for k in row if k not in ("source_language", "source_signal", "source_tag")]
        others_str = ", ".join(
            f"{k}({row[k]['signal'][:12]})" for k in others
        )
        lines.append(f"║    Others  : {others_str:<46}║")

    lines.append(
        "╚══════════════════════════════════════════════════════════════════╝"
    )
    return "\n".join(lines)


def run_tests() -> None:
    """Run all tests and exit."""
    import pytest
    import sys
    sys.exit(pytest.main([str(Path(__file__).parent.parent / "tests"), "-v"]))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        report = generate_signal_report()
        print(format_signal_report(report))
    else:
        print(f"Polyglot Signal v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_signal --test   # Run tests")
        print("  python -m polyglot_signal --report # Generate signal report")