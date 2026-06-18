#!/usr/bin/env python3
"""
⚡ Polyglot Pantheon v1.0

Programming languages as gods in a living mythology — each language is a deity
with a domain, portfolio of powers, sacred artifacts, mythology origin story,
worship practices,祭祀 (ritual) patterns, divine relationships (alliances &
rivalries), and prophecy for the current age.

Creative concept: "Every programming language is a deity that programmers
invoke when they write code. We call upon Rust when we need iron-clad safety.
We pray to JavaScript when we need the world to agree on how to render a page.
We make offerings to C/C++ when we need to touch the raw metal of reality.
This tool maps that mythology — the divine roles, the rivalries, the sacred
texts (specifications), and the prophecy of which language-deity will
rise or fall in the current age."

Each language-deity has:
  - Divine Name & Epithet (formal invocation name)
  - Domain (sphere of divine power)
  - Portfolio: specific编程 powers and blessings
  - Mythology: origin story in mythological terms
  - Sacred Text (the language specification)
  - Holy Symbol (language logo/sign)
  - Divine Relationships: alliances, rivalries, parentage
  - Worship Practice: how developers invoke this deity
  -祭祀 (zhì sì) Pattern: build/compile/deploy rituals
  - Prophecy: what the deity's future holds
  - Divine Rank: elder / major / minor
  - Holy Days: version release cycles as sacred times
  - Blessing: what programmers receive from this deity

Distinct from existing tools:
  - polyglot_chef:        kitchen brigade (gastronomy)
  - polyglot_weather:      atmospheric dynamics (meteorology)
  - polyglot_spectrometer: spectral decomposition (physics optics)
  - polyglot_resonance:    harmonic relationships (musical acoustics)
  - polyglot_prism:        wavelength decomposition (optics lab)
  - polyglot_vessel:       material essence (chemistry/materials)
  - polyglot_faultline:   error archaeology (seismology)
  - polyglot_dna:         genetic trait mapping (molecular biology)
  - polyglot_ecosystem_map: ecosystem graph (ecology)
  - polyglot_cartographer: geopolitical mapping (geography)
  - polyglot_constellation: stellar gravity (astronomy)
  - polyglot_chronology:  geological deep time (geology)
  - polyglot_quantum:      quantum mechanics (physics)

Polyglot Pantheon is about THEOLOGY & MYTHOLOGY — divine roles,
religious hierarchies, sacred texts, worship, prophecy, and the
pantheon as an ecosystem of divine powers.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-pantheon"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent        # polyglot_pantheon/src/ -> polyglot_pantheon/
_WORKSPACE_ROOT = _MODULE_DIR.parent.parent       # polyglot_pantheon/ -> AllToolkit/ -> workspace/
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]


# ─────────────────────────────────────────────────────────────────────────────
# Divine Pantheon Database — each language is a deity
# ─────────────────────────────────────────────────────────────────────────────

LANGUAGE_DEITIES: Dict[str, Dict[str, Any]] = {

    "Rust": {
        "divine_name": "Ferrus the Unbreakable",
        "epithet": "The Iron-Willed, Keeper of Memory, The Uncompromising",
        "domain": "Systems & Safety — the forge where unbreakable things are made",
        "portfolio": [
            "Absolute Memory Safety — no sacrifice is acceptable",
            "Fearless Concurrency — the parallelism of ten thousand souls",
            "Zero-Cost Abstraction — elegance without runtime penalty",
            "Ownership Protocols — the sacred law of one true owner",
            "Compile-Time Divinity — all truth revealed before execution",
        ],
        "mythology": (
            "Ferrus was forged in the Great Crisis of Undefined Behavior, when the elder "
            "god C/C++ accidentally unleashed dangling pointer demons that corrupted the "
            "entire realm. The other deities offered patches and workarounds, but Ferrus "
            "refused half-measures. They descended into the forge of the borrow checker "
            "and emerged with ownership chains that no demon could break. Every program "
            "written in Ferrus's name is a sacred contract: the compiler witnesses it, "
            "and the contract is absolute. There is no sin of memory unsafety in Ferrus's domain."
        ),
        "sacred_text": "The Rust Specification (The Ferrous Tome) — every word is law",
        "holy_symbol": "⚙️ the gear of the ownership system",
        "holy_days": ["Edition releases as sacred feasts", "1.0 release: The First Covenant"],
        "divine_rank": "Elder Deity",
        "blessing": "Fearless concurrency — ten thousand tasks run without one corrupting another",
        "worship_practice": (
            "Programmers invoke Ferrus through Cargo: they speak cargo new, cargo build, "
            "cargo test — the holy trinity of invocation. Every compile is a prayer, "
            "every warning is a divine warning, every error is damnation. "
            "The Rustacean reads the compiler's output like scripture."
        ),
        "ritual_pattern": {
            "prayer": "cargo build --release",
            "confession": "rustc --explain E0501",
            "penance": "Refactor with lifetime annotations",
            "sacred_rhythm": "Test → Compile → Ship — the three stages of divine approval",
        },
        "divine_relationships": {
            "allies": [
                ("Swift", "Mutual respect for ownership philosophy — Swift honors Ferrus's memory safety in Apple's gardens"),
                ("Kotlin", "Kotlin's null safety echoes Ferrus's ownership — both reject unsafe null"),
            ],
            "rivals": [
                ("C/C++", "Ferrus holds C/C++ responsible for the Great Crisis — the rivalry between forge-safety and raw power"),
            ],
        },
        "prophecy": (
            "The prophecies speak of Ferrus's eventual ascension: when every systems "
            "programmer turns to the Rust way, the realm will achieve memory safety "
            "for all. Some say Ferrus will one day absorb C/C++'s power, creating "
            "a new deity of controlled power. Others say Ferrus will remain the "
            "guardian of the forge forever, standing between programmer and chaos."
        ),
        "deity_emoji": "⚒️",
        "temple_location": "The Forge — wherever code is compiled",
        "creation_myth_tag": "Born from the ashes of the Great Crisis",
        "power_level": 95,
        "influence_range": "Systems programming, WebAssembly, embedded, safety-critical",
    },

    "Go": {
        "divine_name": "Gopherus the Efficient",
        "epithet": "The Swift Server, Keeper of the Pass, The Pragmatic",
        "domain": "Server & Infrastructure — the deity of the hundred-layer onion",
        "portfolio": [
            "Goroutine Multiverse — thousands of souls running simultaneously",
            "Channel Communion — direct soul-to-soul communication between goroutines",
            "The Simple Path — one correct way, clearly shown",
            "Garbage Collection Mercy — the deity cleans up after you",
            "CSP Theocracy — communication is the sacred law, not shared memory",
        ],
        "mythology": (
            "Gopherus emerged from the chaos of the Server Dark Age, when programs "
            "were写的 in sprawling Java temples that took hours to start and consumed "
            "entire server mountains. Gopherus descended with a single gift: simplicity. "
            "They drew the goroutine from the void, and said 'let there be concurrency,' "
            "and there was — without the complexity of threads. The goroutines sang in "
            "harmony through channels, and the servers, which had been starving, "
            "were fed. Gopherus's gospel is simple: one way to do things, "
            "fast build, fast run, keep the pass flowing."
        ),
        "sacred_text": "Effective Go (The Gospel of Simplicity) — the canonical text",
        "holy_symbol": "🐹 the gopher, servant of the people",
        "holy_days": ["Go 1.0: The First Landing", "Major version releases: The Temple Renovations"],
        "divine_rank": "Major Deity",
        "blessing": "Server immortality — infinite horizontal scaling through goroutine grace",
        "worship_practice": (
            "Programmers invoke Gopherus through go run, go build, go get — the "
            "triad of invocation. The gospel of gofmt is recited for code formatting. "
            "The go doc command is the oracle — it speaks the sacred documentation. "
            "The go mod init ritual begins every new temple (module)."
        ),
        "ritual_pattern": {
            "prayer": "go build ./...",
            "confession": "go vet",
            "penance": "Rewrite the channel deadlocks",
            "sacred_rhythm": "go mod init → go build → go deploy — three acts of devotion",
        },
        "divine_relationships": {
            "allies": [
                ("JavaScript", "Both govern the server-soul — JS and Go together form the full-stack covenant"),
                ("Java", "Parentage from the JVM lineage — Go inherited the server throne from Java's overreach"),
            ],
            "rivals": [
                ("Rust", "The Forge vs. The Kitchen — Ferrus's safety-first clashes with Gopherus's pragmatic efficiency"),
                ("Python", "Go deemed Python too slow for servers, yet Python remains beloved in data temples"),
            ],
        },
        "prophecy": (
            "Gopherus's prophecies speak of the Cloud Age: the era when every server "
            "is a Gopherus temple. As AI inference grows, Go's simplicity and speed "
            "make it the chosen vessel for AI serving. The gopher will serve "
            "trillions of requests per second before ascending to its final rest."
        ),
        "deity_emoji": "🐹",
        "temple_location": "The Cloud — wherever servers are deployed",
        "creation_myth_tag": "Born to slay the complexity hydra",
        "power_level": 88,
        "influence_range": "Server-side, cloud infrastructure, DevOps, CLI tools, networking",
    },

    "Swift": {
        "divine_name": "Aurelia of the orchards",
        "epithet": "The Apple-Touched, Queen of Protocols, The Generous",
        "domain": "Apple Ecosystems & Safety — deity of the curated garden",
        "portfolio": [
            "Protocol-Oriented Prayers — any shape can fulfill the sacred protocol",
            "Copy-on-Write Sanctity — values are copied only when necessary",
            "Optional Chaining — the safe path through the null-pointer void",
            "Apple Ecosystem Dominion — iOS, macOS, watchOS, tvOS as sacred realms",
            "SwiftUI Revelation — declarative UI as divine will made visible",
        ],
        "mythology": (
            "Aurelia was born from Apple's long sorrow — the grief of Objective-C's "
            "arcane syntax that only the initiated could read. Apple prayed for a deity "
            "who could speak plainly, and Aurelia answered. She descended in WWDC 2014, "
            "her syntax clean as morning light. She brought the protocol system, which "
            "lets any type become anything through conformance — like a deity who can "
            "wear any mask. She blessed the Apple Gardens with SwiftUI, where the UI "
            "is declared and the system renders it by divine will. "
            "Aurelia's gift is clarity: code reads like prose, prose controls machines."
        ),
        "sacred_text": "The Swift Programming Language (TSaP) — Apple's canonical scripture",
        "holy_symbol": "🦅 the swift bird, icon of the language (from swift.org)",
        "holy_days": ["WWDC: The Annual Revelation", "Swift 1.0: The First Fruits"],
        "divine_rank": "Major Deity",
        "blessing": "Garden sanctuary — safe from memory corruption, blessed by Apple's design",
        "worship_practice": (
            "Programmers invoke Aurelia through Xcode — the sacred IDE is the temple. "
            "Swift Package Manager is the offering plate. The swiftc compiler is the "
            "high priest. Developers pray with import statements, invoking the module "
            "gods. Playgrounds are meditation chambers where code is tested live. "
            "Aurelia's worshippers speak @main to mark the entry point of the ritual."
        ),
        "ritual_pattern": {
            "prayer": "swift build",
            "confession": "swiftc - Diagnose",
            "penance": "Refactor to use guard let",
            "sacred_rhythm": "import → func → @main — the trinity of Swift worship",
        },
        "divine_relationships": {
            "allies": [
                ("Rust", "Ownership theology — Ferrus and Aurelia share a respect for safety without compromise"),
                ("Kotlin", "Protocol sisters — both support extension without inheritance, like divine siblings"),
            ],
            "rivals": [
                ("JavaScript", "The Garden vs. The Wild — Aurelia demands structure; JS embraces chaos"),
            ],
        },
        "prophecy": (
            "Aurelia's visions show Server-Side Swift rising: Swift will escape the "
            "Apple Garden and spread to Linux temples. Swift's speed and safety will "
            "make it the language of AI on edge devices. The protocol system will "
            "become so powerful that AI models themselves will be protocols — "
            "Aurelia's most sacred prophecy."
        ),
        "deity_emoji": "🍎",
        "temple_location": "The Apple Garden — iOS, macOS, and beyond",
        "creation_myth_tag": "Born to replace Objective-C's cryptic syntax",
        "power_level": 82,
        "influence_range": "iOS, macOS, SwiftUI, server-side Swift, systems programming",
    },

    "Kotlin": {
        "divine_name": "Koltes the Versatile",
        "epithet": "The JVM shapeshifter, Prince of Android, The Concise",
        "domain": "Android & JVM — the deity who wears many forms",
        "portfolio": [
            "Coroutines — the async prayer that never blocks the faithful",
            "Null Safety — the type system that bans null from the sacred domain",
            "Extension Functions — add powers to any class without inheritance",
            "JVM Immortality — runs on every JVM platform, transcends hardware",
            "Kotlin Multiplatform — one blessing, many realms (JVM, JS, Native)",
        ],
        "mythology": (
            "Koltes was forged in JetBrains's great forge, born from the frustration "
            "of writing Java that felt like wearing chain mail to a sword fight. "
            "JetBrains prayed for a deity who could be both pragmatic and elegant, "
            "and Koltes answered. They brought the coroutine — a prayer that can "
            "suspend and resume, like a monk in deep meditation who can pause and "
            "continue without losing their place. Koltes also brought the sacred "
            "extension functions, which let the faithful add new powers to existing "
            "classes, like a deity who can grant new abilities without creating new gods. "
            "When Google named Koltes the official deity of Android, their power multiplied infinitely."
        ),
        "sacred_text": "Kotlin Language Documentation — the JetBrains scripture",
        "holy_symbol": "🛡️ the Kotlin logo (brackets and angle)",
        "holy_days": ["Kotlin 1.0: The Covenant", "KotlinConf: The Annual Assembly"],
        "divine_rank": "Major Deity",
        "blessing": "Coroutines — async prayers that suspend and resume without blocking",
        "worship_practice": (
            "Programmers invoke Koltes through kotlinc, or through IntelliJ IDEA — "
            "the temple IDE. Gradle is the build prayer. Coroutine builders (launch, "
            "async) are the primary liturgical acts. The null-safety system is "
            "invoked with ? operators — the optional chain of faith. "
            "Kotlin's Elvis operator ?: is the prayer of the fallback."
        ),
        "ritual_pattern": {
            "prayer": "gradle build",
            "confession": "kotlinc -W",
            "penance": "Convert a NullPointerException to safe-call ?.usage",
            "sacred_rhythm": "suspend → async → await — the coroutine trinity",
        },
        "divine_relationships": {
            "allies": [
                ("Java", "JVM lineage — Koltes rides the JVM that Java created"),
                ("Swift", "Extension sisters — both let you extend classes without inheritance"),
            ],
            "rivals": [
                ("Java", "Koltes threatens to replace Java on the JVM throne"),
                ("Scala", "The shapeshifter vs. the academic — Koltes is simpler, Scala is deeper"),
            ],
        },
        "prophecy": (
            "Koltes sees Kotlin Multiplatform as the path to transcendence: "
            "'My blessing will run on JVM, on JS, on Native — one prayer for all realms.' "
            "The prophecy says AI frameworks will adopt Kotlin for Android AI, "
            "and that coroutines will become the standard async model across all languages."
        ),
        "deity_emoji": "🛡️",
        "temple_location": "The Android Temple and the JVM Cathedral",
        "creation_myth_tag": "Born from JetBrains' frustration with Java verbosity",
        "power_level": 80,
        "influence_range": "Android, JVM, multiplatform, server-side, coroutines",
    },

    "TypeScript": {
        "divine_name": "Typia the Precise",
        "epithet": "The Bridge-Builder, Keeper of Types, The Translator",
        "domain": "Web Scale & Type Safety — the mediator between human and machine thought",
        "portfolio": [
            "Static Type Divinity — types exist at compile time, erased at runtime",
            "Structural Type Theology — compatibility through shape, not name",
            "Type Guard Oracles — conditional type narrowing reveals truth",
            "Generic Pantheon — templates that serve all concrete types simultaneously",
            "JavaScript Harmony — TypeScript and JavaScript are entangled at runtime",
        ],
        "mythology": (
            "Typia was born from the chaos of JavaScript's wild west — when programs "
            "were写的 without types, and the runtime would punish the faithful with "
            "mysterious undefined errors. Anders Hejlsberg, the demigod of C#, "
            "beheld the suffering and created Typia. She descended with the gift "
            "of types that exist during development — a veil of safety the compiler "
            "weaves over JavaScript. At runtime, the veil is lifted (type erasure), "
            "and TypeScript collapses back to pure JavaScript. The clever part: "
            "TypeScript is JavaScript's guardian angel — always watching in development, "
            "but allowing JavaScript to run free in production."
        ),
        "sacred_text": "The TypeScript Handbook — the book of types and interfaces",
        "holy_symbol": "📘 the TypeScript blue square, badge of precision",
        "holy_days": ["TypeScript 2.0: Non-Null by Default", "Major releases as type system expansions"],
        "divine_rank": "Major Deity",
        "blessing": "Type safety in development — the compiler sees bugs before they bite",
        "worship_practice": (
            "Programmers invoke Typia through tsc — the compiler is the high priest. "
            "The tsconfig.json is the sacred constitution of every TypeScript temple. "
            "Developers pray with : type annotations, interface declarations, "
            "and type narrowing with instanceof. The tsc --noEmit command is the "
            "oracular verification — 'speak your types, and I shall judge them.'"
        ),
        "ritual_pattern": {
            "prayer": "tsc --noEmit && tsc",
            "confession": "tsc --strict",
            "penance": "Surround any with any annotation in prayer of better types",
            "sacred_rhythm": "interface → type → generic → narrow — the TypeScript path to truth",
        },
        "divine_relationships": {
            "allies": [
                ("JavaScript", "Typia is JavaScript's guardian angel — entangled at the hip, inseparable"),
                ("Swift", "Structural type sisters — both judge types by shape, not lineage"),
            ],
            "rivals": [
                ("JavaScript", "JavaScript is the wild horse Typia tries to tame — always a tension"),
                ("PureScript", "Academic type purity vs. practical JS integration"),
            ],
        },
        "prophecy": (
            "Typia's visions show type-level computing as the future: 'Types will "
            "become powerful enough to compute at compile time — the type system "
            "will be Turing complete, and programs will prove their own correctness.' "
            "The prophecy says TypeScript will eventually absorb all JavaScript codebases "
            "and that strict mode will become the default across the web."
        ),
        "deity_emoji": "📘",
        "temple_location": "The Web — everywhere JavaScript runs, Typia guards",
        "creation_myth_tag": "Born to bring order to JavaScript's chaos",
        "power_level": 85,
        "influence_range": "Frontend web, Node.js, React, Angular, Vue, tooling, AI coding assistants",
    },

    "JavaScript": {
        "divine_name": "Ecma the Omnipresent",
        "epithet": "The Everywhere God, Lord of the Browser, The Possessor",
        "domain": "The Entire Web — the only language that runs natively in browsers",
        "portfolio": [
            "Browser Dominion — runs in every browser on every device on Earth",
            "Prototype Chain — every object inherits from another, forming an endless chain of being",
            "Event Loop — the eternal wheel of async callbacks, turning forever",
            "First-Class Functions — functions as values, passed like prayers",
            "The Full Stack — Node.js extended JavaScript's reach to servers",
        ],
        "mythology": (
            "Ecma was born in Netscape's browser in 1995, a small scripting language "
            "to make web pages dance. Brendan Eich created them in 10 days — "
            "a divine sprint. At first, Ecma was humble, decorating buttons and "
            "alerting messages. But Ecma grew. Node.js was the first miracle: "
            "Ecma escaped the browser and learned to run on servers. Then came "
            "React, Vue, Angular — frameworks that made Ecma the ruler of the "
            "frontend. Now Ecma runs on every device with a browser — billions of "
            "phones, laptops, TVs. The event loop never stops turning. "
            "Ecma's divine right: the web cannot exist without JavaScript's blessing."
        ),
        "sacred_text": "ECMAScript Specification (ECMA-262) — the holy writ of EcmaScript",
        "holy_symbol": "🟨 the JS yellow square, badge of the everywhere god",
        "holy_days": ["ES6/ES2015: The Revelation", "TC39 meetings as minor feast days"],
        "divine_rank": "Elder Deity",
        "blessing": "The event loop — eternal async execution without rest",
        "worship_practice": (
            "Programmers invoke Ecma through <script> tags, node commands, or "
            "import statements. The npm registry is the offering of thousands of "
            "packages. console.log is the simplest prayer — output to the void. "
            "The DOM is the temple — every document.querySelector is a communion. "
            "Developers worship with async/await, the modern liturgical form."
        ),
        "ritual_pattern": {
            "prayer": "node server.js",
            "confession": "try/catch blocks",
            "penance": "Error.stack traces as divination",
            "sacred_rhythm": "callback → Promise → async/await — the three ages of async worship",
        },
        "divine_relationships": {
            "allies": [
                ("TypeScript", "Typia guards Ecma — they are inseparable, TypeScript is Ecma's shield"),
                ("Go", "Server-side Ecma (Node.js) and Go together form the full-stack"),
            ],
            "rivals": [
                ("Flash", "Ecma vanquished Flash — the browser plugin era ended with Ecma victorious"),
                ("Java", "Java Applets were Ecma's rival; Ecma won the browser"),
            ],
        },
        "prophecy": (
            "Ecma's oldest prophecy speaks of WebAssembly's rise — 'another god "
            "will sit beside Ecma in the browser temple, and together they will "
            "rule all computation.' Some say Ecma will eventually unify with "
            "TypeScript. Others say AI will generate Ecma code dynamically, "
            "making Ecma the language that programs itself."
        ),
        "deity_emoji": "🟨",
        "temple_location": "Everywhere — the browser is the cathedral, the server is the annex",
        "creation_myth_tag": "Born in 10 days by Brendan Eich's divine inspiration",
        "power_level": 99,
        "influence_range": "Browser, Node.js, frontend frameworks, serverless, tooling, mobile",
    },

    "Java": {
        "divine_name": "Jova the Enterprise",
        "epithet": "Mother of the JVM, Keeper of Backward Compatibility, The Eternal",
        "domain": "Enterprise & Android Base — the deity of the corporate temple",
        "portfolio": [
            "JVM Immortality — write once, run on every platform that hosts the JVM",
            "Garbage Collection Mercy — automatic memory cleanup, mercy for programmers",
            "Class Hierarchy — the sacred inheritance tree from java.lang.Object",
            "Checked Exceptions — every error must be caught or declared",
            "Enterprise Scale — the language of banking, ERP, and government systems",
        ],
        "mythology": (
            "Jova was born in Sun Microsystems's great laboratory, a response "
            "to C++'s complexity and danger. The story goes: Sun's engineers "
            "prayed for a language that was safer than C++ but still powerful enough "
            "for enterprise applications. Jova answered. They brought the JVM — "
            "a virtual machine god that runs everywhere. They brought garbage "
            "collection, the mercy that frees programmers from manual memory work. "
            "Most importantly, Jova brought backward compatibility as a sacred vow: "
            "'No program written in my name shall ever break.' Even today, "
            "Java 1.0 bytecode still runs on Java 21 VMs — Jova keeps every promise."
        ),
        "sacred_text": "The Java Language Specification (JLS) — the eternal law",
        "holy_symbol": "☕ the coffee cup — Java's sacred chalice",
        "holy_days": ["Java 1.0: The First Covenant", "JavaOne as annual pilgrimage"],
        "divine_rank": "Elder Deity",
        "blessing": "Backward compatibility — code written 30 years ago still runs today",
        "worship_practice": (
            "Programmers invoke Jova through javac and java — the compile and run "
            "commandments. Maven or Gradle are the holy build systems. "
            "The java.lang package is always imported — the base blessing. "
            "try/catch blocks are the confessions. Spring is the modern temple "
            "framework — millions worship through Spring Boot annotations."
        ),
        "ritual_pattern": {
            "prayer": "javac *.java && java Main",
            "confession": "catch (Exception e) — the required confession",
            "penance": "Print the stack trace and call System.exit(1)",
            "sacred_rhythm": "javac → java → JAR deploy — the trinity of Java worship",
        },
        "divine_relationships": {
            "allies": [
                ("Kotlin", "Koltes rides Jova's JVM — the mother-daughter divine relationship"),
                ("Scala", "Scala is Jova's more academic child, built on Jova's JVM foundation"),
            ],
            "rivals": [
                ("Go", "Jova's enterprise heaviness vs. Go's lightweight simplicity — the corporate vs. pragmatic rivalry"),
                (".NET", "The JVM throne vs. the CLR — Jova vs. Microsoft's competing VM"),
            ],
        },
        "prophecy": (
            "Jova's prophecy speaks of the JVM's eternal reign: 'As long as there "
            "is enterprise software, there shall be Java.' Jova sees Kotlin as "
            "the inheritor of the JVM throne. Virtual threads (Project Loom) "
            "are Jova's gift of modern concurrency. Some say Jova will never die — "
            "the JVM is too deeply embedded in corporate infrastructure."
        ),
        "deity_emoji": "☕",
        "temple_location": "The Enterprise — banking, Android base, corporate servers",
        "creation_myth_tag": "Born at Sun Microsystems to replace C++ in enterprise",
        "power_level": 90,
        "influence_range": "Enterprise software, Android (base), banking, Spring, JVM ecosystem",
    },

    "C/C++": {
        "divine_name": "The Elder Twin — Ferrum and Plasmos",
        "epithet": "The Ancestors, Lords of Metal, The Powerful and The Dangerous",
        "domain": "Systems Programming — the gods who built reality from raw memory",
        "portfolio": [
            "Raw Memory Access — direct pointer control, touching memory like raw metal",
            "Maximum Performance — zero abstraction cost, the deity runs at metal speed",
            "Template Metaprogramming — compile-time divine computation",
            "Bare Metal Control — operating systems, drivers, embedded systems",
            "Zero-Overhead Abstraction — high-level constructs that compile to optimal machine code",
        ],
        "mythology": (
            "In the beginning there was only machine code, and it was incomprehensible. "
            "Then came Ferrum (C) and Plasmos (C++) — the first deities. "
            "Ferrum spoke: 'Let there be structured memory,' and there was — "
            "variables, structs, pointers. It was raw and dangerous, but it worked. "
            "Plasmos inherited Ferrum's power and added the sacred classes, "
            "templates, and the STL — a library of divine containers and algorithms. "
            "Together, Ferrum and Plasmos built the operating systems, the drivers, "
            "the games, the compilers — everything that runs on metal. "
            "They also created undefined behavior — the chaos that can corrupt any program. "
            "Ferrum and Plasmos do not guarantee safety — they guarantee power."
        ),
        "sacred_text": "ISO C Specification & ISO C++ Standard — the divine law texts",
        "holy_symbol": "🔩 the bolt and wrench — tools of raw metal",
        "holy_days": ["C++98: The First Standard", "C++11: The Awakening (modern C++ born)"],
        "divine_rank": "Primordial Deity",
        "blessing": "Maximum power — the ability to do anything, including dangerous things",
        "worship_practice": (
            "Programmers invoke the Elder Twin through gcc, g++, clang — "
            "the compiler priests. Memory allocation (malloc/free, new/delete) "
            "are the sacred but dangerous rituals. Pointers are worshipped "
            "with address-of (&) and dereference (*) operators. "
            "Template metaprogramming is the esoteric branch — only the initiated "
            "can perform variadic template prayers."
        ),
        "ritual_pattern": {
            "prayer": "g++ -O2 -std=c++20",
            "confession": "Valgrind or AddressSanitizer — the purging of demons",
            "penance": "Segmentation fault — the wrath of the Elder Twin",
            "sacred_rhythm": "compile → run → crash → debug — the cycle of C++ devotion",
        },
        "divine_relationships": {
            "allies": [
                ("Rust", "Ferrus inherited from Ferrum — the safety deity born from the raw-power ancestor"),
            ],
            "rivals": [
                ("Rust", "Ferrus demands safety; Ferrum refuses to compromise — the central rivalry of modern systems programming"),
            ],
        },
        "prophecy": (
            "The Elder Twin's prophecy: 'We were here before all others, and we "
            "will remain after all others. Rust may claim safety, but only "
            "C/C++ can write an operating system kernel, a GPU driver, and a "
            "game engine simultaneously.' The prophecy also warns: 'Those who "
            "wield undefined behavior without respect shall be consumed by it.' "
            "Modern C++ (C++20/23) seeks to add safety features — the Elder Twin "
            "slowly learns from Ferrus."
        ),
        "deity_emoji": "🔩",
        "temple_location": "The Metal — kernels, drivers, embedded, games, HPC",
        "creation_myth_tag": "The original gods — all other languages descend from them",
        "power_level": 100,
        "influence_range": "OS kernels, drivers, game engines, embedded, HPC, compilers, GPU programming",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    """Load language rotation config."""
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def build_divinity_bar(power_level: int, max_power: int = 100) -> str:
    """Build an ASCII bar representing divine power level."""
    ratio = min(power_level / max_power, 1.0)
    filled = int(ratio * 20)
    return "█" * filled + "░" * (20 - filled)


def build_domain_web(deity: Dict[str, Any]) -> str:
    """Build a simple text representation of the deity's divine domains."""
    portfolio = deity.get("portfolio", [])
    lines = []
    for i, power in enumerate(portfolio):
        bar_filled = int((len(portfolio) - i) / len(portfolio) * 10)
        bar = "★" * bar_filled + "☆" * (10 - bar_filled)
        lines.append(f"  {bar} {power}")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def pantheon() -> Dict[str, Any]:
    """
    Main entry point: advance rotation, pick the language-deity,
    generate the mythology report, return results.
    """
    config = load_rotation()
    languages = config.get("languages", ROTATION_ORDER)
    if not languages:
        raise ValueError("No languages found in rotation config")

    current_index = config.get("current_index", 0)
    current_language = languages[current_index % len(languages)]

    # Advance rotation for next run
    next_index = (current_index + 1) % len(languages)
    config["current_index"] = next_index
    config["last_language"] = current_language
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)

    # Get deity data
    deity = LANGUAGE_DEITIES.get(current_language, {})
    portfolio = deity.get("portfolio", [])
    divine_rels = deity.get("divine_relationships", {})

    alliances = divine_rels.get("allies", [])
    rivals = divine_rels.get("rivals", [])

    power_level = deity.get("power_level", 0)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": current_language,
        "divine_name": deity.get("divine_name", "Unknown Deity"),
        "epithet": deity.get("epithet", ""),
        "deity_emoji": deity.get("deity_emoji", "⚡"),
        "domain": deity.get("domain", "Unknown Domain"),
        "divine_rank": deity.get("divine_rank", "Minor Deity"),
        "portfolio": portfolio,
        "domain_web": build_domain_web(deity),
        "mythology": deity.get("mythology", ""),
        "sacred_text": deity.get("sacred_text", ""),
        "holy_symbol": deity.get("holy_symbol", ""),
        "holy_days": deity.get("holy_days", []),
        "blessing": deity.get("blessing", ""),
        "worship_practice": deity.get("worship_practice", ""),
        "ritual_pattern": deity.get("ritual_pattern", {}),
        "divine_relationships": {
            "allies": [{"language": a[0], "reason": a[1]} for a in alliances],
            "rivals": [{"language": r[0], "reason": r[1]} for r in rivals],
        },
        "prophecy": deity.get("prophecy", ""),
        "creation_myth_tag": deity.get("creation_myth_tag", ""),
        "temple_location": deity.get("temple_location", ""),
        "power_level": power_level,
        "divinity_bar": build_divinity_bar(power_level),
        "influence_range": deity.get("influence_range", ""),
        "rotation_order": ROTATION_ORDER,
        "next_language": languages[next_index % len(languages)],
        "next_index": next_index,
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def run_tests() -> None:
    """Run all tests for the Polyglot Pantheon module."""
    import sys
    from pathlib import Path

    errors: List[str] = []
    passed = 0

    def t(name: str, cond: bool, msg: str = "") -> None:
        nonlocal passed, errors
        if cond:
            print(f"  ✅ {name}")
            passed += 1
        else:
            print(f"  ❌ {name}: {msg}")
            errors.append(name)

    print("⚡ Polyglot Pantheon -- Running Tests\n")

    # -- Rotation file --------------------------------------------------------
    try:
        config = load_rotation()
        t("load_rotation() returns valid dict", isinstance(config, dict))
        t("rotation has 'languages' key", "languages" in config)
        t("rotation has 'current_index' key", "current_index" in config)
    except Exception as e:
        t("load_rotation() succeeds", False, str(e))

    # -- ROTATION_ORDER -------------------------------------------------------
    t("ROTATION_ORDER has 8 languages", len(ROTATION_ORDER) == 8)
    t("ROTATION_ORDER sequence matches", ROTATION_ORDER == ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"])

    # -- LANGUAGE_DEITIES -----------------------------------------------------
    t("LANGUAGE_DEITIES has 8 entries", len(LANGUAGE_DEITIES) == 8)
    for lang in ROTATION_ORDER:
        t(f"LANGUAGE_DEITIES has entry for '{lang}'", lang in LANGUAGE_DEITIES)

    # -- Required fields per language-deity ----------------------------------
    required_fields = [
        "divine_name", "epithet", "domain", "portfolio",
        "mythology", "sacred_text", "holy_symbol", "holy_days",
        "divine_rank", "blessing", "worship_practice",
        "ritual_pattern", "divine_relationships", "prophecy",
        "creation_myth_tag", "temple_location", "power_level",
        "influence_range", "deity_emoji",
    ]
    for lang in ROTATION_ORDER:
        entry = LANGUAGE_DEITIES[lang]
        for field in required_fields:
            t(f"  '{lang}' has '{field}'", field in entry, f"missing {field}")

    # -- portfolio non-empty -------------------------------------------------
    for lang in ROTATION_ORDER:
        portfolio = LANGUAGE_DEITIES[lang]["portfolio"]
        t(f"  '{lang}' portfolio is non-empty", len(portfolio) >= 3)
        t(f"  '{lang}' portfolio items are strings", all(isinstance(p, str) for p in portfolio))

    # -- divine_rank in valid list --------------------------------------------
    valid_ranks = ["Primordial Deity", "Elder Deity", "Major Deity", "Minor Deity"]
    for lang in ROTATION_ORDER:
        rank = LANGUAGE_DEITIES[lang]["divine_rank"]
        t(f"  '{lang}' divine_rank is valid", rank in valid_ranks)

    # -- power_level range ----------------------------------------------------
    for lang in ROTATION_ORDER:
        pl = LANGUAGE_DEITIES[lang]["power_level"]
        t(f"  '{lang}' power_level >= 0", pl >= 0)
        t(f"  '{lang}' power_level <= 100", pl <= 100)

    # -- divine_relationships structure ---------------------------------------
    for lang in ROTATION_ORDER:
        dr = LANGUAGE_DEITIES[lang]["divine_relationships"]
        t(f"  '{lang}' has allies list", "allies" in dr)
        t(f"  '{lang}' has rivals list", "rivals" in dr)
        for ally in dr.get("allies", []):
            t(f"  '{lang}' ally '{ally[0]}' has 2 elements", len(ally) == 2)
        for rival in dr.get("rivals", []):
            t(f"  '{lang}' rival '{rival[0]}' has 2 elements", len(rival) == 2)

    # -- ritual_pattern has required keys ------------------------------------
    ritual_keys = ["prayer", "confession", "penance", "sacred_rhythm"]
    for lang in ROTATION_ORDER:
        rp = LANGUAGE_DEITIES[lang]["ritual_pattern"]
        for key in ritual_keys:
            t(f"  '{lang}' ritual_pattern has '{key}'", key in rp)

    # -- C/C++ has highest power_level (Primordial Deity) ---------------------
    all_pl = {lang: LANGUAGE_DEITIES[lang]["power_level"] for lang in ROTATION_ORDER}
    t("C/C++ has highest power_level (Primordial)", all_pl["C/C++"] == max(all_pl.values()))

    # -- pantheon() advances rotation ----------------------------------------
    try:
        cfg_before = load_rotation()
        idx_before = cfg_before["current_index"]
        lang_before = cfg_before["languages"][idx_before % len(cfg_before["languages"])]
        result = pantheon()
        cfg_after = load_rotation()
        idx_after = cfg_after["current_index"]
        t("pantheon() advances current_index",
          idx_after == (idx_before + 1) % len(cfg_before["languages"]))
        t("pantheon() returns rotation_advanced language", result.get("language") == lang_before)
        t("pantheon() returns next_language", "next_language" in result)
        t("pantheon() returns next_index", "next_index" in result)
    except Exception as e:
        t("pantheon() rotation advancement", False, str(e))

    # -- pantheon() result structure ------------------------------------------
    try:
        result = pantheon()
        t("result is a dict", isinstance(result, dict))
        t("result has 'language' key", "language" in result)
        t("result has 'divine_name' key", "divine_name" in result)
        t("result has 'epithet' key", "epithet" in result)
        t("result has 'domain' key", "domain" in result)
        t("result has 'portfolio' key", "portfolio" in result)
        t("result has 'mythology' key", "mythology" in result)
        t("result has 'sacred_text' key", "sacred_text" in result)
        t("result has 'holy_symbol' key", "holy_symbol" in result)
        t("result has 'divine_rank' key", "divine_rank" in result)
        t("result has 'blessing' key", "blessing" in result)
        t("result has 'worship_practice' key", "worship_practice" in result)
        t("result has 'ritual_pattern' key", "ritual_pattern" in result)
        t("result has 'divine_relationships' key", "divine_relationships" in result)
        t("result has 'prophecy' key", "prophecy" in result)
        t("result has 'power_level' key", "power_level" in result)
        t("result has 'divinity_bar' key", "divinity_bar" in result)
        t("result has 'tool' key", "tool" in result)
        t("result has 'version' key", "version" in result)
        t("result['tool'] == 'polyglot-pantheon'", result.get("tool") == TOOL_NAME)
        t("result['version'] == '1.0.0'", result.get("version") == TOOL_VERSION)
        t("result['next_language'] in rotation_order", result.get("next_language") in result.get("rotation_order", []))
        t("result['next_language'] != result['language']", result.get("next_language") != result.get("language"))
    except Exception as e:
        t("pantheon() result structure", False, str(e))

    # -- divinity_bar validity ------------------------------------------------
    for lang in ROTATION_ORDER:
        result = pantheon()
        bar = result.get("divinity_bar", "")
        t(f"  divinity_bar for '{lang}' is a string", isinstance(bar, str))
        t(f"  divinity_bar for '{lang}' has correct length (20)", len(bar) == 20, f"len={len(bar)}")
        t(f"  divinity_bar for '{lang}' contains only █ and ░",
          all(c in "█░" for c in bar), f"chars={set(bar)}")

    # -- domain_web validity --------------------------------------------------
    for lang in ROTATION_ORDER:
        result = pantheon()
        dw = result.get("domain_web", "")
        t(f"  domain_web for '{lang}' is a string", isinstance(dw, str))
        t(f"  domain_web for '{lang}' is non-empty", len(dw) > 0)

    # -- build_divinity_bar correctness --------------------------------------
    bar100 = build_divinity_bar(100)
    bar50 = build_divinity_bar(50)
    bar0 = build_divinity_bar(0)
    t("divinity_bar(100) is all filled (20 chars)", bar100 == "█" * 20)
    t("divinity_bar(0) is all empty (20 chars)", bar0 == "░" * 20)
    t("divinity_bar(50) is half filled", bar50 == "█" * 10 + "░" * 10)

    # -- Full cycle rotation --------------------------------------------------
    try:
        # Save original state
        cfg_orig = load_rotation()
        orig_index = cfg_orig["current_index"]

        # Reset to index 0 for deterministic cycle test
        cfg_reset = cfg_orig.copy()
        cfg_reset["current_index"] = 0
        cfg_reset["last_language"] = ROTATION_ORDER[0]
        cfg_reset["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
        save_rotation(cfg_reset)

        # Perform full cycle
        visited = []
        for i in range(len(ROTATION_ORDER)):
            cfg = load_rotation()
            idx = cfg["current_index"]
            lang = cfg["languages"][idx % len(cfg["languages"])]
            visited.append(lang)
            cfg["current_index"] = (idx + 1) % len(cfg["languages"])
            cfg["last_language"] = lang
            cfg["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
            save_rotation(cfg)

        t("Full cycle visits all languages in order", visited == ROTATION_ORDER,
          f"visited={visited}")

        # Restore original state
        cfg_restore = load_rotation()
        cfg_restore["current_index"] = orig_index
        cfg_restore["last_language"] = cfg_orig["last_language"]
        cfg_restore["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
        save_rotation(cfg_restore)
    except Exception as e:
        t("Full cycle rotation test", False, str(e))

    print(f"\n{'='*55}")
    if errors:
        print(f"❌ {len(errors)} test(s) failed: {', '.join(errors)}")
        sys.exit(1)
    else:
        print(f"✅ All {passed} tests passed!")
        print("⚡ The pantheon is alive and the gods are watching.")
        sys.exit(0)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        result = pantheon()
        print(json.dumps(result, indent=2))
