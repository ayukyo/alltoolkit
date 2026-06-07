#!/usr/bin/env python3
"""
🎵 Polyglot Resonator v1.0

A creative tool that maps how each programming language "thinks" —
the mental models, philosophical assumptions, and cognitive frames
each language uses to solve the same universal programming problems.

For the selected rotation language, this tool picks a "concept frame"
(how you think about problems) and shows how that concept RESONATES
differently across languages — not just syntax, but the deeper
assumptions each language makes about reality.

Creative concept: "Every language is a different lens on the same universe.
This tool plays them in harmony — showing how the same note sounds
in every instrument."

Distinct from existing tools:
  - polyglot_digest:  syntax-parallel code snippets (same code, different syntax)
  - polyglot_synapse: conceptual bridges finding connections (similar concepts)
  - polyglot_chronicle: today's events and daily challenge (temporal focus)
  - polyglot_dna: genetic trait mapping (static characteristics)
  - language_compass: learning journey maps (future milestones)
  - language_archaeology: historical lineage (past focus)

Resonator is about HOW each language thinks — the mental model itself,
what it prioritizes, what it considers dangerous, what it considers idiomatic.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import random
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-resonator"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "language_rotation.json"
)

# ── Concept frames ─────────────────────────────────────────────────────────────
# Each concept frame explores HOW a language conceptualizes a universal problem.
# The "resonance" shows the language's philosophical stance, assumptions, and
# the mental model it imposes on the programmer.

CONCEPT_FRAMES: List[Dict[str, Any]] = [
    {
        "id": "identity",
        "name": "What is an Identity?",
        "emoji": "🪞",
        "question": "What does it mean for a value to be 'itself'?",
        "dimensions": [
            ("value_vs_reference", "Value vs Reference Identity"),
            ("mutability", "Mutability Assumptions"),
            ("equality", "Equality Semantics"),
        ],
        "resonance": {
            "Rust": {
                "stance": "Identity is a contract — enforced by the borrow checker",
                "summary": "Rust has no garbage collector because it tracks ownership. A value's identity is tied to who 'owns' it. When ownership moves, the old binding becomes invalid. This is not a limitation — it's a proof of identity.",
                "key_concept": "Ownership & Borrowing",
                "philosophy": "If it compiles, this specific chunk of memory is yours alone.",
                "idiom": "let moved = x; // x is gone. This is NOT a bug — it's the borrow checker proving x was moved.",
                "what_hides": "Rust hides nothing — the ownership graph is explicit in types. What it abstracts is the runtime cost (no GC).",
            },
            "Go": {
                "stance": "Identity is about what's inside the pointer",
                "summary": "Go has value types and pointer types, but the distinction is visible at the type level. Two values are identical if their contents are identical. The language is pragmatic: if it looks like a value, it's a value (passed by copy). If you want shared identity, pass a pointer.",
                "key_concept": "Pointers are explicit, values are copied",
                "philosophy": "Identity is what you point to, not the variable holding the pointer.",
                "idiom": "s := MyStruct{}; f(s) // s is COPIED. If f modifies s, caller sees nothing.",
                "what_hides": "Go hides the complexity of memory layout but exposes the pointer/value distinction clearly.",
            },
            "Swift": {
                "stance": "Identity depends on whether the type is a class or struct",
                "summary": "Swift collapses the value/reference distinction into type design. Structs are value types (copied), classes are reference types (shared). But Swift adds a layer: even value types can have identity when they wrap a reference type. The programmer designs identity through type choice.",
                "key_concept": "Value Types vs Reference Types as design choice",
                "philosophy": "You choose what identity means when you choose the type.",
                "idiom": "var s = MyStruct() // copy on assignment. But struct methods can mutate if marked mutating.",
                "what_hides": "Copy-on-write semantics for collections — copies are lazy and cheap until written.",
            },
            "Kotlin": {
                "stance": "Identity is a JVM concern — primitives are values, objects are references",
                "summary": "Kotlin inherits JVM identity semantics: primitives (Int, Boolean) are value types, everything else is a reference. But Kotlin adds `data classes` which give structural equality automatically, and `object` declarations for singletons. The language blurs the line between identity and equality.",
                "key_concept": "Data classes & equals() as identity",
                "philosophy": "Two objects are 'the same' if their contents match (data class) unless you care about reference identity.",
                "idiom": "data class User(val name: String) // equals() is auto-generated for field equality",
                "what_hides": "JVM object identity (== for references, .equals() for content). Kotlin makes == always mean equals().",
            },
            "TypeScript": {
                "stance": "Identity is structural — if it looks the same, it is the same",
                "summary": "TypeScript uses structural typing: a type's identity is its shape. Two objects with the same shape are type-compatible. At runtime, JavaScript objects have no inherent identity system — equality (===) compares primitives by value and objects by reference. TypeScript adds type safety without changing runtime semantics.",
                "key_concept": "Structural typing = identity by shape",
                "philosophy": "If it walks like a Duck and talks like a Duck, it IS a Duck (structurally).",
                "idiom": "interface Point { x: number; y: number } // any object with x,y is a Point",
                "what_hides": "The distinction between type-level identity and runtime identity. Types are erased at runtime.",
            },
            "JavaScript": {
                "stance": "Objects are dictionaries, identity is reference-based",
                "summary": "In JavaScript, everything is either a primitive (value semantics, compared by value) or an object (reference semantics, compared by reference). There's no user-defined value types. Object identity is simply: two variables point to the same heap allocation, or they don't.",
                "key_concept": "Primitives vs Objects — two distinct identity systems",
                "philosophy": "Primitives are immutable atoms. Objects are mutable dictionaries with reference identity.",
                "idiom": "const a = {}; const b = {}; a === b // false — different heap objects, even if identical contents",
                "what_hides": "JavaScript hides memory management entirely — the engine decides when objects die.",
            },
            "Java": {
                "stance": "Identity is JVM-defined: primitives are values, objects are references",
                "summary": "Java made the value/reference distinction explicit at the type level from day one. Two reference variables point to the same object if they hold the same reference. The identity of an object is its memory address. But with records (Java 16+) and data-oriented design, identity becomes more about content.",
                "key_concept": "Reference identity vs content equality",
                "philosophy": "Objects live on the heap, primitives live on the stack. Know which you're holding.",
                "idiom": "String a = new String(\"hi\"); String b = new String(\"hi\"); a == b // false, but a.equals(b) // true",
                "what_hides": "The garbage collector — objects become identity-less when unreferenced.",
            },
            "C/C++": {
                "stance": "Identity IS memory address — you control every byte",
                "summary": "In C/C++, a variable's identity IS its memory address. There's no garbage collector, no runtime. The programmer owns memory completely. Two pointers with the same address point to the same data. The language makes no distinction between identity and address — they're the same thing.",
                "key_concept": "Identity = memory address",
                "philosophy": "If you want identity, allocate memory. If you want a copy, copy bytes.",
                "idiom": "int a = 42; int b = a; // b is a COPY at a DIFFERENT address. &a != &b always.",
                "what_hides": "C++ hides very little — even references are just aliases for addresses. C hides more via pointer arithmetic complexity.",
            },
        },
    },
    {
        "id": "abstraction",
        "name": "What is an Abstraction?",
        "emoji": "🏗️",
        "question": "How does a language let you build higher-level concepts from lower ones?",
        "dimensions": [
            ("abstraction_cost", "Cost of Abstraction"),
            ("interface_flexibility", "Interface Flexibility"),
            ("what_enforces", "What Enforces the Abstraction"),
        ],
        "resonance": {
            "Rust": {
                "stance": "Zero-cost abstractions — the compiler proves there's no runtime overhead",
                "summary": "Rust's abstractions (traits, generics, iterators) are designed to compile to zero overhead. If you write a high-level iterator chain, it compiles to the same machine code as a hand-written loop. The compiler is an abstraction verifier — it proves your high-level code is efficient.",
                "key_concept": "Zero-cost abstraction via monomorphization",
                "philosophy": "You should never pay for what you don't use — including abstraction overhead.",
                "idiom": "iter.map(|x| x * 2).filter(|x| x > 0).collect::<Vec<_>>() // compiles to one loop",
                "what_hides": "The complexity of monomorphization and LLVM optimization passes.",
            },
            "Go": {
                "stance": "Abstractions are lightweight and explicit — no inheritance hierarchies",
                "summary": "Go prefers composition over inheritance. Interfaces are implicit — any type that implements an interface's methods satisfies it. There's no class hierarchy to navigate. Go's abstractions are intentionally shallow: you can always see what you're calling.",
                "key_concept": "Interfaces as implicit contracts",
                "philosophy": "Don't pay for what you don't need. Composition over inheritance.",
                "idiom": "type Reader interface { Read(p []byte) (n int, err error) } // any type with Read() satisfies it",
                "what_hides": "Interface dispatch has a small vtable lookup cost (but Go's compiler optimizes many cases).",
            },
            "Swift": {
                "stance": "Protocols — the language's most powerful abstraction tool",
                "summary": "Swift uses protocols to define abstractions. Protocols can have associated types, default implementations, and retroactive conformance. Swift's type system is sophisticated: you can express constraints, default implementations, and even protocol composition.",
                "key_concept": "Protocol-Oriented Programming",
                "philosophy": "Protocols define what a type can do, not what it inherits.",
                "idiom": "protocol Drawable { func draw() } // anything with draw() can be drawn",
                "what_hides": "Swift hides copy-on-write for value types behind the scenes.",
            },
            "Kotlin": {
                "stance": "Extension functions — add methods to types you don't own",
                "summary": "Kotlin's most distinctive abstraction tool is extension functions. You can add new functionality to existing classes without inheritance. Combined with interface default methods, Kotlin gives you powerful ways to build abstractions without deep inheritance chains.",
                "key_concept": "Extension functions & interfaces with default implementations",
                "philosophy": "Open/Closed principle made easy — extend without modifying.",
                "idiom": "fun String.addExclamation() = this + \"!\" // extends String without touching it",
                "what_hides": "Extensions are resolved statically at compile time — they don't actually modify the class.",
            },
            "TypeScript": {
                "stance": "Types as abstractions — structural typing makes interfaces free",
                "summary": "TypeScript uses structural types. If an object has the right shape, it satisfies the interface. You can define interfaces that are satisfied implicitly. Generics allow parametric polymorphism. TypeScript's abstractions are purely at the type level — erased at runtime.",
                "key_concept": "Structural typing = free interface conformance",
                "philosophy": "If the shape fits, the type conforms — no explicit declaration needed.",
                "idiom": "function process<T extends { id: number }>(item: T): T { return item; }",
                "what_hides": "All type information is erased. Runtime behavior is pure JavaScript.",
            },
            "JavaScript": {
                "stance": "Closures and prototypes — JS builds abstractions from functions and objects",
                "summary": "JavaScript has only two building blocks: functions and objects. Closures capture lexical scope. Prototypes delegate property lookup. Every class system (ES6+) is syntactic sugar over prototypes. This simplicity is powerful but requires understanding the underlying prototype chain.",
                "key_concept": "Prototypal inheritance + closures",
                "philosophy": "Everything is an object (or a function), and functions capture their environment.",
                "idiom": "const makeCounter = (() => { let count = 0; return () => ++count; })()",
                "what_hides": "The prototype chain — ES6 classes make it look like class-based inheritance.",
            },
            "Java": {
                "stance": "Interfaces + abstract classes — explicit hierarchy of abstraction levels",
                "summary": "Java separates interface (pure contract, pre-Java 8 no implementations) from abstract class (partial implementation). Generics use erasure. Java's abstractions are enforced at compile time but have runtime reflection. Virtual method dispatch makes abstraction cost visible.",
                "key_concept": "Interface segregation & abstract classes",
                "philosophy": "Program to an interface, not an implementation.",
                "idiom": "interface List<T> { void add(T t); T get(int i); } // contract, no implementation",
                "what_hides": "Generics type erasure — all generics are Object at runtime (except primitives).",
            },
            "C/C++": {
                "stance": "Templates — compile-time polymorphism with zero runtime cost",
                "summary": "C++ templates are a Turing-complete compile-time computation system. They enable generic programming without runtime overhead. Concepts (C++20) add compile-time constraints. Virtual functions provide runtime polymorphism with a vtable cost. The programmer chooses which to use.",
                "key_concept": "Templates = compile-time polymorphism",
                "philosophy": "If you can express it at compile time, you pay nothing at runtime.",
                "idiom": "template<typename T> T max(T a, T b) { return a > b ? a : b; } // monomorphized at compile time",
                "what_hides": "Template error messages are notoriously cryptic. The complexity lives in the compiler.",
            },
        },
    },
    {
        "id": "state",
        "name": "What is State?",
        "emoji": "🧪",
        "question": "How does a language model change over time?",
        "dimensions": [
            ("state_persistence", "State Persistence"),
            ("concurrency", "State + Concurrency"),
            ("observation", "How is State Observed?"),
        ],
        "resonance": {
            "Rust": {
                "stance": "State is explicit and tracked — the borrow checker IS the state checker",
                "summary": "Rust makes state explicit through ownership. Mutable state is borrow-checked — only one mutable reference at a time. This means state changes are always explicit and provably safe. No hidden state, no data races.",
                "key_concept": "Mutable borrows are exclusive",
                "philosophy": "If the compiler accepts your state transitions, they're memory-safe.",
                "idiom": "let mut v = vec![1, 2, 3]; v.push(4); // mutable borrow for push",
                "what_hides": "The RefCell<T> pattern for runtime-checked borrows when compile-time checking is too restrictive.",
            },
            "Go": {
                "stance": "State lives in structs — concurrency is explicit via goroutines and channels",
                "summary": "Go's approach to state is pragmatic: structs hold state, goroutines mutate it, channels communicate changes. The 'share memory by communicating' philosophy means state management is visible in the code flow.",
                "key_concept": "Communicate by sharing memory (not the other way around)",
                "philosophy": "State is just memory. If you want to change it concurrently, use channels.",
                "idiom": "ch := make(chan int); go func() { ch <- compute() }()",
                "what_hides": "Goroutine stack growth and scheduling are invisible to the programmer.",
            },
            "Swift": {
                "stance": "State and identity are intertwined — value types vs reference types define state semantics",
                "summary": "Swift separates value semantics (structs, enums — copied) from reference semantics (classes — shared). SwiftUI uses @State, @ObservedObject, @StateObject to manage state reactively. The actor model (Swift 6) makes state isolation explicit.",
                "key_concept": "@State, @Observable, actors for state isolation",
                "philosophy": "State lives somewhere specific. Know where it lives.",
                "idiom": "@State private var count = 0 // stored in the SwiftUI view's local state",
                "what_hides": "Actor isolation in Swift 6 makes state isolation explicit but adds boilerplate.",
            },
            "Kotlin": {
                "stance": "State is mutable by default — mutability control is the programmer's job",
                "summary": "Kotlin distinguishes val (immutable reference) from var (mutable reference). But val doesn't mean deep immutability — only reference immutability. Coroutines and Flow provide reactive state management. The programmer explicitly controls what can change.",
                "key_concept": "val/var + coroutines + Flow",
                "philosophy": "Mutability is a choice. Make it consciously.",
                "idiom": "val immutable = listOf(1, 2, 3) // immutable reference, but list contents could still change",
                "what_hides": "Immutability isn't deep — val just means the reference can't change.",
            },
            "TypeScript": {
                "stance": "State is just objects — there's no language-level state model",
                "summary": "TypeScript adds type safety to JavaScript objects but doesn't add a state model. State is whatever your objects hold. Libraries like React popularized useState/useReducer as a convention for state management. The language doesn't enforce any particular model.",
                "key_concept": "State = objects + conventions (not language feature)",
                "philosophy": "State is just data. You decide how to model it.",
                "idiom": "const [count, setCount] = useState(0) // React convention, not TypeScript syntax",
                "what_hides": "TypeScript doesn't prevent you from mutating state anywhere — discipline is the only constraint.",
            },
            "JavaScript": {
                "stance": "Everything mutable — objects are mutable dictionaries, arrays are mutable",
                "summary": "JavaScript has no concept of immutability built into the language. Primitives are immutable, but objects and arrays are mutable. There's no way to freeze an object deeply (Object.freeze is shallow). State changes happen invisibly unless you use patterns.",
                "key_concept": "Primitives are immutable; objects are mutable",
                "philosophy": "State is just memory that changes. Trust your conventions.",
                "idiom": "const obj = { x: 1 }; obj.x = 2; // mutating in place — no error, no copy",
                "what_hides": "There's no shared state detection. Mutations can happen anywhere.",
            },
            "Java": {
                "stance": "State is protected by encapsulation — private fields, public methods",
                "summary": "Java's state model is class-based encapsulation. Fields are private, accessed via methods. The volatile keyword and java.util.concurrent package handle concurrency state. Records (Java 16+) provide immutable state carriers.",
                "key_concept": "Encapsulation via private fields + synchronized/volatile",
                "philosophy": "State is yours. Protect it with access control.",
                "idiom": "private int count; public synchronized void increment() { count++; }",
                "what_hides": "Synchronized is coarse-grained. Java 21 virtual threads make fine-grained locking more important.",
            },
            "C/C++": {
                "stance": "State is raw memory — you own every byte and every race condition",
                "summary": "C/C++ has no built-in state management. Global variables are state. Stack variables are state. Heap allocations are state. The programmer controls all of it. This means state management bugs (use-after-free, data races) are possible — but the model is transparent.",
                "key_concept": "State = memory locations",
                "philosophy": "You own the memory. You own the bugs. You own the fix.",
                "idiom": "int global_state = 0; // explicit global state — visible in any function",
                "what_hides": "Undefined behavior means the compiler can assume state is never 'impossible' — and optimize accordingly.",
            },
        },
    },
    {
        "id": "error",
        "name": "What is an Error?",
        "emoji": "⚡",
        "question": "How does a language model failure, absence, and exceptional cases?",
        "dimensions": [
            ("error_representation", "Error Representation"),
            ("recoverability", "Recoverability"),
            ("visibility", "Error Visibility at Compile Time"),
        ],
        "resonance": {
            "Rust": {
                "stance": "Errors are values — handle them explicitly or the compiler notices",
                "summary": "Rust has no exceptions. Errors are represented as Result<T, E> types. The compiler forces you to handle errors (via ? operator or match). Option<T> handles absence. This makes errors visible at every call site — impossible to ignore.",
                "key_concept": "Result<T, E> and Option<T>",
                "philosophy": "Errors are not special cases — they're part of the return type.",
                "idiom": "let content = std::fs::read_to_string(\"file\")?; // ? propagates error, or returns Ok",
                "what_hides": "Panics (unrecoverable errors) exist but are for programmer errors, not expected failures.",
            },
            "Go": {
                "stance": "Errors are returned values — explicit error interface, no exceptions",
                "summary": "Go has no exceptions. Every function that can fail returns an error as its last return value. The idiomatic pattern is to check errors immediately and return early. This makes error flow explicit but can lead to verbose code.",
                "key_concept": "Errors as returned values (error interface)",
                "philosophy": "If a function can fail, it tells you. No hidden exceptions.",
                "idiom": "f, err := os.Open(\"file\"); if err != nil { return err } // explicit error check",
                "what_hides": "Go 2.0 is redesigning error handling to reduce the boilerplate.",
            },
            "Swift": {
                "stance": "Errors as values with try/catch — typed error protocols",
                "summary": "Swift uses error protocols (Error, CustomNSError) with try/catch. Errors can be any type conforming to Error. Optionals handle absence separately. Swift 2's error handling was heavily inspired by Rust's approach.",
                "key_concept": "throws keyword + try/catch + Error protocol",
                "philosophy": "Errors are first-class — they can be thrown, caught, and propagated.",
                "idiom": "enum FileError: Error { case notFound, permissionDenied }; func read() throws { ... }",
                "what_hides": "Typed throws (Swift 5.20+) — the error type is part of the function signature.",
            },
            "Kotlin": {
                "stance": "Exceptions are unchecked — but Kotlin adds Result and null safety",
                "summary": "Kotlin inherits Java's exception model (exceptions are unchecked) but adds null safety (Nullable types), Result<T>, and runCatching. The philosophy is: use exceptions for truly exceptional cases, use Result for expected failures.",
                "key_concept": "Null safety + Result<T> + exceptions",
                "philosophy": "NullPointerException is a thing of the past. Kotlin makes null impossible to ignore.",
                "idiom": "val name: String? = null // ? means nullable — compiler forces you to handle null",
                "what_hides": "Exceptions cross function boundaries silently — catch or declare them.",
            },
            "TypeScript": {
                "stance": "Errors are thrown and caught — no type-safe error handling",
                "summary": "TypeScript/JavaScript use throw/catch for errors. Errors can be any type. There's no type-safe way to declare what errors a function might throw. This is a known limitation — patterns like fp-ts or zod add type-safe error handling.",
                "key_concept": "throw/catch — type-erased errors",
                "philosophy": "Errors happen. Catch them if you can.",
                "idiom": "try { JSON.parse(input) } catch (e) { console.error('invalid json') }",
                "what_hides": "No compile-time error exhaustiveness checking — you can forget to catch.",
            },
            "JavaScript": {
                "stance": "Throw anything — errors are untyped until caught",
                "summary": "JavaScript's throw can throw any value — strings, numbers, objects. This makes error handling fragile. Promises added a new dimension: rejected promises are 'errors' that must be caught in .catch() or await in try/catch.",
                "key_concept": "throw + Promise rejection",
                "philosophy": "Everything is throwable. Discipline is your only safety net.",
                "idiom": "throw new Error('something went wrong') // best practice — throw Error objects",
                "what_hides": "Unhandled promise rejections silently fail in older environments.",
            },
            "Java": {
                "stance": "Checked exceptions — the compiler forces you to declare or catch",
                "summary": "Java's checked exceptions are unique: the compiler forces you to either declare throws or catch the exception. This is controversial — some consider it verbose, others consider it essential for API clarity.",
                "key_concept": "Checked vs Unchecked exceptions",
                "philosophy": "The compiler knows which functions can fail. Now you do too.",
                "idiom": "public void read() throws IOException { ... } // caller MUST handle or declare",
                "what_hides": "Checked exceptions don't play well with generics and lambdas (hence the controversy).",
            },
            "C/C++": {
                "stance": "No built-in error model — return codes, errno, or exceptions (C++)",
                "summary": "C has no exception system — errors are communicated via return codes and errno. C++ added exceptions, but many codebases avoid them for performance and correctness reasons. The programmer chooses the error model.",
                "key_concept": "Return codes + errno (C) | exceptions + error codes (C++)",
                "philosophy": "No safety net unless you build one. Performance is yours.",
                "idiom": "FILE *f = fopen(\"file\", \"r\"); if (!f) { /* check errno */ } // C style",
                "what_hides": "Exception specifications (deprecated) and noexcept (C++11) — but no compile-time enforcement.",
            },
        },
    },
    {
        "id": "concurrency",
        "name": "What is Concurrency?",
        "emoji": "🌊",
        "question": "How does a language model simultaneous computation?",
        "dimensions": [
            ("task_scheduling", "Task Scheduling"),
            ("communication", "Inter-task Communication"),
            ("safety", "Thread Safety Guarantees"),
        ],
        "resonance": {
            "Rust": {
                "stance": "Fearless concurrency — the borrow checker prevents data races",
                "summary": "Rust's type system enforces that mutable data cannot be shared across threads (Send/Sync traits). If two threads try to mutate the same data simultaneously, the compiler rejects it. Async/await provides a way to express concurrent I/O without threads.",
                "key_concept": "Send/Sync traits — compiler-proven thread safety",
                "philosophy": "If it compiles, there are no data races. The compiler is your concurrency safety net.",
                "idiom": "use std::thread; thread::spawn(move || { /* data ownership moved into thread */ })",
                "what_hides": "Async runtime (Tokio) is a library choice, not part of the language.",
            },
            "Go": {
                "stance": "Goroutines — cheap threads multiplexed onto OS threads by the runtime",
                "summary": "Go's goroutines are lightweight (2KB stack, growable) and multiplexed onto OS threads. Communication via channels follows CSP. The philosophy: 'Don't communicate by sharing memory; share memory by communicating.'",
                "key_concept": "Goroutines + Channels (CSP)",
                "philosophy": "Spawning a goroutine is so cheap, you do it without thinking.",
                "idiom": "go func() { doWork() }() // spawn a goroutine — trivial cost",
                "what_hides": "The goroutine scheduler — GOMAXPROCS, the M:N thread model.",
            },
            "Swift": {
                "stance": "Structured concurrency with async/await and actors",
                "summary": "Swift 6 introduces complete concurrency checking — the compiler verifies that data isn't accessed from multiple threads simultaneously. Actors provide isolated state. Sendable protocol marks types safe to cross actor boundaries.",
                "key_concept": "async/await + actors + Sendable",
                "philosophy": "The compiler proves your concurrent code has no data races.",
                "idiom": "actor Counter { private var count = 0; func increment() { count += 1 } } // actor isolates state",
                "what_hides": "Task trees — structured concurrency means child tasks are tied to parent lifetime.",
            },
            "Kotlin": {
                "stance": "Coroutines — structured concurrency with suspend functions",
                "summary": "Kotlin coroutines are suspend functions that can pause without blocking threads. Structured concurrency means coroutines are scoped to a CoroutineScope. Channels and Flow provide data streams. Lightweight — millions of coroutines can run on few threads.",
                "key_concept": "Coroutines + Flow + Structured Concurrency",
                "philosophy": "Coroutines are to async what goroutines are to threads — cheap and plentiful.",
                "idiom": "launch { delay(1000); println(\"done\") } // structured — tied to scope",
                "what_hides": "The dispatcher determines which thread(s) run the coroutine.",
            },
            "TypeScript": {
                "stance": "Async/await over promises — cooperative concurrency on the event loop",
                "summary": "JavaScript/TypeScript has a single-threaded event loop. Concurrency is cooperative — async functions yield to the event loop when they await. Web Workers provide true parallelism. Node.js Worker Threads add multi-threading.",
                "key_concept": "Single-threaded event loop + promises + async/await",
                "philosophy": "Concurrency without parallelism — unless you explicitly add Workers.",
                "idiom": "await Promise.all([fetchA(), fetchB()]) // concurrent requests, one thread",
                "what_hides": "The event loop — microtask queue, macrotask queue, and when each runs.",
            },
            "JavaScript": {
                "stance": "Event loop concurrency — everything is cooperative",
                "summary": "JavaScript runs on a single thread. Async operations (setTimeout, network, I/O) use the event loop. Promises queue microtasks. There's no pre-emptive multitasking. This model is simple but requires careful handling of long-running computations.",
                "key_concept": "Event loop + microtask queue + macrotask queue",
                "philosophy": "One thing at a time — but I/O never blocks.",
                "idiom": "setTimeout(() => console.log('later'), 0); console.log('now'); // 'now' first",
                "what_hides": "The full event loop order: synchronous → microtasks → macrotasks.",
            },
            "Java": {
                "stance": "Threads + synchronized — virtual threads (Java 21) make threads cheap",
                "summary": "Java has had threads since 1995. Synchronized blocks provide mutual exclusion. The java.util.concurrent package provides higher-level constructs. Java 21's Virtual Threads make threads lightweight — millions can run on few carrier threads.",
                "key_concept": "Virtual Threads (Java 21+) + synchronized + java.util.concurrent",
                "philosophy": "Threads are cheap now. Write blocking code as if threads were infinite.",
                "idiom": "try (var vt = VirtualThread.ofVirtual().start(() -> { /* ... */ })) { }",
                "what_hides": "Virtual threads are still scheduled by the OS — the carrier thread pool is hidden.",
            },
            "C/C++": {
                "stance": "Threads are your responsibility — the standard library helps, but not much",
                "summary": "C++11 added std::thread, std::async, and atomics. Data races are UB. The programmer is responsible for all synchronization. Modern C++ provides RAII-based locks (std::lock_guard), but there's no borrow-checker equivalent.",
                "key_concept": "std::thread + std::mutex + std::atomic",
                "philosophy": "You own the threads. You own the synchronization.",
                "idiom": "std::thread t([](){ doWork(); }); t.join(); // manual thread lifecycle",
                "what_hides": "Memory ordering — sequential consistency vs acquire/release are invisible unless you know them.",
            },
        },
    },
]


def load_rotation():
    """Load language rotation config."""
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data):
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_resonance(language: str, concept_frame: Dict[str, Any]) -> Dict[str, str]:
    """Get the resonance data for a language in a given concept frame."""
    return concept_frame["resonance"].get(language, {
        "stance": "No data available",
        "summary": "No resonance data for this language.",
        "key_concept": "N/A",
        "philosophy": "N/A",
        "idiom": "N/A",
        "what_hides": "N/A",
    })


def resonator(language: Optional[str] = None, seed: Optional[int] = None) -> Dict[str, Any]:
    """
    Generate a concept resonance analysis for the selected rotation language.

    Reads the rotation config, selects the current language, picks a concept
    frame (optionally deterministic via seed), then shows how every language
    in the rotation RESONATES with that concept — their philosophical stances,
    mental models, and key idioms.

    The selected language's resonance is highlighted as the "featured" one.

    Args:
        language: override the selected language (for testing)
        seed: optional seed for deterministic concept frame selection

    Returns:
        dict with resonance analysis and updated rotation state
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

    # Select concept frame (deterministic if seed provided, random otherwise)
    if seed is not None:
        frame_idx = seed % len(CONCEPT_FRAMES)
        concept_frame = CONCEPT_FRAMES[frame_idx]
    else:
        concept_frame = random.choice(CONCEPT_FRAMES)

    # Get resonances for all languages
    all_resonances = {}
    for lang in languages:
        all_resonances[lang] = get_resonance(lang, concept_frame)

    # Featured language's resonance
    featured = all_resonances[language]

    # Build dimension comparisons
    dimension_comparisons = []
    for dim_name, dim_label in concept_frame["dimensions"]:
        comparison = {"dimension": dim_label, "languages": {}}
        for lang in languages:
            res = all_resonances[lang]
            comparison["languages"][lang] = {
                "stance": res["stance"],
                "philosophy": res["philosophy"],
            }
        dimension_comparisons.append(comparison)

    # Emoji map
    emoji_map = {
        "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
        "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "C/C++": "⚙️"
    }
    lang_emoji = emoji_map.get(language, "🔧")
    concept_emoji = concept_frame["emoji"]

    # Update rotation
    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "selected_emoji": lang_emoji,
        "concept_frame": {
            "id": concept_frame["id"],
            "name": concept_frame["name"],
            "emoji": concept_emoji,
            "question": concept_frame["question"],
        },
        "featured_resonance": featured,
        "all_resonances": all_resonances,
        "dimension_comparisons": dimension_comparisons,
        "rotation": languages,
        "next_language": languages[next_idx],
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def run_tests() -> None:
    """Run tests to validate the Polyglot Resonator module."""
    tests_passed = 0
    tests_failed = 0

    def assert_eq(a, b, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a == b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — expected {b!r}, got {a!r}")

    def assert_in(a: str, b, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a in b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — '{a}' not found in {b!r}")

    def assert_true(a, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg}")

    def assert_keys(d: Dict, expected_keys: List[str], msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        missing = [k for k in expected_keys if k not in d]
        if not missing:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — missing keys: {missing}")

    print("Testing Polyglot Resonator...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_eq("Rust", config["languages"][0], "Rust is first language")
    assert_in("current_index", config, "current_index field present")

    print("  Testing resonator() output structure...")
    result = resonator()
    expected_keys = [
        "tool", "version", "selected_language", "selected_emoji",
        "concept_frame", "featured_resonance", "all_resonances",
        "dimension_comparisons", "rotation", "next_language", "timestamp"
    ]
    assert_keys(result, expected_keys, "All expected keys present")

    print("  Testing concept_frame structure...")
    cf = result["concept_frame"]
    assert_keys(cf, ["id", "name", "emoji", "question"], "concept_frame has required fields")
    assert_true(cf["emoji"] in ("🪞", "🏗️", "🧪", "⚡", "🌊"), "concept_frame emoji is valid")
    assert_true(len(cf["question"]) > 5, "concept_frame question is meaningful")

    print("  Testing featured_resonance structure...")
    fr = result["featured_resonance"]
    resonance_keys = ["stance", "summary", "key_concept", "philosophy", "idiom", "what_hides"]
    assert_keys(fr, resonance_keys, "featured_resonance has all required fields")
    assert_true(len(fr["stance"]) > 5, "featured_resonance stance is meaningful")
    assert_true(len(fr["summary"]) > 20, "featured_resonance summary is substantial")

    print("  Testing all_resonances covers all 8 languages...")
    for lang in config["languages"]:
        assert_true(lang in result["all_resonances"], f"{lang} in all_resonances")
        res = result["all_resonances"][lang]
        assert_true(len(res.get("stance", "")) > 3, f"{lang} has a stance")
        assert_true(len(res.get("summary", "")) > 10, f"{lang} has a summary")

    print("  Testing dimension_comparisons structure...")
    dims = result["dimension_comparisons"]
    assert_true(len(dims) >= 3, "at least 3 dimension comparisons")
    for dim in dims:
        assert_in("dimension", dim, "dimension has a name")
        assert_in("languages", dim, "dimension has languages dict")
        for lang in config["languages"]:
            assert_true(lang in dim["languages"], f"{lang} in dimension comparison")

    print("  Testing rotation advances after resonator()...")
    idx_before = load_rotation()["current_index"]
    lang_before = load_rotation()["languages"][idx_before]
    result = resonator()
    idx_after = load_rotation()["current_index"]
    assert_eq((idx_before + 1) % 8, idx_after, "index advanced by 1")
    assert_eq(lang_before, load_rotation()["last_language"], "last_language recorded correctly")

    print("  Testing deterministic concept frame selection by seed...")
    for lang in config["languages"]:
        r1 = resonator(language=lang, seed=42)
        r2 = resonator(language=lang, seed=42)
        assert_eq(r1["concept_frame"]["id"], r2["concept_frame"]["id"], f"seed=42 same concept for {lang}")
        assert_eq(r1["featured_resonance"]["key_concept"], r2["featured_resonance"]["key_concept"], f"seed=42 same resonance for {lang}")

    print("  Testing different seeds produce different concept frames...")
    r1 = resonator(seed=0)
    r2 = resonator(seed=3)
    assert_true(r1["concept_frame"]["id"] != r2["concept_frame"]["id"], "different seeds → different concepts")

    print("  Testing language emoji mapping...")
    emoji_map = {"Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
                 "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "C/C++": "⚙️"}
    for lang, emoji in emoji_map.items():
        result = resonator(language=lang)
        assert_eq(emoji, result["selected_emoji"], f"{lang} has correct emoji {emoji}")

    print("  Testing all 5 concept frames have complete resonance data...")
    for frame in CONCEPT_FRAMES:
        for lang in config["languages"]:
            res = frame["resonance"].get(lang)
            assert_true(res is not None, f"frame '{frame['id']}' has resonance for {lang}")
            assert_true(len(res.get("stance", "")) > 3, f"{frame['id']}/{lang} has stance")
            assert_true(len(res.get("philosophy", "")) > 3, f"{frame['id']}/{lang} has philosophy")
            assert_true(len(res.get("summary", "")) > 10, f"{frame['id']}/{lang} has summary")

    print("  Testing concept frames have required fields...")
    for frame in CONCEPT_FRAMES:
        assert_true("id" in frame, f"frame {frame['id']} has id")
        assert_true("name" in frame, f"frame {frame['id']} has name")
        assert_true("emoji" in frame, f"frame {frame['id']} has emoji")
        assert_true("question" in frame, f"frame {frame['id']} has question")
        assert_true("dimensions" in frame, f"frame {frame['id']} has dimensions")
        assert_true("resonance" in frame, f"frame {frame['id']} has resonance")
        assert_true(len(frame["dimensions"]) >= 3, f"frame {frame['id']} has >= 3 dimensions")

    print("  Testing tool name and version in response...")
    assert_eq("polyglot-resonator", result["tool"], "correct tool name")
    assert_eq("1.0.0", result["version"], "correct tool version")

    print("  Testing next_language is in the rotation list...")
    assert_true(result["next_language"] in result["rotation"], "next_language is in rotation list")
    assert_true(result["selected_language"] in result["rotation"], "selected_language is in rotation list")
    assert_true(result["next_language"] != result["selected_language"], "next != selected (rotation working)")

    print("  Testing all_resonances has resonance for each language...")
    for lang in config["languages"]:
        res = result["all_resonances"][lang]
        assert_true(isinstance(res, dict), f"{lang} resonance is a dict")
        assert_true("stance" in res, f"{lang} resonance has stance")
        assert_true("summary" in res, f"{lang} resonance has summary")

    print("  Testing each concept frame has all 8 languages...")
    for frame in CONCEPT_FRAMES:
        for lang in config["languages"]:
            assert_true(lang in frame["resonance"], f"frame {frame['id']} has {lang}")

    print("  Testing dimension_comparisons for all languages...")
    dims = result["dimension_comparisons"]
    for dim in dims:
        for lang in config["languages"]:
            lang_dim = dim["languages"][lang]
            assert_true("stance" in lang_dim, f"{lang} dimension has stance")
            assert_true("philosophy" in lang_dim, f"{lang} dimension has philosophy")

    print(f"\n{'='*55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("🎵 All Resonator tests passed! Every language resonates.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--resonate":
        result = resonator()
        print(json.dumps(result, indent=2))
    else:
        print(f"Polyglot Resonator v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_resonator --test       # Run tests")
        print("  python -m polyglot_resonator --resonate  # Generate resonance analysis")