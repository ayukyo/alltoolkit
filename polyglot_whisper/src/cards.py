"""Insight card content for each language in the rotation."""

INSIGHT_CARDS = {
    "Rust": {
        "idiom": "\"The borrow checker is your strictest—and most honest—code reviewer.\"",
        "proverb": "A little learning is a dangerous thing (but zero-cost abstractions are safe).",
        "quirk": "Rust's type system prevents data races at compile time. No other mainstream language can claim this.",
        "fun_fact": "Rust has been voted 'most loved programming language' in the Stack Overflow Developer Survey every year since 2016.",
        "syntax_gem": "The `?` operator propagates errors with zero runtime overhead.",
        "philosophy": "Memory safety without garbage collection — through ownership, borrowing, and lifetimes.",
    },
    "Go": {
        "idiom": "\"Goroutines are cheap. Don't be afraid to use them.\"",
        "proverb": "Don't communicate by sharing memory; share memory by communicating.",
        "quirk": "Go has no `try`/`catch` exceptions — errors are plain values returned as `error` type.",
        "fun_fact": "The Go mascot is a cute gopher designed by Renée French. She's also behind the Go t的设计.",
        "syntax_gem": "The `defer` statement runs cleanup logic even when a function panics.",
        "philosophy": "Simplicity, concurrency, and composition over inheritance.",
    },
    "Swift": {
        "idiom": "\"Swift treats `nil` as a first-class concept — if a value can be absent, the compiler forces you to handle it.\"",
        "proverb": "Protocols over inheritance; composition over hierarchy.",
        "quirk": "Swift's `guard` statement dramatically reduces pyramid-of-doom nesting.",
        "fun_fact": "Swift was open-sourced in 2015 and runs on Linux. It was designed to fix Cocoa ( Objective-C) without sacrificing performance.",
        "syntax_gem": "Trailing closures: `arr.map { $0 * 2 }` — the most readable syntax in the Apple ecosystem.",
        "philosophy": "Safety, speed, and expressiveness — in that order.",
    },
    "Kotlin": {
        "idiom": "\"Kotlin's null safety makes entire categories of runtime exceptions compile-time errors.\"",
        "proverb": "Data classes reduce boilerplate; extension functions add behaviour without inheritance.",
        "quirk": "Kotlin compiles to JVM bytecode AND to JavaScript AND to native binaries.",
        "fun_fact": "JetBrains developed Kotlin specifically because they were frustrated with Java's verbosity in IntelliJ IDEA.",
        "syntax_gem": "The `when` expression replaces entire switch statements with elegant pattern matching.",
        "philosophy": "Pragmatic: take the best ideas from Java, Scala, C#, and Groovy — leave out the noise.",
    },
    "TypeScript": {
        "idiom": "\"If it compiles, it probably works. TypeScript has your back.\"",
        "proverb": "Explicit types are documentation that never goes stale.",
        "quirk": "TypeScript is a superset of JavaScript — every valid JS program is valid TypeScript.",
        "fun_fact": "TypeScript was created at Microsoft in 2012, partly because the Outlook Web App team needed scale and safety.",
        "syntax_gem": "Conditional types (`T extends U ? X : Y`) enable types that reason about other types.",
        "philosophy": "Scalable JavaScript — add types for tooling and safety without losing the ecosystem.",
    },
    "JavaScript": {
        "idiom": "\"JavaScript is the only language that runs in a browser, on a server, in a database, on microcontrollers, and everywhere else.\"",
        "proverb": "`undefined` is not `null`. Never assume. Always check.",
        "quirk": "JavaScript has only one number type (IEEE 754 double-precision float). There is no integer type.",
        "fun_fact": "Brendan Eich created JavaScript in 10 days in 1995 — originally named Mocha, then LiveScript.",
        "syntax_gem": "Destructuring: `const { name, age } = user;` — extract values from objects in one line.",
        "philosophy": "Prototypal inheritance, first-class functions, and an event loop — a surprisingly elegant minimal core.",
    },
    "Java": {
        "idiom": "\"Write once, run anywhere — the JVM made that slogan real.\"",
        "proverb": "Favour composition over inheritance. Inheritance is a contract you may not want to keep.",
        "quirk": "Java has no unsigned integer types until JDK 8 (which added unsigned `int` and `long` support via wrapper methods).",
        "fun_fact": "Java was originally called Oak, after the oak tree outside James Gosling's office at Sun Microsystems.",
        "syntax_gem": "The diamond operator `<>` reduces generics verbosity: `List<String> list = new ArrayList<>();`",
        "philosophy": "Strong typing, class-based OOP, and a massive standard library — enterprise software's bedrock.",
    },
    "C/C++": {
        "idiom": "\"In C, if something is undefined, anything can happen — including everything you didn't want.\"",
        "proverb": "C gives you enough rope to hang yourself. C++ gives you enough rope to build a whole circus.",
        "quirk": "C++ can be so low-level you manage memory manually, and so high-level you write generic meta-programming at compile time.",
        "fun_fact": "C was created by Dennis Ritchie in 1972 at Bell Labs — the same place that invented Unix, C's natural habitat.",
        "syntax_gem": "C++ template specialisation lets you write compile-time computed factorials with zero runtime cost.",
        "philosophy": "You pay only for what you use. No runtime overhead. Full control. Full responsibility.",
    },
}


def get_card(language: str) -> dict:
    """Return the insight card for a given language."""
    card = INSIGHT_CARDS.get(language)
    if card is None:
        raise ValueError(f"No insight card available for language: {language}")
    return card


def get_all_languages() -> list:
    """Return the list of languages with insight cards."""
    return list(INSIGHT_CARDS.keys())