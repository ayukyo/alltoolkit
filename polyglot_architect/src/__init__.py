#! /usr/bin/env python3
"""
🏛️ Polyglot Architect v1.0
A creative tool that generates ASCII architectural blueprints showing how each
language "builds" solutions differently — visualized as distinct architectural
styles spanning brutalism, gothic, baroque, modernism, and more.

Creative concept: "Every language has its own architectural philosophy when
solving the same problem. A memory-safe system looks like clean brutalist
concrete. A garbage-collected runtime looks like a baroque palace with ornate
gardens hiding the GC caretaker. A functional pipeline looks like a Japanese
zen garden. Polyglot Architect renders these as ASCII floor plans and 3D
perspectives, letting you compare how different languages construct identical
mental buildings."

Each run selects the current rotation language and renders an ASCII blueprint
for that language's approach to the current CONCEPT THEME.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import math
import random
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-architect"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
    "language_rotation.json"
)

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ─────────────────────────────────────────────────────────────────────────────
# Architectural Concept Themes — each is a universal programming concept
# ─────────────────────────────────────────────────────────────────────────────
# Each theme has:
#   - id / name / emoji
#   - description: the conceptual question
#   - per-language "architecture" dict with:
#       - style: architectural style name
#       - materials: what the building is made of
#       - floors: number of conceptual layers
#       - footprint: 2D layout shape
#       - features: list of architectural features (as ASCII symbols)
#       - foundation: how the language grounds this concept
#       - load_bearing: the core structural element
#       - facade_pattern: the visible pattern on the building face
#       - blueprint_lines: raw ASCII blueprint lines for the building

ARCHITECTURAL_THEMES: List[Dict[str, Any]] = [
    {
        "id": "memory_safety",
        "name": "Memory Safety Building",
        "emoji": "🏗️",
        "question": "How does the language construct a safe memory dwelling?",
        "languages": {
            "Rust": {
                "style": "Brutalist Concrete",
                "materials": "Monolithic ownership contracts, borrow checker rebar",
                "floors": 3,
                "footprint": "compact_sturdy",
                "foundation": "Ownership algebra — statically proven non-aliasing",
                "load_bearing": "Lifetime annotations (rebar)",
                "facade_pattern": "░░▓▓██▓▓░░",
                "description": "Stark concrete walls — no hidden GC, no runtime cost. "
                               "Every wall load-bearing by compile-time proof.",
                "blueprint": [
                    "     ┌──────────────┐     ",
                    "     │ ░░▓▓██▓▓░░  │     ",
                    "  ┌──│──▓▓████▓▓──│──┐  ",
                    "  │  │  ████████  │  │  ",
                    "  │  │ ░░▓▓██▓▓░░ │  │  ",
                    "  │  │──▓▓████▓▓──│  │  ",
                    "  │  │  ████████  │  │  ",
                    "  └──│──▓▓████▓▓──│──┘  ",
                    "     │  ░░▓▓██▓▓░░  │     ",
                    "     └──────────────┘     ",
                    "   [BORROW CHECKER CORE]    ",
                ],
            },
            "Go": {
                "style": "Glass Tower with Steel Frame",
                "materials": "Goroutine glass panels, pointer steel beams",
                "floors": 4,
                "footprint": "tall_slim",
                "foundation": "nil safety via zero-value + map idiom",
                "load_bearing": "Interface{vtable} steel columns",
                "facade_pattern": "┌─┬─┬─┬─┐",
                "description": "Sleek glass curtain walls — you can see through everything. "
                               "Steel frame (interfaces) holds it up. GC is the night janitor.",
                "blueprint": [
                    "   ┌─┬─┬─┬─┐  ",
                    "   │ │ │ │ │  ",
                    "   ├─┼─┼─┼─┤  ",
                    "   │ │ │ │ │  ",
                    "   ├─┼─┼─┼─┤  ",
                    "   │ │ │ │ │  ",
                    "   ├─┼─┼─┼─┤  ",
                    "   │ │ │ │ │  ",
                    "   └─┴─┴─┴─┘  ",
                    " ┌───────────┐ ",
                    " │ GC JANITOR │ ",
                    " └───────────┘ ",
                ],
            },
            "Swift": {
                "style": "Copy-on-Write Modernist Villa",
                "materials": "Value type marble, ARC marble pillars",
                "floors": 2,
                "footprint": "wide_elegant",
                "foundation": "ARC — automatic reference counting pillars",
                "load_bearing": "Copy-on-write marble slabs",
                "facade_pattern": "══╪══╪══",
                "description": "Elegant modernist villa — clean lines, every room a copy. "
                               "ARC butlers maintain pillar refcounts silently.",
                "blueprint": [
                    "  ╔══════════════╗  ",
                    "  ║  ══╪══╪══    ║  ",
                    "  ║────╬────╬────║  ",
                    "  ║  ══╪══╪══    ║  ",
                    "  ╠══════════════╣  ",
                    "  ║  [ARC PILLARS] ║  ",
                    "  ╚══════════════╝  ",
                ],
            },
            "Kotlin": {
                "style": "Scandinavian Functional Townhouse",
                "materials": "Immutable brick, nullable garden paths",
                "floors": 3,
                "footprint": "terraced_row",
                "foundation": "val/var foundation — immutability by default",
                "load_bearing": "Coroutines elevator shaft",
                "facade_pattern": "▓▓▓▓▓▓▓▓",
                "description": "Clean Scandinavian design — white brick, functional furniture. "
                               "Nullable T? paths wind through the garden.",
                "blueprint": [
                    "  ▓▓▓▓▓▓▓▓  ",
                    "  ▓  ▓  ▓  ",
                    "  ▓▓▓▓▓▓▓▓  ",
                    "  ▓  ▓  ▓  ",
                    "  ▓▓▓▓▓▓▓▓  ",
                    "  [COROUTINE SHAFT]",
                ],
            },
            "TypeScript": {
                "style": "Flexible Open-Plan Loft",
                "materials": "Structural typing glass bricks, interface ductwork",
                "floors": 5,
                "footprint": "open_plan",
                "foundation": "Structural typing — any brick fits the mold",
                "load_bearing": "Type annotations as temporary scaffolding",
                "facade_pattern": "┏━┓┏━┓┏━┓",
                "description": "Open-plan loft with glass brick walls — you can reconfigure "
                               "any room at runtime. Scaffolding comes down at compile time.",
                "blueprint": [
                    "  ┏━┓┏━┓┏━┓  ",
                    "  ┗━┛┗━┛┗━┛  ",
                    "  ┏━┓┏━┓┏━┓  ",
                    "  ┗━┛┗━┛┗━┛  ",
                    "  ┏━┓┏━┓┏━┓  ",
                    "  [RUNTIME DUCTS]",
                ],
            },
            "JavaScript": {
                "style": "Convertible Camper Van",
                "materials": "Prototypal van shell, closures as storage cubes",
                "floors": 1,
                "footprint": "compact_wheeled",
                "foundation": "Prototype chain — all wheels connect to Object.root",
                "load_bearing": "Closures as the cargo tie-down straps",
                "facade_pattern": "▔▔▔▔▔▔▔▔",
                "description": "A camper van — everything moves, nothing is bolted down. "
                               "You can reconfigure the whole layout at a rest stop.",
                "blueprint": [
                    "  ┌────────────┐▔▔▔▔",
                    "  │ [CLOSURES] │████│",
                    "  │  STORAGE   │████│",
                    "  └────────────┘████│",
                    "  ○  ○  ○  ○    ○  ○",
                ],
            },
            "Java": {
                "style": "Grand Baroque Palace with Hidden GC Staff",
                "materials": "Class marble, object gold leaf, GC groundskeepers",
                "floors": 6,
                "footprint": "grand_symmetrical",
                "foundation": "Class hierarchy — aristocrat blueprint room assignments",
                "load_bearing": "Interface marble columns (abstraction orders)",
                "facade_pattern": "╔╗╔╗╔╗╔╗",
                "description": "A grand baroque palace — opulent marble halls, gold-trimmed "
                               "objects. Hidden GC staff sweep the halls between guests.",
                "blueprint": [
                    "  ╔╗  ╔╗  ╔╗  ╔╗  ",
                    "  ╠╣  ╠╣  ╠╣  ╠╣  ",
                    "  ║║  ║║  ║║  ║║  ",
                    "  ╠╣  ╠╣  ╠╣  ╠╣  ",
                    "  ║║  ║║  ║║  ║║  ",
                    "  ╠╣  ╠╣  ╠╣  ╠╣  ",
                    "  ╚╝  ╚╝  ╚╝  ╚╝  ",
                    "  [GC GARDENERS BELOW]",
                ],
            },
            "C/C++": {
                "style": "RAW Concrete Bunker with Exposed Rebar",
                "materials": "Raw pointer concrete, manual rebar placement",
                "floors": 1,
                "footprint": "flat_slab",
                "foundation": "Undefined behavior quicksand — you're the engineer",
                "load_bearing": "Raw pointers as load-bearing steel beams",
                "facade_pattern": "▓▓▓▓▓▓▓▓",
                "description": "An exposed rebar bunker — you pour every beam yourself. "
                               "No GC, no safety net. UB quicksand beneath the slab.",
                "blueprint": [
                    "  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ",
                    "  ▓ [RAW REBAR] ▓  ",
                    "  ▓  [POINTER   ▓  ",
                    "  ▓   BEAMS]    ▓  ",
                    "  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ",
                    "  ░░UB QUICKSAND░░  ",
                ],
            },
        },
    },
    {
        "id": "concurrency",
        "name": "Concurrency Highway System",
        "emoji": "🛣️",
        "question": "How does the language design its concurrent traffic system?",
        "languages": {
            "Rust": {
                "style": "Automated Maglev Train Network",
                "materials": "Send/Sync track rails, async maglev pods",
                "floors": 2,
                "footprint": "network_mesh",
                "foundation": "Send/Sync trait tracks — compiler-verified lanes",
                "load_bearing": "async/await maglev terminals",
                "facade_pattern": "═══╦═══╦═══",
                "description": "A maglev network where the track layout is verified before "
                               "construction. Deadlocks impossible by structural design.",
                "blueprint": [
                    "  ═══╦═══╦═══  ",
                    "  ═══╬═══╬═══  ",
                    "  ═══╦═══╦═══  ",
                    "  ═══╬═══╬═══  ",
                    "  [SEND/SYNC TRACKS]",
                    "  ═══╩═══╩═══  ",
                ],
            },
            "Go": {
                "style": "Goroutine Bus Rapid Transit",
                "materials": "Goroutine buses, channel bus lanes",
                "floors": 3,
                "footprint": "arterial_grid",
                "foundation": "CSP channels as dedicated bus lanes",
                "load_bearing": "select() intersection controller",
                "facade_pattern": "┌──┬──┬──┐",
                "description": "A city-wide BRT system — cheap goroutine buses run on "
                               "dedicated channel lanes. select() is the traffic controller.",
                "blueprint": [
                    "  ┌──┬──┬──┐  ",
                    "  │▓▓│▓▓│▓▓│  ",
                    "  ├──┼──┼──┤  ",
                    "  │▓▓│▓▓│▓▓│  ",
                    "  ├──┼──┼──┤  ",
                    "  │▓▓│▓▓│▓▓│  ",
                    "  └──┴──┴──┘  ",
                    "  [SELECT CONTROLLER]",
                ],
            },
            "Swift": {
                "style": "Actor Isolation Islands",
                "materials": "Actor islands, Swift 6 isolation barriers",
                "floors": 2,
                "footprint": "island archipelago",
                "foundation": "Actor isolation — each island self-contained",
                "load_bearing": "async/await ferry network",
                "facade_pattern": "◎─◎─◎─◎─◎",
                "description": "A chain of islands connected by ferries. Each island "
                               "handles its own state — no shared bridges allowed.",
                "blueprint": [
                    "  ◎──◎──◎──◎  ",
                    "  ╱ ╲╱ ╲╱ ╲  ",
                    "  ◎  ◎  ◎  ◎  ",
                    "  ╲ ╱╲ ╱╲ ╱  ",
                    "  ◎──◎──◎──◎  ",
                    "  [ACTOR FERRIES]",
                ],
            },
            "Kotlin": {
                "style": "Suspend Coroutine Ski Lift",
                "materials": "Suspend functions as cable cars, Flow as ski slope streams",
                "floors": 2,
                "footprint": "vertical_resort",
                "foundation": "Structured concurrency — one lift per scope",
                "load_bearing": "Coroutine scope as resort management",
                "facade_pattern": "║║║║║║║║",
                "description": "A ski resort where suspend cable cars carry you up. "
                               "Flow streams are the ski slopes rushing back down.",
                "blueprint": [
                    "  ║  ║  ║  ║  ",
                    "  ║  ║  ║  ║  ",
                    "  ║  ║  ║  ║  ",
                    "  ▼▼▼▼▼▼▼▼  ",
                    "  [COROUTINE RESORT]",
                ],
            },
            "TypeScript": {
                "style": "Single-Threaded Subway Loop",
                "materials": "Event loop tunnel, Promise queue cars",
                "floors": 1,
                "footprint": "loop_circular",
                "foundation": "Call stack as the metro map",
                "load_bearing": "async/await subway cars on circular track",
                "facade_pattern": "○──○──○──○",
                "description": "A one-track subway loop — everything runs on the same "
                               "track. Microtasks queue at stations before boarding.",
                "blueprint": [
                    "  ○──○──○──○  ",
                    "  ╱         ╲  ",
                    "  ○    ◉    ○  ",
                    "  ╲         ╱  ",
                    "  ○──○──○──○  ",
                    "  [EVENT LOOP HUB]",
                ],
            },
            "JavaScript": {
                "style": "Single-Threaded Subway Loop",
                "materials": "Event loop tunnel, Promise queue cars",
                "floors": 1,
                "footprint": "loop_circular",
                "foundation": "Call stack as the metro map",
                "load_bearing": "Promise microtask queue as station master",
                "facade_pattern": "○──○──○──○",
                "description": "A one-track subway loop — everything runs on the same "
                               "track. Microtasks queue at stations before boarding.",
                "blueprint": [
                    "  ○──○──○──○  ",
                    "  ╱         ╲  ",
                    "  ○    ◉    ○  ",
                    "  ╲         ╱  ",
                    "  ○──○──○──○  ",
                    "  [PROMISE STATION]",
                ],
            },
            "Java": {
                "style": "Thread Pool Highway with Toll Booths",
                "materials": "Virtual thread toll booths, CompletableFuture exits",
                "floors": 3,
                "footprint": "highway_grid",
                "foundation": "ThreadPoolExecutor as highway authority",
                "load_bearing": "ReentrantLock toll booth gates",
                "facade_pattern": "═╗═╗═╗═╗",
                "description": "A highway with virtual thread toll booths — Java 21+ cheaptoll "
                               "passes. CompletableFuture interchanges connect ramps.",
                "blueprint": [
                    "  ═╗  ═╗  ═╗  ═╗  ",
                    "  ═╝  ═╝  ═╝  ═╝  ",
                    "  ═╗  ═╗  ═╗  ═╗  ",
                    "  ═╝  ═╝  ═╝  ═╝  ",
                    "  [VIRTUAL THREAD TOLLS]",
                ],
            },
            "C/C++": {
                "style": "Manual Traffic Control Intersection",
                "materials": "std::thread raw asphalt, std::mutex traffic lights",
                "floors": 2,
                "footprint": "intersection_complex",
                "foundation": "You are the traffic engineer — no automatic signals",
                "load_bearing": "std::atomic crosswalk buttons",
                "facade_pattern": "┼┼┼┼┼┼┼┼",
                "description": "A complex intersection where you manually place every traffic "
                               "light and crosswalk button. UB is a rogue driver.",
                "blueprint": [
                    "  ┼┼┼┼┼┼┼┼┼┼┼  ",
                    "  ┼██████████┼  ",
                    "  ┼██████████┼  ",
                    "  ┼┼┼┼┼┼┼┼┼┼┼┼  ",
                    "  [MANUAL SIGNALS]",
                    "  ┼██████████┼  ",
                ],
            },
        },
    },
    {
        "id": "type_system",
        "name": "Type System Library",
        "emoji": "📚",
        "question": "How does the language organize its type library?",
        "languages": {
            "Rust": {
                "style": "Modular Stone Archive with Indexed Catalogs",
                "materials": "Traits as catalog indexes, monomorphized copies",
                "floors": 4,
                "footprint": "modular_stacks",
                "foundation": "Module system — each stack accessible by exact coordinate",
                "load_bearing": "Trait bounds as cross-reference indices",
                "facade_pattern": "│█│█│█│█│",
                "description": "A stone archive with precise catalog cards. Each book "
                               "instantiated per borrower — no shared copies.",
                "blueprint": [
                    "  │█│ │█│ │█│ │█│  ",
                    "  │█│ │█│ │█│ │█│  ",
                    "  ├─┤ ├─┤ ├─┤ ├─┤  ",
                    "  │█│ │█│ │█│ │█│  ",
                    "  ├─┤ ├─┤ ├─┤ ├─┤  ",
                    "  │█│ │█│ │█│ │█│  ",
                    "  [TRAIT INDEX HALL]",
                ],
            },
            "Go": {
                "style": "Open-Shelf Bookstore with Duck-Typed Tags",
                "materials": "Interfaces as shelf labels, struct as any book",
                "floors": 3,
                "footprint": "open_shelves",
                "foundation": "No generics pre-1.18 — tag shelves loosely",
                "load_bearing": "Interface shelf labels (Reader, Writer)",
                "facade_pattern": "┌──┐┌──┐┌──┐",
                "description": "An open bookstore — any book fits any shelf if it has the "
                               "right label. Generics added later as express shelving.",
                "blueprint": [
                    "  ┌──┐┌──┐┌──┐  ",
                    "  │▒▒││▒▒││▒▒│  ",
                    "  └──┘└──┘└──┘  ",
                    "  ┌──┐┌──┐┌──┐  ",
                    "  │▒▒││▒▒││▒▒│  ",
                    "  └──┘└──┘└──┘  ",
                    "  [INTERFACE LABELS]",
                ],
            },
            "Swift": {
                "style": "Generics Custom Print Shop",
                "materials": "Type parameters as custom print settings, protocols as templates",
                "floors": 2,
                "footprint": "print_shop",
                "foundation": "Generic type parameters as print setting dials",
                "load_bearing": "Protocol constraints as template masters",
                "facade_pattern": "╔══╤══╤══╗",
                "description": "A custom print shop where each setting dial configures "
                               "the exact output. Homogeneous output per template.",
                "blueprint": [
                    "  ╔══╤══╤══╗  ",
                    "  ║▓▓╪▓▓╪▓▓║  ",
                    "  ╠══╧══╧══╣  ",
                    "  ║[PROTOCOL] ║  ",
                    "  ╚══════════╝  ",
                ],
            },
            "Kotlin": {
                "style": "Reified Generic Medicine Cabinet",
                "materials": "Reified generics as labeled pill bottles, inline as pharmacy",
                "floors": 2,
                "footprint": "cabinet_grid",
                "foundation": "Declaration-site variance as shelf organization",
                "load_bearing": "inline functions as the pharmacy's compounding bench",
                "facade_pattern": "▓[T]▓[T]▓[T]▓",
                "description": "A medicine cabinet where each bottle is labeled T and "
                               "the pharmacist (inline) reads the label at compile time.",
                "blueprint": [
                    "  ▓[T]▓[T]▓[T]▓  ",
                    "  ▓[T]▓[T]▓[T]▓  ",
                    "  ▓[T]▓[T]▓[T]▓  ",
                    "  [INLINE PHARMACIST]",
                ],
            },
            "TypeScript": {
                "style": "Structural Typing Open Market",
                "materials": "Structural types as market stalls, conditional types as secret doors",
                "floors": 5,
                "footprint": "bazaar_grid",
                "foundation": "Structural typing — if it has the right shape, it fits",
                "load_bearing": "Conditional types as hidden passage operators",
                "facade_pattern": "┏┓┏┓┏┓┏┓",
                "description": "A vibrant bazaar where any stall fits if it has the right "
                               "shapes. Type erasure is the end-of-day cleanup crew.",
                "blueprint": [
                    "  ┏┓  ┏┓  ┏┓  ┏┓  ",
                    "  ┗┛  ┗┛  ┗┛  ┗┛  ",
                    "  ┏┓  ┏┓  ┏┓  ┏┓  ",
                    "  ┗┛  ┗┛  ┗┛  ┗┛  ",
                    "  [TYPE ERASURE CLEANUP]",
                ],
            },
            "JavaScript": {
                "style": "Dynamic Props Toy Store",
                "materials": "Objects as toy boxes, prototype chain as hand-me-down tags",
                "floors": 1,
                "footprint": "open_floor",
                "foundation": "Prototype chain — toys passed down from Object.root",
                "load_bearing": "Closures as toy storage bins",
                "facade_pattern": "▒▒▒▒▒▒▒▒",
                "description": "A toy store with no labels — every box open, every toy "
                               "accessible. Hand-me-down chain passes toys along.",
                "blueprint": [
                    "  ▒▒▒▒▒▒▒▒▒▒▒▒  ",
                    "  ▒  ▒  ▒  ▒  ▒  ",
                    "  ▒▒▒▒▒▒▒▒▒▒▒▒  ",
                    "  [PROTOTYPE HAND-ME-DOWNS]",
                ],
            },
            "Java": {
                "style": "Classified Archive with Type Erasure Quonset Hut",
                "materials": "Class hierarchy as filing rooms, wildcards as flexible folders",
                "floors": 4,
                "footprint": "hierarchical_rooms",
                "foundation": "Type erasure — classified stamps removed at door",
                "load_bearing": "Bounded wildcards (? extends T) as flexible folder labels",
                "facade_pattern": "╔═╗╔═╗╔═╗",
                "description": "A government archive with beautiful filing rooms. "
                               "A Quonset hut (erasure) sits at the back — stamps removed.",
                "blueprint": [
                    "  ╔═╗ ╔═╗ ╔═╗ ╔═╗  ",
                    "  ║▓║ ║▓║ ║▓║ ║▓║  ",
                    "  ╠═╣ ╠═╣ ╠═╣ ╠═╣  ",
                    "  ║▓║ ║▓║ ║▓║ ║▓║  ",
                    "  ╚═╝ ╚═╝ ╚═╝ ╚═╝  ",
                    "  [QUONSET HUT: ERASURE]",
                ],
            },
            "C/C++": {
                "style": "Template Master Craftsman's Workshop",
                "materials": "Templates as custom tool molds, SFINAE as craft techniques",
                "floors": 2,
                "footprint": "workshop_benches",
                "foundation": "Undefined behavior as the craftsman's risk budget",
                "load_bearing": "Concepts (C++20) as the workshop's quality control board",
                "facade_pattern": "▓▓▓▓▓▓▓▓",
                "description": "A master craftsman's workshop — every tool cast to exact "
                               "spec. UB is the risk you accept for bespoke craftsmanship.",
                "blueprint": [
                    "  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ",
                    "  ▓ [TEMPLATE] ▓  ",
                    "  ▓  [BENCHES]  ▓  ",
                    "  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ",
                    "  [CONCEPTS QC]",
                ],
            },
        },
    },
    {
        "id": "error_handling",
        "name": "Error Handling Clinic",
        "emoji": "🏥",
        "question": "How does the language treat its error patients?",
        "languages": {
            "Rust": {
                "style": "Surgical Theater with Exhaustive Case Plans",
                "materials": "Result<T, E> as surgical case plans, ? as automated sutures",
                "floors": 2,
                "footprint": "sterile_operatory",
                "foundation": "Result<T, E> — every failure scenario mapped at design",
                "load_bearing": "Match exhaustion as the surgical checklist",
                "facade_pattern": "░┌─┐░┌─┐░",
                "description": "A sterile surgical theater — every possible complication "
                               "documented in the case plan. No exceptions allowed in.",
                "blueprint": [
                    "  ░┌─┐░┌─┐░┌─┐░  ",
                    "  │║█║│║█║│║█║│  ",
                    "  ├─┴─┴─┴─┴─┴─┤  ",
                    "  │ ? OPERATOR│  ",
                    "  └───────────┘  ",
                    "  [RESULT SURGICAL TEAM]",
                ],
            },
            "Go": {
                "style": "Emergency Room with Error Code Pagers",
                "materials": "error interface as pagers, returned as last value",
                "floors": 3,
                "footprint": "triage_center",
                "foundation": "error interface — pagers beep on failure",
                "load_bearing": "nil = no emergency, non-nil = alert",
                "facade_pattern": "┌─┼─┼─┼─┐",
                "description": "An ER where every doctor carries an error pager. "
                               "nil means all clear. Non-nil means investigate.",
                "blueprint": [
                    "  ┌─┼─┼─┼─┼─┐  ",
                    "  │▓│▓│▓│▓│▓│  ",
                    "  ├─┼─┼─┼─┼─┤  ",
                    "  │▓│▓│▓│▓│▓│  ",
                    "  └─┴─┴─┴─┴─┘  ",
                    "  [ERROR PAGER HQ]",
                ],
            },
            "Swift": {
                "style": "throws Clinic with try/catch Examination Rooms",
                "materials": "throws as patient flag, Error protocol as diagnosis book",
                "floors": 2,
                "footprint": "clinic_rooms",
                "foundation": "throws functions — patient marked before entering",
                "load_bearing": "try/catch as examination room protocol",
                "facade_pattern": "╔╤╤╤╤╤╗",
                "description": "A clean clinic — every patient (function) declares if "
                               "they might throw. catch blocks examine symptoms.",
                "blueprint": [
                    "  ╔╤╤╤╤╤╤╤╗  ",
                    "  ║▓╪▓╪▓╪▓║  ",
                    "  ╠╧╧╧╧╧╧╧╣  ",
                    "  ║ try/catch ║  ",
                    "  ╚════════╝  ",
                ],
            },
            "Kotlin": {
                "style": "runCatching Pharmacy with Result Shelf",
                "materials": "runCatching as the sampling pharmacy, Result<T> as the shelf",
                "floors": 2,
                "footprint": "pharmacy_shelf",
                "foundation": "No checked exceptions — pharmacy open all hours",
                "load_bearing": "Result<T> as the medicine shelf",
                "facade_pattern": "┌─┈─┈─┈─┐",
                "description": "A pharmacy where runCatching samples any medicine. "
                               "Result<T> shelf holds success or failure pills.",
                "blueprint": [
                    "  ┌─┈─┈─┈─┈─┐  ",
                    "  │▓▓│▓▓│▓▓│  ",
                    "  ├─┈─┈─┈─┈─┤  ",
                    "  │ RESULT │  ",
                    "  └───────┘  ",
                    "  [RUN-CATCHING PHARMACIST]",
                ],
            },
            "TypeScript": {
                "style": "throw Rally with try/catch Security",
                "materials": "throw as rally speaker, try/catch as security checkpoint",
                "floors": 2,
                "footprint": "checkpoint",
                "foundation": "throw — anyone can take the mic, any type",
                "load_bearing": "Type erasure removes the mic check at runtime",
                "facade_pattern": "┏━┓┏━┓┏━┓",
                "description": "A public rally where anyone can grab the mic and shout. "
                               "Security (try/catch) handles whoever shows up.",
                "blueprint": [
                    "  ┏━┓  ┏━┓  ┏━┓  ",
                    "  ┃▓┃  ┃▓┃  ┃▓┃  ",
                    "  ┗━┛  ┗━┛  ┗━┛  ",
                    "  [TRY/CATCH SECURITY]",
                ],
            },
            "JavaScript": {
                "style": "throw Open Mic Night",
                "materials": "throw as open mic, unhandled rejections as silent no-shows",
                "floors": 1,
                "footprint": "open_mic",
                "foundation": "throw — untyped rage into the void",
                "load_bearing": "unhandled promise rejections as ghost performers",
                "facade_pattern": "▓▓▓▓▓▓▓▓",
                "description": "Open mic night — anyone throws, any type. Unhandled "
                               "promise rejections are silent no-shows.",
                "blueprint": [
                    "  ▓▓▓▓▓▓▓▓▓▓▓  ",
                    "  ▓ [OPEN MIC] ▓  ",
                    "  ▓ [SILENT   ▓  ",
                    "  ▓  NO-SHOWS] ▓  ",
                    "  ▓▓▓▓▓▓▓▓▓▓▓  ",
                ],
            },
            "Java": {
                "style": "Grand Hospital with Triage Exceptions",
                "materials": "Checked exceptions as mandatory pre-registration, unchecked as walk-ins",
                "floors": 5,
                "footprint": "hospital_wing",
                "foundation": "throws clause as pre-registration form",
                "load_bearing": "try/catch/finally as ward protocol",
                "facade_pattern": "╔╦╦╦╦╦╦╗",
                "description": "A grand hospital — checked exceptions must pre-register. "
                               "Unchecked walk-ins still get treated.",
                "blueprint": [
                    "  ╔╦╦╦╦╦╦╦╦╦╗  ",
                    "  ║█║█║█║█║║║  ",
                    "  ╠╬╬╬╬╬╬╬╬╬╣  ",
                    "  ║█║█║█║█║║║  ",
                    "  ╚╩╩╩╩╩╩╩╩╩╝  ",
                    "  [CHECKED ADMISSIONS]",
                ],
            },
            "C/C++": {
                "style": "DIY Field Hospital",
                "materials": "Return codes as symptom codes, errno as the whiteboard",
                "floors": 1,
                "footprint": "field_tent",
                "foundation": "Undefined behavior — the patient walks with a limp",
                "load_bearing": "return codes as the only symptom checklist",
                "facade_pattern": "▓▓▓▓▓▓▓▓",
                "description": "A field tent — you're the medic, nurse, and pharmacist. "
                               "errno is the whiteboard. UB is the patient who vanishes.",
                "blueprint": [
                    "  ▓▓▓▓▓▓▓▓▓▓▓▓  ",
                    "  ▓  [RETURN] ▓  ",
                    "  ▓  [CODES]  ▓  ",
                    "  ▓▓▓▓▓▓▓▓▓▓▓▓  ",
                    "  [errno WHITEBOARD]",
                ],
            },
        },
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# 3D Perspective renderer
# ─────────────────────────────────────────────────────────────────────────────

def _render_3d_perspective(
    blueprint_lines: List[str],
    style: str,
    width: int = 60,
) -> List[str]:
    """
    Render a simple 3D perspective of the blueprint using ASCII depth cues.
    This creates an isometric-ish view by adding depth lines and a "ground" plane.
    """
    lines: List[str] = []

    # Header
    style_label = f"[{style.upper()}]"
    lines.append(f"  ╭{'─' * (width - 4)}╮")
    lines.append(f"  │{' ' * ((width - len(style_label) - 2) // 2)}{style_label}{' ' * ((width - len(style_label) - 2) // 2)}│")
    lines.append(f"  ├{'─' * (width - 4)}┤")

    # Blueprint with perspective depth
    mid = width // 2
    for i, line in enumerate(blueprint_lines):
        depth = i * 0.5
        indent = int(depth)
        visible = min(len(line), width - 2 - indent * 2)
        if visible < len(line):
            line = line[:visible]
        prefix = " " * indent
        lines.append(f"  │{prefix}{line}{' ' * max(0, width - 2 - indent * 2 - len(line))}│")

    # Ground plane
    lines.append(f"  ├{'─' * (width - 4)}┤")
    ground_chars = list("▀▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▀")
    ground = "".join(random.choice(ground_chars) for _ in range(width - 4))
    lines.append(f"  │{ground}│")
    lines.append(f"  ╰{'─' * (width - 4)}╯")

    return lines


def _render_floor_plan(
    blueprint_lines: List[str],
    floors: int,
    footprint: str,
) -> List[str]:
    """Render a top-down floor plan with floor labels."""
    lines: List[str] = []

    if footprint == "compact_sturdy":
        # Compact grid
        for floor in range(floors, 0, -1):
            marker = f"F{floor}"
            lines.append(f"  ╔═══════════════════╗  {marker}")
            if blueprint_lines:
                lines.append(f"  ║ {blueprint_lines[min(floor - 1, len(blueprint_lines) - 1)]} ║")
            else:
                lines.append(f"  ║{' ' * 19}║")
            lines.append(f"  ╚═══════════════════╝")
    elif footprint == "tall_slim":
        for floor in range(floors, 0, -1):
            marker = f"F{floor}"
            lines.append(f"  ╔═════╗  {marker}")
            lines.append(f"  ║     ║")
            lines.append(f"  ╚═════╝")
    elif footprint == "wide_elegant":
        for floor in range(floors, 0, -1):
            marker = f"F{floor}"
            lines.append(f"  ╔═══════════════╗  {marker}")
            lines.append(f"  ║               ║")
            lines.append(f"  ╚═══════════════╝")
    elif footprint == "arterial_grid":
        for floor in range(floors, 0, -1):
            marker = f"F{floor}"
            lines.append(f"  ╔═══╦═══╦═══╗  {marker}")
            lines.append(f"  ║   ║   ║   ║")
            lines.append(f"  ╚═══╩═══╩═══╝")
    else:
        # Default: simple stacked floors
        for floor in range(floors, 0, -1):
            marker = f"F{floor}"
            lines.append(f"  ╔═══════════════╗  {marker}")
            if blueprint_lines and floor - 1 < len(blueprint_lines):
                lines.append(f"  ║ {blueprint_lines[floor - 1]} ║")
            else:
                lines.append(f"  ║{' ' * 17}║")
            lines.append(f"  ╚═══════════════╝")

    return lines


# ─────────────────────────────────────────────────────────────────────────────
# Rotation helpers
# ─────────────────────────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    """Load language rotation config."""
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


# ─────────────────────────────────────────────────────────────────────────────
# Core API
# ─────────────────────────────────────────────────────────────────────────────

def architect() -> Dict[str, Any]:
    """
    Main entry point: advance rotation, pick a concept theme,
    and return the full architectural analysis.
    """
    config = load_rotation()
    languages = config.get("languages", [])
    if not languages:
        raise ValueError("No languages found in rotation config")

    current_index = config.get("current_index", 0)
    current_language = languages[current_index % len(languages)]

    # Advance rotation for next run
    next_index = (current_index + 1) % len(languages)
    config["current_index"] = next_index
    config["last_language"] = current_language
    config["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation(config)

    # Cycle themes deterministically
    theme_idx = current_index % len(ARCHITECTURAL_THEMES)
    theme = ARCHITECTURAL_THEMES[theme_idx]

    result = generate_architectural_analysis(current_language, theme, languages)
    result["rotation_advanced"] = True
    result["next_language"] = languages[next_index]
    result["next_index"] = next_index
    return result


def generate_architectural_analysis(
    language: str,
    theme: Dict[str, Any],
    languages: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Generate architectural analysis for a language + theme."""
    langs = languages or ROTATION_ORDER
    theme_langs = theme.get("languages", {})

    if language not in theme_langs:
        raise ValueError(f"Language '{language}' not in theme '{theme['id']}'")

    arch = theme_langs[language]

    # Render 3D perspective
    perspective = _render_3d_perspective(
        arch.get("blueprint", []),
        arch["style"],
        width=52,
    )

    # Render floor plan
    floor_plan = _render_floor_plan(
        arch.get("blueprint", []),
        arch.get("floors", 1),
        arch.get("footprint", "default"),
    )

    # Build comparison across all languages on this theme
    comparisons: List[Dict[str, Any]] = []
    for lang in langs:
        if lang not in theme_langs:
            continue
        info = theme_langs[lang]
        comparisons.append({
            "language": lang,
            "style": info["style"],
            "materials": info["materials"],
            "floors": info.get("floors", 1),
            "footprint": info.get("footprint", "default"),
            "foundation": info["foundation"],
            "load_bearing": info["load_bearing"],
        })

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": language,
        "theme": {
            "id": theme["id"],
            "name": theme["name"],
            "emoji": theme["emoji"],
            "question": theme["question"],
        },
        "architecture": {
            "style": arch["style"],
            "materials": arch["materials"],
            "floors": arch.get("floors", 1),
            "footprint": arch.get("footprint", "default"),
            "foundation": arch["foundation"],
            "load_bearing": arch["load_bearing"],
            "facade_pattern": arch.get("facade_pattern", ""),
            "description": arch["description"],
        },
        "blueprint": arch.get("blueprint", []),
        "floor_plan": floor_plan,
        "perspective_view": perspective,
        "comparisons": comparisons,
        "rotation_order": ROTATION_ORDER,
    }


def format_architectural(m: Dict[str, Any]) -> str:
    """Format the architectural analysis as a human-readable string."""
    lang = m["language"]
    theme = m["theme"]
    arch = m["architecture"]
    perspective = m["perspective_view"]
    floor_plan = m["floor_plan"]
    comparisons = m["comparisons"]

    lines: List[str] = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  🏛️ POLYGLOT ARCHITECT — Language Architecture Blueprints         ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Language  : {lang:<48}║",
        f"║  Theme     : {theme['emoji']} {theme['name']:<44}║",
        f"║  Question  : {theme['question']:<45}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🏗️  ARCHITECTURAL PROFILE                                        ║",
        f"║  Style     : {arch['style']:<48}║",
        f"║  Materials : {arch['materials']:<45}║",
        f"║  Floors    : {arch['floors']:<48}║",
        f"║  Footprint : {arch['footprint']:<48}║",
        f"║  Foundation: {arch['foundation']:<45}║",
        f"║  Load Bear : {arch['load_bearing']:<45}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  📐 3D PERSPECTIVE VIEW                                          ║",
    ]

    for row in perspective:
        lines.append(f"║  {row} ║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🗺️  FLOOR PLAN                                                  ║",
    ]

    for row in floor_plan:
        lines.append(f"║  {row}   ║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  📋  CROSS-LANGUAGE COMPARISON                                   ║",
    ]

    for comp in comparisons:
        marker = "►" if comp["language"] == lang else " "
        lines.append(
            f"║  {marker} {comp['language']:<12} {comp['style']:<28}  {comp['floors']}F║"
        )
        lines.append(
            f"║         {comp['foundation']:<47}║"
        )

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🔄 ROTATION ORDER                                              ║",
        f"║  {' → '.join(ROTATION_ORDER):<58}║",
        "╚══════════════════════════════════════════════════════════════════╝",
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────────────

def run_tests() -> None:
    """Run all tests for the polyglot_architect module."""
    import sys

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

    print("🏛️ Polyglot Architect — Running Tests\n")

    # ── Rotation file ─────────────────────────────────────────────────────────
    try:
        config = load_rotation()
        t("load_rotation() returns valid dict", isinstance(config, dict))
        t("rotation has 'languages' key", "languages" in config)
        t("rotation has 'current_index' key", "current_index" in config)
    except Exception as e:
        t("load_rotation() succeeds", False, str(e))

    # ── ROTATION_ORDER ────────────────────────────────────────────────────────
    for lang in ROTATION_ORDER:
        t(f"ROTATION_ORDER contains '{lang}'", lang in ROTATION_ORDER)

    # ── ARCHITECTURAL_THEMES ─────────────────────────────────────────────────
    t("ARCHITECTURAL_THEMES has 4 themes", len(ARCHITECTURAL_THEMES) == 4)
    for theme in ARCHITECTURAL_THEMES:
        t(f"  Theme '{theme['id']}' has 'languages'", "languages" in theme)
        t(f"  Theme '{theme['id']}' has 'question'", "question" in theme)
        for lang, info in theme["languages"].items():
            t(f"    '{lang}' has style/materials/floors/foundation",
              all(k in info for k in ("style", "materials", "floors", "foundation", "load_bearing")))
            t(f"    '{lang}' has blueprint (list)",
              isinstance(info.get("blueprint", []), list))

    # ── Perspective and floor plan renderers ──────────────────────────────────
    for theme in ARCHITECTURAL_THEMES:
        for lang, info in theme["languages"].items():
            try:
                persp = _render_3d_perspective(info.get("blueprint", []), info["style"])
                t(f"3D perspective for '{lang}' succeeds", isinstance(persp, list) and len(persp) > 0)
            except Exception as e:
                t(f"3D perspective for '{lang}'", False, str(e))

            try:
                fp = _render_floor_plan(info.get("blueprint", []), info.get("floors", 1), info.get("footprint", "default"))
                t(f"Floor plan for '{lang}' succeeds", isinstance(fp, list) and len(fp) > 0)
            except Exception as e:
                t(f"Floor plan for '{lang}'", False, str(e))

    # ── generate_architectural_analysis ───────────────────────────────────────
    for theme in ARCHITECTURAL_THEMES:
        for lang in theme["languages"]:
            try:
                result = generate_architectural_analysis(lang, theme)
                t(f"generate_architectural_analysis('{lang}', '{theme['id']}') succeeds", True)
                t(f"  - has 'theme'", "theme" in result)
                t(f"  - has 'architecture'", "architecture" in result)
                t(f"  - has 'blueprint'", "blueprint" in result)
                t(f"  - has 'floor_plan'", "floor_plan" in result)
                t(f"  - has 'perspective_view'", "perspective_view" in result)
                t(f"  - has 'comparisons'", "comparisons" in result)
                t(f"  - comparisons is non-empty list", len(result["comparisons"]) > 0)
                t(f"  - blueprint is list", isinstance(result["blueprint"], list))
                t(f"  - floor_plan is list", isinstance(result["floor_plan"], list))
                t(f"  - perspective_view is list", isinstance(result["perspective_view"], list))
            except Exception as e:
                t(f"generate_architectural_analysis('{lang}', '{theme['id']}')", False, str(e))

    # ── architect() advances rotation ────────────────────────────────────────
    try:
        cfg_before = load_rotation()
        idx_before = cfg_before["current_index"]
        lang_before = cfg_before["languages"][idx_before % len(cfg_before["languages"])]
        result = architect()
        cfg_after = load_rotation()
        idx_after = cfg_after["current_index"]
        t("architect() advances current_index",
          idx_after == (idx_before + 1) % len(cfg_before["languages"]))
        t("architect() returns rotation_advanced=True",
          result.get("rotation_advanced") is True)
        t("architect() returns the selected language",
          result.get("language") == lang_before)
        t("architect() returns next_language",
          "next_language" in result)
        t("architect() returns next_index",
          "next_index" in result)
    except Exception as e:
        t("architect() rotation advancement", False, str(e))

    # ── format_architectural ──────────────────────────────────────────────────
    try:
        theme = ARCHITECTURAL_THEMES[0]
        lang = list(theme["languages"].keys())[0]
        m = generate_architectural_analysis(lang, theme)
        formatted = format_architectural(m)
        t("format_architectural() returns a string", isinstance(formatted, str))
        t("format_architectural() starts with box-drawing char", formatted.startswith("╔"))
        t("format_architectural() ends with box-drawing char", formatted.rstrip().endswith("╝"))
        t("format_architectural() contains the language name", lang in formatted)
        t("format_architectural() contains the theme name", theme["name"] in formatted)
    except Exception as e:
        t("format_architectural()", False, str(e))

    # ── Unknown language raises ValueError ────────────────────────────────────
    try:
        generate_architectural_analysis("Brainfuck", ARCHITECTURAL_THEMES[0])
        t("Unknown language raises ValueError", False, "did not raise")
    except ValueError:
        t("Unknown language raises ValueError", True)
    except Exception as e:
        t("Unknown language raises ValueError", False, f"wrong exception: {e}")

    # ── Rotation index wraps correctly ───────────────────────────────────────
    try:
        cfg = load_rotation()
        langs = cfg["languages"]
        idx = cfg["current_index"]
        for _ in range(len(langs) + 1):
            cfg = load_rotation()
            idx = cfg["current_index"]
            lang = cfg["languages"][idx % len(langs)]
            cfg["current_index"] = (idx + 1) % len(langs)
            cfg["last_language"] = lang
            cfg["updated_at"] = datetime.now(timezone.utc).isoformat()
            save_rotation(cfg)
        cfg_final = load_rotation()
        t("Rotation wraps after full cycle",
          cfg_final["current_index"] == (idx + len(langs) + 1) % len(langs))
    except Exception as e:
        t("Rotation wrap test", False, str(e))

    print(f"\n{'='*50}")
    if errors:
        print(f"❌ {len(errors)} test(s) failed: {', '.join(errors)}")
        sys.exit(1)
    else:
        print(f"✅ All {passed} tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        result = architect()
        print(format_architectural(result))