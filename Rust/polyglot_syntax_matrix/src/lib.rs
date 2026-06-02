//! Polyglot Syntax Matrix
//!
//! A structured comparison of idiomatic syntax across 8 programming languages.
//! Generates side-by-side equivalent snippets for common operations, enabling
//! developers to cross-reference patterns without context-switching between docs.
//!
//! # Supported Languages
//!
//! - Rust, Go, Swift, Kotlin, TypeScript, JavaScript, Java, C/C++
//!
//! # Categories
//!
//! | Category | Description |
//! |---|---|
//! | `hello_world` | Hello world programs |
//! | `variables` | Variable declaration and mutability |
//! | `functions` | Function definitions and calls |
//! | `control_flow` | Conditionals and loops |
//! | `structs` | Struct/class/data class definitions |
//! | `error_handling` | Try/catch/Result/panic patterns |
//! | `concurrency` | Threads, goroutines, async/await, actors |
//! | `collections` | Arrays, lists, maps, iteration |
//! | `options` | Null/Option handling |
//! | `traits` | Interfaces, protocols, traits, type bounds |
//!
//! # Usage
//!
//! ```rust
//! use polyglot_syntax_matrix::{SyntaxMatrix, Category};
//!
//! let matrix = SyntaxMatrix::new();
//! let report = matrix.generate_report();
//! println!("{}", report);
//!
//! // Per-category
//! println!("{}", matrix.category_snippets(Category::Concurrency).render_text());
//! ```

use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

/// All supported languages (in rotation order)
pub const LANGUAGES: [&str; 8] = [
    "Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++",
];

/// Syntax category
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize, PartialOrd, Ord)]
#[serde(rename_all = "snake_case")]
pub enum Category {
    HelloWorld,
    Variables,
    Functions,
    ControlFlow,
    Structs,
    ErrorHandling,
    Concurrency,
    Collections,
    Options,
    Traits,
}

impl Category {
    pub fn label(&self) -> &'static str {
        match self {
            Self::HelloWorld   => "Hello World",
            Self::Variables   => "Variables & Mutability",
            Self::Functions   => "Functions",
            Self::ControlFlow => "Control Flow",
            Self::Structs     => "Structs & Classes",
            Self::ErrorHandling => "Error Handling",
            Self::Concurrency => "Concurrency",
            Self::Collections => "Collections",
            Self::Options     => "Option / Null Handling",
            Self::Traits      => "Traits & Interfaces",
        }
    }

    pub fn all() -> Vec<Category> {
        vec![
            Self::HelloWorld,
            Self::Variables,
            Self::Functions,
            Self::ControlFlow,
            Self::Structs,
            Self::ErrorHandling,
            Self::Concurrency,
            Self::Collections,
            Self::Options,
            Self::Traits,
        ]
    }
}

/// One language's snippet for one category
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Snippet {
    /// Short human-readable description of what this snippet does
    pub description: String,
    /// The source code
    pub code: String,
    /// Optional notes (idioms, footguns, gotchas)
    #[serde(default)]
    pub notes: Vec<String>,
}

impl Snippet {
    pub fn new(description: &str, code: &str) -> Self {
        Self { description: description.to_string(), code: code.to_string(), notes: vec![] }
    }

    pub fn with_note(mut self, note: &str) -> Self {
        self.notes.push(note.to_string());
        self
    }
}

/// A language's full entry for a category (may have multiple snippets)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LanguageEntry {
    pub snippets: Vec<Snippet>,
}

impl LanguageEntry {
    pub fn snip(&self) -> &Snippet {
        self.snippets.first().unwrap()
    }
}

/// Full comparison row: one category × all languages
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CategoryRow {
    pub category: Category,
    pub label: String,
    pub entries: BTreeMap<String, LanguageEntry>,
}

impl CategoryRow {
    /// Render as a formatted multi-line string (plain-text table)
    pub fn render_text(&self) -> String {
        let mut out = String::new();
        let cat_label = format!("▸ {}", self.label);
        out.push_str(&cat_label);
        out.push('\n');
        out.push_str(&"─".repeat(cat_label.chars().count()));
        out.push('\n');

        for (lang, entry) in &self.entries {
            let snip = entry.snip();
            out.push_str(&format!("  ◆ {}\n", lang));
            for line in snip.code.lines() {
                out.push_str(&format!("    {}\n", line));
            }
            if !snip.notes.is_empty() {
                for note in &snip.notes {
                    out.push_str(&format!("    💎 {}\n", note));
                }
            }
            out.push('\n');
        }
        out
    }
}

/// Complete matrix across all categories and languages
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SyntaxMatrix {
    pub categories: BTreeMap<Category, CategoryRow>,
    pub languages: Vec<String>,
}

impl SyntaxMatrix {
    pub fn new() -> Self {
        let languages = LANGUAGES.iter().map(|s| s.to_string()).collect();
        let categories = Self::build_map();
        let mut matrix = Self { categories, languages };
        matrix.build();
        matrix
    }

    fn build_map() -> BTreeMap<Category, CategoryRow> {
        let mut map = BTreeMap::new();
        for cat in Category::all() {
            map.insert(cat, CategoryRow {
                category: cat,
                label: cat.label().to_string(),
                entries: BTreeMap::new(),
            });
        }
        map
    }

    /// Add a snippet for a language in a category
    fn add(&mut self, lang: &str, cat: Category, snippet: Snippet) {
        let row = self.categories.get_mut(&cat).unwrap();
        row.entries.entry(lang.to_string())
            .or_insert_with(|| LanguageEntry { snippets: vec![] })
            .snippets.push(snippet);
    }

    fn build(&mut self) {
        // ─── Hello World ───────────────────────────────────────────
        self.add("Rust", Category::HelloWorld, Snippet::new(
            "Simple program",
            r#"fn main() {
    println!("Hello, world!");
}"#,
        ));

        self.add("Go", Category::HelloWorld, Snippet::new(
            "Simple program",
            r#"func main() {
    fmt.Println("Hello, world!")
}"#,
        ));

        self.add("Swift", Category::HelloWorld, Snippet::new(
            "Simple program",
            r#"print("Hello, world!")"#,
        ));

        self.add("Kotlin", Category::HelloWorld, Snippet::new(
            "Simple program",
            r#"fun main() {
    println("Hello, world!")
}"#,
        ));

        self.add("TypeScript", Category::HelloWorld, Snippet::new(
            "Simple program",
            r#"console.log("Hello, world!");"#,
        ));

        self.add("JavaScript", Category::HelloWorld, Snippet::new(
            "Simple program",
            r#"console.log("Hello, world!");"#,
        ));

        self.add("Java", Category::HelloWorld, Snippet::new(
            "Simple program",
            r#"public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
    }
}"#,
        ));

        self.add("C/C++", Category::HelloWorld, Snippet::new(
            "Simple program",
            r#"#include <stdio.h>
int main() {
    printf("Hello, world!\n");
    return 0;
}"#,
        ));

        // ─── Variables ──────────────────────────────────────────────
        self.add("Rust", Category::Variables, Snippet::new(
            "Immutable & mutable binding",
            r#"let x = 5;           // immutable
let mut y = 5;    // mutable
let z: i32 = 5;   // with type annotation"#,
        ).with_note("Variables are immutable by default — this is the idiomatic path"));

        self.add("Go", Category::Variables, Snippet::new(
            "Short & explicit declaration",
            r#"x := 5               // short (infers int)
var y int = 5     // explicit with type
var z = 5         // explicit, infers type
const PI = 3.14   // constant"#,
        ).with_note(":= is only inside functions; var/const at package level"));

        self.add("Swift", Category::Variables, Snippet::new(
            "Immutable & mutable",
            r#"let x = 5            // immutable (value type)
var y = 5         // mutable
let z: Int = 5    // with type annotation"#,
        ).with_note("let is preferred — var only when mutation needed"));

        self.add("Kotlin", Category::Variables, Snippet::new(
            "Immutable & mutable",
            r#"val x = 5            // immutable (read-mostly)
var y = 5         // mutable
val z: Int = 5    // with type annotation"#,
        ).with_note("val = reference immutability; var = allow reassignment"));

        self.add("TypeScript", Category::Variables, Snippet::new(
            "Typed & inferred",
            r#"const x = 5;              // const (block-scoped, not reassignable)
let y = 5;               // let (block-scoped, reassignable)
let z: number = 5;       // with type annotation"#,
        ).with_note("Prefer const; avoid var (function-scoped, hoisted)"));

        self.add("JavaScript", Category::Variables, Snippet::new(
            "ES6+ declarations",
            r#"const x = 5;         // preferred — const
let y = 5;          // when reassignment needed
var z = 5;          // legacy — function-scoped, hoisted"#,
        ));

        self.add("Java", Category::Variables, Snippet::new(
            "Types & inference",
            r#"int x = 5;                      // primitive type
final int y = 5;                  // compile-time constant
var z = 5;                        // JDK 10+ local type inference"#,
        ));

        self.add("C/C++", Category::Variables, Snippet::new(
            "Types & inference",
            r#"int x = 5;                      // primitive type (C++)
const int y = 5;                  // compile-time constant
auto z = 5;                       // C++11 type inference
let int w = 5;                    // C++26 gentle intro"#,
        ));

        // ─── Functions ─────────────────────────────────────────────
        self.add("Rust", Category::Functions, Snippet::new(
            "Functions with return type",
            r#"fn add(a: i32, b: i32) -> i32 {
    a + b  // no semicolon = implicit return
}"#,
        ).with_note("Last expression without ; is the return value"));

        self.add("Go", Category::Functions, Snippet::new(
            "Multiple return values",
            r#"func add(a, b int) (int, error) {
    return a + b, nil
}"#,
        ).with_note("Multiple returns enable idiomatic error handling"));

        self.add("Swift", Category::Functions, Snippet::new(
            "Parameters & return type",
            r#"func add(_ a: Int, _ b: Int) -> Int {
    return a + b
}"#,
        ));

        self.add("Kotlin", Category::Functions, Snippet::new(
            "Default args & named params",
            r#"fun add(a: Int, b: Int = 0): Int {
    return a + b
}
// call: add(a = 1, b = 2)"#,
        ).with_note("Default arguments reduce overloads"));

        self.add("TypeScript", Category::Functions, Snippet::new(
            "Typed parameters & return",
            r#"function add(a: number, b: number): number {
    return a + b;
}
// arrow form:
const add = (a: number, b: number): number => a + b;"#,
        ));

        self.add("JavaScript", Category::Functions, Snippet::new(
            "Function forms",
            r#"function add(a, b) {
    return a + b;
}
// arrow form:
const add = (a, b) => a + b;"#,
        ));

        self.add("Java", Category::Functions, Snippet::new(
            "Methods in classes",
            r#"public class Util {
    public static int add(int a, int b) {
        return a + b;
    }
}"#,
        ).with_note("Static methods are the idiomatic way to expose utility functions"));

        self.add("C/C++", Category::Functions, Snippet::new(
            "Functions & overloading",
            r#"int add(int a, int b) {
    return a + b;
}
// C++ can overload:
int add(int a, int b, int c) { return a + b + c; }"#,
        ));

        // ─── Control Flow ──────────────────────────────────────────
        self.add("Rust", Category::ControlFlow, Snippet::new(
            "Pattern matching with match",
            r#"let x = 3;
match x {
    1..=5 => println!("small"),
    n if n > 100 => println!("big"),
    _ => println!("somewhere in between"),
}"#,
        ).with_note("match must be exhaustive — wildcard _ covers all remaining"));

        self.add("Go", Category::ControlFlow, Snippet::new(
            "Switch & if",
            r#"switch x {
case 1, 2:
    println("one or two")
default:
    println("other")
}
// if with short init:
if n := compute(); n > 0 {
    println("positive")
}"#,
        ));

        self.add("Swift", Category::ControlFlow, Snippet::new(
            "Pattern matching with switch",
            r#"let x = 3
switch x {
case 1...5:
    print("small")
case 6..<10:
    print("medium")
default:
    print("other")
}
if let val = optional {
    print(val)
}"#,
        ));

        self.add("Kotlin", Category::ControlFlow, Snippet::new(
            "When expression",
            r#"val x = 3
when (x) {
    in 1..5 -> println("small")
    !in 1..100 -> println("big")
    else -> println("middle")
}"#,
        ));

        self.add("TypeScript", Category::ControlFlow, Snippet::new(
            "Switch & ternary",
            r#"switch (x) {
    case 1:
    case 2:
        console.log("one or two");
        break;
    default:
        console.log("other");
}
// ternary:
const label = x > 0 ? "positive" : "non-positive";"#,
        ));

        self.add("JavaScript", Category::ControlFlow, Snippet::new(
            "Switch & ternary",
            r#"switch (x) {
    case 1:
    case 2:
        console.log("one or two");
        break;
    default:
        console.log("other");
}"#,
        ));

        self.add("Java", Category::ControlFlow, Snippet::new(
            "Switch (JDK 14+ enhanced)",
            r#"int x = 3;
switch (x) {
    case 1, 2 -> System.out.println("one or two");
    case 3 -> {
        System.out.println("three");
        // break is auto-suppressed with ->
    }
    default -> System.out.println("other");
}"#,
        ));

        self.add("C/C++", Category::ControlFlow, Snippet::new(
            "Switch & loop",
            r#"int x = 3;
switch (x) {
    case 1:
    case 2:
        printf("one or two\n");
        break;
    default:
        printf("other\n");
}
// C++20 spaceship:
static_assert((1 <=> 2) < 0);"#,
        ));

        // ─── Structs ───────────────────────────────────────────────
        self.add("Rust", Category::Structs, Snippet::new(
            "Struct with impl",
            r#"struct Point {
    x: f64,
    y: f64,
}
impl Point {
    fn new(x: f64, y: f64) -> Self {
        Self { x, y }
    }
    fn distance_to(&self, other: &Point) -> f64 {
        ((self.x - other.x).powi(2) + (self.y - other.y).powi(2)).sqrt()
    }
}"#,
        ));

        self.add("Go", Category::Structs, Snippet::new(
            "Struct with methods",
            r#"type Point struct {
    X, Y float64
}
func NewPoint(x, y float64) *Point {
    return &Point{X: x, Y: y}
}
func (p *Point) DistanceTo(q *Point) float64 {
    dx := p.X - q.X
    dy := p.Y - q.Y
    return math.Sqrt(dx*dx + dy*dy)
}"#,
        ));

        self.add("Swift", Category::Structs, Snippet::new(
            "Struct with methods",
            r#"struct Point {
    var x: Double
    var y: Double
    func distance(to other: Point) -> Double {
        let dx = x - other.x
        let dy = y - other.y
        return (dx*dx + dy*dy).squareRoot()
    }
}"#,
        ));

        self.add("Kotlin", Category::Structs, Snippet::new(
            "Data class",
            r#"data class Point(var x: Double, var y: Double) {
    fun distanceTo(other: Point): Double {
        val dx = x - other.x
        val dy = y - other.y
        return kotlin.math.sqrt(dx*dx + dy*dy)
    }
}"#,
        ).with_note("data class auto-generates equals/hashCode/copy/toString"));

        self.add("TypeScript", Category::Structs, Snippet::new(
            "Interface & class",
            r#"interface Point {
    x: number;
    y: number;
    distanceTo(other: Point): number;
}
class PointImpl implements Point {
    constructor(public x: number, public y: number) {}
    distanceTo(other: Point): number {
        const dx = this.x - other.x;
        const dy = this.y - other.y;
        return Math.sqrt(dx*dx + dy*dy);
    }
}"#,
        ));

        self.add("JavaScript", Category::Structs, Snippet::new(
            "Class (ES6)",
            r#"class Point {
    #x; #y;  // private fields (ES2022)
    constructor(x, y) {
        this.#x = x;
        this.#y = y;
    }
    distanceTo(other) {
        const dx = this.#x - other.#x;
        const dy = this.#y - other.#y;
        return Math.sqrt(dx*dx + dy*dy);
    }
}"#,
        ));

        self.add("Java", Category::Structs, Snippet::new(
            "Class with record (JDK 16+)",
            r#"// Traditional:
public class Point {
    private final double x;
    private final double y;
    public Point(double x, double y) { this.x = x; this.y = y; }
    public double getX() { return x; }
    public double getY() { return y; }
}
// Record (JDK 16+ — immutable data carrier):
public record Point(double x, double y) {}"#,
        ));

        self.add("C/C++", Category::Structs, Snippet::new(
            "Struct & class",
            r#"struct Point {
    double x;
    double y;
};
// C++ class (encapsulated):
class Point {
public:
    Point(double x, double y) : x_(x), y_(y) {}
    double x() const { return x_; }
    double y() const { return y_; }
private:
    double x_, y_;
};"#,
        ));

        // ─── Error Handling ─────────────────────────────────────────
        self.add("Rust", Category::ErrorHandling, Snippet::new(
            "Result<T, E> and ? operator",
            r#"fn read_file(path: &str) -> Result<String, std::io::Error> {
    let mut contents = String::new();
    File::open(path)?.read_to_string(&mut contents)?;
    Ok(contents)
}
fn demo() {
    if let Ok(content) = read_file("foo.txt") {
        println!("{}", content);
    }
}"#,
        ));

        self.add("Go", Category::ErrorHandling, Snippet::new(
            "Multiple return with error",
            r#"func readFile(path string) (string, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return "", fmt.Errorf("read %s: %w", path, err)
    }
    return string(data), nil
}
func demo() {
    content, err := readFile("foo.txt")
    if err != nil {
        log.Fatal(err)
    }
    println(content)
}"#,
        ));

        self.add("Swift", Category::ErrorHandling, Snippet::new(
            "throw / try / catch",
            r#"enum FileError: Error {
    case notFound
    case unreadable
}
func readFile(at path: String) throws -> String {
    guard FileManager.default.fileExists(atPath: path) else {
        throw FileError.notFound
    }
    return try String(contentsOfFile: path)
}
do {
    let content = try readFile(at: "foo.txt")
    print(content)
} catch {
    print("Failed: \(error)")
}"#,
        ));

        self.add("Kotlin", Category::ErrorHandling, Snippet::new(
            "Result<T> and runCatching",
            r#"fun readFile(path: String): Result<String> =
    runCatching { Files.readString(Path.of(path)) }
// Usage:
readFile("foo.txt")
    .onSuccess { println(it) }
    .onFailure { println("Error: ${it.message}") }
// or with try/catch:
try {
    val content = readFile("foo.txt").getOrThrow()
} catch (e: Exception) {
    println("Error: ${e.message}")
}"#,
        ));

        self.add("TypeScript", Category::ErrorHandling, Snippet::new(
            "Error subclass + try/catch",
            r#"class AppError extends Error {
    constructor(public code: string, message: string) {
        super(message);
        this.name = "AppError";
    }
}
async function fetchData(url: string): Promise<string> {
    const res = await fetch(url);
    if (!res.ok) throw new AppError(String(res.status), res.statusText);
    return res.text();
}
try {
    const data = await fetchData("https://api.example.com");
} catch (e) {
    if (e instanceof AppError) console.error(`[${e.code}] ${e.message}`);
    else throw e;
}"#,
        ));

        self.add("JavaScript", Category::ErrorHandling, Snippet::new(
            "Error + try/catch",
            r#"class AppError extends Error {
    constructor(code, message) {
        super(message);
        this.name = "AppError";
        this.code = code;
    }
}
async function fetchData(url) {
    const res = await fetch(url);
    if (!res.ok) throw new AppError(res.status, res.statusText);
    return res.text();
}
try {
    const data = await fetchData("https://api.example.com");
    console.log(data);
} catch (e) {
    if (e instanceof AppError) console.error(`[${e.code}] ${e.message}`);
}"#,
        ));

        self.add("Java", Category::ErrorHandling, Snippet::new(
            "Checked exceptions + try-with-resources",
            r#"public class FileRead {
    public static String readFile(String path) throws IOException {
        try (var reader = Files.newBufferedReader(Path.of(path))) {
            return reader.readLine();
        }
    }
    public static void demo() {
        try {
            String content = readFile("foo.txt");
            System.out.println(content);
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}"#,
        ));

        self.add("C/C++", Category::ErrorHandling, Snippet::new(
            "errno / std::error_code",
            r#"// C style:
FILE* f = fopen("foo.txt", "r");
if (!f) {
    perror("fopen");
    return 1;
}
fclose(f);
// C++ style:
std::error_code ec;
std::ifstream f("foo.txt");
if (!f) {
    std::cerr << "open failed: " << ec.message() << '\n';
}"#,
        ));

        // ─── Concurrency ────────────────────────────────────────────
        self.add("Rust", Category::Concurrency, Snippet::new(
            "async/await with Tokio",
            r#"use tokio;
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        42
    });
    let result = handle.await.unwrap();
    println!("{}", result);
}"#,
        ).with_note("Requires tokio crate; .await gives the return value"));

        self.add("Go", Category::Concurrency, Snippet::new(
            "Goroutines + channels",
            r#"func main() {
    ch := make(chan int)
    go func() { ch <- 42 }()
    result := <-ch
    fmt.Println(result)
}"#,
        ));

        self.add("Swift", Category::Concurrency, Snippet::new(
            "async/await + actors",
            r#"actor Counter {
    var value = 0
    func inc() { value += 1 }
    func get() -> Int { value }
}
func demo() async {
    let counter = Counter()
    await counter.inc()
    let n = await counter.get()
    print(n)
}"#,
        ));

        self.add("Kotlin", Category::Concurrency, Snippet::new(
            "Coroutines",
            r#"suspend fun fetchUser(id: Int): User = coroutineScope {
    launch { /* async work */ }
    async { /* parallel work */ }.await()
}
fun demo() = runBlocking {
    val user = fetchUser(1)
    println(user)
}"#,
        ));

        self.add("TypeScript", Category::Concurrency, Snippet::new(
            "async/await + Promise.all",
            r#"async function fetchUser(id: number): Promise<User> {
    const res = await fetch(`/api/users/${id}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}
async function demo() {
    const [user, posts] = await Promise.all([
        fetchUser(1),
        fetch(`/api/posts?userId=1`).then(r => r.json()),
    ]);
    console.log(user, posts);
}"#,
        ));

        self.add("JavaScript", Category::Concurrency, Snippet::new(
            "async/await + Promise.all",
            r#"async function fetchUser(id) {
    const res = await fetch(`/api/users/${id}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}
const [user, posts] = await Promise.all([
    fetchUser(1),
    fetch(`/api/posts?userId=1`).then(r => r.json()),
]);
console.log(user, posts);"#,
        ));

        self.add("Java", Category::Concurrency, Snippet::new(
            "CompletableFuture + virtual threads (JDK 21+)",
            r#"public CompletableFuture<String> fetchUser(int id) {
    return HttpClient.newHttpClient()
        .sendAsync(
            HttpRequest.new URI("/api/users/" + id),
            HttpResponse.BodyHandlers.ofString()
        )
        .thenApply(HttpResponse::body);
}
// virtual threads (JDK 21+):
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> System.out.println(fetchUser(1).join()));
}"#,
        ));

        self.add("C/C++", Category::Concurrency, Snippet::new(
            "std::thread + std::future",
            r#"// C++20 coroutines:
std::future<int> compute() {
    return std::async(std::launch::async, [] {
        std::this_thread::sleep_for(1s);
        return 42;
    });
}
// std::jthread (C++20) — automatically joins on destruction:
std::jthread worker([] { std::cout << "running\n"; });"#,
        ));

        // ─── Collections ────────────────────────────────────────────
        self.add("Rust", Category::Collections, Snippet::new(
            "Vec, HashMap, iteration",
            r#"let mut v = vec![1, 2, 3];
v.push(4);
for x in &v { println!("{}", x); }
let m: HashMap<&str, i32> = HashMap::new();
m.insert("answer", 42);
for (k, val) in &m { println!("{} = {}", k, val); }"#,
        ));

        self.add("Go", Category::Collections, Snippet::new(
            "Slice, map, range",
            r#"v := []int{1, 2, 3}
v = append(v, 4)
for i, x := range v {
    fmt.Println(i, x)
}
m := map[string]int{"answer": 42}
for k, val := range m {
    fmt.Println(k, val)
}"#,
        ));

        self.add("Swift", Category::Collections, Snippet::new(
            "Array, Dictionary, forEach",
            r#"var v = [1, 2, 3]
v.append(4)
v.forEach { print($0) }
var m = ["answer": 42]
for (k, val) in m {
    print("\(k) = \(val)")
}"#,
        ));

        self.add("Kotlin", Category::Collections, Snippet::new(
            "List, Map, extension functions",
            r#"val v = mutableListOf(1, 2, 3)
v.add(4)
v.forEach { println(it) }
val m = mutableMapOf("answer" to 42)
for ((k, val) in m) {
    println("$k = $val")
}
// Functional:
val doubled = v.map { it * 2 }.filter { it > 4 }"#,
        ));

        self.add("TypeScript", Category::Collections, Snippet::new(
            "Array, Map, iteration",
            r#"const v: number[] = [1, 2, 3];
v.push(4);
v.forEach(x => console.log(x));
const m = new Map<string, number>([["answer", 42]]);
for (const [k, val] of m) {
    console.log(`${k} = ${val}`);
}
// Functional:
const doubled = v.map(x => x * 2).filter(x => x > 4);"#,
        ));

        self.add("JavaScript", Category::Collections, Snippet::new(
            "Array, Map, iteration",
            r#"const v = [1, 2, 3];
v.push(4);
v.forEach(x => console.log(x));
const m = new Map([["answer", 42]]);
for (const [k, val] of m) {
    console.log(`${k} = ${val}`);
}"#,
        ));

        self.add("Java", Category::Collections, Snippet::new(
            "List, Map, streams (JDK 16+)",
            r#"var v = new ArrayList<>(List.of(1, 2, 3));
v.add(4);
v.forEach(System.out::println);
var m = Map.of("answer", 42);
// Stream:
v.stream()
    .map(x -> x * 2)
    .filter(x -> x > 4)
    .forEach(System.out::println);"#,
        ));

        self.add("C/C++", Category::Collections, Snippet::new(
            "std::vector, std::unordered_map, range-for",
            r#"// C++:
std::vector<int> v = {1, 2, 3};
v.push_back(4);
for (int x : v) std::cout << x << '\n';
std::unordered_map<std::string, int> m{{"answer", 42}};
for (const auto& [k, val] : m) std::cout << k << " = " << val << '\n'; "// C++17"#,
        ));

        // ─── Option / Null Handling ─────────────────────────────────
        self.add("Rust", Category::Options, Snippet::new(
            "Option<T> with match / if let",
            r#"fn greet(name: Option<&str>) {
    match name {
        Some(n) => println!("Hello, {}!", n),
        None => println!("Hello, stranger!"),
    }
    if let Some(n) = name {
        println!("named: {}", n);
    }
    // unwrap_or / map / and_then:
    let n = name.unwrap_or("Guest");
    let greeting = name.map(|n| format!("Hi, {}", n));
}"#,
        ));

        self.add("Go", Category::Options, Snippet::new(
            "Nil check (no Option type)",
            r#"func greet(name *string) {
    if name != nil {
        fmt.Printf("Hello, %s!\n", *name)
    } else {
        fmt.Println("Hello, stranger!")
    }
}
// idiomatic: return (*string, error) instead of null
func getName() (string, error) { /* ... */ }"#,
        ).with_note("Go has no built-in Option — use nil checks or return (value, error)"));

        self.add("Swift", Category::Options, Snippet::new(
            "Optional with if let / guard",
            r#"func greet(_ name: String?) {
    if let n = name {
        print("Hello, \(n)!")
    } else {
        print("Hello, stranger!")
    }
    // guard:
    func process(_ input: String?) {
        guard let n = input else { return }
        print(n)
    }
    // optional chaining:
    let len = name?.count ?? 0"#,
        ));

        self.add("Kotlin", Category::Options, Snippet::new(
            "Nullable type ? + safe calls",
            r#"fun greet(name: String?) {
    if (name != null) {
        println("Hello, $name!")
    } else {
        println("Hello, stranger!")
    }
    // safe call + elvis:
    val n = name?.uppercase() ?: "Guest"
    val len = name?.length ?: 0
    // let:
    name?.let { println("Hello, $it!") }
}"#,
        ));

        self.add("TypeScript", Category::Options, Snippet::new(
            "Optional chaining + nullish coalescing",
            r#"function greet(name: string | null | undefined) {
    if (name) {
        console.log(`Hello, ${name}!`);
    } else {
        console.log("Hello, stranger!");
    }
    // safe navigation + elvis:
    const n = name?.toUpperCase() ?? "Guest";
    const len = name?.length ?? 0;
}"#,
        ));

        self.add("JavaScript", Category::Options, Snippet::new(
            "Optional chaining + nullish coalescing",
            r#"function greet(name) {
    if (name) {
        console.log(`Hello, ${name}!`);
    } else {
        console.log("Hello, stranger!");
    }
    const n = name?.toUpperCase() ?? "Guest";
}"#,
        ));

        self.add("Java", Category::Options, Snippet::new(
            "Optional<T> (JDK 8+)",
            r#"public void greet(Optional<String> name) {
    name.ifPresentOrElse(
        n -> System.out.println("Hello, " + n + "!"),
        () -> System.out.println("Hello, stranger!")
    );
    String n = name.orElse("Guest");
    String upper = name.map(String::toUpperCase).orElse("");
}"#,
        ));

        self.add("C/C++", Category::Options, Snippet::new(
            "std::optional (C++17)",
            r#"// C++17:
std::optional<std::string> getName() { return "Alice"; }
auto name = getName();
if (name) {
    std::cout << "Hello, " << *name << "!\n";
} else {
    std::cout << "Hello, stranger!\n";
}
std::string n = name.value_or("Guest");
// pre-C++17: use sentinel values or pointer
int* ptr = findItem();
if (ptr != nullptr) { /* ... */ }"#,
        ));

        // ─── Traits / Interfaces ─────────────────────────────────────
        self.add("Rust", Category::Traits, Snippet::new(
            "Traits + trait bounds",
            r#"trait Greeting {
    fn greet(&self) -> String;
}
struct Person { name: String }
impl Greeting for Person {
    fn greet(&self) -> String {
        format!("Hello, {}!", self.name)
    }
}
fn hello<T: Greeting>(who: &T) {
    println!("{}", who.greet());
}"#,
        ));

        self.add("Go", Category::Traits, Snippet::new(
            "Interfaces (implicit implementation)",
            r#"type Greeter interface {
    Greet() string
}
type Person struct { Name string }
func (p Person) Greet() string {
    return fmt.Sprintf("Hello, %s!", p.Name)
}
func hello(who Greeter) {
    fmt.Println(who.Greet())
}"#,
        ).with_note("Interfaces are satisfied implicitly — no explicit keyword"));

        self.add("Swift", Category::Traits, Snippet::new(
            "Protocol + extensions",
            r#"protocol Greeting {
    func greet() -> String
}
struct Person: Greeting {
    let name: String
    func greet() -> String { "Hello, \(name)!" }
}
extension Greeting {
    func formal() -> String { "Dear friend" }
}"#,
        ));

        self.add("Kotlin", Category::Traits, Snippet::new(
            "Interface + default implementations",
            r#"interface Greeting {
    fun greet(): String
    fun formal(): String = "Dear friend"  // default impl
}
data class Person(val name: String) : Greeting {
    override fun greet() = "Hello, $name!"
}
fun hello(who: Greeting) {
    println(who.greet())
}"#,
        ));

        self.add("TypeScript", Category::Traits, Snippet::new(
            "Interface + implements",
            r#"interface Greeting {
    greet(): string;
}
class Person implements Greeting {
    constructor(private name: string) {}
    greet(): string { return `Hello, ${this.name}!`; }
}
// Structural typing — interface is satisfied implicitly:
const greet = (who: { greet(): string }) => who.greet();"#,
        ));

        self.add("JavaScript", Category::Traits, Snippet::new(
            "Duck typing — no explicit interface",
            r#"// No interface keyword — objects just need the right shape:
const person = {
    name: "Alice",
    greet() { return `Hello, ${this.name}!`; }
};
// or class:
class Person {
    constructor(name) { this.name = name; }
    greet() { return `Hello, ${this.name}!`; }
}"#,
        ));

        self.add("Java", Category::Traits, Snippet::new(
            "Interface + default methods (JDK 8+)",
            r#"public interface Greeting {
    String greet();
    default String formal() { return "Dear friend"; }  // JDK 8+
}
public class Person implements Greeting {
    private final String name;
    public Person(String name) { this.name = name; }
    @Override public String greet() {
        return "Hello, " + name + "!";
    }
}"#,
        ));

        self.add("C/C++", Category::Traits, Snippet::new(
            "Abstract class / concept (C++20)",
            r#"// C++ abstract class:
class Greeting {
public:
    virtual ~Greeting() = default;
    virtual std::string greet() const = 0;
};
class Person : public Greeting {
    std::string name_;
public:
    Person(std::string n) : name_(n) {}
    std::string greet() const override { return "Hello, " + name_ + "!"; }
};
// C++20 concept:
template<typename T>
concept Greeter = requires(T t) { { t.greet() } -> std::convertible_to<std::string>; };"#,
        ));
    }

    /// Generate a complete plain-text report
    pub fn generate_report(&self) -> String {
        let mut out = String::new();
        out.push_str("╔══════════════════════════════════════════════════════════╗\n");
        out.push_str("║       🌏 Polyglot Syntax Matrix — 8 Languages            ║\n");
        out.push_str("╠══════════════════════════════════════════════════════════╣\n");
        out.push_str("║  Rust · Go · Swift · Kotlin · TS · JS · Java · C/C++   ║\n");
        out.push_str("╚══════════════════════════════════════════════════════════╝\n\n");

        for row in self.categories.values() {
            out.push_str(&row.render_text());
            out.push('\n');
        }

        out
    }

    /// All snippets for one category as structured data
    pub fn category_snippets(&self, cat: Category) -> &CategoryRow {
        self.categories.get(&cat).unwrap()
    }

    /// Per-language summary
    pub fn language_summary(&self, lang: &str) -> String {
        let mut out = format!("══ {} ══\n", lang);
        for row in self.categories.values() {
            if let Some(entry) = row.entries.get(lang) {
                out.push_str(&format!("  {}: {}\n", row.label, entry.snip().description));
            }
        }
        out
    }
}

impl Default for SyntaxMatrix {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_matrix_has_all_categories() {
        let matrix = SyntaxMatrix::new();
        assert_eq!(matrix.categories.len(), Category::all().len());
    }

    #[test]
    fn test_matrix_has_all_languages() {
        let matrix = SyntaxMatrix::new();
        assert_eq!(matrix.languages.len(), LANGUAGES.len());
        for lang in LANGUAGES {
            assert!(matrix.languages.contains(&lang.to_string()));
        }
    }

    #[test]
    fn test_hello_world_has_snippets() {
        let matrix = SyntaxMatrix::new();
        let row = matrix.category_snippets(Category::HelloWorld);
        assert_eq!(row.entries.len(), LANGUAGES.len());
        for lang in LANGUAGES {
            assert!(row.entries.contains_key(lang),
                "HelloWorld missing snippet for {}", lang);
        }
    }

    #[test]
    fn test_all_categories_have_all_languages() {
        let matrix = SyntaxMatrix::new();
        for cat in Category::all() {
            let row = matrix.category_snippets(cat);
            assert_eq!(row.entries.len(), LANGUAGES.len(),
                "Category {:?} missing snippets", cat);
        }
    }

    #[test]
    fn test_snippets_have_code() {
        let matrix = SyntaxMatrix::new();
        for row in matrix.categories.values() {
            for (lang, entry) in &row.entries {
                assert!(!entry.snip().code.is_empty(),
                    "Snippet for {} in {:?} is empty", lang, row.category);
            }
        }
    }

    #[test]
    fn test_generate_report_is_nonempty() {
        let matrix = SyntaxMatrix::new();
        let report = matrix.generate_report();
        assert!(!report.is_empty());
        assert!(report.contains("Hello World"));
        assert!(report.contains("Rust"));
        assert!(report.contains("Functions"));
    }

    #[test]
    fn test_language_summary() {
        let matrix = SyntaxMatrix::new();
        let summary = matrix.language_summary("Rust");
        assert!(summary.contains("Rust"));
        assert!(summary.contains("Hello World"));
        assert!(summary.contains("Concurrency"));
    }

    #[test]
    fn test_category_row_render() {
        let matrix = SyntaxMatrix::new();
        let row = matrix.category_snippets(Category::HelloWorld);
        let text = row.render_text();
        assert!(text.contains("Hello World"));
        assert!(text.contains("Rust"));
        assert!(text.contains("fn main"));
        assert!(text.contains("println!"));
    }

    #[test]
    fn test_serialization() {
        let matrix = SyntaxMatrix::new();
        let json = serde_json::to_string_pretty(&matrix).unwrap();
        assert!(json.contains("Rust"));
        assert!(json.contains("hello_world"));
        let deserialized: SyntaxMatrix = serde_json::from_str(&json).unwrap();
        assert_eq!(deserialized.languages.len(), matrix.languages.len());
    }

    #[test]
    fn test_concurrency_snippets_different() {
        let matrix = SyntaxMatrix::new();
        let row = matrix.category_snippets(Category::Concurrency);
        let rust_snip = row.entries.get("Rust").unwrap().snip().code.clone();
        let go_snip = row.entries.get("Go").unwrap().snip().code.clone();
        assert_ne!(rust_snip, go_snip, "Concurrency snippets should differ per language");
    }

    #[test]
    fn test_error_handling_snippets_different() {
        let matrix = SyntaxMatrix::new();
        let row = matrix.category_snippets(Category::ErrorHandling);
        for lang in LANGUAGES {
            for other in LANGUAGES {
                if lang != other {
                    let a = row.entries.get(lang).unwrap().snip().code.clone();
                    let b = row.entries.get(other).unwrap().snip().code.clone();
                    assert_ne!(a, b, "Error handling snippets for {} and {} should differ", lang, other);
                }
            }
        }
    }
}