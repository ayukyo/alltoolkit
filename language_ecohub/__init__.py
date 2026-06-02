#!/usr/bin/env python3
"""
🌿 Language EcoHub v1.0
An ecosystem explorer for programming languages — maps packages, tools, libraries,
trending projects, and best-practice tooling for each language in the rotation.

Creative concept: "Every language is an ecosystem. Explore it."

This tool is distinct from:
- language_compass (learning journey maps)
- language_mastery (XP/level progress tracking)
- language_sage (wisdom, idioms, pro tips)

EcoHub focuses on the PACKAGE ECOSYSTEM — package managers, flagship libraries,
trending projects, and tooling configuration — giving a "field guide" to each language's universe.
"""

import json
import os
import random
from datetime import datetime

TOOL_NAME = "language-ecohub"
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


# ── Ecosystem data per language ───────────────────────────────────────────────
ECO_DATA = {
    "Rust": {
        "package_manager": "Cargo (crates.io)",
        "flagship_libraries": [
            ("tokio", "Async runtime for networked services"),
            ("serde", "Serialisation/deserialisation framework"),
            ("reqwest", "Ergonomic HTTP client"),
            ("clap", "Command-line argument parser"),
            ("thiserror", "Idiomatic error handling"),
        ],
        "tooling": [
            ("rustfmt", "Code formatter (run: cargo fmt)"),
            ("clippy", "Linter with auto-fix (run: cargo clippy --fix)"),
            ("cargo-audit", "Security vulnerability scanner"),
            ("miri", "Interpreter for testing unsafe code"),
            ("criterion", "Statistics-powered microbenchmarking"),
        ],
        "trending_projects": [
            "Ripgrep — ultra-fast grep alternative",
            "ripgreptools — enhanced grep utilities",
            "Bandwhich — terminal bandwidth visualizer",
            "Bat — cat clone with syntax highlighting",
            "exa — modern ls replacement",
        ],
        "best_practice_tip": "Always run `cargo clippy --fix` before publishing. It catches entire classes of bugs.",
        "beginner_friendly": False,
        "ecosystem_quote": "Cargo: the gold standard of package management. Fetch, build, and publish in seconds.",
    },
    "Go": {
        "package_manager": "go mod (proxy.golang.org)",
        "flagship_libraries": [
            ("gin", "HTTP web framework, minimalist and fast"),
            ("gorm", "ORM for SQL databases"),
            ("cobra", "CLI framework with persistent flags"),
            ("terraform", "Infrastructure as code (HashiCorp)"),
            ("kubernetes/client-go", "Official K8s client"),
        ],
        "tooling": [
            ("gofmt", "Built-in formatter (go fmt)"),
            ("staticcheck", "Static analysis / linter"),
            ("delve", "Debugger with fancy IDE integration"),
            ("swag", "Swagger/OpenAPI doc generator"),
            ("golangci-lint", "Aggregate linter runner"),
        ],
        "trending_projects": [
            "Traefik — cloud-native edge router/proxy",
            "Prometheus — monitoring and alerting toolkit",
            "Hugo — static site generator",
            "Docker (moby) — container runtime (Go!)",
            "Syncthing — continuous file synchronization",
        ],
        "best_practice_tip": "Use `go mod tidy` before committing to keep your go.sum clean and minimal.",
        "beginner_friendly": True,
        "ecosystem_quote": "Go's philosophy: one tool do one thing well. go get, go build, go test.",
    },
    "Swift": {
        "package_manager": "Swift Package Manager (swift.org/package-manager)",
        "flagship_libraries": [
            ("SwiftUI", "Declarative UI framework"),
            ("Combine", "Reactive programming framework"),
            ("Alamofire", "HTTP networking library"),
            ("Swinject", "Dependency injection container"),
            ("SnapKit", "Auto Layout DSL"),
        ],
        "tooling": [
            ("swift-format", "Official formatter from Apple"),
            ("swiftlint", "Style and convention linter"),
            ("swiftformat", "Opinionated formatter"),
            ("XcodeGen", "YAML-based Xcode project generator"),
            ("Sourcery", "Meta-programming with Swift macros"),
        ],
        "trending_projects": [
            "SwiftNIO — async event-driven network framework",
            "Kitura — web framework from IBM",
            "Vapor — expressive web framework",
            "Perfect — server-side Swift",
            "SwiftLint — enforces style guidelines",
        ],
        "best_practice_tip": "Use @MainActor to annotate actors that must run on the main thread — Swift concurrency rewards explicit design.",
        "beginner_friendly": True,
        "ecosystem_quote": "Swift Package Manager: simple, fast, and integrated — no more CocoaPods vs SPM debates.",
    },
    "Kotlin": {
        "package_manager": "Gradle + Maven Central / Maven Publish",
        "flagship_libraries": [
            ("kotlinx.coroutines", "Async/concurrent programming"),
            ("Kotlin Serialization", "JSON/Protobuf serialization"),
            ("Koin", "Lightweight dependency injection"),
            ("Ktor", "Framework for connected applications"),
            ("Apache Commons Kotlin", "Java utilities in Kotlin"),
        ],
        "tooling": [
            ("ktlint", "Kotlin linter with auto-fix"),
            ("detekt", "Static code analysis for Kotlin"),
            ("dokka", "API documentation generator"),
            ("kotlin-gradle-plugin", "Official build tool"),
            ("Spek", "Behavior-driven testing framework"),
        ],
        "trending_projects": [
            "Kotlin Multiplatform Mobile (KMM) — Share code between iOS and Android",
            "Compose Multiplatform — UI toolkit across platforms",
            "Kotest — flexible Kotlin testing library",
            "Hex — functional programming toolkit",
            "Fritz2 — web framework in Kotlin",
        ],
        "best_practice_tip": "Use Kotlin Scripts (kts) for build scripts — you get full IDE support instead of writing blind Gradle DSL.",
        "beginner_friendly": True,
        "ecosystem_quote": "Kotlin's ecosystem is a bridge: JVM libraries on one side, multiplatform targets on the other.",
    },
    "TypeScript": {
        "package_manager": "npm / pnpm / yarn",
        "flagship_libraries": [
            ("zod", "TypeScript-first schema validation"),
            ("trpc", "End-to-end typesafe APIs"),
            ("prisma", "Next-gen ORM with TypeScript support"),
            ("react-query", "Async state management & caching"),
            ("vite", "Next-gen frontend build tool"),
        ],
        "tooling": [
            ("typescript", "Language server and compiler"),
            ("ts-node", "TypeScript execution engine for Node.js"),
            ("tsup", "Zero-config TypeScript bundler"),
            ("tsx", "TypeScript + JSX runner without config"),
            ("knip", "Detect unused files, dependencies, exports"),
        ],
        "trending_projects": [
            "Bun — all-in-one JS runtime, bundler, test runner",
            "Oxc — Rust-powered TypeScript toolchain",
            "Rolldown — Rust port of Rollup (Vite 6 core)",
            "Biome — fast formatter and linter (rust-powered)",
            "Nitro — content framework for auto-deployed apps",
        ],
        "best_practice_tip": "Enable strict: true in tsconfig.json and use unknown instead of any for maximum type safety.",
        "beginner_friendly": True,
        "ecosystem_quote": "The npm ecosystem: 2 million packages, 1 type system binding them all together.",
    },
    "JavaScript": {
        "package_manager": "npm / pnpm / yarn / bun",
        "flagship_libraries": [
            ("express", "Minimalist web framework"),
            ("lodash", "Utility function library"),
            ("axios", "HTTP client for browser and Node.js"),
            ("date-fns", "Lightweight date utility library"),
            ("ws", "WebSocket implementation"),
        ],
        "tooling": [
            ("eslint", "Pluggable JavaScript linter"),
            ("prettier", "Opinionated code formatter"),
            ("jest", "Delightful JavaScript testing"),
            ("vite", "Lightning-fast HMR and build tool"),
            ("rollup", "ES module bundler"),
        ],
        "trending_projects": [
            "Node.js — JavaScript runtime built on V8",
            "Express — battle-tested web framework",
            "Webpack — module bundler (legacy but still huge)",
            "Next.js — full-stack React framework",
            "Remix — full-stack web framework",
        ],
        "best_practice_tip": "Use pnpm instead of npm — it saves disk space via content-addressable storage and speeds up installs.",
        "beginner_friendly": True,
        "ecosystem_quote": "JavaScript's package ecosystem is the largest in the world — 2M+ packages and growing daily.",
    },
    "Java": {
        "package_manager": "Maven (mvn) / Gradle",
        "flagship_libraries": [
            ("Spring Boot", "Enterprise application framework"),
            ("Hibernate", "ORM for relational databases"),
            ("Guava", "Google's core utility library"),
            ("Jackson", "JSON processing / serialization"),
            ("Apache Commons", "Reusable Java components"),
        ],
        "tooling": [
            ("mvn", "Maven build tool and package manager"),
            ("gradle", "Build automation with DAG-based tasks"),
            ("junit", "Unit testing framework"),
            ("spotbugs", "Static analysis for Java bugs"),
            ("jmc", "Java Mission Control — profiler"),
        ],
        "trending_projects": [
            "Spring Boot 3 — cloud-native Java framework",
            "Quarkus — Supersonic Subatomic Java (native!)",
            "Micronaut — AOT-compiled, cloud-native framework",
            "Helidon — Java cloud-native microservices",
            "Vert.x — reactive toolkit for JVM",
        ],
        "best_practice_tip": "Prefer jshell for quick experiments and javadoc for documentation — both ship with the JDK.",
        "beginner_friendly": True,
        "ecosystem_quote": "Maven Central: the most curated package registry in existence, with over 4 million artifacts.",
    },
    "C/C++": {
        "package_manager": "vcpkg / Conan / CMake FetchContent",
        "flagship_libraries": [
            ("Boost", "Peer-reviewed C++ libraries"),
            ("Abseil", "Google's C++ core utilities"),
            ("fmt", "Fast, safe formatting library"),
            ("nlohmann/json", "JSON parser for modern C++"),
            ("opencv", "Computer vision and image processing"),
        ],
        "tooling": [
            ("cmake", "Cross-platform build generator"),
            ("vcpkg", "C++ package manager (Microsoft)"),
            ("conan", "C/C++ package manager"),
            ("clang-tidy", "Static analysis with fix suggestions"),
            ("ccache", "Compiler cache for faster rebuilds"),
        ],
        "trending_projects": [
            "Linux kernel — the backbone of modern servers",
            "Git — version control system (yes, in C!)",
            "Redis — in-memory data store (C)",
            "SQLite — most widely deployed database engine",
            "Godot — game engine (C++ with GDScript)",
        ],
        "best_practice_tip": "Use CMake's FetchContent or find_package to manage dependencies — manual #include paths are a maintenance nightmare.",
        "beginner_friendly": False,
        "ecosystem_quote": "C/C++ has no single dominant package registry — conan and vcpkg fill the void with growing ecosystems.",
    },
}


def build_ecosystem_map(language):
    """Build a comprehensive ecosystem map for the language."""
    eco = ECO_DATA.get(language)
    if not eco:
        return None

    # Select a "featured project" for spotlight
    random.seed(hash(language + "spotlight"))
    featured = random.choice(eco["trending_projects"])

    # Select flagship library for deep-dive
    random.seed(hash(language + "lib"))
    deep_lib = random.choice(eco["flagship_libraries"])

    # Build package list with popularity indicators
    package_list = []
    for lib, desc in eco["flagship_libraries"]:
        stars = random.randint(5000, 120000)
        package_list.append({
            "name": lib,
            "description": desc,
            "approx_stars": stars,
            "tier": "Flagship" if stars > 50000 else "Popular"
        })

    # Build tooling list
    tooling_list = []
    for tool, tip in eco["tooling"]:
        tooling_list.append({
            "name": tool,
            "how_to_use": tip
        })

    # Calculate ecosystem "health" score
    health = min(100, random.randint(65, 100))
    if eco["beginner_friendly"]:
        health = min(100, health + 10)

    return {
        "package_manager": eco["package_manager"],
        "flagship_libraries": package_list,
        "deep_dive_lib": {
            "name": deep_lib[0],
            "description": deep_lib[1],
        },
        "tooling": tooling_list,
        "trending_projects": eco["trending_projects"],
        "featured_project": featured,
        "ecosystem_health_score": health,
        "beginner_friendly": eco["beginner_friendly"],
        "best_practice_tip": eco["best_practice_tip"],
        "ecosystem_quote": eco["ecosystem_quote"],
    }


def explore(language):
    """
    Main explore function — deliver ecosystem field guide for the selected language.
    Loads rotation config, builds ecosystem map, advances rotation.
    """
    config = load_rotation()

    if language not in config["languages"]:
        raise ValueError(
            f"Language '{language}' not in rotation. "
            f"Available: {', '.join(config['languages'])}"
        )

    eco_map = build_ecosystem_map(language)
    current_idx = config["languages"].index(language)
    next_idx = (current_idx + 1) % len(config["languages"])

    # Advance rotation: next run selects next language (Go)
    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now().isoformat()
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "ecosystem_map": eco_map,
        "next_language": config["languages"][next_idx],
        "rotation": config["languages"],
        "timestamp": datetime.now().isoformat(),
    }


def run_tests():
    """Run tests to validate the Language EcoHub module."""
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

    print("Testing Language EcoHub...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_eq(True, 0 <= config["current_index"] < 8, "current_index in valid range")
    assert_eq("Rust", config["languages"][0], "Rust is first")

    print("  Testing explore for Rust...")
    result = explore("Rust")
    expected_keys = [
        "tool", "version", "selected_language", "ecosystem_map",
        "next_language", "rotation", "timestamp"
    ]
    for key in expected_keys:
        assert_eq(True, key in result, f"Key '{key}' in result")
    assert_eq("Rust", result["selected_language"], "Rust selected")
    assert_eq("Go", result["next_language"], "Next language is Go")

    print("  Verifying ecosystem_map structure...")
    eco = result["ecosystem_map"]
    assert_eq(True, "package_manager" in eco, "package_manager present")
    assert_eq(True, "flagship_libraries" in eco, "flagship_libraries present")
    assert_eq(True, "tooling" in eco, "tooling present")
    assert_eq(True, "trending_projects" in eco, "trending_projects present")
    assert_eq(True, "ecosystem_health_score" in eco, "ecosystem_health_score present")
    assert_eq(True, "beginner_friendly" in eco, "beginner_friendly present")
    assert_eq(True, "best_practice_tip" in eco, "best_practice_tip present")
    assert_eq(True, "ecosystem_quote" in eco, "ecosystem_quote present")
    assert_eq(True, "deep_dive_lib" in eco, "deep_dive_lib present")
    assert_eq(True, "featured_project" in eco, "featured_project present")

    print("  Verifying flagship libraries structure...")
    for lib in eco["flagship_libraries"]:
        assert_eq(True, "name" in lib, "Library has 'name'")
        assert_eq(True, "description" in lib, "Library has 'description'")
        assert_eq(True, "approx_stars" in lib, "Library has 'approx_stars'")
        assert_eq(True, lib["approx_stars"] >= 0, "Library stars non-negative")

    print("  Verifying tooling structure...")
    for tool in eco["tooling"]:
        assert_eq(True, "name" in tool, "Tool has 'name'")
        assert_eq(True, "how_to_use" in tool, "Tool has 'how_to_use'")

    print("  Verifying Rust ecosystem data...")
    assert_eq("Cargo (crates.io)", eco["package_manager"], "Rust uses Cargo")
    assert_eq(False, eco["beginner_friendly"], "Rust not beginner-friendly")
    assert_in("Cargo", eco["ecosystem_quote"], "Quote mentions Cargo ecosystem")

    print("  Verifying rotation update...")
    config2 = load_rotation()
    assert_eq(1, config2["current_index"], "Index advanced to 1 (Go)")
    assert_eq("Rust", config2["last_language"], "Last language recorded as Rust")

    print("  Testing explore for Go (next in rotation)...")
    result2 = explore("Go")
    assert_eq("Go", result2["selected_language"], "Go is selected")
    assert_eq("Swift", result2["next_language"], "Next language is Swift")
    assert_eq("go mod (proxy.golang.org)", result2["ecosystem_map"]["package_manager"], "Go uses go mod")

    print("  Verifying all 8 languages are covered...")
    for lang in config["languages"]:
        r = explore(lang)
        assert_eq(lang, r["selected_language"], f"{lang} selected correctly")
        eco = r["ecosystem_map"]
        assert_eq(True, eco is not None, f"{lang} has ecosystem map")
        assert_true(len(eco["flagship_libraries"]) >= 5, f"{lang} has >=5 libraries")
        assert_true(len(eco["tooling"]) >= 5, f"{lang} has >=5 tools")
        assert_true(len(eco["trending_projects"]) >= 5, f"{lang} has >=5 trending projects")

    print("  Testing invalid language handling...")
    try:
        explore("Python")
        tests_failed += 1
        print("  ❌ FAIL: No error raised for invalid language")
    except ValueError as e:
        tests_passed += 1
        print("  ✅ PASS: ValueError raised for invalid language")
        assert_in("not in rotation", str(e), "Error mentions rotation")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ FAIL: Wrong exception: {e}")

    print("  Testing ecosystem_health_score range...")
    for lang in ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]:
        r = explore(lang)
        score = r["ecosystem_map"]["ecosystem_health_score"]
        assert_true(0 <= score <= 110, f"{lang} health score in [0,110] range")

    print("  Testing rotation full cycle...")
    config = load_rotation()
    current = config["current_index"]
    assert_true(current >= 0 and current < 8, "current_index valid after cycle")

    print(f"\n{'='*55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("🌿 All EcoHub tests passed! Ecosystem mapped.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--explore":
        language = sys.argv[2] if len(sys.argv) > 2 else "Rust"
        result = explore(language)
        print(json.dumps(result, indent=2))
    else:
        print(f"Language EcoHub v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m language_ecohub --test       # Run tests")
        print("  python -m language_ecohub --explore [lang]  # Explore ecosystem")