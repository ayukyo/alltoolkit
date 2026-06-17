#! /usr/bin/env python3
"""
Anomaly Detector — Core Implementation v1.0
"""

import json
import os
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-anomaly"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = str(Path(__file__).parent.parent.parent / "language_rotation.json")

ROTATION_ORDER = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

ANOMALY_DATA = {
    "Rust": {
        "emoji": "🦀",
        "anomalies": [
            {"id": "rust-001", "name": "Recursive Mutable Borrows Are Forbidden",
             "severity": "high", "description": "Cannot have a data structure with a mutable reference to itself.",
             "paradox": "Safety enforcement creates constraints safe code cannot express.",
             "workaround": "Use Rc<RefCell<T>> or Box<T> for recursive types.",
             "example_code": "struct Node { child: &mut Node } // ERROR"},
            {"id": "rust-002", "name": "Slices Cannot Extend Past Source",
             "severity": "medium", "description": "A slice is a view into existing memory.",
             "paradox": "The borrow checker prevents out-of-bounds but a slice can point past data.",
             "workaround": "Use .get() or .get_mut() which return Option<&T>.",
             "example_code": "let arr = [1,2,3]; let s = &arr[0..5]; // compile error"},
            {"id": "rust-003", "name": "Closures Capture by Borrow or Move — Not Reference",
             "severity": "medium", "description": "Closures capture by value or immutable borrow by default.",
             "paradox": "Closures capturing mutably cannot be called multiple times cleanly.",
             "workaround": "Use move || { ... } to take ownership of captured variables.",
             "example_code": "let mut c = || { x += 1; }; c(); c(); // x must be mut"},
            {"id": "rust-004", "name": "Deref Coercion Only Works in Method Resolution",
             "severity": "low", "description": "Deref coercion works for methods but not for regular assignments.",
             "paradox": "Same value behaves differently in method call vs direct use.",
             "workaround": "Explicitly call .deref() or use &*.",
             "example_code": "let x: &str = &String::new(); // ERROR but works via method"},
            {"id": "rust-005", "name": "PhantomData Marks Unowned Memory",
             "severity": "medium", "description": "PhantomData<T> is a zero-sized marker for borrowed data.",
             "paradox": "A zero-sized marker type is essential for soundness.",
             "workaround": "Always use PhantomData when a type holds borrowed data.",
             "example_code": "struct Slice<T> { ptr: *const T, len: usize, _p: PhantomData<T> }"},
        ],
        "paradoxes": [
            {"quote": "The fastest Rust code is often the safest Rust code.",
             "explanation": "Zero-cost abstractions mean safest abstractions compile to optimal code."},
            {"quote": "You need unsafe to write safe abstractions.",
             "explanation": "All safe abstractions (Box, Vec, Arc) are built on unsafe."},
            {"quote": "The borrow checker prevents bugs, but learning it prevents programmers.",
             "explanation": "The borrow checker eliminates bug classes but has a steep learning curve."},
        ],
        "delightful_contradictions": [
            "You can write 'slow' safe code that compiles to fast machine code.",
            "The more restrictive the type system, the more expressive the programs.",
            "Compile-time checking eliminates runtime errors but adds compile time.",
        ],
    },
    "Go": {
        "emoji": "🐹",
        "anomalies": [
            {"id": "go-001", "name": "nil Interface Is Not nil",
             "severity": "critical", "description": "An interface is nil only when both type and value are nil.",
             "paradox": "A nil pointer stored in an interface is NOT nil.",
             "workaround": "Return (*T)(nil) explicitly, or use a pointer receiver.",
             "example_code": "var e error = (*T)(nil); fmt.Println(e == nil) // false"},
            {"id": "go-002", "name": "Append May Reallocate and Invalidates Old Slices",
             "severity": "high", "description": "append() may allocate new storage, returning a new slice.",
             "paradox": "The append seems to modify in place but gives you a new slice.",
             "workaround": "Always capture the return value: s = append(s, x).",
             "example_code": "s := make([]int,0,1); s = append(s,1); s2 := append(s,2); // s unchanged"},
            {"id": "go-003", "name": "Goroutines Are Stopped by the GC — Not Blocked",
             "severity": "medium", "description": "Blocked goroutines are parked, but GC stops the world.",
             "paradox": "Concurrency is fearless but GC can pause everything.",
             "workaround": "Use GOGC environment variable or runtime.GC() hints.",
             "example_code": "// goroutine blocked on channel: still takes memory, not CPU"},
            {"id": "go-004", "name": "Map Is Not Goroutine-Safe — But Doesn't Panic",
             "severity": "critical", "description": "Concurrent map access causes fatal crash (Go 1.21+).",
             "paradox": "Maps are the most common data structure yet single-threaded by default.",
             "workaround": "Use sync.Map or mutex-protected map, or channels.",
             "example_code": "m := make(map[int]int); go func() { m[1] = 2 }(); m[2] = 3 // race"},
            {"id": "go-005", "name": "len(nil_slice) == 0 But append to nil Allocates",
             "severity": "low", "description": "nil slice acts empty, but append(nil, x) allocates.",
             "paradox": "nil is empty except when you append to it.",
             "workaround": "Prefer var s []int (nil) over s := []int{} (empty non-nil).",
             "example_code": "var s []int; fmt.Println(len(s)) // 0; s = append(s, 1) // allocates"},
        ],
        "paradoxes": [
            {"quote": "Goroutines are cheap — but they still have memory overhead.",
             "explanation": "A goroutine starts at ~2KB, so millions are possible but use GBs."},
            {"quote": "Go's simplicity comes from complexity hidden in the runtime.",
             "explanation": "The runtime includes scheduler, GC, and memory allocator."},
            {"quote": "Interfaces are implicit but essential.",
             "explanation": "Go uses structural typing via interfaces without 'implements' keyword."},
        ],
        "delightful_contradictions": [
            "The language with no exceptions still has a panic/recover mechanism.",
            "You write concurrent code serially and it's correct.",
            "Go's nil is not nil (interface nils).",
        ],
    },
    "Swift": {
        "emoji": "🦅",
        "anomalies": [
            {"id": "swift-001", "name": "String Is a Value Type That Copies",
             "severity": "high", "description": "Swift String is a struct but uses copy-on-write.",
             "paradox": "Value types promise efficiency but String COW adds complexity.",
             "workaround": "Use String.SubSequence for views, or NSString for reference semantics.",
             "example_code": "var s = \"hello\"; var s2 = s; s2 += \" world\" // s unchanged"},
            {"id": "swift-002", "name": "Self Is Immutable in Value Types Unless Mutating",
             "severity": "medium", "description": "Struct methods must be marked mutating to modify self.",
             "paradox": "You need permission to modify your own state in your own methods.",
             "workaround": "Mark mutating methods explicitly, or use classes for mutation.",
             "example_code": "mutating func update() { self.value = 10 }"},
            {"id": "swift-003", "name": "Any and AnyObject Are Hole Types",
             "severity": "medium", "description": "Any accepts anything; AnyObject accepts any class instance.",
             "paradox": "Type system erases itself at the Any boundary.",
             "workaround": "Use existentials with constraints: any Sequence<Int>.",
             "example_code": "var x: Any = 1; print(x + 1) // ERROR — Any doesn't have +"},
            {"id": "swift-004", "name": "Optionals Are Enums — But Have Special Syntax",
             "severity": "low", "description": "Optional<T> is an enum but uses special ? syntax.",
             "paradox": "The most distinctive Swift feature is just an enum with compiler support.",
             "workaround": "Use .none and .some() to use it as a plain enum.",
             "example_code": "let x: Int? = nil; if case .some(let v) = x { }"},
            {"id": "swift-005", "name": "Actors Serialize Access But Are Not Explicit",
             "severity": "high", "description": "Swift actors ensure only one task accesses state at a time.",
             "paradox": "The most powerful concurrency primitive is enforced invisibly.",
             "workaround": "Use async/await, @MainActor for UI, and Sendable types.",
             "example_code": "actor Counter { var count = 0; func inc() { count += 1 } } // safe"},
        ],
        "paradoxes": [
            {"quote": "Value types prevent aliasing bugs, but copying them is not free.",
             "explanation": "COW means sharing until mutation — efficient but subtle."},
            {"quote": "Optionals eliminate nil checks — but introduce a new kind of check.",
             "explanation": "Forced unwrap (!) crashes instead of returning nil."},
            {"quote": "Protocols are duck-typed but checked statically.",
             "explanation": "Swift protocols use structural compatibility checked at compile time."},
        ],
        "delightful_contradictions": [
            "UnsafeSwift lets you bypass safety — inside the safety zone.",
            "A struct with mutating methods is more restrictive but feels modern.",
            "Protocol-oriented programming is OO without inheritance.",
        ],
    },
    "Kotlin": {
        "emoji": "🤖",
        "anomalies": [
            {"id": "kotlin-001", "name": "Extension Functions Don't Actually Extend the Class",
             "severity": "medium", "description": "Extension functions compile to static methods.",
             "paradox": "You can add methods to Any but only Java's methods are visible.",
             "workaround": "Use composition or wrapper types for internals.",
             "example_code": "fun String.addExclamation() = this + \"!\" // compiles to addExclamation(String)"},
            {"id": "kotlin-002", "name": "Nullable Types Are Unboxed — Causing NullPointerException",
             "severity": "high", "description": "Platform types (T!) from Java interop can be null.",
             "paradox": "Kotlin's null safety disappears at the Java boundary.",
             "workaround": "Use @Nullable/@NotNull annotations on Java code.",
             "example_code": "val list: List<String> = javaMethodReturningNull() // platform type"},
            {"id": "kotlin-003", "name": "Coroutines Can Leak Memory If Scope Is Wrong",
             "severity": "high", "description": "Coroutines bound to unterminated scopes leak.",
             "paradox": "Async code that looks structured can still leak.",
             "workaround": "Use structured concurrency: viewModelScope, lifecycleScope.",
             "example_code": "GlobalScope.launch { while(true) { } } // never stops"},
            {"id": "kotlin-004", "name": "Companion Object Members Accessed as Static — But Aren't",
             "severity": "low", "description": "Companion object members seem static from Kotlin but are instance from Java.",
             "paradox": "Companion members behave as static from Kotlin but instance from Java.",
             "workaround": "Use @JvmStatic annotation for true static generation.",
             "example_code": "class Foo { companion object { val x = 1 } }; val y = Foo.x // static-like"},
            {"id": "kotlin-005", "name": "reified Generics Work Via Inline Specialization",
             "severity": "medium", "description": "reified lets T::class.java inside generic functions via inlining.",
             "paradox": "Type info is available at runtime because inlining makes it available before erasure.",
             "workaround": "Only use reified with inline functions.",
             "example_code": "inline fun <reified T> foo() = T::class.java"},
        ],
        "paradoxes": [
            {"quote": "Kotlin eliminates NullPointerException — except at the Java boundary.",
             "explanation": "Platform types (T!) reintroduce null unsafety for Java interop."},
            {"quote": "Coroutines are lightweight threads — but not threads.",
             "explanation": "Kotlin coroutines are continuations; thousands can run on few OS threads."},
            {"quote": "Data classes generate equals/hashCode/toString — but you can't control them.",
             "explanation": "Auto-generated equality based on constructor params; can't customize partially."},
        ],
        "delightful_contradictions": [
            "Smart casts work until they don't (when a local var is captured by a lambda).",
            "Singleton via object declaration is simpler than in Java but still uses a class.",
            "Sealed classes give exhaustive when expressions but exhaustive isn't enforced in inheritance.",
        ],
    },
    "TypeScript": {
        "emoji": "📘",
        "anomalies": [
            {"id": "ts-001", "name": "typeof null Returns 'object'",
             "severity": "medium", "description": "Historical bug from JavaScript's early implementation.",
             "paradox": "The value most clearly meaning 'no object' is typed as 'object'.",
             "workaround": "Use === null or == null for null checks.",
             "example_code": "typeof null === 'object' // true — famous JS bug"},
            {"id": "ts-002", "name": "Structural Typing Is Opposite of Nominal",
             "severity": "medium", "description": "TypeScript uses structural typing — same shape means compatible.",
             "paradox": "Types that seem different can be silently interchangeable.",
             "workaround": "Use branded/nominal types or excess property checks for object literals.",
             "example_code": "interface W { x: number }; interface Z { x: number }; let w: W = { x: 1 } as Z"},
            {"id": "ts-003", "name": "any Opts Out of Type Checking Entirely",
             "severity": "high", "description": "any disables all type checking — the compiler pretends any operation is valid.",
             "paradox": "The type system includes a way to turn itself off.",
             "workaround": "Use unknown instead of any — it forces type narrowing before use.",
             "example_code": "const x: any = 'hello'; console.log(x + 1) // 'hello1' — no error"},
            {"id": "ts-004", "name": "NaN Is Not Equal to Itself",
             "severity": "medium", "description": "NaN === NaN is false per IEEE 754.",
             "paradox": "The only value not equal to itself is also a number.",
             "workaround": "Use Number.isNaN(x) or x !== x (true only for NaN).",
             "example_code": "NaN === NaN // false; Object.is(NaN, NaN) // true"},
            {"id": "ts-005", "name": "async Functions Always Return Promises",
             "severity": "low", "description": "async functions always return Promise — even when you don't.",
             "paradox": "Function signature says T but returns Promise<T>.",
             "workaround": "Remember the async keyword changes the return type.",
             "example_code": "async function f() { return 5; } // returns Promise<number>"},
        ],
        "paradoxes": [
            {"quote": "TypeScript is statically typed — but JavaScript is not.",
             "explanation": "TypeScript adds compile-time types, but compiled output is JavaScript."},
            {"quote": "Type assertions lie to the compiler — and it believes you.",
             "explanation": "as Type tells TS 'trust me' — wrong assertions cause runtime errors."},
            {"quote": "More type annotations can mean less type safety.",
             "explanation": "Explicit any opts out entirely; implicit any generates an error."},
        ],
        "delightful_contradictions": [
            "0.1 + 0.2 !== 0.3 — floating point exact in math, approximate in JS.",
            "['1','2','3'].map(parseInt) returns [1, NaN, NaN] — map passes index as radix.",
            "A function with no return type annotated as void might still return a value.",
        ],
    },
    "JavaScript": {
        "emoji": "🟨",
        "anomalies": [
            {"id": "js-001", "name": "typeof null Is 'object' — Historical Bug",
             "severity": "medium", "description": "null was represented as 0x0, same as object type tag.",
             "paradox": "The value meaning 'no object' is typed as an object.",
             "workaround": "Use === null for null checks. Never use typeof for null.",
             "example_code": "typeof null === 'object' // true — still not fixed"},
            {"id": "js-002", "name": "this Is Determined by Call Site — Not Definition",
             "severity": "critical", "description": "'this' is dynamically scoped — determined by how a function is called.",
             "paradox": "A function's behavior depends on who calls it, not what it is.",
             "workaround": "Use arrow functions for callbacks, .bind(this), or const self = this.",
             "example_code": "const obj = { fn() { setTimeout(function() { this.x }) } } // this is global"},
            {"id": "js-003", "name": "0.1 + 0.2 !== 0.3 — Floating Point Precision",
             "severity": "medium", "description": "IEEE 754 cannot exactly represent 0.1 or 0.2.",
             "paradox": "JS is precise in integers but approximate in basic decimal arithmetic.",
             "workaround": "Use integers for money (cents), or tolerance comparisons.",
             "example_code": "0.1 + 0.2 === 0.3 // false — 0.30000000000000004"},
            {"id": "js-004", "name": "Hoisting Moves Declarations But Not Initializations",
             "severity": "medium", "description": "var declarations are hoisted but initialization stays in place.",
             "paradox": "A variable can be referenced before declaration and get undefined.",
             "workaround": "Use let/const (not hoisted the same way) or declare at top of scope.",
             "example_code": "console.log(x); var x = 1; // undefined, not ReferenceError"},
            {"id": "js-005", "name": "Array Length Is Not Count of Elements",
             "severity": "low", "description": "Array.length is highest numeric index + 1. Sparse arrays have holes.",
             "paradox": "The most basic array operation doesn't tell you actual element count.",
             "workaround": "Use filter(x => x !== undefined) or Object.keys(arr).length.",
             "example_code": "const a = [1,,3]; console.log(a.length) // 3; console.log(a[1]) // undefined"},
        ],
        "paradoxes": [
            {"quote": "JavaScript is object-oriented but had no classes until ES6.",
             "explanation": "Before ES6, JS used prototypal inheritance — objects inherit from objects."},
            {"quote": "The most powerful array method (map) does nothing by default.",
             "explanation": "map returns new array; forgetting return gives array of undefined."},
            {"quote": "== is stricter than === in a confusing way.",
             "explanation": "== performs type coercion; === prevents it, making it less surprising."},
        ],
        "delightful_contradictions": [
            "parseInt('08') returns 0 in some engines — leading 0 triggers octal guess.",
            "Set and Map use NaN as key and it works because Object.is(NaN, NaN) is true.",
            "A function can have any number of arguments regardless of parameters.",
        ],
    },
    "Java": {
        "emoji": "☕",
        "anomalies": [
            {"id": "java-001", "name": "Type Erasure Removes Generics at Runtime",
             "severity": "high", "description": "Java generics are compile-time only; erased to Object at runtime.",
             "paradox": "Type safety at compile time, zero type info at runtime.",
             "workaround": "Use reified solutions (Class<T>), type tokens, or Java 21 type parameters.",
             "example_code": "List<String> ls = new ArrayList<>(); ls.add(1); // compile error; at runtime: just List"},
            {"id": "java-002", "name": "Checked Exceptions Force Handling at Compile Time",
             "severity": "medium", "description": "Java's checked exceptions must be caught or declared.",
             "paradox": "Rigorous enforcement makes developers numb to it — empty catch blocks everywhere.",
             "workaround": "Wrap checked exceptions in RuntimeException, or use Spring exception handling.",
             "example_code": "public void read() throws IOException { } // caller MUST handle"},
            {"id": "java-003", "name": "String Pool vs new String() — Two Different Strings",
             "severity": "medium", "description": "String literals go in the pool; new String() creates heap object.",
             "paradox": "Two logically identical strings can be different objects — == compares references.",
             "workaround": "Always use .equals() for String comparison, or .intern().",
             "example_code": "String a = \"hello\"; String b = new String(\"hello\"); a == b // false"},
            {"id": "java-004", "name": "Integer Cache Is Hidden — Small Integers Are Interned",
             "severity": "low", "description": "Integer objects from -128 to 127 are cached.",
             "paradox": "Small integers are shared (== works), larger ones are not.",
             "workaround": "Use .equals() for Integer comparison, or know the cache range.",
             "example_code": "Integer a = 127; Integer b = 127; a == b // true; a = 128; b = 128; a == b // false"},
            {"id": "java-005", "name": "volatile Only Guarantees Visibility — Not Atomicity",
             "severity": "high", "description": "volatile ensures visibility but compound actions like i++ are not atomic.",
             "paradox": "volatile prevents stale reads but not check-then-act race conditions.",
             "workaround": "Use AtomicInteger, synchronized blocks, or java.util.concurrent locks.",
             "example_code": "volatile int i = 0; i++; // NOT atomic — two threads can read same i"},
        ],
        "paradoxes": [
            {"quote": "Java is 'write once, run anywhere' — but you need the JRE.",
             "explanation": "JVM promise is platform independence but requires a JVM installed."},
            {"quote": "Object is the root of everything — except primitives.",
             "explanation": "Everything except 8 primitive types (int, boolean) is an Object."},
            {"quote": "The finally Block Runs Even After a return in try.",
             "explanation": "finally is always executed; saved return value used after finally runs."},
        ],
        "delightful_contradictions": [
            "You can't extend a final class but can wrap it.",
            "Java has no unsigned bytes — byte is always signed (-128 to 127).",
            "Arrays are covariant: Integer[] extends Object[] but List<Integer> does NOT extend List<Number>.",
        ],
    },
    "C/C++": {
        "emoji": "⚙️",
        "anomalies": [
            {"id": "cpp-001", "name": "C++ Has Undefined Behavior — and Exploits It",
             "severity": "critical", "description": "200+ forms of UB; compiler assumes UB never happens.",
             "paradox": "The language's power comes from its ability to destroy itself.",
             "workaround": "Use -Wall -Wextra -Werror, static analyzers, sanitizers.",
             "example_code": "int* p; int x = *p; // UB — could print, crash, or format硬盘"},
            {"id": "cpp-002", "name": "Most Vexing Parse",
             "severity": "medium", "description": "Widget w(); is parsed as function declaration, not variable.",
             "paradox": "The most natural default-construction syntax is a function declaration.",
             "workaround": "Use Widget w{}; (brace init) or Widget w = Widget();.",
             "example_code": "Widget w(); // declares function w returning Widget — NOT a variable"},
            {"id": "cpp-003", "name": "std::vector<bool> Is Not a Container of bool",
             "severity": "high", "description": "vector<bool> uses packed bit representation — not a real container.",
             "paradox": "vector<bool> violates the Container concept it claims to implement.",
             "workaround": "Use vector<char> or deque<bool> if you need real bool references.",
             "example_code": "vector<bool> vb; vb.push_back(true); bool& r = vb[0]; // ERROR"},
            {"id": "cpp-004", "name": "Virtual Destructor in Base — Non-Virtual in Derived",
             "severity": "high", "description": "Non-virtual base destructor with polymorphic use causes UB.",
             "paradox": "Forgetting one keyword introduces memory leaks that may not manifest until production.",
             "workaround": "Always make base class destructors virtual if used polymorphically.",
             "example_code": "Base* p = new Derived; delete p; // UB — Derived destructor not called"},
            {"id": "cpp-005", "name": "const Member Functions Can Modify via mutable",
             "severity": "low", "description": "mutable members can be modified inside const member functions.",
             "paradox": "const doesn't actually mean immutable — mutable breaks this contract.",
             "workaround": "Use mutable judiciously — typically for caches or debug counters.",
             "example_code": "mutable int cache_; int get() const { cache_ = compute(); return cache_; }"},
        ],
        "paradoxes": [
            {"quote": "C++ can be faster than C when you use more abstractions.",
             "explanation": "Zero-cost abstractions (templates, inline, constexpr) compile to equally fast code."},
            {"quote": "You must understand the entire language to write correct code.",
             "explanation": "Even experts are surprised by corner cases; every feature has footguns."},
            {"quote": "The preprocessor runs before the language — and knows nothing about it.",
             "explanation": "Macro substitution is blind text substitution before parsing."},
        ],
        "delightful_contradictions": [
            "int i = i; is valid C++ and leaves i with an undefined value.",
            "sizeof('a') == sizeof(int) in C++ but not in C.",
            "A C++ template can be instantiated with 0 types and compile successfully.",
        ],
    },
}


def load_rotation():
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data):
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_current_language():
    config = load_rotation()
    languages = config.get("languages", ROTATION_ORDER)
    idx = config.get("current_index", 0)
    return languages[idx % len(languages)]


def advance_rotation():
    config = load_rotation()
    languages = config.get("languages", ROTATION_ORDER)
    idx = config.get("current_index", 0)
    lang = languages[idx % len(languages)]
    next_idx = (idx + 1) % len(languages)
    config["current_index"] = next_idx
    config["last_language"] = lang
    config["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation(config)
    return lang


def detect_anomalies(language=None):
    if language is None:
        language = advance_rotation()
    elif language not in ANOMALY_DATA:
        raise ValueError("Unknown language: {}. Available: {}".format(
            language, list(ANOMALY_DATA.keys())))

    data = ANOMALY_DATA[language]
    config = load_rotation()
    languages = config.get("languages", ROTATION_ORDER)
    current_idx = languages.index(language) if language in languages else 0
    next_idx = (current_idx + 1) % len(languages)
    next_lang = languages[next_idx] if next_idx < len(languages) else languages[0]

    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for a in data["anomalies"]:
        sev = a.get("severity", "medium")
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": language,
        "emoji": data["emoji"],
        "anomaly_count": len(data["anomalies"]),
        "severity_breakdown": severity_counts,
        "anomalies": data["anomalies"],
        "paradoxes": data["paradoxes"],
        "delightful_contradictions": data["delightful_contradictions"],
        "rotation_position": current_idx,
        "next_language": next_lang,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def format_anomaly_report(report):
    lines = [
        "",
        "=" * 56,
        "  {} {} -- Anomaly Report".format(report["emoji"], report["language"]),
        "=" * 56,
        "  Tool: {} v{}".format(report["tool"], report["version"]),
        "  Anomalies documented: {}".format(report["anomaly_count"]),
        "  Severity: CRITICAL={} HIGH={} MEDIUM={} LOW={}".format(
            report["severity_breakdown"].get("critical", 0),
            report["severity_breakdown"].get("high", 0),
            report["severity_breakdown"].get("medium", 0),
            report["severity_breakdown"].get("low", 0)),
        "  Next language: {}".format(report["next_language"]),
        "=" * 56,
    ]
    for i, anomaly in enumerate(report["anomalies"], 1):
        lines.extend([
            "",
            "[{}] {} ({})".format(i, anomaly["name"], anomaly["severity"].upper()),
            "    ID: {}".format(anomaly["id"]),
            "    {}".format(anomaly["description"]),
            "    Paradox: {}".format(anomaly["paradox"]),
            "    Workaround: {}".format(anomaly["workaround"]),
            "    Example: {}".format(anomaly["example_code"]),
        ])
    if report["paradoxes"]:
        lines.extend(["", "-" * 56, "  Paradoxes", "-" * 56])
        for p in report["paradoxes"]:
            lines.extend(["  \"{}\"".format(p["quote"]), "    -> {}".format(p["explanation"])])
    if report["delightful_contradictions"]:
        lines.extend(["", "-" * 56, "  Delightful Contradictions", "-" * 56])
        for c in report["delightful_contradictions"]:
            lines.append("  * {}".format(c))
    lines.extend(["", "=" * 56, "  -> Next: {}".format(report["next_language"]), "=" * 56, ""])
    return "\n".join(lines)


def run_tests():
    import sys

    errors = []
    passed = 0

    def t(name, cond, msg=""):
        nonlocal passed, errors
        if cond:
            passed += 1
            print("  ✅ {}".format(name))
        else:
            errors.append(name)
            print("  ❌ {}: {}".format(name, msg))

    # Save rotation
    with open(ROTATION_FILE, "r", encoding="utf-8") as _f:
        _saved_rotation = _f.read()

    print("📡 Polyglot Anomaly Detector -- Running Tests\n")

    # Test: rotation file integrity
    try:
        config = load_rotation()
        t("load_rotation() returns valid dict", isinstance(config, dict))
        t("rotation has languages list", "languages" in config)
        t("rotation has current_index", "current_index" in config)
        t("8 languages in rotation", len(config["languages"]) == 8)
        t("Rust is first language", config["languages"][0] == "Rust")
    except Exception as e:
        t("load_rotation() succeeds", False, str(e))

    # Test: all 8 languages have anomaly data
    for lang in ROTATION_ORDER:
        t("ANOMALY_DATA has '{}'".format(lang), lang in ANOMALY_DATA)
        data = ANOMALY_DATA[lang]
        t("  - {} has emoji".format(lang), "emoji" in data)
        t("  - {} has anomalies list".format(lang), isinstance(data.get("anomalies"), list))
        t("  - {} has paradoxes list".format(lang), isinstance(data.get("paradoxes"), list))
        t("  - {} has delightful_contradictions".format(lang), isinstance(data.get("delightful_contradictions"), list))

    # Test: anomaly structure
    for lang, data in ANOMALY_DATA.items():
        for anomaly in data["anomalies"]:
            t("{}/{} has required fields".format(lang, anomaly.get("id")),
              all(k in anomaly for k in ["id", "name", "severity", "description", "paradox", "workaround", "example_code"]))
            t("  - {} severity is valid".format(anomaly["id"]),
              anomaly["severity"] in ["critical", "high", "medium", "low"])

    # Test: paradox structure
    for lang, data in ANOMALY_DATA.items():
        for paradox in data["paradoxes"]:
            t("{}/paradox has required fields".format(lang),
              all(k in paradox for k in ["quote", "explanation"]))

    # Test: detect_anomalies with rotation
    try:
        with open(ROTATION_FILE, "r", encoding="utf-8") as _f:
            _rot_save = _f.read()
        cfg_before = load_rotation()
        idx_before = cfg_before["current_index"]
        lang_before = cfg_before["languages"][idx_before]
        result = detect_anomalies()
        cfg_after = load_rotation()
        idx_after = cfg_after["current_index"]
        t("detect_anomalies() advances current_index", idx_after == (idx_before + 1) % 8)
        t("detect_anomalies() returns selected language", result["language"] == lang_before)
        t("detect_anomalies() returns correct anomaly_count",
          result["anomaly_count"] == len(result["anomalies"]))
        t("detect_anomalies() returns next_language", "next_language" in result)
        t("detect_anomalies() returns severity_breakdown", "severity_breakdown" in result)
        t("detect_anomalies() returns anomalies list",
          isinstance(result.get("anomalies"), list) and len(result["anomalies"]) > 0)
        with open(ROTATION_FILE, "w", encoding="utf-8") as _f:
            _f.write(_rot_save)
    except Exception as e:
        t("detect_anomalies() works", False, str(e))

    # Test: detect_anomalies with language override
    try:
        with open(ROTATION_FILE, "r", encoding="utf-8") as _f:
            _rot_save6 = _f.read()
        _idx_before_override = json.loads(_rot_save6)["current_index"]
        result = detect_anomalies("Rust")
        t("detect_anomalies('Rust') returns Rust", result["language"] == "Rust")
        t("detect_anomalies('Rust') does not advance rotation",
          load_rotation()["current_index"] == _idx_before_override)
        with open(ROTATION_FILE, "w", encoding="utf-8") as _f:
            _f.write(_rot_save6)
    except Exception as e:
        t("detect_anomalies('Rust') override", False, str(e))

    # Test: invalid language raises ValueError
    try:
        detect_anomalies("Brainfuck")
        t("Unknown language raises ValueError", False, "did not raise")
    except ValueError:
        t("Unknown language raises ValueError", True)
    except Exception as e:
        t("Unknown language raises ValueError", False, "wrong exception: {}".format(e))

    # Test: format_anomaly_report
    try:
        with open(ROTATION_FILE, "r", encoding="utf-8") as _f:
            _rot_sav7 = _f.read()
        report = detect_anomalies("Go")
        txt = format_anomaly_report(report)
        t("format_anomaly_report() returns string", isinstance(txt, str))
        t("format_anomaly_report() contains language name", report["language"] in txt)
        t("format_anomaly_report() contains anomaly count", str(report["anomaly_count"]) in txt)
        t("format_anomaly_report() contains next_language", report["next_language"] in txt)
        with open(ROTATION_FILE, "w", encoding="utf-8") as _f:
            _f.write(_rot_sav7)
    except Exception as e:
        t("format_anomaly_report()", False, str(e))

    # Test: get_current_language
    try:
        with open(ROTATION_FILE, "r", encoding="utf-8") as _f:
            _rot_sav8 = _f.read()
        lang = get_current_language()
        t("get_current_language() returns valid language", lang in ROTATION_ORDER)
        with open(ROTATION_FILE, "w", encoding="utf-8") as _f:
            _f.write(_rot_sav8)
    except Exception as e:
        t("get_current_language()", False, str(e))

    # Test: advance_rotation
    try:
        with open(ROTATION_FILE, "r", encoding="utf-8") as _f:
            _rot_sav9 = _f.read()
        cfg_before = load_rotation()
        idx_before = cfg_before["current_index"]
        lang = advance_rotation()
        cfg_after = load_rotation()
        idx_after = cfg_after["current_index"]
        t("advance_rotation() returns current language", lang == cfg_before["languages"][idx_before])
        t("advance_rotation() advances index", idx_after == (idx_before + 1) % 8)
        t("advance_rotation() sets last_language", cfg_after.get("last_language") == lang)
        with open(ROTATION_FILE, "w", encoding="utf-8") as _f:
            _f.write(_rot_sav9)
    except Exception as e:
        t("advance_rotation()", False, str(e))

    # Test: tool name and version
    t("TOOL_NAME is polyglot-anomaly", TOOL_NAME == "polyglot-anomaly")
    t("TOOL_VERSION is 1.0.0", TOOL_VERSION == "1.0.0")

    print("\n" + "=" * 50)
    # Restore rotation
    with open(ROTATION_FILE, "w", encoding="utf-8") as _f:
        _f.write(_saved_rotation)
    if errors:
        print("❌ {} test(s) failed: {}".format(len(errors), ", ".join(errors)))
        sys.exit(1)
    else:
        print("✅ All {} tests passed!".format(passed))
        sys.exit(0)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        result = detect_anomalies()
        print(format_anomaly_report(result))
