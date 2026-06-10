#!/usr/bin/env python3
"""
Polyglot Quiz — Language Rotation Quiz Generator
Reads language_rotation.json, advances index, generates quiz questions, updates state.
"""

import json
import sys
import random
from pathlib import Path
from datetime import datetime, timezone

ROTATION = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++"
]

ROTATION_FILE = Path.home() / ".openclaw/workspace/language_rotation.json"

QUIZZES = {
    "Rust": {
        "q": "Rust's ownership system eliminates entire classes of bugs. What Rust feature ensures memory safety without a garbage collector?",
        "a": "Ownership & Borrowing (or 'ownership' or 'borrow checker')",
        "hint": "It involves `&` references and rules about who owns the data.",
    },
    "Go": {
        "q": "Go was designed by Google to be simple and scalable. What lightweight concurrency primitive is central to Go's design?",
        "a": "Goroutines and channels (or 'goroutines')",
        "hint": "They're launched with the `go` keyword and communicate via channels.",
    },
    "Swift": {
        "q": "Swift handles the absence of values safely through a feature that forces you to handle the 'nil' case. What is it called?",
        "a": "Optionals (or 'optional types')",
        "hint": "It's declared with `?`, like `String?`.",
    },
    "Kotlin": {
        "q": "Kotlin's coroutines make async programming manageable. What keyword marks a suspending function that can pause without blocking a thread?",
        "a": "suspend",
        "hint": "It's the keyword before `fun` in a suspending function definition.",
    },
    "TypeScript": {
        "q": "TypeScript extends JavaScript with compile-time type checking. What TypeScript feature narrows the type of a variable within a conditional block?",
        "a": "Type guards (or 'type predicates', ' instanceof')",
        "hint": "A function returning `p is Cat` is a type guard for the Cat type.",
    },
    "JavaScript": {
        "q": "Modern JavaScript uses async/await for asynchronous code. What does `await` do when placed before a Promise?",
        "a": "Pauses execution until the Promise resolves, returning its value",
        "hint": "It can only be used inside an `async` function.",
    },
    "Java": {
        "q": "Java's stream API lets you process collections in a functional style. What method in `Stream<T>` filters elements based on a predicate?",
        "a": "filter()",
        "hint": "It's often followed by `.map()` and `.collect()` in a fluent chain.",
    },
    "C/C++": {
        "q": "C++ uses RAII (Resource Acquisition Is Initialization) to manage resources. What C++ feature automatically calls a destructor when an object goes out of scope?",
        "a": "RAII / smart pointers (unique_ptr, shared_ptr) or stack semantics",
        "hint": "Smart pointers like `unique_ptr<T>` automatically free memory when destroyed.",
    },
}

def get_next_language():
    """Advance rotation and return the next language."""
    if not ROTATION_FILE.exists():
        print("ERROR: language_rotation.json not found", file=sys.stderr)
        sys.exit(1)

    with open(ROTATION_FILE) as f:
        state = json.load(f)

    last = state.get("last_language", "")
    try:
        pos = ROTATION.index(last)
    except ValueError:
        pos = -1
    next_lang = ROTATION[(pos + 1) % len(ROTATION)]

    state["current_index"] = (state.get("current_index", 0) + 1) % len(state.get("languages", ROTATION))
    state["last_language"] = next_lang
    state["updated_at"] = datetime.now(timezone.utc).isoformat()

    with open(ROTATION_FILE, "w") as f:
        json.dump(state, f, indent=2)

    return next_lang, state


def generate_quiz(lang: str) -> dict:
    """Generate a quiz for the given language with a distractor."""
    quiz = QUIZZES.get(lang, {
        "q": f"What is a notable feature of {lang}?",
        "a": "Check the docs",
        "hint": "Consult the language documentation.",
    })

    # Pick a distractor from other languages
    other_langs = [l for l in ROTATION if l != lang]
    distractor_lang = random.choice(other_langs)
    distractor = QUIZZES.get(distractor_lang, {}).get("a", "A valid answer")

    return {
        "language": lang,
        "question": quiz["q"],
        "answer": quiz["a"],
        "hint": quiz["hint"],
        "distractor": distractor,
    }


def main():
    lang, state = get_next_language()
    quiz = generate_quiz(lang)

    print(f"=== Polyglot Quiz ({lang}) ===")
    print()
    print(f"Q: {quiz['question']}")
    print()
    print(f"Think: {quiz['hint']}")
    print()
    print(f"Answer: {quiz['answer']}")
    print()
    print(f"[State updated] index={state['current_index']} last={state['last_language']}")


if __name__ == "__main__":
    main()