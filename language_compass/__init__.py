#!/usr/bin/env python3
"""
🧭 Language Compass v1.0
A creative language learning path planner that generates personalized journey maps.
For each language, it charts a multi-stage learning path with milestones,
daily challenges, core concepts, and a "compass direction" to guide the learner.
"""

import json
import random
import os
from datetime import datetime, timedelta

TOOL_NAME = "language-compass"
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


# ── Language journey maps ──────────────────────────────────────────────────────
LANGUAGE_JOURNEYS = {
    "Rust": {
        "compass_direction": "North ⬆️ — The Borrow Checker",
        "total_stages": 4,
        "stages": [
            {
                "name": "Stage 1: Foundations & Ownership",
                "duration": "1 week",
                "concepts": ["Variables & mutability", "Ownership rules", "Borrowing & references", "Pattern matching"],
                "daily_challenge": "Write a program that demonstrates ownership transfer vs. borrowing",
                "project": "CLI tool with argument parsing using `clap`",
                "resources": ["rust-book.toml", "rustlings exercises", "rust-by-example.com"]
            },
            {
                "name": "Stage 2: Structs, Enums & Error Handling",
                "duration": "1 week",
                "concepts": ["Structs & methods", "Enums with data", "Result<T, E>", "Option<T>", "panic vs. abort"],
                "daily_challenge": "Build a custom error type that implements std::error::Error",
                "project": "JSON parser that handles malformed input gracefully",
                "resources": ["The Rust Book Ch. 5-9", "rust-error-handling.com"]
            },
            {
                "name": "Stage 3: Generics, Traits & Lifetimes",
                "duration": "2 weeks",
                "concepts": ["Generic functions", "Trait bounds", "Standard library traits", "Lifetime annotations"],
                "daily_challenge": "Implement Iterator for a custom collection type",
                "project": "Generic data structure library (tree, graph, or hashmap)",
                "resources": ["Rust Lang reference", "trait bounds cheat sheet"]
            },
            {
                "name": "Stage 4: Concurrency & Advanced Patterns",
                "duration": "2 weeks",
                "concepts": ["Threads & Message Passing", "Arc<Mutex<T>>", "Async with Tokio", "Unsafe Rust basics"],
                "daily_challenge": "Build a concurrent task scheduler using channels",
                "project": "HTTP server with routing, middleware, and graceful shutdown",
                "resources": ["Tokio tutorial", "Rayon for data parallelism", "codec.rs"]
            }
        ],
        "learning_tip": "Fight the borrow checker and you lose. Let it guide you and it becomes your ally."
    },
    "Go": {
        "compass_direction": "East 🌅 — Simplicity in Motion",
        "total_stages": 4,
        "stages": [
            {
                "name": "Stage 1: Basics & Philosophy",
                "duration": "1 week",
                "concepts": ["Variables & types", "Control flow", "Functions & multiple returns", "Packages & imports"],
                "daily_challenge": "Write a pure Go solution to a classic algorithm problem",
                "project": "CLI task manager with file-based storage",
                "resources": ["Go by Example", "A Tour of Go"]
            },
            {
                "name": "Stage 2: Collections, Slices & Maps",
                "duration": "1 week",
                "concepts": ["Slices internals", "Map behavior", "Range loops", "make vs new"],
                "daily_challenge": "Implement a custom sort algorithm for a slice of structs",
                "project": "Data aggregation tool that reads CSV and produces reports",
                "resources": ["Go Blog: Slices", "Effective Go"]
            },
            {
                "name": "Stage 3: Interfaces & Concurrency",
                "duration": "1 week",
                "concepts": ["Interface values", "goroutines", "channels & select", "defer & panic/recover"],
                "daily_challenge": "Build a concurrent web crawler with worker pool pattern",
                "project": "Concurrent log processor with fan-in/fan-out",
                "resources": ["Go Concurrency Patterns", "context package docs"]
            },
            {
                "name": "Stage 4: Production Go & Ecosystem",
                "duration": "2 weeks",
                "concepts": ["Testing & benchmarking", "HTTP servers & middleware", "gRPC basics", "Docker & deployment"],
                "daily_challenge": "Write a middleware chain with logging, auth, and rate-limiting",
                "project": "RESTful API with PostgreSQL, Redis caching, and graceful shutdown",
                "resources": ["Go standard library", "testify.dev", "golangci-lint"]
            }
        ],
        "learning_tip": "Go's philosophy: simple concurrency, clear errors, and code that reads like prose."
    },
    "Swift": {
        "compass_direction": "West 🌄 — Safety Meets Expressiveness",
        "total_stages": 4,
        "stages": [
            {
                "name": "Stage 1: Swift Basics & Optionals",
                "duration": "1 week",
                "concepts": ["Variables, constants & type inference", "Optionals & nil handling", "Control flow", "Functions & closures"],
                "daily_challenge": "Implement a nil-safe data pipeline using optional chaining",
                "project": "CLI tool that processes JSON configuration files",
                "resources": ["The Swift Programming Language (apple.com)", "Swift by Sundell"]
            },
            {
                "name": "Stage 2: Structs, Classes & Protocols",
                "duration": "1 week",
                "concepts": ["Value types vs. reference types", "Protocol-oriented programming", "Extensions & generics"],
                "daily_challenge": "Refactor a class hierarchy to use protocol composition",
                "project": "Data modeling layer for a notes app with Codable",
                "resources": ["WWDC videos", "objc.io on Swift"]
            },
            {
                "name": "Stage 3: Memory Management & Async",
                "duration": "1 week",
                "concepts": ["ARC & retain cycles", "weak & unowned", "async/await", "Actors"],
                "daily_challenge": "Convert a completion-handler API to async/await",
                "project": "Network layer with async/await, retry logic, and caching",
                "resources": ["Swift concurrency evolution proposals", "Swift.org/documentation"]
            },
            {
                "name": "Stage 4: Ecosystem & Production",
                "duration": "2 weeks",
                "concepts": ["SwiftUI fundamentals", "Combine & reactive patterns", "Testing with XCTest", "Swift Package Manager"],
                "daily_challenge": "Build a SwiftUI view that consumes an async stream",
                "project": "iOS/macOS app with local persistence and network sync",
                "resources": ["Apple Developer Documentation", "SwiftUI by Example"]
            }
        ],
        "learning_tip": "Swift rewards those who embrace the type system and Optionals, not fight them."
    },
    "Kotlin": {
        "compass_direction": "South 🌋 — Pragmatic Power",
        "total_stages": 4,
        "stages": [
            {
                "name": "Stage 1: Kotlin Foundations",
                "duration": "1 week",
                "concepts": ["Null safety & smart casts", "Data classes & companion objects", "Extension functions", "Lambdas & higher-order functions"],
                "daily_challenge": "Replace a Java utility class with Kotlin extension functions",
                "project": "Build a DSL for constructing HTML tables",
                "resources": ["Kotlinlang.org", "Kotlin by JetBrains"]
            },
            {
                "name": "Stage 2: Collections & Functional Style",
                "duration": "1 week",
                "concepts": ["Iterable vs. Sequence", "map/filter/reduce & chaining", "Scope functions (let/also/apply/run)", "Delegated properties"],
                "daily_challenge": "Convert a nested loop into a fluid collection pipeline",
                "project": "Data transformation pipeline using Kotlin sequences",
                "resources": ["Kotlin collections docs", "Functional programming in Kotlin (Manning)"]
            },
            {
                "name": "Stage 3: Coroutines & Concurrency",
                "duration": "2 weeks",
                "concepts": ["Suspend functions", "Flow vs. Channel", "Structured concurrency", "Coroutine dispatchers"],
                "daily_challenge": "Migrate a callback-based API to Kotlin Flow",
                "project": "Real-time data dashboard with Flow and Compose",
                "resources": ["Kotlin Coroutines guide", "kotlinx.coroutines docs"]
            },
            {
                "name": "Stage 4: Multiplatform & Production",
                "duration": "2 weeks",
                "concepts": ["Kotlin Multiplatform basics", "KMP structure", "expect/actual", "CI/CD for KMP"],
                "daily_challenge": "Share a business logic module between JVM and JS targets",
                "project": "Cross-platform mobile app skeleton with shared code",
                "resources": ["Kotlin Multiplatform documentation", "KaKit x KMP hands-on"]
            }
        ],
        "learning_tip": "Kotlin's philosophy: make common tasks easy and unusual tasks possible."
    },
    "TypeScript": {
        "compass_direction": "Northeast 📡 — Type-Safe JavaScript",
        "total_stages": 4,
        "stages": [
            {
                "name": "Stage 1: TypeScript Fundamentals",
                "duration": "1 week",
                "concepts": ["Basic types & inference", "Interfaces & type aliases", "Generics", "Utility types (Partial, Pick, Omit)"],
                "daily_challenge": "Convert a JavaScript module to fully-typed TypeScript with strict mode",
                "project": "Typed configuration manager for a CLI tool",
                "resources": ["TypeScript Handbook", "type-challenges.dev"]
            },
            {
                "name": "Stage 2: Advanced Types & Patterns",
                "duration": "1 week",
                "concepts": ["Conditional types", "Template literal types", "Discriminated unions", "Mapped types"],
                "daily_challenge": "Write a type-safe query builder using conditional types",
                "project": "Event system with strongly-typed event names and payloads",
                "resources": ["TypeScript Deep Dive (basarat.com)", "advanced-types.com"]
            },
            {
                "name": "Stage 3: Runtime & Tooling",
                "duration": "1 week",
                "concepts": ["Runtime validation (Zod/Valibot)", "Declaration merging", "Module augmentation", "tsconfig deep dive"],
                "daily_challenge": "Build a schema validator that catches type mismatches at runtime",
                "project": "Config validation pipeline with Zod and hot reload",
                "resources": ["Zod docs", "TypeScript config handbook"]
            },
            {
                "name": "Stage 4: Ecosystem & Frameworks",
                "duration": "2 weeks",
                "concepts": ["React with TypeScript", "Type-safe API clients", "Next.js / Express + TypeScript", "Testing with Vitest"],
                "daily_challenge": "Type an existing React component library from scratch",
                "project": "Full-stack app with tRPC, React Query, and PostgreSQL",
                "resources": ["Total TypeScript", "React TypeScript cheatsheet"]
            }
        ],
        "learning_tip": "TypeScript's real power is using types as documentation that never gets stale."
    },
    "JavaScript": {
        "compass_direction": "Southeast 🌴 — The Language of the Web",
        "total_stages": 4,
        "stages": [
            {
                "name": "Stage 1: JavaScript Essentials",
                "duration": "1 week",
                "concepts": ["Variables, scoping & hoisting", "Prototype chain", "Closures & higher-order functions", "Async fundamentals"],
                "daily_challenge": "Implement a memoization decorator from scratch",
                "project": "Build a task queue with retry logic and event callbacks",
                "resources": ["MDN Web Docs", "You Don't Know JS (Kyle Simpson)"]
            },
            {
                "name": "Stage 2: Modern JavaScript & ES Modules",
                "duration": "1 week",
                "concepts": ["Destructuring & spread", "Async/await patterns", "ES Modules (import/export)", "Proxy & Reflect"],
                "daily_challenge": "Write a recursive deep-freeze utility using Proxy",
                "project": "Module-based plugin architecture with dynamic loading",
                "resources": ["ES spec draft", "javascript.info"]
            },
            {
                "name": "Stage 3: Browser APIs & DOM",
                "duration": "1 week",
                "concepts": ["Event loop & microtasks", "Web APIs (fetch, intersection observer)", "Web Workers", "Service Workers"],
                "daily_challenge": "Build an off-main-thread image processor using a Worker",
                "project": "PWA with offline support, push notifications, and background sync",
                "resources": ["Google Web Dev", "MDN Service Worker guide"]
            },
            {
                "name": "Stage 4: Runtime & Tooling",
                "duration": "2 weeks",
                "concepts": ["Node.js internals & streams", "Package management (pnpm/npm)", "Bundlers (Vite/esbuild)", "Performance profiling"],
                "daily_challenge": "Profile a Node.js app and eliminate a memory leak",
                "project": "High-performance HTTP proxy with streaming and caching",
                "resources": ["Node.js docs", "Node.js Performance (RisingStack)"]
            }
        ],
        "learning_tip": "JavaScript rewards understanding the event loop and closures — they unlock everything else."
    },
    "Java": {
        "compass_direction": "Northwest 🏔️ — Enterprise Strength",
        "total_stages": 4,
        "stages": [
            {
                "name": "Stage 1: Java Foundations",
                "duration": "1 week",
                "concepts": ["Object-oriented principles", "Inheritance & polymorphism", "Interfaces & abstract classes", "Generics"],
                "daily_challenge": "Model a real-world domain with interfaces and implementations",
                "project": "In-memory event sourcing system with a command-query API",
                "resources": ["Oracle Java Tutorials", "Effective Java (Joshua Bloch)"]
            },
            {
                "name": "Stage 2: Collections & Streams",
                "duration": "1 week",
                "concepts": ["List/Set/Map hierarchies", "Stream API & lazy evaluation", "Method references & lambda syntax", "Optional<T> idioms"],
                "daily_challenge": "Process a large dataset using parallel streams efficiently",
                "project": "Streaming data processor using Java Streams and Collector",
                "resources": ["Java Stream JEP", "Baeldung streams guide"]
            },
            {
                "name": "Stage 3: Concurrency & Virtual Threads",
                "duration": "2 weeks",
                "concepts": ["Thread pool sizing", "java.util.concurrent tools", "Virtual threads (Java 21+)", "Memory model & happens-before"],
                "daily_challenge": "Migrate a blocking I/O service to virtual threads",
                "project": "Chat server handling 10K concurrent connections with virtual threads",
                "resources": ["JEP 444 (Virtual Threads)", "Doug Lea's concurrency utils"]
            },
            {
                "name": "Stage 4: JVM Ecosystem & Production",
                "duration": "2 weeks",
                "concepts": ["JVM tuning & GC algorithms", "Records, sealed classes, patterns", "Microservices with Spring Boot", "GraalVM native images"],
                "daily_challenge": "Benchmark a Java app with different GC collectors",
                "project": "Microservice with Spring Boot, rate limiting, and observability",
                "resources": ["JVM options reference", "Spring documentation", "GraalVM guide"]
            }
        ],
        "learning_tip": "Java's platform depth is unmatched: master the JVM and performance follows."
    },
    "C/C++": {
        "compass_direction": "Southwest ⚙️ — Low-Level Mastery",
        "total_stages": 4,
        "stages": [
            {
                "name": "Stage 1: C Fundamentals",
                "duration": "1 week",
                "concepts": ["Pointers & memory layout", "Arrays & strings", "Dynamic allocation (malloc/calloc/free)", "Bitwise operations"],
                "daily_challenge": "Implement a custom string library from scratch",
                "project": "Terminal-based text editor with undo/redo",
                "resources": ["K&R The C Programming Language", "c-faq.com"]
            },
            {
                "name": "Stage 2: C++ Core & RAII",
                "duration": "2 weeks",
                "concepts": ["Classes & RAII", "Smart pointers (unique_ptr, shared_ptr, weak_ptr)", "Move semantics", "Templates & SFINAE"],
                "daily_challenge": "Replace all raw pointers in a codebase with smart pointers",
                "project": "Thread-safe memory pool allocator",
                "resources": ["cppreference.com", "C++ Core Guidelines", "Effective C++ (Scott Meyers)"]
            },
            {
                "name": "Stage 3: Modern C++ (C++17/20/23)",
                "duration": "2 weeks",
                "concepts": ["C++20 Concepts & Ranges", "Modules (C++20)", "Coroutines (C++23)", "constexpr everything"],
                "daily_challenge": "Rewrite a runtime computation as a constexpr function",
                "project": "Compile-time JSON parser using constexpr + reflection",
                "resources": ["C++委员会提案", "C++Con talks on YouTube", "foon conington"]
            },
            {
                "name": "Stage 4: Systems Programming",
                "duration": "2 weeks",
                "concepts": ["Linux system calls (epoll, io_uring)", "Multithreading with atomics", "Address Sanitizer & Memory Sanitizer", "SIMD intrinsics"],
                "daily_challenge": "Profile a program with perf and eliminate a cache miss",
                "project": "High-performance event loop library modeled after libuv",
                "resources": ["Linux kernel internals (rott)', 'Systems Performance (Brendan Gregg)"]
            }
        ],
        "learning_tip": "In C/C++, the abstractions are thin — understand what runs under the hood and you'll never be surprised."
    },
}


def build_journey_map(language):
    """Build a structured journey map for the language."""
    journey = LANGUAGE_JOURNEYS.get(language)
    if not journey:
        return None
    
    # Select a random starting stage (focus point) for variety
    stage_idx = random.randint(0, journey["total_stages"] - 1)
    focused_stage = journey["stages"][stage_idx]
    
    # Build milestone roadmap
    milestones = []
    for i, stage in enumerate(journey["stages"]):
        milestone = {
            "stage": i + 1,
            "name": stage["name"],
            "duration": stage["duration"],
            "core_concepts": stage["concepts"],
            "highlight": stage["name"] == focused_stage["name"]
        }
        milestones.append(milestone)
    
    return {
        "compass_direction": journey["compass_direction"],
        "focused_stage": focused_stage,
        "total_duration": f"{journey['total_stages']} weeks",
        "milestones": milestones,
        "learning_tip": journey["learning_tip"]
    }


def calculate_readiness_score(language):
    """Estimate readiness score (0-100) based on day-of-year randomness."""
    random.seed(hash(language + str(datetime.now().timetuple().tm_yday)))
    score = random.randint(60, 100)
    
    # Boost based on difficulty perception
    difficulty_map = {"Rust": 5, "C/C++": 8, "Kotlin": 3, "Go": 2, "Swift": 4, 
                      "TypeScript": 3, "JavaScript": 2, "Java": 4}
    difficulty = difficulty_map.get(language, 5)
    score = min(100, score + (10 - difficulty * 2))
    
    return score


def navigate(language):
    """
    Main navigate function — chart a learning path for the selected language.
    Loads rotation config, validates language, generates journey, and advances rotation.
    """
    config = load_rotation()

    if language not in config["languages"]:
        raise ValueError(
            f"Language '{language}' not in rotation. "
            f"Available: {', '.join(config['languages'])}"
        )

    journey_map = build_journey_map(language)
    readiness = calculate_readiness_score(language)
    
    # Calculate dates
    today = datetime.now().date()
    total_weeks = 6  # 4 stages + buffer
    next_session = today + timedelta(days=7)
    
    # Build the compass response
    current_idx = config["languages"].index(language)
    next_idx = (current_idx + 1) % len(config["languages"])
    
    # Advance rotation
    config["current_index"] = next_idx
    config["last_language"] = language
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "compass_direction": journey_map["compass_direction"],
        "readiness_score": readiness,
        "focused_stage": journey_map["focused_stage"],
        "milestones": journey_map["milestones"],
        "total_journey_duration": journey_map["total_duration"],
        "next_session_date": next_session.isoformat(),
        "learning_tip": journey_map["learning_tip"],
        "next_language": config["languages"][next_idx],
        "rotation": config["languages"],
        "timestamp": datetime.now().isoformat(),
    }


def run_tests():
    """Run tests to validate the Language Compass module."""
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
            print(f"  ❌ FAIL: {msg} — '{a}' not in '{b}'")

    print("Testing Language Compass...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    # current_index may not be 0 due to prior runs; just verify it's valid
    assert_eq(True, 0 <= config["current_index"] < 8, "current_index is in valid range")
    assert_eq("Rust", config["languages"][0], "Rust is first language")

    print("  Testing navigate for Rust...")
    result = navigate("Rust")
    expected_keys = [
        "tool", "version", "selected_language", "compass_direction",
        "readiness_score", "focused_stage", "milestones",
        "total_journey_duration", "next_session_date", "learning_tip",
        "next_language", "rotation", "timestamp"
    ]
    for key in expected_keys:
        assert_eq(True, key in result, f"Key '{key}' present in response")

    assert_eq(True, "North" in result["compass_direction"] or "⬆️" in result["compass_direction"],
             "Rust compass direction set")
    assert_eq(True, 60 <= result["readiness_score"] <= 100, "Readiness score in valid range [60-100]")
    assert_eq(True, len(result["milestones"]) == 4, "Rust has 4 milestone stages")
    assert_eq(True, result["focused_stage"] is not None, "Focused stage is set")
    assert_in("learning_tip", result.keys(), "Learning tip included")

    print("  Verifying rotation update...")
    config2 = load_rotation()
    assert_eq(1, config2["current_index"], "Index advanced to 1 (Go)")
    assert_eq("Rust", config2["last_language"], "Last language recorded as Rust")

    print("  Testing navigate for Go (next in rotation)...")
    result2 = navigate("Go")
    assert_eq("Go", result2["selected_language"], "Go is selected")
    assert_eq("Swift", result2["next_language"], "Next language is Swift")
    assert_eq(True, len(result2["milestones"]) == 4, "Go has 4 milestone stages")

    print("  Verifying Go compass direction...")
    assert_in("East", result2["compass_direction"], "Go compass direction is East")

    print("  Testing all languages have journeys...")
    for lang in config["languages"]:
        jdata = LANGUAGE_JOURNEYS.get(lang)
        assert_eq(True, jdata is not None, f"Journey exists for {lang}")
        assert_eq(True, jdata["total_stages"] >= 4, f"{lang} has at least 4 stages")
        assert_eq(True, len(jdata["stages"]) >= 4, f"{lang} has at least 4 stage entries")
        assert_eq(True, all(k in jdata for k in ["compass_direction", "stages", "learning_tip"]),
                 f"{lang} has all required journey fields")
        # Each stage should have required sub-fields
        for stage in jdata["stages"]:
            assert_eq(True, all(k in stage for k in ["name", "duration", "concepts", "daily_challenge", "project"]),
                     f"{lang} stage '{stage['name']}' has all fields")

    print("  Testing invalid language handling...")
    try:
        navigate("Python")
        tests_failed += 1
        print("  ❌ FAIL: No error raised for invalid language")
    except ValueError as e:
        tests_passed += 1
        print(f"  ✅ PASS: ValueError raised for invalid language")
        assert_in("not in rotation", str(e), "Error mentions rotation")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ FAIL: Wrong exception: {e}")

    print("  Testing journey structure integrity...")
    result3 = navigate("Kotlin")
    for milestone in result3["milestones"]:
        assert_eq(True, "stage" in milestone, "Milestone has 'stage' number")
        assert_eq(True, "name" in milestone, "Milestone has 'name'")
        assert_eq(True, "duration" in milestone, "Milestone has 'duration'")
        assert_eq(True, "core_concepts" in milestone, "Milestone has 'core_concepts'")
        assert_eq(True, "highlight" in milestone, "Milestone has 'highlight' boolean")
    # Exactly one milestone should be highlighted
    highlighted = [m for m in result3["milestones"] if m["highlight"]]
    assert_eq(1, len(highlighted), "Exactly one milestone is highlighted")

    print("  Testing next_language cycle correctness...")
    config = load_rotation()
    next_idx = config["current_index"]
    assert_eq(True, 0 <= next_idx < 8, "current_index is valid after all navigations")

    print(f"\n{'='*55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("🎉 All tests passed! The compass always points true.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--navigate":
        language = sys.argv[2] if len(sys.argv) > 2 else "Rust"
        result = navigate(language)
        print(json.dumps(result, indent=2))
    else:
        print(f"Language Compass v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m language_compass --test      # Run tests")
        print("  python -m language_compass --navigate [lang]  # Navigate a language journey")