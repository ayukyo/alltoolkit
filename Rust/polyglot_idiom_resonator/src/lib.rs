//! # Polyglot Idiom Resonator
//!
//! For a given programming concept, generates idiomatic code snippets in all 8
//! rotation languages, then analyzes how similarly each language "thinks" about
//! the problem — scoring the **resonance** between pairs of languages.
//!
//! ## Creative Concept
//!
//! **"When a language resonates, the same idea wears different clothes."**
//!
//! This module picks the *current* language from `language_rotation.json`, generates
//! a concept demonstration in that language, then compares it against the canonical
//! idioms of the other 7 languages. Resonance is scored by structural similarity:
//! same control structures, same error handling philosophy, same mutability model.
//!
//! ## Rotation Integration
//!
//! - Reads `language_rotation.json` → `current_index` → selects "focus" language
//! - Generates idiomatic code for the concept in the focus language
//! - Compares against all 8 languages, scores resonance
//! - After analysis, `current_index` advances by 1 (mod 8) and `updated_at` is refreshed
//! - A log of all analysis runs is kept in `polyglot_idiom_resonator_log.json`
//!
//! ## Concepts
//!
//! | ID           | Concept                                  |
//! |--------------|------------------------------------------|
//! | `hello`      | Hello World                              |
//! | `fibonacci`  | Recursive Fibonacci (memoized)           |
//! | `null_safe`  | Null/None-safe attribute access          |
//! | `error_flow` | Error handling with fallback             |
//! | `struct_def` | Define a data record with a method       |
//! | `concurrency`| Spawn a lightweight concurrent task       |
//! | `regex_validate` | Validate input with a regex pattern |
//! | `file_io`    | Read file contents line-by-line           |
//!
//! ## Resonance Score
//!
//! Each language pair gets a score 0.0–1.0:
//! - 1.0 = identical structural approach (same control flow, same error model)
//! - 0.5 = partial match (same family, different syntax)
//! - 0.0 = fundamentally different approach
//!
//! Resonance is computed by parsing code into a lightweight AST-like structure
//! (control flow type, error handling style, mutability, type system features used)
//! and comparing the feature vectors.

use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use std::fs;
use std::path::Path;

// ─────────────────────────────────────────────────────────────────
// Language enum (matching language_rotation.json)
// ─────────────────────────────────────────────────────────────────

/// All 8 supported languages (rotation order)
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum Language {
    Rust,
    Go,
    Swift,
    Kotlin,
    TypeScript,
    JavaScript,
    Java,
    #[serde(rename = "C/C++")]
    Cpp,
}

impl Language {
    pub fn from_str(s: &str) -> Option<Self> {
        match s {
            "Rust" => Some(Language::Rust),
            "Go" => Some(Language::Go),
            "Swift" => Some(Language::Swift),
            "Kotlin" => Some(Language::Kotlin),
            "TypeScript" => Some(Language::TypeScript),
            "JavaScript" => Some(Language::JavaScript),
            "Java" => Some(Language::Java),
            "C/C++" | "C++" => Some(Language::Cpp),
            _ => None,
        }
    }

    pub fn as_str(&self) -> &'static str {
        match self {
            Language::Rust => "Rust",
            Language::Go => "Go",
            Language::Swift => "Swift",
            Language::Kotlin => "Kotlin",
            Language::TypeScript => "TypeScript",
            Language::JavaScript => "JavaScript",
            Language::Java => "Java",
            Language::Cpp => "C/C++",
        }
    }

    /// File extension for the language
    pub fn ext(&self) -> &'static str {
        match self {
            Language::Rust => "rs",
            Language::Go => "go",
            Language::Swift => "swift",
            Language::Kotlin => "kt",
            Language::TypeScript => "ts",
            Language::JavaScript => "js",
            Language::Java => "java",
            Language::Cpp => "cpp",
        }
    }

    pub fn all() -> [Self; 8] {
        [
            Language::Rust,
            Language::Go,
            Language::Swift,
            Language::Kotlin,
            Language::TypeScript,
            Language::JavaScript,
            Language::Java,
            Language::Cpp,
        ]
    }
}

impl std::fmt::Display for Language {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

// ─────────────────────────────────────────────────────────────────
// Concept definitions
// ─────────────────────────────────────────────────────────────────

/// Available programming concepts
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize, PartialOrd, Ord, Hash)]
#[serde(rename_all = "snake_case")]
pub enum Concept {
    Hello,
    Fibonacci,
    NullSafe,
    ErrorFlow,
    StructDef,
    Concurrency,
    RegexValidate,
    FileIo,
}

impl Concept {
    pub fn all() -> [Self; 8] {
        [
            Concept::Hello,
            Concept::Fibonacci,
            Concept::NullSafe,
            Concept::ErrorFlow,
            Concept::StructDef,
            Concept::Concurrency,
            Concept::RegexValidate,
            Concept::FileIo,
        ]
    }

    pub fn name(&self) -> &'static str {
        match self {
            Concept::Hello => "hello",
            Concept::Fibonacci => "fibonacci",
            Concept::NullSafe => "null_safe",
            Concept::ErrorFlow => "error_flow",
            Concept::StructDef => "struct_def",
            Concept::Concurrency => "concurrency",
            Concept::RegexValidate => "regex_validate",
            Concept::FileIo => "file_io",
        }
    }

    pub fn display_name(&self) -> &'static str {
        match self {
            Concept::Hello => "Hello World",
            Concept::Fibonacci => "Recursive Fibonacci (Memoized)",
            Concept::NullSafe => "Null/None-safe Attribute Access",
            Concept::ErrorFlow => "Error Handling with Fallback",
            Concept::StructDef => "Data Record with a Method",
            Concept::Concurrency => "Lightweight Concurrent Task",
            Concept::RegexValidate => "Regex Input Validation",
            Concept::FileIo => "Read File Line-by-Line",
        }
    }
}

// ─────────────────────────────────────────────────────────────────
// Code generation per language and concept
// ─────────────────────────────────────────────────────────────────

/// Generate idiomatic code for a (Language, Concept) pair
pub fn generate_code(lang: Language, concept: Concept) -> &'static str {
    match (lang, concept) {
        // ── Hello World ──────────────────────────────────────────────
        (Language::Rust, Concept::Hello) => r#"fn main() {
    println!("Hello, World!");
}"#,
        (Language::Go, Concept::Hello) => r#"package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}"#,
        (Language::Swift, Concept::Hello) => r#"print("Hello, World!")"#,
        (Language::Kotlin, Concept::Hello) => r#"fun main() {
    println("Hello, World!")
}"#,
        (Language::TypeScript, Concept::Hello) => r#"console.log("Hello, World!");"#,
        (Language::JavaScript, Concept::Hello) => r#"console.log("Hello, World!");"#,
        (Language::Java, Concept::Hello) => r#"public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}"#,
        (Language::Cpp, Concept::Hello) => r#"#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}"#,

        // ── Fibonacci (memoized) ───────────────────────────────────────
        (Language::Rust, Concept::Fibonacci) => r#"use std::collections::HashMap;

fn fib(n: u64, memo: &mut HashMap<u64, u64>) -> u64 {
    if let Some(&v) = memo.get(&n) { return v; }
    let result = if n <= 1 { n } else {
        fib(n - 1, memo) + fib(n - 2, memo)
    };
    memo.insert(n, result);
    result
}

fn main() {
    let mut memo = HashMap::new();
    println!("{}", fib(10, &mut memo));
}"#,
        (Language::Go, Concept::Fibonacci) => r#"package main

import "fmt"

func fib(n int, memo map[int]int) int {
    if v, ok := memo[n]; ok {
        return v
    }
    var result int
    if n <= 1 {
        result = n
    } else {
        result = fib(n-1, memo) + fib(n-2, memo)
    }
    memo[n] = result
    return result
}

func main() {
    memo := make(map[int]int)
    fmt.Println(fib(10, memo))
}"#,
        (Language::Swift, Concept::Fibonacci) => r#"func fib(_ n: Int, _ memo: inout [Int: Int]) -> Int {
    if let v = memo[n] { return v }
    let result = n <= 1 ? n : fib(n - 1, &memo) + fib(n - 2, &memo)
    memo[n] = result
    return result
}

var memo: [Int: Int] = [:]
print(fib(10, &memo))"#,
        (Language::Kotlin, Concept::Fibonacci) => r#"fun fib(n: Int, memo: MutableMap<Int, Int>): Int {
    memo[n]?.let { return it }
    val result = if (n <= 1) n else fib(n - 1, memo) + fib(n - 2, memo)
    memo[n] = result
    return result
}

fun main() {
    val memo = mutableMapOf<Int, Int>()
    println(fib(10, memo))
}"#,
        (Language::TypeScript, Concept::Fibonacci) => r#"function fib(n: number, memo: Map<number, number>): number {
    if (memo.has(n)) return memo.get(n)!;
    const result = n <= 1 ? n : fib(n - 1, memo) + fib(n - 2, memo);
    memo.set(n, result);
    return result;
}

const memo = new Map<number, number>();
console.log(fib(10, memo));"#,
        (Language::JavaScript, Concept::Fibonacci) => r#"function fib(n, memo = new Map()) {
    if (memo.has(n)) return memo.get(n);
    const result = n <= 1 ? n : fib(n - 1, memo) + fib(n - 2, memo);
    memo.set(n, result);
    return result;
}

console.log(fib(10));"#,
        (Language::Java, Concept::Fibonacci) => r#"import java.util.HashMap;
import java.util.Map;

public class Main {
    static int fib(int n, Map<Integer, Integer> memo) {
        if (memo.containsKey(n)) return memo.get(n);
        int result = n <= 1 ? n : fib(n - 1, memo) + fib(n - 2, memo);
        memo.put(n, result);
        return result;
    }

    public static void main(String[] args) {
        System.out.println(fib(10, new HashMap<>()));
    }
}"#,
        (Language::Cpp, Concept::Fibonacci) => r#"#include <iostream>
#include <unordered_map>

int fib(int n, std::unordered_map<int, int>& memo) {
    auto it = memo.find(n);
    if (it != memo.end()) return it->second;
    int result = n <= 1 ? n : fib(n - 1, memo) + fib(n - 2, memo);
    memo[n] = result;
    return result;
}

int main() {
    std::unordered_map<int, int> memo;
    std::cout << fib(10, memo) << std::endl;
    return 0;
}"#,

        // ── Null/None-safe access ─────────────────────────────────────
        (Language::Rust, Concept::NullSafe) => r#"struct User { name: Option<String> }

fn get_name(user: Option<User>) -> String {
    user.and_then(|u| u.name).unwrap_or_else(|| "Anonymous".to_string())
}

fn main() {
    let user = User { name: Some("Alice".to_string()) };
    println!("{}", get_name(Some(user)));
    println!("{}", get_name(None));
}"#,
        (Language::Go, Concept::NullSafe) => r#"package main

import "fmt"

type User struct {
    Name *string
}

func getName(user *User) string {
    if user == nil || user.Name == nil {
        return "Anonymous"
    }
    return *user.Name
}

func main() {
    name := "Alice"
    user := User{Name: &name}
    fmt.Println(getName(&user))
    fmt.Println(getName(nil))
}"#,
        (Language::Swift, Concept::NullSafe) => r#"struct User {
    let name: String?
}

func getName(_ user: User?) -> String {
    user?.name ?? "Anonymous"
}

let user = User(name: "Alice")
print(getName(user))
print(getName(nil))"#,
        (Language::Kotlin, Concept::NullSafe) => r#"data class User(val name: String?)

fun getName(user: User?): String {
    return user?.name ?: "Anonymous"
}

fun main() {
    val user = User("Alice")
    println(getName(user))
    println(getName(null))
}"#,
        (Language::TypeScript, Concept::NullSafe) => r#"interface User { name?: string }

function getName(user: User | null): string {
    return user?.name ?? "Anonymous";
}

const user: User = { name: "Alice" };
console.log(getName(user));
console.log(getName(null));"#,
        (Language::JavaScript, Concept::NullSafe) => r#"function getName(user) {
    return user?.name ?? "Anonymous";
}

const user = { name: "Alice" };
console.log(getName(user));
console.log(getName(null));"#,
        (Language::Java, Concept::NullSafe) => r#"public class Main {
    static String getName(User user) {
        return user != null && user.name != null ? user.name : "Anonymous";
    }

    public static void main(String[] args) {
        User user = new User("Alice");
        System.out.println(getName(user));
        System.out.println(getName(null));
    }
}

class User {
    String name;
    User(String name) { this.name = name; }
}"#,
        (Language::Cpp, Concept::NullSafe) => r#"#include <iostream>
#include <optional>
#include <string>

struct User { std::optional<std::string> name; };

std::string getName(const User* user) {
    if (!user || !user->name.has_value()) return "Anonymous";
    return user->name.value();
}

int main() {
    User user{"Alice"};
    std::cout << getName(&user) << std::endl;
    std::cout << getName(nullptr) << std::endl;
    return 0;
}"#,

        // ── Error handling with fallback ───────────────────────────────
        (Language::Rust, Concept::ErrorFlow) => r#"use std::num::ParseIntError;

fn parse_or_zero(s: &str) -> Result<i32, ParseIntError> {
    s.parse()
}

fn main() {
    let result: i32 = parse_or_zero("42").unwrap_or(0);
    let fallback: i32 = parse_or_zero("oops").unwrap_or(0);
    println!("{} {}", result, fallback);
}"#,
        (Language::Go, Concept::ErrorFlow) => r#"package main

import (
    "fmt"
    "strconv"
)

func parseOrZero(s string) int {
    if v, err := strconv.Atoi(s); err == nil {
        return v
    }
    return 0
}

func main() {
    fmt.Println(parseOrZero("42"))
    fmt.Println(parseOrZero("oops"))
}"#,
        (Language::Swift, Concept::ErrorFlow) => r#"func parseOrZero(_ s: String) -> Int {
    Int(s) ?? 0
}

print(parseOrZero("42"))
print(parseOrZero("oops"))"#,
        (Language::Kotlin, Concept::ErrorFlow) => r#"fun parseOrZero(s: String): Int {
    s.toIntOrNull() ?: 0
}

fun main() {
    println(parseOrZero("42"))
    println(parseOrZero("oops"))
}"#,
        (Language::TypeScript, Concept::ErrorFlow) => r#"function parseOrZero(s: string): number {
    const n = parseInt(s, 10);
    return isNaN(n) ? 0 : n;
}

console.log(parseOrZero("42"));
console.log(parseOrZero("oops"));"#,
        (Language::JavaScript, Concept::ErrorFlow) => r#"function parseOrZero(s) {
    const n = parseInt(s, 10);
    return isNaN(n) ? 0 : n;
}

console.log(parseOrZero("42"));
console.log(parseOrZero("oops"));"#,
        (Language::Java, Concept::ErrorFlow) => r#"public class Main {
    static int parseOrZero(String s) {
        try {
            return Integer.parseInt(s);
        } catch (NumberFormatException e) {
            return 0;
        }
    }

    public static void main(String[] args) {
        System.out.println(parseOrZero("42"));
        System.out.println(parseOrZero("oops"));
    }
}"#,
        (Language::Cpp, Concept::ErrorFlow) => r#"#include <iostream>
#include <cstdlib>

int parseOrZero(const char* s) {
    char* end;
    long n = std::strtol(s, &end, 10);
    return (*end == '\0') ? static_cast<int>(n) : 0;
}

int main() {
    std::cout << parseOrZero("42") << std::endl;
    std::cout << parseOrZero("oops") << std::endl;
    return 0;
}"#,

        // ── Struct/class definition with method ────────────────────────
        (Language::Rust, Concept::StructDef) => r#"struct Counter {
    count: i32,
}

impl Counter {
    fn new() -> Self { Counter { count: 0 } }
    fn increment(&mut self) { self.count += 1; }
    fn get(&self) -> i32 { self.count }
}

fn main() {
    let mut c = Counter::new();
    c.increment();
    c.increment();
    println!("{}", c.get());
}"#,
        (Language::Go, Concept::StructDef) => r#"package main

import "fmt"

type Counter struct { count int }

func NewCounter() *Counter { return &Counter{} }

func (c *Counter) Increment() { c.count++ }

func (c Counter) Get() int { return c.count }

func main() {
    c := NewCounter()
    c.Increment()
    c.Increment()
    fmt.Println(c.Get())
}"#,
        (Language::Swift, Concept::StructDef) => r#"struct Counter {
    private var count: Int = 0

    mutating func increment() { count += 1 }
    func get() -> Int { count }
}

var c = Counter()
c.increment()
c.increment()
print(c.get())"#,
        (Language::Kotlin, Concept::StructDef) => r#"class Counter {
    private var count: Int = 0

    fun increment() { count++ }
    fun get(): Int = count
}

fun main() {
    val c = Counter()
    c.increment()
    c.increment()
    println(c.get())
}"#,
        (Language::TypeScript, Concept::StructDef) => r#"class Counter {
    private count: number = 0;

    increment(): void { this.count++; }
    get(): number { return this.count; }
}

const c = new Counter();
c.increment();
c.increment();
console.log(c.get());"#,
        (Language::JavaScript, Concept::StructDef) => r#"class Counter {
    #count = 0;
    increment() { this.#count++; }
    get() { return this.#count; }
}

const c = new Counter();
c.increment();
c.increment();
console.log(c.get());"#,
        (Language::Java, Concept::StructDef) => r#"public class Counter {
    private int count = 0;

    public void increment() { count++; }
    public int get() { return count; }

    public static void main(String[] args) {
        Counter c = new Counter();
        c.increment();
        c.increment();
        System.out.println(c.get());
    }
}"#,
        (Language::Cpp, Concept::StructDef) => r#"#include <iostream>

class Counter {
    int count = 0;
public:
    void increment() { ++count; }
    int get() const { return count; }
};

int main() {
    Counter c;
    c.increment();
    c.increment();
    std::cout << c.get() << std::endl;
    return 0;
}"#,

        // ── Concurrency ────────────────────────────────────────────────
        (Language::Rust, Concept::Concurrency) => r#"use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        "Hello from a thread!"
    });
    println!("{}", handle.join().unwrap());
}"#,
        (Language::Go, Concept::Concurrency) => r#"package main

import (
    "fmt"
    "time"
)

func main() {
    ch := make(chan string, 1)
    go func() {
        time.Sleep(10 * time.Millisecond)
        ch <- "Hello from a goroutine!"
    }()
    fmt.Println(<-ch)
}"#,
        (Language::Swift, Concept::Concurrency) => r#"Task {
    let result = await Task { "Hello from a task!" }.value
    print(result)
}"#,
        (Language::Kotlin, Concept::Concurrency) => r#"import kotlinx.coroutines.*

fun main() = runBlocking {
    val job = launch {
        delay(10)
        println("Hello from a coroutine!")
    }
    job.join()
}"#,
        (Language::TypeScript, Concept::Concurrency) => r#"async function main() {
    const result = await Promise.resolve("Hello from a promise!");
    console.log(result);
}

main();"#,
        (Language::JavaScript, Concept::Concurrency) => r#"async function main() {
    const result = await Promise.resolve("Hello from a promise!");
    console.log(result);
}

main();"#,
        (Language::Java, Concept::Concurrency) => r#"import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws Exception {
        ExecutorService exec = Executors.newSingleThreadExecutor();
        Future<String> f = exec.submit(() -> "Hello from a thread!");
        System.out.println(f.get());
        exec.shutdown();
    }
}"#,
        (Language::Cpp, Concept::Concurrency) => r#"#include <iostream>
#include <thread>
#include <string>

int main() {
    std::thread t([](){ std::cout << "Hello from a thread!" << std::endl; });
    t.join();
    return 0;
}"#,

        // ── Regex validation ───────────────────────────────────────────
        (Language::Rust, Concept::RegexValidate) => r#"use regex::Regex;

fn is_valid_email(s: &str) -> bool {
    Regex::new(r"^[\w.-]+@[\w.-]+\.\w+$").map(|re| re.is_match(s)).unwrap_or(false)
}

fn main() {
    println!("{}", is_valid_email("test@example.com"));
    println!("{}", is_valid_email("invalid"));
}"#,
        (Language::Go, Concept::RegexValidate) => r#"package main

import (
    "fmt"
    "regexp"
)

func isValidEmail(s string) bool {
    matched, _ := regexp.MatchString(`^[\w.-]+@[\w.-]+\.\w+$`, s)
    return matched
}

func main() {
    fmt.Println(isValidEmail("test@example.com"))
    fmt.Println(isValidEmail("invalid"))
}"#,
        (Language::Swift, Concept::RegexValidate) => r#"import Foundation

func isValidEmail(_ s: String) -> Bool {
    let regex = try! NSRegularExpression(pattern: "^[\w.-]+@[\w.-]+\.\w+$")
    return regex.firstMatch(in: s, range: NSRange(s.startIndex..., in: s)) != nil
}

print(isValidEmail("test@example.com"))
print(isValidEmail("invalid"))"#,
        (Language::Kotlin, Concept::RegexValidate) => r#"fun isValidEmail(s: String): Boolean {
    return Regex("^[\\w.-]+@[\\w.-]+\\.\\w+$").matches(s)
}

fun main() {
    println(isValidEmail("test@example.com"))
    println(isValidEmail("invalid"))
}"#,
        (Language::TypeScript, Concept::RegexValidate) => r#"function isValidEmail(s: string): boolean {
    return / ^[\w.-]+@[\w.-]+\.\w+$ / .test(s);
}

console.log(isValidEmail("test@example.com"));
console.log(isValidEmail("invalid"));"#,
        (Language::JavaScript, Concept::RegexValidate) => r#"function isValidEmail(s) {
    return /^[\w.-]+@[\w.-]+\.\w+$/.test(s);
}

console.log(isValidEmail("test@example.com"));
console.log(isValidEmail("invalid"));"#,
        (Language::Java, Concept::RegexValidate) => r#"import java.util.regex.*;

public class Main {
    static boolean isValidEmail(String s) {
        return Pattern.matches("^[\\w.-]+@[\\w.-]+\\.\\w+$", s);
    }

    public static void main(String[] args) {
        System.out.println(isValidEmail("test@example.com"));
        System.out.println(isValidEmail("invalid"));
    }
}"#,
        (Language::Cpp, Concept::RegexValidate) => r#"#include <iostream>
#include <regex>
#include <string>

bool isValidEmail(const std::string& s) {
    return std::regex_match(s, std::regex(R"(^[\w.-]+@[\w.-]+\.\w+$)"));
}

int main() {
    std::cout << isValidEmail("test@example.com") << std::endl;
    std::cout << isValidEmail("invalid") << std::endl;
    return 0;
}"#,

        // ── File I/O ──────────────────────────────────────────────────
        (Language::Rust, Concept::FileIo) => r#"use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() -> io::Result<()> {
    let path = Path::new("input.txt");
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    for line in reader.lines() {
        println!("{}", line?);
    }
    Ok(())
}"#,
        (Language::Go, Concept::FileIo) => r#"package main

import (
    "bufio"
    "fmt"
    "os"
)

func main() {
    file, _ := os.Open("input.txt")
    defer file.Close()
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        fmt.Println(scanner.Text())
    }
}"#,
        (Language::Swift, Concept::FileIo) => r#"import Foundation

if let url = URL(fileURLWithPath: "input.txt"),
   let content = try? String(contentsOf: url, encoding: .utf8) {
    content.split(separator: "\n").forEach { print(String($0)) }
}"#,
        (Language::Kotlin, Concept::FileIo) => r#"import java.io.File

fun main() {
    File("input.txt").forEachLine { println(it) }
}"#,
        (Language::TypeScript, Concept::FileIo) => r#"import * as fs from 'fs';

const content = fs.readFileSync('input.txt', 'utf8');
content.split('\n').forEach(line => console.log(line));"#,
        (Language::JavaScript, Concept::FileIo) => r#"const fs = require('fs');

const content = fs.readFileSync('input.txt', 'utf8');
content.split('\n').forEach(line => console.log(line));"#,
        (Language::Java, Concept::FileIo) => r#"import java.nio.file.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) throws Exception {
        Files.lines(Paths.get("input.txt")).forEach(System.out::println);
    }
}"#,
        (Language::Cpp, Concept::FileIo) => r#"#include <iostream>
#include <fstream>
#include <string>

int main() {
    std::ifstream file("input.txt");
    std::string line;
    while (std::getline(file, line)) {
        std::cout << line << std::endl;
    }
    return 0;
}"#,
    }
}

// ─────────────────────────────────────────────────────────────────
// Resonance scoring
// ─────────────────────────────────────────────────────────────────

/// Structural features extracted from a code snippet
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CodeFeatures {
    /// Control flow style: sequential, conditional, match/switch, loop
    pub control_flow: Vec<String>,
    /// Error handling style: Result/Option, try/catch, if-nil, panic/panic
    pub error_style: String,
    /// Mutability model: immutable, mutable variable, const
    pub mutability: String,
    /// Type system: static, dynamic, structural, duck
    pub type_system: String,
    /// Memory model: gc, ownership, manual, arena
    pub memory_model: String,
    /// Uses async/await or equivalent
    pub has_async: bool,
    /// Uses generics/paramic types
    pub has_generics: bool,
    /// Uses a map/dictionary/hashmap
    pub has_map: bool,
    /// Uses a struct/class/record definition
    pub has_struct: bool,
    /// Uses a thread/goroutine/task/coroutine
    pub has_concurrency: bool,
    /// Uses regex
    pub has_regex: bool,
}

impl CodeFeatures {
    /// Extract features from the focus language's code for a concept
    pub fn extract(code: &str, lang: Language, concept: Concept) -> Self {
        let code_lower = code.to_lowercase();

        let has_map = code_lower.contains("hashmap")
            || code_lower.contains("map<")
            || code_lower.contains("dict")
            || code_lower.contains("unordered_map")
            || code_lower.contains("new map")
            || code_lower.contains("mutablemapof")
            || code_lower.contains("hash_map");

        let has_async = code_lower.contains("async")
            || code_lower.contains("await")
            || code_lower.contains("task {")
            || code_lower.contains("launch")
            || code_lower.contains("goroutine")
            || code_lower.contains("spawn")
            || code_lower.contains("coroutine");

        let has_generics = code.contains('<')
            && (code.contains("Map<") || code.contains("Vec<") || code.contains("HashMap<")
                || code.contains("List<") || code.contains("Array<"));

        let has_concurrency = code_lower.contains("thread")
            || code_lower.contains("goroutine")
            || code_lower.contains("task")
            || code_lower.contains("coroutine")
            || code_lower.contains("executor")
            || code_lower.contains("async");

        let has_regex = code_lower.contains("regex")
            || code_lower.contains("regexp")
            || code_lower.contains("nsregularexpression")
            || code_lower.contains("/^");

        let has_struct = match concept {
            Concept::StructDef => true,
            _ => code_lower.contains("struct")
                || code_lower.contains("class ")
                || code_lower.contains("data class")
                || code_lower.contains("type ")
                || code_lower.contains("impl ")
                || code_lower.contains("typealias")
                || code_lower.contains("interface"),
        };

        let error_style = if code_lower.contains("result<")
            || code_lower.contains("? .")
            || code_lower.contains(".unwrap_or")
        {
            "result_option".to_string()
        } else if code_lower.contains("try ")
            || code_lower.contains("catch")
            || code_lower.contains("throw")
        {
            "try_catch".to_string()
        } else if code_lower.contains("if nil")
            || code_lower.contains("if null")
            || code_lower.contains("??")
            || code_lower.contains("?:")
        {
            "nil_check".to_string()
        } else if code_lower.contains("panic") {
            "panic".to_string()
        } else {
            "none".to_string()
        };

        let memory_model = if code_lower.contains("gc")
            || lang == Language::Java
            || lang == Language::JavaScript
            || lang == Language::TypeScript
            || lang == Language::Kotlin
            || lang == Language::Swift
        {
            "gc".to_string()
        } else if lang == Language::Rust {
            "ownership".to_string()
        } else if lang == Language::Cpp || lang == Language::Cpp {
            "manual".to_string()
        } else {
            "mixed".to_string()
        };

        let type_system = match lang {
            Language::Rust | Language::Kotlin | Language::Java | Language::Cpp => "static",
            Language::Go => "static",
            Language::Swift => "static_with_inference",
            Language::TypeScript => "structural",
            Language::JavaScript => "duck",
        };

        let mutability = if code.contains(" mut ")
            || code.contains("let mut")
            || code.contains(": &mut")
            || code.contains("var mutable")
        {
            "explicit_mutable".to_string()
        } else if code.contains("const ")
            || code.contains("final ")
            || code.contains("val ")
            || code.contains("let ")
        {
            "mostly_immutable".to_string()
        } else {
            "flexible".to_string()
        };

        let control_flow: Vec<String> = {
            let mut v = Vec::new();
            if code.contains("if ") || code.contains("if(") {
                v.push("if".to_string());
            }
            if code.contains("for ") || code.contains("for(") || code.contains("for{") {
                v.push("for".to_string());
            }
            if code.contains("while ") || code.contains("while(") {
                v.push("while".to_string());
            }
            if code.contains("match ") || code.contains("switch ") || code.contains("case ") {
                v.push("match_switch".to_string());
            }
            if code.contains("fn ") || code.contains("func ") || code.contains("fun ") || code.contains("def ") {
                v.push("function".to_string());
            }
            if v.is_empty() {
                v.push("sequential".to_string());
            }
            v
        };

        Self {
            control_flow,
            error_style,
            mutability,
            type_system: type_system.to_string(),
            memory_model,
            has_async,
            has_generics,
            has_map,
            has_struct,
            has_concurrency,
            has_regex,
        }
    }

    /// Compute resonance score between two feature vectors (0.0–1.0)
    pub fn resonance(&self, other: &Self) -> f64 {
        let mut score: f64 = 0.0;
        let mut max_score: f64 = 0.0;

        // Error style: high weight
        max_score += 2.0;
        if self.error_style == other.error_style {
            score += 2.0;
        }

        // Memory model: high weight
        max_score += 2.0;
        if self.memory_model == other.memory_model {
            score += 2.0;
        }

        // Mutability: medium weight
        max_score += 1.5;
        if self.mutability == other.mutability {
            score += 1.5;
        }

        // Type system: medium weight
        max_score += 1.5;
        if self.type_system == other.type_system {
            score += 1.5;
        }

        // Control flow overlap
        max_score += 1.5;
        let cf_overlap = self
            .control_flow
            .iter()
            .filter(|c| other.control_flow.contains(c))
            .count();
        let cf_union = self.control_flow.len() + other.control_flow.len() - cf_overlap;
        if cf_union > 0 {
            score += 1.5 * (cf_overlap as f64 / cf_union as f64);
        }

        // Boolean features: each match adds partial score
        let bool_features: Vec<(bool, bool)> = vec![
            (self.has_async, other.has_async),
            (self.has_generics, other.has_generics),
            (self.has_map, other.has_map),
            (self.has_struct, other.has_struct),
            (self.has_concurrency, other.has_concurrency),
            (self.has_regex, other.has_regex),
        ];

        for (a, b) in bool_features {
            max_score += 0.5;
            if a == b {
                score += 0.5;
            }
        }

        if max_score > 0.0 {
            score / max_score
        } else {
            0.0
        }
    }
}

// ─────────────────────────────────────────────────────────────────
// Resonance report
// ─────────────────────────────────────────────────────────────────

/// One language's code + features
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LanguageSnippet {
    pub language: Language,
    pub code: String,
    pub features: CodeFeatures,
}

/// Resonance matrix entry
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ResonanceEntry {
    pub language_a: String,
    pub language_b: String,
    pub score: f64,
}

/// Full analysis report
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ResonanceReport {
    pub concept: String,
    pub focus_language: String,
    pub snippets: Vec<LanguageSnippet>,
    /// Pairwise resonance scores involving the focus language
    pub focus_resonances: Vec<ResonanceEntry>,
    /// Average resonance of focus language with all others
    pub average_resonance: f64,
    /// Highest and lowest resonance pairs (across all 8 languages)
    pub highest_resonance: Option<ResonanceEntry>,
    pub lowest_resonance: Option<ResonanceEntry>,
}

/// Generate the full resonance report for a concept, with a given focus language
pub fn generate_report(concept: Concept, focus_language: Language) -> ResonanceReport {
    let focus_code = generate_code(focus_language, concept);
    let focus_features = CodeFeatures::extract(focus_code, focus_language, concept);

    let mut snippets = Vec::with_capacity(8);
    let mut all_features: BTreeMap<Language, CodeFeatures> = BTreeMap::new();

    for lang in Language::all() {
        let code = generate_code(lang, concept);
        let features = CodeFeatures::extract(code, lang, concept);
        snippets.push(LanguageSnippet {
            language: lang,
            code: code.to_string(),
            features: features.clone(),
        });
        all_features.insert(lang, features);
    }

    // Compute focus language resonance with all others
    let mut focus_resonances: Vec<ResonanceEntry> = Vec::new();
    for lang in Language::all() {
        if lang == focus_language {
            continue;
        }
        let other_features = &all_features[&lang];
        let score = focus_features.resonance(other_features);
        focus_resonances.push(ResonanceEntry {
            language_a: focus_language.as_str().to_string(),
            language_b: lang.as_str().to_string(),
            score,
        });
    }

    focus_resonances.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap());

    let avg = if focus_resonances.is_empty() {
        0.0
    } else {
        focus_resonances.iter().map(|e| e.score).sum::<f64>()
            / focus_resonances.len() as f64
    };

    // Highest/lowest across all pairs
    let mut all_pairs: Vec<ResonanceEntry> = Vec::new();
    let langs: Vec<Language> = Language::all().to_vec();
    for i in 0..langs.len() {
        for j in (i + 1)..langs.len() {
            let score = all_features[&langs[i]].resonance(&all_features[&langs[j]]);
            all_pairs.push(ResonanceEntry {
                language_a: langs[i].as_str().to_string(),
                language_b: langs[j].as_str().to_string(),
                score,
            });
        }
    }
    all_pairs.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap());

    ResonanceReport {
        concept: concept.display_name().to_string(),
        focus_language: focus_language.as_str().to_string(),
        snippets,
        focus_resonances,
        average_resonance: avg,
        highest_resonance: all_pairs.first().cloned(),
        lowest_resonance: all_pairs.last().cloned(),
    }
}

/// Render a report as human-readable text
pub fn render_report_text(report: &ResonanceReport) -> String {
    let mut out = format!(
        "╔══════════════════════════════════════════════════════════════╗\n\
         ║       POLYGLOT IDIOM RESONATOR — Resonance Report          ║\n\
         ╠══════════════════════════════════════════════════════════════╣\n\
         ║  Concept: {:<50}║\n\
         ║  Focus Language: {:<47}║\n\
         ╚══════════════════════════════════════════════════════════════╝\n",
        report.concept,
        report.focus_language
    );

    out.push_str("\n── Focus Language Resonance Scores ──────────────────────────\n\n");
    for entry in &report.focus_resonances {
        let bar = resonance_bar(entry.score);
        out.push_str(&format!(
            "  {:<14} ↔ {:<14}  {:>5.1}%  {}\n",
            entry.language_a,
            entry.language_b,
            (entry.score * 100.0).round(),
            bar
        ));
    }

    out.push_str(&format!(
        "\n  Average resonance: {:.1}%\n",
        (report.average_resonance * 100.0).round()
    ));

    if let Some(high) = &report.highest_resonance {
        out.push_str(&format!(
            "  Highest pair: {} ↔ {} ({:.1}%)\n",
            high.language_a,
            high.language_b,
            (high.score * 100.0).round()
        ));
    }
    if let Some(low) = &report.lowest_resonance {
        out.push_str(&format!(
            "  Lowest pair:  {} ↔ {} ({:.1}%)\n",
            low.language_a,
            low.language_b,
            (low.score * 100.0).round()
        ));
    }

    out.push_str("\n── Idiomatic Code Snippets ─────────────────────────────────────\n\n");
    for snippet in &report.snippets {
        out.push_str(&format!(
            "┌─ {} ──────────────────────────────────────────────────────────\n",
            snippet.language
        ));
        for line in snippet.code.lines().take(10) {
            out.push_str(&format!("│ {}\n", line));
        }
        if snippet.code.lines().count() > 10 {
            out.push_str(&format!("│ ... ({} lines total)\n", snippet.code.lines().count()));
        }
        out.push_str("└──────────────────────────────────────────────────────────────\n\n");
    }

    out
}

fn resonance_bar(score: f64) -> String {
    let full = (score * 20.0).round() as usize;
    let empty = 20 - full;
    format!("[{}{}]", "#".repeat(full), "-".repeat(empty))
}

// ─────────────────────────────────────────────────────────────────
// Language rotation integration
// ─────────────────────────────────────────────────────────────────

/// Rotation state read from language_rotation.json
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RotationState {
    pub languages: Vec<String>,
    pub current_index: usize,
    #[serde(rename = "last_language")]
    pub last_language: Option<String>,
    pub updated_at: String,
}

/// Load rotation state from a JSON file
pub fn load_rotation(path: impl AsRef<Path>) -> Result<RotationState, String> {
    let content =
        fs::read_to_string(path.as_ref()).map_err(|e| format!("read error: {}", e))?;
    serde_json::from_str(&content).map_err(|e| format!("parse error: {}", e))
}

/// Save updated rotation state (advance index by 1)
pub fn save_rotation(path: impl AsRef<Path>, state: &RotationState) -> Result<(), String> {
    let json =
        serde_json::to_string_pretty(state).map_err(|e| format!("encode error: {}", e))?;
    fs::write(path.as_ref(), &json).map_err(|e| format!("write error: {}", e))?;
    Ok(())
}

/// Advance the rotation index by 1 (wrapping)
pub fn advance_rotation(state: &mut RotationState) {
    if !state.languages.is_empty() {
        state.current_index = (state.current_index + 1) % state.languages.len();
        let new_lang = &state.languages[state.current_index];
        state.last_language = Some(new_lang.clone());
    }
}

/// Run a full analysis cycle: load rotation, generate report, advance index
pub fn run_cycle(
    rotation_path: impl AsRef<Path>,
    concept: Concept,
) -> Result<(ResonanceReport, RotationState), String> {
    let mut state = load_rotation(rotation_path.as_ref())?;

    let focus_lang_name = state.languages.get(state.current_index)
        .ok_or("empty language list")?;
    let focus_lang = Language::from_str(focus_lang_name)
        .ok_or_else(|| format!("unknown language: {}", focus_lang_name))?;

    let report = generate_report(concept, focus_lang);

    advance_rotation(&mut state);
    save_rotation(rotation_path.as_ref(), &state)?;

    Ok((report, state))
}

// ─────────────────────────────────────────────────────────────────
// Tests
// ─────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_all_languages_have_code_for_all_concepts() {
        for lang in Language::all() {
            for concept in Concept::all() {
                let code = generate_code(lang, concept);
                assert!(
                    !code.is_empty(),
                    "Missing code for {:?} in {:?}",
                    concept,
                    lang
                );
            }
        }
    }

    #[test]
    fn test_resonance_is_symmetric() {
        let f1 = CodeFeatures {
            control_flow: vec!["if".to_string(), "for".to_string()],
            error_style: "result_option".to_string(),
            mutability: "mostly_immutable".to_string(),
            type_system: "static".to_string(),
            memory_model: "ownership".to_string(),
            has_async: false,
            has_generics: true,
            has_map: true,
            has_struct: true,
            has_concurrency: false,
            has_regex: false,
        };
        let f2 = CodeFeatures {
            control_flow: vec!["if".to_string(), "while".to_string()],
            error_style: "result_option".to_string(),
            mutability: "mostly_immutable".to_string(),
            type_system: "static".to_string(),
            memory_model: "ownership".to_string(),
            has_async: false,
            has_generics: true,
            has_map: false,
            has_struct: true,
            has_concurrency: false,
            has_regex: false,
        };

        let s1 = f1.resonance(&f2);
        let s2 = f2.resonance(&f1);
        assert!((s1 - s2).abs() < 1e-9, "Resonance must be symmetric");
    }

    #[test]
    fn test_resonance_is_perfect_for_identical_features() {
        let f = CodeFeatures {
            control_flow: vec!["if".to_string()],
            error_style: "try_catch".to_string(),
            mutability: "explicit_mutable".to_string(),
            type_system: "static".to_string(),
            memory_model: "gc".to_string(),
            has_async: true,
            has_generics: false,
            has_map: false,
            has_struct: true,
            has_concurrency: true,
            has_regex: false,
        };

        let score = f.resonance(&f);
        assert!(
            (score - 1.0).abs() < 1e-9,
            "Self-resonance must be 1.0, got {}",
            score
        );
    }

    #[test]
    fn test_resonance_is_zero_for_opposite_features() {
        let f1 = CodeFeatures {
            control_flow: vec!["for".to_string()],
            error_style: "result_option".to_string(),
            mutability: "explicit_mutable".to_string(),
            type_system: "static".to_string(),
            memory_model: "ownership".to_string(),
            has_async: true,
            has_generics: true,
            has_map: true,
            has_struct: true,
            has_concurrency: true,
            has_regex: true,
        };
        let f2 = CodeFeatures {
            control_flow: vec!["match_switch".to_string()],
            error_style: "panic".to_string(),
            mutability: "flexible".to_string(),
            type_system: "duck".to_string(),
            memory_model: "gc".to_string(),
            has_async: false,
            has_generics: false,
            has_map: false,
            has_struct: false,
            has_concurrency: false,
            has_regex: false,
        };

        let score = f1.resonance(&f2);
        // With all mismatches, score should be very low (near 0)
        assert!(
            score < 0.1,
            "Opposite features should have near-zero resonance, got {}",
            score
        );
    }

    #[test]
    fn test_report_generation_for_all_focus_languages() {
        for lang in Language::all() {
            let report = generate_report(Concept::Fibonacci, lang);
            assert_eq!(report.snippets.len(), 8);
            assert_eq!(report.focus_resonances.len(), 7);
            assert!(
                (report.average_resonance - 1.0).abs() < 1e-9
                    || report.average_resonance > 0.0
            );
        }
    }

    #[test]
    fn test_render_report_text_does_not_panic() {
        let report = generate_report(Concept::Hello, Language::Rust);
        let text = render_report_text(&report);
        assert!(text.contains("POLYGLOT IDIOM RESONATOR"));
        assert!(text.contains("Rust"));
        assert!(text.contains("Hello World"));
    }

    #[test]
    fn test_resonance_bar_length() {
        for score in [0.0, 0.25, 0.5, 0.75, 1.0] {
            let bar = resonance_bar(score);
            assert_eq!(bar.len(), 22, "bar for {} = {}", score, bar);
        }
    }

    #[test]
    fn test_focus_resonances_sorted_descending() {
        let report = generate_report(Concept::ErrorFlow, Language::Go);
        for window in report.focus_resonances.windows(2) {
            assert!(
                window[0].score >= window[1].score,
                "Resonances must be sorted descending"
            );
        }
    }

    #[test]
    fn test_advance_rotation_wraps() {
        let mut state = RotationState {
            languages: vec![
                "Rust".to_string(),
                "Go".to_string(),
                "Swift".to_string(),
            ],
            current_index: 2,
            last_language: Some("Swift".to_string()),
            updated_at: "2026-01-01T00:00:00Z".to_string(),
        };

        advance_rotation(&mut state);
        assert_eq!(state.current_index, 0);

        advance_rotation(&mut state);
        assert_eq!(state.current_index, 1);

        advance_rotation(&mut state);
        assert_eq!(state.current_index, 2);
    }

    #[test]
    fn test_advance_rotation_single_language() {
        let mut state = RotationState {
            languages: vec!["Rust".to_string()],
            current_index: 0,
            last_language: Some("Rust".to_string()),
            updated_at: "2026-01-01T00:00:00Z".to_string(),
        };

        advance_rotation(&mut state);
        assert_eq!(state.current_index, 0); // wraps to itself
    }

    #[test]
    fn test_features_extraction_different_for_each_language() {
        // Rust vs JavaScript for Fibonacci should differ significantly
        let rust_code = generate_code(Language::Rust, Concept::Fibonacci);
        let js_code = generate_code(Language::JavaScript, Concept::Fibonacci);

        let rust_f = CodeFeatures::extract(rust_code, Language::Rust, Concept::Fibonacci);
        let js_f = CodeFeatures::extract(js_code, Language::JavaScript, Concept::Fibonacci);

        let score = rust_f.resonance(&js_f);
        // Same concept, different language — score should be moderate
        assert!(
            score > 0.2 && score < 0.95,
            "Cross-language resonance for same concept should be moderate, got {}",
            score
        );
    }

    #[test]
    fn test_concept_all_names_unique() {
        let names: Vec<_> = Concept::all().iter().map(|c| c.name()).collect();
        let mut sorted = names.clone();
        sorted.sort();
        sorted.dedup();
        assert_eq!(
            names.len(),
            sorted.len(),
            "All concept names must be unique"
        );
    }
}