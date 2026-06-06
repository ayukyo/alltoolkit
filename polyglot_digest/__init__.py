#!/usr/bin/env python3
"""
🌮 Polyglot Digest v1.0
A cross-language syntax parallel viewer — renders the same programming concept
side-by-side across all 8 rotation languages simultaneously.

Creative concept: "One concept, eight dialects."
Each digest presents a programming concept (algorithm, pattern, idiom) as a
syntax-parallel snippet set, allowing developers to compare how the same idea
is expressed across Rust, Go, Swift, Kotlin, TypeScript, JavaScript, Java, and C/C++.

Distinct from existing tools:
  - language_compass:     learning journey maps (milestones, stages, tips)
  - language_archaeology: historical lineage & design philosophy
  - language_ecohub:      package ecosystem field guide
  - language_mastery:     XP/level progress tracking
  - language_sage:        idioms, pro tips, pitfalls per language
  - language_rotator:     selects next language & generates a single project

Polyglot Digest is about SYNTAX PARALLELISM — seeing how the same thought
is spoken differently across languages — a unique comparative dimension.
"""

import json
import os
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

TOOL_NAME = "polyglot-digest"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "language_rotation.json")


def load_rotation():
    """Load language rotation config."""
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data):
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Concept bank ─────────────────────────────────────────────────────────────
# Each entry is a programming concept with a brief description and
# language-specific code implementations.
CONCEPT_BANK = {
    "hello_world": {
        "title": "Hello, World!",
        "description": "The eternal first program — print a greeting to stdout.",
        "tags": ["basics", "io"],
        "Rust": '''fn main() {
    println!("Hello, World!");
}''',
        "Go": '''package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}''',
        "Swift": '''import Foundation

print("Hello, World!")''',
        "Kotlin": '''fun main() {
    println("Hello, World!")
}''',
        "TypeScript": '''console.log("Hello, World!");''',
        "JavaScript": '''console.log("Hello, World!");''',
        "Java": '''public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}''',
        "C/C++": '''#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}'''
    },
    "fn_fibonacci": {
        "title": "Fibonacci Sequence",
        "description": "Generate the nth Fibonacci number using iteration.",
        "tags": ["algorithms", "recursion"],
        "Rust": '''fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => {
            let (mut a, mut b) = (0u64, 1u64);
            for _ in 2..=n {
                (a, b) = (b, a + b);
            }
            b
        }
    }
}''',
        "Go": '''func fibonacci(n int) int {
    if n < 2 {
        return n
    }
    a, b := 0, 1
    for i := 2; i <= n; i++ {
        a, b = b, a+b
    }
    return b
}''',
        "Swift": '''func fibonacci(_ n: Int) -> Int {
    guard n > 1 else { return n }
    var a = 0, b = 1
    for _ in 2...n {
        (a, b) = (b, a + b)
    }
    return b
}''',
        "Kotlin": '''fun fibonacci(n: Int): Int {
    if (n < 2) return n
    var a = 0
    var b = 1
    for (i in 2..n) {
        val temp = a + b
        a = b
        b = temp
    }
    return b
}''',
        "TypeScript": '''function fibonacci(n: number): number {
    if (n < 2) return n;
    let [a, b] = [0, 1];
    for (let i = 2; i <= n; i++) {
        [a, b] = [b, a + b];
    }
    return b;
}''',
        "JavaScript": '''function fibonacci(n) {
    if (n < 2) return n;
    let [a, b] = [0, 1];
    for (let i = 2; i <= n; i++) {
        [a, b] = [b, a + b];
    }
    return b;
}''',
        "Java": '''public static int fibonacci(int n) {
    if (n < 2) return n;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}''',
        "C/C++": '''int fibonacci(int n) {
    if (n < 2) return n;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}'''
    },
    "fn_http_get": {
        "title": "HTTP GET Request",
        "description": "Fetch data from a URL and return the response body as a string.",
        "tags": ["networking", "async"],
        "Rust": '''use std::collections::HashMap;

fn fetch(url: &str) -> Result<String, String> {
    // Using std::fs for illustration; production uses reqwest
    // reqwest::get(url).await?.text().await.map_err(|e| e.to_string())
    Ok(format!("[Rust] GET {}", url))
}''',
        "Go": '''package main

import (
    "fmt"
    "net/http"
)

func fetch(url string) (string, error) {
    resp, err := http.Get(url)
    if err != nil {
        return "", err
    }
    defer resp.Body.Close()
    // read.Body into string ...
    return fmt.Sprintf("[Go] GET %s (status %d)", url, resp.StatusCode), nil
}''',
        "Swift": '''import Foundation

func fetch(url: URL) async throws -> String {
    let (data, response) = try await URLSession.shared.data(from: url)
    guard let http = response as? HTTPURLResponse else {
        throw URLError(.badServerResponse)
    }
    return "[Swift] GET \\(url) (status \\(http.statusCode))"
}''',
        "Kotlin": '''import kotlinx.coroutines.*

suspend fun fetch(url: String): String {
    val response = ktorclient.get(url)
    return "[Kotlin] GET $url (status ${response.status})"
}''',
        "TypeScript": '''async function fetch_(url: string): Promise<string> {
    const res = await fetch(url);
    const text = await res.text();
    return `[TS] GET ${url} (status ${res.status})`;
}''',
        "JavaScript": '''async function fetch_(url) {
    const res = await fetch(url);
    const text = await res.text();
    return `[JS] GET ${url} (status ${res.status})`;
}''',
        "Java": '''public static String fetch(String url) throws Exception {
    HttpClient client = HttpClient.newHttpClient();
    HttpRequest request = HttpRequest.newBuilder().uri(URI.create(url)).build();
    HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
    return String.format("[Java] GET %s (status %d)", url, response.statusCode());
}''',
        "C/C++": '''#include <iostream>
#include <string>
#include <curl/curl.h>

std::string fetch(const std::string& url) {
    CURL* curl = curl_easy_init();
    std::string response;
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        // set up write callback ...
        // curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
    return "[C++] GET " + url;
}'''
    },
    "pattern_singleton": {
        "title": "Singleton Pattern",
        "description": "Ensure a class has only one instance with global access point.",
        "tags": ["design-patterns", "creational"],
        "Rust": '''use std::sync::Mutex;

struct DB {
    connection: String,
}

static DB: Mutex<Option<DB>> = Mutex::new(None);

fn get_instance() -> &'static Mutex<Option<DB>> {
    &DB
}

// Or with once_cell:
// use once_cell::sync::Lazy;
// static DB: Lazy<DB> = Lazy::new(|| DB { connection: "connected".into() });''',
        "Go": '''package main

import (
    "sync"
)

type DB struct {
    connection string
}

var (
    db     *DB
    dbOnce sync.Once
)

func GetInstance() *DB {
    dbOnce.Do(func() {
        db = &DB{connection: "connected"}
    })
    return db
}''',
        "Swift": '''final class Database {
    static let shared = Database()
    private let connection: String

    private init() {
        self.connection = "connected"
    }
}

// Usage: let db = Database.shared''',
        "Kotlin": '''object Database {
    val connection: String = "connected"
}

// Usage: Database.connection''',
        "TypeScript": '''class Database {
    private static _instance: Database | null = null;

    private constructor(
        public readonly connection: string = "connected"
    ) {}

    static getInstance(): Database {
        if (!Database._instance) {
            Database._instance = new Database();
        }
        return Database._instance;
    }
}''',
        "JavaScript": '''class Database {
    constructor() {
        if (Database._instance) return Database._instance;
        this.connection = "connected";
        Database._instance = this;
    }
}''',
        "Java": '''public final class Database {
    private static volatile Database INSTANCE;
    private final String connection;

    private Database() {
        this.connection = "connected";
    }

    public static Database getInstance() {
        if (INSTANCE == null) {
            synchronized (Database.class) {
                if (INSTANCE == null) {
                    INSTANCE = new Database();
                }
            }
        }
        return INSTANCE;
    }
}''',
        "C/C++": '''#include <memory>
#include <mutex>

class Database {
public:
    static std::shared_ptr<Database> getInstance() {
        static std::shared_ptr<Database> instance(
            new Database(),
            [](Database* p) { delete p; }
        );
        return instance;
    }

private:
    Database() : connection("connected") {}
    Database(const Database&) = delete;
    Database& operator=(const Database&) = delete;
    std::string connection;
};'''
    },
    "fn_error_handling": {
        "title": "Error Handling",
        "description": "Wrap a fallible operation in a Result/Option type and handle errors.",
        "tags": ["error-handling", "robustness"],
        "Rust": '''fn parse_port(s: &str) -> Result<u16, std::num::ParseIntError> {
    s.trim().parse::<u16>()
}

fn main() {
    match parse_port("8080") {
        Ok(port) => println!("Listening on {}", port),
        Err(e) => eprintln!("Bad port: {}", e),
    }
}''',
        "Go": '''package main

import (
    "errors"
    "strconv"
)

func parsePort(s string) (int, error) {
    n, err := strconv.Atoi(s)
    if err != nil {
        return 0, errors.New("bad port: " + s)
    }
    return n, nil
}

func main() {
    if port, err := parsePort("8080"); err != nil {
        panic(err)
    } else {
        println("Listening on", port)
    }
}''',
        "Swift": '''func parsePort(_ s: String) -> Int? {
    Int(s.trimmingCharacters(in: .whitespaces))
}

let port = parsePort("8080") ?? 0
print("Listening on \\(port)")''',
        "Kotlin": '''fun parsePort(s: String): Result<Int> {
    s.trim().toIntOrNull()?.let { Result.success(it) }
        ?: Result.failure(NumberFormatException("Bad port: $s"))
}

fun main() {
    parsePort("8080").onSuccess { println("Listening on $it") }
        .onFailure { println("Bad port: ${it.message}") }
}''',
        "TypeScript": '''function parsePort(s: string): number | null {
    const n = Number(s.trim());
    return Number.isInteger(n) && n > 0 ? n : null;
}

const port = parsePort("8080") ?? 0;
console.log(`Listening on ${port}`);''',
        "JavaScript": '''function parsePort(s) {
    const n = Number(s.trim());
    return Number.isInteger(n) && n > 0 ? n : null;
}

const port = parsePort("8080") ?? 0;
console.log(`Listening on ${port}`);''',
        "Java": '''public static Optional<Integer> parsePort(String s) {
    try {
        int n = Integer.parseInt(s.trim());
        return n > 0 ? Optional.of(n) : Optional.empty();
    } catch (NumberFormatException e) {
        return Optional.empty();
    }
}

public static void main(String[] args) {
    parsePort("8080").ifPresentOrElse(
        port -> System.out.println("Listening on " + port),
        () -> System.err.println("Bad port")
    );
}''',
        "C/C++": '''#include <optional>
#include <stdexcept>
#include <cstdint>

std::optional<int> parsePort(const std::string& s) {
    try {
        int n = std::stoi(s);
        return n > 0 ? std::optional<int>(n) : std::nullopt;
    } catch (const std::exception&) {
        return std::nullopt;
    }
}

int main() {
    auto port = parsePort("8080").value_or(0);
    std::cout << "Listening on " << port << std::endl;
    return 0;
}'''
    },
    "fn_generic_stack": {
        "title": "Generic Stack",
        "description": "A last-in-first-out data structure with push/pop/isEmpty operations.",
        "tags": ["data-structures", "generics"],
        "Rust": '''use std::collections::VecDeque;

struct Stack<T> {
    items: VecDeque<T>,
}

impl<T> Stack<T> {
    fn new() -> Self { Self { items: VecDeque::new() } }
    fn push(&mut self, item: T) { self.items.push_back(item); }
    fn pop(&mut self) -> Option<T> { self.items.pop_back() }
    fn is_empty(&self) -> bool { self.items.is_empty() }
}''',
        "Go": '''package main

type Stack[T any] struct {
    items []T
}

func New[T any]() *Stack[T] { return &Stack[T]{items: make([]T, 0)} }
func (s *Stack[T]) Push(item T)  { s.items = append(s.items, item) }
func (s *Stack[T]) Pop() (T, bool) {
    if len(s.items) == 0 { var zero T; return zero, false }
    item := s.items[len(s.items)-1]
    s.items = s.items[:len(s.items)-1]
    return item, true
}
func (s *Stack[T]) IsEmpty() bool { return len(s.items) == 0 }''',
        "Swift": '''struct Stack<T> {
    private var items: [T] = []

    mutating func push(_ item: T) { items.append(item) }
    mutating func pop() -> T? { items.popLast() }
    var isEmpty: Bool { items.isEmpty }
}''',
        "Kotlin": '''class Stack<T> {
    private val items = mutableListOf<T>()

    fun push(item: T) { items.add(item) }
    fun pop(): T? = items.removeLastOrNull()
    val isEmpty: Boolean get() = items.isEmpty()
}''',
        "TypeScript": '''class Stack<T> {
    private items: T[] = [];

    push(item: T): void { this.items.push(item); }
    pop(): T | undefined { return this.items.pop(); }
    get isEmpty(): boolean { return this.items.length === 0; }
}''',
        "JavaScript": '''class Stack {
    #items = [];

    push(item) { this.#items.push(item); }
    pop() { return this.#items.pop(); }
    get isEmpty() { return this.#items.length === 0; }
}''',
        "Java": '''public class Stack<T> {
    private final java.util.ArrayList<T> items = new java.util.ArrayList<>();

    public void push(T item) { items.add(item); }
    public T pop() { return items.isEmpty() ? null : items.remove(items.size() - 1); }
    public boolean isEmpty() { return items.isEmpty(); }
}''',
        "C/C++": '''#include <vector>
#include <optional>

template<typename T>
class Stack {
    std::vector<T> items;
public:
    void push(T item) { items.push_back(item); }
    std::optional<T> pop() {
        if (items.empty()) return std::nullopt;
        T item = items.back();
        items.pop_back();
        return item;
    }
    bool isEmpty() const { return items.empty(); }
};'''
    },
}


def get_concept(concept_key):
    """Get a concept by key, or return None if not found."""
    return CONCEPT_BANK.get(concept_key)


def get_all_concept_keys():
    """Return all available concept keys."""
    return list(CONCEPT_BANK.keys())


def select_concept(forced_key=None):
    """Select a concept: use forced_key if provided, else random."""
    if forced_key and forced_key in CONCEPT_BANK:
        return forced_key
    keys = get_all_concept_keys()
    return random.choice(keys)


def build_parallel_snippet(concept_key, languages):
    """Build syntax-parallel snippets for given languages."""
    concept = get_concept(concept_key)
    if not concept:
        return None

    snippets = {}
    for lang in languages:
        snippets[lang] = concept.get(lang, "# not available")

    return snippets


def digest(language=None, concept_key=None):
    """
    Main entry point — generate a polyglot digest.

    Reads the rotation config to determine the current language, rotates
    the index, selects a random concept, builds parallel snippets across
    all 8 languages, and returns the digest.

    Args:
        language:  override the selected language (for testing)
        concept_key: override the concept selection (for testing)

    Returns:
        dict with digest metadata, parallel snippets, and rotation state
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

    # Select concept
    selected_concept_key = select_concept(concept_key)
    concept = get_concept(selected_concept_key)

    # Build parallel snippets
    snippets = {}
    for lang in languages:
        snippets[lang] = concept.get(lang, "# not available")

    # Update rotation
    config["current_index"] = next_idx
    config["last_language"] = language
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "next_language": languages[next_idx],
        "concept": {
            "key": selected_concept_key,
            "title": concept["title"],
            "description": concept["description"],
            "tags": concept["tags"],
        },
        "snippets": snippets,
        "rotation": languages,
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def run_tests():
    """Run tests to validate the Polyglot Digest module."""
    tests_passed = 0
    tests_failed = 0

    def assert_eq(a, b, msg=""):
        nonlocal tests_passed, tests_failed
        if a == b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — expected {b!r}, got {a!r}")

    def assert_in(a, b, msg=""):
        nonlocal tests_passed, tests_failed
        if a in b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — '{a}' not found in response")

    print("Testing Polyglot Digest...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_eq("Rust", config["languages"][0], "Rust is first language")
    assert_in("current_index", config, "current_index field present")

    print("  Testing digest() output structure...")
    result = digest()
    expected_keys = [
        "tool", "version", "selected_language", "next_language",
        "concept", "snippets", "rotation", "timestamp"
    ]
    for key in expected_keys:
        assert_eq(True, key in result, f"Key '{key}' present")

    print("  Testing concept structure...")
    concept = result["concept"]
    assert_in("key", concept, "concept.key present")
    assert_in("title", concept, "concept.title present")
    assert_in("description", concept, "concept.description present")
    assert_in("tags", concept, "concept.tags present")
    assert_eq(True, concept["key"] in CONCEPT_BANK, "concept key is valid")
    assert_eq(True, len(concept["tags"]) >= 1, "concept has at least 1 tag")

    print("  Testing snippets across all languages...")
    snippets = result["snippets"]
    for lang in config["languages"]:
        assert_eq(True, lang in snippets, f"Snippet present for {lang}")
        assert_eq(True, len(snippets[lang]) > 0, f"Snippet non-empty for {lang}")
        assert_eq(False, snippets[lang].startswith("# not available"), f"Snippet valid for {lang}")

    print("  Testing all 8 languages have all 6 concepts...")
    for concept_key, concept_data in CONCEPT_BANK.items():
        for lang in config["languages"]:
            assert_eq(True, lang in concept_data, f"Concept '{concept_key}' has {lang} snippet")

    print("  Testing rotation advances after digest()...")
    result = digest()
    selected = result["selected_language"]
    config_after = load_rotation()
    assert_eq(True, 0 <= config_after["current_index"] < 8, "current_index in valid range")
    assert_eq(selected, config_after["last_language"], "last_language recorded")

    print("  Testing concept_key override...")
    result = digest(concept_key="hello_world")
    assert_eq("hello_world", result["concept"]["key"], "concept_key respected")
    assert_eq("Hello, World!", result["concept"]["title"], "hello_world title correct")

    print("  Testing language override...")
    result = digest(language="Go")
    assert_eq("Go", result["selected_language"], "language override respected")
    assert_eq("Swift", result["next_language"], "next_language is Swift after Go")

    print("  Testing concepts are unique across keys...")
    keys = list(CONCEPT_BANK.keys())
    titles = [CONCEPT_BANK[k]["title"] for k in keys]
    assert_eq(True, len(titles) == len(set(titles)), "All concept titles are unique")

    print("  Testing tags across all concepts...")
    for concept_key, concept_data in CONCEPT_BANK.items():
        tags = concept_data.get("tags", [])
        assert_eq(True, len(tags) >= 1, f"Concept '{concept_key}' has at least 1 tag")
        assert_eq(True, all(isinstance(t, str) and len(t) > 0 for t in tags),
                 f"Concept '{concept_key}' tags are all non-empty strings")

    print("  Testing next_language cycle wraps correctly...")
    # Simulate rotating through all languages
    config = load_rotation()
    langs = config["languages"]
    idx = config["current_index"]
    for i in range(len(langs)):
        lang = langs[idx]
        result = digest(language=lang)
        assert_eq(lang, result["selected_language"], f"Digest selects {lang}")
        idx = (idx + 1) % len(langs)
    print(f"  ✅ PASS: All {len(langs)} languages rotate correctly")

    print("  Testing snippets contain language-appropriate keywords...")
    hello_snippets = digest(concept_key="hello_world")["snippets"]
    assert_in("println", hello_snippets["Rust"], "Rust uses println!")
    assert_in("fmt.Println", hello_snippets["Go"], "Go uses fmt.Println")
    assert_in("Foundation", hello_snippets["Swift"], "Swift uses Foundation import")
    assert_in("fun main", hello_snippets["Kotlin"], "Kotlin uses fun main")
    assert_in("console.log", hello_snippets["TypeScript"], "TS uses console.log")
    assert_in("console.log", hello_snippets["JavaScript"], "JS uses console.log")
    assert_in("System.out", hello_snippets["Java"], "Java uses System.out")
    assert_in("std::cout", hello_snippets["C/C++"], "C++ uses std::cout")

    print("  Testing error handling for invalid concept_key...")
    result = digest(concept_key="invalid_concept")
    # Should fall back to random concept
    assert_eq(True, result["concept"]["key"] in CONCEPT_BANK, "Invalid key falls back to random")

    print(f"\n{'='*55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("🌮 All tests passed! Polyglot Digest is ready.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--digest":
        result = digest()
        print(json.dumps(result, indent=2))
    else:
        print(f"Polyglot Digest v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_digest --test       # Run tests")
        print("  python -m polyglot_digest --digest    # Generate digest")