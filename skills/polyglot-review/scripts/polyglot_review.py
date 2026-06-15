#!/usr/bin/env python3
"""
Polyglot Review — Language-Aware Code Review Generator
Reads language_rotation.json, advances the rotation, and generates idiomatic
code review feedback for a given code snippet in the current language.
"""

import json
import sys
import os
import re
import textwrap
from pathlib import Path
from datetime import datetime, timezone

ROTATION_FILE = Path.home() / ".openclaw/workspace/language_rotation.json"

LANG_REVIEW_TEMPLATES = {
    "Rust": {
        "topics": [
            ("Ownership & Borrowing", [
                "Is every value owned by exactly one variable?",
                "Are borrows (&, &mut) used correctly — no dangling references?",
                "Does the borrow checker complain? Fix aliasing violations.",
                "Prefer borrowing over cloning unless necessary.",
            ]),
            ("Error Handling", [
                "Using Result<T, E> instead of panicking on recoverable errors?",
                "Is ? operator used cleanly for error propagation?",
                "Are unwrap() calls justified or should they be handled?",
            ]),
            ("Performance", [
                "Are allocations minimized? Use stack allocation where possible.",
                "Is Iterator chaining used instead of imperative loops for efficiency?",
                "Check for unnecessary .clone() calls in hot paths.",
            ]),
        ],
        "checklist": [
            "No raw unwrap() on Result/Option in production paths",
            "Clippy warnings addressed (cargo clippy)",
            "unsafe blocks minimal and documented",
            "Lifetime annotations present when needed",
        ],
    },
    "Go": {
        "topics": [
            ("Error Handling", [
                "Are errors checked immediately after each operation?",
                "Is error context preserved (fmt.Errorf with %w)?",
                "No error variables discarded with _",
            ]),
            ("Concurrency", [
                "Are goroutines properly synchronized (channels, sync)?",
                "Potential race conditions on shared memory?",
                "Do long-running goroutines have shutdown signals?",
            ]),
            ("Code Style", [
                "Does it follow gofmt formatting?",
                "Is the error wrapping idiomatic (pkgerrors or wrapped)?",
                "Are interfaces small and focused (interface segregation)?",
            ]),
        ],
        "checklist": [
            "No sync.Mutex when sync.RWMutex would be better",
            "Context propagated through the call chain",
            "defer for cleanup (files, connections)",
            " slice capacity hints provided when known",
        ],
    },
    "Swift": {
        "topics": [
            ("Memory Safety", [
                "Are optionals handled properly (if let, guard let)?",
                "Any retain cycles with closures — use [weak self] / [unowned self]?",
                "Are class/struct choices intentional?",
            ]),
            ("API Design", [
                "Does the API feel Swifty — naming, labeled arguments?",
                "Are protocols used for abstraction over concrete types?",
                "Value types (structs) preferred for data models?",
            ]),
            ("Error Handling", [
                "Using Result<T, Error> or throws for recoverable errors?",
                "No force unwrap (!) or force cast (as!) unless provably safe",
            ]),
        ],
        "checklist": [
            "No force unwrap in production code",
            "Delegate/concurrency patterns match target iOS version",
            "lazy properties used for expensive computations",
            "access control (private/fileprivate) applied appropriately",
        ],
    },
    "Kotlin": {
        "topics": [
            ("Null Safety", [
                "Are nullable types (?.) handled correctly?",
                "No !! operator unless absolutely certain?",
                "Elvis operator (?:) used for defaults?",
            ]),
            ("Coroutines & Async", [
                "Are coroutines launched with correct scope and context?",
                "Is dispatching appropriate (Dispatchers.IO vs Main)?",
                "No blocking calls inside suspend functions?",
            ]),
            ("Pragmatic Style", [
                "Are data classes used for simple DTOs?",
                "Extension functions used to reduce nesting?",
                "Are sequences used for large collections to avoid intermediate allocations?",
            ]),
        ],
        "checklist": [
            "No .runBlocking in production coroutine code",
            "Inlined reified generics used where appropriate",
            "Visibility modifiers explicit (public by default is fine)",
            "Companion object used correctly for static members",
        ],
    },
    "TypeScript": {
        "topics": [
            ("Type Safety", [
                "Are strict types used — no implicit any?",
                "Are discriminated unions or type guards used for branching?",
                "Generic constraints appropriate for shared logic?",
            ]),
            ("Async Patterns", [
                "Is async/await used consistently (not mixing .then chains)?",
                "Are Promise.all() used for parallel operations?",
                "Error handling in async functions with try/catch?",
            ]),
            ("Module Quality", [
                "Are interfaces defined for object shapes?",
                "Is there appropriate use of readonly and const assertions?",
                "Barrel exports (index.ts) used for clean public API?",
            ]),
        ],
        "checklist": [
            "No @ts-ignore or @ts-nocheck without justification",
            "strict: true in tsconfig for new projects",
            "Type annotations on exported functions",
            "No use of 'any' type — prefer 'unknown' and type narrowing",
        ],
    },
    "JavaScript": {
        "topics": [
            ("Async Discipline", [
                "Is async/await used consistently?",
                "Are Promise chains properly chained (no callback hell)?",
                "Are errors caught in try/catch blocks?",
            ]),
            ("Variable Practices", [
                "const used by default — let only when reassignment needed?",
                "Are destructuring and spread operators used?",
                "No implicit global variables (use strict or ES modules)?",
            ]),
            ("Modern Syntax", [
                "Template literals used for string interpolation?",
                "Optional chaining (?.) and nullish coalescing (??) used?",
                "Are arrow functions used for callbacks?",
            ]),
        ],
        "checklist": [
            "No var keyword — const/let only",
            "No console.log in production code",
            "Module exports using ES modules (export) or proper CommonJS",
            "Error handling on all async operations",
        ],
    },
    "Java": {
        "topics": [
            ("Streams & Lambdas", [
                "Are streams preferred over imperative loops for transformations?",
                "Are method references used for simple lambdas?",
                "No side effects in stream operations (pure functions)?",
            ]),
            ("Generics", [
                "Are generic type bounds correct (extends, super)?",
                "Is there appropriate use of wildcards vs raw types?",
                "No raw types in new code (use diamond operator)?",
            ]),
            ("OO & Design", [
                "Are classes immutable where possible (final fields)?",
                "Is inheritance used appropriately vs composition?",
                "Are Optional and null used correctly?",
            ]),
        ],
        "checklist": [
            "try-with-resources used for AutoCloseable resources",
            "stream operations are stateless and non-interfering",
            "no raw types — use generics consistently",
            "Optional used for return types, not fields",
        ],
    },
    "C/C++": {
        "topics": [
            ("Memory Safety", [
                "Is every allocation matched with exactly one deallocation?",
                "Are smart pointers (unique_ptr, shared_ptr) used instead of raw new/delete?",
                "Any buffer overflow or out-of-bounds access risks?",
            ]),
            ("RAII & Resources", [
                "Are all resources (files, handles, locks) wrapped in RAII objects?",
                "Are locks held for minimal duration?",
                "Rule of Zero vs Rule of Five respected?",
            ]),
            ("Templates & Generics", [
                "Are template parameters constrained where appropriate (C++20 concepts)?",
                "Is SFINAE or concepts used cleanly?",
                "Any header bloat from over-inclusion?",
            ]),
        ],
        "checklist": [
            "No raw new/delete in modern C++",
            "No resource leaks — RAII or smart pointers",
            "Threadsafe access to shared mutable state",
            "Move semantics used for non-copyable types",
        ],
    },
}

def advance_rotation():
    if not ROTATION_FILE.exists():
        print("ERROR: language_rotation.json not found", file=sys.stderr)
        sys.exit(1)

    with open(ROTATION_FILE) as f:
        state = json.load(f)

    langs = state.get("languages", [])
    rotation = langs  # same order as languages array

    # Find position of last used language in the languages array
    last = state.get("last_language", "")
    try:
        pos = rotation.index(last)
    except ValueError:
        pos = -1

    # Advance to next language in rotation
    next_index = (pos + 1) % len(rotation)
    next_lang = rotation[next_index]

    state["current_index"] = next_index
    state["last_language"] = next_lang
    state["updated_at"] = datetime.now(timezone.utc).isoformat()

    with open(ROTATION_FILE, "w") as f:
        json.dump(state, f, indent=2)

    return next_lang, state


def generate_review(lang: str, code: str = "") -> str:
    template = LANG_REVIEW_TEMPLATES.get(lang, LANG_REVIEW_TEMPLATES["JavaScript"])

    output_lines = [
        f"=== Polyglot Review ({lang}) ===",
        "",
        f"📋 **Code Review — {lang}**",
        "",
    ]

    for topic_name, questions in template["topics"]:
        output_lines.append(f"### 🔍 {topic_name}")
        for q in questions:
            output_lines.append(f"- {q}")
        output_lines.append("")

    if template["checklist"]:
        output_lines.append("### ✅ General Checklist")
        for item in template["checklist"]:
            output_lines.append(f"- [ ] {item}")
        output_lines.append("")

    if code:
        output_lines.append(f"### 📝 Code Under Review")
        output_lines.append("```" + ("rust" if lang == "Rust" else lang.lower().replace("/","") if "/" not in lang else "cpp"))
        output_lines.append(code.strip())
        output_lines.append("```")
        output_lines.append("")

    return "\n".join(output_lines)


def main():
    lang, state = advance_rotation()

    # Read code from stdin or args
    code = ""
    if len(sys.argv) > 1:
        code = sys.argv[1]
    elif not sys.stdin.isatty():
        code = sys.stdin.read()

    review = generate_review(lang, code)

    print(review)
    print(f"\n[State updated] index={state['current_index']} last={state['last_language']}")


if __name__ == "__main__":
    main()