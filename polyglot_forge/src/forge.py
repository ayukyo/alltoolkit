"""Polyglot Forge — Language Alloy Forge Workshop."""

import json
import os
import random
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional

TOOL_NAME = "polyglot-forge"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = str(
    Path(__file__).parent.parent.parent / "language_rotation.json"
)

# ── Metallurgical database ───────────────────────────────────────────────────

# Each language has "metal properties" across dimensions
METAL_PROPERTIES: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "element": "Adamantine",
        "grade": "Military-grade alloy",
        "composition": ["carbon", "chromium", "manganese"],
        "hardness": 9.5,
        "ductility": 3.0,   # low — brittle
        "conductivity": 4.5,
        "heat_resistance": 9.8,
        "corrosion_resistance": 9.0,
        "forge_temp_c": 1538,
        "temper_color": "blue-white",
        "primary_use": "weaponry, load-bearing structures",
        "properties": ["ultra-high tensile strength", "zero-defect certification", "extreme longevity"],
        "forging_skill": "master smith",
    },
    "Go": {
        "element": "Crucible Steel",
        "grade": "Industrial alloy",
        "composition": ["iron", "silicon", "carbon"],
        "hardness": 7.0,
        "ductility": 8.5,
        "conductivity": 7.0,
        "heat_resistance": 7.5,
        "corrosion_resistance": 7.0,
        "forge_temp_c": 1510,
        "temper_color": "straw-yellow",
        "primary_use": "tools, machinery, pipelines",
        "properties": ["high machinability", "consistent grain structure", "mass production friendly"],
        "forging_skill": "journeyman smith",
    },
    "Swift": {
        "element": "Aurum Argentum",
        "grade": "Precious precision alloy",
        "composition": ["silver", "gold", "platinum traces"],
        "hardness": 6.5,
        "ductility": 9.0,
        "conductivity": 9.5,
        "heat_resistance": 6.0,
        "corrosion_resistance": 9.5,
        "forge_temp_c": 1063,
        "temper_color": "rose-pink",
        "primary_use": "jewelry, precision instruments",
        "properties": ["work-hardenable", "biocompatible", "aesthetic malleability"],
        "forging_skill": "artisan goldsmith",
    },
    "Kotlin": {
        "element": "Damascus Composite",
        "grade": "Pattern-welded composite",
        "composition": ["iron", "nickel", "vanadium"],
        "hardness": 7.5,
        "ductility": 8.0,
        "conductivity": 6.5,
        "heat_resistance": 8.0,
        "corrosion_resistance": 8.5,
        "forge_temp_c": 1450,
        "temper_color": "purple-violet",
        "primary_use": "cutlery, architectural panels",
        "properties": ["layered strength", "aesthetic pattern", "jvm compatibility"],
        "forging_skill": "pattern welder",
    },
    "TypeScript": {
        "element": "Crystal Steel",
        "grade": "Optical-grade composite",
        "composition": ["borosilicate", "silica", "lanthanum"],
        "hardness": 7.0,
        "ductility": 8.5,
        "conductivity": 5.0,
        "heat_resistance": 8.5,
        "corrosion_resistance": 9.0,
        "forge_temp_c": 1700,
        "temper_color": "iridescent",
        "primary_use": "optics, medical devices",
        "properties": ["transparency to type information", "refractive precision", "diagnostic clarity"],
        "forging_skill": "optical glassblower",
    },
    "JavaScript": {
        "element": "Amorphous Polymer",
        "grade": "Thermoplastic compound",
        "composition": ["carbon", "hydrogen", "oxygen chains"],
        "hardness": 4.0,
        "ductility": 9.5,
        "conductivity": 3.0,
        "heat_resistance": 4.0,
        "corrosion_resistance": 8.0,
        "forge_temp_c": 200,
        "temper_color": "translucent amber",
        "primary_use": "packaging, flexible components",
        "properties": ["thermoplastic flexibility", "rapid prototyping", "ecosystem ubiquity"],
        "forging_skill": "plastic injection molder",
    },
    "Java": {
        "element": "Cast Iron",
        "grade": "Foundry-grade",
        "composition": ["iron", "carbon", "silicon"],
        "hardness": 7.5,
        "ductility": 4.0,
        "conductivity": 5.5,
        "heat_resistance": 8.5,
        "corrosion_resistance": 4.0,
        "forge_temp_c": 1200,
        "temper_color": "charcoal-grey",
        "primary_use": "engine blocks, pipes, cookware",
        "properties": ["high compressive strength", "excellent castability", "stable at scale"],
        "forging_skill": "foundry caster",
    },
    "C/C++": {
        "element": "Wootz Steel",
        "grade": "Ancient legendary alloy",
        "composition": ["iron", "carbon nanotubes", "rare earth elements"],
        "hardness": 9.0,
        "ductility": 3.5,
        "conductivity": 6.0,
        "heat_resistance": 9.0,
        "corrosion_resistance": 5.0,
        "forge_temp_c": 1500,
        "temper_color": "deep crimson",
        "primary_use": "legendary blades, historical monuments",
        "properties": ["carbon nanotube microstructure", "legendary edge retention", "ancient secret"],
        "forging_skill": "ancient master smith",
    },
}

# Compatibility matrix — how well pairs of metals combine
# Score: 1.0 (perfect blend) to 0.0 (catastrophic mismatch)
COMPATIBILITY_MATRIX: Dict[str, Dict[str, float]] = {
    "Rust":     {"Go": 0.70, "Swift": 0.60, "Kotlin": 0.75, "TypeScript": 0.55, "JavaScript": 0.40, "Java": 0.65, "C/C++": 0.85},
    "Go":       {"Rust": 0.70, "Swift": 0.65, "Kotlin": 0.80, "TypeScript": 0.60, "JavaScript": 0.55, "Java": 0.75, "C/C++": 0.70},
    "Swift":    {"Rust": 0.60, "Go": 0.65, "Kotlin": 0.85, "TypeScript": 0.75, "JavaScript": 0.60, "Java": 0.70, "C/C++": 0.55},
    "Kotlin":   {"Rust": 0.75, "Go": 0.80, "Swift": 0.85, "TypeScript": 0.70, "JavaScript": 0.65, "Java": 0.90, "C/C++": 0.60},
    "TypeScript":{"Rust": 0.55, "Go": 0.60, "Swift": 0.75, "Kotlin": 0.70, "JavaScript": 0.90, "Java": 0.65, "C/C++": 0.50},
    "JavaScript":{"Rust": 0.40, "Go": 0.55, "Swift": 0.60, "Kotlin": 0.65, "TypeScript": 0.90, "Java": 0.60, "C/C++": 0.45},
    "Java":     {"Rust": 0.65, "Go": 0.75, "Swift": 0.70, "Kotlin": 0.90, "TypeScript": 0.65, "JavaScript": 0.60, "C/C++": 0.70},
    "C/C++":    {"Rust": 0.85, "Go": 0.70, "Swift": 0.55, "Kotlin": 0.60, "TypeScript": 0.50, "JavaScript": 0.45, "Java": 0.70},
}

# Forge process descriptions per compatibility tier
FORGE_PROCESS: Dict[str, Dict[str, str]] = {
    "legendary": {
        "name": "Legendary Forge",
        "description": "Two metals enter perfect resonance. The ancient technique of folding the metals ten thousand times creates a blade of unparalleled sharpness.",
        "techniques": ["ten-thousand fold", "resonance tempering", "spirit quenching"],
        "cooling_medium": "moonlight oil",
        "hammer_strikes": "144 strikes at dawn",
    },
    "excellent": {
        "name": "Master Forge",
        "description": "A harmonious blend where both metals contribute their finest properties. The alloy achieves near-perfect grain structure.",
        "techniques": ["pattern welding", "layered lamination", "gradient tempering"],
        "cooling_medium": "quenching oil",
        "hammer_strikes": "49 strikes",
    },
    "good": {
        "name": "Standard Forge",
        "description": "A workable combination with distinct identities. Some metallurgical compromises but result is serviceable.",
        "techniques": ["basic lamination", "oil quench", "normalizing"],
        "cooling_medium": "linseed oil",
        "hammer_strikes": "21 strikes",
    },
    "challenging": {
        "name": "Experimental Forge",
        "description": "These metals resist bonding. Requires unconventional techniques and careful heat management to avoid metallurgical failure.",
        "techniques": ["explosive bonding", "rapid quench", "stress annealing"],
        "cooling_medium": "brine solution",
        "hammer_strikes": "7 strikes — too many risks cracking",
    },
}

# Alloy application domains based on primary metal
ALLOY_APPLICATIONS: Dict[str, List[str]] = {
    "Rust": ["systems software", "security-critical components", "concurrency primitives", "embedded firmware"],
    "Go": ["cloud infrastructure", "network services", "CLI tools", "distributed systems"],
    "Swift": ["iOS/macOS applications", "server-side services", "game development", "scientific computing"],
    "Kotlin": ["Android development", "JVM backend services", "multiplatform mobile", "scripting"],
    "TypeScript": ["web applications", "type-safe APIs", "developer tooling", "frontend architecture"],
    "JavaScript": ["prototyping", "web interactivity", "build tools", "full-stack web"],
    "Java": ["enterprise systems", "Android (legacy)", "large-scale backend", "big data processing"],
    "C/C++": ["operating systems", "game engines", "high-frequency trading", "embedded real-time systems"],
}


def get_tier(compatibility: float) -> str:
    if compatibility >= 0.85:
        return "legendary"
    elif compatibility >= 0.75:
        return "excellent"
    elif compatibility >= 0.60:
        return "good"
    else:
        return "challenging"


def compute_alloy_strength(primary: Dict, secondary: Dict, compatibility: float) -> float:
    """Compute an alloy strength score (0-10) from metal properties and compatibility."""
    base = (
        (primary["hardness"] + secondary["hardness"]) / 2 * 0.3
        + (primary["heat_resistance"] + secondary["heat_resistance"]) / 2 * 0.25
        + (primary["corrosion_resistance"] + secondary["corrosion_resistance"]) / 2 * 0.25
        + compatibility * 10 * 0.20
    )
    return round(min(base, 10.0), 2)


def select_pairing_languages(
    primary_language: str,
    languages: List[str],
    seed: Optional[int] = None,
) -> str:
    """Select a secondary language to pair with the primary.

    The secondary is chosen from languages that are NOT the primary.
    Uses a deterministic rng when seed is provided.
    """
    if seed is not None:
        rng = random.Random(seed)
    else:
        rng = random.Random()

    candidates = [l for l in languages if l != primary_language]
    return rng.choice(candidates)


def forge_alloy(
    primary_language: str,
    secondary_language: str,
    seed: Optional[int] = None,
) -> "AlloyCard":
    """Forge an alloy card from two programming languages.

    Args:
        primary_language: The main language (from rotation).
        secondary_language: The pairing language (auto-selected).
        seed: Optional random seed for reproducibility.

    Returns:
        An AlloyCard namedtuple describing the forged alloy.
    """
    primary = METAL_PROPERTIES[primary_language]
    secondary = METAL_PROPERTIES[secondary_language]

    compatibility = COMPATIBILITY_MATRIX.get(primary_language, {}).get(secondary_language, 0.5)
    tier = get_tier(compatibility)
    process = FORGE_PROCESS[tier]

    alloy_strength = compute_alloy_strength(primary, secondary, compatibility)

    # Determine primary applications
    apps = ALLOY_APPLICATIONS[primary_language]

    return AlloyCard(
        primary_language=primary_language,
        secondary_language=secondary_language,
        primary_element=primary["element"],
        secondary_element=secondary["element"],
        alloy_name=f"{primary['element']}-{secondary['element']} Alloy",
        compatibility_score=compatibility,
        tier=tier,
        forge_process=process,
        primary_properties=primary["properties"],
        secondary_properties=secondary["properties"],
        alloy_strength=alloy_strength,
        recommended_applications=apps,
    )


class AlloyCard(NamedTuple):
    primary_language: str
    secondary_language: str
    primary_element: str
    secondary_element: str
    alloy_name: str
    compatibility_score: float
    tier: str
    forge_process: Dict[str, str]
    primary_properties: List[str]
    secondary_properties: List[str]
    alloy_strength: float
    recommended_applications: List[str]


def advance_rotation(config_path: str) -> dict:
    """Read the rotation config, advance to the next language, and return updated data.

    Returns:
        Updated config dict with new current_index and last_language.
    """
    from .config import load_config, save_config
    from datetime import datetime, timezone

    data = load_config(config_path)
    languages = data["languages"]
    current_index = data["current_index"]

    new_index = (current_index + 1) % len(languages)
    data["current_index"] = new_index
    data["last_language"] = languages[new_index]
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_config(config_path, data)

    return data


def get_current_language(config_path: str) -> str:
    """Return the language at current_index in the rotation config."""
    from .config import load_config
    data = load_config(config_path)
    return data["languages"][data["current_index"]]


def generate_forge_card(
    config_path: str,
    seed: Optional[int] = None,
) -> dict:
    """Main entry point: advance rotation and generate an alloy card.

    Returns:
        {
            "current_language": str,
            "pairing_language": str,
            "alloy_card": AlloyCard,
        }
    """
    updated = advance_rotation(config_path)
    current = updated["last_language"]
    languages = updated["languages"]
    secondary = select_pairing_languages(current, languages, seed=seed)
    card = forge_alloy(current, secondary, seed=seed)
    return {
        "current_language": current,
        "pairing_language": secondary,
        "alloy_card": card,
    }


def format_alloy_card(result: dict) -> str:
    """Format an alloy card into a human-readable string."""
    card = result["alloy_card"]
    proc = card.forge_process
    tier_emojis = {"legendary": "🗡️", "excellent": "⚒️", "good": "🔧", "challenging": "🔥"}
    emoji = tier_emojis.get(card.tier, "⚙️")

    lines = [
        f"{'='*54}",
        f"  🏔️  POLYGLOT FORGE — Language Alloy Workshop  🏔️",
        f"{'='*54}",
        "",
        f"  🥇 Primary Metal : {card.primary_element}  [{card.primary_language}]",
        f"  🥈 Secondary Metal: {card.secondary_element}  [{card.secondary_language}]",
        f"",
        f"  ⚗️  Alloy Name   : {card.alloy_name}",
        f"  🔬 Compatibility : {card.compatibility_score:.0%}  [{card.tier}]",
        f"  💪 Alloy Strength: {card.alloy_strength}/10",
        f"",
        f"{'-'*54}",
        f"  {emoji} FORGE PROCESS: {proc['name']}",
        f"{'-'*54}",
        f"  {proc['description']}",
        f"",
        f"  🔥 Techniques    : {', '.join(proc['techniques'])}",
        f"  🧊 Cooling       : {proc['cooling_medium']}",
        f"  🔨 Hammer Strikes: {proc['hammer_strikes']}",
        f"",
        f"{'-'*54}",
        f"  ⚙️  Primary Properties [{card.primary_language}]:",
        f"    • " + "\n    • ".join(card.primary_properties),
        f"",
        f"  ⚙️  Secondary Properties [{card.secondary_language}]:",
        f"    • " + "\n    • ".join(card.secondary_properties),
        f"",
        f"{'-'*54}",
        f"  🛠️  Recommended Applications:",
        f"    • " + "\n    • ".join(card.recommended_applications),
        f"{'='*54}",
    ]
    return "\n".join(lines)
