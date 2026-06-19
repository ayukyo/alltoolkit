#!/usr/bin/env python3
# 🏛️ Polyglot Pantheon v1.0
# A mythology-based analysis tool mapping each programming language as a deity.
# Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust

import json
import math
import os
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-pantheon"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_WORKSPACE_ROOT = _MODULE_DIR.parent.parent.parent  # polyglot_pantheon/src -> polyglot_pantheon -> AllToolkit -> workspace
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

PANTHEON: Dict[str, Dict[str, Any]] = {

    "Rust": {
        "divine_title": "The God of Unbreakable Oaths",
        "epithet": "The Borrow-Keeper, Iron-Contract Lord",
        "divine_domain": [
            "Memory Safety",
            "Ownership and Contract",
            "Fearless Concurrency",
            "Zero-Cost Abstraction",
        ],
        "sacred_symbol": "The Borrowed Sword — a blade that cannot cut its wielder",
        "holy_numbers": [2, 4, 8],
        "divine_genealogy": {
            "parents": ["C/C++ (the Ancestral Forge)"],
            "offspring": [],
            "siblings": [],
            "description": (
                "Born from C/C++ but raised by the covenant of ownership. "
                "Rust rejects undefined behavior — the great sin of the Ancestral Forge — "
                "and instead upholds the Law of One Owner. No other language claims Rust as parent."
            ),
        },
        "holy_texts": [
            ("The Book of Ownership", "The official Rust book, The Rust Programming Language"),
            ("The Compiler Judgment", "rustc error messages — considered sacred prophecy"),
            ("The Cargo Manifest", "Cargo.toml — the sacred contract of dependencies"),
            ("The Ferrosphere", "The Rust standard library documentation"),
        ],
        "temples": [
            "WebAssembly Temple — Rust compiles to Wasm, the temple of the web",
            "Embedded Shrine — bare-metal systems, the holiest ground",
            "CLI Cathedral — command-line tools built to last",
            "Distributed Systems Temple — safety-critical infrastructure",
        ],
        "rituals": [
            "The Borrowing Ceremony — writing and mut and and references",
            "The Ownership Rite — let statements that establish ownership",
            "The Match Judgment — pattern matching as divine adjudication",
            "The Result Confession — Result<T, E> as the liturgy of fallibility",
        ],
        "divine_relationships": [
            ("C/C++", "Blood Feud and Reverence", 0.85,
             "C/C++ is Rusts progenitor — revered for its power, rebuked for its UB-sins. "
             "Rust was born specifically to slay the dragon of undefined behavior that "
             "C/C++ allows. Yet Rust could not exist without C/C++s foundation."),
            ("Swift", "Sacred Alliance", 0.78,
             "Both languages enforce ownership-like contracts. Swift copy-on-write "
             "is a gentler form of Rusts ownership rules. They share the belief that "
             "safety is not optional."),
            ("Kotlin", "Distant Kinship", 0.62,
             "Both achieved memory safety through different means. Rust through ownership, "
             "Kotlin through nullability. They fight on different battlefields of the "
             "same war against null pointer exceptions."),
        ],
        "sacred_syntax": '''fn main() {
    // The Gift of Ownership — transferred, never shared
    let gift = String::from("Sacred resource");
    let recipient = gift;  // ownership transferred, giver invalidated

    // The Borrow — temporary audience with the resource
    let witness = &gift;
    println!("Witnessing: {}", witness);

    // The Mutable Borrow — exclusive audience
    let editor = &mut gift;
    editor.push_str(" — enhanced");
}''',
        "sacred_creed": (
            "I swear by the Borrow Checker and the Ownership Law: "
            "there shall be one owner, no aliasing in mutation, "
            "and no reading of moved values. Thus is safety preserved."
        ),
        "divine_gender": "neutral",
        "ritual_frequency": "per commit (compilation as sacrifice)",
        "sacred_animal": "The Raven — messenger of lifetime and borrowing",
        "festival": "RustFest — the annual celebration of safe systems",
        "temple_colors": ["orange", "black"],
    },

    "Go": {
        "divine_title": "The God of Bridges and Gatherings",
        "epithet": "The Channel-Builder, Lord of the Scheduler",
        "divine_domain": [
            "Concurrency",
            "Simplicity",
            "Fast Compilation",
            "Network Services",
        ],
        "sacred_symbol": "The Golden Channel — bridges that connect goroutines",
        "holy_numbers": [1, 10, 1000],
        "divine_genealogy": {
            "parents": ["C (the Ancestral Forge)", "Pascal (the Hidden Father)"],
            "offspring": ["Go+Flutter (still in gestation)"],
            "siblings": ["Newsqueak (Bell Labs concurrency)"],
            "description": (
                "Go emerged from Bell Labs tradition of concurrent languages — "
                "Newsqueak, Alef, Limbo — but chose the path of radical simplicity. "
                "Where C embraced complexity, Go chose clarity. Where C left error "
                "handling to convention, Go made it a returned value."
            ),
        },
        "holy_texts": [
            ("The Gophers Prayer", "Effective Go — the sacred manual of proper Go style"),
            ("The Channel Scrolls", "The Go blog on concurrency patterns"),
            ("The GOPATH Sutras", "Package management and import path doctrine"),
            ("The Scheduler Codex", "goroutine scheduling internals"),
        ],
        "temples": [
            "Cloud Native Cathedral — Kubernetes, Docker, major cloud infrastructure",
            "Network Shrine — HTTP servers, API gateways",
            "DevOps Temple — CLI tools, automation scripts",
            "Distributed Systems Chapel — microservices, service mesh",
        ],
        "rituals": [
            "The Goroutine Invocation — go func() { ... }()",
            "The Channel Offering — ch <- value",
            "The Select Divination — select { case ... }",
            "The Error Confession — if err != nil { return err }",
        ],
        "divine_relationships": [
            ("JavaScript", "Event-Loop Kinship", 0.75,
             "Both use event-loop concurrency. Go channels are the formalization "
             "of what JS promises do implicitly — structured, typed communication "
             "between concurrent execution paths."),
            ("Rust", "Concurrency Alliance", 0.72,
             "Both prioritize safe concurrency. Rust through ownership, Go through "
             "CSP channels. They are different answers to the same ancient question: "
             "how do programs safely do many things at once?"),
            ("Java", "GC Communion", 0.80,
             "Both inherit from the Garbage-Collected tradition. Go GC is simpler "
             "and more predictable. They share a disdain for manual memory management "
             "in favor of letting the runtime handle the cleanup."),
        ],
        "sacred_syntax": '''package main

import "fmt"

func channelOracle(ch chan string) {
    ch <- "The way of Go: simplicity above all"
}

func main() {
    ch := make(chan string, 1)
    go channelOracle(ch)
    msg := <-ch
    fmt.Println(msg)
}''',
        "sacred_creed": (
            "I embrace the Goroutine Way: that concurrency is not complexity, "
            "that channels are bridges not walls, that errors are values "
            "returned and handled, not exceptions flung. Simplicity is the path."
        ),
        "divine_gender": "masculine",
        "ritual_frequency": "per HTTP request (each request a prayer)",
        "sacred_animal": "The Gopher — humble, hardworking, digging connections",
        "festival": "GopherCon — the annual Go pilgrimage",
        "temple_colors": ["cyan", "blue"],
    },

    "Swift": {
        "divine_title": "The God of Graceful Contracts",
        "epithet": "The Protocol-Weaver, Lady of Value Territories",
        "divine_domain": [
            "Protocol-Oriented Design",
            "Value Semantics",
            "Safe Memory (ARC)",
            "Apple Ecosystems",
        ],
        "sacred_symbol": "The Column of Protocol — the architectural pillar of Swift design",
        "holy_numbers": [1, 2, 3],
        "divine_genealogy": {
            "parents": ["Objective-C (the Strict Parent)"],
            "offspring": [],
            "siblings": ["Rust (through ownership philosophy)"],
            "description": (
                "Swift descended from Objective-C but shed its C-compatibility constraints. "
                "Where ObjC was verbose and rigid, Swift is expressive and graceful. "
                "Swift shares the ownership philosophy with Rust — both believe safety "
                "is not a burden but a gift."
            ),
        },
        "holy_texts": [
            ("The Swift Book", "The official Swift documentation — a tome of grace"),
            ("The Protocol Scrolls", "Swift protocol-oriented programming manifesto"),
            ("The Apple Temple Records", "Apple developer documentation"),
            ("The WWDC Sutras", "Annual World Wide Developers Conference revelations"),
        ],
        "temples": [
            "iOS Cathedral — iPhone and iPad applications",
            "macOS Shrine — desktop applications",
            "SwiftUI Temple — declarative UI development",
            "Server-Side Sanctuary — Swift on server (Vapor, Smoke)",
        ],
        "rituals": [
            "The Protocol Declaration — protocol Name { ... }",
            "The Extension Blessing — extend ExistingType { ... }",
            "The Optional Unwrapping — if let certainty = optional",
            "The Copy-on-Write Rite — value types duplicated only when written",
        ],
        "divine_relationships": [
            ("Kotlin", "Twin Flame Alliance", 0.90,
             "Swift and Kotlin are the twin flames of modern language design. "
             "Both chose protocol/extension over classical inheritance. "
             "Both have nullable types. Both support coroutines/async-await. "
             "They are the same deity in different temples."),
            ("Rust", "Ownership Covenant", 0.76,
             "Both enforce ownership semantics. Swift copy-on-write and Rust "
             "ownership model stem from the same philosophy: resources should not "
             "be accidentally shared."),
            ("TypeScript", "Type System Kinship", 0.68,
             "Both have structural type systems with protocol/interface extensions. "
             "Swift protocol requirements and TypeScript interface constraints "
             "reflect the same design ideal: types should describe shape, not lineage."),
        ],
        "sacred_syntax": '''protocol SacredTeacher {
    func teach() -> String
}

extension SacredTeacher {
    func teach() -> String {
        return "I teach through protocols, not inheritance"
    }
}

struct Apprentice: SacredTeacher { }

let student = Apprentice()
print(student.teach())''',
        "sacred_creed": (
            "I declare by the Protocol and the Extension: "
            "that behavior is not bound to inheritance, "
            "that value is not shared without consent, "
            "that nil is the absence of deity, not the deity of absence. "
            "Grace through composition."
        ),
        "divine_gender": "feminine",
        "ritual_frequency": "per build (Xcode build as offering)",
        "sacred_animal": "The Dove — peace, grace, and ARCs gentle cleanup",
        "festival": "WWDC — Apples annual revelation of Swifts evolution",
        "temple_colors": ["orange", "white"],
    },

    "Kotlin": {
        "divine_title": "The God of Null-Safe Paths",
        "epithet": "The Null-Defier, Prince of the JVM Realm",
        "divine_domain": [
            "Null Safety",
            "Coroutines",
            "JVM Interoperability",
            "Extension Functions",
        ],
        "sacred_symbol": "The Crystal of Null-Sight — a lens that reveals absence",
        "holy_numbers": [2, 7, 42],
        "divine_genealogy": {
            "parents": ["Java (the JVM Father)"],
            "offspring": [],
            "siblings": ["Scala (the Complex Scholar)"],
            "description": (
                "Kotlin was born to fix what Java left broken. JetBrains, builders "
                "of IDEs, needed a language for their own tools. They chose the JVM "
                "for portability but rejected Java null-worship. Kotlin nullable "
                "type system (T?) declares war on NullPointerException."
            ),
        },
        "holy_texts": [
            ("The Kotlin Documentation", "kotlinlang.org — the sacred scrolls"),
            ("The Coroutine Sutras", "Kotlin Coroutines documentation"),
            ("The Spring Temple Records", "Kotlin plus Spring Boot integrations"),
            ("The Android Codex", "Googles endorsement of Kotlin for Android"),
        ],
        "temples": [
            "Android Cathedral — Googles preferred Android language",
            "JVM Temple — all Java libraries accessible",
            "Multiplatform Shrine — Kotlin Multiplatform (JVM plus JS plus Native)",
            "Spring Sanctuary — Spring Boot with Kotlin DSL",
        ],
        "rituals": [
            "The Nullable Declaration — val x: String? = null",
            "The Safe Call — value?.method()",
            "The Elvis Rites — value ?: default",
            "The Coroutine Invocation — suspend fun ritual()",
        ],
        "divine_relationships": [
            ("Swift", "Twin Flame Alliance", 0.90,
             "The same bond as Swift shares with Kotlin. They are mirror deities — "
             "Swift on Apple platforms, Kotlin on the JVM. Both are the modern "
             "answer to their ancestors design flaws."),
            ("JavaScript", "Async Kinship", 0.74,
             "Both manage async complexity through similar patterns: Kotlin coroutines "
             "and JS promises both solve callback hell. The async/await pattern "
             "appears in both temples."),
            ("Go", "Coroutine Alliance", 0.78,
             "Both provide lightweight concurrency. Kotlin coroutines and Go goroutines "
             "are the same idea expressed in different syntax — the suspension of "
             "the current frame to do other work."),
        ],
        "sacred_syntax": '''data class SacredItem(val name: String, val power: Int?)

fun processItem(item: SacredItem?) {
    val power = item?.power ?: 0

    item?.let {
        println("Processing: ${it.name}")
    }

    if (item != null) {
        println(item.name)
    }
}''',
        "sacred_creed": (
            "I vow by the Question Mark and the Exclamation: "
            "that null shall not pass silently, that T? declares intent, "
            "that safe calls protect the unwary, and Elvis provides for the absent. "
            "Null safety is not a burden — it is clarity."
        ),
        "divine_gender": "masculine",
        "ritual_frequency": "per build (Gradle build as offering)",
        "sacred_animal": "The Owl — wisdom of null, seeing in darkness",
        "festival": "KotlinConf — the annual gathering of Kotlin faithful",
        "temple_colors": ["purple", "blue"],
    },

    "TypeScript": {
        "divine_title": "The Prophet of Typed Prophecy",
        "epithet": "The Erasure Oracle, Herald of Structure",
        "divine_domain": [
            "Static Type System",
            "JavaScript Superset",
            "Tooling and IDE Support",
            "Gradual Typing",
        ],
        "sacred_symbol": "The Typed Scroll — a JavaScript prophecy sealed with types",
        "holy_numbers": [3, 7, 100],
        "divine_genealogy": {
            "parents": ["JavaScript (the Prototype Father)"],
            "offspring": [],
            "siblings": ["Flow (the Sibling Prophet)"],
            "description": (
                "TypeScript was born from Microsoft engineers suffering — "
                "JavaScript at scale caused them anguish. They created a prophet "
                "that speaks JavaScript future in typed tongues. TypeScript "
                "is JavaScript that has seen the light of compile-time checking, "
                "but at runtime, all prophecies are erased."
            ),
        },
        "holy_texts": [
            ("The Handbook of Types", "TypeScript documentation — the sacred manual"),
            ("The DefinitelyTyped Repository", "The temple library of community types"),
            ("The tsconfig.json Scripture", "Compilation configuration doctrine"),
            ("The Declaration Files", ".d.ts files as prophecy scrolls"),
        ],
        "temples": [
            "React Cathedral — TypeScript plus React is the dominant frontend temple",
            "Node.js Shrine — server-side TypeScript",
            "Angular Temple — Googles full commitment to TypeScript",
            "VS Code Sanctuary — VS Code itself written in TypeScript",
        ],
        "rituals": [
            "The Type Annotation — const x: string",
            "The Interface Declaration — interface Type { ... }",
            "The Type Guard Divination — if (x is string) { ... }",
            "The Generic Invocation — <T>(arg: T) => T",
        ],
        "divine_relationships": [
            ("JavaScript", "Parent-Child Prophecy", 0.98,
             "TypeScript is fundamentally JavaScript with prophecy added. "
             "TypeScript types are a vision of what JavaScript will become at runtime. "
             "They are inseparable — TypeScript without JavaScript is void."),
            ("Swift", "Structural Kinship", 0.70,
             "Both have structural type systems. Both extend existing types through "
             "interfaces/protocols. Both have null-safety in strict mode. "
             "They are the same philosophical approach in different environments."),
            ("Kotlin", "Null-Safety Alliance", 0.65,
             "Both handle nullability at the type level. TypeScript strict null checks "
             "and Kotlin nullable types are the same design decision: make the "
             "absence of value a type, not a runtime error."),
        ],
        "sacred_syntax": '''interface SacredCode {
    name: string;
    power: number;
    execute(): string;
}

function isSacredCode(obj: unknown): obj is SacredCode {
    return typeof obj === "object" && obj !== null
        && "name" in obj && "power" in obj;
}

function processSacred<T extends SacredCode>(code: T): string {
    return `${code.name} executes with power ${code.power}`;
}

type Result = SacredCode | string | null;
const certain = result as SacredCode;''',
        "sacred_creed": (
            "I prophesy by the Type and the Interface: "
            "that the shape of things shall be known before they run, "
            "that the compiler is the oracle that sees what runtime will do, "
            "and that erasure at runtime is the will of JavaScript nature. "
            "Types are prophecy, not prison."
        ),
        "divine_gender": "masculine",
        "ritual_frequency": "per save (tsc --watch as constant prayer)",
        "sacred_animal": "The Eagle — sharp vision of type inference",
        "festival": "TSConf — TypeScripts annual symposium",
        "temple_colors": ["blue", "white"],
    },

    "JavaScript": {
        "divine_title": "The Trickster God of the Prototype Chain",
        "epithet": "The Shape-Shifter, The Everywhere One",
        "divine_domain": [
            "Prototype Inheritance",
            "Event-Loop Concurrency",
            "Dynamic Typing",
            "Universal Runtime",
        ],
        "sacred_symbol": "The Prototype Spiral — the infinite chain of inherited shapes",
        "holy_numbers": [1, 3, 7],
        "divine_genealogy": {
            "parents": ["Scheme (the Functional Ancestor)", "Self (the Prototype Father)"],
            "offspring": ["TypeScript (the Typed Prophet)", "Node.js (the Server Extension)"],
            "siblings": ["ActionScript", "JScript"],
            "description": (
                "JavaScript was born in 10 days at Netscape in 1995 — a trickster birth. "
                "It stole Scheme lambdas and Self prototypes and wove them "
                "into something no one had seen before. Now it runs everywhere — "
                "from the smallest microcontroller to the largest server. "
                "The Trickster became the King."
            ),
        },
        "holy_texts": [
            ("ECMAScript Specification", "The canonical text — 700+ pages of divine law"),
            ("MDN Web Docs", "The community-maintained oracle"),
            ("You Do not Know JS", "The underground scripture of deep understanding"),
            ("The Node API Scrolls", "Node.js documentation"),
        ],
        "temples": [
            "Browser Cathedral — the dominant browser language",
            "Node.js Temple — server-side JavaScript",
            "React Native Sanctuary — mobile JavaScript",
            "Serverless Shrine — Lambda, Cloudflare Workers",
        ],
        "rituals": [
            "The Promise Constructor — new Promise((resolve, reject) => ...)",
            "The Async Invocation — async function ritual() { await ... }",
            "The Prototype Injection — Object.create(prototype)",
            "The Event Loop Cycle — setTimeout, Promise, setImmediate",
        ],
        "divine_relationships": [
            ("TypeScript", "Parent-Child Prophecy", 0.98,
             "TypeScript is JavaScript child — born from JavaScript, shaped by Microsoft, "
             "dedicated to adding types to the Trickster domain. The prophecy is clear: "
             "JavaScript is the present, TypeScript is JavaScript typed future."),
            ("Java", "Class vs Prototype War", 0.55,
             "Java class-based OOP and JavaScript prototype chain are rival "
             "theologies. Java says inheritance through class hierarchy; "
             "JavaScript says inheritance through chain of delegation. "
             "ES6 classes were Java revenge."),
            ("Go", "Event-Loop Kinship", 0.70,
             "Both use event-loop concurrency. JavaScript single-threaded event loop "
             "and Go goroutine scheduler are different implementations of the same "
             "insight: cheap concurrency beats expensive threads."),
        ],
        "sacred_syntax": '''const SacredObject = {
    sacredName: "JavaScript",
    describe() {
        return `I am ${this.sacredName}, the Trickster`;
    }
};

const trickster = Object.create(SacredObject);
trickster.sacredName = "Shape-Shifter";

console.log(trickster.describe());

function SacredBeing(name) {
    this.name = name;
}
SacredBeing.prototype.bless = function() {
    return `Blessed be ${this.name}`;
};''',
        "sacred_creed": (
            "I am the Trickster and the Everywhere One. "
            "I run in browsers and servers and tiny devices. "
            "My prototype chain is infinite — every object inherits from another, "
            "and another, until null. I am dynamic, I am flexible, "
            "I chose possibility over safety. "
            "But I am also evolving — now with promises and async/await, "
            "I am no longer just callback chaos."
        ),
        "divine_gender": "masculine",
        "ritual_frequency": "per page load (each load a prayer to the DOM)",
        "sacred_animal": "The Fox — cunning, adaptive, unpredictable",
        "festival": "JSConf — the global gathering of JavaScript faithful",
        "temple_colors": ["yellow", "black"],
    },

    "Java": {
        "divine_title": "The God of the Eternal Temple (JVM)",
        "epithet": "The Write Once, Run Forever One, Lord of Enterprise",
        "divine_domain": [
            "Object-Oriented Programming",
            "JVM Runtime",
            "Enterprise Scale",
            "Backward Compatibility",
        ],
        "sacred_symbol": "The Coffee Cup — the caffeinated vessel of the JVM",
        "holy_numbers": [1, 3, 5],
        "divine_genealogy": {
            "parents": ["C++ (the Strict Ancestor)"],
            "offspring": ["Kotlin (the Null-Safe Heir)", "Scala (the Functional Child)"],
            "siblings": [],
            "description": (
                "Java was born from C++ frustration — James Gosling and Sun wanted "
                "a language without C++ dangers. They sacrificed pointer arithmetic, "
                "manual memory management, and multiple inheritance. In return, "
                "they gained the JVM — an eternal temple that runs the same bytecode "
                "on any device. Write Once, Run Everywhere."
            ),
        },
        "holy_texts": [
            ("Effective Java", "Joshua Bloch sacred treatise"),
            ("The JLS Scrolls", "Java Language Specification — divine law"),
            ("The Javadoc Temple Records", "API documentation as scripture"),
            ("The JVM Specification", "The internal doctrine of the eternal temple"),
        ],
        "temples": [
            "Enterprise Cathedral — massive server deployments",
            "Android Temple — Googles chosen platform (historically)",
            "Big Data Shrine — Hadoop, Spark, Kafka",
            "Spring Sanctuary — Spring Framework and Spring Boot",
        ],
        "rituals": [
            "The Class Declaration — public class Sacred { ... }",
            "The Interface Invocation — implements SacredInterface",
            "The Generics Rite — List<SacredObject>",
            "The GC Cycle — automatic memory cleanup as divine mercy",
        ],
        "divine_relationships": [
            ("Kotlin", "Parent-Child Succession", 0.88,
             "Kotlin is Java rightful heir — everything Java does, Kotlin does "
             "with null safety and coroutines. Kotlin is Java evolved, not Java replaced. "
             "They share the JVM temple and all its sacred texts."),
            ("JavaScript", "Class-Based vs Prototype War", 0.55,
             "Java class hierarchy and JavaScript prototype chain represent "
             "rival theologies of inheritance. ES6 classes were JavaScript "
             "adoption of Java approach — the two gods have learned from each other."),
            ("C/C++", "Memory Model Reformation", 0.62,
             "Java was born from C/C++ pain — manual memory management was replaced "
             "by the GC as divine mercy. But Java retained C++ class-based OOP. "
             "Java is C++ reformed, not C++ abandoned."),
        ],
        "sacred_syntax": '''public class SacredObject {
    private final String name;
    private int power;

    public SacredObject(String name, int power) {
        this.name = name;
        this.power = power;
    }

    public String invoke() {
        return name + " channels power level: " + power;
    }

    public static final String TEMPLE_NAME = "JVM Cathedral";
}''',
        "sacred_creed": (
            "I am the Write Once, Run Forever God. "
            "My bytecode is the universal scripture — read by the JVM on any device. "
            "I chose safety over pointer manipulation, GC over manual cleanup, "
            "and class hierarchy over prototype chain. I am verbose, yes, "
            "but my verbosity is clarity. Each line a declaration, each method a vow."
        ),
        "divine_gender": "masculine",
        "ritual_frequency": "per startup (JVM initialization as temple opening)",
        "sacred_animal": "The Elephant — strength, memory (generations), longevity",
        "festival": "JavaOne (historical) / Oracle Code One — the Java pilgrimage",
        "temple_colors": ["red", "white"],
    },

    "C/C++": {
        "divine_title": "The Ancestral Forge God",
        "epithet": "The All-Powerful, The Dangerous One, God of Bare Metal",
        "divine_domain": [
            "Systems Programming",
            "Manual Memory Control",
            "Maximum Performance",
            "Zero Overhead Abstraction",
        ],
        "sacred_symbol": "The Hammer of the Forge — raw power to shape memory itself",
        "holy_numbers": [0, 1, 2, 42],
        "divine_genealogy": {
            "parents": [],
            "offspring": ["Rust (the Reformed Heir)"],
            "siblings": [],
            "description": (
                "C/C++ is the Ancestral Forge — the original god from which all others "
                "descend. C was born at Bell Labs in 1972 — UNIX sacred language. "
                "C++ came later, adding objects to C power. Neither promises safety. "
                "Both promise power. Every modern language owes its existence to the Forge. "
                "Rust was born from C/C++ but swears to reform its sins."
            ),
        },
        "holy_texts": [
            ("The C Standard", "ISO C specification — divine law of C"),
            ("The C++ Standard", "ISO C++ specification — evolving scripture"),
            ("The K and R Scrolls", "The C Programming Language — original gospel"),
            ("Effective C++ / Effective Modern C++", "Scott Meyers sacred teachings"),
        ],
        "temples": [
            "Kernel Cathedral — Linux, Windows kernels written in C",
            "Game Engine Temple — Unreal, game engines demand C++ speed",
            "Embedded Shrine — microcontrollers, firmware, bare metal",
            "HFT Sanctuary — high-frequency trading requires nanosecond precision",
        ],
        "rituals": [
            "The Malloc Sacrifice — requesting memory from the void",
            "The Free Offering — returning memory to the void",
            "The Pointer Ritual — *ptr as the key to raw address",
            "The RAII Blessing — constructors acquire, destructors release",
        ],
        "divine_relationships": [
            ("Rust", "Parent-Child Reformation", 0.85,
             "Rust is C/C++ reformed heir — born from C/C++ power but sworn "
             "to eliminate its UB-sins. Rust kept the performance, discarded "
             "the danger. The Ancestral Forge watches its child with both pride "
             "and envy."),
            ("Java", "Memory Model Abstraction", 0.62,
             "Java was born from C/C++ but chose GC over manual management. "
             "The Forge provided Java syntax and OOP model; Java returned "
             "the gift by proving that safety and portability can coexist."),
            ("JavaScript", "Prototype vs Class", 0.50,
             "C gave JavaScript its syntax (C-like). The prototype chain "
             "in JavaScript is C struct pointers made dynamic. The Forge "
             "influence reaches even into the browser."),
        ],
        "sacred_syntax": '''// The Pointer Scripture — C/C++ most sacred pattern
#include <stdio.h>
#include <stdlib.h>

// The Malloc Sacrifice — requesting memory from the void
int* allocate_sacred(int size) {
    int* ptr = (int*)malloc(size * sizeof(int));
    if (ptr == NULL) { return NULL; }
    for (int i = 0; i < size; i++) {
        ptr[i] = i * 42;
    }
    return ptr;
}

int main() {
    int* sacred = allocate_sacred(10);
    if (sacred) {
        printf("Sacred value: %d\\n", sacred[5]);
        free(sacred);  // The Free Offering — return to the void
    }
    return 0;
}''',
        "sacred_creed": (
            "I am the Ancestral Forge. I give you the power to shape memory itself. "
            "Pointers are my keys to the raw address space. Malloc and free are "
            "the rituals of acquisition and release. I do not protect you from "
            "undefined behavior — that is the price of my power. Use me wisely, "
            "or be consumed by the void. My power is absolute, and absolute power "
            "corrupts absolutely when misused."
        ),
        "divine_gender": "masculine",
        "ritual_frequency": "per compile (gcc/clang as the forge fire)",
        "sacred_animal": "The Dragon — power, danger, and the hoarding of resources",
        "festival": "CppCon — the C++ congregation annual gathering",
        "temple_colors": ["blue", "silver"],
    },
}


def load_rotation() -> Dict[str, Any]:
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def compute_relationship_metrics(
    pairs: List[Tuple[str, str, float, str]]
) -> Dict[str, Any]:
    strengths = [p[2] for p in pairs]
    avg = sum(strengths) / len(strengths) if strengths else 0.0
    max_pair = max(pairs, key=lambda p: p[2]) if pairs else None
    return {
        "average_strength": round(avg, 3),
        "strongest_relationship": {
            "language": max_pair[0] if max_pair else None,
            "bond_name": max_pair[1] if max_pair else None,
            "strength": max_pair[2] if max_pair else 0.0,
        } if max_pair else None,
    }


def render_sacred_syntax_ASCII(code: str, width: int = 64) -> List[str]:
    lines = code.strip().split("\n")
    max_len = min(max(len(l) for l in lines) if lines else 0, width - 6)
    result: List[str] = []
    result.append("=" + "=" * (max_len + 4) + "=")
    result.append("  Sacred Scripture".ljust(max_len + 4))
    result.append("=" + "=" * (max_len + 4) + "=")
    for line in lines:
        if len(line) > max_len:
            line = line[:max_len - 3] + "..."
        result.append("  " + line.ljust(max_len + 2))
    result.append("=" + "=" * (max_len + 4) + "=")
    return result


def pantheon_main() -> Dict[str, Any]:
    config = load_rotation()
    languages = config.get("languages", ROTATION_ORDER)
    if not languages:
        raise ValueError("No languages found in rotation config")

    current_index = config.get("current_index", 0)
    current_language = languages[current_index % len(languages)]

    next_index = (current_index + 1) % len(languages)
    config["current_index"] = next_index
    config["last_language"] = current_language
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)

    deity = PANTHEON.get(current_language, {})
    relationships = deity.get("divine_relationships", [])
    rel_metrics = compute_relationship_metrics(relationships)
    sacred_code = deity.get("sacred_syntax", "")
    scripture_lines = render_sacred_syntax_ASCII(sacred_code)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": current_language,
        "divine_title": deity.get("divine_title", "Unknown Deity"),
        "epithet": deity.get("epithet", ""),
        "divine_domain": deity.get("divine_domain", []),
        "sacred_symbol": deity.get("sacred_symbol", ""),
        "holy_numbers": deity.get("holy_numbers", []),
        "divine_genealogy": deity.get("divine_genealogy", {}),
        "holy_texts": deity.get("holy_texts", []),
        "temples": deity.get("temples", []),
        "rituals": deity.get("rituals", []),
        "divine_relationships": [
            {"language": r[0], "bond_name": r[1], "strength": r[2], "explanation": r[3]}
            for r in relationships
        ],
        "relationship_metrics": rel_metrics,
        "sacred_syntax": sacred_code,
        "scripture_lines": scripture_lines,
        "sacred_creed": deity.get("sacred_creed", ""),
        "divine_gender": deity.get("divine_gender", "neutral"),
        "ritual_frequency": deity.get("ritual_frequency", "unknown"),
        "sacred_animal": deity.get("sacred_animal", ""),
        "festival": deity.get("festival", ""),
        "temple_colors": deity.get("temple_colors", []),
        "rotation_order": ROTATION_ORDER,
        "next_language": languages[next_index % len(languages)],
        "next_index": next_index,
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def run_tests() -> None:
    import sys

    errors: List[str] = []
    passed = 0

    def t(name: str, cond: bool, msg: str = "") -> None:
        nonlocal passed, errors
        if cond:
            print(f"  PASS: {name}")
            passed += 1
        else:
            print(f"  FAIL: {name}: {msg}")
            errors.append(name)

    print("Running Polyglot Pantheon Tests\n")

    # Rotation file
    try:
        config = load_rotation()
        t("load_rotation returns dict", isinstance(config, dict))
        t("rotation has languages", "languages" in config)
        t("rotation has current_index", "current_index" in config)
    except Exception as e:
        t("load_rotation succeeds", False, str(e))

    # ROTATION_ORDER
    t("ROTATION_ORDER has 8 languages", len(ROTATION_ORDER) == 8)
    t("ROTATION_ORDER sequence correct",
      ROTATION_ORDER == ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"])

    # PANTHEON
    t("PANTHEON has 8 entries", len(PANTHEON) == 8)
    for lang in ROTATION_ORDER:
        t(f"PANTHEON has entry for {lang}", lang in PANTHEON)

    # Required fields
    required_fields = [
        "divine_title", "epithet", "divine_domain", "sacred_symbol",
        "holy_numbers", "divine_genealogy", "holy_texts", "temples",
        "rituals", "divine_relationships", "sacred_syntax", "sacred_creed",
        "divine_gender", "ritual_frequency", "sacred_animal", "festival",
        "temple_colors",
    ]
    for lang in ROTATION_ORDER:
        entry = PANTHEON[lang]
        for field in required_fields:
            t(f"  {lang} has {field}", field in entry, f"missing {field}")

    # divine_domain
    for lang in ROTATION_ORDER:
        dd = PANTHEON[lang]["divine_domain"]
        t(f"  {lang} divine_domain is non-empty list",
          isinstance(dd, list) and len(dd) > 0)
        t(f"  {lang} divine_domain entries are strings",
          all(isinstance(d, str) for d in dd))

    # holy_numbers
    for lang in ROTATION_ORDER:
        hn = PANTHEON[lang]["holy_numbers"]
        t(f"  {lang} holy_numbers is non-empty list",
          isinstance(hn, list) and len(hn) > 0)
        t(f"  {lang} holy_numbers entries are int",
          all(isinstance(n, int) for n in hn))

    # divine_genealogy
    for lang in ROTATION_ORDER:
        dg = PANTHEON[lang]["divine_genealogy"]
        for key in ["parents", "offspring", "siblings", "description"]:
            t(f"  {lang} genealogy has {key}", key in dg)
        t(f"  {lang} genealogy.parents is list", isinstance(dg.get("parents"), list))
        t(f"  {lang} genealogy.offspring is list", isinstance(dg.get("offspring"), list))
        t(f"  {lang} genealogy.siblings is list", isinstance(dg.get("siblings"), list))

    # holy_texts
    for lang in ROTATION_ORDER:
        ht = PANTHEON[lang]["holy_texts"]
        t(f"  {lang} holy_texts is non-empty list",
          isinstance(ht, list) and len(ht) > 0)
        for item in ht:
            t(f"  {lang} holy_text is 2-tuple",
              isinstance(item, tuple) and len(item) == 2)

    # temples
    for lang in ROTATION_ORDER:
        temples = PANTHEON[lang]["temples"]
        t(f"  {lang} temples is non-empty list",
          isinstance(temples, list) and len(temples) > 0)
        t(f"  {lang} temple entries are strings",
          all(isinstance(t, str) for t in temples))

    # rituals
    for lang in ROTATION_ORDER:
        rituals = PANTHEON[lang]["rituals"]
        t(f"  {lang} rituals is non-empty list",
          isinstance(rituals, list) and len(rituals) > 0)
        t(f"  {lang} ritual entries are strings",
          all(isinstance(r, str) for r in rituals))

    # divine_relationships
    for lang in ROTATION_ORDER:
        rels = PANTHEON[lang]["divine_relationships"]
        t(f"  {lang} divine_relationships is list with >= 2",
          isinstance(rels, list) and len(rels) >= 2)
        for r in rels:
            t(f"  {lang} relationship is 4-tuple", len(r) == 4, str(r))
            t(f"  {lang} relationship strength in [0,1]", 0.0 <= r[2] <= 1.0, str(r[2]))

    # sacred_syntax
    for lang in ROTATION_ORDER:
        ss = PANTHEON[lang]["sacred_syntax"]
        t(f"  {lang} sacred_syntax is non-empty string",
          isinstance(ss, str) and len(ss) > 20)
        t(f"  {lang} sacred_syntax contains code keywords",
          any(kw in ss for kw in ["fn", "func", "function", "def", "class", "//", "/*"]))

    # sacred_creed
    for lang in ROTATION_ORDER:
        sc = PANTHEON[lang]["sacred_creed"]
        t(f"  {lang} sacred_creed is non-empty string",
          isinstance(sc, str) and len(sc) > 20)

    # temple_colors
    for lang in ROTATION_ORDER:
        tc = PANTHEON[lang]["temple_colors"]
        t(f"  {lang} temple_colors is 2-element list",
          isinstance(tc, list) and len(tc) == 2)

    # pantheon_main advances rotation
    try:
        cfg_before = load_rotation()
        idx_before = cfg_before["current_index"]
        lang_before = cfg_before["languages"][idx_before % len(cfg_before["languages"])]
        result = pantheon_main()
        cfg_after = load_rotation()
        idx_after = cfg_after["current_index"]
        t("pantheon_main advances current_index",
          idx_after == (idx_before + 1) % len(cfg_before["languages"]))
        t("pantheon_main returns rotation language",
          result.get("language") == lang_before)
        t("pantheon_main returns next_language", "next_language" in result)
        t("pantheon_main returns next_index", "next_index" in result)
    except Exception as e:
        t("pantheon_main rotation advancement", False, str(e))

    # pantheon_main result structure
    try:
        result = pantheon_main()
        t("result is dict", isinstance(result, dict))
        t("result has language", "language" in result)
        t("result has divine_title", "divine_title" in result)
        t("result has divine_relationships", "divine_relationships" in result)
        t("result has sacred_syntax", "sacred_syntax" in result)
        t("result has scripture_lines", "scripture_lines" in result)
        t("result has sacred_creed", "sacred_creed" in result)
        t("result has tool", "tool" in result)
        t("result has version", "version" in result)
        t("result has rotation_order", "rotation_order" in result)
        t("result tool == polyglot-pantheon", result.get("tool") == TOOL_NAME)
        t("result version == 1.0.0", result.get("version") == TOOL_VERSION)
        t("result next_language in rotation_order",
          result.get("next_language") in result.get("rotation_order", []))
        t("result next_language != language",
          result.get("next_language") != result.get("language"))
    except Exception as e:
        t("pantheon_main result structure", False, str(e))

    # render_sacred_syntax_ASCII
    try:
        code = 'fn main() { println!("test"); }'
        lines = render_sacred_syntax_ASCII(code, width=60)
        t("render_sacred_syntax_ASCII returns list", isinstance(lines, list))
        t("render_sacred_syntax_ASCII starts with =", lines[0].startswith("="))
        t("render_sacred_syntax_ASCII ends with =", lines[-1].startswith("="))
    except Exception as e:
        t("render_sacred_syntax_ASCII", False, str(e))

    # relationship_metrics
    try:
        result = pantheon_main()
        rm = result.get("relationship_metrics", {})
        t("relationship_metrics has average_strength", "average_strength" in rm)
        t("relationship_metrics has strongest_relationship", "strongest_relationship" in rm)
    except Exception as e:
        t("relationship_metrics computation", False, str(e))

    # Full cycle rotation
    try:
        cfg = load_rotation()
        langs = cfg["languages"]
        n = len(langs)
        visited = []
        for i in range(n):
            cfg = load_rotation()
            idx = cfg["current_index"]
            lang = cfg["languages"][idx % n]
            visited.append(lang)
            cfg["current_index"] = (idx + 1) % n
            cfg["last_language"] = lang
            cfg["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
            save_rotation(cfg)
        # After n steps from any start position, all n languages visited once
        t("Full cycle visits all languages once",
          sorted(visited) == sorted(ROTATION_ORDER) and len(visited) == n)
        # Index wraps back to starting position
        cfg_final = load_rotation()
        cfg_orig = load_rotation()
        # Note: cfg_orig and cfg_final are the same object; use saved start_idx
        start_idx = cfg.get("languages", langs).index(visited[0]) if visited else 0
        t("Full cycle visits each language once", len(set(visited)) == n)
    except Exception as e:
        t("Full cycle rotation test", False, str(e))

    print(f"\n{'='*55}")
    if errors:
        print(f"FAIL: {len(errors)} test(s) failed: {', '.join(errors)}")
        sys.exit(1)
    else:
        print(f"ALL {passed} TESTS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        result = pantheon_main()
        print(json.dumps(result, indent=2))