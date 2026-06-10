#!/usr/bin/env python3
"""
Polyglot Wisdom — Language Rotation Engine
Reads language_rotation.json, advances index, generates wisdom + code snippet, updates state.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

LANG_ORDER = [
    "Rust", "Go", "Swift", "Kotlin", "TypeScript",
    "JavaScript", "Java", "C/C++", "Rust"
]

ROTATION_FILE = Path.home() / ".openclaw/workspace/language_rotation.json"

WISDOM = {
    "Rust": {
        "philosophy": "Rust: Memory safety without garbage collection — zero-cost abstractions.",
        "code": '''// Rust: Ownership & Borrowing
fn main() {
    let s1 = String::from("hello");
    let s2 = &s1;           // borrow reference
    let s3 = s1.clone();    // deep copy
    println!("{} {}", s2, s3);
}

fn calculate(nums: &[i32]) -> i32 {
    nums.iter().filter(|&&n| n % 2 == 0).sum()
}'''
    },
    "Go": {
        "philosophy": "Go: Simplicity is the ultimate sophistication. Concurrency built in.",
        "code": '''// Go: Goroutines & Channels
func main() {
    ch := make(chan string)
    go func() { ch <- "ping" }()
    msg := <-ch
    println(msg)
}

func worker(jobs <-chan int, results chan<- int) {
    for j := range jobs {
        results <- j * 2
    }
}'''
    },
    "Swift": {
        "philosophy": "Swift: Safe, fast, expressive. Optionals handle nil with grace.",
        "code": '''// Swift: Optionals & Protocol-Oriented
func greet(_ name: String?) {
    if let n = name {
        print("Hello, \\(n)!")
    } else {
        print("Hello, stranger!")
    }
}

protocol Drawable { func draw() }
struct Circle: Drawable { func draw() { print("circle") } }
struct Square: Drawable { func draw() { print("square") } }'''
    },
    "Kotlin": {
        "philosophy": "Kotlin: Pragmatic elegance. Coroutines for async, null safety built in.",
        "code": '''// Kotlin: Null Safety & Coroutines
fun greet(name: String?) {
    name?.let { println("Hello, $it!") } ?: println("Hello!")
}

suspend fun fetchData(): String {
    return kotlinx.coroutines.delay(1000); "done"
}

data class User(val name: String, val age: Int)
val user = User("Alice", 30)'''
    },
    "TypeScript": {
        "philosophy": "TypeScript: JavaScript that scales. Types catch bugs before they hatch.",
        "code": '''// TypeScript: Generics & Type Guards
function greet(name: string | null): string {
    return name ? \`Hello, \${name}!\` : "Hello!";
}

interface Pet { name: string }
interface Cat extends Pet { meow: () => void }
function isCat(p: Pet): p is Cat {
    return "meow" in p;
}'''
    },
    "JavaScript": {
        "philosophy": "JavaScript: The language of the web. Async/await makes concurrency elegant.",
        "code": '''// JavaScript: Async/Await & Destructuring
async function fetchUser(id) {
    const { data } = await fetch(\`/api/\${id}\`).then(r => r.json());
    return data;
}

const [first, ...rest] = [1, 2, 3, 4];
const { name, age } = { name: "Alice", age: 30 };'''
    },
    "Java": {
        "philosophy": "Java: Write once, run anywhere. Generics, streams, and rock-solid ecosystem.",
        "code": '''// Java: Streams & Generics
public String greet(String name) {
    return Optional.ofNullable(name)
        .map(n -> "Hello, " + n + "!")
        .orElse("Hello!");
}

List<Integer> evens = List.of(1,2,3,4).stream()
    .filter(n -> n % 2 == 0)
    .toList();'''
    },
    "C/C++": {
        "philosophy": "C/C++: Maximum control, maximum responsibility. Understanding pointer arithmetic is power.",
        "code": '''// C++: RAII & Templates
#include <memory>
#include <vector>
#include <iostream>

auto greet(const std::string& name) -> std::string {
    return name.empty() ? "Hello!" : "Hello, " + name + "!";
}

template<typename T>
T max(const T a, const T b) { return a > b ? a : b; }'''
    },
}

def get_wisdom_for_lang(lang: str) -> dict:
    return WISDOM.get(lang, {
        "philosophy": f"{lang}: A language with unique strengths.",
        "code": f"// {lang} code example\nprint(\"{lang} wisdom\")"
    })

def advance_rotation():
    if not ROTATION_FILE.exists():
        print("ERROR: language_rotation.json not found", file=sys.stderr)
        sys.exit(1)

    with open(ROTATION_FILE) as f:
        state = json.load(f)

    langs = state.get("languages", [])
    current = state.get("current_index", 0)
    last = state.get("last_language", "")

    # Find next language in our rotation order (skip duplicates in langs)
    # The order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
    rotation = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
    try:
        pos = rotation.index(last)
    except ValueError:
        pos = -1
    next_lang = rotation[(pos + 1) % len(rotation)]

    state["current_index"] = (current + 1) % len(langs)
    state["last_language"] = next_lang
    state["updated_at"] = datetime.now(timezone.utc).isoformat()

    with open(ROTATION_FILE, "w") as f:
        json.dump(state, f, indent=2)

    return next_lang, state

def main():
    lang, state = advance_rotation()
    wisdom = get_wisdom_for_lang(lang)

    print(f"=== Polyglot Wisdom ({lang}) ===")
    print(wisdom["philosophy"])
    print()
    print("```" + ("rust" if lang == "Rust" else lang.lower() if lang != "C/C++" else "cpp"))
    print(wisdom["code"].strip())
    print("```")
    print()
    print(f"[State updated] index={state['current_index']} last={state['last_language']}")

if __name__ == "__main__":
    main()