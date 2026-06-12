#!/usr/bin/env python3
"""
🗺️ Polyglot Chronology v1.0
Temporal Cartography — maps programming languages as geological eras
and evolutionary epochs, revealing the deep-time forces that shaped them.

Creative concept: "Languages are not born in a vacuum — they emerge from the
geological pressures of their era: the memory crises, the concurrency earthquakes,
the type-system continental drifts. Chronology reads those pressures."

Each language is mapped to a geological/evolutionary epoch with:
  - Era signature (Precambrian, Paleozoic, Mesozoic, Cenozoic, etc.)
  - Formative pressures (what crisis drove this language into existence?)
  - Fossil record (the code fossils / artifacts that survived from this era)
  - Extinction resistance (why did this language survive its era?)
  - Epoch alignment (which era does this language best belong to?)

The tool generates a "temporal map" for the current rotation language,
showing where it sits on the programming-language geological timescale,
what pressures shaped it, and how it relates to neighboring languages
across deep time.

Distinct from existing tools:
  - language_archaeology:   historical lineage & design philosophy (specific facts)
  - polyglot_chronicle:      daily diary + challenge (day-scale temporal)
  - polyglot_dna:            genetic trait mapping (molecular level)
  - polyglot_weather:        atmospheric dynamics (weather-scale)
  - polyglot_sentinel:       threat detection (present-moment threats)
  - polyglot_harmony:        compatibility analysis (pair relationships)
  - polyglot_constellation:  spatial night-sky navigation (spatial)

Chronology is about DEEP GEOLOGICAL TIME — the macro-scale forces spanning
decades that birth, shape, and test every programming language.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-chronology"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent.parent  # polyglot_chronology/
_WORKSPACE_ROOT = _MODULE_DIR.parent              # AllToolkit/ -> workspace/
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

# Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]


# ─────────────────────────────────────────────────────────────────────────────
# Geological / Evolutionary Epoch Database
# ─────────────────────────────────────────────────────────────────────────────

GEOLOGICAL_EPOCHS: Dict[str, Dict[str, Any]] = {

    "C": {
        "epoch": "Paleozoic",
        "period": "Cambrian",
        "geological_age_mya": 541,
        "language_age": 1972,
        "formative_pressure": (
            "The Operating System Ice Age: Unix needed a language that could "
            "talk to hardware without drowning in assembly. C bridged the gap — "
            "portable, low-level, and close enough to the machine that "
            "the Unix revolution could spread across continents."
        ),
        "fossil_record": [
            "int main(int argc, char *argv[]) {",
            "    while (*str) *out++ = *str++;",
            "    return 0;",
            "}",
        ],
        "extinction_resistance": (
            "The lingua franca of systems programming. Every operating system, "
            "embedded runtime, and performance-critical path traces lineage to C."
        ),
        "extinction_risk": "low",
        "era_tagline": "The Cambrian Explosion of Systems Thinking",
    },

    "C/C++": {
        "epoch": "Mesozoic",
        "period": "Jurassic",
        "geological_age_mya": 201,
        "language_age": 1983,
        "formative_pressure": (
            "The Complexity Ice Sheet: C was powerful but couldn't manage "
            "large programs. C++ brought object orientation to systems-level "
            "programming — the Jurassic megafauna of programming languages."
        ),
        "fossil_record": [
            "template<typename T>",
            "class Stack {",
            "  std::vector<T> data_;",
            "public:",
            "  void push(const T& item) { data_.push_back(item); }",
            "};",
        ],
        "extinction_resistance": (
            "The backbone of game engines, operating systems, databases, "
            "and browsers. Modern C++ (C++11 onward) is a living renaissance."
        ),
        "extinction_risk": "low",
        "era_tagline": "The Jurassic Megafauna — Complexity with Teeth",
    },

    "Go": {
        "epoch": "Cenozoic",
        "period": "Miocene",
        "geological_age_mya": 23,
        "language_age": 2009,
        "formative_pressure": (
            "The Concurrency Ice Sheet: multi-core machines were the new "
            "geological reality, but threads were heavy and error-prone. "
            "Go's goroutines were the adaptive radiation — lightweight "
            "coroutines that made concurrent programming feel natural."
        ),
        "fossil_record": [
            "func worker(ch <-chan int) {",
            "    for n := range ch {",
            "        go process(n)",
            "    }",
            "}",
        ],
        "extinction_resistance": (
            "Cloud-native infrastructure runs on Go: Kubernetes, Docker, "
            "Terraform, Prometheus. The Miocene was an age of diversification."
        ),
        "extinction_risk": "low",
        "era_tagline": "The Miocene Diversification — Lightweight Concurrency",
    },

    "Java": {
        "epoch": "Mesozoic",
        "period": "Cretaceous",
        "geological_age_mya": 145,
        "language_age": 1995,
        "formative_pressure": (
            "The Platform Independence Andes: Sun asked — what if you could "
            "write once and run anywhere? Java's JVM was a continental drift "
            "that separated code from machine."
        ),
        "fossil_record": [
            "public class HelloWorld {",
            "    public static void main(String[] args) {",
            "        System.out.println(\"Hello, World!\");",
            "    }",
            "}",
        ],
        "extinction_resistance": (
            "Android, enterprise backends, and Hadoop built empires on JVM. "
            "Despite the Cretaceous extinction of applet-era hype, Java "
            "remains one of the most deployed languages on Earth."
        ),
        "extinction_risk": "low",
        "era_tagline": "The Cretaceous Platform Shift — Write Once, Run Anywhere",
    },

    "JavaScript": {
        "epoch": "Mesozoic",
        "period": "Late Cretaceous",
        "geological_age_mya": 100,
        "language_age": 1995,
        "formative_pressure": (
            "The Browser Jungle: Netscape needed a scripting language in 10 days. "
            "Brendan Eich wrote it in a fever — prototype-based, dynamic, "
            "and wildly different from anything that came before."
        ),
        "fossil_record": [
            "function greet(name) {",
            "  return `Hello, ${name}!`;",
            "}",
            "console.log(greet('World'));",
        ],
        "extinction_resistance": (
            "The only language that runs natively in every browser on Earth. "
            "Node.js spread it to the server. npm has more packages than "
            "any ecosystem in history."
        ),
        "extinction_risk": "low",
        "era_tagline": "The Browser Jungle — Ten Days That Reshaped the Web",
    },

    "Kotlin": {
        "epoch": "Cenozoic",
        "period": "Eocene",
        "geological_age_mya": 56,
        "language_age": 2011,
        "formative_pressure": (
            "The JVM Verbosity Ice Age: Java was powerful but verbose — "
            "the boilerplate Permian layer was suffocating productivity. "
            "Kotlin emerged from JetBrains as an Eocene diversification."
        ),
        "fossil_record": [
            "fun main() {",
            "    val result = listOf(1, 2, 3)",
            "        .filter { it > 1 }",
            "        .map { it * 2 }",
            "    println(result)  // [4, 6]",
            "}",
        ],
        "extinction_resistance": (
            "Android's preferred language since Google backed it in 2017. "
            "Coroutines brought structured concurrency to the JVM."
        ),
        "extinction_risk": "low",
        "era_tagline": "The Eocene Diversification — JVM Verbosity Meets its Match",
    },

    "Rust": {
        "epoch": "Cenozoic",
        "period": "Pliocene",
        "geological_age_mya": 5,
        "language_age": 2010,
        "formative_pressure": (
            "The Memory Safety Mass Extinction: the C/C++ generation left "
            "a landscape littered with buffer overflows, use-after-free "
            "bugs, and data races. Graydon Hoare asked: what if a language "
            "proved memory safety at compile time?"
        ),
        "fossil_record": [
            "fn main() {",
            "    let s = String::from(\"hello\");",
            "    let t = s;  // s is moved, not copied",
            "    println!(\"{}\", t);",
            "}",
        ],
        "extinction_resistance": (
            "Systems programming, WebAssembly, and security-critical code "
            "are Rust's niches. The Pliocene is still being settled."
        ),
        "extinction_risk": "low",
        "era_tagline": "The Pliocene Safety Radiation — Filling the Memory Safety Niche",
    },

    "Swift": {
        "epoch": "Cenozoic",
        "period": "Holocene",
        "geological_age_mya": 0.012,
        "language_age": 2014,
        "formative_pressure": (
            "The Apple Ecosystem Reformation: Objective-C was the old megafauna "
            "— capable but showing its age. Apple needed a modern language "
            "for iOS and macOS development."
        ),
        "fossil_record": [
            "func greet(_ name: String) -> String {",
            "    return \"Hello, \\(name)!\"",
            "}",
            "let numbers = [1, 2, 3].map { $0 * 2 }",
        ],
        "extinction_resistance": (
            "The primary language for iOS/macOS development. Swift's move "
            "to open source and Linux keeps it expanding beyond the Apple continent."
        ),
        "extinction_risk": "low",
        "era_tagline": "The Holocene Reformation — Modern Safety for the Apple Ecosystem",
    },

    "TypeScript": {
        "epoch": "Cenozoic",
        "period": "Oligocene",
        "geological_age_mya": 34,
        "language_age": 2012,
        "formative_pressure": (
            "The JavaScript Jungle Tectonics: the web had exploded but "
            "JavaScript was dynamic, untyped, and prone to runtime errors "
            "at scale. Anders Hejlsberg designed TypeScript as a continental "
            "plate — adding static types without fracturing the ecosystem."
        ),
        "fossil_record": [
            "interface Result<T, E> {",
            "    ok: T;",
            "    err: E;",
            "}",
            "function divide(a: number, b: number): Result<number, string> {",
            "    return b === 0 ? { ok: 0, err: 'div by zero' } : { ok: a / b };",
            "}",
        ],
        "extinction_resistance": (
            "The standard language of modern web development. VS Code, "
            "Angular, and most major frameworks are TypeScript-first."
        ),
        "extinction_risk": "low",
        "era_tagline": "The Oligocene Adaptive Radiation — Types Fill the JavaScript Jungle",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Epoch hierarchy for cross-language comparison
# ─────────────────────────────────────────────────────────────────────────────

EPOCH_ORDER = ["Precambrian", "Paleozoic", "Mesozoic", "Cenozoic"]

EPOCH_DESCRIPTIONS: Dict[str, str] = {
    "Precambrian": (
        "The first era — primordial languages that invented core concepts "
        "(recursion, symbolic processing, business logic) before the ecosystem had structure."
    ),
    "Paleozoic": (
        "The Cambrian explosion — the great diversification of structured "
        "programming. C and Pascal built the reef systems that supported all subsequent life."
    ),
    "Mesozoic": (
        "The age of giants — compiled and interpreted megafauna that dominated "
        "enterprise computing, the web, and systems programming."
    ),
    "Cenozoic": (
        "The modern era of specialized mammals — languages born from specific "
        "geological pressures: memory unsafety, verbosity, concurrency, and type safety."
    ),
}


# ─────────────────────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────────────────────

def _load_rotation(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load language rotation config."""
    path = config_path if config_path is not None else ROTATION_FILE
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_rotation(data: Dict[str, Any], config_path: Optional[str] = None) -> None:
    """Save updated rotation config."""
    path = config_path if config_path is not None else ROTATION_FILE
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _compute_next_index(current_index: int, languages: List[str]) -> int:
    """Advance index by 1, wrapping at end."""
    return (current_index + 1) % len(languages)


def _build_time_scale_bar(language_age: int) -> str:
    """Draw a relative time-scale bar (oldest=left, newest=right)."""
    oldest, newest, width = 1950, 2025, 20
    position = min(max(int(((language_age - oldest) / (newest - oldest)) * width), 0), width)
    return "█" * position + "░" * (width - position)


def _get_neighboring_epochs(language_epoch: str) -> List[str]:
    """Return adjacent epochs in the geological timeline."""
    try:
        idx = EPOCH_ORDER.index(language_epoch)
    except ValueError:
        return []
    neighbors = []
    if idx > 0:
        neighbors.append(EPOCH_ORDER[idx - 1])
    if idx < len(EPOCH_ORDER) - 1:
        neighbors.append(EPOCH_ORDER[idx + 1])
    return neighbors


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def get_current_language(config_path: Optional[str] = None) -> str:
    """Return the current language from rotation config (no rotation)."""
    data = _load_rotation(config_path)
    idx = data["current_index"]
    return data["languages"][idx]


def get_epoch_for_language(language: str) -> Optional[Dict[str, Any]]:
    """Return the epoch data for a given language, or None if unknown."""
    return GEOLOGICAL_EPOCHS.get(language)


def generate_temporal_map(rotate: bool = True,
                         config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate a temporal cartography report for the current rotation language.

    Args:
        rotate: If True, advance the rotation index after generating the report.
        config_path: Optional path to language_rotation.json (defaults to workspace).

    Returns:
        {
            "current_language": str,
            "current_index": int,
            "epoch": str,
            "period": str,
            "geological_age_mya": float,
            "formative_pressure": str,
            "fossil_record": List[str],
            "extinction_resistance": str,
            "extinction_risk": str,
            "era_tagline": str,
            "neighboring_epochs": List[str],
            "epoch_description": str,
            "epoch_order": List[str],
            "time_scale_bar": str,
            "rotated": bool,
            "new_index": Optional[int],
        }
    """
    data = _load_rotation(config_path)
    languages = data["languages"]
    current_index = data["current_index"]

    current_language = languages[current_index]
    epoch_data = GEOLOGICAL_EPOCHS.get(current_language)

    new_index = _compute_next_index(current_index, languages)
    if rotate:
        data["current_index"] = new_index
        data["last_language"] = current_language
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        _save_rotation(data, config_path)

    if epoch_data is None:
        return {
            "current_language": current_language,
            "current_index": current_index,
            "epoch": "Unknown",
            "period": "Unknown",
            "geological_age_mya": 0.0,
            "formative_pressure": "No geological data available for this era.",
            "fossil_record": [],
            "extinction_resistance": "Unknown.",
            "extinction_risk": "unknown",
            "era_tagline": "An undiscovered era in the programming landscape.",
            "neighboring_epochs": [],
            "epoch_description": "",
            "epoch_order": EPOCH_ORDER,
            "time_scale_bar": "░" * 20,
            "rotated": rotate,
            "new_index": new_index if rotate else None,
        }

    neighboring = _get_neighboring_epochs(epoch_data["epoch"])

    return {
        "current_language": current_language,
        "current_index": current_index,
        "epoch": epoch_data["epoch"],
        "period": epoch_data["period"],
        "geological_age_mya": epoch_data["geological_age_mya"],
        "formative_pressure": epoch_data["formative_pressure"],
        "fossil_record": epoch_data["fossil_record"],
        "extinction_resistance": epoch_data["extinction_resistance"],
        "extinction_risk": epoch_data["extinction_risk"],
        "era_tagline": epoch_data["era_tagline"],
        "neighboring_epochs": neighboring,
        "epoch_description": EPOCH_DESCRIPTIONS.get(epoch_data["epoch"], ""),
        "epoch_order": EPOCH_ORDER,
        "time_scale_bar": _build_time_scale_bar(epoch_data["language_age"]),
        "rotated": rotate,
        "new_index": new_index if rotate else None,
    }


def format_epoch_card(m: Dict[str, Any]) -> str:
    """
    Format the temporal map result as a human-readable card.
    """
    risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(
        m.get("extinction_risk", "low"), "🟢"
    )
    fossils = "\n".join(f"    {line}" for line in m["fossil_record"])
    neighboring = ", ".join(m["neighboring_epochs"]) if m["neighboring_epochs"] else "None"

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  🗺️  POLYGLOT CHRONOLOGY — Temporal Cartography Report             ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Language         : {m['current_language']:<47}║",
        f"║  Epoch           : {m['epoch']:<47}║",
        f"║  Period          : {m['period']:<47}║",
        f"║  Geo Age (MYA)   : {m['geological_age_mya']:<47}║",
        f"║  Era Tagline      : {m['era_tagline']:<47}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  ⏳  Time Scale Bar (oldest ░░░░░░░░░░░░░░░░░ newest)            ║",
        f"║     [{m['time_scale_bar']}]                                      ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🌋  FORMATIVE PRESSURE                                          ║",
        f"║  {m['formative_pressure']:<64}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🐾  FOSSIL RECORD (code artifacts from this era)                 ║",
        fossils,
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  🛡️  EXTINCTION RESISTANCE: {risk_emoji} ({m['extinction_risk']})                          ║",
        f"║  {m['extinction_resistance']:<64}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  🌐  Neighboring Epochs : {neighboring:<47}║",
        "║  📜  EPOCH DESCRIPTION                                             ║",
        f"║  {m['epoch_description']:<64}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Rotated         : {str(m['rotated']):<47}║",
        f"║  New Index      : {str(m.get('new_index', '')):<47}║",
        "╚══════════════════════════════════════════════════════════════════╝",
    ]
    return "\n".join(lines)


def run_tests() -> None:
    """Run all tests and exit."""
    import pytest
    import sys
    sys.exit(pytest.main([str(Path(__file__).parent.parent / "tests"), "-v"]))