"""
Polyglot Odyssey — Language Journey Tracker
A creative tool that tracks your programming language journey as a travelogue.
Each language is a destination; transitions are paradigm adventures.

Reads from language_rotation.json to advance the rotation, then generates
a narrative "journey leg" connecting the previous language to the next.
"""

from __future__ import annotations

import json
import random
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript →
#                  Java → C/C++ → Rust (loops)
# ---------------------------------------------------------------------------
ROTATION: list[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

STATE_FILE = Path.home() / ".openclaw/workspace/language_rotation.json"

# ---------------------------------------------------------------------------
# Paradigm data: what makes each language special, what concept it introduces
# ---------------------------------------------------------------------------
PARADIGM: dict[str, dict] = {
    "Rust": {
        "tagline": "The Guardian of Memory",
        "paradigm": "Systems / Zero-Cost Abstraction",
        "superpower": "Ownership & Borrowing",
        "motto": "Fearless concurrency",
        "companion": "a strict but fair teacher",
    },
    "Go": {
        "tagline": "The Minimalist Monk",
        "paradigm": "Concurrent / Procedural",
        "superpower": "Goroutines & Channels",
        "motto": "Simplicity is the ultimate sophistication",
        "companion": "a calm zen master",
    },
    "Swift": {
        "tagline": "The Safety Poet",
        "paradigm": "Protocol-Oriented / Functional",
        "superpower": "Optionals & Protocol Extensions",
        "motto": "Safe, fast, expressive",
        "companion": "an elegant writer",
    },
    "Kotlin": {
        "tagline": "The Pragmatic Sage",
        "paradigm": "Object-Oriented / Functional",
        "superpower": "Coroutines & Null Safety",
        "motto": "Better code, less boilerplate",
        "companion": "a pragmatic architect",
    },
    "TypeScript": {
        "tagline": "The Type Architect",
        "paradigm": "Static Typing / Object-Oriented",
        "superpower": "Structural Types & Generics",
        "motto": "JavaScript that scales",
        "companion": "a meticulous planner",
    },
    "JavaScript": {
        "tagline": "The Web Wanderer",
        "paradigm": "Dynamic / Prototype-Based",
        "superpower": "Async/Await & First-Class Functions",
        "motto": "The language of the web",
        "companion": "a creative improviser",
    },
    "Java": {
        "tagline": "The Enterprise Explorer",
        "paradigm": "Object-Oriented / Generic",
        "superpower": "Streams & Virtual Machine",
        "motto": "Write once, run anywhere",
        "companion": "a seasoned explorer",
    },
    "C/C++": {
        "tagline": "The Control Master",
        "paradigm": "Procedural / Systems",
        "superpower": "Pointers, RAII, Templates",
        "motto": "Maximum control, maximum responsibility",
        "companion": "an ancient wizard",
    },
}

# ---------------------------------------------------------------------------
# Transition narratives: how each language transitions to the next
# ---------------------------------------------------------------------------
TRANSITIONS: dict[tuple[str, str], str] = {
    ("Rust", "Go"):
        "You leave the borrow checker behind and discover the gentle simplicity "
        "of goroutines. Memory is still safe — but now you let the runtime "
        "share the burden. A weight lifts from your shoulders.",
    ("Go", "Swift"):
        "From Go's sparse package files you step into Swift's expressive terrain. "
        "Optionals feel like a foreign concept at first — but soon nil itself "
        "seems less frightening. You begin to appreciate the elegance of "
        "`guard let`.",
    ("Swift", "Kotlin"):
        "Swift showed you protocols; Kotlin opens the door to extension functions "
        "and coroutines. You traded optional chaining for null-safe operators. "
        "Both worlds feel like home now.",
    ("Kotlin", "TypeScript"):
        "Kotlin's JVM pragmatism meets TypeScript's structural types. "
        "You trade the JVM for a runtime, but gain the flexibility of a "
        "dynamic backbone with a static spine. The type annotations feel "
        "like scaffolding for creativity.",
    ("TypeScript", "JavaScript"):
        "You shed the type annotations and run freely through JavaScript's "
        "prototype chain. Callbacks rise from the dead as async/await — "
        "familiar yet transformed. The web was always your home.",
    ("JavaScript", "Java"):
        "The wild west of JS gives way to Java's structured ecosystem. "
        "Streams flow through your code now; generics add a new dimension "
        "to how you think about types. The JVM is vast and well-trodden.",
    ("Java", "C/C++"):
        "You descend to the bare metal. Pointers are back, the garbage collector "
        "is gone, and RAII stands guard where GC used to roam. You hold memory "
        "in your own two hands — with great power comes great responsibility.",
    ("C/C++", "Rust"):
        "The cycle completes: back to Rust, where the compiler checks what "
        "C/C++ leaves to discipline. Ownership is no longer a burden — it is "
        "a gift. You've traveled far enough to understand why Rust was built "
        "the way it was.",
}

# Fallback transitions
FALLBACK_FROM: dict[str, str] = {
    "Rust":     "You bid farewell to Rust's compiler校验.",
    "Go":       "You leave Go's channels behind.",
    "Swift":    "You step away from Swift's safe harbor.",
    "Kotlin":   "You depart from Kotlin's pragmatic shores.",
    "TypeScript":"You shed TypeScript's type armor.",
    "JavaScript":"You wave goodbye to the web's native tongue.",
    "Java":     "You depart from the JVM kingdom.",
    "C/C++":    "You turn away from bare metal.",
}

FALLBACK_TO: dict[str, str] = {
    "Rust":     "Rust awaits — memory safety with zero-cost abstractions.",
    "Go":       "Go beckons — simplicity and concurrency.",
    "Swift":    "Swift calls — safe, fast, expressive.",
    "Kotlin":   "Kotlin invites — pragmatic elegance.",
    "TypeScript":"TypeScript summons — scale with types.",
    "JavaScript":"JavaScript welcomes — the language of everywhere.",
    "Java":     "Java opens its arms — write once, run anywhere.",
    "C/C++":    "C/C++ calls — maximum control.",
}


# ---------------------------------------------------------------------------
# Waypoints: scenic stops to describe what to explore in each language
# ---------------------------------------------------------------------------
WAYPOINTS: dict[str, list[str]] = {
    "Rust": [
        "Lifetime annotations — the compiler's love letters",
        "The borrow checker — a strict guardian with your best interests at heart",
        "Pattern matching — exhaustive and elegant",
        "Traits — Rust's take on interfaces, done right",
    ],
    "Go": [
        "Goroutines — thousands of conversations happening at once",
        "Channels — the safe pipes between concurrent worlds",
        "Defer — cleaning up after yourself, automatically",
        "The gofmt tool — one style to rule them all",
    ],
    "Swift": [
        "Optionals — making nil impossible to ignore",
        "Protocol extensions — default behaviour, elegantly composed",
        "Result type — errors as values, not exceptions",
        "SwiftUI's declarative DSL — UI as a function of state",
    ],
    "Kotlin": [
        "Extension functions — adding methods to types you don't own",
        "Coroutines — async code that reads like sync",
        "Data classes — POJOs that write themselves",
        "Sealed classes — exhaustive when/else expressions",
    ],
    "TypeScript": [
        "Structural types — compatibility by shape, not name",
        "Conditional types — types that compute",
        "Template literal types — types that spell things out",
        "Utility types — Partial, Required, Pick on demand",
    ],
    "JavaScript": [
        "Closures — functions that remember their birthplace",
        "The event loop — single-threaded but never idle",
        "Prototypal inheritance — objects inheriting from objects",
        "Destructuring & spread — unpacking the world",
    ],
    "Java": [
        "Streams — functional-style pipelines over collections",
        "Generics — types that parameterize other types",
        "The ClassLoader — loading classes on demand",
        "CompletableFuture — composing asynchronous operations",
    ],
    "C/C++": [
        "RAII — resources acquired in constructor, released in destructor",
        "Templates — compile-time polymorphism with zero runtime cost",
        "Smart pointers — RAII wrappers for dynamic memory",
        "Move semantics — transferring ownership without copying",
    ],
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class JourneyEntry:
    leg: int
    from_lang: str
    to_lang: str
    transition_story: str
    waypoints: list[str]
    timestamp: str


@dataclass
class OdysseyState:
    languages: list[str]
    current_index: int
    last_language: str
    updated_at: str
    total_legs: int = 0
    journey_log: list[JourneyEntry] = field(default_factory=list)

    @classmethod
    def load(cls, path: Path) -> OdysseyState:
        if not path.exists():
            # Bootstrap from defaults
            return cls(
                languages=ROTATION,
                current_index=0,
                last_language="C/C++",  # so first advance lands on Rust
                updated_at=datetime.now(timezone.utc).isoformat(),
            )
        with open(path) as f:
            data = json.load(f)
        log = [
            JourneyEntry(
                leg=e["leg"],
                from_lang=e["from_lang"],
                to_lang=e["to_lang"],
                transition_story=e["transition_story"],
                waypoints=e.get("waypoints", []),
                timestamp=e["timestamp"],
            )
            for e in data.get("journey_log", [])
        ]
        return cls(
            languages=data.get("languages", ROTATION),
            current_index=data.get("current_index", 0),
            last_language=data.get("last_language", ""),
            updated_at=data.get("updated_at", ""),
            total_legs=data.get("total_legs", 0),
            journey_log=log,
        )

    def advance(self) -> tuple[str, str, str]:
        """Advance rotation, return (from_lang, to_lang, transition_story)."""
        last = self.last_language
        rotation = self.languages

        try:
            pos = rotation.index(last)
        except ValueError:
            pos = -1

        next_lang = rotation[(pos + 1) % len(rotation)]

        # Build transition narrative
        key = (last, next_lang)
        if key in TRANSITIONS:
            story = TRANSITIONS[key]
        else:
            story = (
                f"{FALLBACK_FROM.get(last, 'Leaving ' + last)}. "
                f"{FALLBACK_TO.get(next_lang, 'Arriving at ' + next_lang)}"
            )

        # Pick 2 scenic waypoints
        all_waypoints = WAYPOINTS.get(next_lang, [])
        chosen = random.sample(all_waypoints, min(2, len(all_waypoints)))

        self.total_legs += 1
        entry = JourneyEntry(
            leg=self.total_legs,
            from_lang=last,
            to_lang=next_lang,
            transition_story=story,
            waypoints=chosen,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.journey_log.append(entry)

        # Update rotation state
        self.current_index = (self.current_index + 1) % len(rotation)
        self.last_language = next_lang
        self.updated_at = datetime.now(timezone.utc).isoformat()

        return last, next_lang, story, chosen, entry.leg

    def save(self, path: Path) -> None:
        data = {
            "languages": self.languages,
            "current_index": self.current_index,
            "last_language": self.last_language,
            "updated_at": self.updated_at,
            "total_legs": self.total_legs,
            "journey_log": [
                {
                    "leg": e.leg,
                    "from_lang": e.from_lang,
                    "to_lang": e.to_lang,
                    "transition_story": e.transition_story,
                    "waypoints": e.waypoints,
                    "timestamp": e.timestamp,
                }
                for e in self.journey_log
            ],
        }
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        tmp.rename(path)


def format_odyssey(from_lang: str, to_lang: str, story: str,
                   waypoints: list[str], leg: int) -> str:
    from_info = PARADIGM.get(from_lang, {})
    to_info = PARADIGM.get(to_lang, {})

    lines = [
        "",
        f"  ╔══════════════════════════════════════════════════╗",
        f"  ║       POLYGLOT ODYSSEY  ·  Leg #{leg:03d}          ║",
        f"  ╚══════════════════════════════════════════════════╝",
        "",
        f"  📍 From: {from_lang} — {from_info.get('tagline', '')}",
        f"     \"{from_info.get('motto', '')}\"",
        "",
        f"  ✈️  Departing...",
        "",
        f"  📖 The Journey:",
        f"  {story}",
        "",
        f"  🎯 Destination: {to_lang} — {to_info.get('tagline', '')}",
        f"     Paradigm: {to_info.get('paradigm', '')}",
        f"     Superpower: {to_info.get('superpower', '')}",
        f"     \"{to_info.get('motto', '')}\"",
        "",
        f"  🗺️  Scenic Waypoints in {to_lang}:",
    ]
    for w in waypoints:
        lines.append(f"    · {w}")

    lines += [
        "",
        f"  👤 Your guide: {to_info.get('companion', 'a fellow traveler')}",
        "",
        f"  Distance traveled: {leg} leg{'s' if leg != 1 else ''}",
        "",
    ]
    return "\n".join(lines)
