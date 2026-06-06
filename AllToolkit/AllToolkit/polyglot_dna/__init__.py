#! /usr/bin/env python3
"""
🧬 Polyglot DNA v1.0
A creative tool that decodes programming languages into DNA sequences.

Creative concept: "Every language has a genetic code — a sequence of traits
that define its identity. Polyglot DNA sequences these traits into a visual
double-helix metaphor, revealing what makes each language unique."

Each language's DNA consists of genes encoding:
  - Memory model (who manages memory?)
  - Type system (static vs dynamic, strong vs weak)
  - Concurrency approach (threads, actors, goroutines, async...)
  - Paradigm (OO, functional, procedural, multi-paradigm)
  - Error handling philosophy (exceptions vs values)
  - Performance character (compiled, interpreted, VM)

The tool generates:
  1. A "DNA sequence" (visual ASCII art helix + string representation)
  2. Gene annotations explaining each trait
  3. Compatibility matrix with other languages (can you port to it easily?)
  4. A "mutation comparison" showing how two languages differ

Distinct from existing tools:
  - language_archaeology:   historical lineage & design philosophy (temporal)
  - language_compass:       learning journey maps (progress)
  - language_synapse:       conceptual bridges between languages (cross-section)
  - polyglot_chronicle:     daily diary + history + challenge (temporal today)
  - polyglot_digest:        side-by-side syntax parallel (spatial comparison)
  - language_ethos:         philosophical manifesto (belief/identity)
  - language_sage:          idioms, tips, pitfalls (practical wisdom)
  - language_ecohub:        package ecosystem guide (tooling)

Polyglot DNA is about GENETIC MAPPING — the underlying trait sequence
that defines each language's identity at the molecular level.
"""

import json
import os
import random
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "polyglot-dna"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "language_rotation.json"
)

# ── Nucleotide base mapping ────────────────────────────────────────────────────
# Each base (A, T, G, C) encodes a spectrum of traits
NUCLEOTIDE_MEANING = {
    "A": "Adapts at runtime (interpreted / JIT)",
    "T": "Types are proven at compile time",
    "G": "Garbage-collected (runtime memory management)",
    "C": "Compiled to native machine code (AOT)",
}
COMPLEMENT = {"A": "T", "T": "A", "G": "C", "C": "G"}


def load_rotation():
    """Load language rotation config."""
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data):
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Language DNA definitions ───────────────────────────────────────────────────
# Each gene position encodes a specific trait. Positions 0-9:
#  0: Memory model
#  1: Type system
#  2: Null safety
#  3: Concurrency model
#  4: Error handling
#  5: Primary paradigm
#  6: Performance character
#  7: Abstraction mechanism
#  8: Module/package system
#  9: Development philosophy
LANGUAGE_DNA: Dict[str, str] = {
    # 10 genes × 3 chars (2 nucleotide + 1 dash separator) = 30 chars per language
    # Gene positions: 0=Memory, 1=Types, 2=NullSafety, 3=Concurrency, 4=Errors,
    #                 5=Paradigm, 6=Performance, 7=Abstraction, 8=Modules, 9=Philosophy
    "Rust":        "TC-GT-CT-GC-AC-CT-GT-CT-GT-CT",  # 10 genes
    "Go":          "AC-GT-AT-TC-TT-CT-TT-TT-TT-TT",
    "Swift":       "TC-GT-CT-GT-AT-CT-TT-GT-GT-GT",
    "Kotlin":      "TC-GT-CT-TA-AT-CT-TT-TT-TT-TG",
    "TypeScript":  "TC-GT-AT-TA-AT-TT-TT-TT-TT-TT",
    "JavaScript":  "AC-GT-AA-TA-AT-TT-AT-TT-TT-TT",
    "Java":        "TC-GT-CT-TA-AT-CT-TT-TT-TT-TT",
    "C/C++":       "CC-CT-CC-GC-CC-CC-CC-CC-CC-CC",
}


def _normalize(seq: str) -> str:
    """Remove dash separators for computation."""
    return seq.replace("-", "")


def _gap(seq: str, pos: int) -> str:
    """Return the gene at position (each gene is 3 chars)."""
    return seq[pos * 3 : (pos + 1) * 3]


GENE_NAMES = [
    "Memory Model",
    "Type System",
    "Null Safety",
    "Concurrency",
    "Error Handling",
    "Paradigm",
    "Performance",
    "Abstraction",
    "Module System",
    "Philosophy",
]

GENE_LEGENDS: Dict[int, Dict[str, str]] = {
    0: {  # Memory Model
        "A": "Garbage collected — runtime reclaims memory automatically",
        "C": "Manual/Custom — programmer explicitly manages memory",
        "T": "Ownership/ARC — compile-time or reference-counted, no GC",
        "G": "Hybrid — escape analysis + GC for short-lived objects",
    },
    1: {  # Type System
        "A": "Dynamic — types resolved at runtime, very flexible",
        "C": "Static nominal — types declared, checked at compile time",
        "T": "Static structural — types inferred, shape-based checking",
        "G": "Dependent/Refined — types carry runtime value constraints",
    },
    2: {  # Null Safety
        "A": "Null is a value — no null safety, easy foot-guns",
        "C": "No null type — use Optional/Option explicitly",
        "T": "Nullable type — T? is distinct from T, enforced",
        "G": "Non-null by default — null requires explicit annotation",
    },
    3: {  # Concurrency
        "A": "Async/await — single-threaded event loop, cooperative",
        "C": "Actors/CSP — message-passing, memory isolation guaranteed",
        "T": "Threads + Send/Sync — compile-time data race prevention",
        "G": "Coroutines — structured concurrency with lightweight stacks",
    },
    4: {  # Error Handling
        "A": "Errors as values — return Result/Option, handle explicitly",
        "C": "Checked exceptions — compiler enforces error declaration",
        "T": "Unchecked exceptions — throw/catch, caller may ignore",
        "G": "Multiple mechanisms — Result + exceptions coexist",
    },
    5: {  # Primary Paradigm
        "A": "Functional-first — pure functions, immutability, composition",
        "C": "Object-oriented — classes, inheritance, encapsulation",
        "T": "Multi-paradigm — blends OO, functional, and procedural",
        "G": "Systems-oriented — low-level control, procedural core",
    },
    6: {  # Performance
        "A": "Interpreted — portable, moderate speed, warm-up time",
        "C": "AOT compiled — maximum performance, static binary",
        "T": "JIT compiled — adaptive optimization, fast after warm-up",
        "G": "VM bytecode — portable execution, moderate performance",
    },
    7: {  # Abstraction
        "A": "Interfaces/protocols — implicit satisfaction, duck typing",
        "C": "Traits/tYPE CLASSES — explicit contracts, generic bounds",
        "T": "Inheritance hierarchies — classical subtype polymorphism",
        "G": "Extension methods — add behavior to closed types freely",
    },
    8: {  # Module System
        "A": "File-based — modules = files, implicit dependencies",
        "C": "Explicit packages — namespaces, import/export statements",
        "T": "Hierarchical packages — nested namespaces, visibility modifiers",
        "G": "Workspace/crate — multi-module projects, dependency graphs",
    },
    9: {  # Development Philosophy
        "A": "Pragmatic — simplicity over purity, get things done",
        "C": "Principled — correctness over convenience, safety first",
        "T": "Balanced — ergonomics and safety both valued",
        "G": "Expressive — powerful features, complex but capable",
    },
}


def _annotate_gene(seq: str, gene_idx: int) -> List[Dict[str, str]]:
    """Return annotation for a single gene position."""
    gene_seq = _gap(seq, gene_idx)
    base = gene_seq[0]  # first char is the nucleotide
    gene_name = GENE_NAMES[gene_idx]
    legend = GENE_LEGENDS[gene_idx]
    meaning = legend.get(base, "Unknown gene variant")
    return {
        "position": gene_idx,
        "nucleotide": base,
        "gene_name": gene_name,
        "meaning": meaning,
    }


def generate_dna_sequence(language: str) -> Dict[str, Any]:
    """Main function: generate full DNA analysis for a language."""
    if language not in LANGUAGE_DNA:
        raise ValueError(f"Unknown language: {language}. Available: {list(LANGUAGE_DNA.keys())}")

    raw_seq = LANGUAGE_DNA[language]
    normalized = _normalize(raw_seq)

    # ── Build double helix ASCII art ──────────────────────────────────────────
    lines = []
    complement_seq = "".join(COMPLEMENT.get(c, c) for c in normalized if c in COMPLEMENT)
    seq_len = len(normalized)
    cols = min(seq_len, 30)  # cap width for display
    lines.append("  ╔══╤══╤══╤══╗  ╔══╤══╤══╤══╗")
    lines.append("  ║  │  │  │  ║  ║  │  │  │  ║")
    lines.append("──╫══╪══╪══╪══╫──╫══╪══╪══╪══╫──")
    lines.append("  ║  │  │  │  ║  ║  │  │  │  ║")
    lines.append("  ╚══╧══╧══╧══╝  ╚══╧══╧══╧══╝")
    lines.append(f"  5' ──────────────────────────────── 3'")
    lines.append(f"  Sequence: {normalized[:cols]}{'...' if seq_len > cols else ''}")
    lines.append(f"  Length: {seq_len} base pairs (genes: {len(GENE_NAMES)})")

    # ── Gene annotations ─────────────────────────────────────────────────────
    genes = [_annotate_gene(raw_seq, i) for i in range(len(GENE_NAMES))]

    # ── Helix visual (compact) ───────────────────────────────────────────────
    helix_rows = []
    display = normalized[:40]
    for i, base in enumerate(display):
        comp = COMPLEMENT.get(base, base)
        row_num = i % 10
        if row_num == 0:
            helix_rows.append("")
        helix_rows.append(f"  {base} ────── {comp}")

    return {
        "language": language,
        "dna_sequence": raw_seq,
        "dna_normalized": normalized,
        "length_bp": len(normalized),
        "gene_count": len(GENE_NAMES),
        "helix_art": "\n".join(helix_rows),
        "flat_sequence_display": normalized[:50] + ("..." if len(normalized) > 50 else ""),
        "genes": genes,
    }


def compare_dna(lang_a: str, lang_b: str) -> Dict[str, Any]:
    """Compare two languages' DNA and find mutations (differences)."""
    seq_a = _normalize(LANGUAGE_DNA.get(lang_a, ""))
    seq_b = _normalize(LANGUAGE_DNA.get(lang_b, ""))
    if not seq_a or not seq_b:
        raise ValueError("One or both languages not found in DNA database")

    max_len = max(len(seq_a), len(seq_b))
    mutations = []
    for i in range(max_len):
        a = seq_a[i] if i < len(seq_a) else "-"
        b = seq_b[i] if i < len(seq_b) else "-"
        if a != b:
            gene_idx = i  # approximate gene index
            gene_name = GENE_NAMES[gene_idx] if gene_idx < len(GENE_NAMES) else "Unknown"
            mutations.append({
                "position": i,
                "gene_index": gene_idx,
                "gene_name": gene_name,
                f"{lang_a}_base": a,
                f"{lang_b}_base": b,
            })

    similarity = 1 - (len(mutations) / max_len) if max_len > 0 else 0

    return {
        "language_a": lang_a,
        "language_b": lang_b,
        "similarity_score": round(similarity, 3),
        "mutation_count": len(mutations),
        "mutations": mutations,
        "summary": f"{lang_a} and {lang_b} share {round(similarity * 100, 1)}% of their DNA — {len(mutations)} gene differences.",
    }


def compatibility_score(lang_from: str, lang_to: str) -> Dict[str, Any]:
    """Estimate how hard it is to port from one language to another."""
    comparison = compare_dna(lang_from, lang_to)
    sim = comparison["similarity_score"]

    # Semantic difficulty tiers
    if sim >= 0.9:
        difficulty = "Effortless"
        note = "Nearly identical DNA — expect near-mechanical translation."
    elif sim >= 0.7:
        difficulty = "Moderate"
        note = "Some significant mutations; idioms will differ."
    elif sim >= 0.5:
        difficulty = "Challenging"
        note = "Major paradigm differences; architecture may need rethinking."
    else:
        difficulty = "Revolutionary"
        note = "Very different genetic makeups; treat as a full rewrite."

    return {
        "from": lang_from,
        "to": lang_to,
        "similarity": sim,
        "difficulty": difficulty,
        "note": note,
        "mutation_count": comparison["mutation_count"],
    }


# ── Rotation-aware entry point ─────────────────────────────────────────────────

def dna() -> Dict[str, Any]:
    """
    Main entry: advance rotation and generate DNA for the selected language.
    Reads current_index from language_rotation.json, selects that language,
    advances index, saves, then returns the DNA analysis.
    """
    config = load_rotation()
    languages = config.get("languages", [])
    if not languages:
        raise ValueError("No languages found in rotation config")

    current_index = config.get("current_index", 0)
    current_language = languages[current_index % len(languages)]

    # Advance for next run
    next_index = (current_index + 1) % len(languages)
    config["current_index"] = next_index
    config["last_language"] = current_language
    config["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation(config)

    result = generate_dna_sequence(current_language)
    result["rotation_advanced"] = True
    result["next_language"] = languages[next_index]
    result["next_index"] = next_index
    return result


# ── Tests ─────────────────────────────────────────────────────────────────────

def run_tests():
    """Run all tests for the polyglot_dna module."""
    import sys

    errors = []
    passed = 0

    def t(name: str, cond: bool, msg: str = ""):
        nonlocal passed, errors
        if cond:
            print(f"  ✅ {name}")
            passed += 1
        else:
            print(f"  ❌ {name}: {msg}")
            errors.append(name)

    print("🧬 Polyglot DNA — Running Tests\n")

    # Test: rotation file exists and is valid JSON
    try:
        config = load_rotation()
        t("load_rotation() returns valid dict", isinstance(config, dict))
        t("rotation has languages list", "languages" in config)
        t("rotation has current_index", "current_index" in config)
    except Exception as e:
        t("load_rotation() succeeds", False, str(e))

    # Test: LANGUAGE_DNA has all 8 languages
    for lang in ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]:
        t(f"LANGUAGE_DNA has '{lang}'", lang in LANGUAGE_DNA)

    # Test: DNA sequences have 2 nucleotides per gene × 10 genes = 20 chars
    for lang, seq in LANGUAGE_DNA.items():
        norm = _normalize(seq)
        t(f"{lang} DNA encodes 10 genes (20 nt)", len(norm) == len(GENE_NAMES) * 2,
          f"got {len(norm)}")

    # Test: generate_dna_sequence
    for lang in LANGUAGE_DNA:
        try:
            result = generate_dna_sequence(lang)
            t(f"generate_dna_sequence('{lang}') succeeds", True)
            t(f"  - returns 'genes' list", isinstance(result.get("genes"), list))
            t(f"  - returns 'helix_art'", "helix_art" in result)
            t(f"  - gene count matches", len(result["genes"]) == len(GENE_NAMES))
            t(f"  - gene positions are 0..{len(GENE_NAMES)-1}",
              [g["position"] for g in result["genes"]] == list(range(len(GENE_NAMES))))
            # Check all expected keys in each gene
            for g in result["genes"]:
                t(f"  - gene has required keys", all(k in g for k in ["position", "nucleotide", "gene_name", "meaning"]))
        except Exception as e:
            t(f"generate_dna_sequence('{lang}')", False, str(e))

    # Test: compare_dna
    try:
        cmp = compare_dna("Rust", "Go")
        t("compare_dna('Rust', 'Go') succeeds", True)
        t("compare_dna returns similarity_score", "similarity_score" in cmp)
        t("compare_dna returns mutation_count", "mutation_count" in cmp)
        t("compare_dna returns mutations list", isinstance(cmp.get("mutations"), list))
        t("similarity between 0 and 1", 0 <= cmp["similarity_score"] <= 1)
    except Exception as e:
        t("compare_dna('Rust', 'Go')", False, str(e))

    # Test: compare_dna symmetric
    try:
        cmp_ab = compare_dna("Rust", "Go")
        cmp_ba = compare_dna("Go", "Rust")
        t("compare_dna is symmetric (similarity)", cmp_ab["similarity_score"] == cmp_ba["similarity_score"])
    except Exception as e:
        t("compare_dna symmetry", False, str(e))

    # Test: compatibility_score
    try:
        score = compatibility_score("JavaScript", "TypeScript")
        t("compatibility_score('JS', 'TS') succeeds", True)
        t("compatibility_score has difficulty", "difficulty" in score)
        t("difficulty is non-empty string", isinstance(score.get("difficulty"), str) and score["difficulty"])
    except Exception as e:
        t("compatibility_score", False, str(e))

    # Test: dna() advances rotation
    try:
        cfg_before = load_rotation()
        idx_before = cfg_before["current_index"]
        lang_before = cfg_before["languages"][idx_before % len(cfg_before["languages"])]
        result = dna()
        cfg_after = load_rotation()
        idx_after = cfg_after["current_index"]
        t("dna() advances current_index", idx_after == (idx_before + 1) % len(cfg_before["languages"]))
        t("dna() returns rotation_advanced=True", result.get("rotation_advanced") is True)
        t("dna() returns selected language", result.get("language") == lang_before)
        t("dna() returns next_language", "next_language" in result)
    except Exception as e:
        t("dna() rotation advancement", False, str(e))

    # Test: unknown language raises ValueError
    try:
        generate_dna_sequence("Brainfuck")
        t("Unknown language raises ValueError", False, "did not raise")
    except ValueError as e:
        t("Unknown language raises ValueError", True)
    except Exception as e:
        t("Unknown language raises ValueError", False, f"wrong exception: {e}")

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
        result = dna()
        print(json.dumps(result, indent=2))