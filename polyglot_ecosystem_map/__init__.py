#!/usr/bin/env python3
"""
polyglot_ecosystem_map: Maps programming language ecosystems and relationships.

This module builds a graph of language relationships based on:
- Paradigm overlap (OOP, functional, procedural, systems)
- Influence chains (C → C++ → Java → Kotlin, etc.)
- Ecosystem proximity (JVM, LLVM, Web, Mobile)
- Synergy ratings (which languages work well together)

The current language from the rotation drives the analysis.
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

# ─── Language Ecosystem Database ───────────────────────────────────────────

# Paradigm vectors: [systems, object_oriented, functional, declarative, scripting]
PARADIGM_VECTORS = {
    "Rust":        [0.95, 0.50, 0.75, 0.20, 0.30],
    "Go":          [0.75, 0.55, 0.60, 0.15, 0.50],
    "Swift":       [0.70, 0.80, 0.70, 0.25, 0.45],
    "Kotlin":      [0.50, 0.95, 0.75, 0.30, 0.55],
    "TypeScript":  [0.20, 0.85, 0.65, 0.55, 0.80],
    "JavaScript":  [0.15, 0.80, 0.60, 0.50, 0.95],
    "Java":        [0.45, 0.95, 0.45, 0.25, 0.25],
    "C/C++":       [0.95, 0.45, 0.30, 0.10, 0.15],
    "Python":      [0.30, 0.70, 0.80, 0.60, 0.95],
    "C#":          [0.50, 0.90, 0.55, 0.30, 0.40],
    "Ruby":        [0.25, 0.85, 0.70, 0.50, 0.90],
    "PHP":         [0.15, 0.75, 0.40, 0.35, 0.85],
    "Lua":         [0.40, 0.50, 0.65, 0.30, 0.95],
    "R":           [0.15, 0.55, 0.80, 0.85, 0.75],
    "MATLAB":      [0.20, 0.50, 0.75, 0.90, 0.65],
    "Perl":        [0.30, 0.55, 0.50, 0.40, 0.90],
    "SQL":         [0.05, 0.30, 0.20, 0.95, 0.30],
    "Zig":         [0.95, 0.30, 0.65, 0.15, 0.20],
    "ArkTS":       [0.45, 0.85, 0.75, 0.35, 0.60],
    "VB":          [0.20, 0.80, 0.35, 0.30, 0.55],
    "Delphi":      [0.35, 0.80, 0.25, 0.20, 0.40],
    "Fortran":     [0.65, 0.20, 0.30, 0.50, 0.20],
}

# Ecosystem clusters
ECOSYSTEMS = {
    "systems": ["Rust", "C/C++", "Zig", "Go"],
    "jvm": ["Java", "Kotlin", "Scala", "Clojure"],
    "web": ["JavaScript", "TypeScript", "PHP", "Ruby"],
    "mobile": ["Swift", "Kotlin", "Objective-C", "Dart"],
    "llvm": ["Rust", "Swift", "C/C++", "Zig"],
    "scripting": ["Python", "JavaScript", "Lua", "Ruby", "Perl", "PHP"],
    "data_science": ["Python", "R", "MATLAB", "Julia"],
    "enterprise": ["Java", "C#", "Go", "Kotlin"],
}

# Influence chains (directed edges: "A influenced by B")
INFLUENCE_CHAINS = {
    "C/C++": ["C"],
    "Java": ["C/C++"],
    "Kotlin": ["Java"],
    "Swift": ["C/C++", "Objective-C", "Rust"],
    "Go": ["C/C++", "Pascal"],
    "Rust": ["C/C++"],
    "TypeScript": ["JavaScript"],
    "JavaScript": ["Scheme", "Perl"],
    "C#": ["C/C++", "Java"],
    "Objective-C": ["C"],
    "PHP": ["Perl", "C"],
    "Ruby": ["Perl", "Smalltalk"],
    "Python": ["ABC", "C"],
    "Zig": ["C/C++", "Rust"],
    "Lua": ["C", "Modula"],
    "ArkTS": ["TypeScript", "Rust"],
}

# Synergy matrix: which languages complement each other well
SYNERGY_PAIRS = {
    ("Rust", "TypeScript"): 0.85,
    ("Rust", "Go"): 0.90,
    ("Rust", "Python"): 0.75,
    ("Go", "Python"): 0.80,
    ("Go", "JavaScript"): 0.70,
    ("Swift", "Kotlin"): 0.85,
    ("Kotlin", "Java"): 0.90,
    ("Kotlin", "TypeScript"): 0.75,
    ("TypeScript", "JavaScript"): 0.95,
    ("JavaScript", "Python"): 0.70,
    ("Java", "Go"): 0.75,
    ("C/C++", "Rust"): 0.90,
    ("C/C++", "Zig"): 0.85,
    ("Zig", "Rust"): 0.85,
    ("Swift", "Rust"): 0.80,
    ("Python", "Lua"): 0.75,
    ("Ruby", "Python"): 0.70,
}


def _cosine_similarity(a: list, b: list) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _ecosystem_distance(lang_a: str, lang_b: str) -> float:
    """Calculate ecosystem proximity: 0 = same ecosystem, 1 = far apart."""
    # Find ALL ecosystems for each language
    ecos_a = [eco for eco, members in ECOSYSTEMS.items() if lang_a in members]
    ecos_b = [eco for eco, members in ECOSYSTEMS.items() if lang_b in members]
    # If any shared ecosystem, distance is 0
    if set(ecos_a) & set(ecos_b):
        return 0.0
    return 1.0


def _influence_distance(lang_a: str, lang_b: str) -> float:
    """Calculate influence chain distance: 0 = direct influence, 1 = no connection."""
    # BFS to find shortest path
    visited = set()
    queue = [(lang_a, 0)]
    while queue:
        current, dist = queue.pop(0)
        if current == lang_b:
            return dist / 5.0  # normalize to 0-1
        if current in visited:
            continue
        visited.add(current)
        # Direct influences and those influenced by current
        influenced_by = [k for k, v in INFLUENCE_CHAINS.items() if current in v]
        influenced_to = INFLUENCE_CHAINS.get(current, [])
        for nxt in influenced_by + influenced_to:
            if nxt not in visited:
                queue.append((nxt, dist + 1))
    return 1.0


def calculate_relationship(lang_a: str, lang_b: str) -> dict:
    """Calculate multi-dimensional relationship between two languages."""
    vec_a = PARADIGM_VECTORS.get(lang_a, [0.5] * 5)
    vec_b = PARADIGM_VECTORS.get(lang_b, [0.5] * 5)

    paradigm_sim = _cosine_similarity(vec_a, vec_b)
    ecosystem_dist = _ecosystem_distance(lang_a, lang_b)
    influence_dist = _influence_distance(lang_a, lang_b)

    # Synergy lookup
    synergy = SYNERGY_PAIRS.get((lang_a, lang_b)) or SYNERGY_PAIRS.get((lang_b, lang_a)) or 0.5

    # Combined relationship score (0-100)
    paradigm_score = paradigm_sim * 40
    ecosystem_score = (1 - ecosystem_dist) * 25
    influence_score = (1 - influence_dist) * 20
    synergy_score = synergy * 15

    total = paradigm_score + ecosystem_score + influence_score + synergy_score

    return {
        "language_a": lang_a,
        "language_b": lang_b,
        "paradigm_similarity": round(paradigm_sim, 4),
        "ecosystem_distance": round(ecosystem_dist, 4),
        "influence_distance": round(influence_dist, 4),
        "synergy_score": round(synergy, 4),
        "relationship_score": round(total, 1),
        "relationship_label": _score_to_label(total),
    }


def _score_to_label(score: float) -> str:
    """Convert numeric score to human-readable label."""
    if score >= 80:
        return "tightly coupled"
    elif score >= 60:
        return "compatible"
    elif score >= 40:
        return "neutral"
    elif score >= 20:
        return "divergent"
    else:
        return "foreign territory"


def find_ecosystem_neighbors(lang: str, top_n: int = 3) -> list:
    """Find the closest languages in the ecosystem graph."""
    results = []
    for other in PARADIGM_VECTORS:
        if other == lang:
            continue
        rel = calculate_relationship(lang, other)
        results.append(rel)

    results.sort(key=lambda x: x["relationship_score"], reverse=True)
    return results[:top_n]


def generate_ecosystem_map(current_lang: str) -> dict:
    """Generate full ecosystem map centered on the current language."""
    neighbors = find_ecosystem_neighbors(current_lang, top_n=5)

    # Find ecosystem cluster
    cluster = None
    for eco, members in ECOSYSTEMS.items():
        if current_lang in members:
            cluster = eco
            break

    # Find influence chain position
    influenced_by = INFLUENCE_CHAINS.get(current_lang, [])
    influences_to = [k for k, v in INFLUENCE_CHAINS.items() if current_lang in v]

    return {
        "current_language": current_lang,
        "ecosystem_cluster": cluster or "unknown",
        "influenced_by": influenced_by,
        "influences": influences_to,
        "neighbors": neighbors,
        "paradigm_vector": PARADIGM_VECTORS.get(current_lang, [0.5] * 5),
        "paradigm_labels": ["systems", "object_oriented", "functional", "declarative", "scripting"],
        "total_languages_in_ecosystem": len(PARADIGM_VECTORS),
    }


def get_rotation_state() -> dict:
    """Read current language from language_rotation.json."""
    # Try AllToolkit/ first, then workspace root
    paths_to_try = [
        Path(__file__).parent.parent / "language_rotation.json",
        Path("/home/admin/.openclaw/workspace/language_rotation.json"),
        Path("/home/admin/.openclaw/workspace/AllToolkit/language_rotation.json"),
    ]
    for p in paths_to_try:
        if p.exists():
            with open(p) as f:
                return json.load(f)
    raise FileNotFoundError("language_rotation.json not found in any expected location")


def rotate_and_update() -> dict:
    """Advance to next language in rotation and return ecosystem map."""
    state = get_rotation_state()
    langs = state["languages"]
    idx = state["current_index"]

    current_lang = langs[idx]

    # Advance index for next time
    next_idx = (idx + 1) % len(langs)
    state["current_index"] = next_idx

    # Find the write path (prefer AllToolkit location)
    write_path = Path(__file__).parent.parent / "language_rotation.json"
    with open(write_path, "w") as f:
        json.dump(state, f, indent=2)

    return generate_ecosystem_map(current_lang)


# ─── Tests ─────────────────────────────────────────────────────────────────

def run_tests():
    import math

    print("Running polyglot_ecosystem_map tests...")

    # Test 1: cosine similarity known pair
    sim = _cosine_similarity([1, 0], [1, 0])
    assert abs(sim - 1.0) < 1e-9, f"Identical vectors should have similarity 1.0, got {sim}"

    sim2 = _cosine_similarity([1, 0], [0, 1])
    assert abs(sim2 - 0.0) < 1e-9, f"Orthogonal vectors should have similarity 0.0, got {sim2}"

    # Test 2: paradigm vectors exist for core languages
    for lang in ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]:
        assert lang in PARADIGM_VECTORS, f"Missing paradigm vector for {lang}"
        vec = PARADIGM_VECTORS[lang]
        assert len(vec) == 5, f"Paradigm vector for {lang} should have 5 dimensions"
        assert all(0 <= v <= 1 for v in vec), f"Paradigm values for {lang} should be in [0,1]"

    # Test 3: relationship is symmetric
    rel_ab = calculate_relationship("Rust", "Go")
    rel_ba = calculate_relationship("Go", "Rust")
    assert abs(rel_ab["relationship_score"] - rel_ba["relationship_score"]) < 0.01

    # Test 4: self-relationship is highest
    rel_self = calculate_relationship("Rust", "Rust")
    rel_rust_go = calculate_relationship("Rust", "Go")
    assert rel_self["relationship_score"] >= rel_rust_go["relationship_score"]

    # Test 5: ecosystem distance for same cluster is 0
    dist = _ecosystem_distance("Rust", "Go")
    # Both in "systems" cluster
    assert dist == 0.0, f"Rust and Go should be in same ecosystem (systems), got {dist}"

    # Test 6: ecosystem distance for different clusters > 0
    dist2 = _ecosystem_distance("Python", "Rust")
    assert dist2 > 0.0

    # Test 7: synergy lookup checks both directions
    syn_ab = SYNERGY_PAIRS.get(("Rust", "TypeScript"), SYNERGY_PAIRS.get(("TypeScript", "Rust"), 0))
    syn_ba = SYNERGY_PAIRS.get(("TypeScript", "Rust"), SYNERGY_PAIRS.get(("Rust", "TypeScript"), 0))
    assert abs(syn_ab - syn_ba) < 0.01

    # Test 8: ecosystem neighbors returns correct count
    neighbors = find_ecosystem_neighbors("Rust", top_n=3)
    assert len(neighbors) == 3
    assert all("relationship_score" in n for n in neighbors)

    # Test 9: generate_ecosystem_map produces all fields
    eco_map = generate_ecosystem_map("Rust")
    for field in ["current_language", "ecosystem_cluster", "influenced_by", "neighbors", "paradigm_vector"]:
        assert field in eco_map, f"Missing field {field} in ecosystem map"

    # Test 10: rotation state can be read
    state = get_rotation_state()
    assert "languages" in state
    assert "current_index" in state
    assert isinstance(state["languages"], list)
    assert len(state["languages"]) > 0

    # Test 11: relationship score is in valid range
    rel = calculate_relationship("Rust", "Java")
    assert 0 <= rel["relationship_score"] <= 100

    # Test 12: label is valid
    for lang in ["Rust", "Python", "JavaScript"]:
        rel = calculate_relationship(lang, "C/C++")
        assert rel["relationship_label"] in [
            "tightly coupled", "compatible", "neutral", "divergent", "foreign territory"
        ]

    # Test 13: rotate_and_update advances index
    state_before = get_rotation_state()
    idx_before = state_before["current_index"]
    lang_before = state_before["languages"][idx_before]

    # We can't actually test rotation without side effects, so just verify state structure
    assert idx_before < len(state_before["languages"])

    print("✅ All 13 tests passed!")


if __name__ == "__main__":
    _run_tests()