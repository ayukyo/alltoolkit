#! /usr/bin/env python3
"""
Polyglot Spectrometer v1.0

A creative tool that decomposes how the rotation language expresses a universal
"Hello, World" program across 7 spectral bands, visualized as a spectroscopic
barcode signature.

Creative concept: "Every language refracts the same simple program through its
own unique prism. Like light through a spectrometer, code splits into distinct
spectral bands -- lexical tokens, syntactic structure, semantic depth, naming
conventions, control-flow complexity, type expressiveness, and IO patterns.
The resulting barcode is as unique as a fingerprint."

Each run:
  1. Reads language_rotation.json, advances current_index
  2. Selects the rotation language
  3. Decomposes a "Hello, World" implementation into 7 spectral bands
  4. Visualizes as an ASCII spectroscopic barcode
  5. Saves updated rotation config

Distinct from existing tools:
  - polyglot_resonance:   harmonic frequency shifts / waveform visualization
  - polyglot_dna:         genetic trait mapping (static molecular traits)
  - polyglot_meridian:    spectral positioning (coordinates in design space)
  - polyglot_resonator:   thinking philosophy (mental models & cognitive frames)
  - polyglot_signal:      signal semantics (alarm systems for conditions)
  - polyglot_craft:       practical skill cards (patterns, gotchas, exercises)
  - polyglot_harmony:     pairwise compatibility scores
  - language_archaeology: historical lineage (temporal origin)
  - language_compass:     learning journey maps (future milestones)
  - polyglot_chronicle:   daily diary + today's challenge (temporal today)
  - polyglot_digest:      syntax-parallel code snippets (spatial syntax)

Polyglot Spectrometer is about SPECTRAL DECOMPOSITION -- breaking the same
universal program down the 7 dimensions of language design, visualized as
a spectroscopic barcode that reveals each language's unique fingerprint.

Rotation order: Rust -> Go -> Swift -> Kotlin -> TypeScript -> JavaScript -> Java -> C/C++ -> Rust
"""

import json
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-spectrometer"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
    "language_rotation.json"
)

ROTATION_ORDER: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

# --------------------------------------------------------------------
# Hello World programs per language
# --------------------------------------------------------------------

HELLO_WORLD: Dict[str, str] = {
    "Rust": (
        "fn main() {\n"
        "    println!(\"Hello, World!\");\n"
        "}"
    ),
    "Go": (
        "package main\n\n"
        "import \"fmt\"\n\n"
        "func main() {\n"
        "    fmt.Println(\"Hello, World!\")\n"
        "}"
    ),
    "Swift": (
        "import Foundation\n\n"
        "func main() {\n"
        "    print(\"Hello, World!\")\n"
        "}\n\n"
        "main()"
    ),
    "Kotlin": (
        "fun main() {\n"
        "    println(\"Hello, World!\")\n"
        "}"
    ),
    "TypeScript": (
        "function main(): void {\n"
        "    console.log(\"Hello, World!\");\n"
        "}\n\n"
        "main();"
    ),
    "JavaScript": (
        "function main() {\n"
        "    console.log(\"Hello, World!\");\n"
        "}\n\n"
        "main();"
    ),
    "Java": (
        "public class Main {\n"
        "    public static void main(String[] args) {\n"
        "        System.out.println(\"Hello, World!\");\n"
        "    }\n"
        "}"
    ),
    "C/C++": (
        "#include <iostream>\n\n"
        "int main() {\n"
        "    std::cout << \"Hello, World!\" << std::endl;\n"
        "    return 0;\n"
        "}"
    ),
}

# --------------------------------------------------------------------
# Spectral band definitions
# --------------------------------------------------------------------

SPECTRAL_BANDS: List[Dict[str, Any]] = [
    {
        "id": "lexical",
        "name": "Lexical",
        "emoji": "🔤",
        "weight": 1.0,
        "description": "Token variety: keywords, symbols, literals",
    },
    {
        "id": "syntactic",
        "name": "Syntactic",
        "emoji": "🏗️",
        "weight": 1.0,
        "description": "Structural complexity: braces, indentation, newlines",
    },
    {
        "id": "semantic",
        "name": "Semantic",
        "emoji": "🧠",
        "weight": 1.0,
        "description": "Meaning density: meaningful words vs noise",
    },
    {
        "id": "naming",
        "name": "Naming",
        "emoji": "🏷️",
        "weight": 1.0,
        "description": "Identifier style and length",
    },
    {
        "id": "control_flow",
        "name": "Control Flow",
        "emoji": "🔀",
        "weight": 1.0,
        "description": "Branching, loops, function calls",
    },
    {
        "id": "type_system",
        "name": "Type System",
        "emoji": "📐",
        "weight": 1.0,
        "description": "Type annotations and expressiveness",
    },
    {
        "id": "io_pattern",
        "name": "IO Pattern",
        "emoji": "📤",
        "weight": 1.0,
        "description": "Output mechanism: print, puts, cout, println",
    },
]

# Bar characters for each score level (0-10)
BAR_CHARS: List[str] = [" ", "▌", "▌", "█", "█", "█", "▓", "▓", "▓", "▊", "▊"]

# --------------------------------------------------------------------
# Spectral analysis functions
# --------------------------------------------------------------------

def _analyze_lexical(code: str) -> Dict[str, Any]:
    """Band 1: Lexical -- token variety and density."""
    keywords = set(re.findall(
        r"\b(fn|func|function|fun|public|private|import|package|"
        r"include|use|struct|class|let|var|val|const|if|else|for|while|"
        r"return|int|String|str|void|main|static|public)\b", code))
    symbols = set(re.findall(r"[{}()\[\];,.<>!=+*/%&-]", code))
    literals = re.findall(r'"[^"]*"|\'[^\']*\'|\b\d+\b', code)
    token_count = len(keywords) + len(symbols) + len(literals)
    code_length = len(code.replace(" ", "").replace("\n", ""))
    density = token_count / max(code_length, 1) * 100
    score = min(10, int(density / 3))
    return {
        "score": score,
        "bar": BAR_CHARS[score] * 10,
        "keywords": sorted(keywords),
        "symbols_count": len(symbols),
        "literals_count": len(literals),
        "token_variety": len(keywords) + len(symbols),
        "detail": f"{len(keywords)} kw, {len(symbols)} sym, {len(literals)} lit -> {token_count} tokens",
    }


def _analyze_syntactic(code: str) -> Dict[str, Any]:
    """Band 2: Syntactic -- structural complexity."""
    lines = code.split("\n")
    non_empty = [l for l in lines if l.strip()]
    avg_indent = 0.0
    if non_empty:
        indent_levels = [len(l) - len(l.lstrip()) for l in non_empty]
        avg_indent = sum(indent_levels) / len(indent_levels)
    brace_pairs = code.count("{") + code.count("}")
    max_depth = 0
    depth = 0
    for ch in code:
        if ch == "{":
            depth += 1
            max_depth = max(max_depth, depth)
        elif ch == "}":
            depth -= 1
    structural_score = len(non_empty) * 0.3 + max_depth * 2 + brace_pairs * 0.5
    score = min(10, int(structural_score))
    return {
        "score": score,
        "bar": BAR_CHARS[score] * 10,
        "lines": len(non_empty),
        "max_nesting": max_depth,
        "brace_pairs": brace_pairs,
        "avg_indent": round(avg_indent, 1),
        "detail": f"{len(non_empty)} lines, depth={max_depth}, braces={brace_pairs}",
    }


def _analyze_semantic(code: str) -> Dict[str, Any]:
    """Band 3: Semantic -- meaning density."""
    words = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", code)
    stopwords = {"the", "a", "an", "is", "are", "was", "were", "be", "been",
                 "and", "or", "but", "in", "on", "at", "to", "for", "of",
                 "with", "by", "from", "as", "it", "this", "that"}
    meaningful = [w for w in words if w.lower() not in stopwords and len(w) > 1]
    code_length = len(code.replace(" ", "").replace("\n", ""))
    density = len(meaningful) / max(code_length, 1) * 100
    score = min(10, int(density / 2))
    return {
        "score": score,
        "bar": BAR_CHARS[score] * 10,
        "meaningful_words": meaningful[:15],
        "word_count": len(words),
        "meaningful_count": len(meaningful),
        "detail": f"{len(meaningful)} meaningful / {len(words)} total words",
    }


def _analyze_naming(code: str) -> Dict[str, Any]:
    """Band 4: Naming -- identifier style and expressiveness."""
    identifiers = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", code)
    long_names = [i for i in identifiers if len(i) >= 4]
    short_names = [i for i in identifiers
                   if len(i) <= 2 and i.lower() not in {"i", "j", "k", "x", "y", "z"}]
    camel_case = len(re.findall(r"[a-z][A-Z]", code))
    snake_case = len(re.findall(r"_[a-z]", code))
    pascal_case = len(re.findall(r"^[A-Z][a-z]", code, re.MULTILINE))
    total = len(identifiers)
    expressiveness = (len(long_names) / max(total, 1)) * 10 - (len(short_names) * 0.3)
    style_score = camel_case * 0.5 + snake_case * 0.3 + pascal_case * 0.4
    final = max(0, min(10, int(expressiveness + style_score)))
    return {
        "score": final,
        "bar": BAR_CHARS[final] * 10,
        "total_identifiers": len(identifiers),
        "long_names": len(long_names),
        "camel_case": camel_case,
        "snake_case": snake_case,
        "pascal_case": pascal_case,
        "detail": f"{len(identifiers)} idents, {len(long_names)} long, camel={camel_case}, snake={snake_case}",
    }


def _analyze_control_flow(code: str) -> Dict[str, Any]:
    """Band 5: Control Flow -- branching and function calls."""
    function_calls = len(re.findall(r"\b\w+\s*\(", code))
    function_defs = len(re.findall(
        r"\b(func|fn|function|fun|def|public|private)\s+\w+", code))
    branches = len(re.findall(r"\b(if|else|switch|case|when|match)\b", code))
    loops = len(re.findall(r"\b(for|while|loop|iterate)\b", code))
    total = function_calls + function_defs + branches + loops
    score = min(10, int(total * 0.8 + function_defs * 0.5))
    return {
        "score": score,
        "bar": BAR_CHARS[score] * 10,
        "function_defs": function_defs,
        "function_calls": function_calls,
        "branches": branches,
        "loops": loops,
        "detail": f"defs={function_defs}, calls={function_calls}, branches={branches}, loops={loops}",
    }


def _analyze_type_system(code: str) -> Dict[str, Any]:
    """Band 6: Type System -- type annotation expressiveness."""
    type_annotations = len(re.findall(
        r":\s*(int|string|str|String|bool|Boolean|f64|f32|i32|u32|void|"
        r"Option|Result|any|Any|Map|Vec|Array|T|usize)\b|<\w+>", code))
    generic_types = len(re.findall(r"<\w+>|<[^>]+>", code))
    total_declarations = len(re.findall(
        r"\b(let|var|const|val|fn|func|function|fun|def|public|private)\b", code))
    type_expressiveness = (
        (type_annotations + generic_types) / max(total_declarations, 1) * 10
        if total_declarations > 0 else 0
    )
    score = min(10, int(type_expressiveness + type_annotations * 0.3))
    return {
        "score": score,
        "bar": BAR_CHARS[score] * 10,
        "type_annotations": type_annotations,
        "generic_types": generic_types,
        "total_declarations": total_declarations,
        "detail": f"{type_annotations} type annotations, {generic_types} generics",
    }


def _analyze_io_pattern(code: str) -> Dict[str, Any]:
    """Band 7: IO Pattern -- output mechanism."""
    patterns = {
        "println": len(re.findall(r"println!\s*\(|\bprintln\s*\(", code)),
        "print": len(re.findall(r"print!\s*\(|\bprint\s*\(", code)),
        "fmt_print": len(re.findall(r"fmt\.Print", code)),
        "console_log": len(re.findall(r"console\.log", code)),
        "cout": len(re.findall(r"cout\s*<<|printf\s*\(", code)),
        "system_out": len(re.findall(r"System\.out\.print", code)),
        "puts": len(re.findall(r"\bputs\s*\(", code)),
        "echo": len(re.findall(r"\becho\s+", code)),
    }
    dominant = max(patterns, key=patterns.get)
    io_score = (
        sum(1 for v in patterns.values() if v > 0) * 1.5
        + patterns[dominant] * 0.5
    )
    score = min(10, int(io_score))
    return {
        "score": score,
        "bar": BAR_CHARS[score] * 10,
        "io_patterns": {k: v for k, v in patterns.items() if v > 0},
        "dominant_pattern": dominant,
        "detail": f"dominant={dominant} ({patterns[dominant]})",
    }


ANALYZERS: Dict[str, Any] = {
    "lexical": _analyze_lexical,
    "syntactic": _analyze_syntactic,
    "semantic": _analyze_semantic,
    "naming": _analyze_naming,
    "control_flow": _analyze_control_flow,
    "type_system": _analyze_type_system,
    "io_pattern": _analyze_io_pattern,
}


# --------------------------------------------------------------------
# Rotation helpers
# --------------------------------------------------------------------

def load_rotation() -> Dict[str, Any]:
    """Load language rotation config."""
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


# --------------------------------------------------------------------
# Core API
# --------------------------------------------------------------------

def spectrometer() -> Dict[str, Any]:
    """
    Main entry point: advance rotation, pick the language,
    run spectral analysis, return results.
    """
    config = load_rotation()
    languages = config.get("languages", ROTATION_ORDER)
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

    result = analyze_language(current_language)
    result["rotation_advanced"] = True
    result["next_language"] = languages[next_index % len(languages)]
    result["next_index"] = next_index
    return result


def analyze_language(language: str) -> Dict[str, Any]:
    """Run full spectral analysis for a given language."""
    if language not in HELLO_WORLD:
        raise ValueError(f"No Hello World sample for '{language}'")

    code = HELLO_WORLD[language]
    bands: List[Dict[str, Any]] = []

    for band_def in SPECTRAL_BANDS:
        band_id = band_def["id"]
        analyzer = ANALYZERS.get(band_id)
        if not analyzer:
            continue
        analysis = analyzer(code)
        bands.append({
            "id": band_id,
            "name": band_def["name"],
            "emoji": band_def["emoji"],
            "weight": band_def["weight"],
            "description": band_def["description"],
            "score": analysis["score"],
            "bar": analysis["bar"],
            "detail": analysis["detail"],
            "raw": {k: v for k, v in analysis.items() if k not in ("score", "bar")},
        })

    # Weighted composite score
    total_weight = sum(b["weight"] for b in bands)
    composite = sum(b["score"] * b["weight"] for b in bands) / max(total_weight, 1)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "language": language,
        "source_code": code,
        "bands": bands,
        "composite_score": round(composite, 2),
        "rotation_order": ROTATION_ORDER,
    }


def format_spectrometer(m: Dict[str, Any]) -> str:
    """Format the spectral analysis as a spectroscopic barcode display."""
    lang = m["language"]
    bands = m["bands"]
    composite = m["composite_score"]

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  🔬 POLYGLOT SPECTROMETER -- Language Spectral Fingerprinting     ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Language      : {lang:<47}║",
        f"║  Composite avg : {composite:.2f} / 10.00{' ' * 35}║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  📊 SPECTRAL BAND BARCODES                                     ║",
    ]

    for b in bands:
        lines.append(
            f"║  {b['emoji']} {b['name']:<11} │{b['bar']}│ {b['score']:2d}/10  {b['detail']:<28}║"
        )

    # ASCII spectroscopic barcode summary (vertical bars)
    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🖨️  SPECTROSCOPIC BARCODE (score per band, vertical)             ║",
    ]

    band_labels = [b["emoji"] for b in bands]
    band_scores = [b["score"] for b in bands]

    for level in range(10, 0, -1):
        row = "║  "
        for score in band_scores:
            ch = BAR_CHARS[level] if level <= score else " "
            row += f" {ch} "
        row += f"  ║  level {level:2d}"
        lines.append(row)

    lines.append("║  " + "─" * 29 + "║")
    lines.append("║  " + "  ".join(band_labels) + "  ║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  💻 SOURCE CODE                                                  ║",
    ]

    code_lines = m["source_code"].split("\n")
    for cl in code_lines[:12]:
        display = cl if len(cl) <= 50 else cl[:47] + "..."
        lines.append(f"║  {display:<52}  ║")
    if len(code_lines) > 12:
        lines.append(f"║  ... (+{len(code_lines) - 12} more lines){' ' * 37}║")

    lines += [
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  🔄 ROTATION ORDER                                               ║",
        f"║  {' -> '.join(ROTATION_ORDER):<58}║",
        "╚══════════════════════════════════════════════════════════════════╝",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------

def run_tests() -> None:
    """Run all tests for the polyglot_spectrometer module."""
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

    print("🔬 Polyglot Spectrometer -- Running Tests\n")

    # -- Rotation file --------------------------------------------------------
    try:
        config = load_rotation()
        t("load_rotation() returns valid dict", isinstance(config, dict))
        t("rotation has 'languages' key", "languages" in config)
        t("rotation has 'current_index' key", "current_index" in config)
    except Exception as e:
        t("load_rotation() succeeds", False, str(e))

    # -- ROTATION_ORDER ------------------------------------------------------
    for lang in ROTATION_ORDER:
        t(f"ROTATION_ORDER contains '{lang}'", lang in ROTATION_ORDER)

    # -- HELLO_WORLD ---------------------------------------------------------
    for lang in ROTATION_ORDER:
        t(f"HELLO_WORLD has sample for '{lang}'", lang in HELLO_WORLD)
        t(f"  sample for '{lang}' is non-empty", bool(HELLO_WORLD.get(lang, "")))

    # -- SPECTRAL_BANDS ------------------------------------------------------
    t("SPECTRAL_BANDS has 7 bands", len(SPECTRAL_BANDS) == 7)
    for band in SPECTRAL_BANDS:
        t(f"  Band '{band['id']}' has required fields",
          all(k in band for k in ("id", "name", "emoji", "weight")))

    # -- BAR_CHARS -----------------------------------------------------------
    t("BAR_CHARS has 11 entries", len(BAR_CHARS) == 11)
    t("BAR_CHARS[0] is space", BAR_CHARS[0] == " ")
    t("BAR_CHARS[10] is filled bar", BAR_CHARS[10] in ("▊", "█"))

    # -- Individual analyzers ------------------------------------------------
    sample_code = HELLO_WORLD["Rust"]
    for band_id, analyzer in ANALYZERS.items():
        try:
            result = analyzer(sample_code)
            t(f"Analyzer '{band_id}' returns dict", isinstance(result, dict))
            t(f"  Analyzer '{band_id}' has 'score' (0-10)", 0 <= result["score"] <= 10)
            t(f"  Analyzer '{band_id}' has 'bar' string", "bar" in result)
            t(f"  Analyzer '{band_id}' has 'detail' string", "detail" in result)
        except Exception as e:
            t(f"Analyzer '{band_id}' succeeds", False, str(e))

    # -- analyze_language ----------------------------------------------------
    for lang in HELLO_WORLD:
        try:
            result = analyze_language(lang)
            t(f"analyze_language('{lang}') succeeds", True)
            t(f"  Result has 'bands' (7 bands)", len(result["bands"]) == 7)
            t(f"  Result has 'composite_score'", "composite_score" in result)
            t(f"  Result has 'source_code'", "source_code" in result)
            t(f"  All bands have score 0-10",
              all(0 <= b["score"] <= 10 for b in result["bands"]))
            t(f"  All bands have bar string", all("bar" in b for b in result["bands"]))
            t(f"  Composite score is float", isinstance(result["composite_score"], float))
        except Exception as e:
            t(f"analyze_language('{lang}')", False, str(e))

    # -- spectrometer() advances rotation ------------------------------------
    try:
        cfg_before = load_rotation()
        idx_before = cfg_before["current_index"]
        lang_before = cfg_before["languages"][idx_before % len(cfg_before["languages"])]
        result = spectrometer()
        cfg_after = load_rotation()
        idx_after = cfg_after["current_index"]
        t("spectrometer() advances current_index",
          idx_after == (idx_before + 1) % len(cfg_before["languages"]))
        t("spectrometer() returns rotation_advanced=True",
          result.get("rotation_advanced") is True)
        t("spectrometer() returns the selected language",
          result.get("language") == lang_before)
        t("spectrometer() returns next_language", "next_language" in result)
        t("spectrometer() returns next_index", "next_index" in result)
    except Exception as e:
        t("spectrometer() rotation advancement", False, str(e))

    # -- format_spectrometer -------------------------------------------------
    try:
        m = analyze_language("Rust")
        formatted = format_spectrometer(m)
        t("format_spectrometer() returns a string", isinstance(formatted, str))
        t("format_spectrometer() starts with box-drawing char", formatted.startswith("╔"))
        t("format_spectrometer() ends with box-drawing char", formatted.rstrip().endswith("╝"))
        t("format_spectrometer() contains the language name", "Rust" in formatted)
        t("format_spectrometer() has barcode rows", "│" in formatted)
    except Exception as e:
        t("format_spectrometer()", False, str(e))

    # -- Unknown language raises ValueError ----------------------------------
    try:
        analyze_language("Brainfuck")
        t("Unknown language raises ValueError", False, "did not raise")
    except ValueError:
        t("Unknown language raises ValueError", True)
    except Exception as e:
        t("Unknown language raises ValueError", False, f"wrong exception: {e}")

    # -- Composite score range ------------------------------------------------
    for lang in HELLO_WORLD:
        try:
            m = analyze_language(lang)
            cs = m["composite_score"]
            t(f"Composite score for '{lang}' is 0-10", 0.0 <= cs <= 10.0)
        except Exception as e:
            t(f"Composite score for '{lang}'", False, str(e))

    # -- Rotation index wraps correctly --------------------------------------
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
        result = spectrometer()
        print(format_spectrometer(result))
