#!/usr/bin/env python3
"""
🗼 Polyglot Sentinel v1.0 — Language Ecosystem Watchtower

A sentinel monitors the programming language ecosystem from a watchtower,
detecting threats, opportunities, and shifts in the landscape. Where
polyglot_weather watches atmospheric pressure and polyglot_ecosystem_map
charts relationships, the sentinel watches for DANGER and OPPORTUNITY.

Creative concept: "The sentinel never sleeps. From the watchtower, it scans
the horizon for threats (declining languages, security vulnerabilities,
paradigm shifts) and opportunities (rising stars, new synergies, market
gaps). Every rotation, the sentinel reports from the front lines."

The sentinel:
  1. Reads current language from language_rotation.json
  2. Generates a threat/opportunity report for the language
  3. Detects "signals" — weak signals of upcoming changes
  4. Updates the rotation index
  5. Commits changes to git

Threat categories:
  - EXTINCTION   — language on borrowed time
  - VULNERABLE   — declining adoption, fading ecosystem
  - STABLE       — healthy but not growing
  - RISING       — growing adoption and momentum
  - DOMINANT     — peak influence and saturation

Signals detected:
  - "Low moon" — early warning of decline
  - "Convergence front" — languages merging paradigms
  - "Echo" — historical patterns repeating
  - "Aurora" — rare opportunity window opening
  - "Static" — interference/blocking in the ecosystem

Distinct from existing tools:
  - polyglot_weather:        atmospheric dynamics (pressure, fronts, seasons)
  - polyglot_ecosystem_map:   relationship graphs (proximity, synergy, influence)
  - polyglot_meridian:       spectral positioning (coordinate lens)
  - polyglot_digest:         syntax comparison (static snapshots)
  - polyglot_resonator:      harmonic relationships (frequency lens)
  - polyglot_dna:            genetic traits (trait lens)
  - polyglot_chronicle:      daily history (temporal)
  - polyglot_flavor:         sensory tasting notes (sensory)
  - polyglot_code_printer:   code postcard aesthetic (visual)
  - polyglot_translation:    cultural linguistics (cultural)
  - polyglot_cipher:         cryptographic puzzles (crypto)
  - polyglot_selector:       rotation + challenge (challenge)
  - polyglot_bridges:        problem→solution maps (conceptual)
  - polyglot_wire:           wire protocol reports (protocol)
  - polyglot_harmony:        compatibility analysis (compatibility)

Sentinel is about WATCHDOG THREAT DETECTION and OPPORTUNITY RECOGNITION.
"""

import json
import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .config import load_config, save_config

# ─── Constants ────────────────────────────────────────────────────────────────

TOOL_NAME = "polyglot-sentinel"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = str(Path(__file__).parent.parent.parent / "language_rotation.json")

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

# ─── Sentinel profiles ─────────────────────────────────────────────────────────

# Each language has sentinel characteristics:
#   threat_level      — how at-risk is this language? (1=extinct, 5=dominant)
#   stability_score   — ecosystem robustness (0.0=fragile, 1.0=ironclad)
#   opportunity_index — growth/market opportunity (0.0=none, 1.0=wide open)
#   signal_risk       — likelihood of disruption in next 6 months
#   sentinel_reading  — raw watchtower data (ephemeral conditions)

LANGUAGE_PROFILES: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "threat_level": 4,
        "stability_score": 0.82,
        "opportunity_index": 0.75,
        "signal_risk": 0.25,
        "sentinel_reading": "Rising static — memory safety awareness spreading",
        "threat_category": "RISING",
        "watchtower_notes": [
            "Systems programming displacement of C/C++ accelerating",
            "Memory safety mandates in government contracts",
            "Growing adoption in cloud infrastructure",
        ],
        "opportunities": [
            "Security-critical systems adoption",
            "WebAssembly expansion",
            "Embedded systems new territory",
        ],
        "signals": [
            {"type": "Aurora", "desc": "Government contracts mandate memory-safe languages"},
            {"type": "Convergence front", "desc": "Rust+WebAssembly convergence zone expanding"},
        ],
        "watchtower_alert": "⚠️ RUST: Systems programming displacement pressure increasing",
    },
    "Go": {
        "threat_level": 4,
        "stability_score": 0.90,
        "opportunity_index": 0.60,
        "signal_risk": 0.15,
        "sentinel_reading": "Clear skies — cloud-native dominance continues",
        "threat_category": "STABLE",
        "watchtower_notes": [
            "Kubernetes ecosystem remains the backbone of cloud infrastructure",
            "Microservices adoption plateauing but not declining",
            "Simple concurrency model still compelling",
        ],
        "opportunities": [
            "Edge computing expansion",
            "CLI tooling consolidation",
            "IoT backend services",
        ],
        "signals": [
            {"type": "Stable", "desc": "Kubernetes dependency keeps Go relevant"},
            {"type": "Low moon", "desc": "Generic backend competition intensifying"},
        ],
        "watchtower_alert": "🟢 GO: Stable positioning, no immediate threats",
    },
    "Swift": {
        "threat_level": 3,
        "stability_score": 0.78,
        "opportunity_index": 0.65,
        "signal_risk": 0.30,
        "sentinel_reading": "Patchy visibility — Apple ecosystem dependency noted",
        "threat_category": "RISING",
        "watchtower_notes": [
            "Apple ecosystem lock-in provides stable territory",
            "SwiftData and modern concurrency attracting new developers",
            "Cross-platform ambitions (Swift on Linux, Serverside) partial success",
        ],
        "opportunities": [
            "Server-side Swift expansion",
            "SwiftData adoption wave",
            "Cross-platform UI framework potential",
        ],
        "signals": [
            {"type": "Convergence front", "desc": "Swift+Kotlin cross-pollination increasing"},
            {"type": "Echo", "desc": "History repeating: Objective-C→Swift transition mirrors Pascal→C"},
        ],
        "watchtower_alert": "🔔 SWIFT: Apple ecosystem stable, cross-platform ambitions monitored",
    },
    "Kotlin": {
        "threat_level": 4,
        "stability_score": 0.85,
        "opportunity_index": 0.70,
        "signal_risk": 0.20,
        "sentinel_reading": "Clearing — Android momentum and JVM relevance",
        "threat_category": "STABLE",
        "watchtower_notes": [
            "Android primary language status unchallenged",
            "JVM ecosystem consolidation continuing",
            "Kotlin Multiplatform gaining traction slowly",
        ],
        "opportunities": [
            "Android development dominance",
            "JVM modernization projects",
            "Multiplatform expansion (iOS, Web, Native)",
        ],
        "signals": [
            {"type": "Stable", "desc": "Android ecosystem dependency is structural"},
            {"type": "Aurora", "desc": "Kotlin Multiplatform could break new ground in 2026"},
        ],
        "watchtower_alert": "🟢 KOTLIN: Strong Android position, multiplatform watched",
    },
    "TypeScript": {
        "threat_level": 5,
        "stability_score": 0.92,
        "opportunity_index": 0.80,
        "signal_risk": 0.10,
        "sentinel_reading": "High pressure — JS ecosystem dominance continues",
        "threat_category": "DOMINANT",
        "watchtower_notes": [
            "JavaScript superset status nearly absolute in web development",
            "Type annotations becoming expected in modern JS codebases",
            "AI coding assistants accelerating TypeScript adoption",
        ],
        "opportunities": [
            "AI-assisted development integration",
            "Full-stack unification (React/Vue/Svelte all TS-native)",
            "Backend expansion via Bun/Node/Deno",
        ],
        "signals": [
            {"type": "Aurora", "desc": "AI coding assistants making TypeScript the 'default' for web"},
            {"type": "Stable", "desc": "Ecosystem dominance approaching saturation"},
        ],
        "watchtower_alert": "🟢 TYPESCRIPT: Dominant position, AI wave accelerating adoption",
    },
    "JavaScript": {
        "threat_level": 5,
        "stability_score": 0.95,
        "opportunity_index": 0.70,
        "signal_risk": 0.05,
        "sentinel_reading": "Settled — runtime dominance across all platforms",
        "threat_category": "DOMINANT",
        "watchtower_notes": [
            "Every browser, every Node runtime, every modern build tool",
            "Paradigm convergence: modules, async/await, arrow functions everywhere",
            "TypeScript absorbing the type-safety demand, leaving JS pure",
        ],
        "opportunities": [
            "Deno/Bun runtime evolution",
            "Edge computing expansion",
            "WebAssembly JS interop deepening",
        ],
        "signals": [
            {"type": "Stable", "desc": "Runtime dominance is structural — no near-term threat"},
            {"type": "Static", "desc": "TS absorbing type-safety mindshare, pure JS niche shifting"},
        ],
        "watchtower_alert": "🟢 JAVASCRIPT: Ironclad runtime position, ecosystem maturation",
    },
    "Java": {
        "threat_level": 4,
        "stability_score": 0.88,
        "opportunity_index": 0.45,
        "signal_risk": 0.20,
        "sentinel_reading": "Overcast — enterprise anchor but innovation plateau",
        "threat_category": "STABLE",
        "watchtower_notes": [
            "Enterprise backend bedrock — Banks, governments, Android (legacy)",
            "LTS versions providing stability but creating upgrade inertia",
            "Virtual threads (Loom) breathe new life into concurrency model",
        ],
        "opportunities": [
            "Modernization of legacy enterprise systems",
            "Cloud-native Java frameworks (Quarkus, Micronaut)",
            "Virtual threads adoption wave",
        ],
        "signals": [
            {"type": "Low moon", "desc": "Younger developers migrating to Kotlin/Go/TS"},
            {"type": "Echo", "desc": "Enterprise lock-in patterns mirror COBOL legacy concerns"},
        ],
        "watchtower_alert": "🔔 JAVA: Stable enterprise position, modernization opportunities watched",
    },
    "C/C++": {
        "threat_level": 3,
        "stability_score": 0.70,
        "opportunity_index": 0.50,
        "signal_risk": 0.45,
        "sentinel_reading": "Turbulence — memory safety displacement and performance pressure",
        "threat_category": "VULNERABLE",
        "watchtower_notes": [
            "Memory safety displacement accelerating (Rust/Go eating territory)",
            "Game engine and embedded stronghold remains strong",
            "C23/C++26 standards bringing incremental improvements",
        ],
        "opportunities": [
            "Embedded systems (microcontrollers, IoT)",
            "Game development (Unity/Unreal engines)",
            "High-frequency trading (latency-critical)",
        ],
        "signals": [
            {"type": "Low moon", "desc": "Government mandates memory-safe alternatives"},
            {"type": "Convergence front", "desc": "Rust/C++ interop increasing (bindgen, CXX)"},
            {"type": "Static", "desc": "Security vulnerability fatigue reducing adoption"},
        ],
        "watchtower_alert": "⚠️ C/C++: Vulnerability pressure and Rust displacement — watched closely",
    },
}


# ─── Sentinel data structures ──────────────────────────────────────────────────

@dataclass
class Signal:
    type: str
    description: str
    severity: str  # "low", "medium", "high"


@dataclass
class SentinelReport:
    """Complete sentinel report for a language rotation."""
    previous_language: str
    current_language: str
    threat_category: str
    threat_level: int
    stability_score: float
    opportunity_index: float
    signal_risk: float
    sentinel_reading: str
    watchtower_alert: str
    watchtower_notes: List[str]
    opportunities: List[str]
    signals: List[Signal]
    rotated: bool = False
    new_index: Optional[int] = None
    generated_at: str = ""


# ─── Core functions ─────────────────────────────────────────────────────────────

def get_current_language(config_path: str = ROTATION_FILE) -> str:
    """Read the current language from the rotation file."""
    data = load_config(config_path)
    languages = data["languages"]
    idx = data["current_index"]
    return languages[idx]


def advance_rotation(config_path: str = ROTATION_FILE) -> Tuple[str, int]:
    """Advance the rotation and return (new_language, new_index)."""
    data = load_config(config_path)
    languages = data["languages"]
    current_index = data["current_index"]

    previous_language = languages[current_index]
    new_index = (current_index + 1) % len(languages)
    current_language = languages[new_index]

    data["current_index"] = new_index
    data["last_language"] = current_language
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_config(config_path, data)

    return current_language, new_index


def generate_sentinel_report(
    language: str,
    previous_language: Optional[str] = None,
    new_index: Optional[int] = None,
    rotated: bool = False,
    seed: Optional[int] = None,
) -> SentinelReport:
    """Generate a full sentinel report for a language.

    Args:
        language: The language to generate a report for.
        previous_language: The language before rotation (for context).
        new_index: The new rotation index (if rotation just happened).
        rotated: Whether a rotation just occurred.
        seed: Optional random seed for deterministic output.

    Returns:
        A SentinelReport dataclass with full ecosystem analysis.
    """
    if seed is not None:
        rng = random.Random(seed)
    else:
        rng = random.Random()

    profile = LANGUAGE_PROFILES.get(language, LANGUAGE_PROFILES["C/C++"])

    # Build signals
    signals = []
    for sig in profile.get("signals", []):
        severity = "high" if sig["type"] in ("Low moon", "Static") else \
                   "medium" if sig["type"] in ("Convergence front", "Echo") else "low"
        signals.append(Signal(type=sig["type"], description=sig["desc"], severity=severity))

    return SentinelReport(
        previous_language=previous_language or "",
        current_language=language,
        threat_category=profile["threat_category"],
        threat_level=profile["threat_level"],
        stability_score=profile["stability_score"],
        opportunity_index=profile["opportunity_index"],
        signal_risk=profile["signal_risk"],
        sentinel_reading=profile["sentinel_reading"],
        watchtower_alert=profile["watchtower_alert"],
        watchtower_notes=profile.get("watchtower_notes", []),
        opportunities=profile.get("opportunities", []),
        signals=signals,
        rotated=rotated,
        new_index=new_index,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


def format_report(report: SentinelReport) -> str:
    """Format a sentinel report as a human-readable watchtower bulletin."""
    lines = [
        f"═══════════════════════════════════════",
        f"     🗼 POLYGLOT SENTINEL BULLETIN      ",
        f"═══════════════════════════════════════",
        f"",
        f"  Language   : {report.current_language}",
        f"  Threat     : [{report.threat_category}] (level {report.threat_level}/5)",
        f"  Stability  : {report.stability_score:.2f}",
        f"  Opportunity: {report.opportunity_index:.2f}",
        f"  Signal Risk: {report.signal_risk:.2f}",
        f"",
        f"  📡 Sentinel Reading",
        f"  ─────────────────────────────────────",
        f"  {report.sentinel_reading}",
        f"",
        f"  ⚠️  Watchtower Alert",
        f"  ─────────────────────────────────────",
        f"  {report.watchtower_alert}",
        f"",
    ]

    if report.watchtower_notes:
        lines.append("  📋 Watchtower Notes")
        lines.append("  ─────────────────────────────────────")
        for note in report.watchtower_notes:
            lines.append(f"    • {note}")
        lines.append("")

    if report.opportunities:
        lines.append("  🚀 Opportunity Index")
        lines.append("  ─────────────────────────────────────")
        for opp in report.opportunities:
            lines.append(f"    → {opp}")
        lines.append("")

    if report.signals:
        lines.append("  📡 Detected Signals")
        lines.append("  ─────────────────────────────────────")
        for sig in report.signals:
            sev_icon = "🔴" if sig.severity == "high" else "🟡" if sig.severity == "medium" else "🟢"
            lines.append(f"    {sev_icon} [{sig.type}] {sig.description}")
        lines.append("")

    if report.rotated:
        lines.append(f"  🔄 Rotated from: {report.previous_language} → {report.current_language}")
        lines.append(f"  📍 New index: {report.new_index}")

    lines.append(f"  🕐 Generated: {report.generated_at}")
    lines.append(f"═══════════════════════════════════════")

    return "\n".join(lines)


def run() -> str:
    """Main entry point — rotate, generate report, return formatted output."""
    prev_lang = get_current_language()
    new_lang, new_idx = advance_rotation()
    report = generate_sentinel_report(
        language=new_lang,
        previous_language=prev_lang,
        new_index=new_idx,
        rotated=True,
    )
    return format_report(report)


# ─── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    """CLI entry point."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        from . import run_tests
        run_tests()
    else:
        print(run())