"""
Fossil configuration and data definitions.
"""

# Rotation order (reversed to match physical file + prev-idx walking):
# Walking prev_idx = (idx - 1) % 8 gives: C/C++(7) → Java(6) → JS(5) → TS(4) → Kotlin(3) → Swift(2) → Go(1) → Rust(0) → loop
ROTATION_ORDER = [
    "C/C++",
    "Java",
    "JavaScript",
    "TypeScript",
    "Kotlin",
    "Swift",
    "Go",
    "Rust",
]

ROTATION_FILE = __import__("pathlib").Path(__file__).parent.parent.parent.parent / "language_rotation.json"

# Ancestor map: for each language, which prior languages influenced it
# Key = language, Value = list of ancestor languages (in order of influence)
ANCESTOR_MAP = {
    "Rust": ["C/C++"],
    "Go": ["C/C++"],
    "Swift": ["Objective-C", "Rust", "Python"],
    "Kotlin": ["Java"],
    "TypeScript": ["JavaScript"],
    "JavaScript": ["Scheme", "Java"],
    "Java": ["C/C++"],
    "C/C++": ["C"],
}

# Fossil definitions: each fossil has a name, concept description,
# and which languages carry it (INHERITED from ancestors)
FOSSIL_DEFINITIONS = {
    "null_safety": {
        "name": "Null Safety",
        "concept": "Language-level mechanisms to handle absence of value",
        "carriers": {
            "Rust": "Option<T>",
            "Kotlin": "Nullable types (T?)",
            "Swift": "Optional<T>",
            "TypeScript": "undefined / null",
            "Go": "nil (no compile-time safety)",
        },
    },
    "generics": {
        "name": "Generics / Parametric Polymorphism",
        "concept": "Writing code that works with multiple types without sacrificing type safety",
        "carriers": {
            "Rust": "impl<T>",
            "Go": "Go 1.18+ generics (type parameters)",
            "Kotlin": "<T>",
            "Swift": "Generic functions and types",
            "TypeScript": "Generic functions <T>",
            "Java": "Generics since Java 5",
            "C/C++": "Templates",
        },
    },
    "closure": {
        "name": "Closures / Lambda Expressions",
        "concept": "First-class functions that capture their lexical environment",
        "carriers": {
            "Rust": " closures |x| expr",
            "Go": "func literals / go func(){}",
            "Swift": " { (x: T) -> R in body }",
            "Kotlin": " { x: T -> body }",
            "TypeScript": " (x: T) => expr",
            "JavaScript": " function() {} or () => {}",
            "Java": " Lambda expressions since Java 8",
        },
    },
    "pattern_matching": {
        "name": "Pattern Matching",
        "concept": "Matching values against structures and binding variables",
        "carriers": {
            "Rust": "match expr { ... }",
            "Go": "type switch, select (limited)",
            "Swift": "switch with where, if case",
            "Kotlin": "when expression",
            "Java": "switch expressions (Java 14+)",
            "JavaScript": "destructuring in assignment",
        },
    },
    "ownership_borrow": {
        "name": "Ownership / Borrow Checking",
        "concept": "Resource management through ownership transfer and loan inspection",
        "carriers": {
            "Rust": "move semantics, & and &mut borrows, lifetimes",
            "C/C++": "manual move semantics (C++11+)",
        },
    },
    "goroutine_channel": {
        "name": "CSP-style Concurrency Primitives",
        "concept": "Lightweight concurrency via channels and goroutines/actors",
        "carriers": {
            "Go": "goroutines + channels",
            "Kotlin": "coroutines (similar mental model)",
            "Rust": "async/await + channels (Tokio)",
            "Swift": "async/await (Swift 5.5+)",
        },
    },
    "type_inference": {
        "name": "Type Inference",
        "concept": "Compiler deduces types without explicit annotation",
        "carriers": {
            "Rust": "let x = 42; // i32 inferred",
            "Go": "x := 42 // type inferred",
            "Swift": "let x = 42 // inferred",
            "Kotlin": "val x = 42 // inferred",
            "TypeScript": "const x: number = 42 (partial inference)",
            "JavaScript": "const x = 42 (inferred at runtime)",
            "Java": "var x = 42 (Java 10+)",
        },
    },
    "immutable_default": {
        "name": "Immutable by Default",
        "concept": "Variables/values are immutable unless explicitly declared mutable",
        "carriers": {
            "Rust": "let (immutable) / let mut (mutable)",
            "Go": "all vars are mutable; const for constants",
            "Swift": "let (immutable) / var (mutable)",
            "Kotlin": "val (immutable) / var (mutable)",
            "JavaScript": "const (immutable binding)",
            "Java": "final fields, immutable object patterns",
        },
    },
    "error_as_value": {
        "name": "Error as Value / Algebraic Error Types",
        "concept": "Errors handled as values in the type system, not exceptions",
        "carriers": {
            "Rust": "Result<T, E>",
            "Go": "multiple return values (error)",
            "Swift": "Result<T, Error>",
            "Kotlin": "sealed class Result, Throwable",
            "Java": "Optional<T> (partial), checked exceptions",
            "C/C++": "std::expected (C++23)",
        },
    },
    "struct_adt": {
        "name": "Algebraic Data Types (ADTs)",
        "concept": "Types formed by Sum (OR) and Product (AND) constructions",
        "carriers": {
            "Rust": "enum with variants (tagged unions), struct",
            "Swift": "enum with associated values, struct",
            "Kotlin": "sealed classes, data classes",
            "TypeScript": "union types, interface",
            "Go": "struct + interface (structural typing)",
            "Java": "sealed classes (Java 17+)",
        },
    },
    "destructuring": {
        "name": "Destructuring / Pattern Decomposition",
        "concept": "Breaking structured values into constituent parts",
        "carriers": {
            "Rust": "let (a, b) = tuple; let Foo { x, y } = foo;",
            "Go": "a, b := tuple[0], tuple[1] (no native destructuring)",
            "Swift": "let (x, y) = point; if case Foo(x) = bar",
            "Kotlin": "val (a, b) = pair; destructuring declarations",
            "TypeScript": "const { x, y } = obj; const [a, b] = arr",
            "JavaScript": "const { x, y } = obj; const [a, b] = arr",
            "Java": "record pattern matching (Java 16+)",
        },
    },
    "trait_bounds": {
        "name": "Trait Bounds / Interfaces / Protocols",
        "concept": "Constraining generics with capabilities contracts",
        "carriers": {
            "Rust": "impl<T: Clone>",
            "Go": "interface{} + method sets",
            "Swift": "protocol<T>",
            "Kotlin": "interface, where clauses",
            "TypeScript": "interface, extends keyword",
            "Java": "interface, abstract classes",
            "C/C++": "concepts (C++20)",
        },
    },
    "module_system": {
        "name": "Modules / Namespaces",
        "concept": "Organizing code into named scopes",
        "carriers": {
            "Rust": "mod, crate, use",
            "Go": "package, import",
            "Swift": "struct, enum (inner), module via import",
            "Kotlin": "package, import, namespace",
            "TypeScript": "namespace, ES modules",
            "JavaScript": "ES modules (import/export)",
            "Java": "package, import",
            "C/C++": "namespace, header includes",
        },
    },
    "iterator_protocol": {
        "name": "Iterator / Sequence Protocol",
        "concept": "Traversing collections via a standardized protocol",
        "carriers": {
            "Rust": "Iterator trait, .into_iter(), .iter()",
            "Go": "range over slices/maps",
            "Swift": "Sequence, IteratorProtocol",
            "Kotlin": "Iterable, Sequence, forEach",
            "TypeScript": "for...of, Array methods",
            "JavaScript": "for...of, Symbol.iterator",
            "Java": "java.lang.Iterable, for-each",
        },
    },
    "smart_pointer": {
        "name": "Smart Pointers",
        "concept": "RAII-based ownership wrappers with automatic cleanup",
        "carriers": {
            "Rust": "Box<T>, Rc<T>, Arc<T>, Cell<T>",
            "C/C++": "std::unique_ptr, std::shared_ptr, std::weak_ptr",
            "Go": "pointers (no RAII, GC)",
            "Swift": "class types, autorelease pools",
            "Kotlin": "managed references, no raw pointers",
        },
    },
    "async_await": {
        "name": "Async/Await Syntax",
        "concept": "Syntactic sugar for asynchronous programming",
        "carriers": {
            "Rust": "async/await (via async-std or Tokio)",
            "Go": "goroutines + channels (no async keyword)",
            "Swift": "async/await (Swift 5.5+)",
            "Kotlin": "suspend functions (coroutines)",
            "TypeScript": "async/await",
            "JavaScript": "async/await",
            "Java": "virtual threads (Java 21), CompletableFuture",
        },
    },
    "memory_model": {
        "name": "Memory Model / Atomics",
        "concept": "Formal specification of memory behavior under concurrency",
        "carriers": {
            "Rust": "unsafe Rust atomics, std::sync::atomic",
            "Go": "memory model (happens-before)",
            "Swift": "Sendable, actor isolation",
            "C/C++": "C++11 memory model, std::atomic",
            "Java": "Java Memory Model, java.util.concurrent.atomic",
        },
    },
    "comprehensions": {
        "name": "Comprehensions / Collection Literals",
        "concept": "Creating collections from expressions",
        "carriers": {
            "Rust": "[expr; n], vec![], HashMap",
            "Go": "slice := []int{1, 2, 3}",
            "Swift": "Array<Int>(), Dictionary",
            "Kotlin": "listOf(), mapOf(), setOf()",
            "TypeScript": "[], {}, Array.from()",
            "JavaScript": "[], {}, Array literal",
            "Java": "Arrays.asList(), List.of()",
        },
    },
}

# How many steps back in the rotation to consider ancestors
ANCESTOR_DEPTH = 3