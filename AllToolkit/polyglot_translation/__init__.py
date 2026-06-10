#!/usr/bin/env python3
"""
🌏 Polyglot Translation v1.0

A creative tool that treats programming languages as living cultures —
generating "cultural translation cards" that show how idioms, proverbs,
and cultural expressions from one language map (or fail to map) to others.

Creative concept: "Every language has its own proverbs, mantras, and cultural
sayings. Polyglot Translation maps the untranslatable — the concepts that don't
survive crossing from one language to another."

Each run:
  1. Reads language_rotation.json, gets current rotation language
  2. Selects a cultural "expression" (idiom, mantra, war story, maxim)
     from that language's culture
  3. Maps it to all other languages in the rotation — showing:
     - Direct translation (equivalent concept)
     - Near-equivalent (requires adaptation)
     - Untranslatable (no native equivalent)
  4. Updates current_index and commits to git

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust

Distinct from existing tools:
  - polyglot_digest:      syntax-parallel snippets (same code, different syntax)
  - polyglot_bridges:     semantic problem→solution maps (concepts to solutions)
  - polyglot_resonator:   mental model frames (how each language THINKS)
  - polyglot_dna:         genetic trait mapping (static characteristics)
  - polyglot_chronicle:   daily history and trivia (temporal today)
  - polyglot_flavor:      sensory tasting notes (aesthetic texture)
  - polyglot_code_printer: code postcard aesthetic (visual code art)
  - language_sage:        idioms & tips (practical wisdom)
  - language_compass:     learning journey maps (future milestones)
  - language_archaeology: historical lineage (temporal depth)
  - language_ethos:       philosophical manifesto (belief/identity)

Translation is about CULTURAL LINGUISTICS — the unwritten social contracts,
memes, and cultural cargo that travels (or gets lost) when you move between
programming languages.
"""

import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-translation"
TOOL_VERSION = "1.0.0"

ROTATION_FILE = str(
    Path(__file__).parent.parent.parent / "language_rotation.json"
)

# The 8-language rotation sequence
ROTATION_ORDER = [
    "Rust",
    "Go",
    "Swift",
    "Kotlin",
    "TypeScript",
    "JavaScript",
    "Java",
    "C/C++",
]

# ── Cultural expression database per language ───────────────────────────────────
# Each language has multiple cultural expressions across categories:
#   idiom        — a saying about writing/code
#   mantra       — a developer mindset or rallying cry
#   war_story    — a cautionary tale from the community
#   maxim        — a first-principles truth
#   meme         — a well-known community joke or ironic self-deprecation

CULTURAL_DB: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
    "Rust": {
        "idiom": [
            {
                "text": "If it compiles, it's correct.",
                "context": "The borrow checker is your strict but brilliant mentor. Trust the errors.",
                "culture": "Rust culture values correctness above all. The compiler is not an obstacle but a collaborator.",
            },
            {
                "text": "Don't fight the borrow checker — listen to it.",
                "context": "Every lifetime error is the compiler trying to save you from a data race at 3 AM.",
                "culture": "Rustaceans believe the borrow checker has insights the programmer lacks at first glance.",
            },
            {
                "text": "Match your way to correctness.",
                "context": "Exhaustive pattern matching forces you to handle every case.",
                "culture": "Rust's type system and match are a power couple — together they make invalid states unrepresentable.",
            },
        ],
        "mantra": [
            {
                "text": "Zero-cost abstractions.",
                "context": "If you don't use it, you don't pay for it.",
                "culture": "The foundational promise: idiomatic Rust code should be as fast as hand-written C.",
            },
            {
                "text": "Fearless concurrency.",
                "context": "The compiler prevents data races at compile time.",
                "culture": "Rust is the only language that can honestly make this claim. Every other language says it metaphorically.",
            },
        ],
        "war_story": [
            {
                "text": "I spent three days fighting the borrow checker over aRc<Mutex<T>>.",
                "context": "The fix was restructuring the ownership graph — not the code, but how I thought about it.",
                "culture": "The Rust learning curve is legendary. Every veteran has a borrow checker story.",
            },
        ],
        "maxim": [
            {
                "text": "Ownership is not hoarding; it's stewardship.",
                "context": "You don't own data — you care for it. When you're done, you pass it on.",
                "culture": "Rust's ownership model is a philosophy disguised as a feature.",
            },
        ],
        "meme": [
            {
                "text": "My program won't compile, and it's 11 PM.",
                "context": "Classic. The compiler is the final judge.",
                "culture": "Rust memes are uniformly about the borrow checker being simultaneously frustrating and beloved.",
            },
        ],
    },
    "Go": {
        "idiom": [
            {
                "text": "Don't communicate by sharing memory; share memory by communicating.",
                "context": "Channels are Go's answer to shared-state concurrency. Goroutines talk, they don't fight.",
                "culture": "This is the Go community's most recited mantra — the zen of Go.",
            },
            {
                "text": "If a function returns an error, handle it or propagate it — never ignore it.",
                "context": "Go has no exceptions. Errors are values. Deal with them.",
                "culture": "Go's error handling forces explicit attention to failure modes.",
            },
            {
                "text": "Make the zero value useful.",
                "context": "Slices, maps, and channels are all valid when zero-initialized.",
                "culture": "Go's zero-value philosophy eliminates a large class of null pointer bugs.",
            },
        ],
        "mantra": [
            {
                "text": "Simplicity is complicated.",
                "context": "Rob Pike's famous observation — keeping things simple requires hard work.",
                "culture": "Go's simplicity is not accidental; it's the result of deliberate choices to exclude features.",
            },
        ],
        "war_story": [
            {
                "text": "We rewrote it in Go and it was 10x slower.",
                "context": "The goroutine model is cheap, but not free. The bottleneck was GC pauses.",
                "culture": "Go's garbage collector has improved dramatically, but it still has a 'GC pause' story.",
            },
        ],
        "maxim": [
            {
                "text": "The empty interface tells you nothing. The type assertion panics.",
                "context": "Interface{} was Go's pre-generics escape hatch. It's still a leap of faith.",
                "culture": "Go's type system is minimal by design. Generics (1.18+) helped, but the culture is still 'interface{} everything'.",
            },
        ],
        "meme": [
            {
                "text": "go fmt has never formatted a line of code anyone disagreed with.",
                "context": "The formatter is not configurable. And somehow, everyone is OK with this.",
                "culture": "Go's opinionated formatter is a social contract that somehow works.",
            },
        ],
    },
    "Swift": {
        "idiom": [
            {
                "text": "If let soothes the soul.",
                "context": "Optional binding turns a maybe-nil into a definite. The compiler sleeps easier.",
                "culture": "Swift's optionals are its most celebrated feature — nil safety as a first-class concept.",
            },
            {
                "text": "Protocols are the new inheritance.",
                "context": "Swift prefers composition over class hierarchies. Protocols over superclasses.",
                "culture": "Swift's protocol-oriented programming is its signature design philosophy.",
            },
        ],
        "mantra": [
            {
                "text": "Swift is a protocol-oriented language.",
                "context": "Apple's tagline, and a genuine design principle, not just marketing.",
                "culture": "Every Swift developer eventually 'gets' protocols. It's a rite of passage.",
            },
        ],
        "war_story": [
            {
                "text": "Retain cycles in closures nearly sank our app.",
                "context": "[weak self] is now typed automatically in Swift 5. Back then, it was a minefield.",
                "culture": "Swift memory management is ARC-based, and retain cycles in closures were the main pitfall.",
            },
        ],
        "maxim": [
            {
                "text": "Value types are cheap to copy. Reference types are cheap to share.",
                "context": "Choose struct for independence, class for shared identity.",
                "culture": "Swift's blend of value and reference types is a deliberate design that forces clarity about intent.",
            },
        ],
        "meme": [
            {
                "text": "It's just like Python, but compiled.",
                "context": "No. It's not. But we keep saying it anyway.",
                "culture": "Swift's syntax is approachable, but it's a deeply systems-oriented language underneath.",
            },
        ],
    },
    "Kotlin": {
        "idiom": [
            {
                "text": "Null is not a value — it's an absence.",
                "context": "Kotlin's type system makes nullability explicit in the type: String vs String?.",
                "culture": "Kotlin absorbed Java's null problems and solved them at the type level.",
            },
            {
                "text": "Extension functions let you pretend the standard library is yours.",
                "context": "Kotlin lets you add methods to any class without touching the original.",
                "culture": "Extension functions are Kotlin's most loved feature — they enable DSLs and readable APIs.",
            },
        ],
        "mantra": [
            {
                "text": "Pragmatic over purist.",
                "context": "Kotlin doesn't dogmatically enforce functional or OO — it lets you pick what fits.",
                "culture": "The Kotlin community's unofficial motto — pick the right tool in the right context.",
            },
        ],
        "war_story": [
            {
                "text": "Coroutines were the answer to everything — except backpressure.",
                "context": "We wrapped async in a try/catch and called it a day. Until the queue grew unbounded.",
                "culture": "Kotlin coroutines are powerful but require explicit backpressure thinking.",
            },
        ],
        "maxim": [
            {
                "text": "Data classes eliminate the ceremony of getters, setters, equals, hashCode, and toString.",
                "context": "One keyword. Done.",
                "culture": "Kotlin's data class is perhaps the most-loved syntactic sugar in the language.",
            },
        ],
        "meme": [
            {
                "text": "It's like Scala, but compiles before the heat death of the universe.",
                "context": "Kotlin compiles much faster than Scala. But we still tell this joke.",
                "culture": "Kotlin's fast incremental compilation is a genuine differentiator from Scala.",
            },
        ],
    },
    "TypeScript": {
        "idiom": [
            {
                "text": "TypeScript is JavaScript with training wheels — and the training wheels are actually good.",
                "context": "The gradual typing system means you can start loose and tighten up incrementally.",
                "culture": "TypeScript's type system is the most adopted optional type system in history.",
            },
            {
                "text": "If it compiles, it probably works at runtime.",
                "context": "TypeScript's types are erased. The runtime is still JavaScript.",
                "culture": "TypeScript's type system is a lint/contract tool, not a hard guarantee.",
            },
        ],
        "mantra": [
            {
                "text": "Propagate types, not values.",
                "context": "Structural typing means you only describe the shape you need.",
                "culture": "TypeScript's structural type system means compatibility is based on shape, not name.",
            },
        ],
        "war_story": [
            {
                "text": "We used 'any' for two years. Then we enabled strict mode. Everything broke simultaneously.",
                "context": "The 'any' escape hatch is real. And it has a cost.",
                "culture": "TypeScript's migration story often involves 'any' as a temporary fix that becomes permanent.",
            },
        ],
        "maxim": [
            {
                "text": "Type assertions are lies you tell the compiler.",
                "context": "as SomeType bypasses the type checker. Use with extreme caution.",
                "culture": "TypeScript's escape hatches are powerful but dangerous — they opt out of type safety.",
            },
        ],
        "meme": [
            {
                "text": "I don't trust JavaScript, but I trust TypeScript to generate it.",
                "context": "The type system as a code quality filter, not a guarantee.",
                "culture": "TypeScript developers have a love-hate relationship with the JavaScript they compile to.",
            },
        ],
    },
    "JavaScript": {
        "idiom": [
            {
                "text": "Everything is an object, except when it isn't.",
                "context": "Primitives (number, string, boolean) are coerced, not truly OO. typeof lies.",
                "culture": "JavaScript's object model is a historical artifact that requires memorization.",
            },
            {
                "text": " == or ===? Always ===. Always.",
                "context": "Type coercion == is a footgun. === checks value AND type.",
                "culture": "This is the first rule every JavaScript developer learns, usually after a bug.",
            },
        ],
        "mantra": [
            {
                "text": "The event loop is single-threaded. Everything else is async.",
                "context": "JavaScript runs on one thread. All I/O is non-blocking.",
                "culture": "JavaScript's concurrency model is unique — callbacks, promises, and async/await all feed the same event loop.",
            },
        ],
        "war_story": [
            {
                "text": "We shipped on a Friday. The callback queue filled up. Weekend was ruined.",
                "context": "Callback hell is real. Promises and async/await were the community's answer.",
                "culture": "JavaScript's callback-based async history created the 'pyramid of doom' — a rite of passage.",
            },
        ],
        "maxim": [
            {
                "text": "Hoisting: declarations rise, initializations don't.",
                "context": "var is hoisted but undefined until the assignment runs. const/let are TDZ.",
                "culture": "JavaScript's hoisting rules are the source of countless bugs and the reason for eslint.",
            },
        ],
        "meme": [
            {
                "text": "JavaScript: the language where 0.1 + 0.2 !== 0.3 is a feature.",
                "context": "IEEE 754 floating point. Everyone knows. Everyone is still surprised.",
                "culture": "This joke appears in nearly every JavaScript presentation's opening slide.",
            },
        ],
    },
    "Java": {
        "idiom": [
            {
                "text": "Write once, run anywhere — except on my machine.",
                "context": "JVM's promise of portability was real, but classpath hell is legendary.",
                "culture": "Java's 'write once, run anywhere' was revolutionary in 1995. The reality is more nuanced.",
            },
            {
                "text": "Checked exceptions: the feature everyone loves to hate.",
                "context": "Java forces you to declare or handle checked exceptions. It's verbose.",
                "culture": "Checked exceptions are Java's most controversial design decision — even Java itself has retreated from them.",
            },
        ],
        "mantra": [
            {
                "text": "Object-oriented, or it doesn't count.",
                "context": "Java is the language that made OOP mainstream. Everything is a class.",
                "culture": "Java's class-first design shaped two decades of enterprise software architecture.",
            },
        ],
        "war_story": [
            {
                "text": "The GC paused for 30 seconds and the traders noticed.",
                "context": "Early JVM garbage collectors were not suitable for low-latency trading systems.",
                "culture": "Java G1 and ZGC solved most of this, but the memory management anxiety persists.",
            },
        ],
        "maxim": [
            {
                "text": "A final class is a sealed contract.",
                "context": "final on classes means no subclasses. Immutability is a design decision.",
                "culture": "Java's final keyword is underused — effective Java style emphasizes immutability.",
            },
        ],
        "meme": [
            {
                "text": "Java is verbose. Enterprise Java is verboser.",
                "context": "Spring Boot helped, but the culture of ceremony takes time to shake.",
                "culture": "Java's boilerplate culture is the source of endless jokes and the Lombok library.",
            },
        ],
    },
    "C/C++": {
        "idiom": [
            {
                "text": "C: you have the memory, the pointer, and nothing else. Good luck.",
                "context": "No safety net. No bounds checks. No GC. Raw, honest, brutal.",
                "culture": "C's philosophy: the programmer is always right. The compiler tells you nothing.",
            },
            {
                "text": "Undefined behavior is not a bug — it's a feature of the C standard.",
                "context": "UB lets compilers optimize aggressively. It also means your program can do anything.",
                "culture": "C's UB culture is both a performance lever and the source of security vulnerabilities.",
            },
        ],
        "mantra": [
            {
                "text": "You pay for what you use.",
                "context": "C++'s zero-overhead principle: no hidden costs, no unnecessary abstractions.",
                "culture": "C++'s founding principle — if you don't use it, you don't pay for it. The basis of zero-cost abstractions.",
            },
        ],
        "war_story": [
            {
                "text": "Buffer overflow in production. It was in the changelog under 'security update'.",
                "context": "The vulnerability was known for 6 months before the fix shipped.",
                "culture": "C/C++ memory safety issues are the defining security challenge of systems programming.",
            },
        ],
        "maxim": [
            {
                "text": "RAII: Resource Acquisition Is Initialization — the destructor is your friend.",
                "context": "In C++, acquiring a resource in a constructor and releasing it in the destructor is deterministic cleanup.",
                "culture": "RAII is C++'s answer to garbage collection — deterministic, scope-based resource management.",
            },
        ],
        "meme": [
            {
                "text": "Segmentation fault: the most informative error message in programming.",
                "context": "It tells you SOMETHING went wrong. That's about all it tells you.",
                "culture": "C programmers develop a peculiar affection for segfaults — they've all seen too many.",
            },
        ],
    },
}


# ── Translation quality ratings ───────────────────────────────────────────────
# How well does an expression from source language map to target language?

TRANSLATION_RATING = {
    "direct":     "✅ Direct equivalent — the same concept exists natively",
    "near":       "⚡ Near equivalent — same idea, different expression",
    "adapted":    "🔧 Adapted — requires significant cultural adaptation",
    "untranslatable": "❌ Untranslatable — no native equivalent exists",
}


# ── Helper: build a translation card ───────────────────────────────────────────

def _build_card(
    source_lang: str,
    expression: Dict[str, Any],
    category: str,
    lang_index: int,
) -> Dict[str, Any]:
    """Build a translation record for one language mapping."""
    return {
        "category": category,
        "original_text": expression["text"],
        "context": expression["context"],
        "culture": expression["culture"],
    }


def _get_all_translations(
    source_lang: str,
    expression: Dict[str, Any],
    category: str,
) -> List[Dict[str, Any]]:
    """Get translation mappings for one expression across all languages."""
    results = []
    for target in ROTATION_ORDER:
        if target == source_lang:
            continue
        rating = _rate_translation_quality(source_lang, target, expression)
        results.append({
            "target_language": target,
            "rating": rating,
        })
    return results


def _rate_translation_quality(
    source: str, target: str, expression: Dict[str, Any]
) -> str:
    """Rate how well an expression translates from source to target."""
    # Map expressions to their translation feasibility
    # This is a simplified heuristic model based on cultural similarity
    category = expression.get("category", "idiom")

    # Rust expressions
    if source == "Rust":
        if target in ("C/C++",):
            return "direct"
        if target in ("Swift", "Kotlin", "TypeScript"):
            return "near"
        if target in ("Go",):
            return "adapted"
        return "untranslatable"

    # Go expressions
    if source == "Go":
        if target in ("Rust",):
            return "direct"
        if target in ("Kotlin", "Swift", "Java"):
            return "near"
        if target in ("C/C++",):
            return "adapted"
        return "untranslatable"

    # Swift expressions
    if source == "Swift":
        if target in ("Kotlin", "TypeScript"):
            return "direct"
        if target in ("JavaScript", "Java"):
            return "near"
        if target in ("Go",):
            return "adapted"
        return "untranslatable"

    if source == "Kotlin":
        if target in ("Swift", "Java"):
            return "direct"
        if target in ("TypeScript", "JavaScript"):
            return "near"
        if target in ("Go", "Rust"):
            return "adapted"
        return "untranslatable"

    if source == "TypeScript":
        if target in ("JavaScript",):
            return "direct"
        if target in ("Kotlin", "Swift"):
            return "near"
        if target in ("Go", "Rust", "Java"):
            return "adapted"
        return "untranslatable"

    if source == "JavaScript":
        if target in ("TypeScript",):
            return "direct"
        if target in ("Java",):
            return "near"
        if target in ("Go", "Rust"):
            return "adapted"
        return "untranslatable"

    if source == "Java":
        if target in ("Kotlin", "Swift"):
            return "direct"
        if target in ("C/C++",):
            return "near"
        if target in ("JavaScript", "TypeScript"):
            return "adapted"
        return "untranslatable"

    if source == "C/C++":
        if target in ("Rust",):
            return "direct"
        if target in ("Go",):
            return "near"
        if target in ("Swift", "Kotlin"):
            return "adapted"
        return "untranslatable"

    return "untranslatable"


# ── Core API ───────────────────────────────────────────────────────────────────

def get_current_language(rotation_file: str = None) -> str:
    """Read language_rotation.json, return current language name."""
    if rotation_file is None:
        rotation_file = ROTATION_FILE
    with open(rotation_file, "r") as f:
        data = json.load(f)
    langs = data.get("languages", ROTATION_ORDER)
    idx = data.get("current_index", 0)
    return langs[idx % len(langs)]


def advance_rotation(rotation_file: str = None) -> int:
    """Advance current_index by 1, save, return old index."""
    if rotation_file is None:
        rotation_file = ROTATION_FILE
    with open(rotation_file, "r") as f:
        data = json.load(f)

    old_index = data["current_index"]
    langs = data.get("languages", ROTATION_ORDER)
    new_index = (old_index + 1) % len(langs)

    data["current_index"] = new_index
    data["last_language"] = langs[old_index]
    data["updated_at"] = datetime.now(timezone.utc).isoformat()

    with open(rotation_file, "w") as f:
        json.dump(data, f, indent=2)

    return old_index


def pick_expression(language: str) -> Dict[str, Any]:
    """Pick a random cultural expression from the given language."""
    categories = CULTURAL_DB.get(language, {})
    if not categories:
        return {
            "text": f"No cultural data for {language}.",
            "context": "",
            "culture": "",
        }

    # Pick a random category, then a random expression
    category = random.choice(list(categories.keys()))
    expression = random.choice(categories[category])
    expression["category"] = category
    return expression


def generate_card(language: str) -> Dict[str, Any]:
    """Generate a full translation card for a language."""
    expression = pick_expression(language)
    translations = _get_all_translations(language, expression, expression["category"])

    card = {
        "language": language,
        "expression": expression,
        "translations": translations,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    return card


def format_card(card: Dict[str, Any]) -> str:
    """Format a translation card as a human-readable string."""
    lang = card["language"]
    expr = card["expression"]

    lines = []
    lines.append(f"🌏 POLYGLOT TRANSLATION CARD")
    lines.append(f"   Language: {lang}")
    lines.append(f"   Category: {expr['category'].upper()}")
    lines.append("")
    lines.append(f"   📜 EXPRESSION")
    lines.append(f"   \"{expr['text']}\"")
    lines.append("")
    lines.append(f"   💡 CONTEXT")
    lines.append(f"   {expr['context']}")
    lines.append("")
    lines.append(f"   🎭 CULTURE")
    lines.append(f"   {expr['culture']}")
    lines.append("")
    lines.append(f"   🌍 TRANSLATION MAP")
    for t in card["translations"]:
        rating_label = TRANSLATION_RATING.get(t["rating"], t["rating"])
        lines.append(f"   [{t['target_language']:12}] {rating_label}")
    lines.append("")
    lines.append(f"   ⏭️  NEXT: {lang} → {next_language(lang)}")

    return "\n".join(lines)


def next_language(current: str) -> str:
    """Return the next language in rotation after current."""
    idx = ROTATION_ORDER.index(current)
    return ROTATION_ORDER[(idx + 1) % len(ROTATION_ORDER)]


def run() -> str:
    """Main entry point. Generate card, advance rotation, return output."""
    lang = get_current_language()
    card = generate_card(lang)
    advance_rotation()
    return format_card(card)