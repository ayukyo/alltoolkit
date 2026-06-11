#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Polyglot Pattern Translation Utilities
====================================================
A zero-dependency, production-ready utility that translates programming patterns
across the language rotation: Rust → Go → Swift → Kotlin → TypeScript →
JavaScript → Java → C/C++ → (repeat)

This module teaches idiomatic patterns by showing the SAME concept expressed in
each language's native style. Patterns include: error handling, null/Option
handling, concurrency, iteration, function composition, and more.

Author: AllToolkit Contributors
License: MIT
"""

import json
import re
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum

# =============================================================================
# Constants
# =============================================================================

ROTATION_FILE = Path.home() / ".openclaw/workspace/language_rotation.json"

# The official language rotation order
LANGUAGE_ROTATION = [
    "Rust", "Go", "Swift", "Kotlin", "TypeScript",
    "JavaScript", "Java", "C/C++"
]

# Language metadata
LANGUAGE_META = {
    "Rust": {
        "extension": ".rs",
        "style": "rust",
        "paradigm": "Systems / Functional",
        "gc": False,
        "null_safety": "Algebraic types (Option<T>)",
    },
    "Go": {
        "extension": ".go",
        "style": "go",
        "paradigm": "Concurrent / Imperative",
        "gc": True,
        "null_safety": "No null; use pointers or explicit opt",
    },
    "Swift": {
        "extension": ".swift",
        "style": "swift",
        "paradigm": "Protocol-Oriented / Functional",
        "gc": True,
        "null_safety": "Optional<T> (nil)",
    },
    "Kotlin": {
        "extension": ".kt",
        "style": "kotlin",
        "paradigm": "Object-Oriented / Functional",
        "gc": True,
        "null_safety": "Nullable types (T?)",
    },
    "TypeScript": {
        "extension": ".ts",
        "style": "typescript",
        "paradigm": "Static typing over JS",
        "gc": True,
        "null_safety": "union T | null; strict null checks",
    },
    "JavaScript": {
        "extension": ".js",
        "style": "javascript",
        "paradigm": "Dynamic / Functional",
        "gc": True,
        "null_safety": "Dynamic; undefined / null",
    },
    "Java": {
        "extension": ".java",
        "style": "java",
        "paradigm": "Object-Oriented / Generic",
        "gc": True,
        "null_safety": "Reference types can be null",
    },
    "C/C++": {
        "extension": ".cpp",
        "style": "cpp",
        "paradigm": "Systems / Generic",
        "gc": False,
        "null_safety": "Raw pointers; manual ownership",
    },
}

# =============================================================================
# Pattern Definitions
# =============================================================================

@dataclass
class PatternExample:
    """A single code example in one language."""
    language: str
    code: str
    annotation: str = ""


@dataclass
class Pattern:
    """A programming pattern demonstrated across all languages."""
    id: str
    name: str
    description: str
    category: str
    examples: List[PatternExample]


# -----------------------------------------------------------------------------
# Pattern 1: Null/Option Handling — The "Hello, X!" pattern
# Every language has its own way to handle a possibly-absent name.
# -----------------------------------------------------------------------------
NULL_PATTERNS = Pattern(
    id="null_safety",
    name="Null/Option Safety",
    description="Handle potentially missing values with each language's idiomatic approach.",
    category="Error Handling",
    examples=[
        PatternExample(
            "Rust",
            '''fn greet(name: Option<&str>) {
    match name {
        Some(n) => println!("Hello, {}!", n),
        None => println!("Hello, stranger!"),
    }
}

fn main() {
    greet(Some("Alice"));
    greet(None);
}''',
            "Option<T> enum: Some(T) or None"
        ),
        PatternExample(
            "Go",
            '''package main

import "fmt"

func greet(name *string) {
    if name != nil {
        fmt.Printf("Hello, %s!\\n", *name)
    } else {
        fmt.Println("Hello, stranger!")
    }
}

func main() {
    alice := "Alice"
    greet(&alice)
    greet(nil)
}''',
            "Nil pointers; explicit nil check"
        ),
        PatternExample(
            "Swift",
            '''func greet(_ name: String?) {
    if let n = name {
        print("Hello, \\(n)!")
    } else {
        print("Hello, stranger!")
    }
}

greet("Alice")
greet(nil)''',
            "Optional<T> with if-let unwrap"
        ),
        PatternExample(
            "Kotlin",
            '''fun greet(name: String?) {
    name?.let { println("Hello, $it!") } ?: println("Hello, stranger!")
}

fun main() {
    greet("Alice")
    greet(null)
}''',
            "Safe-call operator ?.let and Elvis ?:"
        ),
        PatternExample(
            "TypeScript",
            '''function greet(name: string | null): string {
    return name !== null ? `Hello, ${name}!` : "Hello, stranger!";
}

console.log(greet("Alice"));
console.log(greet(null));''',
            "Union type with explicit null guard"
        ),
        PatternExample(
            "JavaScript",
            '''function greet(name) {
    return name != null
        ? `Hello, ${name}!`
        : "Hello, stranger!";
}

console.log(greet("Alice"));
console.log(greet(null));''',
            "Dynamic != null check (covers undefined too)"
        ),
        PatternExample(
            "Java",
            '''import java.util.Optional;

public String greet(Optional<String> name) {
    return name
        .map(n -> "Hello, " + n + "!")
        .orElse("Hello, stranger!");
}

public static void main(String[] args) {
    System.out.println(greet(Optional.of("Alice")));
    System.out.println(greet(Optional.empty()));
}''',
            "Optional<T> with map/orElse"
        ),
        PatternExample(
            "C/C++",
            '''#include <optional>
#include <iostream>
#include <string>

std::string greet(const std::optional<std::string>& name) {
    if (name.has_value()) {
        return "Hello, " + name.value() + "!";
    }
    return "Hello, stranger!";
}

int main() {
    std::cout << greet(std::make_optional("Alice")) << std::endl;
    std.out << greet(std::nullopt) << std::endl;
}''',
            "std::optional (C++17) with has_value()/value()"
        ),
    ]
)

# -----------------------------------------------------------------------------
# Pattern 2: Error Handling — Result/Either type patterns
# -----------------------------------------------------------------------------
ERROR_PATTERNS = Pattern(
    id="error_handling",
    name="Error Handling with Result/Either",
    description="Each language has its own error-reporting idiom — from Rust's Result<T,E> to Go's multi-return.",
    category="Error Handling",
    examples=[
        PatternExample(
            "Rust",
            '''use std::num::ParseIntError;

fn parse_and_double(s: &str) -> Result<i32, ParseIntError> {
    let n: i32 = s.parse()?;
    Ok(n * 2)
}

fn main() {
    match parse_and_double("42") {
        Ok(v) => println!("Result: {}", v),
        Err(e) => println!("Error: {}", e),
    }
}''',
            "Result<T, E> with ? operator"
        ),
        PatternExample(
            "Go",
            '''package main

import (
    "errors"
    "strconv"
)

func parseAndDouble(s string) (int, error) {
    n, err := strconv.Atoi(s)
    if err != nil {
        return 0, err
    }
    return n * 2, nil
}

func main() {
    if v, err := parseAndDouble("42"); err == nil {
        println("Result:", v)
    } else {
        println("Error:", err)
    }
}''',
            "Multiple return values (value, error)"
        ),
        PatternExample(
            "Swift",
            '''enum ParseError: Error { case invalidFormat }

func parseAndDouble(_ s: String) throws -> Int {
    guard let n = Int(s) else { throw ParseError.invalidFormat }
    return n * 2
}

do {
    let result = try parseAndDouble("42")
    print("Result: \\(result)")
} catch {
    print("Error: \\(error)")
}''',
            "throws keyword with do-try-catch"
        ),
        PatternExample(
            "Kotlin",
            '''fun parseAndDouble(s: String): Result<Int> {
    return try {
        val n = s.toInt()
        Result.success(n * 2)
    } catch (e: NumberFormatException) {
        Result.failure(e)
    }
}

fun main() {
    parseAndDouble("42")
        .onSuccess { println("Result: $it") }
        .onFailure { println("Error: $it") }
}''',
            "Result<T> with onSuccess/onFailure"
        ),
        PatternExample(
            "TypeScript",
            '''type Result<T, E = Error> =
    | { ok: true; value: T }
    | { ok: false; error: E };

function parseAndDouble(s: string): Result<number> {
    const n = parseInt(s, 10);
    return isNaN(n)
        ? { ok: false, error: new Error("invalid") }
        : { ok: true, value: n * 2 };
}

const r = parseAndDouble("42");
if (r.ok) {
    console.log("Result:", r.value);
} else {
    console.log("Error:", r.error);
}''',
            "Discriminated union Result type"
        ),
        PatternExample(
            "JavaScript",
            '''// No built-in Result — use a simple object or throw
function parseAndDouble(s) {
    const n = parseInt(s, 10);
    if (isNaN(n)) throw new Error("invalid number");
    return n * 2;
}

try {
    console.log("Result:", parseAndDouble("42"));
} catch (e) {
    console.log("Error:", e.message);
}''',
            "Thow/catch (JavaScript-native approach)"
        ),
        PatternExample(
            "Java",
            '''import java.util.Optional;

public static Optional<Integer> parseAndDouble(String s) {
    try {
        int n = Integer.parseInt(s);
        return Optional.of(n * 2);
    } catch (NumberFormatException e) {
        return Optional.empty();
    }
}

public static void main(String[] args) {
    parseAndDouble("42")
        .ifPresentOrElse(
            v -> System.out.println("Result: " + v),
            () -> System.out.println("Error: invalid")
        );
}''',
            "Optional<Integer> for error-or-value"
        ),
        PatternExample(
            "C/C++",
            '''#include <expected>
#include <iostream>
#include <string>

std::expected<int, std::string> parseAndDouble(const std::string& s) {
    try {
        int n = std::stoi(s);
        return n * 2;
    } catch (...) {
        return std::unexpected("invalid number");
    }
}

int main() {
    auto r = parseAndDouble("42");
    if (r) {
        std::cout << "Result: " << r.value() << std::endl;
    } else {
        std::cout << "Error: " << r.error() << std::endl;
    }
}''',
            "std::expected (C++23) with value/error"
        ),
    ]
)

# -----------------------------------------------------------------------------
# Pattern 3: Concurrency — Parallel task execution
# -----------------------------------------------------------------------------
CONCURRENCY_PATTERNS = Pattern(
    id="concurrency",
    name="Concurrent Task Execution",
    description="Run multiple tasks concurrently — each language uses its own concurrency model.",
    category="Concurrency",
    examples=[
        PatternExample(
            "Rust",
            '''use std::sync::mpsc::channel;
use std::thread;

fn main() {
    let (tx, rx) = channel();

    for i in 0..3 {
        let tx = tx.clone();
        thread::spawn(move || {
            tx.send(i * 2).unwrap();
        });
    }

    for _ in 0..3 {
        println!("Got: {}", rx.recv().unwrap());
    }
}''',
            "threads + channels (std::sync::mpsc)"
        ),
        PatternExample(
            "Go",
            '''package main

import (
    "fmt"
    "sync"
)

func main() {
    // Launch 3 goroutines concurrently
    var wg sync.WaitGroup
    for i := 0; i < 3; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            println("Task", id, "->", id*2)
        }(i)
    }
    wg.Wait()
}''',
            "goroutines + sync.WaitGroup"
        ),
        PatternExample(
            "Swift",
            '''import Foundation

let group = DispatchGroup()
for i in 0..<3 {
    group.enter()
    DispatchQueue.global().async {
        print("Task \\(i) -> \\(i*2)")
        group.leave()
    }
}
group.wait()''',
            "Grand Central Dispatch (DispatchGroup)"
        ),
        PatternExample(
            "Kotlin",
            '''import kotlinx.coroutines.*

fun main() = runBlocking {
    val jobs = (0..2).map { i ->
        async {
            println("Task $i -> ${i*2}")
        }
    }
    jobs.awaitAll()
}''',
            "Kotlin Coroutines with async/awaitAll"
        ),
        PatternExample(
            "TypeScript",
            '''async function runTasks(ids: number[]) {
    const results = await Promise.all(
        ids.map(id =>
            (async () => {
                await delay(10);
                return id * 2;
            })()
        )
    );
    console.log("Results:", results);
}

function delay(ms: number) {
    return new Promise(r => setTimeout(r, ms));
}

runTasks([0, 1, 2]);''',
            "Promise.all with async IIFEs"
        ),
        PatternExample(
            "JavaScript",
            '''// Node.js cluster (simplified)
async function runTasks(ids) {
    const results = await Promise.all(
        ids.map(id =>
            new Promise(resolve => {
                setTimeout(() => resolve(id * 2), 10);
            })
        )
    );
    console.log("Results:", results);
}

runTasks([0, 1, 2]);''',
            "Promise.all with setTimeout"
        ),
        PatternExample(
            "Java",
            '''import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws Exception {
        ExecutorService exec = Executors.newFixedThreadPool(3);
        var futures = IntStream.range(0, 3)
            .mapToObj(i ->
                exec.submit(() -> {
                    Thread.sleep(10);
                    return i * 2;
                })
            )
            .toList();

        futures.forEach(f ->
            System.out.println("Got: " + f.get())
        );
        exec.shutdown();
    }
}''',
            "ExecutorService + CompletableFuture"
        ),
        PatternExample(
            "C/C++",
            '''#include <future>
#include <vector>
#include <iostream>
#include <thread>
#include <chrono>

int main() {
    std::vector<std::future<int>> futures;
    for (int i = 0; i < 3; ++i) {
        futures.push_back(std::async(std::launch::async, [i]() {
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
            return i * 2;
        }));
    }
    for (auto& f : futures) {
        std::cout << "Got: " << f.get() << std::endl;
    }
}''',
            "std::async with std::future"
        ),
    ]
)

# -----------------------------------------------------------------------------
# Pattern 4: Iteration & Transformation
# -----------------------------------------------------------------------------
ITERATION_PATTERNS = Pattern(
    id="iteration",
    name="Iteration & Transformation",
    description="Transform a list of numbers by doubling the even ones — every language's idiomatic way.",
    category="Functional",
    examples=[
        PatternExample(
            "Rust",
            '''fn main() {
    let nums = vec![1, 2, 3, 4, 5, 6];
    let result: Vec<i32> = nums
        .iter()
        .filter(|&&n| n % 2 == 0)
        .map(|&n| n * 2)
        .collect();
    println!("{:?}", result); // [4, 8, 12]
}''',
            "Iterator chains: filter + map + collect"
        ),
        PatternExample(
            "Go",
            '''package main

import (
    "fmt"
    "slices"
)

func main() {
    nums := []int{1, 2, 3, 4, 5, 6}
    // filter evens, then map *2
    evens := slices.Filter(nil, nums, func(n int) bool { return n%2 == 0 })
    result := slices.Map(evens, func(n int) int { return n * 2 })
    fmt.Println(result) // [4 8 12]
}''',
            "slices.Filter + slices.Map (Go 1.21)"
        ),
        PatternExample(
            "Swift",
            '''let nums = [1, 2, 3, 4, 5, 6]
let result = nums
    .filter { $0 % 2 == 0 }
    .map { $0 * 2 }
print(result) // [4, 8, 12]''',
            "Collection chains with trailing closures"
        ),
        PatternExample(
            "Kotlin",
            '''val nums = listOf(1, 2, 3, 4, 5, 6)
val result = nums
    .filter { it % 2 == 0 }
    .map { it * 2 }
println(result) // [4, 8, 12]''',
            "filter + map on List; it parameter"
        ),
        PatternExample(
            "TypeScript",
            '''const nums = [1, 2, 3, 4, 5, 6];
const result = nums
    .filter(n => n % 2 === 0)
    .map(n => n * 2);
console.log(result); // [4, 8, 12]''',
            "Array.filter + Array.map"
        ),
        PatternExample(
            "JavaScript",
            '''const nums = [1, 2, 3, 4, 5, 6];
const result = nums
    .filter(n => n % 2 === 0)
    .map(n => n * 2);
console.log(result); // [4, 8, 12]''',
            "Array.filter + Array.map"
        ),
        PatternExample(
            "Java",
            '''import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<Integer> nums = List.of(1, 2, 3, 4, 5, 6);
        List<Integer> result = nums.stream()
            .filter(n -> n % 2 == 0)
            .map(n -> n * 2)
            .toList();
        System.out.println(result); // [4, 8, 12]
    }
}''',
            "Stream API with filter/map/toList"
        ),
        PatternExample(
            "C/C++",
            '''#include <vector>
#include <algorithm>
#include <iostream>

int main() {
    std::vector<int> nums{1, 2, 3, 4, 5, 6};
    std::vector<int> result;

    std::copy_if(nums.begin(), nums.end(),
        std::back_inserter(result),
        [](int n) { return n % 2 == 0; });

    std::transform(result.begin(), result.end(),
        result.begin(),
        [](int n) { return n * 2; });

    for (int n : result) std::cout << n << " "; // 4 8 12
}''',
            "std::copy_if + std::transform (C++17/20)"
        ),
    ]
)

# -----------------------------------------------------------------------------
# Pattern 5: Function Composition
# -----------------------------------------------------------------------------
COMPOSITION_PATTERNS = Pattern(
    id="function_composition",
    name="Function Composition",
    description="Chain operations: add 1, then multiply by 2, then convert to string.",
    category="Functional",
    examples=[
        PatternExample(
            "Rust",
            '''fn main() {
    let result = (0..5)
        .map(|n| n + 1)
        .map(|n| n * 2)
        .map(|n| n.to_string())
        .collect::<Vec<_>>();
    println!("{:?}", result);
}''',
            "Iterator chain with turbofish ::collect"
        ),
        PatternExample(
            "Go",
            '''package main

import (
    "fmt"
    "slices"
)

func main() {
    nums := []int{0, 1, 2, 3, 4}
    result := slices.Map(
        slices.Map(
            slices.Map(nums,
                func(n int) int { return n + 1 }),
            func(n int) int { return n * 2 }),
        func(n int) string { return fmt.Sprintf("%d", n) })
    fmt.Println(result)
}''',
            "slices.Map chains (Go 1.21)"
        ),
        PatternExample(
            "Swift",
            '''let result = (0..<5)
    .map { $0 + 1 }
    .map { $0 * 2 }
    .map { String($0) }
print(result)''',
            "Method chain with trailing closures"
        ),
        PatternExample(
            "Kotlin",
            '''val result = (0..4)
    .map { it + 1 }
    .map { it * 2 }
    .map { it.toString() }
println(result)''',
            "Range + map chain"
        ),
        PatternExample(
            "TypeScript",
            '''const result = [0,1,2,3,4]
    .map(n => n + 1)
    .map(n => n * 2)
    .map(n => String(n));
console.log(result);''',
            "Array.map chain"
        ),
        PatternExample(
            "JavaScript",
            '''const result = [0,1,2,3,4]
    .map(n => n + 1)
    .map(n => n * 2)
    .map(n => String(n));
console.log(result);''',
            "Array.map chain"
        ),
        PatternExample(
            "Java",
            '''import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<String> result = List.of(0,1,2,3,4).stream()
            .map(n -> n + 1)
            .map(n -> n * 2)
            .map(Object::toString)
            .toList();
        System.out.println(result);
    }
}''',
            "Stream with method reference Object::toString"
        ),
        PatternExample(
            "C/C++",
            '''#include <vector>
#include <ranges>
#include <string>
#include <iostream>

int main() {
    using namespace std::ranges;
    auto result = (std::views::iota(0)
        | views::transform([](int n) { return n + 1; })
        | views::transform([](int n) { return n * 2; })
        | views::transform([](int n) { return std::to_string(n); })
    );
    for (auto&& s : result) std::cout << s << " ";
}''',
            "std::views::transform with range | pipe (C++20)"
        ),
    ]
)

# =============================================================================
# All Patterns Registry
# =============================================================================

ALL_PATTERNS = {
    p.id: p for p in [
        NULL_PATTERNS,
        ERROR_PATTERNS,
        CONCURRENCY_PATTERNS,
        ITERATION_PATTERNS,
        COMPOSITION_PATTERNS,
    ]
}

PATTERN_CATEGORIES = list(set(p.category for p in ALL_PATTERNS.values()))

# =============================================================================
# Language Rotation Utilities
# =============================================================================

def get_rotation_state() -> Dict[str, Any]:
    """Load the current language rotation state from language_rotation.json."""
    if not ROTATION_FILE.exists():
        raise FileNotFoundError(
            f"Rotation file not found: {ROTATION_FILE}. "
            "Run polyglot-companion or polyglot-quiz first."
        )
    with open(ROTATION_FILE) as f:
        return json.load(f)


def advance_rotation() -> str:
    """Advance the language rotation and return the newly selected language."""
    state = get_rotation_state()
    last = state.get("last_language", "")

    try:
        pos = LANGUAGE_ROTATION.index(last)
    except ValueError:
        pos = -1

    next_lang = LANGUAGE_ROTATION[(pos + 1) % len(LANGUAGE_ROTATION)]

    state["current_index"] = (state.get("current_index", 0) + 1) % len(state.get("languages", LANGUAGE_ROTATION))
    state["last_language"] = next_lang
    state["updated_at"] = __import__('datetime').datetime.now(
        __import__('datetime').timezone.utc
    ).isoformat()

    with open(ROTATION_FILE, "w") as f:
        json.dump(state, f, indent=2)

    return next_lang


def get_current_language() -> str:
    """Get the last selected language from rotation state."""
    state = get_rotation_state()
    return state.get("last_language", LANGUAGE_ROTATION[0])


def get_next_language() -> str:
    """Preview which language comes next in the rotation."""
    state = get_rotation_state()
    last = state.get("last_language", "")
    try:
        pos = LANGUAGE_ROTATION.index(last)
    except ValueError:
        pos = -1
    return LANGUAGE_ROTATION[(pos + 1) % len(LANGUAGE_ROTATION)]


# =============================================================================
# Pattern Query API
# =============================================================================

def get_pattern(pattern_id: str, language: Optional[str] = None) -> Pattern:
    """Get a pattern by ID, optionally filtered to a specific language."""
    if pattern_id not in ALL_PATTERNS:
        available = ", ".join(ALL_PATTERNS.keys())
        raise ValueError(f"Unknown pattern '{pattern_id}'. Available: {available}")
    pattern = ALL_PATTERNS[pattern_id]
    if language:
        lang_lower = language.lower().replace("#", "sharp").replace(" ", "")
        def matches(ex: PatternExample) -> bool:
            return ex.language.lower().replace("#", "sharp").replace(" ", "") == lang_lower
        filtered = [ex for ex in pattern.examples if matches(ex)]
        if not filtered:
            raise ValueError(
                f"Language '{language}' not found in pattern '{pattern_id}'. "
                f"Available: {[e.language for e in pattern.examples]}"
            )
        pattern = Pattern(
            id=pattern.id,
            name=pattern.name,
            description=pattern.description,
            category=pattern.category,
            examples=filtered,
        )
    return pattern


def get_all_patterns() -> List[Pattern]:
    """Get all available patterns."""
    return list(ALL_PATTERNS.values())


def get_patterns_by_category(category: str) -> List[Pattern]:
    """Get patterns filtered by category."""
    return [p for p in ALL_PATTERNS.values() if p.category == category]


def get_pattern_for_language(language: str) -> List[tuple]:
    """Get one pattern example per language (first pattern of each category)."""
    results = []
    for pattern in ALL_PATTERNS.values():
        for ex in pattern.examples:
            if ex.language == language:
                results.append((pattern, ex))
                break
    return results


def format_pattern_markdown(pattern: Pattern, language: Optional[str] = None) -> str:
    """Format a pattern as a markdown string for display."""
    lines = [
        f"## {pattern.name}",
        f"{pattern.description}",
        "",
        f"**Category:** {pattern.category}",
        "",
    ]
    examples = pattern.examples if not language else [
        ex for ex in pattern.examples if ex.language == language
    ]
    for ex in examples:
        style = LANGUAGE_META.get(ex.language, {}).get("style", ex.language.lower())
        lines.append(f"### {ex.language}")
        if ex.annotation:
            lines.append(f"*{ex.annotation}*")
        lines.append(f"```{style}")
        lines.append(ex.code.strip())
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


# =============================================================================
# Demo / CLI
# =============================================================================

def main():
    import sys
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print("""Polyglot Pattern Translation Utilities

Usage:
    python mod.py [pattern_id] [language]

Patterns:
    null_safety          Null/Option Safety
    error_handling       Error Handling with Result/Either
    concurrency          Concurrent Task Execution
    iteration            Iteration & Transformation
    function_composition Function Composition

Languages:
    Rust, Go, Swift, Kotlin, TypeScript, JavaScript, Java, C/C++

Examples:
    python mod.py                     # Show all patterns
    python mod.py null_safety         # Show null_safety pattern in all languages
    python mod.py iteration Rust      # Show iteration in Rust only
    python mod.py --rotation          # Show current rotation state
    python mod.py --advance           # Advance rotation and show next language
    python mod.py --list              # List all available patterns
    python mod.py --preview           # Preview all patterns in all languages (markdown)
    python mod.py --meta              # Show language metadata
    python mod.py --categories        # Show pattern categories
""")
        return

    if "--rotation" in args:
        state = get_rotation_state()
        current = get_current_language()
        next_lang = get_next_language()
        print(f"Current:  {current}")
        print(f"Next:     {next_lang}")
        print(f"Index:    {state.get('current_index', '?')}")
        print(f"Languages: {', '.join(state.get('languages', LANGUAGE_ROTATION))}")
        return

    if "--advance" in args:
        lang = advance_rotation()
        print(f"Advanced to: {lang}")
        return

    if "--list" in args:
        print("Available Patterns:")
        for p in ALL_PATTERNS.values():
            print(f"  {p.id:25s} [{p.category}] {p.name}")
        return

    if "--categories" in args:
        print("Pattern Categories:")
        for cat in sorted(set(p.category for p in ALL_PATTERNS.values())):
            print(f"  {cat}")
        return

    if "--meta" in args:
        print("Language Metadata:")
        for lang in LANGUAGE_ROTATION:
            meta = LANGUAGE_META.get(lang, {})
            print(f"  {lang:12s} | {meta.get('paradigm', ''):20s} | gc={str(meta.get('gc', '?')):5s} | {meta.get('null_safety', '')}")
        return

    if "--preview" in args:
        for p in ALL_PATTERNS.values():
            print(format_pattern_markdown(p))
        return

    pattern_id = args[0] if args else None
    language = args[1] if len(args) > 1 else None

    if pattern_id and pattern_id not in ALL_PATTERNS:
        print(f"ERROR: Unknown pattern '{pattern_id}'", file=sys.stderr)
        print(f"Available: {', '.join(ALL_PATTERNS.keys())}", file=sys.stderr)
        sys.exit(1)

    try:
        if pattern_id:
            pattern = get_pattern(pattern_id, language)
        else:
            pattern = NULL_PATTERNS
        print(format_pattern_markdown(pattern, language))
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()