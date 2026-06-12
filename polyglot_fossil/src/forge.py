#!/usr/bin/env python3
"""
🪨 Polyglot Fossil — Core Engine

Identifies inherited syntax and conceptual "fossils" across the programming
language rotation chain. Each fossil is classified as INHERITED (carried from
an ancestor), MUTATED (changed from an ancestor form), or NOVEL (newly evolved).
"""

import json
import textwrap
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .config import (
    ANCESTOR_DEPTH,
    ANCESTOR_MAP,
    FOSSIL_DEFINITIONS,
    ROTATION_FILE,
    ROTATION_ORDER,
)


# ── Enums ────────────────────────────────────────────────────────────────────

class FossilClassification(str, Enum):
    INHERITED = "INHERITED"   # Carried from ancestor, recognizably similar
    MUTATED  = "MUTATED"    # Present but significantly changed from ancestor
    NOVEL    = "NOVEL"      # Evolved anew in this language
    ABSENT   = "ABSENT"     # Not present in this language

    def symbol(self) -> str:
        return {
            "INHERITED": "◉",
            "MUTATED":   "◌",
            "NOVEL":     "✦",
            "ABSENT":    "—",
        }[self.value]


# ── Dataclasses ──────────────────────────────────────────────────────────────

@dataclass
class FossilRecord:
    """A single fossil found in a language."""
    fossil_id: str
    name: str
    concept: str
    classification: FossilClassification
    detail: str          # Language-specific syntax/behavior
    ancestral_form: str   # What it looks like in the ancestor
    stratum: int          # How many steps back the ancestor is (1 = direct parent)
    ancestor: str        # Which ancestor this came from (empty if NOVEL)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fossil_id": self.fossil_id,
            "name": self.name,
            "concept": self.concept,
            "classification": self.classification.value,
            "detail": self.detail,
            "ancestral_form": self.ancestral_form,
            "stratum": self.stratum,
            "ancestor": self.ancestor,
        }

    def layer_bar(self, max_depth: int = ANCESTOR_DEPTH) -> str:
        """Render a stratified layer bar showing depth."""
        filled = "█" * self.stratum
        empty = "░" * (max_depth - self.stratum)
        depth_label = f"L{self.stratum}"
        return f"[{filled}{empty}] {depth_label}"

    def badge(self) -> str:
        return f"{self.classification.symbol()} {self.classification.value}"


# ── Rotation Helpers ──────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    """Load language rotation config."""
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def get_rotation_chain(language: str) -> List[str]:
    """
    Get the rotation chain starting from `language` and walking through
    its predecessors in the rotation order.
    E.g., for TypeScript (reversed file): [TypeScript, Kotlin, Swift, Go, Rust, C/C++, Java, JavaScript]
    """
    if language not in ROTATION_ORDER:
        return [language]

    rot_idx = ROTATION_ORDER.index(language)
    rot_len = len(ROTATION_ORDER)

    # Walk backward via offset: offset 1 → (rot_idx+1)%8 (direct predecessor)
    # This wraps correctly: Rust(7)+1→C/C++(0), Go(6)+1→Rust(7), TS(3)+1→Kotlin(4)
    chain = [language]
    for offset in range(1, rot_len):
        prev_idx = (rot_idx + offset) % rot_len
        prev_lang = ROTATION_ORDER[prev_idx]
        if prev_lang == language:
            break
        chain.append(prev_lang)

    return chain


def get_ancestors(language: str, depth: int = ANCESTOR_DEPTH) -> List[Tuple[str, int]]:
    """
    Return ancestors of `language` with their stratum depth.
    Each tuple is (ancestor_language, stratum) where stratum=1 is the direct predecessor
    in the rotation order.
    """
    if language not in ROTATION_ORDER:
        return []

    rot_idx = ROTATION_ORDER.index(language)
    rot_len = len(ROTATION_ORDER)
    ancestors: List[Tuple[str, int]] = []

    # Walk forward via offset: offset 1 → (rot_idx+1)%8 (direct predecessor)
    # This wraps correctly: Rust(7)+1→C/C++(0), Go(6)+1→Rust(7), TS(3)+1→Kotlin(4)
    for stratum in range(1, depth + 1):
        prev_idx = (rot_idx + stratum) % rot_len
        prev_lang = ROTATION_ORDER[prev_idx]
        if prev_lang == language:
            break
        ancestors.append((prev_lang, stratum))

    return ancestors
    return result


# ── Fossil Analysis ──────────────────────────────────────────────────────────

def classify_fossil(
    fossil_id: str,
    language: str,
    ancestors: List[Tuple[str, int]],
) -> FossilRecord:
    """
    Classify how a fossil manifests in `language` given its `ancestors`.
    """
    fd = FOSSIL_DEFINITIONS[fossil_id]
    carriers = fd.get("carriers", {})

    if language not in carriers:
        return FossilRecord(
            fossil_id=fossil_id,
            name=fd["name"],
            concept=fd["concept"],
            classification=FossilClassification.ABSENT,
            detail="",
            ancestral_form="",
            stratum=0,
            ancestor="",
        )

    detail = carriers[language]

    # Find closest ancestor that also carries this fossil
    closest_ancestor = ""
    closest_stratum = 99
    for anc, stratum in ancestors:
        if anc in carriers:
            closest_ancestor = anc
            closest_stratum = stratum
            break

    if not closest_ancestor:
        # No ancestor carries it → NOVEL
        return FossilRecord(
            fossil_id=fossil_id,
            name=fd["name"],
            concept=fd["concept"],
            classification=FossilClassification.NOVEL,
            detail=detail,
            ancestral_form="",
            stratum=0,
            ancestor="",
        )

    ancestral_form = carriers[closest_ancestor]

    # Classify: INHERITED if very similar, MUTATED if different
    if _is_similar(detail, ancestral_form):
        classification = FossilClassification.INHERITED
    else:
        classification = FossilClassification.MUTATED

    return FossilRecord(
        fossil_id=fossil_id,
        name=fd["name"],
        concept=fd["concept"],
        classification=classification,
        detail=detail,
        ancestral_form=ancestral_form,
        stratum=closest_stratum,
        ancestor=closest_ancestor,
    )


def _is_similar(a: str, b: str) -> bool:
    """
    Heuristic: two fossil forms are 'similar' if they share significant
    structural or keyword DNA.
    """
    # Strip syntax noise
    keywords_a = set(a.lower().split())
    keywords_b = set(b.lower().split())

    # Remove generic tokens
    noise = {"the", "a", "an", "of", "in", "to", "and", "or", "for", "with"}
    keywords_a -= noise
    keywords_b -= noise

    # Direct match of key syntax markers
    key_markers = {"option", "nullable", "result", "match", "switch", "when",
                   "enum", "struct", "trait", "impl", "fn", "func", "fun",
                   "let", "var", "const", "type", "class", "interface",
                   "pub", "pub", "mut", "move", "async", "await", "suspend",
                   "iter", "iterator", "channel", "goroutine", "coroutine",
                   "nil", "null", "none", "void", "undefined"}
    shared = keywords_a & keywords_b & key_markers
    if shared:
        return True

    # Check if one is a subset of the other (common in inheritance)
    if keywords_a <= keywords_b or keywords_b <= keywords_a:
        return True

    return False


def get_fossils(language: str) -> List[FossilRecord]:
    """
    Excavate all fossils for `language`, returning classified FossilRecords.
    """
    ancestors = get_ancestors(language)
    records = []

    for fossil_id in FOSSIL_DEFINITIONS:
        record = classify_fossil(fossil_id, language, ancestors)
        records.append(record)

    return records


# ── Strata Summary ────────────────────────────────────────────────────────────

def build_strata_summary(records: List[FossilRecord]) -> Dict[str, Any]:
    """Aggregate fossil records into a strata summary."""
    by_classification: Dict[str, List[FossilRecord]] = {}
    by_stratum: Dict[int, List[FossilRecord]] = {}

    for rec in records:
        by_classification.setdefault(rec.classification.value, []).append(rec)
        by_stratum.setdefault(rec.stratum, []).append(rec)

    return {
        "total": len(records),
        "by_classification": {k: len(v) for k, v in by_classification.items()},
        "by_stratum": {k: len(v) for k, v in by_stratum.items()},
    }


# ── Text Renderer ─────────────────────────────────────────────────────────────

def _section(label: str, text: str, width: int = 62) -> str:
    lines = textwrap.wrap(text, width=width)
    sep = "─" * (width + 2)
    header = f"  {label}"
    padded = header + " " * (width - len(header)) + " │"
    content = "\n".join(f"  {line}" + " " * (width - len(line)) + " │" for line in lines)
    return f"┌{sep}┐\n{padded}\n{content}\n└{sep}┘"


def _render_record(rec: FossilRecord, max_depth: int = ANCESTOR_DEPTH) -> str:
    badge = rec.badge()
    name = rec.name
    concept = rec.concept[:48] + ("…" if len(rec.concept) > 48 else "")
    layer = rec.layer_bar(max_depth)
    detail = rec.detail[:42] + ("…" if len(rec.detail) > 42 else "")

    if rec.classification == FossilClassification.ABSENT:
        detail_line = f"  ✗ Not present in this language"
    elif rec.classification == FossilClassification.NOVEL:
        detail_line = f"  ✦ NEW     │ {detail}"
    elif rec.classification == FossilClassification.INHERITED:
        anc_line = f"  ◉ from {rec.ancestor} ({layer})"
        detail_line = f"  {detail}"
        return f"{badge} {name}\n{anc_line}\n  {detail_line}"
    else:  # MUTATED
        anc_line = f"  ◌ evolved  │ ancestral: {rec.ancestral_form[:38]}"
        detail_line = f"  {detail}"
        return f"{badge} {name}\n{anc_line}\n  {detail_line}"

    return f"{badge} {name}\n  {detail_line}"


def render_dig_report(
    language: str,
    chain: List[str],
    records: List[FossilRecord],
    summary: Dict[str, Any],
) -> str:
    """Render a full archaeological dig report."""
    inherited = [r for r in records if r.classification == FossilClassification.INHERITED]
    mutated  = [r for r in records if r.classification == FossilClassification.MUTATED]
    novel    = [r for r in records if r.classification == FossilClassification.NOVEL]
    absent   = [r for r in records if r.classification == FossilClassification.ABSENT]

    chain_display = " → ".join(chain)
    chain_filled = f"  ROTATION CHAIN: {chain_display}"
    chain_wrapped = textwrap.wrap(chain_filled, width=62)
    chain_lines = "\n".join(f"  {line}" for line in chain_wrapped)

    strata = f"""
╔══════════════════════════════════════════════════════════════════════╗
║       🪨  POLYGLOT FOSSIL — ARCHAEOLOGICAL DIG REPORT  🪨             ║
╠══════════════════════════════════════════════════════════════════════╣
║  Language     : {language:<54} ║
╠══════════════════════════════════════════════════════════════════════╣
║  ROTATION CHAIN (oldest → current)                                   ║
║                                                                      ║
║{chain_lines[:62] + ' ' * max(0, 62 - len(chain_lines[:62]))} ║
╠══════════════════════════════════════════════════════════════════════╣
║  STRATA SUMMARY                                                       ║
║  ◉ INHERITED  : {len(inherited):<3} fossils   ║
║  ◌ MUTATED   : {len(mutated):<3} fossils    ║
║  ✦ NOVEL     : {len(novel):<3} fossils    ║
║  — ABSENT    : {len(absent):<3} fossils   ║
╠══════════════════════════════════════════════════════════════════════╣
║  FOSSIL LAYERS (stratified by ancestor depth)                         ║"""

    # Build fossil list
    fossil_lines = []
    for rec in sorted(records, key=lambda r: (
        0 if r.classification == FossilClassification.INHERITED else
        1 if r.classification == FossilClassification.MUTATED else
        2 if r.classification == FossilClassification.NOVEL else 3,
        r.stratum,
        r.name,
    )):
        badge = rec.badge()
        name = rec.name
        concept = rec.concept[:44] + ("…" if len(rec.concept) > 44 else "")
        layer = rec.layer_bar()

        if rec.classification == FossilClassification.ABSENT:
            fossil_lines.append(f"║  {badge} {name:<36} {layer}  ║")
        elif rec.classification == FossilClassification.NOVEL:
            fossil_lines.append(f"║  {badge} {name:<36} {layer}  ║")
        else:
            anc = f"← {rec.ancestor}" if rec.ancestor else ""
            fossil_lines.append(f"║  {badge} {name:<36} {layer} {anc}  ║")

    # Pad fossil lines
    while len(fossil_lines) % 4 != 0:
        fossil_lines.append("║" + " " * 62 + "║")

    rows = []
    for i in range(0, len(fossil_lines), 4):
        rows.append("\n".join(fossil_lines[i:i+4]))

    fossil_block = "\n".join(rows)

    return f"""
{strata}
{fossil_block}
╚══════════════════════════════════════════════════════════════════════╝"""


# ── Main API ────────────────────────────────────────────────────────────────

def fossil_dig(language: Optional[str] = None) -> Dict[str, Any]:
    """
    Main entry point. Reads rotation, selects current language, excavates
    fossils, and returns structured data with a rendered report.

    Updates language_rotation.json when done.
    """
    config = load_rotation()
    languages = config["languages"]

    if language is None:
        current_idx = config.get("current_index", 0)
        language = languages[current_idx % len(languages)]

    if language not in ROTATION_ORDER:
        language = ROTATION_ORDER[0]

    chain = get_rotation_chain(language)
    ancestors = get_ancestors(language)
    records = get_fossils(language)
    summary = build_strata_summary(records)
    report = render_dig_report(language, chain, records, summary)

    # Advance rotation
    current_idx = languages.index(language) if language in languages else 0
    next_idx = (current_idx + 1) % len(languages)

    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)

    return {
        "tool": "polyglot-fossil",
        "version": "0.1.0",
        "language": language,
        "rotation_chain": chain,
        "ancestors": [{"ancestor": anc, "stratum": d} for anc, d in ancestors],
        "fossils": [r.to_dict() for r in records],
        "strata_summary": summary,
        "report": report,
        "next_language": languages[next_idx],
        "rotated_at": config["updated_at"],
    }