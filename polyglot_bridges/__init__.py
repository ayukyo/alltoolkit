#!/usr/bin/env python3
"""
🌉 Polyglot Semantic Bridges v1.0

A creative tool that maps universal programming PROBLEMS to their solutions
across all 8 rotation languages — finding the conceptual "bridges" that
let you translate thought patterns from one language to another.

Creative concept: "Every programming problem has been solved in every
language. This tool builds the bridge between them."

For the selected rotation language, this tool:
  1. Picks the next UNSOLVED problem slot (round-robin across 8 problem types)
  2. Shows how THAT problem manifests and is solved in the selected language
  3. Compares it against all other languages' solutions
  4. Identifies "translation gaps" — concepts that have no direct equivalent
  5. Generates a "semantic bridge diagram" showing conceptual distance

Distinct from existing tools:
  - polyglot_digest:     syntax-parallel code snippets (same problem, same code, different syntax)
  - polyglot_resonator:  mental model frames (how each language THINKS about problems)
  - polyglot_dna:        genetic trait mapping (what each language IS)
  - polyglot_chronicle:  daily history, challenge, mood (temporal focus)
  - language_synapse:    conceptual bridges finding connections between concepts
  - language_compass:   learning journey maps (future milestones)
  - language_ethos:     philosophical manifesto (belief/identity)

Bridges is about PROBLEM→SOLUTION mappings — for each universal problem,
show how every language solves it, and where the conceptual gaps are.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-semantic-bridges"
TOOL_VERSION = "1.0.0"

# The 8 languages this tool manages — matches the rotation order
TOOL_LANGUAGES = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]

ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
    "language_rotation.json"
)


def load_rotation():
    """Load language rotation config."""
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data):
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Universal problem bank ─────────────────────────────────────────────────────
# 8 universal programming problems, each with language-specific solutions
UNIVERSAL_PROBLEMS: List[Dict[str, Any]] = [
    {
        "id": "null_safety",
        "name": "Null Safety",
        "emoji": "🕳️",
        "description": "How do you represent the absence of a value?",
        "why_it_matters": "Null pointer bugs have cost the industry billions. Every language solves 'absence' differently — some at the type level, some at runtime.",
        "slot": 0,
        "solutions": {
            "Rust": {
                "approach": "Option<T> as a first-class algebraic type",
                "mechanism": "enum Option<T> { Some(T), None } — nullity is a TYPE, enforced at compile time",
                "code_example": "fn find_user(id: u64) -> Option<User> { ... } // Returns None or Some(user)",
                "idiom": "if let Some(user) = find_user(42) { ... } else { not_found! }",
                "translation_gap": "No direct equivalent in untyped languages — requires manual null checks",
                "key_insight": "Rust makes NULL the EXCEPTION, not the default. Every potentially-absent value is explicit in the type."
            },
            "Go": {
                "approach": "Nil pointers + zero values",
                "mechanism": "Pointers can be nil; zero values ('', 0, false) serve as 'none' for primitives",
                "code_example": "func findUser(id uint64) (*User, error) { ... } // Returns nil or user+nil error",
                "idiom": "if user, err := findUser(42); err != nil { not_found } else { use(user) }",
                "translation_gap": "No Option type — must use (value, error) tuple pattern; nil vs zero-value ambiguity",
                "key_insight": "Go uses ERROR as the primary absence mechanism, not nil. Nil is for pointer/reference absence only."
            },
            "Swift": {
                "approach": "Optional<T> as a first-class type",
                "mechanism": "Optional is enum-based (Some or None), integrated into syntax with ? and ??",
                "code_example": "func findUser(id: UInt64) -> User? { ... } // Returns nil or user",
                "idiom": "if let user = findUser(42) { use(user) } // nil-coalescing: user ?? defaultUser",
                "translation_gap": "None — Swift's Optional maps cleanly to Rust's Option",
                "key_insight": "Swift's ? syntax makes null handling feel native — no special wrapper class needed."
            },
            "Kotlin": {
                "approach": "Nullable types (?.) with built-in safe operators",
                "mechanism": "T? means nullable; ?. is safe call, ?: is elvis operator for default",
                "code_example": "fun findUser(id: Long): User? { ... } // null if not found",
                "idiom": "val user = findUser(42) ?: throw UserNotFoundException() // elvis operator",
                "translation_gap": "None for JVM languages — Java interop requires @Nullable annotations",
                "key_insight": "Kotlin's type system makes nullability visible at a glance — no Javadoc guessing."
            },
            "TypeScript": {
                "approach": "Optional property types + undefined/null union",
                "mechanism": "TypeScript 2.0+ added strict null checks; use T | undefined or T | null",
                "code_example": "function findUser(id: number): User | undefined { ... } // explicit absence",
                "idiom": "const user = findUser(42); if (user !== undefined) { use(user) }",
                "translation_gap": "Runtime types are erased — T | undefined and T are the same at runtime",
                "key_insight": "TypeScript adds compile-time safety but JS runtime has no null-safety net. Strict mode required."
            },
            "JavaScript": {
                "approach": "undefined and null as two distinct 'absent' values",
                "mechanism": "undefined = uninitialized, not provided; null = explicitly absent; typeof辨别",
                "code_example": "function findUser(id) { return users[id] ?? null; } // ?? is nullish coalescing",
                "idiom": "const user = findUser(42); if (user != null) { use(user) } // != catches both",
                "translation_gap": "No type-level enforcement — null checks are entirely convention and discipline",
                "key_insight": "JavaScript has TWO absence values (null, undefined) with different semantics — confusing for newcomers."
            },
            "Java": {
                "approach": "Object references can be null; Optional<T> since Java 8",
                "mechanism": "java.util.Optional<T> provides explicit absence; null remains the pre-8 convention",
                "code_example": "Optional<User> findUser(long id) { return users.stream().filter(...).findFirst(); }",
                "idiom": "User user = findUser(42).orElseThrow(() -> new UserNotFoundException());",
                "translation_gap": "Optional is Optional — pre-Java-8 codebases use null everywhere; no enforcement",
                "key_insight": "Java 8's Optional is a CLUMSY Option type — it's a wrapper class, not a language feature."
            },
            "C/C++": {
                "approach": "Raw pointers: nullptr (C++11) or NULL macro",
                "mechanism": "nullptr is type-safe null pointer; uninitialized pointers contain garbage",
                "code_example": "User* findUser(uint64_t id) { auto it = users.find(id); return it != users.end() ? &it->second : nullptr; }",
                "idiom": "if (auto* user = findUser(42)) { use(*user); } else { not_found; }",
                "translation_gap": "No type-safe Option — nullptr is just a zero address. No safe navigation operator.",
                "key_insight": "C++ trusts the programmer completely — nullptr is a valid address value (address 0), not a type-level guarantee."
            },
        },
    },
    {
        "id": "error_handling",
        "name": "Error Handling",
        "emoji": "⚠️",
        "description": "How do you represent, propagate, and handle errors?",
        "why_it_matters": "Error handling is where software quality is decided. Explicit error handling produces robust code; suppressed errors produce bugs.",
        "slot": 1,
        "solutions": {
            "Rust": {
                "approach": "Result<T, E> as an algebraic return type",
                "mechanism": "Errors are VALUES returned from functions, not thrown. ? operator propagates automatically.",
                "code_example": "fn read_config(path: &Path) -> Result<Config, io::Error> { ... }",
                "idiom": "let config = read_config(path)?; // ? propagates Err, Ok unwrapped",
                "translation_gap": "No equivalent in exception-based languages — requires mental model shift",
                "key_insight": "Rust's Result forces you to acknowledge errors at every call site. You can't accidentally ignore them."
            },
            "Go": {
                "approach": "Errors as return values — explicit tuple (value, error)",
                "mechanism": "Every function that can fail returns (T, error). No exceptions for recoverable errors.",
                "code_example": "func readConfig(path string) (Config, error) { ... }",
                "idiom": "config, err := readConfig(path); if err != nil { return err } // explicit check",
                "translation_gap": "No compiler enforcement — forgetting to check err is a convention, not an error",
                "key_insight": "Go's error handling is VERBOSE but explicit. The verbosity is the point — it forces acknowledgment."
            },
            "Swift": {
                "approach": "throws keyword + do/catch with typed errors",
                "mechanism": "Functions marked throws return a 'thrown' error; callers must use do/catch or try?",
                "code_example": "func readConfig(at path: URL) throws -> Config { ... }",
                "idiom": "do { let config = try readConfig(path) } catch { print(error) }",
                "translation_gap": "No equivalent in non-typed contexts",
                "key_insight": "Swift's typed throws means the compiler knows what CAN go wrong — unlike unchecked exceptions."
            },
            "Kotlin": {
                "approach": "Exceptions + Result<T> for explicit handling",
                "mechanism": "Traditional exceptions for unrecoverable; Result<T> for explicit error returns",
                "code_example": "fun readConfig(path: Path): Result<Config> { return try { Success(parse(path)) } catch(e: Exception) { Failure(e) } }",
                "idiom": "readConfig(path).onSuccess { config -> use(config) }.onFailure { error -> handle(error) }",
                "translation_gap": "Checked exceptions (from Java interop) vs Kotlin's unchecked — inconsistent",
                "key_insight": "Kotlin doesn't have checked exceptions — a deliberate design choice to avoid Java's verbosity."
            },
            "TypeScript": {
                "approach": "Union types for error states + try/catch for exceptions",
                "mechanism": "Discriminated unions model error states; throw is for truly exceptional cases",
                "code_example": "async function readConfig(path: string): Promise<Result<Config, Error>> { ... }",
                "idiom": "const result = await readConfig(path); if (result.kind === 'err') handle(result.error);",
                "translation_gap": "No language-level Result type — must define it manually or use a library",
                "key_insight": "TypeScript can model Result at the type level, but requires discipline — no built-in ? operator."
            },
            "JavaScript": {
                "approach": "throw/catch for exceptions; return error-object patterns for values",
                "mechanism": "throw is 'exceptional'; most APIs use error-object callbacks or Promise rejection",
                "code_example": "async function readConfig(path) { try { return await fs.readFile(path) } catch(e) { return { err: e } } }",
                "idiom": "try { const data = await readConfig(path) } catch (e) { handle(e) }",
                "translation_gap": "No type enforcement — errors can be thrown anywhere, caught anywhere",
                "key_insight": "JavaScript's error handling is dual-mode: throw (exceptional) and return-error (expected). Confusing mix."
            },
            "Java": {
                "approach": "Checked exceptions (legacy) + Unchecked exceptions + Optional",
                "mechanism": "Checked: compiler enforces handling. Unchecked: RuntimeException hierarchy.",
                "code_example": "Config readConfig(String path) throws IOException { ... } // caller MUST handle",
                "idiom": "try { Config c = readConfig(path); } catch (IOException e) { throw new RuntimeException(e); }",
                "translation_gap": "Checked exceptions are unique to Java — controversial, verbose, often avoided",
                "key_insight": "Java's checked exceptions were intended to make errors explicit — but they created verbose boilerplate."
            },
            "C/C++": {
                "approach": "errno + return codes + exceptions (C++), RAII for cleanup",
                "mechanism": "C: errno, return codes. C++: exceptions + RAII. No standard Result type.",
                "code_example": "FILE* f = fopen(path, \"r\"); if (!f) { perror(\"fopen\"); return error; }",
                "idiom": "// RAII: file closes automatically when 'f' goes out of scope",
                "translation_gap": "No type-safe error wrapping — errno is global state, not typed",
                "key_insight": "C++ exceptions have UNDEFINED BEHAVIOR if destructors throw — a subtle footgun."
            },
        },
    },
    {
        "id": "concurrency",
        "name": "Concurrency",
        "emoji": "⚡",
        "description": "How do you handle multiple tasks executing simultaneously?",
        "why_it_matters": "Modern hardware is parallel. How a language models concurrency determines whether your software scales or bottlenecks.",
        "slot": 2,
        "solutions": {
            "Rust": {
                "approach": "Fearless concurrency via ownership + Send/Sync traits",
                "mechanism": "Arc<Mutex<T>> for shared mutable state; channels for message passing. Data races are compile-time errors.",
                "code_example": "let counter = Arc::new(Mutex::new(0)); let c = counter.clone(); tokio::spawn(async move { *c.lock().unwrap() += 1; });",
                "idiom": "spawn a thread with Arc<Mutex<T>> — the compiler PROVES no data races exist",
                "translation_gap": "Requires explicit Arc/Mutex — no implicit sharing. Verbose but safe.",
                "key_insight": "Rust's type system makes data races a COMPILE ERROR, not a runtime bug. This is unprecedented."
            },
            "Go": {
                "approach": "Goroutines + channels (CSP model)",
                "mechanism": "Goroutines are cheap green threads; channels communicate between them; select multiplexes.",
                "code_example": "ch := make(chan int); go func() { ch <- 42 }(); result := <-ch",
                "idiom": "Don't communicate by sharing memory; share memory by communicating.",
                "translation_gap": "Goroutines are unique to Go — cheap enough to spawn thousands per request",
                "key_insight": "Go's concurrency model is the most approachable: goroutines are cheap, channels are simple, select is elegant."
            },
            "Swift": {
                "approach": "Structured concurrency with async/await + Actors (Swift 6)",
                "mechanism": "Swift 6: actors guarantee no data races. @MainActor isolates UI state.",
                "code_example": "actor Counter { private var count = 0; func increment() { count += 1 } }",
                "idiom": "let counter = Counter(); await counter.increment() // actor-isolated access",
                "translation_gap": "Actors are a unique model — neither message-passing nor shared-memory",
                "key_insight": "Swift 6's actor model is the most principled approach to concurrency safety — the compiler enforces isolation."
            },
            "Kotlin": {
                "approach": "Coroutines with structured concurrency",
                "mechanism": "Suspend functions + StructuredTaskScope tie coroutines to scope lifetime",
                "code_example": "suspend fun fetchUser(id: Long): User = withContext(Dispatchers.IO) { userApi.get(id) }",
                "idiom": "scope.launch { fetchUser(42) }.join() // child coroutines tied to scope",
                "translation_gap": "Coroutines are stackless — lighter than threads but heavier than goroutines",
                "key_insight": "Kotlin's Flow is a lazy async stream — different from both Go channels and JS Promises."
            },
            "TypeScript": {
                "approach": "async/await + Web Workers for true parallelism",
                "mechanism": "Single-threaded event loop; async/await for I/O concurrency; Workers for CPU parallelism",
                "code_example": "const result = await Promise.all([fetch('/api/1'), fetch('/api/2')]); // concurrent I/O",
                "idiom": "Worker-based parallelism: const w = new Worker('compute.js'); w.postMessage(data);",
                "translation_gap": "No built-in parallelism — Workers are isolated, communication is message-passing boilerplate",
                "key_insight": "TypeScript's concurrency is async-first — parallelism requires manual worker management."
            },
            "JavaScript": {
                "approach": "Event loop + Promises + Web Workers",
                "mechanism": "Single-threaded event loop handles async; Workers provide true parallelism",
                "code_example": "const result = await Promise.race([fetch(url1), fetch(url2)]); // race condition",
                "idiom": "setTimeout(() => { ... }, 0) // defer to next event loop tick",
                "translation_gap": "True parallelism requires Web Workers — no shared memory",
                "key_insight": "JavaScript's event loop is unique: single-threaded but non-blocking. Async is cooperative, not preemptive."
            },
            "Java": {
                "approach": "Threads + ExecutorService + Virtual Threads (Java 21+)",
                "mechanism": "Traditional thread pools + lightweight virtual threads that multiplex onto OS threads",
                "code_example": "try (var scope = new StructuredTaskScope.ShutdownOnFailure()) { Future<String> f = scope.fork(() -> api.call()); scope.join(); }",
                "idiom": "Virtual threads: 'scoped continuations' — millions per process with near-zero cost",
                "translation_gap": "Virtual threads are a JVM implementation detail — not visible in the type system",
                "key_insight": "Java 21's virtual threads finally make thread-per-request affordable — the end of thread pool tuning."
            },
            "C/C++": {
                "approach": "std::thread + atomics + mutexes + async (C++11)",
                "mechanism": "Native OS threads, std::atomic for lock-free, std::future/std::async for abstraction",
                "code_example": "std::thread t([]{ process(data); }); t.join(); // or: auto f = std::async(std::launch::async, task);",
                "idiom": "std::atomic<int> counter{0}; counter.fetch_add(1, std::memory_order_relaxed);",
                "translation_gap": "Data races are UNDEFINED BEHAVIOR — the standard doesn't specify what happens",
                "key_insight": "C++ gives you raw power and zero safety — the memory model is formally defined but complex."
            },
        },
    },
    {
        "id": "generics",
        "name": "Generics / Polymorphism",
        "emoji": "🔧",
        "description": "How do you write code that works across multiple types?",
        "why_it_matters": "Generics enable code reuse without sacrificing type safety. The difference between generics and runtime casting is compile-time vs. runtime.",
        "slot": 3,
        "solutions": {
            "Rust": {
                "approach": "Generics with trait bounds — compile-time monomorphization",
                "mechanism": "Generic functions are compiled per-type (monomorphization); trait bounds constrain what types are valid",
                "code_example": "fn largest<T: PartialOrd>(list: &[T]) -> &T { ... } // T must implement PartialOrd",
                "idiom": "impl<T: Display> Display for Wrapper<T> { fn fmt(&self, f: &mut Formatter) -> ... }",
                "translation_gap": "No runtime overhead — generics are erased at compile time, like C++ templates",
                "key_insight": "Rust's trait bounds are like Haskell typeclasses — constraints that define what a type MUST provide."
            },
            "Go": {
                "approach": "Generics (Go 1.18+) — structural constraint via interface method sets",
                "mechanism": "Type parameters with interface constraints; monomorphization at compile time",
                "code_example": "func Map[T, U any](slice []T, f func(T) U) []U { result := make([]U, len(slice)); for i := range slice { result[i] = f(slice[i]) }; return result }",
                "idiom": "type Comparable interface { Less(than Comparable) bool } // or use comparable constraint",
                "translation_gap": "Go's generics lack specialization — no overloading based on type. Also no type class inheritance.",
                "key_insight": "Go added generics AFTER 17 years — and chose a simple model that avoids complex specialization."
            },
            "Swift": {
                "approach": "Generics with protocol constraints + associated types",
                "mechanism": "Generics are compile-time; protocols define requirements; associated types enable polymorphic containers",
                "code_example": "protocol Container { associatedtype Item; mutating func append(_ item: Item); subscript(i: Int) -> Item { get } }",
                "idiom": "struct Stack<T>: Container { var items: [T] = []; mutating func push(_ item: T) { items.append(item) } }",
                "translation_gap": "Swift's where clauses for additional constraints — very expressive",
                "key_insight": "Swift protocols with associated types are like Rust traits + associated types — both are Haskell-inspired."
            },
            "Kotlin": {
                "approach": "Reified generics (JVM) — type preserved at runtime",
                "mechanism": "inline functions with reified type parameters enable type-of-T at runtime; JVM erasure is circumvented",
                "code_example": "inline fun <reified T> typeOf(): T = T::class.java // works! despite JVM erasure",
                "idiom": "val list: List<String> = listOf(\"a\", \"b\"); if (list is List<*>) { ... } // star projection",
                "translation_gap": "JVM type erasure is a pain — Kotlin's reified types are a workaround, not a solution",
                "key_insight": "Kotlin's reified generics are unique — an inline-function trick that recovers type info at runtime."
            },
            "TypeScript": {
                "approach": "TypeScript generics — compile-time only, structural",
                "mechanism": "Generics with constraints (extends), conditional types, mapped types — all erased at runtime",
                "code_example": "function merge<T extends object, U extends object>(a: T, b: U): T & U { return { ...a, ...b }; }",
                "idiom": "type Pick<T, K extends keyof T> = { [P in K]: T[P]; }; // mapped type",
                "translation_gap": "TypeScript generics are PURELY compile-time — no runtime artifacts, no performance cost",
                "key_insight": "TypeScript's type-level computation is Turing-complete — you can compute types at the type level."
            },
            "JavaScript": {
                "approach": "No compile-time generics — use runtime patterns",
                "mechanism": "No type system — use factory functions, duck typing, or TypeScript for compile-time safety",
                "code_example": "function merge(a, b) { return Object.assign({}, a, b); } // runtime, untyped",
                "idiom": "const cache = new Map(); function getOrSet(key, factory) { return cache.get(key) ?? cache.set(key, factory()).value; }",
                "translation_gap": "N/A — no type system at all",
                "key_insight": "JavaScript uses duck typing where generics would be — 'if it has the methods, it works'."
            },
            "Java": {
                "approach": "Java Generics — erasure at runtime, bridge methods at compile time",
                "mechanism": "Type parameters erased to Object (or bound); compiler generates bridge methods",
                "code_example": "class Box<T> { private T content; public void set(T content) { this.content = content; } public T get() { return content; } }",
                "idiom": "List<String> strings = new ArrayList<>(); // compiler inserts casts",
                "translation_gap": "Type erasure means List<String> and List<Integer> are the SAME class at runtime",
                "key_insight": "Java's type erasure was a pragmatic choice for JVM backwards compatibility — but it limits what generics can express."
            },
            "C/C++": {
                "approach": "Templates — Turing-complete compile-time computation",
                "mechanism": "C++ templates are instantiated per-type; template specialization; SFINAE; C++20 Concepts",
                "code_example": "template<typename T, size_t N> constexpr size_t array_size(T (&)[N]) { return N; } // compile-time size",
                "idiom": "template<std::integral T> T square(T x) { return x * x; } // C++20 Concepts constrain T",
                "translation_gap": "C++ templates are more powerful than any other language's generics — but error messages are famously cryptic",
                "key_insight": "C++ templates are Turing-complete at compile time — you can compute factorials, sort arrays, all at compile time."
            },
        },
    },
    {
        "id": "immutability",
        "name": "Immutability",
        "emoji": "🔒",
        "description": "How do you create values that cannot change after creation?",
        "why_it_matters": "Immutability eliminates an entire class of bugs (shared state mutation), enables safe parallelism, and makes code more predictable.",
        "slot": 4,
        "solutions": {
            "Rust": {
                "approach": "Immutable bindings by default; Mut<T> or interior mutability for mutation",
                "mechanism": "let x = 5; // immutable. let mut y = 5; // mutable. Arc<Mutex<T>> for shared mutation.",
                "code_example": "struct Config { port: u16, debug: bool } // all fields immutable by default",
                "idiom": "let config = Config { port: 8080, debug: false }; // config.port = 80 would fail",
                "translation_gap": "No equivalent of const_cast — mutation requires explicit opt-in via mut",
                "key_insight": "Rust defaults to immutability — mutation is the special case, not the default."
            },
            "Go": {
                "approach": "No built-in immutability — convention + function parameters",
                "mechanism": "Go has const for compile-time constants; for data structures, convention is to return new copies",
                "code_example": "func addPort(cfg Config, port int) Config { newCfg := cfg; newCfg.port = port; return newCfg }",
                "idiom": "// Idiomatic Go: shadow variables to create new values rather than mutate",
                "translation_gap": "No language-level immutability for structs — compiler can't enforce it",
                "key_insight": "Go's philosophy: if you want immutability, design your API to return new values. The language doesn't help."
            },
            "Swift": {
                "approach": "let for immutable bindings; structs are copied (value semantics)",
                "mechanism": "let x = 5; // immutable binding. Structs are copied; classes are shared. @Published for reactive mutation.",
                "code_example": "let config = Config(port: 8080, debug: false); // config.port = 80 — ERROR",
                "idiom": "var stack = Stack<Int>(); stack.push(42) // var required for mutating methods",
                "translation_gap": "Swift's let is binding immutability, not object immutability — for objects, use let + value types",
                "key_insight": "Swift distinguishes MUTABLE BINDINGS (var) from IMMUTABLE BINDINGS (let) — and value types are copied."
            },
            "Kotlin": {
                "approach": "val for read-only references; data classes are immutable by convention",
                "mechanism": "val x = 5; // read-only binding. data class vals are immutable; use copy() for modified versions",
                "code_example": "data class Config(val port: Int, val debug: Boolean) // copy() creates modified version",
                "idiom": "val newConfig = config.copy(port = 443) // new instance with port changed",
                "translation_gap": "Kotlin's val is like Swift's let — read-only binding, not deep immutability",
                "key_insight": "Kotlin's data class + copy() is the most ergonomic immutable pattern — creates modified copies cleanly."
            },
            "TypeScript": {
                "approach": "const for bindings; Readonly<T> utility type for deep immutability",
                "mechanism": "const x = { port: 8080 }; // x = something would error. But x.port = 80 would NOT error.",
                "code_example": "type ImmutableConfig = Readonly<{ port: number; debug: boolean }>;",
                "idiom": "Object.freeze() for shallow freeze; for deep freeze, recursively apply freeze",
                "translation_gap": "const is shallow — prevents reassignment but not property mutation",
                "key_insight": "TypeScript's const is for BINDINGS, not VALUES. Object.freeze() is the runtime equivalent."
            },
            "JavaScript": {
                "approach": "const for bindings; Object.freeze() for shallow immutability",
                "mechanism": "const x = { port: 8080 }; // x = newObj throws. But x.port = 80 doesn't throw.",
                "code_example": "const frozen = Object.freeze({ port: 8080 }); frozen.port = 80; // silently ignored in strict mode, fails in freeze",
                "idiom": "const createConfig = (port) => Object.freeze({ port, debug: false });",
                "translation_gap": "No deep freeze built-in — Object.freeze() is shallow only",
                "key_insight": "JavaScript's const is the most misunderstood keyword — it prevents reassignment, not mutation."
            },
            "Java": {
                "approach": "final for references; immutable classes (String pattern)",
                "mechanism": "final int x = 5; // x can't be reassigned. For objects: don't expose setters.",
                "code_example": "class Config { private final int port; public Config(int port) { this.port = port; } public int getPort() { return port; } }",
                "idiom": "// Effective Java item 17: 'Make immutable objects simple. Simpler than mutable ones.'",
                "translation_gap": "final is for REFERENCES only — a final List can still have elements added",
                "key_insight": "Java's final is shallow and limited — true immutability requires class design discipline."
            },
            "C/C++": {
                "approach": "const for compile-time immutability; constexpr for compile-time evaluation",
                "mechanism": "const int N = 5; // compile-time constant. constexpr auto square(int x) { return x * x; } // computed at compile time",
                "code_example": "constexpr auto fib(int n) { return n <= 1 ? n : fib(n-1) + fib(n-2); } // computed at compile time!",
                "idiom": "constinit thread_local int tls_var; // initialized once per thread, enforced at compile time",
                "translation_gap": "const in C++ is NOT transitive — const pointer and const data are different",
                "key_insight": "C++ has the most granular immutability model: const, constexpr, consteval, constinit — each at different compile-time stages."
            },
        },
    },
    {
        "id": "async_patterns",
        "name": "Async Patterns",
        "emoji": "⏰",
        "description": "How do you handle operations that complete in the future?",
        "why_it_matters": "Modern software is I/O-bound. How a language handles async directly impacts throughput, latency, and code readability.",
        "slot": 5,
        "solutions": {
            "Rust": {
                "approach": "async/await + Futures — zero-cost, composable futures",
                "mechanism": "async fn returns a Future; .await runs it to completion; Tokio runtime for I/O",
                "code_example": "async fn fetch(url: &str) -> Result<String, reqwest::Error> { reqwest::get(url).await?.text().await }",
                "idiom": "// Futures are polled, not started. They don't run without a runtime.",
                "translation_gap": "Rust futures are polled — not started immediately. This is different from JS Promises.",
                "key_insight": "Rust's async is the most powerful model: futures are lazy (polled), composable, and zero-cost."
            },
            "Go": {
                "approach": "Goroutines + channels — sequential code that runs concurrently",
                "mechanism": "goroutines are cheap; channels connect them; select handles multiplexing; no async keyword needed",
                "code_example": "go func() { result <- fetch(url) }(); // runs concurrently, result via channel",
                "idiom": "// Go doesn't HAVE async/await — every function can run concurrently with 'go'",
                "translation_gap": "No async/await syntax — Go uses goroutines for everything. Simpler but less explicit.",
                "key_insight": "Go's model is the simplest: just add 'go' before a function call and it runs concurrently."
            },
            "Swift": {
                "approach": "async/await (Swift 5.5+) with structured concurrency",
                "mechanism": "async functions; await for non-blocking; async let for parallel tasks; TaskGroup for dynamic concurrency",
                "code_example": "async let a = fetch(url1); async let b = fetch(url2); let results = await [a, b]",
                "idiom": "let (data, _) = try await session.data(for: request) // structured async",
                "translation_gap": "async let parallel = Python-like structured concurrency — unique to Swift",
                "key_insight": "Swift's async let is the cleanest parallel async syntax — structured, explicit, safe."
            },
            "Kotlin": {
                "approach": "Suspend functions + Coroutines — structured async",
                "mechanism": "suspend marks a function as async; coroutines run within CoroutineScope; Flow for async streams",
                "code_example": "suspend fun fetch(url: String): String = withContext(Dispatchers.IO) { client.get(url).string() }",
                "idiom": "scope.launch { val data = fetch(url) }.join() // structured concurrency",
                "translation_gap": "Kotlin Flow is a cold async stream — unlike JS Observables or Go channels",
                "key_insight": "Kotlin coroutines are the most versatile: they can be suspended, cancelled, and composed with Flow."
            },
            "TypeScript": {
                "approach": "Promises + async/await — the standard modern async model",
                "mechanism": "Promise is eager (starts immediately); async/await is syntactic sugar; Promise.all for parallel",
                "code_example": "const [a, b] = await Promise.all([fetch(url1), fetch(url2)]); // parallel",
                "idiom": "async function process() { const result = await Promise.race([fetch(url1), fetch(url2)]); }",
                "translation_gap": "Promises are eager — they start immediately. Rust futures are lazy (polled).",
                "key_insight": "TypeScript's async model is the most widely adopted — and most readable. But Promises are eager, not lazy."
            },
            "JavaScript": {
                "approach": "Promises + async/await + Microtask queue",
                "mechanism": "new Promise() creates eager future; .then chains; async/await (ES2017) for readable syntax",
                "code_example": "async function load() { const res = await fetch(url); return res.json(); }",
                "idiom": "Promise.resolve(42).then(x => x * 2).then(console.log); // chain",
                "translation_gap": "Microtasks (Promise callbacks) run before macrotasks (setTimeout) — event loop priority",
                "key_insight": "JavaScript Promises are EAGER — they're started immediately. This is different from Rust's lazy futures."
            },
            "Java": {
                "approach": "CompletableFuture (Java 8+) + Virtual Threads (Java 21+)",
                "mechanism": "CompletableFuture for composable async; virtual threads for cheap threading",
                "code_example": "Future<String> f = CompletableFuture.supplyAsync(() -> fetch(url)); String result = f.get(); // blocking",
                "idiom": "CompletableFuture.allOf(f1, f2).join(); // wait for all",
                "translation_gap": "Java's Future.get() is BLOCKING — unlike every other language's async",
                "key_insight": "Java Future.get() is the worst async pattern — it blocks. Use CompletableFuture for proper async."
            },
            "C/C++": {
                "approach": "std::future + std::async (C++11); coroutines (C++20, experimental)",
                "mechanism": "std::async launches a future; std::future.get() blocks; C++20 coroutines are compiler-generated state machines",
                "code_example": "auto f = std::async(std::launch::async, [] { return fetch(url); }); auto result = f.get(); // blocks",
                "idiom": "// C++20 coroutines: co_await, co_return — experimental, library support varies",
                "translation_gap": "No standard async/await — C++20 coroutines are compiler intrinsics, not library-level",
                "key_insight": "C++ has the least ergonomic async — no language-level await until C++20, and even then it's experimental."
            },
        },
    },
    {
        "id": "iteration",
        "name": "Iteration & Lazy Sequences",
        "emoji": "🔁",
        "description": "How do you process sequences of data efficiently?",
        "why_it_matters": "Data processing is fundamental. The difference between eager and lazy evaluation can be orders of magnitude in memory and time.",
        "slot": 6,
        "solutions": {
            "Rust": {
                "approach": "Iterators are lazy — map/filter/reduce chains that zero-cost abstract",
                "mechanism": "Iterator trait; .iter() for borrowed; .into_iter() for owned; lazy evaluation by default",
                "code_example": "let sum: u32 = (0..1000).filter(|x| x % 3 == 0 || x % 5 == 0).sum(); // no intermediate collection",
                "idiom": "for (i, item) in items.iter().enumerate() { ... } // enumerate adds index",
                "translation_gap": "No equivalent to JavaScript generators for infinite sequences",
                "key_insight": "Rust iterators are ZERO-COST — the compiler optimizes away the iterator pattern entirely."
            },
            "Go": {
                "approach": "Slices + for range — eager evaluation, no lazy chains",
                "mechanism": "for i, v := range slice { ... } // eager; no map/filter/reduce in stdlib pre-Go 1.21",
                "code_example": "sum := 0; for _, v := range slice { sum += v } // manual accumulation",
                "idiom": "// Go 1.21 added slices.Concurrent, slices.DeleteFunc, slices.Apply — similar to map/filter",
                "translation_gap": "No lazy iterator chains — every operation allocates or loops eagerly",
                "key_insight": "Go deliberately avoided lazy sequences for simplicity — 'explicit is better than implicit.'"
            },
            "Swift": {
                "approach": "Sequence protocol + lazy map/filter via Sequence.lazy",
                "mechanism": "for item in collection { ... } // eager; lazy collection avoids intermediate arrays",
                "code_example": "let sum = (0..<1000).lazy.filter { $0 % 3 == 0 || $0 % 5 == 0 }.reduce(0, +)",
                "idiom": "for case let x in values where x > 0 { ... } // pattern matching in for",
                "translation_gap": "Swift Sequences are eager by default — .lazy makes them lazy",
                "key_insight": "Swift's for case let pattern is uniquely expressive for filtered iteration."
            },
            "Kotlin": {
                "approach": "Sequences (lazy) vs Collections (eager) — two modes",
                "mechanism": "Collection.map().filter() creates intermediate lists; Sequence is lazy, evaluated per-element",
                "code_example": "val sum = (1..1000).asSequence().filter { it % 3 == 0 || it % 5 == 0 }.sum() // lazy",
                "idiom": "listOf(1,2,3).asSequence().map { it * 2 }.toList() // explicit about laziness",
                "translation_gap": "Java Streams vs Kotlin Sequences — both lazy but different APIs",
                "key_insight": "Kotlin Sequences are the key to memory-efficient processing of large data sets — use them for I/O."
            },
            "TypeScript": {
                "approach": "Array methods are eager; Generator functions for lazy",
                "mechanism": "[1,2,3].map(x => x * 2).filter(x => x > 2) // eager, creates intermediate arrays",
                "code_example": "function* fibonacci(): Generator<number> { let [a,b] = [0,1]; while(true) { yield a; [a,b] = [b, a+b]; } }",
                "idiom": "for (const x of fibonacci()) { if (x > 1000) break; sum += x; } // lazy, infinite",
                "translation_gap": "No lazy map/filter chain — generators are the only lazy option",
                "key_insight": "TypeScript's async generators enable lazy async iteration — ES2018 feature."
            },
            "JavaScript": {
                "approach": "Array methods are eager; for...of for iteration; generators for lazy",
                "mechanism": "[1,2,3].map(x => x * 2).filter(x => x > 2) // eager intermediate arrays",
                "code_example": "function* range(start, end) { for (let i = start; i < end; i++) yield i; }",
                "idiom": "for (const x of fibonacci()) { if (x > 1000) break; console.log(x); }",
                "translation_gap": "No lazy map/filter in standard library — need generators or libraries like lodash",
                "key_insight": "JavaScript iterators and generators (ES2015) enable lazy sequences — but they're rarely used compared to array methods."
            },
            "Java": {
                "approach": "Streams API (Java 8+) — lazy pipeline with terminal operations",
                "mechanism": "stream.filter().map().sum() — lazy until terminal operation; parallel() enables parallel",
                "code_example": "int sum = IntStream.range(1, 1000).filter(x -> x % 3 == 0 || x % 5 == 0).sum();",
                "idiom": "stream.collect(Collectors.groupingBy(...)) // collect into groups",
                "translation_gap": "Java Streams are single-use — consuming a stream exhausts it",
                "key_insight": "Java Streams are the most composable lazy pipeline — but they hide their laziness until you understand the model."
            },
            "C/C++": {
                "approach": "Range-v3 library (C++20 Ranges) — lazy, composable ranges",
                "mechanism": "for (auto x : views::iota(1) | views::filter(...)) { ... } // lazy, composable",
                "code_example": "auto sum = ranges::accumulate(views::iota(1, 1000) | views::filter([](int x){ return x%3==0||x%5==0; }), 0);",
                "idiom": "// C++20 Ranges: | pipe operator chains views lazily — the most expressive iteration model",
                "translation_gap": "No standard lazy map/filter in C++17 — only C++20 Ranges or third-party libraries",
                "key_insight": "C++20 Ranges are the most powerful iteration model — composable with | operator, lazy by design."
            },
        },
    },
    {
        "id": "resource_management",
        "name": "Resource Management",
        "emoji": "🗺️",
        "description": "How do you ensure resources (memory, files, connections) are properly cleaned up?",
        "why_it_matters": "Resource leaks bring down systems. Whether cleanup is automatic, deterministic, or manual determines system reliability.",
        "slot": 7,
        "solutions": {
            "Rust": {
                "approach": "RAII via Drop trait + Arc/Mutex for shared resources",
                "mechanism": "When a value goes out of scope, Drop::drop() is called. Deterministic, no GC.",
                "code_example": "struct File { f: File } impl Drop for File { fn drop(&mut self) { self.f.close(); } }",
                "idiom": "let file = File::open(\"data.txt\"); // file is automatically closed when dropped",
                "translation_gap": "No equivalent of garbage collector — all resources must have explicit Drop",
                "key_insight": "Rust's RAII is deterministic: cleanup happens when the last reference goes out of scope."
            },
            "Go": {
                "approach": "defer for deterministic cleanup; GC for memory",
                "mechanism": "defer runs on scope exit regardless of how; GC handles memory asynchronously",
                "code_example": "func read() error { f, err := os.Open(file); if err != nil { return err }; defer f.Close(); ... }",
                "idiom": "defer f.Close() // runs LAST, even if you return early",
                "translation_gap": "No RAII — resources other than memory need explicit defer; no deterministic cleanup for all resources",
                "key_insight": "Go's defer is a simpler model than RAII — but less powerful for complex resource hierarchies."
            },
            "Swift": {
                "approach": "ARC (Automatic Reference Counting) — compile-time reference counting",
                "mechanism": "Objects are deallocated when their reference count hits zero. No background GC thread.",
                "code_example": "class Cache { deinit { print(\"Cleaning up cache\") } } // called when last reference released",
                "idiom": "weak var delegate: AppDelegate? // break retain cycles",
                "translation_gap": "Retain cycles require weak/unowned — not a problem in GC languages",
                "key_insight": "Swift's ARC is deterministic like Rust's RAII — but uses reference counting, not scope-based Drop."
            },
            "Kotlin": {
                "approach": "JVM GC + try-with-resources (AutoCloseable)",
                "mechanism": "GC handles memory automatically; use.use { } for file/connection cleanup (Kotlin idiom)",
                "code_example": "FileInputStream(file).use { fis -> fis.bufferedReader().readText() } // auto-closed",
                "idiom": "connection.use { conn -> conn.execute(query) } // resource closed even on exception",
                "translation_gap": "JVM GC is non-deterministic — no guarantee WHEN memory is reclaimed",
                "key_insight": "Kotlin's .use {} is the idiomatic equivalent of Go's defer for AutoCloseable resources."
            },
            "TypeScript": {
                "approach": "No automatic resource management — convention + finally blocks",
                "mechanism": "try { use(resource) } finally { resource.close() } // manual cleanup",
                "code_example": "const file = fs.openSync('data.txt', 'r'); try { const content = fs.readFileSync(file, 'utf8'); } finally { fs.closeSync(file); }",
                "idiom": "// No using statement — manual finally or wrapper function required",
                "translation_gap": "No RAII, no ARC, no GC for managed resources — manual cleanup is the only option",
                "key_insight": "TypeScript has ZERO built-in resource management — every resource requires manual lifecycle management."
            },
            "JavaScript": {
                "approach": "try/finally + garbage collector for memory; no deterministic cleanup for files",
                "mechanism": "Memory: GC handles deallocation. Files: close() explicitly or via finally",
                "code_example": "const file = fs.openSync('data.txt', 'r'); try { return fs.readFileSync(file, 'utf8'); } finally { fs.closeSync(file); }",
                "idiom": "// Node.js: resource leaks are common — connection pools, file handles must be managed",
                "translation_gap": "No RAII equivalent — JS has no deterministic cleanup for anything but memory",
                "key_insight": "JavaScript's GC is non-deterministic — you can't know WHEN an object is collected, only that it WILL be."
            },
            "Java": {
                "approach": "try-with-resources (Java 7+) + JVM GC",
                "mechanism": "AutoCloseable resources closed automatically; GC handles memory with varying pause times",
                "code_example": "try (var conn = dataSource.getConnection(); var stmt = conn.prepareStatement(sql)) { ... } // auto-closed",
                "idiom": "try-with-resources: 'the resource is scoped to the try block and auto-closed at the end'",
                "translation_gap": "Non-deterministic GC — ZGC (<1ms pause) and Shenandoah (no-pause) are the modern solution",
                "key_insight": "Java's try-with-resources is the most ergonomic resource management — cleaner than manual finally."
            },
            "C/C++": {
                "approach": "RAII (Resource Acquisition Is Initialization) + smart pointers",
                "mechanism": "Constructor acquires, destructor releases; smart pointers (unique_ptr, shared_ptr) automate this",
                "code_example": "auto file = std::make_unique<File>(\"data.txt\"); // closed when unique_ptr destroyed",
                "idiom": "std::unique_ptr<File> file(new File(\"data.txt\")); // file closed automatically on scope exit",
                "translation_gap": "No GC safety net — forgetting to free memory causes leaks; double-free causes crashes",
                "key_insight": "C++ RAII is the most powerful resource management model — tied to object lifetime, not scope or GC."
            },
        },
    },
]


def build_bridge(language: str) -> Dict[str, Any]:
    """
    Build a semantic bridge for the selected language.

    Selects a problem slot based on current rotation index,
    shows how the selected language solves that problem,
    compares with all other languages, and advances the rotation.
    """
    config = load_rotation()
    # Use tool's own 8-language list for logic
    languages = TOOL_LANGUAGES

    if language not in languages:
        raise ValueError(
            f"Language '{language}' not in this tool's rotation. "
            f"Available: {', '.join(languages)}"
        )

    # Determine which problem slot to address — based on the LANGUAGE'S position,
    # not the global config index (allows direct calls with any language)
    language_idx = languages.index(language)
    problem_slot = language_idx % len(UNIVERSAL_PROBLEMS)

    # Also track the global rotation index for advancement
    current_idx = config.get("current_index", 0) % len(languages)
    problem = UNIVERSAL_PROBLEMS[problem_slot]

    solution = problem["solutions"].get(language)
    if not solution:
        raise ValueError(f"No solution data for '{language}' in problem '{problem['id']}'")

    # Build language comparison table
    comparison = {}
    for lang in languages:
        sol = problem["solutions"].get(lang, {})
        comparison[lang] = {
            "approach": sol.get("approach", "Unknown"),
            "mechanism": sol.get("mechanism", "Unknown"),
            "code_example": sol.get("code_example", "N/A"),
            "idiom": sol.get("idiom", "N/A"),
            "key_insight": sol.get("key_insight", "Unknown"),
        }

    # Identify translation gaps for this language
    this_sol = problem["solutions"].get(language, {})
    gaps = []
    for lang in languages:
        if lang == language:
            continue
        gap_desc = _find_gap(this_sol, problem["solutions"].get(lang, {}))
        if gap_desc:
            gaps.append({"language": lang, "gap": gap_desc})

    # Compute difficulty rating (how hard to translate this concept)
    difficulty = _compute_difficulty(problem["id"], language)

    # Advance rotation — use language_idx so next is always the sequential neighbor
    next_idx = (language_idx + 1) % len(languages)
    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)

    # Build bridge emoji path
    emoji_path = _build_bridge_path(languages, language, problem_slot)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "problem": {
            "id": problem["id"],
            "name": problem["name"],
            "emoji": problem["emoji"],
            "description": problem["description"],
            "why_it_matters": problem["why_it_matters"],
            "slot": problem["slot"],
        },
        "solution": {
            "approach": solution["approach"],
            "mechanism": solution["mechanism"],
            "code_example": solution["code_example"],
            "idiom": solution["idiom"],
            "translation_gap": solution["translation_gap"],
            "key_insight": solution["key_insight"],
        },
        "comparison": comparison,
        "translation_gaps": gaps,
        "difficulty_rating": difficulty,
        "emoji_path": emoji_path,
        "next_language": languages[next_idx],
        "rotation_order": languages,
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def _find_gap(solution_a: Dict, solution_b: Dict) -> Optional[str]:
    """Find the conceptual translation gap between two solutions."""
    gap_a = solution_a.get("translation_gap", "")
    gap_b = solution_b.get("translation_gap", "")

    if gap_a and "No direct equivalent" in gap_a:
        return f"No Option/Result type — requires manual null/error handling pattern"
    if gap_a and "requires" in gap_a.lower() and gap_a.lower().startswith("requires"):
        return gap_a
    if gap_b and "No direct equivalent" in gap_b:
        return f"Concept absent in target language"
    if gap_a and gap_b and gap_a != gap_b:
        return f"Approaches differ: A uses '{solution_a.get('approach', 'unknown')}', B uses '{solution_b.get('approach', 'unknown')}'"
    return None


def _compute_difficulty(problem_id: str, language: str) -> str:
    """Compute a difficulty rating for translating this problem to/from this language."""
    # Difficulty is based on how different this language's approach is
    difficulty_map = {
        "null_safety": {"JavaScript": "⭐⭐", "TypeScript": "⭐", "Rust": "⭐⭐", "Go": "⭐⭐⭐", "Java": "⭐⭐", "C/C++": "⭐⭐⭐⭐⭐"},
        "error_handling": {"Rust": "⭐⭐", "Go": "⭐⭐⭐", "TypeScript": "⭐⭐", "JavaScript": "⭐⭐", "Java": "⭐⭐", "C/C++": "⭐⭐⭐⭐"},
        "concurrency": {"Rust": "⭐⭐⭐", "Swift": "⭐⭐⭐", "Kotlin": "⭐⭐", "Java": "⭐⭐", "JavaScript": "⭐⭐⭐", "C/C++": "⭐⭐⭐⭐⭐"},
        "generics": {"C/C++": "⭐⭐⭐⭐", "Rust": "⭐⭐⭐", "Kotlin": "⭐⭐", "TypeScript": "⭐⭐", "Java": "⭐⭐", "JavaScript": "⭐"},
        "immutability": {"Rust": "⭐⭐", "Kotlin": "⭐⭐", "Swift": "⭐⭐", "JavaScript": "⭐⭐⭐", "Go": "⭐⭐⭐⭐", "C/C++": "⭐⭐⭐"},
        "async_patterns": {"Rust": "⭐⭐⭐", "Swift": "⭐⭐", "Kotlin": "⭐⭐", "Java": "⭐⭐⭐", "JavaScript": "⭐", "C/C++": "⭐⭐⭐⭐⭐"},
        "iteration": {"Rust": "⭐⭐", "Kotlin": "⭐⭐", "Java": "⭐⭐", "JavaScript": "⭐⭐", "Go": "⭐⭐⭐⭐", "C/C++": "⭐⭐⭐"},
        "resource_management": {"Rust": "⭐⭐", "Kotlin": "⭐⭐", "Java": "⭐⭐", "JavaScript": "⭐⭐⭐⭐", "Go": "⭐⭐⭐", "C/C++": "⭐⭐⭐"},
    }
    return difficulty_map.get(problem_id, {}).get(language, "⭐⭐")


def _build_bridge_path(languages: List[str], selected: str, slot: int) -> str:
    """Build a visual bridge emoji path showing the rotation."""
    idx = languages.index(selected)
    # Show selected language centered, neighbors on each side
    left = languages[idx - 1] if idx > 0 else languages[-1]
    right = languages[(idx + 1) % len(languages)]
    emoji_map = {
        "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
        "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "C/C++": "⚙️"
    }
    problem_emojis = [p["emoji"] for p in UNIVERSAL_PROBLEMS]
    problem_emoji = problem_emojis[slot]
    return f"{emoji_map.get(left, '🔧')} ════{problem_emoji}════ {emoji_map.get(selected, '🔧')} ════🌉═══ {emoji_map.get(right, '🔧')}"


def semantic_bridge(language: Optional[str] = None) -> Dict[str, Any]:
    """
    Main entry point: build a semantic bridge for the selected language.
    If language is None, uses the current rotation index.
    """
    config = load_rotation()
    languages = TOOL_LANGUAGES

    if language is None:
        current_idx = config.get("current_index", 0) % len(languages)
        language = languages[current_idx]

    return build_bridge(language)


def run_tests():
    """Run tests to validate the Polyglot Semantic Bridges module."""
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
            print(f"  ❌ FAIL: {msg}")

    def assert_true(a, msg=""):
        nonlocal tests_passed, tests_failed
        if a:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg}")

    print("Testing Polyglot Semantic Bridges...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(TOOL_LANGUAGES), "Tool manages 8 languages")
    assert_eq(True, 0 <= config["current_index"] < len(TOOL_LANGUAGES), "current_index in valid range for tool's 8 languages")
    assert_eq("Rust", TOOL_LANGUAGES[0], "Rust is first language")

    print("  Testing build_bridge for Rust...")
    result = build_bridge("Rust")
    expected_keys = [
        "tool", "version", "selected_language", "problem", "solution",
        "comparison", "translation_gaps", "difficulty_rating",
        "emoji_path", "next_language", "rotation_order", "timestamp"
    ]
    for key in expected_keys:
        assert_eq(True, key in result, f"Key '{key}' present in response")

    assert_eq("Rust", result["selected_language"], "Rust is selected")
    assert_eq("Rust", result["rotation_order"][0], "Rust is first in rotation_order")
    assert_eq("Go", result["next_language"], "Next language is Go")

    print("  Verifying problem structure...")
    prob = result["problem"]
    assert_eq(True, "id" in prob, "problem has id")
    assert_eq(True, "name" in prob, "problem has name")
    assert_eq(True, "emoji" in prob, "problem has emoji")
    assert_eq(True, "description" in prob, "problem has description")
    assert_eq(True, "why_it_matters" in prob, "problem has why_it_matters")
    assert_eq(True, "slot" in prob, "problem has slot")
    assert_true(len(prob["description"]) > 10, "problem description is non-empty")
    assert_true(len(prob["why_it_matters"]) > 10, "problem why_it_matters is non-empty")

    print("  Verifying solution structure...")
    sol = result["solution"]
    assert_eq(True, "approach" in sol, "solution has approach")
    assert_eq(True, "mechanism" in sol, "solution has mechanism")
    assert_eq(True, "code_example" in sol, "solution has code_example")
    assert_eq(True, "idiom" in sol, "solution has idiom")
    assert_eq(True, "translation_gap" in sol, "solution has translation_gap")
    assert_eq(True, "key_insight" in sol, "solution has key_insight")
    assert_true(len(sol["approach"]) > 5, "approach is non-empty")
    assert_true(len(sol["mechanism"]) > 10, "mechanism is substantive")
    assert_true(len(sol["code_example"]) > 5, "code_example is non-empty")
    assert_true(len(sol["key_insight"]) > 10, "key_insight is substantive")

    print("  Verifying comparison structure...")
    comp = result["comparison"]
    assert_eq(8, len(comp), "comparison has entries for all 8 languages")
    for lang in TOOL_LANGUAGES:
        assert_eq(True, lang in comp, f"comparison has entry for {lang}")
        assert_eq(True, "approach" in comp[lang], f"{lang} comparison has approach")
        assert_eq(True, "mechanism" in comp[lang], f"{lang} comparison has mechanism")
        assert_eq(True, "code_example" in comp[lang], f"{lang} comparison has code_example")
        assert_eq(True, "idiom" in comp[lang], f"{lang} comparison has idiom")
        assert_eq(True, "key_insight" in comp[lang], f"{lang} comparison has key_insight")

    print("  Verifying translation_gaps...")
    gaps = result["translation_gaps"]
    assert_true(isinstance(gaps, list), "translation_gaps is a list")
    for gap in gaps:
        assert_eq(True, "language" in gap, "gap has language field")
        assert_eq(True, "gap" in gap, "gap has gap description")
        assert_true(len(gap["gap"]) > 5, "gap description is substantive")
        assert_true(gap["language"] != result["selected_language"], "gap language is different from selected")

    print("  Verifying difficulty_rating...")
    assert_true("⭐" in result["difficulty_rating"], "difficulty_rating contains star emoji")

    print("  Verifying emoji_path...")
    assert_true("🌉" in result["emoji_path"], "emoji_path contains bridge emoji")
    assert_true("════" in result["emoji_path"], "emoji_path contains connector")

    print("  Verifying rotation update...")
    config2 = load_rotation()
    assert_eq(1, config2["current_index"], "Index advanced to 1 (Go)")
    assert_eq("Rust", config2["last_language"], "Last language recorded as Rust")

    # Reset rotation to known state before next test phase
    config = load_rotation()
    config["current_index"] = 1  # At Go
    config["last_language"] = "Rust"
    save_rotation(config)

    print("  Testing build_bridge for Go (next in rotation)...")
    result2 = build_bridge("Go")
    assert_eq("Go", result2["selected_language"], "Go is selected")
    assert_eq("Swift", result2["next_language"], "Next language is Swift")
    # Go's next should be Swift
    assert_eq("Swift", result2["next_language"], "Go -> Swift rotation is correct")

    print("  Testing all 8 languages have valid bridges...")
    for lang in TOOL_LANGUAGES:
        r = build_bridge(lang)
        assert_eq(lang, r["selected_language"], f"{lang} selected correctly")
        assert_eq(8, len(r["comparison"]), f"{lang}: comparison has 8 entries")
        assert_eq(True, "problem" in r, f"{lang}: result has problem field")
        assert_eq(True, "solution" in r, f"{lang}: result has solution field")
        assert_true(len(r["solution"]["key_insight"]) > 10, f"{lang}: key_insight is substantive")
        assert_true(len(r["emoji_path"]) > 5, f"{lang}: emoji_path is non-empty")

    print("  Testing all UNIVERSAL_PROBLEMS are covered...")
    problem_ids = {p["id"] for p in UNIVERSAL_PROBLEMS}
    expected_ids = {"null_safety", "error_handling", "concurrency", "generics",
                    "immutability", "async_patterns", "iteration", "resource_management"}
    assert_eq(expected_ids, problem_ids, "All 8 problem IDs are present")

    print("  Testing each problem has solutions for all 8 languages...")
    for problem in UNIVERSAL_PROBLEMS:
        for lang in TOOL_LANGUAGES:
            assert_eq(True, lang in problem["solutions"], f"Problem '{problem['id']}' has solution for {lang}")
            sol = problem["solutions"][lang]
            assert_true(len(sol.get("approach", "")) > 3, f"{lang} in {problem['id']}: approach is non-empty")
            assert_true(len(sol.get("mechanism", "")) > 10, f"{lang} in {problem['id']}: mechanism is substantive")
            assert_true(len(sol.get("code_example", "")) > 5, f"{lang} in {problem['id']}: code_example is non-empty")
            assert_true(len(sol.get("idiom", "")) > 5, f"{lang} in {problem['id']}: idiom is non-empty")
            assert_true(len(sol.get("key_insight", "")) > 10, f"{lang} in {problem['id']}: key_insight is substantive")

    print("  Testing invalid language handling...")
    try:
        build_bridge("Python")
        tests_failed += 1
        print("  ❌ FAIL: No error raised for invalid language")
    except ValueError as e:
        tests_passed += 1
        print("  ✅ PASS: ValueError raised for invalid language")
        assert_in("not in this tool's rotation", str(e), "Error mentions rotation")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ FAIL: Wrong exception: {e}")

    print("  Testing semantic_bridge() with None (auto-select)...")
    current_idx = load_rotation()["current_index"] % len(TOOL_LANGUAGES)
    current_lang = TOOL_LANGUAGES[current_idx]
    result_auto = semantic_bridge()
    assert_eq(current_lang, result_auto["selected_language"], f"Auto-selected: {current_lang}")

    print("  Testing emoji_path contains valid language emojis...")
    emoji_map = {"Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
                 "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "C/C++": "⚙️"}
    for lang in TOOL_LANGUAGES:
        r = build_bridge(lang)
        # Should contain the language's emoji
        assert_true(emoji_map[lang] in r["emoji_path"], f"{lang}: emoji_path contains {emoji_map[lang]}")

    print("  Testing difficulty_rating varies by language and problem...")
    seen_ratings = set()
    for lang in TOOL_LANGUAGES:
        r = build_bridge(lang)
        seen_ratings.add(r["difficulty_rating"])
    assert_true(len(seen_ratings) >= 2, f"Multiple difficulty ratings found: {seen_ratings}")

    print("  Testing next_language is different from selected...")
    for lang in TOOL_LANGUAGES:
        r = build_bridge(lang)
        assert_true(r["next_language"] != lang, f"{lang}: next_language differs from selected")

    print("  Testing timestamp format...")
    ts = result["timestamp"]
    assert_true("T" in ts, "timestamp has ISO format with T separator")

    print(f"\n{'='*55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("🌉 All Semantic Bridges tests passed! Every problem has a solution.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--bridge":
        language = sys.argv[2] if len(sys.argv) > 2 else None
        result = semantic_bridge(language)
        print(json.dumps(result, indent=2))
    else:
        print(f"Polyglot Semantic Bridges v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_bridges --test        # Run tests")
        print("  python -m polyglot_bridges --bridge [lang]  # Build semantic bridge")