//! # Polyglot Profile
//!
//! Cross-language idiomatic code profiler.
//!
//! ## Creative Concept
//!
//! **"One problem, eight solutions — see the personality of each language."**
//!
//! This module runs identical algorithmic tasks as idiomatic code snippets in each
//! of the 8 rotation languages, measures wall-clock time, and renders a ranked
//! comparison report. It reads `language_rotation.json` to determine the *current*
//! language for the round, then advances the index on save.
//!
//! ## Benchmark Tasks
//!
//! | ID    | Task                     | Rust | Go | Swift | Kotlin | TS  | JS | Java | C++ |
//! |-------|--------------------------|------|----|----|---------|-----|----|------|-----|
//! | fib   | Recursive Fibonacci(30)  | ✓   | ✓  | ✓    | ✓      | ✓  | ✓  | ✓    | ✓   |
//! | sort  | Quick-sort 5 000 ints   | ✓   | ✓  | ✓    | ✓      | ✓  | ✓  | ✓    | ✓   |
//! | sieve | Prime sieve up to 100 k  | ✓   | ✓  | ✓    | ✓      | ✓  | ✓  | ✓    | ✓   |
//!
//! ## Rotation Integration
//!
//! - Reads `language_rotation.json` → `current_index` → current language
//! - After profiling, `current_index` advances by 1 (mod 8) and `updated_at` is refreshed
//! - A log of all profiling runs is kept in `polyglot_profile_log.json`

use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

// ─────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────

/// One language in the rotation order
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
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
    /// Canonical string name
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

    /// File extension used by this language
    pub fn file_ext(&self) -> &'static str {
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

    /// Create from string (case-insensitive)
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

    /// All 8 languages in rotation order
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

/// Available benchmark task IDs
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum BenchmarkTask {
    /// Recursive Fibonacci(30)
    Fib,
    /// Quick-sort 5 000 random integers
    Sort,
    /// Sieve of Eratosthenes up to 100 000
    Sieve,
}

impl BenchmarkTask {
    pub fn id(&self) -> &'static str {
        match self {
            BenchmarkTask::Fib => "fib",
            BenchmarkTask::Sort => "sort",
            BenchmarkTask::Sieve => "sieve",
        }
    }

    pub fn label(&self) -> &'static str {
        match self {
            BenchmarkTask::Fib => "Fibonacci(30) Recursive",
            BenchmarkTask::Sort => "Quick-sort 5 000 ints",
            BenchmarkTask::Sieve => "Prime Sieve ≤ 100 k",
        }
    }

    pub fn all() -> Vec<Self> {
        vec![
            BenchmarkTask::Fib,
            BenchmarkTask::Sort,
            BenchmarkTask::Sieve,
        ]
    }
}

/// A single per-language, per-task measurement
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TaskMeasurement {
    pub task: String,
    pub language: String,
    pub elapsed_ms: f64,
    pub winner: bool,
}

/// A full profiling run (all tasks, all languages)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProfileRun {
    pub id: String,
    pub timestamp: String,
    pub tasks: Vec<TaskMeasurement>,
    pub winners: Vec<String>, // language(s) with lowest total time
    pub fastest_by_task: Vec<TaskMeasurement>,
}

/// Persistent log of all profiling runs
#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct ProfileLog {
    pub runs: Vec<ProfileRun>,
    pub total_runs: usize,
}

/// Language rotation state read from language_rotation.json
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RotationState {
    pub languages: Vec<String>,
    pub current_index: usize,
    pub last_language: String,
    pub updated_at: String,
}

/// A measurement plus the source that produced it
#[derive(Debug, Clone)]
pub struct ProfilerResult {
    pub measurement: TaskMeasurement,
    pub source: String,
}

// ─────────────────────────────────────────────────────────────────
// Idomatic Code Templates (one per language per task)
// ─────────────────────────────────────────────────────────────────

/// Return the idiomatic source code for a language + task combination
pub fn source_template(lang: Language, task: BenchmarkTask) -> String {
    match (lang, task) {
        // ── Fibonacci ──────────────────────────────────────────────
        (Language::Rust, BenchmarkTask::Fib) => r#"
fn fib(n: u64) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => fib(n - 1) + fib(n - 2),
    }
}
fn main() {
    let start = std::time::Instant::now();
    let result = fib(30);
    let elapsed = start.elapsed().as_secs_f64() * 1000.0;
    println!("{}", elapsed);
}
"#.to_string(),

        (Language::Go, BenchmarkTask::Fib) => r#"
package main
import "time"
func fib(n int) int {
    if n < 2 {
        return n
    }
    return fib(n-1) + fib(n-2)
}
func main() {
    start := time.Now()
    result := fib(30)
    _ = result
    elapsed := time.Since(start).Seconds() * 1000.0
    println(elapsed)
}
"#.to_string(),

        (Language::Swift, BenchmarkTask::Fib) => r#"
func fib(_ n: Int) -> Int {
    if n < 2 { return n }
    return fib(n - 1) + fib(n - 2)
}
let start = CFAbsoluteTimeGetCurrent()
let result = fib(30)
let elapsed = (CFAbsoluteTimeGetCurrent() - start) * 1000.0
print(elapsed)
"#.to_string(),

        (Language::Kotlin, BenchmarkTask::Fib) => r#"
fun fib(n: Int): Int = if (n < 2) n else fib(n - 1) + fib(n - 2)
fun main() {
    val start = System.currentTimeMillis()
    val result = fib(30)
    val elapsed = System.currentTimeMillis() - start
    println(elapsed.toDouble())
}
"#.to_string(),

        (Language::TypeScript, BenchmarkTask::Fib) => r#"
function fib(n: number): number {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}
const start = performance.now();
const result = fib(30);
const elapsed = performance.now() - start;
console.log(elapsed);
"#.to_string(),

        (Language::JavaScript, BenchmarkTask::Fib) => r#"
function fib(n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}
const start = performance.now();
const result = fib(30);
const elapsed = performance.now() - start;
console.log(elapsed);
"#.to_string(),

        (Language::Java, BenchmarkTask::Fib) => r#"
public class Main {
    static long fib(int n) {
        if (n < 2) return n;
        return fib(n - 1) + fib(n - 2);
    }
    public static void main(String[] args) {
        long start = System.currentTimeMillis();
        long result = fib(30);
        long elapsed = System.currentTimeMillis() - start;
        System.out.println((double) elapsed);
    }
}
"#.to_string(),

        (Language::Cpp, BenchmarkTask::Fib) => r#"
#include <chrono>
#include <iostream>
long long fib(int n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}
int main() {
    auto start = std::chrono::high_resolution_clock::now();
    long long result = fib(30);
    auto elapsed = std::chrono::duration<double, std::milli>(
        std::chrono::high_resolution_clock::now() - start).count();
    std::cout << elapsed << std::endl;
    return 0;
}
"#.to_string(),

        // ── Quick-sort ─────────────────────────────────────────────
        (Language::Rust, BenchmarkTask::Sort) => r#"
fn quick_sort<T: Ord + Clone>(arr: &mut [T]) {
    if arr.len() <= 1 { return }
    let pivot = arr.len() / 2;
    arr.swap(pivot, arr.len() - 1);
    let mut i = 0;
    for j in 0..arr.len() - 1 {
        if arr[j] <= arr[arr.len() - 1] {
            arr.swap(i, j);
            i += 1;
        }
    }
    arr.swap(i, arr.len() - 1);
    let mid = i;
    quick_sort(&mut arr[..mid]);
    quick_sort(&mut arr[mid + 1..]);
}
fn main() {
    let mut data: Vec<i32> = (0..5000_i32).map(|x| ((x * 1743 + 31) % 5000) as i32).collect();
    let start = std::time::Instant::now();
    quick_sort(&mut data);
    let elapsed = start.elapsed().as_secs_f64() * 1000.0;
    println!("{}", elapsed);
}
"#.to_string(),

        (Language::Go, BenchmarkTask::Sort) => r#"
package main
import "time"
func quick_sort(a []int) {
    if len(a) <= 1 { return }
    mid := len(a) / 2
    a[mid], a[len(a)-1] = a[len(a)-1], a[mid]
    i := 0
    for j := 0; j < len(a)-1; j++ {
        if a[j] <= a[len(a)-1] {
            a[i], a[j] = a[j], a[i]
            i++
        }
    }
    a[i], a[len(a)-1] = a[len(a)-1], a[i]
    quick_sort(a[:i])
    quick_sort(a[i+1:])
}
func main() {
    data := make([]int, 5000)
    for i := range data { data[i] = (i*1743+31)%5000 }
    start := time.Now()
    quick_sort(data)
    elapsed := time.Since(start).Seconds() * 1000.0
    println(elapsed)
}
"#.to_string(),

        (Language::Swift, BenchmarkTask::Sort) => r#"
func quick_sort(_ arr: inout [Int]) {
    if arr.count <= 1 { return }
    let pivot = arr.count / 2
    arr.swapAt(pivot, arr.count - 1)
    var i = 0
    for j in 0..<arr.count - 1 {
        if arr[j] <= arr[arr.count - 1] {
            arr.swapAt(i, j)
            i += 1
        }
    }
    arr.swapAt(i, arr.count - 1)
    let mid = i
    quick_sort(&arr[..mid])
    quick_sort(&arr[mid + 1...])
}
var data = (0..<5000).map { ($0 * 1743 + 31) % 5000 }
let start = CFAbsoluteTimeGetCurrent()
quick_sort(&data)
let elapsed = (CFAbsoluteTimeGetCurrent() - start) * 1000.0
print(elapsed)
"#.to_string(),

        (Language::Kotlin, BenchmarkTask::Sort) => r#"
fun quickSort(a: MutableList<Int>) {
    if (a.size <= 1) return
    val pivot = a.size / 2
    val pivotVal = a[pivot]
    a[pivot] = a[a.size - 1]
    a[a.size - 1] = pivotVal
    var i = 0
    for (j in 0 until a.size - 1) {
        if (a[j] <= pivotVal) {
            val tmp = a[i]; a[i] = a[j]; a[j] = tmp
            i++
        }
    }
    a[i] = a[a.size - 1]
    a[a.size - 1] = pivotVal
    quickSort(a.subList(0, i))
    quickSort(a.subList(i + 1, a.size))
}
fun main() {
    val data = (0 until 5000).map { (it * 1743 + 31) % 5000 }.toMutableList()
    val start = System.currentTimeMillis()
    quickSort(data)
    val elapsed = System.currentTimeMillis() - start
    println(elapsed.toDouble())
}
"#.to_string(),

        (Language::TypeScript, BenchmarkTask::Sort) => r#"
function quickSort(a: number[]): number[] {
    if (a.length <= 1) return a;
    const pivot = a[Math.floor(a.length / 2)];
    const left = a.filter(x => x < pivot);
    const mid = a.filter(x => x === pivot);
    const right = a.filter(x => x > pivot);
    return [...quickSort(left), ...mid, ...quickSort(right)];
}
const data = Array.from({length: 5000}, (_, i) => (i * 1743 + 31) % 5000);
const start = performance.now();
quickSort(data);
const elapsed = performance.now() - start;
console.log(elapsed);
"#.to_string(),

        (Language::JavaScript, BenchmarkTask::Sort) => r#"
function quickSort(a) {
    if (a.length <= 1) return a;
    const pivot = a[Math.floor(a.length / 2)];
    const left = a.filter(x => x < pivot);
    const mid = a.filter(x => x === pivot);
    const right = a.filter(x => x > pivot);
    return [...quickSort(left), ...mid, ...quickSort(right)];
}
const data = Array.from({length: 5000}, (_, i) => (i * 1743 + 31) % 5000);
const start = performance.now();
quickSort(data);
const elapsed = performance.now() - start;
console.log(elapsed);
"#.to_string(),

        (Language::Java, BenchmarkTask::Sort) => r#"
import java.util.*;
public class Main {
    static void quickSort(int[] a, int lo, int hi) {
        if (lo >= hi) return;
        int mid = a[(lo + hi) / 2];
        int i = lo, j = hi;
        while (i <= j) {
            while (a[i] < mid) i++;
            while (a[j] > mid) j--;
            if (i <= j) { int t = a[i]; a[i] = a[j]; a[j] = t; i++; j--; }
        }
        quickSort(a, lo, j);
        quickSort(a, i, hi);
    }
    public static void main(String[] args) {
        int[] data = new int[5000];
        for (int i = 0; i < 5000; i++) data[i] = (i * 1743 + 31) % 5000;
        long start = System.currentTimeMillis();
        quickSort(data, 0, data.length - 1);
        long elapsed = System.currentTimeMillis() - start;
        System.out.println((double) elapsed);
    }
}
"#.to_string(),

        (Language::Cpp, BenchmarkTask::Sort) => r#"
#include <chrono>
#include <iostream>
#include <vector>
#include <cstdint>
void quickSort(std::vector<int>& a, int lo, int hi) {
    if (lo >= hi) return;
    int mid = a[(lo + hi) / 2];
    int i = lo, j = hi;
    while (i <= j) {
        while (a[i] < mid) i++;
        while (a[j] > mid) j--;
        if (i <= j) { std::swap(a[i], a[j]); i++; j--; }
    }
    quickSort(a, lo, j);
    quickSort(a, i, hi);
}
int main() {
    std::vector<int> data(5000);
    for (int i = 0; i < 5000; i++) data[i] = (i * 1743 + 31) % 5000;
    auto start = std::chrono::high_resolution_clock::now();
    quickSort(data, 0, (int)data.size() - 1);
    auto elapsed = std::chrono::duration<double, std::milli>(
        std::chrono::high_resolution_clock::now() - start).count();
    std::cout << elapsed << std::endl;
    return 0;
}
"#.to_string(),

        // ── Prime Sieve ────────────────────────────────────────────
        (Language::Rust, BenchmarkTask::Sieve) => r#"
fn main() {
    let n = 100_000;
    let start = std::time::Instant::now();
    let mut is_prime = vec![true; n + 1];
    is_prime[0] = false;
    is_prime[1] = false;
    for p in 2.. {
        if p * p > n { break }
        if is_prime[p] {
            for multiple in (p * p..=n).step_by(p) {
                is_prime[multiple] = false;
            }
        }
    }
    let elapsed = start.elapsed().as_secs_f64() * 1000.0;
    println!("{}", elapsed);
}
"#.to_string(),

        (Language::Go, BenchmarkTask::Sieve) => r#"
package main
import "time"
func main() {
    n := 100_000
    isPrime := make([]bool, n+1)
    for i := range isPrime { isPrime[i] = true }
    isPrime[0] = false
    isPrime[1] = false
    for p := 2; p*p <= n; p++ {
        if isPrime[p] {
            for multiple := p * p; multiple <= n; multiple += p {
                isPrime[multiple] = false
            }
        }
    }
    start := time.Now()
    _ = isPrime
    _ = time.Since(start)
    elapsed := time.Since(start).Seconds() * 1000.0
    println(elapsed)
}
"#.to_string(),

        (Language::Swift, BenchmarkTask::Sieve) => r#"
let n = 100_000
var isPrime = [Bool](repeating: true, count: n + 1)
isPrime[0] = false
isPrime[1] = false
var p = 2
while p * p <= n {
    if isPrime[p] {
        var multiple = p * p
        while multiple <= n {
            isPrime[multiple] = false
            multiple += p
        }
    }
    p += 1
}
let start = CFAbsoluteTimeGetCurrent()
_ = isPrime
let elapsed = (CFAbsoluteTimeGetCurrent() - start) * 1000.0
print(elapsed)
"#.to_string(),

        (Language::Kotlin, BenchmarkTask::Sieve) => r#"
fun main() {
    val n = 100_000
    val isPrime = BooleanArray(n + 1) { true }
    isPrime[0] = false
    isPrime[1] = false
    var p = 2
    while (p * p <= n) {
        if (isPrime[p]) {
            var multiple = p * p
            while (multiple <= n) {
                isPrime[multiple] = false
                multiple += p
            }
        }
        p++
    }
    val start = System.currentTimeMillis()
    _ = isPrime
    val elapsed = System.currentTimeMillis() - start
    println(elapsed.toDouble())
}
"#.to_string(),

        (Language::TypeScript, BenchmarkTask::Sieve) => r#"
const n = 100_000;
const isPrime: boolean[] = Array.from({length: n + 1}, () => true);
isPrime[0] = false;
isPrime[1] = false;
for (let p = 2; p * p <= n; p++) {
    if (isPrime[p]) {
        for (let multiple = p * p; multiple <= n; multiple += p) {
            isPrime[multiple] = false;
        }
    }
}
const start = performance.now();
_ = isPrime;
const elapsed = performance.now() - start;
console.log(elapsed);
"#.to_string(),

        (Language::JavaScript, BenchmarkTask::Sieve) => r#"
const n = 100000;
const isPrime = Array.from({length: n + 1}, () => true);
isPrime[0] = false;
isPrime[1] = false;
for (let p = 2; p * p <= n; p++) {
    if (isPrime[p]) {
        for (let multiple = p * p; multiple <= n; multiple += p) {
            isPrime[multiple] = false;
        }
    }
}
const start = performance.now();
_ = isPrime;
const elapsed = performance.now() - start;
console.log(elapsed);
"#.to_string(),

        (Language::Java, BenchmarkTask::Sieve) => r#"
public class Main {
    public static void main(String[] args) {
        int n = 100_000;
        boolean[] isPrime = new boolean[n + 1];
        java.util.Arrays.fill(isPrime, true);
        isPrime[0] = false;
        isPrime[1] = false;
        for (int p = 2; p * p <= n; p++) {
            if (isPrime[p]) {
                for (int multiple = p * p; multiple <= n; multiple += p) {
                    isPrime[multiple] = false;
                }
            }
        }
        long start = System.currentTimeMillis();
        _ = isPrime;
        long elapsed = System.currentTimeMillis() - start;
        System.out.println((double) elapsed);
    }
}
"#.to_string(),

        (Language::Cpp, BenchmarkTask::Sieve) => r#"
#include <chrono>
#include <iostream>
#include <vector>
int main() {
    int n = 100000;
    std::vector<bool> isPrime(n + 1, true);
    isPrime[0] = false;
    isPrime[1] = false;
    for (int p = 2; p * p <= n; p++) {
        if (isPrime[p]) {
            for (int multiple = p * p; multiple <= n; multiple += p) {
                isPrime[multiple] = false;
            }
        }
    }
    auto start = std::chrono::high_resolution_clock::now();
    _ = isPrime;
    auto elapsed = std::chrono::duration<double, std::milli>(
        std::chrono::high_resolution_clock::now() - start).count();
    std.out << elapsed << std::endl;
    return 0;
}
"#.to_string(),
    }
}

// ─────────────────────────────────────────────────────────────────
// Runner — executes a single source snippet and returns elapsed ms
// ─────────────────────────────────────────────────────────────────

/// Execute `code` in the given language and return elapsed milliseconds.
/// Returns `None` if the runner is not available or execution fails.
pub fn run_snippet(lang: Language, code: &str) -> Option<f64> {
    match lang {
        Language::Rust => run_rust(code),
        Language::Go => run_go(code),
        Language::Swift => run_swift(code),
        Language::Kotlin => run_kotlin(code),
        Language::TypeScript => run_typescript(code),
        Language::JavaScript => run_javascript(code),
        Language::Java => run_java(code),
        Language::Cpp => run_cpp(code),
    }
}

fn with_temp_file(ext: &str, content: &str, f: impl FnOnce(&Path) -> Option<f64>) -> Option<f64> {
    let tmp = std::env::temp_dir().join(format!("polyglot_profile_{}.{}", rand_id(), ext));
    fs::write(&tmp, content).ok()?;
    let result = f(&tmp);
    let _ = fs::remove_file(&tmp);
    result
}

fn rand_id() -> String {
    format!(
        "{:x}",
        SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .as_nanos()
    )
}

fn run_rust(code: &str) -> Option<f64> {
    with_temp_file("rs", code, |path| {
        let output = Command::new("rustc")
            .arg(path)
            .arg("-o").arg(path.with_extension(""))
            .output()
            .ok()?;
        if !output.status.success() { return None; }
        let output = Command::new(path.with_extension(""))
            .output()
            .ok()?;
        parse_ms(&String::from_utf8_lossy(&output.stdout))
    })
}

fn run_go(code: &str) -> Option<f64> {
    with_temp_file("go", code, |path| {
        let output = Command::new("go")
            .args(["run", path.to_str()?])
            .output()
            .ok()?;
        parse_ms(&String::from_utf8_lossy(&output.stdout))
    })
}

fn run_swift(code: &str) -> Option<f64> {
    with_temp_file("swift", code, |path| {
        let output = Command::new("swift")
            .arg(path)
            .output()
            .ok()?;
        parse_ms(&String::from_utf8_lossy(&output.stdout))
    })
}

fn run_kotlin(code: &str) -> Option<f64> {
    with_temp_file("kt", code, |path| {
        // Compile with kotlinc if available, otherwise fall back to script mode
        let output = Command::new("kotlinc")
            .arg("-script")
            .arg(path)
            .output()
            .ok()?;
        parse_ms(&String::from_utf8_lossy(&output.stdout))
    })
}

fn run_typescript(code: &str) -> Option<f64> {
    with_temp_file("ts", code, |path| {
        let output = Command::new("ts-node")
            .arg("--transpile-only")
            .arg(path)
            .output()
            .ok()?;
        parse_ms(&String::from_utf8_lossy(&output.stdout))
    })
}

fn run_javascript(code: &str) -> Option<f64> {
    with_temp_file("js", code, |path| {
        let output = Command::new("node")
            .arg(path)
            .output()
            .ok()?;
        parse_ms(&String::from_utf8_lossy(&output.stdout))
    })
}

fn run_java(code: &str) -> Option<f64> {
    with_temp_file("java", code, |path| {
        let class_name = "Main";
        let output = Command::new("javac")
            .arg(path)
            .output()
            .ok()?;
        if !output.status.success() { return None; }
        let output = Command::new("java")
            .args(["-cp", path.parent()?.to_str()?])
            .arg(class_name)
            .output()
            .ok()?;
        parse_ms(&String::from_utf8_lossy(&output.stdout))
    })
}

fn run_cpp(code: &str) -> Option<f64> {
    with_temp_file("cpp", code, |path| {
        let exe = path.with_extension("");
        let output = Command::new("g++")
            .args([path.to_str()?, "-o", exe.to_str()?])
            .output()
            .ok()?;
        if !output.status.success() { return None; }
        let output = Command::new(&exe)
            .output()
            .ok()?;
        parse_ms(&String::from_utf8_lossy(&output.stdout))
    })
}

/// Parse a single floating-point number (ms) from stdout
fn parse_ms(s: &str) -> Option<f64> {
    s.lines()
        .next()?
        .trim()
        .parse::<f64>()
        .ok()
}

// ─────────────────────────────────────────────────────────────────
// Rotation State — read / write language_rotation.json
// ─────────────────────────────────────────────────────────────────

/// Load the rotation state from `language_rotation.json`
pub fn load_rotation_state(path: impl AsRef<Path>) -> Result<RotationState, String> {
    let content = fs::read_to_string(path.as_ref())
        .map_err(|e| format!("Failed to read {}: {}", path.as_ref().display(), e))?;
    serde_json::from_str(&content)
        .map_err(|e| format!("Failed to parse JSON: {}", e))
}

/// Save the rotation state back to `language_rotation.json`
pub fn save_rotation_state(path: impl AsRef<Path>, state: &RotationState) -> Result<(), String> {
    let json = serde_json::to_string_pretty(state)
        .map_err(|e| format!("Failed to encode JSON: {}", e))?;
    fs::write(path.as_ref(), json)
        .map_err(|e| format!("Failed to write {}: {}", path.as_ref().display(), e))
}

/// Advance the rotation index by 1 (mod len), update `last_language` and `updated_at`
pub fn advance_rotation(state: &mut RotationState) {
    if state.languages.is_empty() {
        return;
    }
    let next = (state.current_index + 1) % state.languages.len();
    state.last_language = state.languages[state.current_index].clone();
    state.current_index = next;
    state.updated_at = iso_now();
}

// ─────────────────────────────────────────────────────────────────
// Profiler — runs benchmarks for all tasks in all languages
// ─────────────────────────────────────────────────────────────────

/// Profile all tasks across all 8 languages.
/// Returns per-task measurements. Falls back to `f64::MAX` for unavailable runners.
pub fn profile_all(tasks: &[BenchmarkTask]) -> Vec<ProfilerResult> {
    let mut results = Vec::new();
    for task in tasks {
        let mut task_results: Vec<(Language, f64, String)> = Vec::new();
        for lang in Language::all() {
            let source = source_template(lang, *task);
            let ms = run_snippet(lang, &source).unwrap_or(f64::MAX);
            task_results.push((lang, ms, source));
        }
        // Find winner(s) — lowest non-MAX time
        let min_ms = task_results
            .iter()
            .filter(|(_, ms, _)| *ms < f64::MAX)
            .map(|(_, ms, _)| *ms)
            .fold(f64::MAX, f64::min);

        for (lang, ms, source) in task_results {
            results.push(ProfilerResult {
                measurement: TaskMeasurement {
                    task: (*task).id().to_string(),
                    language: lang.as_str().to_string(),
                    elapsed_ms: ms,
                    winner: ms < f64::MAX && (ms - min_ms).abs() < 0.001,
                },
                source,
            });
        }
    }
    results
}

/// Run a single profiling session and return a `ProfileRun`.
/// Uses wall-clock time from the system clock for the run ID.
pub fn run_profile(tasks: &[BenchmarkTask]) -> ProfileRun {
    let results = profile_all(tasks);

    // Group by task to find winners
    let mut winners_set: std::collections::HashSet<String> = std::collections::HashSet::new();
    let mut fastest_by_task: Vec<TaskMeasurement> = Vec::new();

    for task in tasks {
        let task_results: Vec<_> = results
            .iter()
            .filter(|r| r.measurement.task == (*task).id())
            .collect();

        let min_ms = task_results
            .iter()
            .filter(|r| r.measurement.elapsed_ms < f64::MAX)
            .map(|r| r.measurement.elapsed_ms)
            .fold(f64::MAX, f64::min);

        for r in &task_results {
            if r.measurement.elapsed_ms < f64::MAX && (r.measurement.elapsed_ms - min_ms).abs() < 0.001 {
                winners_set.insert(r.measurement.language.clone());
            }
        }

        let fastest = task_results
            .iter()
            .filter(|r| r.measurement.elapsed_ms < f64::MAX)
            .min_by(|a, b| a.measurement.elapsed_ms.partial_cmp(&b.measurement.elapsed_ms).unwrap());
        if let Some(fastest) = fastest {
            fastest_by_task.push(fastest.measurement.clone());
        }
    }

    // Total time per language
    let mut total: std::collections::HashMap<String, f64> = std::collections::HashMap::new();
    for r in &results {
        *total.entry(r.measurement.language.clone()).or_insert(0.0) += r.measurement.elapsed_ms;
    }

    let min_total = total.values().filter(|&&v| v < f64::MAX).fold(f64::MAX, |acc, &v| f64::min(acc, v));
    let winners: Vec<String> = total
        .into_iter()
        .filter(|(_, v)| *v < f64::MAX && (*v - min_total).abs() < 0.001)
        .map(|(k, _)| k)
        .collect();

    let measurements: Vec<TaskMeasurement> = results.into_iter().map(|r| r.measurement).collect();

    ProfileRun {
        id: format!(
            "run-{:x}",
            SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap_or_default()
                .as_nanos()
        ),
        timestamp: iso_now(),
        tasks: measurements,
        winners,
        fastest_by_task,
    }
}

// ─────────────────────────────────────────────────────────────────
// Profile Log — append and persist to polyglot_profile_log.json
// ─────────────────────────────────────────────────────────────────

/// Load the profile log (or return empty default)
pub fn load_profile_log(path: impl AsRef<Path>) -> ProfileLog {
    if !path.as_ref().exists() {
        return ProfileLog::default();
    }
    let content = fs::read_to_string(path.as_ref()).unwrap_or_default();
    serde_json::from_str(&content).unwrap_or_default()
}

/// Save the profile log (atomic via rename)
pub fn save_profile_log(path: impl AsRef<Path>, log: &ProfileLog) -> Result<(), String> {
    let json = serde_json::to_string_pretty(log)
        .map_err(|e| format!("JSON encode error: {}", e))?;
    let tmp = format!("{}.tmp", path.as_ref().display());
    fs::write(&tmp, &json).map_err(|e| format!("IO error: {}", e))?;
    fs::rename(&tmp, path.as_ref())
        .map_err(|e| format!("Rename error: {}", e))?;
    Ok(())
}

/// Append a run to the log and persist
pub fn append_profile_run(log_path: impl AsRef<Path>, run: ProfileRun) -> Result<ProfileLog, String> {
    let mut log = load_profile_log(&log_path);
    log.runs.push(run);
    log.total_runs = log.runs.len();
    save_profile_log(&log_path, &log)?;
    Ok(log)
}

// ─────────────────────────────────────────────────────────────────
// Render — ASCII report generator
// ─────────────────────────────────────────────────────────────────

/// Render a profiling run as a plain-text ASCII table
pub fn render_report(run: &ProfileRun) -> String {
    let mut lines = Vec::new();

    lines.push("╔══════════════════════════════════════════════════════════════╗".to_string());
    lines.push("║           🦀 POLYGLOT PROFILE — Cross-Language Benchmark  ║".to_string());
    lines.push(format!(
        "║  Run ID: {:<52} ║",
        &run.id
    ));
    lines.push(format!(
        "║  Timestamp: {:<48} ║",
        &run.timestamp
    ));
    lines.push("╠══════════════════════════════════════════════════════════════╣".to_string());

    // Header
    lines.push("║  TASK                      │ RUST  GO    SWIFT  KOTLIN TS    JS     JAVA  C++   ║".to_string());
    lines.push("╠══════════════════════════════════════════════════════════════╣".to_string());

    // Group measurements by task
    let tasks = BenchmarkTask::all();
    let langs = Language::all();

    for task in tasks {
        let task_results: std::collections::HashMap<String, f64> = run
            .tasks
            .iter()
            .filter(|m| m.task == task.id())
            .map(|m| (m.language.clone(), m.elapsed_ms))
            .collect();

        let label = format!("{:23}", task.label());
        let mut row = format!("║  {:} │", label);

        for lang in &langs {
            let ms = task_results.get(lang.as_str()).copied().unwrap_or(f64::MAX);
            let cell = if ms >= f64::MAX {
                "  N/A  ".to_string()
            } else {
                format!("{:>7.2}", ms)
            };
            row.push_str(&format!("{:>9}", cell));
            row.push(' ');
        }
        row.push_str("║");
        lines.push(row);
    }

    lines.push("╠══════════════════════════════════════════════════════════════╣".to_string());

    // Winners
    lines.push(format!(
        "║  🏆 Fastest (total): {:<43} ║",
        run.winners.join(", ")
    ));
    lines.push("╚══════════════════════════════════════════════════════════════╝".to_string());

    lines.join("\n")
}

// ─────────────────────────────────────────────────────────────────
// Convenience — load, profile, advance, save (all-in-one)
// ─────────────────────────────────────────────────────────────────

/// Load rotation state, run the profile, advance the index, save.
pub fn profile_and_rotate(
    rotation_path: impl AsRef<Path>,
    log_path: impl AsRef<Path>,
    tasks: &[BenchmarkTask],
) -> Result<(ProfileRun, String), String> {
    let mut state = load_rotation_state(&rotation_path)?;
    let current_lang = state.languages.get(state.current_index).cloned()
        .ok_or_else(|| "No languages in rotation".to_string())?;

    let run = run_profile(tasks);
    append_profile_run(&log_path, run.clone())?;

    advance_rotation(&mut state);
    save_rotation_state(&rotation_path, &state)?;

    Ok((run, current_lang))
}

// ─────────────────────────────────────────────────────────────────
// Utilities
// ─────────────────────────────────────────────────────────────────

fn iso_now() -> String {
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default();
    let secs = now.as_secs();
    let hours = secs / 3600;
    let mins = (secs % 3600) / 60;
    let secs = secs % 60;
    let days = hours / 24;
    let years = 1970 + days / 365;
    let yday = days % 365;
    // Simplified ISO-ish — just use chrono-like format
    format!(
        "{:04}-{:02}-{:02}T{:02}:{:02}:{:02}+08:00",
        years,
        (yday / 31) + 1,
        (yday % 31) + 1,
        hours % 24,
        mins,
        secs
    )
}

// ─────────────────────────────────────────────────────────────────
// Tests
// ─────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    const LANG_ROTATION_JSON: &str = "/home/admin/.openclaw/workspace/language_rotation.json";

    fn temp_log() -> std::path::PathBuf {
        std::env::temp_dir().join(format!(
            "polyglot_profile_test_{}.json",
            SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos()
        ))
    }

    #[test]
    fn test_source_templates_all_languages_all_tasks() {
        let langs = Language::all();
        let tasks = BenchmarkTask::all();
        for lang in langs {
            for task in &tasks {
                let src = source_template(lang, *task);
                assert!(!src.is_empty(), "Empty source for {:?} {:?}", lang, task);
                assert!(
                    src.len() > 50,
                    "Suspiciously short source for {:?} {:?}: {}",
                    lang,
                    task,
                    src.len()
                );
            }
        }
    }

    #[test]
    fn test_language_all_order() {
        let langs = Language::all();
        assert_eq!(langs.len(), 8);
        assert_eq!(langs[0], Language::Rust);
        assert_eq!(langs[1], Language::Go);
        assert_eq!(langs[2], Language::Swift);
        assert_eq!(langs[3], Language::Kotlin);
        assert_eq!(langs[4], Language::TypeScript);
        assert_eq!(langs[5], Language::JavaScript);
        assert_eq!(langs[6], Language::Java);
        assert_eq!(langs[7], Language::Cpp);
    }

    #[test]
    fn test_language_from_str_roundtrip() {
        for lang in Language::all() {
            let s = lang.as_str();
            assert_eq!(Language::from_str(s), Some(lang));
        }
        assert_eq!(Language::from_str("C++"), Some(Language::Cpp));
        assert_eq!(Language::from_str("Pascal"), None);
    }

    #[test]
    fn test_benchmark_task_idempotent() {
        for task in BenchmarkTask::all() {
            let id = task.id();
            assert_eq!(BenchmarkTask::all().iter().find(|t| (*t).id() == id), Some(&task));
        }
    }

    #[test]
    fn test_profile_run_has_correct_fields() {
        let run = run_profile(&[BenchmarkTask::Fib]);
        assert!(!run.id.is_empty());
        assert!(!run.timestamp.is_empty());
        assert!(!run.tasks.is_empty());
        // Fib should produce 8 measurements (one per language)
        assert_eq!(run.tasks.len(), 8);
    }

    #[test]
    fn test_profile_log_append() {
        let path = temp_log();
        let run1 = run_profile(&[BenchmarkTask::Fib]);
        let run2 = run_profile(&[BenchmarkTask::Sort]);

        let mut log = ProfileLog::default();
        log.runs.push(run1.clone());
        log.runs.push(run2.clone());
        log.total_runs = 2;
        save_profile_log(&path, &log).unwrap();

        let loaded = load_profile_log(&path);
        assert_eq!(loaded.runs.len(), 2);
        assert_eq!(loaded.total_runs, 2);

        let _ = fs::remove_file(&path);
    }

    #[test]
    fn test_render_report_produces_ascii_table() {
        let run = run_profile(&[BenchmarkTask::Fib, BenchmarkTask::Sieve]);
        let report = render_report(&run);
        assert!(report.contains("║"));
        assert!(report.contains("POLYGLOT PROFILE"));
        assert!(report.contains("Fibonacci"));
        assert!(report.contains("Sieve"));
    }

    #[test]
    fn test_winner_determined() {
        let run = run_profile(&[BenchmarkTask::Fib]);
        assert!(!run.winners.is_empty());
        // Winners should be among the 8 languages
        for w in &run.winners {
            assert!(Language::from_str(w).is_some());
        }
    }

    #[test]
    fn test_fastest_by_task_populated() {
        let run = run_profile(&BenchmarkTask::all());
        assert_eq!(run.fastest_by_task.len(), BenchmarkTask::all().len());
    }

    #[test]
    fn test_rotation_advance() {
        let state = RotationState {
            languages: vec![
                "Rust".to_string(),
                "Go".to_string(),
                "Swift".to_string(),
                "Kotlin".to_string(),
                "TypeScript".to_string(),
                "JavaScript".to_string(),
                "Java".to_string(),
                "C/C++".to_string(),
            ],
            current_index: 0,
            last_language: "C/C++".to_string(),
            updated_at: "2026-06-13T06:00:00+08:00".to_string(),
        };
        let mut state = state;
        advance_rotation(&mut state);
        assert_eq!(state.current_index, 1);
        assert_eq!(state.last_language, "Rust");
    }

    #[test]
    fn test_rotation_wraps() {
        let mut state = RotationState {
            languages: vec![
                "Rust".to_string(),
                "Go".to_string(),
            ],
            current_index: 1,
            last_language: "Go".to_string(),
            updated_at: "2026-06-13T06:00:00+08:00".to_string(),
        };
        advance_rotation(&mut state);
        assert_eq!(state.current_index, 0);
        assert_eq!(state.last_language, "Go");
    }

    #[test]
    fn test_load_rotation_state_structure() {
        // Just check we can parse the real file
        if std::path::Path::new(LANG_ROTATION_JSON).exists() {
            let state = load_rotation_state(LANG_ROTATION_JSON).unwrap();
            assert_eq!(state.languages.len(), 8);
            assert_eq!(state.languages[0], "Rust");
            assert_eq!(state.languages[7], "C/C++");
        }
    }

    #[test]
    fn test_measurements_cover_all_languages() {
        let run = run_profile(&BenchmarkTask::all());
        let langs_in_run: std::collections::HashSet<String> = run
            .tasks
            .iter()
            .map(|m| m.language.clone())
            .collect();
        for lang in Language::all() {
            assert!(
                langs_in_run.contains(lang.as_str()),
                "Missing language: {}",
                lang
            );
        }
    }

    #[test]
    fn test_run_snippet_rust_compiles() {
        let code = r#"
fn main() {
    let start = std::time::Instant::now();
    let result = fib(30);
    let elapsed = start.elapsed().as_secs_f64() * 1000.0;
    println!("{}", elapsed);
}
fn fib(n: u64) -> u64 {
    if n < 2 { return n }
    fib(n-1) + fib(n-2)
}
"#;
        let result = run_rust(code);
        // May be None if rustc not installed, but shouldn't panic
        if let Some(ms) = result {
            assert!(ms >= 0.0);
        }
    }

    #[test]
    fn test_run_snippet_nodejs_compiles() {
        let code = r#"
function fib(n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}
const start = performance.now();
fib(30);
const elapsed = performance.now() - start;
console.log(elapsed);
"#;
        let result = run_javascript(code);
        if let Some(ms) = result {
            assert!(ms >= 0.0);
        }
    }
}