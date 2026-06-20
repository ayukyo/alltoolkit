#!/usr/bin/env python3
"""
✉️ polyglot_correspondent v1.0.0 — Epistolary Engine for Programming Languages

Concept
-------
"Every program is a letter. Every language signs its letters differently.
Rust is a Swiss watchmaker — precision engraved on heavy parchment, signed
with a wax seal of types. Go is a 1950s civil servant — typed on onionskin,
signed in block letters, copied in triplicate. Swift is a Victorian
gentleman-scholar — embossed on cream laid paper, signed with an italic nib,
sealed in crimson wax. Java is a Victorian-era law firm — foolscap,
three-carbon copy, embossed company seal, registered post. JavaScript is
a Telegram — brief, dashed-off, no envelope. C is a chisel-stone inscription —
no envelope at all, the wall is the letter."

Each language is examined as a correspondence tradition with twelve facets:
  - letterhead   : the file/module/namespace (printed header)
  - addressing   : imports / packages (addressing the recipient)
  - salutation   : entry point (the opening greeting)
  - quill        : primary unit of expression (struct/class/function)
  - wax_seal     : type system (the embossed seal of authenticity)
  - margin_notes : comment culture and grammar
  - postscript   : defer/finally/afterAll (the P.S. after the body)
  - valediction  : return/exit/close (the closing salutation)
  - signature    : author identity, version, package metadata
  - stationery   : file extension, encoding, source layout
  - postal_route : package manager / module resolution
  - tone         : formal / terse / friendly / official

Distinct from existing tools (oracle, tarot, echoes, horology, architect,
signal, loom, resonator, ...) — uniquely about the *epistolary voice*:
the conventions of address, salutation, signature, postscript, stationery,
and the postal route.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import random
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-correspondent"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent  # polyglot_correspondent/
_WORKSPACE_ROOT = _MODULE_DIR.parent         # AllToolkit/ -> workspace/
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# Tone classes — letters carry a register.
TONE_FORMAL = "FORMAL"      # deferential, structured
TONE_OFFICIAL = "OFFICIAL"  # bureaucratic, certified
TONE_TERSE = "TERSE"        # brief, clipped
TONE_FRIENDLY = "FRIENDLY"  # warm, personal
TONE_FLORID = "FLORID"      # ornamental, decorative
TONE_MONOLITHIC = "MONOLITHIC"  # one big file, the wall is the letter

# Postal route families — how the language moves its letters.
POSTAL_DIRECT = "DIRECT"        # no module system; the wall is the letter
POSTAL_STD = "STANDARD"         # conventional package manager + module path
POSTAL_REGISTRY = "REGISTRY"    # central index of packages (crates, npm, maven)
POSTAL_VENDOR = "VENDOR"        # vendored dependencies, in-tree


# ─────────────────────────────────────────────────────────────────────────────
# Epistolary Database — one entry per rotation language
# ─────────────────────────────────────────────────────────────────────────────

EPISTOLARY_DB: Dict[str, Dict[str, Any]] = {

    # ── Rust ────────────────────────────────────────────────────────────────
    "Rust": {
        "letterhead": {
            "style": "Cargo.toml on heavy parchment — edition-stamped",
            "mechanism": "Cargo.toml declares [package], [dependencies], [features]. Edition = letterhead printing (2015, 2018, 2021, 2024).",
            "idiom": "[package]\nname = \"hello\"\nedition = \"2021\"  # the printed edition",
            "key_traits": ["edition-stamped", "feature-flagged", "manifest + lockfile"],
            "paper": "heavy parchment (strong types)",
            "emoji": "📜",
        },
        "addressing": {
            "style": "use crate:: / use std:: / use external::",
            "mechanism": "Items are addressed by absolute or relative paths. pub makes them public. Crates are the city of origin.",
            "idiom": "use crate::module::Type;\nuse std::collections::HashMap;",
            "key_traits": ["explicit visibility (pub)", "no namespace collisions", "tree-shaken"],
            "postage": "compile-time checked",
            "emoji": "📮",
        },
        "salutation": {
            "style": "fn main() { ... } — the formal opening",
            "mechanism": "A single main function. No top-level statements. The program begins with a deliberate greeting.",
            "idiom": "fn main() {\n    println!(\"Dear developer,\");\n}",
            "key_traits": ["single entry point", "no top-level code", "Result return possible"],
            "emoji": "👋",
        },
        "quill": {
            "style": "struct / enum / trait / impl",
            "mechanism": "struct = paper. enum = choice. trait = letterhead seal. impl = ink applied.",
            "idiom": "struct Letter { to: String, from: String, body: String }",
            "key_traits": ["algebraic data types", "trait-based polymorphism", "ownership as paper trail"],
            "emoji": "✍️",
        },
        "wax_seal": {
            "style": "Compile-time type system — embossed on every line",
            "mechanism": "The borrow checker & type checker are the seal-makers. Every letter leaves the press already sealed.",
            "idiom": "fn send(letter: &Letter) -> Result<(), PostageError> { ... }",
            "key_traits": ["no runtime type erasure", "memory safety proven", "exhaustive matching"],
            "seal_color": "crimson",
            "emoji": "🕯️",
        },
        "margin_notes": {
            "style": "// line comments, /// doc comments, //! module docs",
            "mechanism": "/// generates rustdoc. //! documents the enclosing module. //! produces MD books.",
            "idiom": "/// Send a letter, returning postage due.\n///\n/// # Errors\n/// Returns `PostageError` if postage is insufficient.",
            "key_traits": ["/// for items", "//! for modules", "sections like # Errors, # Panics, # Examples"],
            "emoji": "💬",
        },
        "postscript": {
            "style": "Drop / RAII / explicit close — no implicit P.S.",
            "mechanism": "Destructors run on scope exit. No defer keyword; the letter's postscript is the type system releasing resources.",
            "idiom": "{ let f = File::open(\"data\")?; /* ... */ }  // f closed at brace end",
            "key_traits": ["RAII = postscript", "no defer keyword", "Drop trait customizable"],
            "emoji": "📨",
        },
        "valediction": {
            "style": "Ok(()) or main() returning () — the formal close",
            "mechanism": "main() returns () or Result<(), E>. The letter is sealed when main returns.",
            "idiom": "fn main() -> Result<(), Box<dyn Error>> { send_letter()?; Ok(()) }",
            "key_traits": ["exit code = Result Err", "Ok(()) = success", "process::exit available"],
            "emoji": "🖋️",
        },
        "signature": {
            "style": "edition = \"2021\" in Cargo.toml, package.version",
            "mechanism": "Every crate is signed with its version, edition, authors, license.",
            "idiom": "[package]\nversion = \"1.0.0\"\nedition = \"2021\"\nauthors = [\"Jane <jane@example.com>\"]\nlicense = \"MIT\"",
            "key_traits": ["semver enforced", "edition marks", "authors + license"],
            "emoji": "👤",
        },
        "stationery": {
            "extension": ".rs",
            "encoding": "UTF-8",
            "layout": "modules in src/, examples in examples/, benches in benches/",
            "extra": "rustfmt is the stationer — re-flows every letter to the same margin.",
            "key_traits": ["file extension as the printed mark", "encoding = character set", "layout = folder structure convention"],
            "emoji": "📜",
        },
        "postal_route": {
            "system": POSTAL_REGISTRY,
            "manager": "Cargo + crates.io",
            "mechanism": "crates.io is the post office. Cargo.lock pins every letter. Vendoring via cargo vendor.",
            "idiom": "[dependencies]\nserde = \"1.0\"  # latest 1.x",
            "key_traits": ["semver-resolved", "lockfile mandatory for binaries", "feature unification"],
            "emoji": "🚚",
        },
        "tone": {
            "register": TONE_FORMAL,
            "feel": "A precise, courteous letter on heavy parchment. Every paragraph sealed and postmarked before sending.",
            "key_traits": ["epistolary register", "social convention", "mood of the letter"],
            "emoji": "🎭",
        },
    },

    # ── Go ──────────────────────────────────────────────────────────────────
    "Go": {
        "letterhead": {
            "style": "go.mod — minimal printed header, no edition",
            "mechanism": "go.mod declares module path + Go version. No edition flag; the toolchain version is the edition.",
            "idiom": "module example.com/hello\n\ngo 1.22",
            "key_traits": ["minimal manifest", "toolchain-versioned", "single go.mod per module"],
            "paper": "onionskin",
            "emoji": "📜",
        },
        "addressing": {
            "style": "import \"path/to/pkg\" — flat, slash-separated",
            "mechanism": "Imports are URL-like paths. Package name is the last element. Exported = starts with capital letter (case-based visibility).",
            "idiom": "import (\n    \"fmt\"\n    \"example.com/hello/internal/letter\"\n)",
            "key_traits": ["case-based visibility", "no explicit pub", "single package per dir"],
            "postage": "compile-time",
            "emoji": "📮",
        },
        "salutation": {
            "style": "package main + func main() — civil-service opening",
            "mechanism": "Top-level statements prohibited. main() is the greeting, in package main.",
            "idiom": "package main\n\nimport \"fmt\"\n\nfunc main() {\n    fmt.Println(\"Hello, developer.\")\n}",
            "key_traits": ["package main", "func main is required", "init() runs before main"],
            "emoji": "👋",
        },
        "quill": {
            "style": "struct + methods (no classes, no inheritance)",
            "mechanism": "struct is the paper. methods (func (r *R) Write) are the ink. Composition over inheritance.",
            "idiom": "type Letter struct { To, From, Body string }\n\nfunc (l *Letter) Send() error { return nil }",
            "key_traits": ["no classes", "no generics pre-1.18 (now available)", "struct embedding for composition"],
            "emoji": "✍️",
        },
        "wax_seal": {
            "style": "Static typing + interface satisfaction — embossed by compiler",
            "mechanism": "Types are static. Interfaces are satisfied implicitly. No runtime seal needed.",
            "idiom": "type Sender interface { Send() error }",
            "key_traits": ["implicit interface satisfaction", "no generics before 1.18", "structural typing for interfaces"],
            "seal_color": "navy",
            "emoji": "🕯️",
        },
        "margin_notes": {
            "style": "// line comments, /* block */ for big sections",
            "mechanism": "godoc reads comments above declarations. // FunctionName: line is the docstring.",
            "idiom": "// Send dispatches a letter.\n// It returns nil on success.\nfunc Send() error { ... }",
            "key_traits": ["doc = comment above decl", "no /// distinction", "package comment at top of one file"],
            "emoji": "💬",
        },
        "postscript": {
            "style": "defer — the only explicit postscript in the rotation",
            "mechanism": "defer f.Close() schedules a postscript at function return. LIFO order.",
            "idiom": "func read() error {\n    f, err := os.Open(\"data\")\n    if err != nil { return err }\n    defer f.Close()  // P.S.\n    return process(f)\n}",
            "key_traits": ["LIFO", "runs even on panic", "arguments evaluated immediately"],
            "emoji": "📨",
        },
        "valediction": {
            "style": "return error or nil — the civil-service close",
            "mechanism": "Function returns its last value. main returns nothing; os.Exit(code) for explicit code.",
            "idiom": "func send() error { return nil }  // nil = signed and sealed",
            "key_traits": ["nil error = success", "no Result wrapper", "os.Exit for explicit code"],
            "emoji": "🖋️",
        },
        "signature": {
            "style": "git tag + go.mod version — minimal, version-control-signed",
            "mechanism": "No author field in code. Module path is the signature. Semantic versioning via git tags.",
            "idiom": "git tag v1.0.0 && git push --tags",
            "key_traits": ["git-driven versioning", "no in-source author", "module path as identity"],
            "emoji": "👤",
        },
        "stationery": {
            "extension": ".go",
            "encoding": "UTF-8, must be in package declaration",
            "layout": "package per directory, no nesting of packages",
            "extra": "gofmt is the stationer. tabs for indent. goimports manages addressing.",
            "key_traits": ["file extension as the printed mark", "encoding = character set", "layout = folder structure convention"],
            "emoji": "📜",
        },
        "postal_route": {
            "system": POSTAL_REGISTRY,
            "manager": "Go modules + proxy.golang.org",
            "mechanism": "Module proxy by default. GOPROXY can be set to direct, off, or a custom proxy.",
            "idiom": "GOPROXY=https://proxy.golang.org,direct",
            "key_traits": ["proxy by default", "sum.golang.org for checksums", "replace directives for forks"],
            "emoji": "🚚",
        },
        "tone": {
            "register": TONE_TERSE,
            "feel": "A clipped letter on onionskin. The civil service writes clearly, in block letters, three copies stapled together.",
            "key_traits": ["epistolary register", "social convention", "mood of the letter"],
            "emoji": "🎭",
        },
    },

    # ── Swift ───────────────────────────────────────────────────────────────
    "Swift": {
        "letterhead": {
            "style": "Package.swift — embossed, gilt-edged",
            "mechanism": "Package.swift declares products, targets, dependencies. platforms array = letterhead restrictions.",
            "idiom": "// swift-tools-version: 5.9\nimport PackageDescription\n\nlet package = Package(\n    name: \"Hello\",\n    platforms: [.macOS(.v13)],\n    products: [.library(name: \"Hello\", targets: [\"Hello\"])],\n    targets: [.target(name: \"Hello\")]\n)",
            "key_traits": ["swift-tools-version pragma", "platform-restricted", "gilt-edged by convention"],
            "paper": "cream laid paper",
            "emoji": "📜",
        },
        "addressing": {
            "style": "import Module / internal / fileprivate / public / open",
            "mechanism": "Five visibility levels. module-wide is the default for top-level decls. fileprivate is the private study.",
            "idiom": "import Foundation\n\npublic struct Letter {\n    public let to: String\n    fileprivate let seal: Seal\n}",
            "key_traits": ["five access levels", "open for subclassing across modules", "internal is default"],
            "postage": "compile-time",
            "emoji": "📮",
        },
        "salutation": {
            "style": "@main + static func main() — the gentleman's bow",
            "mechanism": "@main attribute marks the entry point. Or top-level executable code in scripts.",
            "idiom": "@main\nstruct Hello {\n    static func main() {\n        print(\"Dear developer,\")\n    }\n}",
            "key_traits": ["@main attribute", "top-level code allowed in scripts", "no func main() boilerplate"],
            "emoji": "👋",
        },
        "quill": {
            "style": "struct / class / protocol / extension",
            "mechanism": "struct = value-type letter. class = reference-type. protocol = letterhead seal. extension = marginal additions.",
            "idiom": "protocol Sendable { func send() throws }\n\nstruct Letter: Sendable {\n    let to: String\n    func send() throws { ... }\n}",
            "key_traits": ["value + reference types", "protocol-oriented", "extensions add to types retroactively"],
            "emoji": "✍️",
        },
        "wax_seal": {
            "style": "Strong static typing + optionals — sealed with crimson wax",
            "mechanism": "Optional<T> forces handling. throws is type-checked. Generics are first-class. The seal is intricate.",
            "idiom": "func send(_ letter: Letter) throws -> Receipt",
            "key_traits": ["Optional<T> forces handling", "typed throws (Swift 6)", "Sendable for thread safety"],
            "seal_color": "crimson",
            "emoji": "🕯️",
        },
        "margin_notes": {
            "style": "//, ///, /** */, // MARK:-, #warning, #error",
            "mechanism": "/// DocC comments. // MARK:- for Xcode section breaks. #warning / #error for compile-time marginalia.",
            "idiom": "/// Sends the letter, throwing on postage failure.\n///\n/// - Parameter letter: The letter to dispatch.\n/// - Throws: ``PostageError``\nfunc send(_ letter: Letter) throws { ... }",
            "key_traits": ["DocC markup", "MARK for navigation", "#warning / #error pragmas"],
            "emoji": "💬",
        },
        "postscript": {
            "style": "defer — same LIFO postscript as Go",
            "mechanism": "defer { f.close() } runs at scope exit. Available since Swift 2.",
            "idiom": "func read() throws {\n    let f = try FileHandle(forReadingFrom: url)\n    defer { try? f.close() }  // P.S.\n    return try process(f)\n}",
            "key_traits": ["LIFO", "closure form", "runs on throw"],
            "emoji": "📨",
        },
        "valediction": {
            "style": "return / throw — the gentleman's bow at the door",
            "mechanism": "Function returns its value, or throws. No special success type. The reader takes leave gracefully.",
            "idiom": "func send() throws -> Receipt { ... }  // throws, not Result",
            "key_traits": ["throws for failure", "no Result required", "guard let for early leave"],
            "emoji": "🖋️",
        },
        "signature": {
            "style": "version in Package.swift, author in git",
            "mechanism": "Version in Package.swift or git tag. No in-source author. Each library is signed with the maintainer's name in the repo.",
            "idiom": "git tag 1.0.0 && git push --tags",
            "key_traits": ["semver in Package.swift", "git tag for release", "no header author field"],
            "emoji": "👤",
        },
        "stationery": {
            "extension": ".swift",
            "encoding": "UTF-8",
            "layout": "one type per file by convention; Sources/<Target>/",
            "extra": "swift-format is the stationer. swiftlint checks the seal. DocC publishes the marginalia.",
            "key_traits": ["file extension as the printed mark", "encoding = character set", "layout = folder structure convention"],
            "emoji": "📜",
        },
        "postal_route": {
            "system": POSTAL_REGISTRY,
            "manager": "Swift Package Manager + GitHub",
            "mechanism": "SPM resolves packages by URL. No central registry; the post office is Git itself.",
            "idiom": ".package(url: \"https://github.com/apple/swift-argument-parser\", from: \"1.3.0\")",
            "key_traits": ["Git as the post office", "semver tags", "Package.resolved locks"],
            "emoji": "🚚",
        },
        "tone": {
            "register": TONE_FLORID,
            "feel": "A cream-laid letter, written with an italic nib, sealed in crimson wax. Verbose courtesies, named parameters, protocol-oriented elegance.",
            "key_traits": ["epistolary register", "social convention", "mood of the letter"],
            "emoji": "🎭",
        },
    },

    # ── Kotlin ──────────────────────────────────────────────────────────────
    "Kotlin": {
        "letterhead": {
            "style": "build.gradle.kts (Kotlin DSL) — modern business letter",
            "mechanism": "build.gradle.kts uses Kotlin DSL. version, group, dependencies declared as typed Kotlin code.",
            "idiom": "plugins { kotlin(\"jvm\") version \"1.9.0\" }\ngroup = \"com.example\"\nversion = \"1.0.0\"",
            "key_traits": ["Kotlin DSL", "typed build", "multiplatform-aware"],
            "paper": "modern business paper",
            "emoji": "📜",
        },
        "addressing": {
            "style": "package com.example + import com.other.lib.Type",
            "mechanism": "Java-style package paths. Default visibility is public. internal for module-scoped.",
            "idiom": "package com.example.letters\n\nimport com.postal.Seal\nimport com.postal.Stamp",
            "key_traits": ["Java-compatible", "internal = module-scoped", "default public"],
            "postage": "compile-time",
            "emoji": "📮",
        },
        "salutation": {
            "style": "fun main(args: Array<String>) — concise bow",
            "mechanism": "Single main function. Or top-level functions callable as entry. Kotlin 1.3+ has no args requirement.",
            "idiom": "fun main() {\n    println(\"Dear developer,\")\n}",
            "key_traits": ["fun main() without args in 1.3+", "top-level functions", "expression-body allowed"],
            "emoji": "👋",
        },
        "quill": {
            "style": "class / data class / object / sealed class / interface",
            "mechanism": "class is reference. data class auto-generates equals/hashCode/copy. object = singleton. sealed class = sealed letter set.",
            "idiom": "data class Letter(val to: String, val from: String, val body: String)\n\nobject PostalService { fun send(l: Letter) = ... }",
            "key_traits": ["data class", "sealed class for ADT", "object for singleton"],
            "emoji": "✍️",
        },
        "wax_seal": {
            "style": "Static typing + nullable types (T?) — embossed in violet",
            "mechanism": "T? means nullable. Elvis (?:) provides default. The seal is the null-safety signature.",
            "idiom": "fun send(letter: Letter?): Receipt = letter?.let { ... } ?: error(\"no letter\")",
            "key_traits": ["null safety at type level", "platform types for Java interop", "sealed class for restricted hierarchies"],
            "seal_color": "violet",
            "emoji": "🕯️",
        },
        "margin_notes": {
            "style": "//, /* */, /** KDoc */",
            "mechanism": "/** ... */ KDoc with @param, @return, @throws, @sample tags. dokka generates docs.",
            "idiom": "/**\n * Sends the letter.\n *\n * @param letter the letter to send\n * @return the receipt\n * @throws PostageError if postage insufficient\n * @sample samples.sendLetter\n */\nfun send(letter: Letter): Receipt { ... }",
            "key_traits": ["KDoc tags", "@sample for example generation", "dokka is the doc stationer"],
            "emoji": "💬",
        },
        "postscript": {
            "style": "try { } finally { } — the P.S. with cleanup",
            "mechanism": "finally block always runs. use { } function (kotlin's closeable-with-postscript) is shorthand.",
            "idiom": "FileInputStream(\"data\").use { fis -> return process(fis) }  // P.S. = close()\n\ntry { ... } finally { close() }",
            "key_traits": ["use {} = closeable pattern", "finally always runs", "T.use is in stdlib"],
            "emoji": "📨",
        },
        "valediction": {
            "style": "return value or throw — concise close",
            "mechanism": "Function returns typed value or throws. Result<T> available for functional style.",
            "idiom": "fun send(): Receipt = sendInternal()  // no special wrapper",
            "key_traits": ["return value or throw", "Result<T> available", "Nothing return type for always-throw"],
            "emoji": "🖋️",
        },
        "signature": {
            "style": "build.gradle.kts: version = \"1.0.0\", group = \"com.example\"",
            "mechanism": "Version + group declared in build script. Author via git or build config.",
            "idiom": "group = \"com.example\"\nversion = \"1.0.0\"",
            "key_traits": ["gradle metadata", "git tag for release", "POM for Maven"],
            "emoji": "👤",
        },
        "stationery": {
            "extension": ".kt",
            "encoding": "UTF-8",
            "layout": "src/main/kotlin/<package-path>/",
            "extra": "ktlint is the stationer. IntelliJ formatter is canonical.",
            "key_traits": ["file extension as the printed mark", "encoding = character set", "layout = folder structure convention"],
            "emoji": "📜",
        },
        "postal_route": {
            "system": POSTAL_REGISTRY,
            "manager": "Maven Central + Gradle",
            "mechanism": "Maven Central is the main post office. Gradle resolves via metadata.",
            "idiom": "implementation(\"com.google.guava:guava:32.1.0-jre\")",
            "key_traits": ["Maven coordinates", "kotlinx for Kotlin-specific", "version catalog (libs.versions.toml)"],
            "emoji": "🚚",
        },
        "tone": {
            "register": TONE_FRIENDLY,
            "feel": "A modern letter on good paper. Concise, friendly, signed with a smiley. Concise bow at the door, no ornamentation.",
            "key_traits": ["epistolary register", "social convention", "mood of the letter"],
            "emoji": "🎭",
        },
    },

    # ── TypeScript ──────────────────────────────────────────────────────────
    "TypeScript": {
        "letterhead": {
            "style": "package.json — modern stationery with optional wax stamp",
            "mechanism": "package.json declares name, version, dependencies. typescript field for TS version. tsconfig.json for letterhead formatting.",
            "idiom": "{\n  \"name\": \"hello\",\n  \"version\": \"1.0.0\",\n  \"devDependencies\": { \"typescript\": \"^5.4.0\" }\n}",
            "key_traits": ["tsconfig.json separate", "compilerOptions typed", "include/exclude file globs"],
            "paper": "modern stationery",
            "emoji": "📜",
        },
        "addressing": {
            "style": "import { X } from 'pkg' — modern addressing",
            "mechanism": "ES modules. import / export. npm scope (@org/pkg) for organizational addressing.",
            "idiom": "import { send } from '@post/letter';\nimport type { Letter } from './types';",
            "key_traits": ["ES module syntax", "import type for types-only", "scoped packages (@org)"],
            "postage": "transpile-time (erased at runtime)",
            "emoji": "📮",
        },
        "salutation": {
            "style": "Top-level await, async function main(), or no main",
            "mechanism": "No mandatory main. Modules execute on import. main() is a convention, not a language feature.",
            "idiom": "// index.ts — no main required\nconst letter: Letter = { to: 'dev' };\nawait send(letter);",
            "key_traits": ["no main function", "top-level await", "module side-effects on import"],
            "emoji": "👋",
        },
        "quill": {
            "style": "interface / type / class / function",
            "mechanism": "interface and type alias are paper. class is reference. function is verb.",
            "idiom": "interface Letter { to: string; body: string }\ntype Sendable = (l: Letter) => Promise<void>;",
            "key_traits": ["structural typing", "type aliases for unions", "interface for object shape"],
            "emoji": "✍️",
        },
        "wax_seal": {
            "style": "Compile-time types, but erased at runtime — seal stamped, then dissolved",
            "mechanism": "TypeScript adds types that are erased by tsc. Runtime has no type safety (except what you write).",
            "idiom": "function send(letter: Letter): Promise<Receipt> { ... }  // types erased, runtime is JS",
            "key_traits": ["type erasure", "structural typing", "no runtime type guarantees"],
            "seal_color": "indigo (translucent)",
            "emoji": "🕯️",
        },
        "margin_notes": {
            "style": "//, /* */, /** JSDoc */",
            "mechanism": "/** JSDoc */ works for both TS and plain JS. TSDoc for richer TS-specific docs.",
            "idiom": "/**\n * Sends the letter.\n * @param letter - the letter to dispatch\n * @returns the receipt\n */\nexport function send(letter: Letter): Promise<Receipt> { ... }",
            "key_traits": ["JSDoc compatible", "TSDoc extensions", "@remarks, @example"],
            "emoji": "💬",
        },
        "postscript": {
            "style": "try { } finally { } + using (TC39 stage 3) — modern P.S.",
            "mechanism": "try/finally for cleanup. `using` keyword (stage 3 / TS 5.2+) for explicit disposable.",
            "idiom": "using f = await openFile(\"data\");\nreturn process(f);  // P.S.: f disposed at scope end",
            "key_traits": ["try/finally classic", "using for disposable", "Symbol.dispose protocol"],
            "emoji": "📨",
        },
        "valediction": {
            "style": "return / throw / Promise.reject — the modern close",
            "mechanism": "Function returns value or throws. Async functions return Promise. No Result wrapper by default.",
            "idiom": "export async function send(letter: Letter): Promise<Receipt> { ... }",
            "key_traits": ["return or throw", "Promise<T> for async", "Result via libraries like ts-results"],
            "emoji": "🖋️",
        },
        "signature": {
            "style": "package.json: version, name, author, license",
            "mechanism": "package.json declares the signature. Author + version + license in JSON.",
            "idiom": "{\n  \"name\": \"@scope/letter\",\n  \"version\": \"1.0.0\",\n  \"author\": \"Jane <jane@example.com>\",\n  \"license\": \"MIT\"\n}",
            "key_traits": ["author + license", "scoped (@scope) names", "publishConfig"],
            "emoji": "👤",
        },
        "stationery": {
            "extension": ".ts",
            "encoding": "UTF-8",
            "layout": "src/, dist/, lib/ — convention varies",
            "extra": "prettier is the stationer. eslint checks the seal. tsc checks types.",
            "key_traits": ["file extension as the printed mark", "encoding = character set", "layout = folder structure convention"],
            "emoji": "📜",
        },
        "postal_route": {
            "system": POSTAL_REGISTRY,
            "manager": "npm + node_modules",
            "mechanism": "npm registry is the post office. package-lock.json pins every letter. node_modules is the mailroom.",
            "idiom": "npm install @post/letter",
            "key_traits": ["npm by default", "yarn / pnpm alternatives", "lockfile mandatory"],
            "emoji": "🚚",
        },
        "tone": {
            "register": TONE_FRIENDLY,
            "feel": "A modern letter on translucent stationery. Type-safe at the desk, dissolved at the door. Friendly, modern, sign-off with a smiley.",
            "key_traits": ["epistolary register", "social convention", "mood of the letter"],
            "emoji": "🎭",
        },
    },

    # ── JavaScript ──────────────────────────────────────────────────────────
    "JavaScript": {
        "letterhead": {
            "style": "package.json — the same stationery, no seal",
            "mechanism": "Same as TypeScript but no type field. 'type': 'module' for ESM. No tsconfig.",
            "idiom": "{\n  \"name\": \"hello\",\n  \"version\": \"1.0.0\",\n  \"type\": \"module\"\n}",
            "key_traits": ["type: module for ESM", "no compile step", "engines field for node version"],
            "paper": "thin, flexible",
            "emoji": "📜",
        },
        "addressing": {
            "style": "import { X } from 'pkg' (ESM) or require('pkg') (CJS)",
            "mechanism": "ES modules or CommonJS. Two addressing systems in the same language.",
            "idiom": "import { send } from './letter.js';\nconst { send } = require('./letter.js');  // CJS",
            "key_traits": ["ESM + CJS dual", "default + named exports", "dynamic import()"],
            "postage": "runtime only (no compile)",
            "emoji": "📮",
        },
        "salutation": {
            "style": "No main. Module side-effects on import.",
            "mechanism": "Code runs on import. index.js is the conventional entry. No compiler-enforced entry point.",
            "idiom": "// index.js — runs on import\nconst letter = { to: 'dev' };\nsend(letter);",
            "key_traits": ["no main", "side-effects on import", "IIFE pattern (legacy)"],
            "emoji": "👋",
        },
        "quill": {
            "style": "function / class / object literal",
            "mechanism": "function is verb. class is sugar over prototype. object literal is letter on the fly.",
            "idiom": "function send(letter) { return Promise.resolve(receipt); }\n\nconst Letter = class { constructor(to) { this.to = to; } };",
            "key_traits": ["first-class functions", "prototype-based", "object literal shorthand"],
            "emoji": "✍️",
        },
        "wax_seal": {
            "style": "No seal at all — the letter travels unsealed",
            "mechanism": "JavaScript has no type system. typeof lies. The letter is delivered as-is.",
            "idiom": "typeof null === 'object'  // the unsealed letter quirk",
            "key_traits": ["no compile-time types", "typeof quirks", "JSDoc for hint only"],
            "seal_color": "none (unsealed)",
            "emoji": "🕯️",
        },
        "margin_notes": {
            "style": "//, /* */, /** JSDoc */",
            "mechanism": "JSDoc for tooling. JSDoc is the only marginal hint; no compiler reads it.",
            "idiom": "/**\n * @param {Letter} letter - the letter to send\n * @returns {Promise<Receipt>}\n */\nfunction send(letter) { ... }",
            "key_traits": ["JSDoc for type hints", "no compiler enforcement", "// @ts-check for opt-in"],
            "emoji": "💬",
        },
        "postscript": {
            "style": "try { } finally { } + using (TS stage 3) — same as TS",
            "mechanism": "try/finally. Stage 3 `using` proposal at TC39. Node's stream.pipeline also acts as P.S.",
            "idiom": "try { ... } finally { close(); }\n\n// Node:\nawait pipeline(source, transform, sink);  // implicit close",
            "key_traits": ["try/finally", "TC39 `using` proposal", "stream.pipeline auto-close"],
            "emoji": "📨",
        },
        "valediction": {
            "style": "return / throw / reject — the hasty close",
            "mechanism": "Function returns value, throws, or rejects a Promise. No type distinguishes success.",
            "idiom": "function send(letter) { return Promise.resolve(receipt); }",
            "key_traits": ["return / throw", "Promise resolve / reject", "unhandled rejection is silent failure"],
            "emoji": "🖋️",
        },
        "signature": {
            "style": "package.json author, version, license",
            "mechanism": "package.json carries the signature. CommonJS/ESM dual format. Maintainers field for org.",
            "idiom": "{\n  \"name\": \"@scope/letter\",\n  \"version\": \"1.0.0\",\n  \"author\": \"Jane\",\n  \"license\": \"MIT\"\n}",
            "key_traits": ["maintainers + authors", "engines field", "type: module/commonjs"],
            "emoji": "👤",
        },
        "stationery": {
            "extension": ".js / .mjs / .cjs",
            "encoding": "UTF-8",
            "layout": "src/, dist/, lib/ — convention varies",
            "extra": "prettier / eslint are the stationers. No seal inspector.",
            "key_traits": ["file extension as the printed mark", "encoding = character set", "layout = folder structure convention"],
            "emoji": "📜",
        },
        "postal_route": {
            "system": POSTAL_REGISTRY,
            "manager": "npm + node_modules",
            "mechanism": "Same as TypeScript: npm registry, package-lock.json, node_modules.",
            "idiom": "npm install letter",
            "key_traits": ["npm registry", "yarn / pnpm", "Deno uses URLs (no node_modules)"],
            "emoji": "🚚",
        },
        "tone": {
            "register": TONE_TERSE,
            "feel": "A telegram. Brief, dashed-off, no envelope. The letter travels unsealed and trusts the recipient.",
            "key_traits": ["epistolary register", "social convention", "mood of the letter"],
            "emoji": "🎭",
        },
    },

    # ── Java ────────────────────────────────────────────────────────────────
    "Java": {
        "letterhead": {
            "style": "pom.xml / build.gradle — embossed company letterhead",
            "mechanism": "Maven or Gradle. Heavy XML or modern DSL. groupId:artifactId:version is the GAV coordinate.",
            "idiom": "<project>\n  <modelVersion>4.0.0</modelVersion>\n  <groupId>com.example</groupId>\n  <artifactId>letter</artifactId>\n  <version>1.0.0</version>\n</project>",
            "key_traits": ["GAV coordinate", "XML or Kotlin DSL", "corporate letterhead"],
            "paper": "foolscap, three-carbon copy",
            "emoji": "📜",
        },
        "addressing": {
            "style": "package + import — Victorian addressing",
            "mechanism": "package matches directory. import brings types. public/private/protected/package-private.",
            "idiom": "package com.example.letters;\n\nimport com.postal.Seal;\nimport com.postal.Stamp;",
            "key_traits": ["four access levels", "package-private default", "directory-mirrored package"],
            "postage": "compile-time",
            "emoji": "📮",
        },
        "salutation": {
            "style": "public static void main(String[] args) — the formal bow",
            "mechanism": "Static main method. Class-based entry point. public + static + void + main is the universal greeting.",
            "idiom": "public class Hello {\n    public static void main(String[] args) {\n        System.out.println(\"Dear developer,\");\n    }\n}",
            "key_traits": ["exactly 'public static void main'", "args[] for command-line", "class-enclosed"],
            "emoji": "👋",
        },
        "quill": {
            "style": "class / interface / abstract class / record",
            "mechanism": "class is paper. record is value-type letter (Java 14+). interface is seal. abstract is incomplete letter.",
            "idiom": "public record Letter(String to, String from, String body) {}\n\npublic interface Sendable { Receipt send() throws PostageError; }",
            "key_traits": ["record for value types", "interface for abstraction", "sealed class for restricted hierarchy"],
            "emoji": "✍️",
        },
        "wax_seal": {
            "style": "Strong static typing + checked exceptions — corporate embossed seal",
            "mechanism": "The compiler is the company secretary. Every method signature declares what it throws. The seal is the JLS.",
            "idiom": "public Receipt send(Letter letter) throws PostageException { ... }",
            "key_traits": ["checked exceptions", "generics with type erasure", "sealed class hierarchies"],
            "seal_color": "navy + gold",
            "emoji": "🕯️",
        },
        "margin_notes": {
            "style": "//, /* */, /** Javadoc */",
            "mechanism": "/** Javadoc */ with @param, @return, @throws, @since tags. javadoc tool generates HTML.",
            "idiom": "/**\n * Sends the letter.\n *\n * @param letter the letter to dispatch\n * @return the receipt\n * @throws PostageException if postage is insufficient\n * @since 1.0\n */\npublic Receipt send(Letter letter) throws PostageException { ... }",
            "key_traits": ["Javadoc tags", "@since for version", "javadoc tool generates HTML"],
            "emoji": "💬",
        },
        "postscript": {
            "style": "try-with-resources (since Java 7) + finally",
            "mechanism": "try-with-resources on AutoCloseable. finally as fallback. The postscript is auto-generated by the compiler.",
            "idiom": "try (var f = new FileInputStream(\"data\")) {\n    return process(f);\n}  // P.S.: f.close() inserted by compiler",
            "key_traits": ["try-with-resources", "AutoCloseable protocol", "suppressed exceptions accessible"],
            "emoji": "📨",
        },
        "valediction": {
            "style": "return value or throw checked exception — the corporate close",
            "mechanism": "Method returns value or throws (declared) exception. The reader acknowledges the receipt.",
            "idiom": "public Receipt send(Letter letter) throws PostageException { ... }",
            "key_traits": ["checked exceptions declared", "Optional<T> for null-safety (Java 8+)", "no Result wrapper"],
            "emoji": "🖋️",
        },
        "signature": {
            "style": "pom.xml: groupId, artifactId, version, scm",
            "mechanism": "Maven POM carries the corporate signature. scm block links to source. developers listed.",
            "idiom": "<developers>\n  <developer><name>Jane</name><email>jane@example.com</email></developer>\n</developers>",
            "key_traits": ["scm block", "developers + contributors", "organization block"],
            "emoji": "👤",
        },
        "stationery": {
            "extension": ".java",
            "encoding": "UTF-8",
            "layout": "src/main/java/<package-path>/, src/test/java/",
            "extra": "google-java-format is the stationer. The letter follows a strict three-part outline.",
            "key_traits": ["file extension as the printed mark", "encoding = character set", "layout = folder structure convention"],
            "emoji": "📜",
        },
        "postal_route": {
            "system": POSTAL_REGISTRY,
            "manager": "Maven Central",
            "mechanism": "Maven Central is the main post office. mvn deploy publishes. Gradle can also resolve Maven artifacts.",
            "idiom": "<dependency>\n  <groupId>com.google.guava</groupId>\n  <artifactId>guava</artifactId>\n  <version>32.1.0-jre</version>\n</dependency>",
            "key_traits": ["Maven Central", "Gradle compatibility", "BOM for version alignment"],
            "emoji": "🚚",
        },
        "tone": {
            "register": TONE_OFFICIAL,
            "feel": "A foolscap letter from a Victorian-era law firm. Three-carbon copy, embossed company seal, registered post. Every word formal.",
            "key_traits": ["epistolary register", "social convention", "mood of the letter"],
            "emoji": "🎭",
        },
    },

    # ── C/C++ ──────────────────────────────────────────────────────────────
    "C/C++": {
        "letterhead": {
            "style": "CMakeLists.txt / Makefile — chiseled into stone",
            "mechanism": "No manifest. The wall is the letter. CMake or Make declares targets, includes, link flags.",
            "idiom": "cmake_minimum_required(VERSION 3.20)\nproject(letter C CXX)\nadd_executable(letter main.c)",
            "key_traits": ["no package manifest", "build script = letterhead", "header/source split"],
            "paper": "stone, chiseled",
            "emoji": "📜",
        },
        "addressing": {
            "style": "#include <stdio.h> or #include \"my.h\"",
            "mechanism": "Preprocessor textually pastes headers. No module system (C++20 has modules, but rare). extern declares external.",
            "idiom": "#include <stdio.h>\n#include \"letter.h\"\n\nextern int postage_due;",
            "key_traits": ["textual inclusion", "header guards", "C++20 modules emerging"],
            "postage": "preprocessor + linker",
            "emoji": "📮",
        },
        "salutation": {
            "style": "int main(int argc, char** argv) — the chiseled bow",
            "mechanism": "main returns int. argc/argv for command-line. The letter begins with a chisel strike.",
            "idiom": "int main(int argc, char** argv) {\n    printf(\"Dear developer,\\n\");\n    return 0;\n}",
            "key_traits": ["int return type", "argc/argv convention", "no string class — char*"],
            "emoji": "👋",
        },
        "quill": {
            "style": "struct / class (C++) / function / typedef",
            "mechanism": "C: struct + function pointers. C++: class with virtual methods. No properties, no closures (in C).",
            "idiom": "// C\ntypedef struct { char* to; char* body; } Letter;\nint send_letter(Letter* l);\n\n// C++\nclass Letter { public: std::string to; void send(); };",
            "key_traits": ["POD structs in C", "classes with virtuals in C++", "no closures in C"],
            "emoji": "✍️",
        },
        "wax_seal": {
            "style": "No seal — the wall accepts what you chisel",
            "mechanism": "C has no type checking beyond function signatures. C++ has more, but still trusts the chisel wielder.",
            "idiom": "void send_letter(Letter* l);  // l could be anything, including null",
            "key_traits": ["void* in C", "no null safety", "undefined behavior on misuse"],
            "seal_color": "none (chiseled bare)",
            "emoji": "🕯️",
        },
        "margin_notes": {
            "style": "//, /* */, /// (Doxygen)",
            "mechanism": "Doxygen reads /** */ and /// as documentation. @param, @return, @brief, @file.",
            "idiom": "/**\n * @brief Send a letter.\n * @param l the letter to send\n * @return 0 on success, errno on failure\n */\nint send_letter(const Letter* l);",
            "key_traits": ["Doxygen tags", "@brief, @param, @return", "no @throws — use @retval"],
            "emoji": "💬",
        },
        "postscript": {
            "style": "goto cleanup + return code (C) / RAII + destructor (C++)",
            "mechanism": "C: label-based cleanup at end of function. C++: destructors on scope exit (RAII). Both run after the body.",
            "idiom": "// C\nint send(Letter* l) {\n    int rc = -1;\n    FILE* f = fopen(\"data\", \"r\");\n    if (!f) goto cleanup;\n    rc = process(f);\ncleanup:\n    if (f) fclose(f);\n    return rc;\n}\n\n// C++\n{ auto f = std::ofstream(\"data\"); process(f); }  // P.S.: ~ofstream closes",
            "key_traits": ["goto cleanup (C idiom)", "RAII (C++)", "no language-level defer"],
            "emoji": "📨",
        },
        "valediction": {
            "style": "return 0 for success, non-zero for error — the chiseled close",
            "mechanism": "C: main returns int. 0 = success, non-zero = error. errno is global state. C++: same, with exceptions as opt-in.",
            "idiom": "int main() { return 0; }  // 0 = signed and sealed",
            "key_traits": ["0 = success convention", "errno global", "exit(code) for early leave"],
            "emoji": "🖋️",
        },
        "signature": {
            "style": "#define VERSION \"1.0.0\" or const in header",
            "mechanism": "Version declared as macro or constant. Author via git. No package metadata.",
            "idiom": "#define LETTER_VERSION \"1.0.0\"\n#define LETTER_AUTHOR \"Jane\"",
            "key_traits": ["#define macros", "no package manifest", "header files for public version"],
            "emoji": "👤",
        },
        "stationery": {
            "extension": ".c / .cpp / .cc / .cxx / .h / .hpp",
            "encoding": "ASCII (legacy) or UTF-8 (modern)",
            "layout": "include/ for headers, src/ for sources, build/ for artifacts",
            "extra": "clang-format is the stone-carver. The wall is laid out by hand.",
            "key_traits": ["file extension as the printed mark", "encoding = character set", "layout = folder structure convention"],
            "emoji": "📜",
        },
        "postal_route": {
            "system": POSTAL_VENDOR,
            "manager": "CMake / Make / system package manager (apt, vcpkg, conan)",
            "mechanism": "No built-in package manager. Vendored sources, system packages, or third-party (vcpkg, conan).",
            "idiom": "#include <openssl/ssl.h>  // from system package\n// or vendored: #include \"third_party/openssl/ssl.h\"",
            "key_traits": ["no built-in registry", "system packages", "vcpkg / conan / hunter"],
            "emoji": "🚚",
        },
        "tone": {
            "register": TONE_MONOLITHIC,
            "feel": "A chiseled inscription on the wall itself. No envelope, no post office. The letter is the wall, and the wall is the letter.",
            "key_traits": ["epistolary register", "social convention", "mood of the letter"],
            "emoji": "🎭",
        },
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Tone + system classification
# ─────────────────────────────────────────────────────────────────────────────

def classify_tone(tone_register: str) -> str:
    """Map a tone register to a one-line description."""
    descriptions = {
        TONE_FORMAL: "precise, courteous, sealed on heavy parchment",
        TONE_OFFICIAL: "bureaucratic, certified, embossed company seal",
        TONE_TERSE: "brief, clipped, no ornamentation",
        TONE_FRIENDLY: "warm, modern, sign-off with a smiley",
        TONE_FLORID: "ornamental, decorative, sealed in crimson wax",
        TONE_MONOLITHIC: "chiseled into stone, the wall is the letter",
    }
    return descriptions.get(tone_register, "unknown register")


def classify_postal_route(system: str) -> str:
    descriptions = {
        POSTAL_DIRECT: "no postal system — the wall is the letter",
        POSTAL_STD: "conventional module path + stdlib",
        POSTAL_REGISTRY: "central registry (crates.io, npm, Maven Central) + lockfile",
        POSTAL_VENDOR: "vendored dependencies, system packages, third-party",
    }
    return descriptions.get(system, "unknown route")


# ─────────────────────────────────────────────────────────────────────────────
# Rotation plumbing
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
    """Advance index, save, return the language we just finished with."""
    data = _load_rotation(config_path)
    langs = data["languages"]
    old_idx = data["current_index"]
    new_idx = (old_idx + 1) % len(langs)
    data["current_index"] = new_idx
    data["last_language"] = langs[old_idx]
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    _save_rotation(data, config_path)
    return langs[old_idx]


def get_epistolary(language: str) -> Dict[str, Any]:
    """Return the full epistolary record for a language."""
    return EPISTOLARY_DB.get(language, {})


def list_facets() -> List[str]:
    """The 12 facets of every letter."""
    return [
        "letterhead",
        "addressing",
        "salutation",
        "quill",
        "wax_seal",
        "margin_notes",
        "postscript",
        "valediction",
        "signature",
        "stationery",
        "postal_route",
        "tone",
    ]


def get_cross_comparison(facet: str) -> Dict[str, Any]:
    """Build a cross-language comparison of one facet across the rotation.

    Picks the most representative string for each facet:
      - letterhead / addressing / salutation / quill / wax_seal / margin_notes /
        postscript / valediction / signature → "style"
      - stationery      → "extension" (the printed mark)
      - postal_route    → "manager" (the post office)
      - tone            → "register" (the epistolary register)
    """
    field_map = {
        "letterhead": "style",
        "addressing": "style",
        "salutation": "style",
        "quill": "style",
        "wax_seal": "style",
        "margin_notes": "style",
        "postscript": "style",
        "valediction": "style",
        "signature": "style",
        "stationery": "extension",
        "postal_route": "manager",
        "tone": "register",
    }
    field = field_map.get(facet, "style")
    comparison: Dict[str, Any] = {"facet": facet, "languages": {}}
    for lang in ROTATION_ORDER:
        record = EPISTOLARY_DB.get(lang, {}).get(facet, {})
        style_text = record.get(field, "?")
        # Map register to friendlier text
        if facet == "tone" and style_text in (
            TONE_FORMAL, TONE_OFFICIAL, TONE_TERSE,
            TONE_FRIENDLY, TONE_FLORID, TONE_MONOLITHIC,
        ):
            style_text = classify_tone(style_text)
        comparison["languages"][lang] = {
            "style": style_text,
            "emoji": record.get("emoji", "✉️"),
        }
    return comparison


# ─────────────────────────────────────────────────────────────────────────────
# Letter generation
# ─────────────────────────────────────────────────────────────────────────────

OPENINGS = {
    TONE_FORMAL: [
        "Dear developer,",
        "Esteemed colleague,",
        "To the reader of these words,",
    ],
    TONE_OFFICIAL: [
        "Pursuant to your request,",
        "This office hereby acknowledges,",
        "In compliance with regulations,",
    ],
    TONE_TERSE: [
        "yo.",
        "Listen.",
        "Heads up.",
    ],
    TONE_FRIENDLY: [
        "Hi there!",
        "Hey friend,",
        "Greetings, fellow traveller,",
    ],
    TONE_FLORID: [
        "Most gracious recipient of this humble correspondence,",
        "It is with the greatest pleasure that I take quill in hand,",
        "Pray, give ear to these words, gentle reader,",
    ],
    TONE_MONOLITHIC: [
        "// from the wall:",
        "/* chiseled into stone: */",
        "/* the wall says: */",
    ],
}

CLOSINGS = {
    TONE_FORMAL: [
        "Yours in service,",
        "With highest regards,",
        "I remain, faithfully yours,",
    ],
    TONE_OFFICIAL: [
        "Filed and registered,",
        "By order of the compiler,",
        "This office, in due course,",
    ],
    TONE_TERSE: [
        "kthxbye.",
        "— end.",
        "ship it.",
    ],
    TONE_FRIENDLY: [
        "Cheers! 🚀",
        "Happy hacking! 💜",
        "Until next time! ✨",
    ],
    TONE_FLORID: [
        "I have the honour to remain, your most obliged servant,",
        "With profoundest courtesies and the seal of my approval,",
        "Ever yours, in wax and ribbon,",
    ],
    TONE_MONOLITHIC: [
        "// end of inscription.",
        "/* the chisel rests. */",
        "/* the wall stands. */",
    ],
}


def _open_quote(text: str) -> str:
    """Return text with leading // or /* replaced by quotation marks for display."""
    return text


def generate_letter(
    language: str,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """Generate a synthetic letter *from* the language to the developer.

    Returns a dict with:
      - language, tone_register, tone_description
      - opening, body, closing, signature_line
      - facets: list of 12 facet dicts
      - cross_comparison: {facet: {other_lang: {style, emoji}}}
    """
    record = EPISTOLARY_DB.get(language)
    if record is None:
        return {"error": f"unknown language: {language}"}

    tone_register = record["tone"]["register"]
    rng = random.Random(seed) if seed is not None else random.Random()
    opening = rng.choice(OPENINGS.get(tone_register, ["Dear developer,"]))
    closing = rng.choice(CLOSINGS.get(tone_register, ["Yours,"]))

    # Body: a short narrative stitched from the 12 facets.
    salutation = record["salutation"]
    quill = record["quill"]
    wax = record["wax_seal"]
    margin = record["margin_notes"]
    postscript = record["postscript"]
    valediction = record["valediction"]
    stationery = record["stationery"]
    postal = record["postal_route"]
    letterhead = record["letterhead"]
    addressing = record["addressing"]
    signature = record["signature"]

    body = (
        f"You find this letter on {stationery['paper'] if 'paper' in stationery else stationery['layout']}, "
        f"addressed via {addressing['style'].split('—')[0].strip()}. "
        f"It opens with {salutation['style'].split('—')[0].strip()}, "
        f"for {language} has only one proper way to greet the world. "
        f"The ink flows from a {quill['style'].split(' / ')[0].strip()}; "
        f"the seal is {wax['style'].split('—')[0].strip()}. "
        f"Marginalia are written in {margin['style'].split(',')[0].strip()}. "
        f"When the body ends, a postscript runs by {postscript['style'].split('—')[0].strip()}, "
        f"and the letter takes leave with {valediction['style'].split('—')[0].strip()}. "
        f"It is carried by {postal['manager']}, and the letterhead reads: "
        f"{letterhead['style'].split('—')[0].strip()}."
    )

    sig_idiom = signature.get("idiom", "")
    version_token = "1.0.0"
    if '"' in sig_idiom:
        try:
            version_token = sig_idiom.split('"')[-2]
        except IndexError:
            version_token = "1.0.0"
    signature_line = "—— {lang} v{ver}".format(lang=language, ver=version_token)

    # Build facet list
    facets = []
    for facet_name in list_facets():
        f = record[facet_name]
        facets.append({
            "facet": facet_name,
            "emoji": f.get("emoji", "✉️"),
            "style": f.get("style", "?"),
            "mechanism": f.get("mechanism", f.get("system", f.get("extension", ""))),
            "idiom": f.get("idiom", ""),
            "key_traits": f.get("key_traits", []),
        })

    # Cross-comparison for every facet
    cross: Dict[str, Any] = {}
    for facet_name in list_facets():
        cross[facet_name] = get_cross_comparison(facet_name)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": language,
        "tone_register": tone_register,
        "tone_description": classify_tone(tone_register),
        "opening": opening,
        "body": body,
        "closing": closing,
        "signature_line": signature_line,
        "facets": facets,
        "cross_comparison": cross,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Report generation
# ─────────────────────────────────────────────────────────────────────────────

def generate_correspondent_report(
    rotate: bool = True,
    config_path: Optional[str] = None,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """Generate a full correspondent report for the current rotation language.

    Args:
        rotate: advance the rotation index after generating
        config_path: optional path to language_rotation.json
        seed: optional RNG seed for deterministic openings/closings

    Returns:
        full report dict (includes letter + metadata + rotation info)
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

    letter = generate_letter(current_language, seed=seed)
    record = EPISTOLARY_DB.get(current_language, {})

    # The "address" of the recipient
    salutation_style = record.get("salutation", {}).get("style", "?")

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": current_language,
        "current_index": old_idx,
        "new_index": new_idx if rotate else None,
        "rotated": rotate,
        "salutation_style": salutation_style,
        "letter": letter,
        "facets": letter["facets"],
        "cross_comparison": letter["cross_comparison"],
        "rotation_order": ROTATION_ORDER,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Pretty-printing
# ─────────────────────────────────────────────────────────────────────────────

FACET_LABELS = {
    "letterhead": "LETTERHEAD",
    "addressing": "ADDRESSING",
    "salutation": "SALUTATION",
    "quill": "QUILL",
    "wax_seal": "WAX SEAL",
    "margin_notes": "MARGIN NOTES",
    "postscript": "POSTSCRIPT",
    "valediction": "VALEDICTION",
    "signature": "SIGNATURE",
    "stationery": "STATIONERY",
    "postal_route": "POSTAL ROUTE",
    "tone": "TONE",
}


def _wrap(text: str, width: int, indent: str = "║  ") -> List[str]:
    """Wrap text to width characters, prefixing each line with indent."""
    words = text.split()
    lines: List[str] = []
    current = ""
    for word in words:
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= width:
            current += " " + word
        else:
            lines.append(indent + current)
            current = word
    if current:
        lines.append(indent + current)
    return lines


def format_correspondent_report(m: Dict[str, Any]) -> str:
    """Format a correspondent report as a human-readable letter."""
    lang = m["language"]
    letter = m["letter"]
    line_width = 66

    out: List[str] = []
    out.append("╔" + "═" * line_width + "╗")
    out.append("║  ✉️  POLYGLOT CORRESPONDENT — Epistolary Engine                  ║")
    out.append("╠" + "═" * line_width + "╣")
    out.append(f"║  Language      : {lang:<48}║")
    out.append(f"║  Tone          : {letter['tone_register']:<48}║")
    out.append(f"║  Tone (in word): {letter['tone_description']:<48}║")
    out.append("╠" + "═" * line_width + "╣")
    out.append("║  THE LETTER                                                     ║")
    out.append("╠" + "═" * line_width + "╣")
    out += _wrap(letter["opening"], line_width - 4)
    out.append("║" + " " * line_width + "║")
    out += _wrap(letter["body"], line_width - 4)
    out.append("║" + " " * line_width + "║")
    out += _wrap(letter["closing"], line_width - 4)
    out.append("║" + " " * line_width + "║")
    out += _wrap(letter["signature_line"], line_width - 4)
    out.append("╠" + "═" * line_width + "╣")
    out.append("║  THE TWELVE FACETS                                              ║")
    out.append("╠" + "═" * line_width + "╣")

    for facet in letter["facets"]:
        label = FACET_LABELS.get(facet["facet"], facet["facet"].upper())
        header = f"{facet['emoji']}  {label}"
        out.append(f"║  {header:<{line_width - 2}}║")
        for trait in facet["key_traits"][:3]:
            out += _wrap("• " + trait, line_width - 6, indent="║    ")
        if facet["idiom"]:
            short_idiom = facet["idiom"].split("\n")[0][:60]
            if len(facet["idiom"].split("\n")[0]) > 60:
                short_idiom += "…"
            out += _wrap("  ⌨  " + short_idiom, line_width - 6, indent="║    ")

    out.append("╠" + "═" * line_width + "╣")
    out.append("║  CROSS-LANGUAGE COMPARISON (one facet at a time)                 ║")
    out.append("╠" + "═" * line_width + "╣")

    for facet_name, comp in m["cross_comparison"].items():
        label = FACET_LABELS.get(facet_name, facet_name.upper())
        out.append(f"║  ── {label} " + "─" * (line_width - 4 - len(label) - 4) + "║")
        for other_lang, info in comp["languages"].items():
            marker = " ▸ " if other_lang == lang else "   "
            style_short = info["style"][:54]
            line = f"║{marker}{other_lang:<10} {style_short}"
            pad = line_width - len(line) + 1  # +1 because the ║ is in `line` but not in width
            out.append(line + " " * max(1, pad) + "║")

    out.append("╚" + "═" * line_width + "╝")
    return "\n".join(out)


# ─────────────────────────────────────────────────────────────────────────────
# Test runner
# ─────────────────────────────────────────────────────────────────────────────

def run_tests() -> None:
    """Run all tests and exit."""
    import pytest
    import sys
    sys.exit(pytest.main([str(_MODULE_DIR / "tests"), "-v"]))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        report = generate_correspondent_report()
        print(format_correspondent_report(report))
    else:
        print(f"Polyglot Correspondent v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_correspondent --test    # Run tests")
        print("  python -m polyglot_correspondent --report  # Generate a letter")
