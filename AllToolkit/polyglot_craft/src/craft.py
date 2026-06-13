#!/usr/bin/env python3
"""
🛠️ Polyglot Craft v1.0 — Language Crafting Recipes.

Creative concept: "Every language has a craft — a way of working with it
that only makes sense within that language's philosophy. This tool
distills that craft into a single practical skill card you can study
in 10 minutes and start using immediately."

Unlike existing tools:
  - polyglot_resonator:    maps thinking philosophy per language
  - polyglot_digest:        syntax-parallel code (same logic, different syntax)
  - polyglot_translation:  cultural idioms/proverbs
  - polyglot_chronology:   geological timeline of language emergence
  - polyglot_signal:        signal semantics (how languages signal conditions)
  - polyglot_harmony:       compatibility between consecutive pairs
  - polyglot_sentinel:      ecosystem monitoring

Polyglot Craft distills the PRACTICAL CRAFT of a language into:
  - 3 signature patterns (most idiomatic constructs)
  - 3 blind spots (gotchas for devs coming from other languages)
  - 1 mental model (operating principle)
  - 3 micro-exercises (code snippets to internalize feel)

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-craft"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent.parent  # polyglot_craft/
_WORKSPACE_ROOT = _MODULE_DIR.parent                 # AllToolkit/ -> workspace/
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ─────────────────────────────────────────────────────────────────────────────
# Language Craft Database
# ─────────────────────────────────────────────────────────────────────────────

CRAFT_DB: Dict[str, Dict[str, Any]] = {

    "Rust": {
        "mental_model": "The compiler is your pair programmer — it catches every mistake at compile time, so embrace the error messages.",
        "emoji": "🦀",
        "signature_patterns": [
            {
                "name": "Result propagation with ?",
                "pattern": "let f = File::open(\"data\")?;",
                "why": "The ? operator unwraps Ok and propagates Err — eliminates boilerplate match chains.",
            },
            {
                "name": "match for exhaustive control flow",
                "pattern": "match opt { Some(x) => process(x), None => default() }",
                "why": "Rust's match must cover every variant — the compiler enforces completeness.",
            },
            {
                "name": "Struct with impl methods",
                "pattern": "struct Counter { count: u32 }\nimpl Counter { fn new() -> Self { Self { count: 0 } } fn inc(&mut self) { self.count += 1 } }",
                "why": "Data and behavior live together. No classes — structs + impl blocks are the Rust OOP model.",
            },
        ],
        "blind_spots": [
            {
                "from": "other languages",
                "issue": "Ownership and borrowing feel like runtime garbage collection — but they're entirely compile-time.",
                "idiom": "// Drop fires when the variable goes out of scope — no GC, no reference counting needed\nfn scope_demo() { let s = String::from(\"hello\"); } // s dropped here, no heap leak",
            },
            {
                "from": "Python/JavaScript",
                "issue": "Default variables are immutable. Trying to mutate a let binding after the fact is a compile error.",
                "idiom": "let x = 5; x = 6; // error[E0384]: cannot assign twice to immutable variable `x`",
            },
            {
                "from": "Java/C++",
                "issue": "No exceptions — errors are values in Result<T, E>. Throwing an exception doesn't exist.",
                "idiom": "// No throw keyword. Errors must be explicitly propagated via Result<T, E>\nfn read() -> Result<String, io::Error> { Ok(\"data\".to_string()) }",
            },
        ],
        "micro_exercises": [
            {
                "title": "Chain two Result-returning functions with ?",
                "snippet": "fn first() -> Result<u32, &'static str> { Ok(1) }\nfn second(x: u32) -> Result<u32, &'static str> { Ok(x * 2) }\nfn main() { let r = first().and_then(second); println!(\"{:?}\", r); } // Ok(2)",
                "concept": "Result.and_then for rail-switching error handling",
            },
            {
                "title": "Use Option to safely unwrap a value with a default",
                "snippet": "let values = [Some(1), None, Some(3)];\nlet sum: u32 = values.iter().filter_map(|x| *x).sum();\nassert_eq!(sum, 4);",
                "concept": "filter_map to skip None values and unwrap Some in one step",
            },
            {
                "title": "Define a struct with a constructor and a mutating method",
                "snippet": "struct Stack<T> { items: Vec<T> }\nimpl<T> Stack<T> {\n  fn new() -> Self { Self { items: vec![] } }\n  fn push(&mut self, item: T) { self.items.push(item); }\n  fn pop(&mut self) -> Option<T> { self.items.pop() }\n}",
                "concept": "Generic structs with impl blocks — data and behavior co-located",
            },
        ],
    },

    "Go": {
        "mental_model": "Simplicity is the goal — explicit is better than implicit, and concurrency is a first-class citizen.",
        "emoji": "🐹",
        "signature_patterns": [
            {
                "name": "Multiple return values (error as last value)",
                "pattern": "result, err := riskyCall()\nif err != nil { return err }\n// use result",
                "why": "Errors are values, not exceptions. The idiomatic Go error check is inline and explicit.",
            },
            {
                "name": "Goroutine + channel for concurrency",
                "pattern": "ch := make(chan int)\ngo func() { ch <- compute() }()\nresult := <-ch",
                "why": "Goroutines are cheap threads. Channels communicate between them. No shared memory by default.",
            },
            {
                "name": "Interface for polymorphism",
                "pattern": "type Writer interface { Write([]byte) error }\n// Anything with Write([]byte) error satisfies Writer — no explicit declaration",
                "why": "Interfaces are implicit. A type satisfies an interface by implementing its methods — no 'implements' keyword.",
            },
        ],
        "blind_spots": [
            {
                "from": "Java/Python",
                "issue": "Go has no classes, no inheritance, and no generics (pre-1.18). Methods are defined on structs directly.",
                "idiom": "type Counter struct { count int }\nfunc (c *Counter) Add(n int) { c.count += n } // method on ptr receiver, no class keyword",
            },
            {
                "from": "JavaScript",
                "issue": "nil slices behave like empty slices but are not the same — appending to nil allocates.",
                "idiom": "var s []int; s = append(s, 1); // s is now []int{1}, not nil. len(s) == 1.",
            },
            {
                "from": "C/C++",
                "issue": "No exceptions. All errors are returned as error values. defer is the cleanup mechanism.",
                "idiom": "f, _ := os.Open(file); defer f.Close() // defer runs at end of enclosing function",
            },
        ],
        "micro_exercises": [
            {
                "title": "Fan-out: spawn multiple goroutines, collect results via channel",
                "snippet": "func main() {\n  ch := make(chan int, 3)\n  for i := 1; i <= 3; i++ {\n    go func(n int) { ch <- n * n }(i)\n  }\n  for i := 0; i < 3; i++ { fmt.Println(<-ch) }\n}",
                "concept": "Goroutines are cheap — spawning many is cheap. Buffered channels prevent deadlock.",
            },
            {
                "title": "Implement an interface by defining its methods",
                "snippet": "type Reader interface { Read([]byte) (int, error) }\ntype NullReader struct {}\nfunc (NullReader) Read(b []byte) (int, error) { return len(b), nil }\n// NullReader satisfies Reader — no explicit declaration needed",
                "concept": "Implicit interface satisfaction — struct defines methods = struct implements interface",
            },
            {
                "title": "Use defer to ensure cleanup runs even on panic",
                "snippet": "func safeOp() {\n  f, err := os.Open(\"data\")\n  if err != nil { return }\n  defer f.Close()\n  // ... work with f. Close() runs even if function panics.\n}",
                "concept": "defer runs LIFO (last-in-first-out) at function exit — guaranteed cleanup",
            },
        ],
    },

    "Swift": {
        "mental_model": "Safety and clarity first — the compiler prevents entire categories of bugs, and the syntax is designed to be read aloud.",
        "emoji": "🦅",
        "signature_patterns": [
            {
                "name": "guard let for early-exit unwrap",
                "pattern": "guard let name = user.name else { return }",
                "why": "guard let unwraps Optional and requires exit on nil — keeps the happy path at the top level.",
            },
            {
                "name": "Struct + protocol for composition",
                "pattern": "struct Bird { var name: String }\nprotocol Flyable { var altitude: Int { get } }\nextension Bird: Flyable { var altitude: Int { 100 } }",
                "why": "Swift prefers structs over classes. Protocols add behavior without inheritance. Extensions retrofit protocols.",
            },
            {
                "name": "async/await for async flow",
                "pattern": "let data = try await fetch()\nlet processed = process(data)",
                "why": "async/await makes asynchronous code read like synchronous code — no pyramid of callbacks.",
            },
        ],
        "blind_spots": [
            {
                "from": "Objective-C",
                "issue": "Swift uses value types (struct, enum) by default where ObjC used reference types (class). Copy-on-write makes them efficient.",
                "idiom": "var arr = [1, 2, 3]; var arr2 = arr; arr2.append(4); // arr is unchanged — copy on write",
            },
            {
                "from": "Python",
                "issue": "Swift is strongly typed at compile time. Generic type parameters must be specified or inferred — no dynamic duck typing.",
                "idiom": "func identity<T>(_ x: T) -> T { x } // T is a type parameter, not a runtime variable",
            },
            {
                "from": "Java/Kotlin",
                "issue": "Swift has no checked exceptions. Errors are propagated via throws, but there's no 'throws' in the function signature for non-throwing functions.",
                "idiom": "enum MyError: Error { case badInput, notFound }\nfunc risky() throws -> String { throw MyError.notFound }\ndo { try risky() } catch { print(error) }",
            },
        ],
        "micro_exercises": [
            {
                "title": "Chain optional unwrapping with optional chaining and nil coalescing",
                "snippet": "struct User { var address: Address? }\nstruct Address { var street: String? }\nlet u = User(address: Address(street: \"123 Main\"))\nlet street: String = u.address?.street ?? \"unknown\" // \"123 Main\"",
                "concept": "?. for optional chaining, ?? for nil coalescing — no explicit unwrap needed",
            },
            {
                "title": "Define an enum with associated values and a switch handler",
                "snippet": "enum Result<T> { case success(T); case failure(Error) }\nfunc handle<T>(_ r: Result<T>) {\n  switch r { case .success(let v): print(v); case .failure(let e): print(e) }\n}",
                "concept": "Enums with associated values = tagged unions. The compiler forces exhaustive switch coverage.",
            },
            {
                "title": "Actor for thread-safe state",
                "snippet": "actor Counter { private var count = 0; func inc() { count += 1 } }\nTask { let c = Counter(); await c.inc() }",
                "concept": "Actors isolate state — no data races by construction. async/await for actor communication.",
            },
        ],
    },

    "Kotlin": {
        "mental_model": "Pragmatic JVM language that merges the best of Java and functional programming — null safety is a first-class concept.",
        "emoji": "🟣",
        "signature_patterns": [
            {
                "name": "Extension functions",
                "pattern": "fun String.addExclamation() = this + \"!\"\nval msg = \"hello\".addExclamation() // \"hello!\"",
                "why": "Add behavior to existing classes without inheritance or decoration. The most-loved Kotlin feature.",
            },
            {
                "name": "Data class + destructuring",
                "pattern": "data class Point(val x: Int, val y: Int)\nval (px, py) = Point(3, 4) // x=3, y=4",
                "why": "data class auto-generates equals, hashCode, toString, copy, and component functions for destructuring.",
            },
            {
                "name": "Coroutine suspend functions",
                "pattern": "suspend fun fetchData(): String { delay(1000); return \"data\" }\n// launch in a scope: launch { val d = fetchData() }",
                "why": "Coroutines are stackless threads — suspending is non-blocking and cheap. Structured concurrency scopes.",
            },
        ],
        "blind_spots": [
            {
                "from": "Java",
                "issue": "Kotlin has no checked exceptions. A function that throws doesn't declare it — callers aren't forced to handle.",
                "idiom": "fun readFile(): List<String> = Files.readAllLines(path) // no throws IOException in signature",
            },
            {
                "from": "Scala",
                "issue": "Kotlin has no case classes in the Scala sense — data class is the equivalent, but doesn't have the same pattern matching.",
                "idiom": "data class Result<out T>(val value: T, val error: Throwable? = null) // no sealed exhaustiveness",
            },
            {
                "from": "Python",
                "issue": "Kotlin is statically typed. Generics use declaration-site variance (out/in) — not use-site like Java's ? super.",
                "idiom": "interface Producer<out T> { fun produce(): T } // out T = covariant. interface Consumer<in T> { fun consume(t: T) }",
            },
        ],
        "micro_exercises": [
            {
                "title": "Elvis operator + safe call for safe null access",
                "snippet": "data class User(val name: String?, val age: Int?)\nval u = User(\"Alice\", null)\nval displayAge = u.age ?: \"unknown\" // \"unknown\"\nval nameLen = u.name?.length ?: 0 // 5",
                "concept": "?. for safe call, ?: for elvis (default on null) — Kotlin's null safety at a glance",
            },
            {
                "title": "Sequence for lazy collection processing",
                "snippet": "val result = listOf(1, 2, 3, 4, 5)\n  .asSequence()\n  .map { it * it }\n  .filter { it > 5 }\n  .take(2)\n  .toList() // [9, 16, 25] → [9, 16, 25] → [25] → [16, 25] → [16, 25]",
                "concept": "Sequences are lazy (intermediate ops don't execute until terminal op) — efficient for large data",
            },
            {
                "title": "Use 'reified' generics with inline to get type at runtime",
                "snippet": "inline fun <reified T> serialize(value: T): String = JSON.stringify(value)\nval json: String = serialize<User>(User(\"Bob\")) // type T is reified, available at runtime",
                "concept": "reified makes type parameter T available at runtime — normally generics are erased",
            },
        ],
    },

    "TypeScript": {
        "mental_model": "TypeScript adds a optional type layer on top of JavaScript — type annotations are erased, but the compiler checks your work.",
        "emoji": "🔷",
        "signature_patterns": [
            {
                "name": "Structural typing via interface",
                "pattern": "interface Named { name: string }\nfunction greet(p: Named) { console.log(\"Hello \" + p.name) }\n// Any object with a .name string satisfies Named — no explicit 'implements'",
                "why": "TypeScript uses structural typing — if it has the right shape, it fits. No nominal type declarations needed.",
            },
            {
                "name": "Discriminated union + exhaustive switch",
                "pattern": "type Result<T> = { ok: true; value: T } | { ok: false; error: string }\nfunction unwrap<T>(r: Result<T>): T {\n  if (r.ok) return r.value;\n  throw new Error(r.error);\n}",
                "why": "Discriminated unions with a shared literal field let the compiler narrow types in branches.",
            },
            {
                "name": "Generic constraints with keyof",
                "pattern": "function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] { return obj[key] }\nconst name = getProperty({ name: \"Alice\", age: 30 }, \"name\") // string",
                "why": "keyof T creates a union of the keys of T. K extends keyof T ensures the key is valid at compile time.",
            },
        ],
        "blind_spots": [
            {
                "from": "Java/C#",
                "issue": "TypeScript types are erased at runtime. There's no runtime type information — typeof at runtime sees only the JavaScript value.",
                "idiom": "interface Person { name: string; age: number }\nconst p: Person = { name: \"Alice\", age: 30 };\ntypeof p === 'Person' // false — types are compile-time only. typeof p === 'object' // true",
            },
            {
                "from": "Python",
                "issue": "TypeScript has no optional parameters in the Python sense — use default values or the ? operator, not Python's None default.",
                "idiom": "function greet(name: string = \"World\"): string { return `Hello ${name}` } // default value in signature",
            },
            {
                "from": "Rust/Kotlin",
                "issue": "TypeScript's null/undefined is not handled by the type system by default — strictNullChecks is needed for compile-time null safety.",
                "idiom": "// tsconfig: \"strictNullChecks\": true\nlet name: string | null = getName();\nif (name !== null) { console.log(name.toUpperCase()); } // name narrowed to string in branch",
            },
        ],
        "micro_exercises": [
            {
                "title": "Model a Result type with a discriminated union",
                "snippet": "type Result<T, E> =\n  | { success: true; value: T }\n  | { success: false; error: E };\n\nfunction map<T, E, U>(r: Result<T, E>, f: (v: T) => U): Result<U, E> {\n  return r.success ? { success: true, value: f(r.value) } : r;\n}",
                "concept": "Discriminated union with a boolean tag — TypeScript narrows the type inside each branch",
            },
            {
                "title": "Use keyof to constrain a generic function parameter",
                "snippet": "function pluck<T, K extends keyof T>(obj: T, keys: K[]): T[K][] {\n  return keys.map(k => obj[k]);\n}\nconst user = { name: \"Alice\", age: 30, admin: true };\nconst vals = pluck(user, [\"name\", \"age\"]); // (string | number)[]",
                "concept": "K extends keyof T guarantees type-safe property access — the compiler catches invalid keys",
            },
            {
                "title": "Use satisfies to validate without widening type",
                "snippet": "const palette = {\n  red: [255, 0, 0], green: \"#00ff00\", blue: [0, 0, 255]\n} satisfies Record<string, string | number[]>;\n// palette.red is still [255, 0, 0] (number[]), not widened to string | number[]",
                "concept": "satisfies validates the shape without losing the literal type — preserves autocomplete on narrow types",
            },
        ],
    },

    "JavaScript": {
        "mental_model": "JavaScript runs in one thread via an event loop — everything async is a callback, promise, or async function waiting on that single thread.",
        "emoji": "🟨",
        "signature_patterns": [
            {
                "name": "Closures for private state",
                "pattern": "function makeCounter() { let count = 0; return { inc: () => ++count, get: () => count } }\nconst c = makeCounter(); c.inc(); c.get(); // 1",
                "why": "Closures capture variables from their enclosing scope. makeCounter's count is private — not accessible except via returned methods.",
            },
            {
                "name": "Destructuring + rest/spread",
                "pattern": "const { name, ...rest } = { name: \"Alice\", age: 30, city: \"NYC\" };\n// name = \"Alice\", rest = { age: 30, city: \"NYC\" }",
                "why": "Destructuring unpacks values from objects/arrays. Rest collects remaining properties into a new object.",
            },
            {
                "name": "Promises + async/await",
                "pattern": "const result = await fetch(url).then(r => r.json());\nasync function load() { const data = await fetch(url); return data.json(); }",
                "why": "async functions return Promises. await suspends the function's execution without blocking the thread — non-blocking async.",
            },
        ],
        "blind_spots": [
            {
                "from": "Python/Ruby",
                "issue": "JavaScript has no list comprehension, no generator expressions, and no built-in map/filter/reduce on Object (only Array).",
                "idiom": "// Object.keys(obj).map() is the idiom for mapping over object values\nObject.entries({a:1, b:2}).forEach(([k, v]) => console.log(k, v));",
            },
            {
                "from": "Java",
                "issue": "JavaScript has no block-scoped constants — const means the binding is fixed, but objects it points to are mutable.",
                "idiom": "const obj = { x: 1 }; obj.x = 2; // OK — obj is const but obj's properties are mutable. obj = {} // TypeError",
            },
            {
                "from": "Rust",
                "issue": "JavaScript has no Option/Maybe type — absence is signaled with undefined or null. No compile-time enforcement.",
                "idiom": "const name = map.get('key'); if (name === undefined || name === null) { /* absence */ } // runtime check only",
            },
        ],
        "micro_exercises": [
            {
                "title": "Implement a simple event emitter using closures",
                "snippet": "function EventEmitter() {\n  const handlers = {};\n  return {\n    on(event, fn) { (handlers[event] = handlers[event] || []).push(fn); },\n    emit(event, ...args) { (handlers[event] || []).forEach(h => h(...args)); }\n  };\n}",
                "concept": "Closures encapsulate private state (handlers) while exposing public methods — the module pattern",
            },
            {
                "title": "Use Promise.all to run multiple async operations in parallel",
                "snippet": "const [a, b] = await Promise.all([\n  fetch('/api/a').then(r => r.json()),\n  fetch('/api/b').then(r => r.json())\n]);",
                "concept": "Promise.all waits for all promises — parallel execution. Promise.race resolves on first settling.",
            },
            {
                "title": "Use a WeakMap for private object state",
                "snippet": "const _cache = new WeakMap();\nclass Cache {\n  constructor() { _cache.set(this, new Map()); }\n  set(k, v) { _cache.get(this).set(k, v); }\n  get(k) { return _cache.get(this).get(k); }\n}",
                "concept": "WeakMap keys are objects and are garbage-collected when the key object is gone — perfect for per-instance private state",
            },
        ],
    },

    "Java": {
        "mental_model": "Write once, run anywhere — Java's contract is the class file, not the machine. Object-orientation is the primary organizing principle.",
        "emoji": "☕",
        "signature_patterns": [
            {
                "name": "Interface + implementation class",
                "pattern": "interface Animal { String speak(); }\nclass Dog implements Animal { public String speak() { return \"woof\"; } }",
                "why": "Interfaces define contracts. Classes implement them. A method can accept Animal — any implementation satisfies the contract.",
            },
            {
                "name": "Stream API for functional data processing",
                "pattern": "List<String> names = people.stream().filter(p -> p.age > 18).map(p -> p.name).collect(Collectors.toList());",
                "why": "Streams are lazy pipelines — intermediate ops don't execute until a terminal op (collect, forEach, reduce) triggers them.",
            },
            {
                "name": "try-with-resources for automatic cleanup",
                "pattern": "try (var f = new FileReader(\"data\")) { f.read(); } // f.close() called automatically",
                "why": "Any resource implementing AutoCloseable is closed at end of try block — no manual finally needed.",
            },
        ],
        "blind_spots": [
            {
                "from": "Kotlin/Scala",
                "issue": "Java has no extension functions. You must either add methods to the class or use static utility methods (Collections.sort(list)).",
                "idiom": "// Java 8+ default methods let you add behavior to interfaces without modifying implementing classes:\ninterface List<T> { default void sort(Comparator<? super T> c) { Collections.sort(this, c); } }",
            },
            {
                "from": "Python",
                "issue": "Java has no first-class functions — methods are not values. Use lambda for simple cases, or Method References (String::toUpperCase).",
                "idiom": "list.stream().map(String::toUpperCase).collect(Collectors.toList()); // method reference, not lambda",
            },
            {
                "from": "Rust",
                "issue": "Java has no value types (struct) — everything is a reference except primitives. Primitives auto-box to reference types.",
                "idiom": "int x = 5; // primitive, stored inline. Integer x2 = 5; // boxed, heap allocated. Streams auto-box primitives.",
            },
        ],
        "micro_exercises": [
            {
                "title": "Use Optional to safely handle absence",
                "snippet": "Optional<String> name = Optional.ofNullable(getName());\nString greeting = name.map(String::toUpperCase).orElse(\"anonymous\");",
                "concept": "Optional<T> is a container that may or may not hold a value — forces explicit handling instead of null",
            },
            {
                "title": "Implement a Comparator using Comparator.comparing",
                "snippet": "List<Person> sorted = people.stream()\n  .sorted(Comparator.comparing(Person::getName).reversed())\n  .collect(Collectors.toList());",
                "concept": "Comparator.comparing builds a comparator from a function — method references keep it concise",
            },
            {
                "title": "Use CompletableFuture for async chaining",
                "snippet": "CompletableFuture.supplyAsync(() -> fetchUser(id))\n  .thenApply(User::getEmail)\n  .thenCompose(email -> sendEmail(email))\n  .exceptionally(ex -> { logger.error(ex); return null; })\n  .join();",
                "concept": "CompletableFuture chains async steps — supplyAsync starts, thenApply maps, thenCompose flattens nested futures",
            },
        ],
    },

    "C/C++": {
        "mental_model": "You control everything — memory, layout, threading. The compiler does what you tell it, not what you meant. Zero-cost abstraction means you pay only for what you use.",
        "emoji": "⚙️",
        "signature_patterns": [
            {
                "name": "RAII (Resource Acquisition Is Initialization)",
                "pattern": "{\n  std::lock_guard<std::mutex> lk(m);\n  // critical section\n} // lock_guard destructor releases mutex automatically",
                "why": "RAII ties resource lifetimes to object lifetimes. When the object goes out of scope, the destructor releases the resource.",
            },
            {
                "name": "Template metaprogramming for generic containers",
                "pattern": "template<typename T, size_t N>\nstruct Array { T data[N]; T* begin() { return data; } T* end() { return data + N; } };\nArray<int, 3> ints = {{1, 2, 3}};",
                "why": "Templates generate type-specific code at compile time — no boxing, no virtual dispatch for container operations.",
            },
            {
                "name": "Smart pointers for heap-allocated objects",
                "pattern": "auto ptr = std::make_unique<int>(42); // exclusive ownership\nauto shared = std::make_shared<int>(42); // shared ownership\n// ptr and shared free their memory automatically when destroyed",
                "why": "Smart pointers prevent memory leaks by tying deallocation to object destruction. unique_ptr = exclusive, shared_ptr = shared.",
            },
        ],
        "blind_spots": [
            {
                "from": "Java/Python",
                "issue": "C++ has no garbage collector. Dynamic memory (new) must be explicitly freed — or use smart pointers (RAII).",
                "idiom": "auto p = std::make_unique<int>(5); // unique_ptr — freed when p goes out of scope. raw new/delete are error-prone.",
            },
            {
                "from": "JavaScript",
                "issue": "C++ is statically typed with manual memory management. Arrays are not dynamic by default — std::vector is the dynamic array.",
                "idiom": "std::vector<int> v = {1, 2, 3}; v.push_back(4); // vector grows dynamically. int arr[10] is fixed-size.",
            },
            {
                "from": "Rust",
                "issue": "C++ has no ownership system — two pointers can point to the same memory ( Aliasing). No borrow checker.",
                "idiom": "int* p = new int(5); int* q = p; delete p; delete q; // double-free = undefined behavior. Use unique_ptr for exclusive ownership.",
            },
        ],
        "micro_exercises": [
            {
                "title": "Use std::lock_guard for exception-safe mutex locking",
                "snippet": "std::mutex m;\nvoid safe_increment() {\n  std::lock_guard<std::mutex> lock(m);\n  ++counter; // lock released automatically if exception thrown\n}",
                "concept": "RAII + lock_guard — destructor called on scope exit, guaranteed to release lock",
            },
            {
                "title": "Define a template function for type-safe printing",
                "snippet": "template<typename T>\nvoid print(const T& v) {\n  std::cout << v << std::endl;\n}\ntemplate<typename T, typename... Args>\nvoid print(const T& first, const Args&... rest) {\n  std::cout << first << ' ';\n  print(rest...); // recursive variadic template\n}",
                "concept": "Variadic templates for type-safe variadic functions — no void* or type erasure needed",
            },
            {
                "title": "Use std::future and std::async for parallel computation",
                "snippet": "auto fut1 = std::async(std::launch::async, [](){ return slow_computation(1); });\nauto fut2 = std::async(std::launch::async, [](){ return slow_computation(2); });\nint result = fut1.get() + fut2.get(); // runs in parallel",
                "concept": "std::async spawns a task — launch::async = new thread, launch::deferred = lazy (on .get())",
            },
        ],
    },
}


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
    """Advance the index, save, return the language we just finished with."""
    data = _load_rotation(config_path)
    langs = data["languages"]
    old_idx = data["current_index"]
    new_idx = (old_idx + 1) % len(langs)
    data["current_index"] = new_idx
    data["last_language"] = langs[old_idx]
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    _save_rotation(data, config_path)
    return langs[old_idx]


def generate_craft_card(
    rotate: bool = True,
    config_path: Optional[str] = None,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Generate a craft skill-card for the current rotation language.

    Args:
        rotate: advance rotation after generating
        config_path: optional path to language_rotation.json
        seed: optional seed for deterministic shuffling of micro-exercises (unused here for API compat)

    Returns:
        full craft card dict
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

    craft = CRAFT_DB.get(current_language, {})

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": current_language,
        "current_index": old_idx,
        "new_index": new_idx if rotate else None,
        "rotated": rotate,
        "mental_model": craft.get("mental_model", "?"),
        "emoji": craft.get("emoji", "🔧"),
        "signature_patterns": craft.get("signature_patterns", []),
        "blind_spots": craft.get("blind_spots", []),
        "micro_exercises": craft.get("micro_exercises", []),
        "rotation_order": ROTATION_ORDER,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def format_craft_card(m: Dict[str, Any]) -> str:
    """Format the craft card as a human-readable string."""
    lang = m["language"]
    emoji = m["emoji"]

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  🛠️  POLYGLOT CRAFT — Language Crafting Recipes                   ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Language     : {lang:<48}║",
        f"║  Index        : {m['current_index']:<48}║",
        f"║  Rotated      : {str(m['rotated']):<48}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🧠 MENTAL MODEL                                               ║",
        f"║  {m['mental_model']:<58}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  ✦ SIGNATURE PATTERNS                                           ║",
    ]

    for i, pat in enumerate(m["signature_patterns"], 1):
        lines.append(f"║  {i}. {pat['name']:<55}║")
        lines.append(f"║     Pattern : {pat['pattern'].split(chr(10))[0]:<47}║")
        for line in pat["pattern"].split(chr(10))[1:]:
            lines.append(f"║              {line:<47}║")
        lines.append(f"║     Why     : {pat['why']:<47}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  ⚠️  BLIND SPOTS                                                 ║",
    ]

    for spot in m["blind_spots"]:
        lines.append(f"║  From {spot['from']:<53}║")
        lines.append(f"║  Issue: {spot['issue']:<49}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🏋️ MICRO-EXERCISES                                               ║",
    ]

    for i, ex in enumerate(m["micro_exercises"], 1):
        lines.append(f"║  {i}. {ex['title']:<55}║")
        for line in ex["snippet"].split("\n")[:3]:
            lines.append(f"║     {line:<56}║")
        lines.append(f"║     Concept: {ex['concept']:<48}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🔄 ROTATION ORDER                                               ║",
        f"║  {' → '.join(ROTATION_ORDER):<58}║",
        "╚══════════════════════════════════════════════════════════════════╝",
    ]
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
    elif len(sys.argv) > 1 and sys.argv[1] == "--card":
        card = generate_craft_card()
        print(format_craft_card(card))
    else:
        print(f"Polyglot Craft v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_craft --test   # Run tests")
        print("  python -m polyglot_craft --card  # Generate craft card")
