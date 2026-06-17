#!/usr/bin/env python3
"""
⚛️ Polyglot Quantum v1.0

A creative tool that maps each programming language as a quantum system —
wave functions, energy states, superposition of paradigms, quantum
entanglement with related languages, uncertainty principle trade-offs,
and decoherence patterns that determine when a language "collapses"
from potential to concrete behavior.

Creative concept: "Every programming language exists in superposition before
it is measured — it contains all possibilities until observation forces it
to collapse into a specific state. Rust's ownership model is a collapsed
wave function: the universe of possible references collapses to exactly one
owner. JavaScript's prototype chain is quantum entanglement — changes to
a prototype instantly affect all objects that inherit from it, regardless
of distance. Go's goroutines are superposition: thousands of execution
paths exist simultaneously until the scheduler observes and collapses
them. This tool maps that quantum reality."

Each run:
  1. Reads language_rotation.json, advances current_index
  2. Selects the rotation language
  3. Generates a quantum system report:
     - Wave Function: the language's paradigm superposition
     - Energy Levels: abstraction tiers (ground state → excited states)
     - Quantum Entanglement: relationships with other languages
     - Uncertainty Principle: what you can't simultaneously know
     - Decoherence Pattern: how the language "collapses" possibilities
     - Hamiltonian Signature: the operator that governs the system
  4. Updates language_rotation.json

Distinct from existing tools:
  - polyglot_spectrometer:    spectral decomposition (7 bands, barcode)
  - polyglot_resonance:        harmonic relationships (oscilloscope waves)
  - polyglot_meridian:         spectral positioning (design space coordinates)
  - polyglot_constellation:     stellar gravity map (astronomy/navigation)
  - polyglot_vessel:           material essence (pressure/density/buoyancy)
  - polyglot_prism:            wavelength decomposition (physics lab)
  - polyglot_chronology:       geological epochs (deep time)
  - polyglot_tempo:            rhythm patterns (musical beats)
  - polyglot_cartographer:     geopolitical map (spatial/nations)
  - polyglot_harmony:          pairwise compatibility scores (musical intervals)
  - polyglot_resonator:        mental model frames (cognitive philosophy)
  - polyglot_flavor:           sensory tasting notes (sommelier)
  - polyglot_dna:              genetic trait mapping (molecular biology)
  - polyglot_faultline:        error archaeology (seismic)
  - polyglot_ecosystem_map:    ecosystem graph (ecological)
  - polyglot_anomaly:          quirks/gotchas catalog (paradoxes)
  - polyglot_translation:       cultural proverbs (social cargo)
  - polyglot_digest:            syntax-parallel code (spatial syntax)
  - polyglot_chronicle:        daily diary + challenge (temporal)
  - polyglot_signal:            signal semantics (alarm systems)

Polyglot Quantum is about QUANTUM MECHANICS METAPHOR — wave functions,
entanglement, uncertainty, and decoherence as a lens for understanding
how programming languages fundamentally work under the hood.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import math
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-quantum"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent
_WORKSPACE_ROOT = _MODULE_DIR.parent
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]


# ─────────────────────────────────────────────────────────────────────────────
# Quantum System Database — each language as a quantum system
# ─────────────────────────────────────────────────────────────────────────────

QUANTUM_SYSTEMS: Dict[str, Dict[str, Any]] = {

    "Rust": {
        "wave_function": [
            ("Systems Programming", 0.35),
            ("Memory Safety", 0.25),
            ("Functional Style", 0.20),
            ("Zero-Cost Abstraction", 0.15),
            ("Fearless Concurrency", 0.05),
        ],
        "ground_state": "Safe Systems (ownership-guaranteed)",
        "excited_states": [
            ("Embedded Systems",     "Excited to bare-metal hardware control"),
            ("WebAssembly Target",   "Collapses to Wasm bytecode"),
            ("Async Networking",     "Superposition of thousands of connections"),
            ("ML/AI Infrastructure","NumericsCollide with tensor abstractions"),
        ],
        "uncertainty_principle": {
            "dx": "You cannot simultaneously know the exact memory address and the value stored there",
            "dp": "You cannot simultaneously predict performance and guarantee safety",
            "description": "Rust's uncertainty principle: safety and mutability exist in tension — observing one disturbs the other through borrow rules",
        },
        "decoherence_pattern": {
            "trigger": "Compilation (measurement)",
            "description": (
                "Rust code exists as superposition of all possible behaviors "
                "until compile-time borrow checking collapses the wave function "
                "into exactly one outcome — either safe ownership or rejection. "
                "There is no runtime uncertainty: the collapse happens at compile time."
            ),
            "uncertainty_bits": 0,  # zero runtime uncertainty by design
        },
        "entanglement_pairs": [
            ("C/C++", "Manual Memory Entanglement",        0.80, "Both observe memory at the finest granularity; their borrow checker is a collapsed version of C's undefined behavior"),
            ("Swift", "Ownership Protocol Entanglement",  0.75, "Both enforce ownership semantics; Swift's copy-on-write is Rust's ownership model in cleaner clothing"),
            ("Kotlin","Null-Safety Entanglement",          0.65, "Both achieve memory safety through different quantum channels — Rust through ownership, Kotlin through nullability"),
        ],
        "hamiltonian": {
            "operator": "H_ownership = Σᵢ (owner_i · borrowed_i) - λ·dangling_refs",
            "description": "The Ownership Hamiltonian: the total energy of the system is minimized when every resource has exactly one owner and no dangling references exist",
            "eigenvalue_label": "Safe State (E₀ = 0)",
        },
        "uncertainty_product": 1.0,  # ħ/2 = 0.527 (representing borrow-rule uncertainty)
        "quantum_description": (
            "Rust is a quantum system where every variable exists in superposition "
            "between 'shared' and 'exclusive' until the borrow checker observes it. "
            "The act of observation (compiling) collapses all possibilities into a "
            "single eigenstate: either perfectly owned memory or a compile error. "
            "There is no quantum tunneling into undefined behavior — Rust's wave function "
            "never collapses into a dangerous state."
        ),
        "quantum_glyph": "⚛️",
        "orbital_config": "1s² 2s² 3s² | ownership-core | 4p⁶ concurrency-orbitals",
        "superposition_cardinality": 3,  # number of simultaneous states before collapse
        "collapse_mechanism": "compile_time",
        "measurement_disturbance": " borrow checker rejects the program if safety is violated",
    },

    "Go": {
        "wave_function": [
            ("Simple Concurrency", 0.35),
            ("Pragmatic Design",  0.25),
            ("Fast Compilation",  0.20),
            ("CSP Model",         0.15),
            ("Garbage Collection",0.05),
        ],
        "ground_state": "Goroutine Superposition",
        "excited_states": [
            ("Network Servers",     "Thousands of goroutines in simultaneous superposition"),
            ("CLI Tools",           "Collapses to fast single-binary executables"),
            ("Cloud Infrastructure","Go-routine wave functions manage microservices"),
            ("DevOps Scripts",      "Collapse into highly portable containers"),
        ],
        "uncertainty_principle": {
            "dx": "You cannot simultaneously know the exact goroutine count and when each will execute",
            "dp": "You cannot simultaneously predict GC pause duration and memory usage",
            "description": "Go's uncertainty principle: the scheduler's observation collapses the goroutine superposition — you know when it runs OR how many exist, but not both simultaneously",
        },
        "decoherence_pattern": {
            "trigger": "Scheduler observation",
            "description": (
                "Go code exists as superposition of all possible goroutine interleavings "
                "until the scheduler observes and collapses them to a single execution path. "
                "Unlike Rust, Go's collapse happens at runtime — the outcome is "
                "deterministic within a single run but unpredictable across runs. "
                "This is true quantum uncertainty: multiple valid outcomes exist until measured."
            ),
            "uncertainty_bits": 8,  # goroutine scheduling uncertainty
        },
        "entanglement_pairs": [
            ("JavaScript", "Event-Loop Entanglement",        0.70, "Both use event-loop concurrency; Go's channel-based CSP is entangled with JS's callback-based model"),
            ("Rust",      "Concurrency Safety Entanglement", 0.65, "Both prioritize safe concurrency; Rust through ownership, Go through communication"),
            ("Java",      "Garbage Collection Entanglement", 0.80, "Both rely on GC; entangled through the memory management crisis that birthed them"),
        ],
        "hamiltonian": {
            "operator": "H_scheduler = Σᵢ goroutine_i · channel_capacity_i",
            "description": "The Scheduler Hamiltonian: system energy is a function of active goroutines and channel bandwidth — more goroutines means more potential energy states",
            "eigenvalue_label": "Goroutine State (E_goroutine)",
        },
        "uncertainty_product": 8.0,  # high runtime uncertainty
        "quantum_description": (
            "Go is a quantum system where goroutines exist in superposition — "
            "thousands of execution paths exist simultaneously until the scheduler "
            "measures (schedules) one. The measurement disturbs the system: adding "
            "a goroutine changes the energy landscape for all others. "
            "Channels are entanglement channels: changing a value in one goroutine "
            "instantly affects receivers regardless of their physical location."
        ),
        "quantum_glyph": "⚛️",
        "orbital_config": "1s² 2s² 3s² | scheduler-core | 4p⁶ goroutine-orbitals",
        "superposition_cardinality": 7,  # many simultaneous goroutines
        "collapse_mechanism": "runtime_scheduler",
        "measurement_disturbance": " adding goroutines changes scheduler behavior for all others",
    },

    "Swift": {
        "wave_function": [
            ("Protocol-Oriented",     0.30),
            ("Value Types",          0.25),
            ("Safe Memory",          0.20),
            ("Apple Ecosystem",       0.15),
            ("Functional Style",     0.10),
        ],
        "ground_state": "Protocol Quantum Superposition",
        "excited_states": [
            ("iOS Development",    "Swift collapses into native iOS apps"),
            ("Server-Side Swift",   "Collapses to high-performance server binaries"),
            ("SwiftUI Declarative", "UI exists in superposition until user interaction collapses it"),
            ("Systems Programming", "Collapses to bare-metal embedded targets"),
        ],
        "uncertainty_principle": {
            "dx": "You cannot simultaneously know the exact copy cost and the memory address of a String",
            "dp": "You cannot simultaneously predict method dispatch time and protocol conformance",
            "description": "Swift's uncertainty: value types copy on assignment, but the copy is lazy — until you observe the value, it exists in superposition of 'copied' and 'shared'",
        },
        "decoherence_pattern": {
            "trigger": "Assignment or function call",
            "description": (
                "Swift values exist in superposition between 'copy-on-write shared' "
                "and 'uniquely owned' until an assignment or function call forces the "
                "copy-on-write mechanism to measure and resolve the state. "
                "Protocol existentials add another dimension of superposition — "
                "a protocol type contains all conforming types until type erasure collapses it."
            ),
            "uncertainty_bits": 4,
        },
        "entanglement_pairs": [
            ("Kotlin",      "Protocol Extension Entanglement",  0.88, "Both extend types without inheritance; Swift protocols and Kotlin extension functions are entangled through the extension mechanism"),
            ("Rust",        "Ownership Safety Entanglement",   0.75, "Both enforce safety through ownership-like models; Swift's copy-on-write mirrors Rust's ownership rules"),
            ("TypeScript",  "Type System Entanglement",        0.70, "Both have structural type systems; Swift's protocol requirements and TypeScript's interface constraints are entangled"),
        ],
        "hamiltonian": {
            "operator": "H_swift = Σᵢ protocol_i · concrete_type_i · copy_cost_i",
            "description": "The Swift Hamiltonian: system energy depends on protocol conformance complexity and copy cost — more generic constraints raise the energy barrier",
            "eigenvalue_label": "Protocol Eigenstate (E_protocol)",
        },
        "uncertainty_product": 4.0,
        "quantum_description": (
            "Swift is a quantum system where protocols represent superposition — "
            "a single protocol type contains all its conforming implementations "
            "simultaneously. The compiler observes (specializes) the protocol "
            "at monomorphization time, collapsing the wave function. "
            "Value types exist in copy-on-write superposition: shared until "
            "mutation forces a collapse to unique ownership."
        ),
        "quantum_glyph": "⚛️",
        "orbital_config": "1s² 2s² 3s² | protocol-core | 4f⁶ apple-ecosystem-orbitals",
        "superposition_cardinality": 4,
        "collapse_mechanism": "copy_on_write_assignment",
        "measurement_disturbance": " mutation causes copy, disturbing the shared state",
    },

    "Kotlin": {
        "wave_function": [
            ("JVM Interoperability",  0.30),
            ("Coroutines Async",      0.25),
            ("Null Safety",           0.20),
            ("Extension Functions",   0.15),
            ("Functional Style",      0.10),
        ],
        "ground_state": "Coroutine Quantum State",
        "excited_states": [
            ("Android Development",  "Kotlin collapses into Android apps"),
            ("Server-Side Kotlin",   "Collapses to JVM-based server applications"),
            ("Multiplatform Kotlin", "Superposition across JVM, JS, and native targets"),
            ("Spring Boot",          "Kotlin coroutines collapse into reactive Spring endpoints"),
        ],
        "uncertainty_principle": {
            "dx": "You cannot simultaneously know the exact suspension point and the caller that resumes it",
            "dp": "You cannot simultaneously predict coroutine completion order and memory usage",
            "description": "Kotlin's uncertainty: coroutines suspend at unknown points — the suspension boundary is a quantum event that collapses the call stack into an indeterminate state",
        },
        "decoherence_pattern": {
            "trigger": "Coroutine launch or suspend",
            "description": (
                "Kotlin coroutines exist in superposition of all possible "
                "suspension points until the suspending function is called. "
                "Each yield is a quantum measurement — the coroutine collapses "
                "from 'running' to 'suspended', preserving its state for later resumption. "
                "This is genuine quantum-like state preservation across time."
            ),
            "uncertainty_bits": 6,
        },
        "entanglement_pairs": [
            ("Swift",      "Protocol Extension Entanglement",  0.88, "Both enable extension without inheritance; entangled through the same quantum mechanism"),
            ("JavaScript", "Async Callback Entanglement",      0.75, "Both manage async complexity; Kotlin coroutines and JS promises are entangled through the async/await pattern"),
            ("Go",         "Coroutine Entanglement",          0.80, "Both provide lightweight concurrency; Kotlin coroutines and Go goroutines are entangled through the concurrent execution paradigm"),
        ],
        "hamiltonian": {
            "operator": "H_kotlin = Σᵢ suspend_point_i · continuation_i",
            "description": "The Kotlin Hamiltonian: system energy is determined by suspension points and their continuation closures — more suspend functions raise the quantum uncertainty",
            "eigenvalue_label": "Suspend Eigenstate (E_suspend)",
        },
        "uncertainty_product": 6.0,
        "quantum_description": (
            "Kotlin is a quantum system where coroutines exist in superposition "
            "of execution and suspension. The suspend keyword creates a quantum "
            "boundary — the function collapses from 'running' to 'suspended' "
            "at a measurement point determined by the scheduler. "
            "Continuation closures are entanglement channels: the suspended "
            "state is preserved and can be resumed from any compatible context."
        ),
        "quantum_glyph": "⚛️",
        "orbital_config": "1s² 2s² 3s² | jvm-core | 4p⁶ coroutine-orbitals",
        "superposition_cardinality": 5,
        "collapse_mechanism": "suspend_resume",
        "measurement_disturbance": " suspending a coroutine disturbs all its continuations",
    },

    "TypeScript": {
        "wave_function": [
            ("Static Type System",  0.35),
            ("JavaScript Superset",0.25),
            ("Structural Types",    0.20),
            ("Tooling Ecosystem",   0.15),
            ("Generic Constraints", 0.05),
        ],
        "ground_state": "Type Superposition",
        "excited_states": [
            ("Frontend Web Apps",    "TS collapses into transpiled JavaScript"),
            ("Node.js Backend",      "Collapses to typed server applications"),
            ("React/Angular/Vue",    "Framework superpositions collapse to component trees"),
            ("Type-Level Computing", "TypeScript types exist in type-level computation superposition"),
        ],
        "uncertainty_principle": {
            "dx": "You cannot simultaneously know the exact runtime type and the compile-time type annotation",
            "dp": "You cannot simultaneously predict type guard behavior and narrowing precision",
            "description": "TypeScript's uncertainty: a variable typed as 'string | number' exists in superposition of both types until a type guard collapses it — but the runtime value is always concrete",
        },
        "decoherence_pattern": {
            "trigger": "Runtime execution (type erasure)",
            "description": (
                "TypeScript code exists in superposition of all possible type "
                "configurations during development — the type system is a quantum "
                "measurement tool. At compile time (transpilation), the type wave "
                "function collapses to JavaScript: all type annotations are erased, "
                "leaving only the concrete runtime values. The collapse is irreversible — "
                "type information is not present at runtime."
            ),
            "uncertainty_bits": 2,  # compile-time uncertainty is low, most collapses are clean
        },
        "entanglement_pairs": [
            ("JavaScript", "Prototype Entanglement",        0.95, "TypeScript is fundamentally entangled with JavaScript — the type system sits on top of JS's prototype chain, and erasing types always returns to pure JS"),
            ("Swift",     "Type System Entanglement",        0.70, "Both have structural types; TS interfaces and Swift protocols are entangled through the structural typing mechanism"),
            ("Kotlin",   "Null-Safety Entanglement",       0.65, "Both handle nullability at the type level; TS's strict null checks and Kotlin's null-safety are entangled through the same design principle"),
        ],
        "hamiltonian": {
            "operator": "H_ts = Σᵢ type_annotation_i · runtime_value_i - λ·any_type",
            "description": "The TypeScript Hamiltonian: system energy is a balance between type annotations and runtime values — the any type introduces maximum uncertainty (highest energy state)",
            "eigenvalue_label": "Typed State (E_typed) or Untyped State (E_any)",
        },
        "uncertainty_product": 2.0,  # type erasure collapses most uncertainty cleanly
        "quantum_description": (
            "TypeScript is a quantum system where types exist in superposition "
            "during development — a union type contains all its member types "
            "simultaneously. The compiler observes (type-checks) each branch, "
            "collapsing the wave function. Type guards are measurement operators "
            "that resolve the superposition. But at runtime, all types are erased — "
            "the wave function collapses to pure JavaScript with zero remaining uncertainty."
        ),
        "quantum_glyph": "⚛️",
        "orbital_config": "1s² 2s² 3s² | type-core | 4p⁶ transpile-orbitals",
        "superposition_cardinality": 6,
        "collapse_mechanism": "type_guard_or_transpilation",
        "measurement_disturbance": " type narrowing collapses the union, disturbing the 'both types' state",
    },

    "JavaScript": {
        "wave_function": [
            ("Prototype Inheritance",  0.30),
            ("Event-Loop Concurrency", 0.25),
            ("First-Class Functions",  0.20),
            ("Dynamic Typing",         0.15),
            ("Everywhere Runtime",     0.10),
        ],
        "ground_state": "Prototype Quantum Entanglement",
        "excited_states": [
            ("Browser Applications",   "JS collapses into DOM manipulation and UI rendering"),
            ("Server (Node.js)",       "Collapses to async I/O handlers"),
            ("Mobile (React Native)",  "Superposition across iOS and Android targets"),
            ("Serverless Functions",   "Collapses to stateless event handlers"),
        ],
        "uncertainty_principle": {
            "dx": "You cannot simultaneously know the exact prototype chain depth and the property lookup time",
            "dp": "You cannot simultaneously predict async callback order and memory usage of closures",
            "description": "JavaScript's uncertainty: prototypes form an entangled chain — modifying a prototype instantly affects all objects inheriting from it, no matter where they are in memory. The prototype chain is a quantum entanglement channel.",
        },
        "decoherence_pattern": {
            "trigger": "Property access or async callback resolution",
            "description": (
                "JavaScript objects exist in prototype superposition — they simultaneously "
                "inherit from all prototypes in the chain until a property access "
                "forces measurement and resolution. The prototype lookup is a "
                "quantum observation: it collapses the superposition to the "
                "first property found. Async callbacks add another layer — "
                "the event loop collapses callback superpositions at timer resolution."
            ),
            "uncertainty_bits": 10,  # highest uncertainty: prototype chain + event loop
        },
        "entanglement_pairs": [
            ("TypeScript", "Type Erasure Entanglement",      0.95, "TypeScript's types are entangled with JS's runtime — type erasure always collapses TS back to pure JS"),
            ("Java",      "Class-Based Entanglement",       0.60, "JS's prototype chain is the quantum alternative to Java's class hierarchy — same inheritance concept, different collapse mechanism"),
            ("Go",        "Event-Loop Entanglement",        0.70, "Both use event-loop concurrency; entangled through the async execution model"),
        ],
        "hamiltonian": {
            "operator": "H_js = Πᵢ prototype_chain_i · callback_queue_i",
            "description": "The JavaScript Hamiltonian: system energy is the product (not sum) of prototype chain depth and callback queue length — both grow multiplicatively as complexity increases",
            "eigenvalue_label": "Prototype Eigenstate (E_proto) or Callback Eigenstate (E_callback)",
        },
        "uncertainty_product": 10.0,  # maximum uncertainty: prototype chain + event loop
        "quantum_description": (
            "JavaScript is the most uncertain quantum system in the polyglot: "
            "the prototype chain creates genuine entanglement — changing a shared "
            "prototype instantly affects all objects that inherit from it, "
            "regardless of their location. The event loop creates superposition "
            "of thousands of async operations that collapse only when their "
            "turn arrives. Closures are quantum prisons: captured variables "
            "maintain their state indefinitely until the closure is called."
        ),
        "quantum_glyph": "⚛️",
        "orbital_config": "1s² 2s² 3s² | prototype-core | 4p¹⁰ event-loop-orbitals",
        "superposition_cardinality": 10,  # maximum superposition
        "collapse_mechanism": "property_lookup_or_callback_resolution",
        "measurement_disturbance": " prototype modification instantly disturbs all inheritors",
    },

    "Java": {
        "wave_function": [
            ("Object-Oriented",      0.35),
            ("JVM Runtime",          0.25),
            ("Enterprise Scale",     0.20),
            ("Checked Exceptions",   0.10),
            ("Backward Compatibility",0.10),
        ],
        "ground_state": "Class Hierarchy Quantum State",
        "excited_states": [
            ("Enterprise Applications",  "Java collapses into massive server deployments"),
            ("Android Apps",           "Collapses to Dalvik/ART bytecode"),
            ("Big Data Processing",     "Spark/MapReduce superpositions process massive datasets"),
            ("Microservices",          "Collapses to Spring Boot containers"),
        ],
        "uncertainty_principle": {
            "dx": "You cannot simultaneously know the exact object layout in memory and the GC pause duration",
            "dp": "You cannot simultaneously predict method dispatch target and JIT compilation status",
            "description": "Java's uncertainty: objects exist in superposition of 'eden', 'survivor', and 'old-gen' spaces until the GC measures and moves them — the object's identity is preserved across all generational spaces",
        },
        "decoherence_pattern": {
            "trigger": "Class loading or GC cycle",
            "description": (
                "Java classes exist in superposition between loaded and unloaded states "
                "until first use. The classloader is a measurement operator — "
                "it collapses the class into existence when first referenced. "
                "Objects exist in generational superposition: young generation "
                "(short-lived), survivor space (transitional), old generation (stable). "
                "GC cycles collapse this superposition, promoting surviving objects."
            ),
            "uncertainty_bits": 5,
        },
        "entanglement_pairs": [
            ("JavaScript", "Class-Based Entanglement",    0.60, "Both use class-based OOP; Java's static class model and JS's ES6 class model are entangled through the class concept"),
            ("Kotlin",    "JVM Interop Entanglement",     0.85, "Kotlin runs on the JVM and is entangled with Java through complete bytecode compatibility"),
            ("C/C++",     "Memory Model Entanglement",   0.62, "Java abstracted C++'s manual memory model into GC; entangled through the memory management crisis that drove Java's creation"),
        ],
        "hamiltonian": {
            "operator": "H_java = Σᵢ class_i · object_count_i + GC_pause_duration",
            "description": "The Java Hamiltonian: system energy is determined by loaded classes and object counts, plus GC pause duration as an energy dissipation term",
            "eigenvalue_label": "Class Eigenstate (E_class) or Object Eigenstate (E_object)",
        },
        "uncertainty_product": 3.5,
        "quantum_description": (
            "Java is a quantum system where classes exist in superposition "
            "of loaded/unloaded until the classloader measures them. "
            "Objects exist in generational superposition across GC spaces — "
            "simultaneously 'young' and 'old' until a GC cycle collapses "
            "the wave function and promotes survivors. The JIT compiler "
            "is a quantum optimizer: it collapses hot code paths into "
            "optimized machine code at runtime."
        ),
        "quantum_glyph": "⚛️",
        "orbital_config": "1s² 2s² 3s² | jvm-core | 4p⁶ gc-orbitals",
        "superposition_cardinality": 5,
        "collapse_mechanism": "class_loading_or_gc_cycle",
        "measurement_disturbance": " GC pause collapses the heap state, disturbing all running threads",
    },

    "C/C++": {
        "wave_function": [
            ("Systems Programming", 0.35),
            ("Manual Memory",       0.30),
            ("Maximum Control",     0.20),
            ("Zero Overhead",       0.10),
            ("Template Metaprogramming", 0.05),
        ],
        "ground_state": "Pointer Quantum Superposition",
        "excited_states": [
            ("Operating Systems",     "C/C++ collapses into kernel code and drivers"),
            ("Game Engines",          "Collapses to maximum-FPS rendering pipelines"),
            ("Embedded Firmware",    "C/C++ superposes across all microcontroller architectures"),
            ("High-Frequency Trading","Collapses to nanosecond-latency trading systems"),
        ],
        "uncertainty_principle": {
            "dx": "You cannot simultaneously know the exact memory address and the value stored there (pointer uncertainty)",
            "dp": "You cannot simultaneously predict undefined behavior outcomes and execution speed",
            "description": "C/C++'s uncertainty: pointers exist in superposition of all valid memory addresses — dereferencing an uninitialized or dangling pointer collapses the wave function into undefined behavior, the most dangerous collapse in computing",
        },
        "decoherence_pattern": {
            "trigger": "Pointer dereference or manual memory operation",
            "description": (
                "C/C++ is the only language where undefined behavior creates genuine "
                "quantum unpredictability — the program's wave function collapses "
                "into states that the C++ standard does not specify. "
                "This is not measurement uncertainty; it is fundamental quantum "
                "indeterminacy baked into the language specification. "
                "A buffer overflow collapses the wave function into anything from "
                "silent corruption to immediate segfault. "
                "There is no collapse mechanism that guarantees safety."
            ),
            "uncertainty_bits": 12,  # maximum danger: undefined behavior
        },
        "entanglement_pairs": [
            ("Rust",      "Memory Control Entanglement",    0.80, "Rust's ownership model was designed as a quantum collapse of C's undefined behavior — the same problem, solved with a collapse operator (borrow checker) that guarantees safety"),
            ("Java",      "Memory Model Entanglement",    0.62, "Java's GC abstracted C++'s manual memory management; entangled through the memory management crisis that Java was born to solve"),
            ("JavaScript","Pointer-Pointer Entanglement", 0.50, "Both allow pointer-like behavior through references, but JS hides the raw pointer behind prototype chains"),
        ],
        "hamiltonian": {
            "operator": "H_cpp = Σᵢ pointer_i · memory_location_i · undefined_behavior_i",
            "description": "The C/C++ Hamiltonian: system energy is the product of pointer arithmetic, memory location access, and undefined behavior potential — the most dangerous quantum system in computing",
            "eigenvalue_label": "Defined State (E_defined) or Undefined State (E_undefined = ∞)",
        },
        "uncertainty_product": 12.0,  # maximum uncertainty: undefined behavior is the most uncertain
        "quantum_description": (
            "C/C++ is a quantum system in the most extreme sense — "
            "undefined behavior is genuine quantum indeterminacy. "
            "A pointer in superposition of a valid address and a dangling "
            "address collapses differently each time depending on runtime state. "
            "The collapse is irreversible and unobservable post-collapse. "
            "Template metaprogramming creates compile-time quantum computation "
            "— templates are quantum circuits that resolve at compile time. "
            "C/C++ is the only language where the programmer directly controls "
            "the quantum hardware of memory."
        ),
        "quantum_glyph": "⚛️",
        "orbital_config": "1s² 2s² 3s² | pointer-core | 4p⁶ systems-orbitals",
        "superposition_cardinality": 12,  # maximum superposition
        "collapse_mechanism": "pointer_dereference_or_undefined_behavior",
        "measurement_disturbance": " undefined behavior collapse disturbs the entire process address space",
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


def compute_entanglement_strength(ent_pairs: List[Tuple[str, str, float, str]]) -> Dict[str, Any]:
    """Compute entanglement metrics from pairs."""
    strengths = [p[2] for p in ent_pairs]
    avg = sum(strengths) / len(strengths) if strengths else 0.0
    max_pair = max(ent_pairs, key=lambda p: p[2]) if ent_pairs else None
    return {
        "average_strength": round(avg, 3),
        "strongest_pair": {
            "language": max_pair[0] if max_pair else None,
            "bond_name": max_pair[1] if max_pair else None,
            "strength": max_pair[2] if max_pair else 0.0,
        } if max_pair else None,
    }


def build_uncertainty_bar(uncertainty_product: float, max_val: float = 12.0) -> str:
    """Build an ASCII bar representing uncertainty level."""
    ratio = min(uncertainty_product / max_val, 1.0)
    filled = int(ratio * 20)
    return "█" * filled + "░" * (20 - filled)


def build_wave_function_bar(components: List[Tuple[str, float]]) -> str:
    """Build a horizontal bar showing paradigm superposition distribution."""
    bars = []
    for name, weight in components:
        filled = int(weight * 20)
        bar = "▓" * filled + "░" * (20 - filled)
        bars.append(f"{bar} {weight:.0%} {name}")
    return "\n".join(bars)


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def quantum() -> Dict[str, Any]:
    """
    Main entry point: advance rotation, pick the language,
    run quantum analysis, return results.
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

    # Get quantum system data
    qdata = QUANTUM_SYSTEMS.get(current_language, {})
    ent_pairs = qdata.get("entanglement_pairs", [])
    ent_metrics = compute_entanglement_strength(ent_pairs)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": current_language,
        "quantum_glyph": qdata.get("quantum_glyph", "⚛️"),
        "orbital_config": qdata.get("orbital_config", "unknown"),
        "wave_function": qdata.get("wave_function", []),
        "ground_state": qdata.get("ground_state", "Unknown State"),
        "excited_states": qdata.get("excited_states", []),
        "uncertainty_principle": qdata.get("uncertainty_principle", {}),
        "decoherence_pattern": qdata.get("decoherence_pattern", {}),
        "entanglement_pairs": [
            {
                "language": p[0],
                "bond_name": p[1],
                "strength": p[2],
                "explanation": p[3],
            }
            for p in ent_pairs
        ],
        "entanglement_metrics": ent_metrics,
        "hamiltonian": qdata.get("hamiltonian", {}),
        "uncertainty_product": qdata.get("uncertainty_product", 0.0),
        "uncertainty_bar": build_uncertainty_bar(qdata.get("uncertainty_product", 0.0)),
        "superposition_cardinality": qdata.get("superposition_cardinality", 0),
        "collapse_mechanism": qdata.get("collapse_mechanism", "unknown"),
        "measurement_disturbance": qdata.get("measurement_disturbance", ""),
        "quantum_description": qdata.get("quantum_description", ""),
        "wave_function_bar": build_wave_function_bar(qdata.get("wave_function", [])),
        "rotation_order": ROTATION_ORDER,
        "next_language": languages[next_index % len(languages)],
        "next_index": next_index,
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def run_tests() -> None:
    """Run all tests for the Polyglot Quantum module."""
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

    print("⚛️ Polyglot Quantum -- Running Tests\n")

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

    # -- QUANTUM_SYSTEMS ------------------------------------------------------
    t("QUANTUM_SYSTEMS has 8 entries", len(QUANTUM_SYSTEMS) == 8)
    for lang in ROTATION_ORDER:
        t(f"QUANTUM_SYSTEMS has entry for '{lang}'", lang in QUANTUM_SYSTEMS)

    # -- Required fields per language -----------------------------------------
    required_fields = [
        "wave_function", "ground_state", "excited_states",
        "uncertainty_principle", "decoherence_pattern",
        "entanglement_pairs", "hamiltonian", "uncertainty_product",
        "quantum_description", "quantum_glyph", "orbital_config",
        "superposition_cardinality", "collapse_mechanism",
        "measurement_disturbance",
    ]
    for lang in ROTATION_ORDER:
        entry = QUANTUM_SYSTEMS[lang]
        for field in required_fields:
            t(f"  '{lang}' has '{field}'", field in entry, f"missing {field}")

    # -- Wave function validity -----------------------------------------------
    for lang in ROTATION_ORDER:
        wf = QUANTUM_SYSTEMS[lang]["wave_function"]
        t(f"  '{lang}' wave_function is non-empty", len(wf) > 0)
        total = sum(w for _, w in wf)
        t(f"  '{lang}' wave_function weights sum to ~1.0 ({total:.2f})", 0.99 <= total <= 1.01, f"sum={total}")

    # -- Entanglement pairs validity ------------------------------------------
    for lang in ROTATION_ORDER:
        pairs = QUANTUM_SYSTEMS[lang]["entanglement_pairs"]
        t(f"  '{lang}' has entanglement_pairs", isinstance(pairs, list))
        for p in pairs:
            t(f"  '{lang}' pair '{p[0]}' has 4 elements", len(p) == 4, str(p))
            t(f"  '{lang}' pair '{p[0]}' strength in [0,1]", 0.0 <= p[2] <= 1.0, str(p[2]))

    # -- Uncertainty product range --------------------------------------------
    for lang in ROTATION_ORDER:
        up = QUANTUM_SYSTEMS[lang]["uncertainty_product"]
        t(f"  '{lang}' uncertainty_product >= 0", up >= 0.0)
        t(f"  '{lang}' uncertainty_product reasonable (<= 15)", up <= 15.0)

    # -- superposition_cardinality range ------------------------------------
    for lang in ROTATION_ORDER:
        sc = QUANTUM_SYSTEMS[lang]["superposition_cardinality"]
        t(f"  '{lang}' superposition_cardinality >= 1", sc >= 1)
        t(f"  '{lang}' superposition_cardinality <= 15", sc <= 15)

    # -- collapse_mechanism is a non-empty string ----------------------------
    for lang in ROTATION_ORDER:
        cm = QUANTUM_SYSTEMS[lang]["collapse_mechanism"]
        t(f"  '{lang}' collapse_mechanism is non-empty", len(cm) > 0)

    # -- quantum() advances rotation -----------------------------------------
    try:
        cfg_before = load_rotation()
        idx_before = cfg_before["current_index"]
        lang_before = cfg_before["languages"][idx_before % len(cfg_before["languages"])]
        result = quantum()
        cfg_after = load_rotation()
        idx_after = cfg_after["current_index"]
        t("quantum() advances current_index",
          idx_after == (idx_before + 1) % len(cfg_before["languages"]))
        t("quantum() returns rotation_advanced language", result.get("language") == lang_before)
        t("quantum() returns next_language", "next_language" in result)
        t("quantum() returns next_index", "next_index" in result)
    except Exception as e:
        t("quantum() rotation advancement", False, str(e))

    # -- quantum() result structure ------------------------------------------
    try:
        result = quantum()
        t("result is a dict", isinstance(result, dict))
        t("result has 'language' key", "language" in result)
        t("result has 'wave_function' key", "wave_function" in result)
        t("result has 'ground_state' key", "ground_state" in result)
        t("result has 'excited_states' key", "excited_states" in result)
        t("result has 'uncertainty_principle' key", "uncertainty_principle" in result)
        t("result has 'decoherence_pattern' key", "decoherence_pattern" in result)
        t("result has 'entanglement_pairs' key", "entanglement_pairs" in result)
        t("result has 'hamiltonian' key", "hamiltonian" in result)
        t("result has 'uncertainty_product' key", "uncertainty_product" in result)
        t("result has 'uncertainty_bar' key", "uncertainty_bar" in result)
        t("result has 'wave_function_bar' key", "wave_function_bar" in result)
        t("result has 'quantum_description' key", "quantum_description" in result)
        t("result has 'tool' key", "tool" in result)
        t("result has 'version' key", "version" in result)
        t("result has 'rotation_order' key", "rotation_order" in result)
        t("result['tool'] == 'polyglot-quantum'", result.get("tool") == TOOL_NAME)
        t("result['version'] == '1.0.0'", result.get("version") == TOOL_VERSION)
        t("result['next_language'] in rotation_order", result.get("next_language") in result.get("rotation_order", []))
        t("result['next_language'] != result['language']", result.get("next_language") != result.get("language"))
    except Exception as e:
        t("quantum() result structure", False, str(e))

    # -- uncertainty_bar validity --------------------------------------------
    for lang in ROTATION_ORDER:
        result = quantum()
        bar = result.get("uncertainty_bar", "")
        t(f"  uncertainty_bar for '{lang}' is a string", isinstance(bar, str))
        t(f"  uncertainty_bar for '{lang}' has correct length (20)", len(bar) == 20, f"len={len(bar)}")
        t(f"  uncertainty_bar for '{lang}' contains only █ and ░",
          all(c in "█░" for c in bar), f"chars={set(bar)}")

    # -- entanglement_metrics computed correctly ------------------------------
    result = quantum()
    em = result.get("entanglement_metrics", {})
    t("entanglement_metrics has 'average_strength'", "average_strength" in em)
    t("entanglement_metrics has 'strongest_pair'", "strongest_pair" in em)

    # -- C/C++ has highest uncertainty_product --------------------------------
    all_up = {lang: QUANTUM_SYSTEMS[lang]["uncertainty_product"] for lang in ROTATION_ORDER}
    t("C/C++ has highest uncertainty_product", all_up["C/C++"] == max(all_up.values()))
    t("Rust has lowest uncertainty_product", all_up["Rust"] == min(all_up.values()))

    # -- Wave function bar ----------------------------------------------------
    for lang in ROTATION_ORDER:
        result = quantum()
        wfb = result.get("wave_function_bar", "")
        t(f"  wave_function_bar for '{lang}' is a string", isinstance(wfb, str))
        t(f"  wave_function_bar for '{lang}' is non-empty", len(wfb) > 0)

    # -- Full cycle rotation ---------------------------------------------------
    try:
        cfg = load_rotation()
        langs = cfg["languages"]
        idx = cfg["current_index"]
        visited = []
        for i in range(len(langs)):
            cfg = load_rotation()
            idx = cfg["current_index"]
            lang = cfg["languages"][idx % len(langs)]
            visited.append(lang)
            cfg["current_index"] = (idx + 1) % len(langs)
            cfg["last_language"] = lang
            cfg["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
            save_rotation(cfg)
        expected = ROTATION_ORDER[:]
        t("Full cycle visits all languages in order", visited == expected)
    except Exception as e:
        t("Full cycle rotation test", False, str(e))

    print(f"\n{'='*55}")
    if errors:
        print(f"❌ {len(errors)} test(s) failed: {', '.join(errors)}")
        sys.exit(1)
    else:
        print(f"✅ All {passed} tests passed!")
        print("⚛️  The quantum systems are stable.")
        sys.exit(0)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        result = quantum()
        print(json.dumps(result, indent=2))
