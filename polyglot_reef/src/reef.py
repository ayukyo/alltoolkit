#!/usr/bin/env python3
"""
🐚 Polyglot Reef v1.0
Language Ecosystem Simulator — treats programming languages as species
competing for ecological niches in the software ecosystem.
"""

import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-reef"
TOOL_VERSION = "1.0.0"

_MODULE_DIR = Path(__file__).parent.parent          # polyglot_reef/
_WORKSPACE_ROOT = _MODULE_DIR.parent.parent        # AllToolkit/ -> workspace/
ROTATION_FILE = str(_WORKSPACE_ROOT / "language_rotation.json")

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# ─────────────────────────────────────────────────────────────────────────────
# Species Database — each language as a biological species
# ─────────────────────────────────────────────────────────────────────────────

LANGUAGE_SPECIES: Dict[str, Dict[str, Any]] = {

    "C/C++": {
        "scientific_name": "Carnivorous coral brutus-maximus",
        "niche": "Systems",
        "primary_habitat": "Operating systems, kernels, embedded firmware, databases, game engines",
        "traits": {
            "safety": 2,
            "speed": 10,
            "ergonomics": 3,
            "concurrency": 4,
            "type_safety": 3,
        },
        "role": "Apex predator —无处不在，无人能挡",
        "keystone": False,
        "invasive": False,
        "diet": ["raw memory", "direct hardware access", "zero-cost abstractions"],
        "predators": [],
        "symbionts": ["Rust", "Python", "Lua"],
        "competitors": ["Rust", "Zig"],
        "population_trend": "stable",
        "extinction_risk": "negligible",
        "reef_impact": "structural foundation of the entire reef",
        "conservation_status": "Least Concern",
        "fun_fact": "Drove the first browser engine, the first database, and the first operating system — all while being manually memory-managed.",
    },

    "Rust": {
        "scientific_name": "Safety-oriented coral memoria-sapiens",
        "niche": "Systems",
        "primary_habitat": "WebAssembly, OS kernels, safety-critical embedded, CLI tools, browser engines",
        "traits": {
            "safety": 10,
            "speed": 10,
            "ergonomics": 7,
            "concurrency": 10,
            "type_safety": 10,
        },
        "role": "Keystone species — shapes reef architecture through safety-by-default",
        "keystone": True,
        "invasive": False,
        "diet": ["safe memory", "zero-cost abstractions", "algebraic data types"],
        "predators": [],
        "symbionts": ["C/C++", "TypeScript", "Kotlin"],
        "competitors": ["C/C++", "Zig", "Go"],
        "population_trend": "growing",
        "extinction_risk": "low",
        "reef_impact": "raising the safety floor of the entire systems ecosystem",
        "conservation_status": "Least Concern",
        "fun_fact": "The borrow checker is basically a coral polyp — it rejects bad formations before they can grow.",
    },

    "Go": {
        "scientific_name": "Concurrency coral goroutinus-cloudus",
        "niche": "Cloud",
        "primary_habitat": "Cloud infrastructure, microservices, networking tools, CLI tools",
        "traits": {
            "safety": 7,
            "speed": 8,
            "ergonomics": 9,
            "concurrency": 10,
            "type_safety": 6,
        },
        "role": " keystone species — the cloud-native reef builder",
        "keystone": True,
        "invasive": False,
        "diet": ["goroutines", "channels", "simple syntax"],
        "predators": [],
        "symbionts": ["Rust", "TypeScript", "Python"],
        "competitors": ["Java", "Node.js", "Rust"],
        "population_trend": "growing",
        "extinction_risk": "low",
        "reef_impact": "primary builder of cloud-native infrastructure — Kubernetes, Docker, Terraform",
        "conservation_status": "Least Concern",
        "fun_fact": "Rob Pike designed goroutines as the 'fish' of concurrent programming — small, numerous, and cheap.",
    },

    "Java": {
        "scientific_name": "Enterprise coral enterprise-maximus",
        "niche": "Enterprise",
        "primary_habitat": "Enterprise backends, Android, big data (Hadoop/Spark), financial systems",
        "traits": {
            "safety": 7,
            "speed": 7,
            "ergonomics": 5,
            "concurrency": 8,
            "type_safety": 7,
        },
        "role": "Ecosystem engineer — shaped entire islands through JVM dominance",
        "keystone": True,
        "invasive": False,
        "diet": ["JVM bytecode", "Spring beans", "antipatterns"],
        "predators": ["Go", "Kotlin"],
        "symbionts": ["Kotlin", "Scala", "Clojure"],
        "competitors": ["Go", "Kotlin", "Node.js"],
        "population_trend": "stable",
        "extinction_risk": "low",
        "reef_impact": "legacy ecosystem — enormous biomass but facing displacement pressure",
        "conservation_status": "Near Threatened (appreciation declining, deployment still massive)",
        "fun_fact": "Writes once, runs everywhere — except when it doesn't (JVM version hell is real).",
    },

    "JavaScript": {
        "scientific_name": "Web coral browser-us-allus",
        "niche": "Web",
        "primary_habitat": "Web browsers, server-side (Node.js), mobile apps (React Native), tooling",
        "traits": {
            "safety": 3,
            "speed": 6,
            "ergonomics": 7,
            "concurrency": 7,
            "type_safety": 2,
        },
        "role": "Apex web species — the only coral that grows in every browser ocean",
        "keystone": True,
        "invasive": True,
        "diet": ["DOM manipulation", "JSON", "callbacks", "npm packages"],
        "predators": ["TypeScript", "WebAssembly"],
        "symbionts": ["TypeScript", "React", "Node.js"],
        "competitors": ["TypeScript", "Dart", "WebAssembly"],
        "population_trend": "stable",
        "extinction_risk": "low",
        "reef_impact": "dominates the web reef — npm has more species (packages) than any ocean",
        "conservation_status": "Least Concern",
        "fun_fact": "Created in 10 days by Brendan Eich. Has since grown to run on servers, mobile, desktop, and even robots.",
    },

    "TypeScript": {
        "scientific_name": "Typed web coral javascript-evolved-us",
        "niche": "Web",
        "primary_habitat": "Web applications, VS Code, Angular, React, Node.js backends",
        "traits": {
            "safety": 6,
            "speed": 6,
            "ergonomics": 8,
            "concurrency": 7,
            "type_safety": 7,
        },
        "role": " keystone species — TypeScript IS the modern web reef",
        "keystone": True,
        "invasive": False,
        "diet": ["static types", "IDE autocomplete", "structural typing"],
        "predators": [],
        "symbionts": ["JavaScript", "Rust", "Go"],
        "competitors": ["JavaScript", "PureScript", "ReScript"],
        "population_trend": "growing rapidly",
        "extinction_risk": "very low",
        "reef_impact": "the type annotation layer is reshaping the entire JavaScript reef",
        "conservation_status": "Least Concern",
        "fun_fact": "Anders Hejlsberg designed it — the same engineer who created Turbo Pascal and C#.",
    },

    "Swift": {
        "scientific_name": "Apple reef coral ios-hybridus",
        "niche": "Mobile",
        "primary_habitat": "iOS apps, macOS apps, server-side (SwiftNIO), interop with Objective-C",
        "traits": {
            "safety": 9,
            "speed": 9,
            "ergonomics": 9,
            "concurrency": 8,
            "type_safety": 9,
        },
        "role": " keystone species — reshaped the Apple island ecosystem",
        "keystone": True,
        "invasive": False,
        "diet": ["protocols", "optionals", "value types", "ARC"],
        "predators": ["Kotlin Multiplatform"],
        "symbionts": ["Objective-C", "Rust", "Kotlin"],
        "competitors": ["Objective-C", "Kotlin", "Dart"],
        "population_trend": "growing",
        "extinction_risk": "low",
        "reef_impact": "primary reef-builder for Apple ecosystem — shapes mobile reef standards",
        "conservation_status": "Least Concern",
        "fun_fact": "Uses ARC like Rust uses ownership — automatic memory management without a garbage collector.",
    },

    "Kotlin": {
        "scientific_name": "JVM reef coral verbosity-reducer",
        "niche": "Mobile",
        "primary_habitat": "Android development, Spring Boot backends, multiplatform (Kotlin Multiplatform)",
        "traits": {
            "safety": 8,
            "speed": 8,
            "ergonomics": 9,
            "concurrency": 9,
            "type_safety": 8,
        },
        "role": " keystone species — Kotlin is eating Java's reef from the inside",
        "keystone": True,
        "invasive": False,
        "diet": ["null safety", "coroutines", "extension functions", "type inference"],
        "predators": [],
        "symbionts": ["Java", "Swift", "Rust"],
        "competitors": ["Java", "Scala", "Swift"],
        "population_trend": "growing",
        "extinction_risk": "very low",
        "reef_impact": "the language Google officially endorses for Android is reshaping enterprise reef",
        "conservation_status": "Least Concern",
        "fun_fact": "JetBrains created it to be 'Java done right' — and then Google made it the preferred Android language.",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Niche and Role Descriptions
# ─────────────────────────────────────────────────────────────────────────────

NICHE_DESCRIPTIONS: Dict[str, str] = {
    "Systems": "Raw computational substrate — operating systems, kernels, embedded devices, drivers. Zero abstraction from hardware.",
    "Web": "The browser ocean and server-side reef. Dominated by JavaScript and TypeScript, preyed upon by WebAssembly.",
    "Mobile": "The Apple and Android archipelagos. Swift owns iOS; Kotlin owns Android. Cross-platform is the contested zone.",
    "Cloud": "Microservices, containers, and infrastructure. Go is the dominant coral here, building Kubernetes and Docker.",
    "Enterprise": "Massive legacy reef systems — Java and C# still dominate banking, ERP, and government systems.",
    "Data": "The data processing abyss — Python, R, and SQL dominate analytics and ML.",
    "Embedded": "The deep ocean floor where C still reigns supreme. Rust is making inroads.",
}

ROLE_DESCRIPTIONS: Dict[str, str] = {
    "keystone": "Keystone species — shapes reef architecture disproportionately to its population",
    "apex": "Apex predator — sits at the top of the food chain, few or no natural predators",
    "indicator": "Indicator species — sensitive to ecosystem health, its presence signals reef vitality",
    "invasive": "Invasive species — spreads rapidly, displaces native species, disruptive to balance",
    "stable": "Stable generalist — survives across niches, adaptable, no acute threats",
}


# ─────────────────────────────────────────────────────────────────────────────
# Reef Health Conditions
# ─────────────────────────────────────────────────────────────────────────────

REEF_CONDITIONS = [
    {
        "name": "Memory Safety Crisis",
        "description": "Buffer overflows and use-after-free are destabilizing C/C++ territories",
        "affected": ["C/C++"],
        "beneficiaries": ["Rust", "Go"],
    },
    {
        "name": "Type Annotation Bloom",
        "description": "Static types are spreading rapidly through the JavaScript reef",
        "affected": ["JavaScript"],
        "beneficiaries": ["TypeScript"],
    },
    {
        "name": "Cloud-Native Expansion",
        "description": "Containerization is expanding Go's territory at Java's expense",
        "affected": ["Java"],
        "beneficiaries": ["Go"],
    },
    {
        "name": "Apple Ecosystem Convergence",
        "description": "Swift is expanding beyond iOS into server-side",
        "affected": [],
        "beneficiaries": ["Swift"],
    },
    {
        "name": "Android Consolidation",
        "description": "Kotlin is now the primary Android language, Java territory shrinking",
        "affected": ["Java"],
        "beneficiaries": ["Kotlin"],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Rotation Helpers
# ─────────────────────────────────────────────────────────────────────────────

def load_rotation(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load language rotation config."""
    path = config_path if config_path is not None else ROTATION_FILE
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any], config_path: Optional[str] = None) -> None:
    """Save updated rotation config."""
    path = config_path if config_path is not None else ROTATION_FILE
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def compute_next_index(current_index: int, languages: List[str]) -> int:
    """Advance index by 1, wrapping at end."""
    return (current_index + 1) % len(languages)


# ─────────────────────────────────────────────────────────────────────────────
# Analysis Core
# ─────────────────────────────────────────────────────────────────────────────

def _build_trait_bar(value: int) -> str:
    """Build a 10-character bar chart for a trait (0-10)."""
    filled = min(max(value, 0), 10)
    return "█" * filled + "░" * (10 - filled)


def _assess_reef_health(language: str, species_data: Optional[Dict[str, Any]], all_species: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Assess the reef health from the perspective of this species."""
    if not species_data:
        return {
            "score": 50,
            "label": "Unknown",
            "emoji": "❓",
            "active_conditions": [],
            "competitor_count": 0,
            "symbiont_count": 0,
        }

    lang = species_data
    competitors_data = [all_species[c] for c in lang.get("competitors", []) if c in all_species]
    symbionts_data = [all_species[s] for s in lang.get("symbionts", []) if s in all_species]

    # Find current reef conditions affecting this species
    active_conditions = []
    scientific_word = lang["scientific_name"].split()[0]
    for cond in REEF_CONDITIONS:
        if lang["niche"] in cond.get("affected", []) or scientific_word in cond.get("affected", []):
            active_conditions.append(cond["name"])
        if scientific_word in cond.get("beneficiaries", []) or language in cond.get("beneficiaries", []):
            active_conditions.append(f"{cond['name']} (benefits)")

    health_score = 50
    if lang.get("keystone"):
        health_score += 20
    if lang.get("invasive"):
        health_score += 10
    if lang["population_trend"] == "growing":
        health_score += 15
    elif lang["population_trend"] == "declining":
        health_score -= 20

    health_score = min(max(health_score, 0), 100)

    if health_score >= 80:
        health_label = "Thriving"
        health_emoji = "🌊✨"
    elif health_score >= 60:
        health_label = "Stable"
        health_emoji = "🌊"
    elif health_score >= 40:
        health_label = "Under Pressure"
        health_emoji = "🌊⚠️"
    else:
        health_label = "At Risk"
        health_emoji = "🌊🔴"

    return {
        "score": health_score,
        "label": health_label,
        "emoji": health_emoji,
        "active_conditions": active_conditions[:3],
        "competitor_count": len(competitors_data),
        "symbiont_count": len(symbionts_data),
    }


def analyze_species(language: str) -> Optional[Dict[str, Any]]:
    """Analyze a language as a species in the reef ecosystem."""
    if language not in LANGUAGE_SPECIES:
        return None

    data = LANGUAGE_SPECIES[language]
    traits = data["traits"]

    # Build trait bars
    trait_bars = {k: _build_trait_bar(v) for k, v in traits.items()}

    # Average overall fitness
    avg_fitness = sum(traits.values()) / len(traits)

    # Niche breadth (how many niches this language touches)
    niche_breadth = len([n for n in NICHE_DESCRIPTIONS if data["primary_habitat"].lower() in n.lower() or n.lower() in data["primary_habitat"].lower()])
    # Simple heuristic: count shared niche keywords
    habitat_words = set(data["primary_habitat"].lower().replace(",", " ").replace("-", " ").split())
    niche_matches = sum(1 for niche in NICHE_DESCRIPTIONS for word in habitat_words if word in niche.lower())
    niche_breadth = min(max(niche_matches, 1), 5)

    return {
        "language": language,
        "scientific_name": data["scientific_name"],
        "niche": data["niche"],
        "niche_description": NICHE_DESCRIPTIONS.get(data["niche"], "Unknown niche"),
        "primary_habitat": data["primary_habitat"],
        "traits": traits,
        "trait_bars": trait_bars,
        "avg_fitness": round(avg_fitness, 1),
        "niche_breadth": niche_breadth,
        "role": data["role"],
        "role_type": "keystone" if data["keystone"] else ("apex" if data["invasive"] else "stable"),
        "role_description": ROLE_DESCRIPTIONS.get(
            "keystone" if data["keystone"] else ("apex" if data["invasive"] else "stable"),
            "Stable generalist"
        ),
        "keystone": data["keystone"],
        "invasive": data["invasive"],
        "diet": data["diet"],
        "predators": data["predators"],
        "symbionts": data["symbionts"],
        "competitors": data["competitors"],
        "population_trend": data["population_trend"],
        "extinction_risk": data["extinction_risk"],
        "reef_impact": data["reef_impact"],
        "conservation_status": data["conservation_status"],
        "fun_fact": data["fun_fact"],
    }


def get_ecosystem_report(rotate: bool = True,
                         config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate a full ecosystem report for the current rotation language.

    Args:
        rotate: If True, advance the rotation index after generating.
        config_path: Optional path to language_rotation.json.

    Returns a dict with species analysis + reef health + rotation metadata.
    """
    data = load_rotation(config_path)
    languages = data["languages"]
    current_index = data["current_index"]
    current_language = languages[current_index]

    species = analyze_species(current_language)

    new_index = compute_next_index(current_index, languages)
    rotated = False
    if rotate:
        data["current_index"] = new_index
        data["last_language"] = current_language
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        save_rotation(data, config_path)
        rotated = True

    reef_health = _assess_reef_health(
        current_language,
        LANGUAGE_SPECIES.get(current_language),
        LANGUAGE_SPECIES
    )

    result = {
        "tool_name": TOOL_NAME,
        "tool_version": TOOL_VERSION,
        "current_language": current_language,
        "current_index": current_index,
        "new_index": new_index if rotated else None,
        "rotated": rotated,
        "species": species,
        "reef_health": reef_health,
        "reef_conditions": REEF_CONDITIONS,
        "niche_descriptions": NICHE_DESCRIPTIONS,
        "role_descriptions": ROLE_DESCRIPTIONS,
        "updated_at": data.get("updated_at"),
    }
    return result


def format_reef_report(report: Dict[str, Any]) -> str:
    """Format the ecosystem report as a readable card."""
    species = report["species"]
    health = report["reef_health"]

    # Trait rows
    trait_lines = []
    for trait, bar in species["trait_bars"].items():
        val = species["traits"][trait]
        trait_lines.append(f"  {trait:<16} [{bar}] {val}/10")

    # Competitors / Symbionts
    competitors_str = ", ".join(species["competitors"]) if species["competitors"] else "None"
    symbionts_str = ", ".join(species["symbionts"]) if species["symbionts"] else "None"
    predators_str = ", ".join(species["predators"]) if species["predators"] else "None"

    # Conservation emoji
    cons_emoji = {
        "Least Concern": "🟢",
        "Near Threatened": "🟡",
        "Vulnerable": "🟠",
        "Endangered": "🔴",
    }.get(species["conservation_status"], "⚪")

    # Trend arrow
    trend_arrow = {
        "growing": "📈",
        "stable": "➡️",
        "declining": "📉",
    }.get(species["population_trend"], "➡️")

    active_cond = ", ".join(health["active_conditions"]) if health["active_conditions"] else "None"

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  🐚  POLYGLOT REEF — Language Ecosystem Simulator                 ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Species         : {species['language']:<47}║",
        f"║  Scientific Name : {species['scientific_name']:<47}║",
        f"║  Niche           : {species['niche']:<47}║",
        f"║  Role            : {species['role']:<47}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  📊  TRAIT PROFILE                                              ║",
        *trait_lines,
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  ⚖️  Avg Fitness    : {species['avg_fitness']}/10                                   ║",
        f"║  🌿  Niche Breadth  : {'●' * species['niche_breadth'] + '○' * (5 - species['niche_breadth'])}                                      ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  🦈  Predators     : {predators_str:<47}║",
        f"║  🤝  Symbionts     : {symbionts_str:<47}║",
        f"║  ⚔️  Competitors   : {competitors_str:<47}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🌊  REEF HEALTH                                                 ║",
        f"║  {health['emoji']}  {health['label']:<14} Score: {health['score']}/100                               ║",
        f"║  🌡️  Active Conditions: {active_cond:<36}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  📜  NICHE DESCRIPTION                                          ║",
        f"║  {species['niche_description']:<64}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🌍  ECOSYSTEM IMPACT                                           ║",
        f"║  {species['reef_impact']:<64}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  {trend_arrow}  Population Trend : {species['population_trend']:<37}║",
        f"║  {cons_emoji}  Conservation     : {species['conservation_status']:<37}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  💡  FUN FACT                                                    ║",
        f"║  {species['fun_fact']:<64}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Rotated         : {str(report['rotated']):<47}║",
        f"║  New Index      : {str(report.get('new_index', '')):<47}║",
        "╚══════════════════════════════════════════════════════════════════╝",
    ]
    return "\n".join(lines)


def run_tests() -> None:
    """Run all tests and exit."""
    import pytest
    import sys
    sys.exit(pytest.main([str(Path(__file__).parent.parent / "tests"), "-v"]))
