#!/usr/bin/env python3
"""
🎛️ Polyglot Compile Cache v1.0

A tool that simulates compilation cache behavior and build performance characteristics
across the language rotation:
`Rust -> Go -> Swift -> Kotlin -> TypeScript -> JavaScript -> Java -> C/C++ -> Rust (loop)`

## Creative Concept

**"Every language compiles differently — this tool makes the invisible visible."**

Compilers are black boxes. This tool demystifies the build pipeline by simulating:
- **Incremental compilation**: how fast is a recompile after a tiny change?
- **Cache warming**: how does the compiler learn from your code?
- **Binary size**: what does your code weigh after compilation?
- **Optimization depth**: what LLVM/O2/O3 passes does this language's compiler run?
- **Type checking overhead**: how expensive is the type system's work?

Distinct from existing tools:
  - polyglot_syntax_matrix: syntax side-by-side (what it looks like)
  - syntax_translator: real translation between languages (what it does)
  - language_probe: runtime characteristics (how it behaves)
  - polyglot_resonator: philosophical mental models (how it thinks)
  - compile_cache: build pipeline characteristics (how it compiles)

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

import json
import os
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-compile-cache"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = "/home/admin/.openclaw/workspace/AllToolkit/language_rotation.json"

ROTATION_LANGUAGES = [
    "Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"
]

LANG_EMOJI = {
    "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
    "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "C/C++": "⚙️"
}

# ─────────────────────────────────────────────────────────────────
# Compiler Metadata Database
# ─────────────────────────────────────────────────────────────────

COMPILER_META_DB: Dict[str, Dict[str, Any]] = {
    "Rust": {"language": "Rust",
        "compiler": "rustc + LLVM",
        "version_hint": "1.75+ (incremental by default)",
        "pipeline": [
            {"name": "Parsing", "description": "Parse into AST", "duration_ms": 15, "cacheable": True, "parallelizable": False},
            {"name": "Name Resolution", "description": "Resolve imports and names", "duration_ms": 30, "cacheable": True, "parallelizable": True},
            {"name": "Type Checking", "description": "HIR type inference and borrow check", "duration_ms": 80, "cacheable": True, "parallelizable": True},
            {"name": "MIR Lowering", "description": "Mid-level IR generation", "duration_ms": 25, "cacheable": True, "parallelizable": True},
            {"name": "LLVM Codegen", "description": "LLVM IR → machine code", "duration_ms": 120, "cacheable": False, "parallelizable": True},
            {"name": "LLVM Optimization", "description": "LTO + LLVM passes (O3)", "duration_ms": 200, "cacheable": False, "parallelizable": True},
            {"name": "Linking", "description": "Link all crates", "duration_ms": 40, "cacheable": False, "parallelizable": False},
        ],
        "incremental": {
            "full_rebuild_ms": 500, "after_small_change_ms": 45,
            "after_type_change_ms": 180, "cache_hit_ratio": 0.85,
            "unchanged_modules_reused": 8, "total_modules": 10,
        },
        "binary_size_kb": 850,
        "optimization_passes": [
            "Inline", "Loop Vectorization", "LTO", "Copy Propagation",
            "Dead Code Elimination", "Constant Folding", "Memory Promotion",
        ],
        "type_checker_cost": "very_high",
        "cold_build_time_s": 8.5,
        "incremental_speedup": 11.1,
        "memory_usage_mb": 512,
        "lto_overhead_s": 3.2,
        "lto_binary_reduction": 0.72,
    },
    "Go": {"language": "Go",
        "compiler": "gc (go build)",
        "version_hint": "1.21+",
        "pipeline": [
            {"name": "Parsing", "description": "Parse Go source", "duration_ms": 12, "cacheable": True, "parallelizable": False},
            {"name": "Type Checking", "description": "Type check all packages", "duration_ms": 45, "cacheable": True, "parallelizable": True},
            {"name": "AST → SSA", "description": "Convert to Static Single Assignment", "duration_ms": 35, "cacheable": True, "parallelizable": True},
            {"name": "SSA Lowering", "description": "Lower generic operations", "duration_ms": 20, "cacheable": True, "parallelizable": True},
            {"name": "Native Code Gen", "description": "Generate machine code", "duration_ms": 60, "cacheable": False, "parallelizable": True},
            {"name": "Linking", "description": "Link all packages", "duration_ms": 25, "cacheable": False, "parallelizable": False},
        ],
        "incremental": {
            "full_rebuild_ms": 280, "after_small_change_ms": 35,
            "after_type_change_ms": 120, "cache_hit_ratio": 0.82,
            "unchanged_modules_reused": 12, "total_modules": 15,
        },
        "binary_size_kb": 1200,
        "optimization_passes": [
            "Inlining", "Dead Code Elimination", "Peephole Optimization", "Register Allocation",
        ],
        "type_checker_cost": "medium",
        "cold_build_time_s": 4.8,
        "incremental_speedup": 8.0,
        "memory_usage_mb": 350,
        "lto_overhead_s": 0.0,
        "lto_binary_reduction": 1.0,
    },
    "Swift": {"language": "Swift",
        "compiler": "swiftc + LLVM",
        "version_hint": "5.9+",
        "pipeline": [
            {"name": "Parsing", "description": "Parse Swift source", "duration_ms": 18, "cacheable": True, "parallelizable": False},
            {"name": "SIL Generation", "description": "Swift Intermediate Language", "duration_ms": 40, "cacheable": True, "parallelizable": True},
            {"name": "SIL Optimization", "description": "Swift-level optimizations", "duration_ms": 90, "cacheable": True, "parallelizable": True},
            {"name": "IR Generation", "description": "LLVM IR generation", "duration_ms": 50, "cacheable": False, "parallelizable": True},
            {"name": "LLVM Optimization", "description": "LLVM passes", "duration_ms": 150, "cacheable": False, "parallelizable": True},
            {"name": "Code Generation", "description": "Machine code emission", "duration_ms": 60, "cacheable": False, "parallelizable": True},
            {"name": "Linking", "description": "Link with linker", "duration_ms": 30, "cacheable": False, "parallelizable": False},
        ],
        "incremental": {
            "full_rebuild_ms": 620, "after_small_change_ms": 55,
            "after_type_change_ms": 220, "cache_hit_ratio": 0.78,
            "unchanged_modules_reused": 7, "total_modules": 12,
        },
        "binary_size_kb": 1400,
        "optimization_passes": [
            "Generic Specialization", "Devirtualization", "COP Memory Analysis",
            "LLVM Vectorization", "LTO", "ARC Optimization",
        ],
        "type_checker_cost": "high",
        "cold_build_time_s": 12.0,
        "incremental_speedup": 11.3,
        "memory_usage_mb": 800,
        "lto_overhead_s": 4.5,
        "lto_binary_reduction": 0.68,
    },
    "Kotlin": {"language": "Kotlin",
        "compiler": "kotlinc (JVM)",
        "version_hint": "1.9+",
        "pipeline": [
            {"name": "Parsing", "description": "Parse Kotlin source", "duration_ms": 25, "cacheable": True, "parallelizable": False},
            {"name": "Resolution", "description": "Resolve symbols and types", "duration_ms": 60, "cacheable": True, "parallelizable": True},
            {"name": "Type Checking", "description": "Kotlin type inference", "duration_ms": 55, "cacheable": True, "parallelizable": True},
            {"name": "IR Generation", "description": "Kotlin IR for JVM", "duration_ms": 40, "cacheable": False, "parallelizable": True},
            {"name": "JVM Bytecode", "description": "Generate .class bytecode", "duration_ms": 30, "cacheable": False, "parallelizable": True},
            {"name": "Linking", "description": "Compile modules together", "duration_ms": 20, "cacheable": False, "parallelizable": False},
        ],
        "incremental": {
            "full_rebuild_ms": 450, "after_small_change_ms": 40,
            "after_type_change_ms": 160, "cache_hit_ratio": 0.80,
            "unchanged_modules_reused": 10, "total_modules": 14,
        },
        "binary_size_kb": 600,
        "optimization_passes": [
            "Inline Functions", "Dead Code Elimination", "Box Elimination", "JVM Inlining",
        ],
        "type_checker_cost": "high",
        "cold_build_time_s": 7.5,
        "incremental_speedup": 9.4,
        "memory_usage_mb": 600,
        "lto_overhead_s": 0.0,
        "lto_binary_reduction": 1.0,
    },
    "TypeScript": {"language": "TypeScript",
        "compiler": "tsc (TypeScript compiler)",
        "version_hint": "5.3+",
        "pipeline": [
            {"name": "Parsing", "description": "Parse TS → AST", "duration_ms": 20, "cacheable": True, "parallelizable": False},
            {"name": "Binding", "description": "Symbol resolution", "duration_ms": 30, "cacheable": True, "parallelizable": True},
            {"name": "Type Checking", "description": "Full type inference", "duration_ms": 70, "cacheable": True, "parallelizable": True},
            {"name": "Transform", "description": "TS → JS transformation", "duration_ms": 25, "cacheable": False, "parallelizable": True},
            {"name": "Emit", "description": "JavaScript + sourcemaps", "duration_ms": 15, "cacheable": False, "parallelizable": True},
        ],
        "incremental": {
            "full_rebuild_ms": 180, "after_small_change_ms": 25,
            "after_type_change_ms": 90, "cache_hit_ratio": 0.88,
            "unchanged_modules_reused": 15, "total_modules": 18,
        },
        "binary_size_kb": 0,
        "optimization_passes": [
            "Tree Shaking", "Minification", "Babel transforms",
        ],
        "type_checker_cost": "medium",
        "cold_build_time_s": 3.2,
        "incremental_speedup": 7.2,
        "memory_usage_mb": 280,
        "lto_overhead_s": 0.0,
        "lto_binary_reduction": 1.0,
    },
    "JavaScript": {"language": "JavaScript",
        "compiler": "V8 / Node / Browser JIT",
        "version_hint": "ES2023+",
        "pipeline": [
            {"name": "Parsing", "description": "Parse JS to AST", "duration_ms": 8, "cacheable": False, "parallelizable": False},
            {"name": "Baseline Compile", "description": "Ignition bytecode interpreter", "duration_ms": 12, "cacheable": False, "parallelizable": False},
            {"name": "Optimizing Compile", "description": "TurboFan JIT (hot paths)", "duration_ms": 40, "cacheable": False, "parallelizable": False},
            {"name": "Deoptimization", "description": "On invalid type assumptions", "duration_ms": 20, "cacheable": False, "parallelizable": False},
        ],
        "incremental": {
            "full_rebuild_ms": 0, "after_small_change_ms": 0,
            "after_type_change_ms": 0, "cache_hit_ratio": 0.0,
            "unchanged_modules_reused": 0, "total_modules": 0,
        },
        "binary_size_kb": 0,
        "optimization_passes": [
            "Inlining", "Hidden Class Transitions", "Inline Caching",
            "TurboFan Optimization", "Escape Analysis", "Dead Code Elimination",
        ],
        "type_checker_cost": "none",
        "cold_build_time_s": 0.0,
        "incremental_speedup": 1.0,
        "memory_usage_mb": 0,
        "lto_overhead_s": 0.0,
        "lto_binary_reduction": 1.0,
    },
    "Java": {"language": "Java",
        "compiler": "javac + JVM JIT",
        "version_hint": "21+",
        "pipeline": [
            {"name": "Parsing", "description": "Parse .java to AST", "duration_ms": 22, "cacheable": True, "parallelizable": False},
            {"name": "Annotation Processing", "description": "Annotation processors", "duration_ms": 35, "cacheable": True, "parallelizable": True},
            {"name": "Type Checking", "description": "Symbol resolution + type checking", "duration_ms": 50, "cacheable": True, "parallelizable": True},
            {"name": "Desugar", "description": "Lambda + switch desugaring", "duration_ms": 30, "cacheable": False, "parallelizable": True},
            {"name": "Bytecode Generation", "description": "Generate .class files", "duration_ms": 28, "cacheable": False, "parallelizable": True},
            {"name": "Linking", "description": "Classpath resolution", "duration_ms": 15, "cacheable": False, "parallelizable": False},
        ],
        "incremental": {
            "full_rebuild_ms": 380, "after_small_change_ms": 38,
            "after_type_change_ms": 145, "cache_hit_ratio": 0.81,
            "unchanged_modules_reused": 11, "total_modules": 13,
        },
        "binary_size_kb": 550,
        "optimization_passes": [
            "JVM JIT Tiered Compilation", "Escape Analysis", "Inline Caching",
            "Lock Elision", "Devirtualization", "Scalar Replacement",
        ],
        "type_checker_cost": "medium",
        "cold_build_time_s": 6.2,
        "incremental_speedup": 10.0,
        "memory_usage_mb": 480,
        "lto_overhead_s": 0.0,
        "lto_binary_reduction": 1.0,
    },
    "C/C++": {"language": "C/C++",
        "compiler": "gcc/clang + LLVM",
        "version_hint": "C++20 / C23",
        "pipeline": [
            {"name": "Preprocessing", "description": "#include expansion, macro substitution", "duration_ms": 30, "cacheable": False, "parallelizable": True},
            {"name": "Parsing", "description": "C++ grammar to AST", "duration_ms": 25, "cacheable": True, "parallelizable": False},
            {"name": "Template Instantiation", "description": "SFINAE + template expansion", "duration_ms": 100, "cacheable": False, "parallelizable": True},
            {"name": "Name Lookup", "description": "ADL + namespace resolution", "duration_ms": 20, "cacheable": True, "parallelizable": True},
            {"name": "Code Generation", "description": "AST → LLVM IR", "duration_ms": 45, "cacheable": False, "parallelizable": True},
            {"name": "Optimization", "description": "LLVM passes (O2/O3)", "duration_ms": 180, "cacheable": False, "parallelizable": True},
            {"name": "Assembly", "description": "Machine code emission", "duration_ms": 35, "cacheable": False, "parallelizable": True},
            {"name": "Linking", "description": "Symbol resolution + relocations", "duration_ms": 50, "cacheable": False, "parallelizable": False},
        ],
        "incremental": {
            "full_rebuild_ms": 550, "after_small_change_ms": 60,
            "after_type_change_ms": 250, "cache_hit_ratio": 0.75,
            "unchanged_modules_reused": 9, "total_modules": 14,
        },
        "binary_size_kb": 920,
        "optimization_passes": [
            "Template Instantiation", "Inline", "Vectorization", "LTO",
            "Dead Code Elimination", "Constant Propagation", "Loop Unrolling",
        ],
        "type_checker_cost": "very_high",
        "cold_build_time_s": 9.8,
        "incremental_speedup": 9.2,
        "memory_usage_mb": 700,
        "lto_overhead_s": 5.0,
        "lto_binary_reduction": 0.65,
    },
}

# ─────────────────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    """Load language rotation config."""
    try:
        with open(ROTATION_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"languages": ROTATION_LANGUAGES, "current_index": 0, "last_language": None, "updated_at": None}


def save_rotation(data: Dict[str, Any]) -> None:
    """Save updated rotation config."""
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


def build_pipeline_diagram(meta: Dict[str, Any]) -> str:
    """Build a text diagram of the compilation pipeline."""
    stages = meta["pipeline"]
    lang_name = meta.get("language", meta.get("language", "Unknown"))
    total_ms = sum(s["duration_ms"] for s in stages)
    max_ms = max(s["duration_ms"] for s in stages) or 1

    stage_lines = []
    for stage in stages:
        bar_len = int((stage["duration_ms"] / max_ms) * 30)
        bar = "█" * bar_len
        cache_icon = "⚡" if stage["cacheable"] else "⏱"
        para_icon = "∥" if stage["parallelizable"] else "○"
        stage_lines.append(
            f"  {cache_icon}{para_icon} {stage['name']:<25} {stage['duration_ms']:>6}ms │{bar}"
        )

    binary_note = f" ({meta['binary_size_kb']}KB)" if meta["binary_size_kb"] > 0 else " (interpreted/transpiled)"
    return (
        f"Compilation Pipeline: {lang_name} ({meta['compiler']})\n"
        f"──{'─' * 51}\n"
        + "\n".join(stage_lines) + "\n"
        f"──{'─' * 51}\n"
        f"Total: {total_ms}ms (cold build: {meta['cold_build_time_s']:.1f}s){binary_note}"
    )


def build_benchmarks() -> List[Dict[str, Any]]:
    """Build cross-language benchmark comparisons."""
    return [
        {
            "operation": "Incremental Build Speed",
            "language_scores": {
                "Rust": 9.2, "Go": 8.0, "Swift": 7.5, "Kotlin": 8.5,
                "TypeScript": 7.0, "JavaScript": 10.0, "Java": 8.2, "C/C++": 7.0,
            },
            "unit": "relative (higher = faster)",
            "description": "Speed of recompiling after a small change",
        },
        {
            "operation": "Type Checking Cost",
            "language_scores": {
                "Rust": 3.0, "Go": 6.0, "Swift": 3.5, "Kotlin": 3.0,
                "TypeScript": 5.5, "JavaScript": 10.0, "Java": 6.0, "C/C++": 2.0,
            },
            "unit": "relative cost (lower = cheaper)",
            "description": "How expensive is the type system's work at compile time",
        },
        {
            "operation": "Binary Size Efficiency",
            "language_scores": {
                "Rust": 8.5, "Go": 6.0, "Swift": 6.5, "Kotlin": 8.0,
                "TypeScript": 10.0, "JavaScript": 10.0, "Java": 8.5, "C/C++": 7.5,
            },
            "unit": "relative (higher = smaller)",
            "description": "Typical binary size relative to functionality",
        },
        {
            "operation": "Cold Build Time",
            "language_scores": {
                "Rust": 4.0, "Go": 7.5, "Swift": 3.0, "Kotlin": 5.5,
                "TypeScript": 8.5, "JavaScript": 10.0, "Java": 5.8, "C/C++": 3.8,
            },
            "unit": "relative (higher = faster)",
            "description": "Time to build from scratch",
        },
        {
            "operation": "Cache Warmth",
            "language_scores": {
                "Rust": 8.5, "Go": 8.2, "Swift": 7.8, "Kotlin": 8.0,
                "TypeScript": 8.8, "JavaScript": 0.0, "Java": 8.1, "C/C++": 7.5,
            },
            "unit": "cache hit ratio (higher = better)",
            "description": "How well incremental compilation caches work",
        },
        {
            "operation": "Memory Usage During Build",
            "language_scores": {
                "Rust": 4.5, "Go": 6.5, "Swift": 3.0, "Kotlin": 4.0,
                "TypeScript": 7.5, "JavaScript": 10.0, "Java": 5.0, "C/C++": 3.5,
            },
            "unit": "relative (higher = less memory)",
            "description": "How memory-efficient the build process is",
        },
    ]


def build_optimization_recommendations(meta: Dict[str, Any]) -> List[str]:
    """Build optimization recommendations for a language."""
    recs = []
    tc_cost = meta["type_checker_cost"]

    if tc_cost == "very_high":
        recs.append("Consider using incremental compilation flags (-j for parallel)")
        recs.append("Split large modules to improve cache hit rates")
    elif tc_cost == "high":
        recs.append("Enable build cache if available (e.g., sbt for Scala)")
        recs.append("Use forward declarations to reduce type resolution depth")
    elif tc_cost == "medium":
        recs.append("Cache check results between builds")
    elif tc_cost in ("low", "none"):
        recs.append("Build system is lightweight; focus on runtime optimization")

    if meta["lto_overhead_s"] > 0:
        reduction_pct = (1.0 - meta["lto_binary_reduction"]) * 100
        recs.append(
            f"LTO adds {meta['lto_overhead_s']:.1f}s overhead "
            f"but reduces binary by {reduction_pct:.0f}% — use for release builds"
        )

    binary_note = f"{meta['binary_size_kb']}KB" if meta["binary_size_kb"] > 0 else "N/A (interpreted/transpiled)"
    recs.append(f"Binary size: {binary_note}")

    if meta["incremental_speedup"] > 5.0:
        recs.append(
            f"Incremental builds are {meta['incremental_speedup']:.1f}x faster "
            f"than cold builds — use often!"
        )

    return recs


def now_iso() -> str:
    """Return current timestamp in ISO format (Asia/Shanghai timezone)."""
    tz = timezone(timedelta(hours=8))
    return datetime.now(tz).isoformat()


# ─────────────────────────────────────────────────────────────────
# Core API
# ─────────────────────────────────────────────────────────────────

def compile_cache_analysis(language: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate compile cache analysis for the selected rotation language.

    Reads the rotation config, selects the current language, advances the
    rotation index, and returns detailed compilation pipeline metadata,
    cross-language benchmarks, pipeline diagrams, and optimization tips.

    Args:
        language: override the selected language (for testing)

    Returns:
        dict with full compile cache analysis
    """
    config = load_rotation()

    # Determine selected language (intersect config with our 8-language rotation)
    if language is None:
        idx = config.get("current_index", 0)
        config_lang = config["languages"][idx % len(config["languages"])]
        if config_lang in ROTATION_LANGUAGES:
            language = config_lang
        else:
            # Config has more languages than our 8-language rotation;
            # find the nearest rotation language forward
            rot_idx = 0
            language = ROTATION_LANGUAGES[rot_idx]

    # Get compiler metadata
    meta = COMPILER_META_DB.get(language)
    if meta is None:
        meta = COMPILER_META_DB["Rust"]
        language = "Rust"

    # Advance rotation within our 8-language rotation
    rot_idx = ROTATION_LANGUAGES.index(language) if language in ROTATION_LANGUAGES else 0
    next_idx = (rot_idx + 1) % len(ROTATION_LANGUAGES)
    next_lang = ROTATION_LANGUAGES[next_idx]

    # Also update the config file to track our position
    # Find where our language appears in the config (for continuity with other tools)
    try:
        config_idx = config["languages"].index(language)
    except ValueError:
        config_idx = rot_idx % len(config["languages"])

    # Build response
    pipeline_diagram = build_pipeline_diagram(meta)
    cross_language_benchmarks = build_benchmarks()
    optimization_recommendations = build_optimization_recommendations(meta)

    # Update rotation config — advance the position of our language in the config
    try:
        current_pos = config["languages"].index(language)
    except ValueError:
        current_pos = 0
    config["current_index"] = (current_pos + 1) % len(config["languages"])
    config["last_language"] = language
    config["updated_at"] = now_iso()
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "selected_emoji": LANG_EMOJI.get(language, "🔧"),
        "compiler_meta": meta,
        "cross_language_benchmarks": cross_language_benchmarks,
        "pipeline_diagram": pipeline_diagram,
        "optimization_recommendations": optimization_recommendations,
        "rotation": ROTATION_LANGUAGES,
        "next_language": next_lang,
        "timestamp": now_iso(),
    }


def pipeline_for(language: str) -> Optional[str]:
    """Get pipeline diagram for a specific language (no rotation update)."""
    meta = COMPILER_META_DB.get(language)
    if meta is None:
        return None
    return build_pipeline_diagram(meta)


# ─────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────

def run_tests() -> None:
    """Run all tests for the compile cache module."""
    passed = 0
    failed = 0

    def assert_eq(a, b, msg: str = "") -> None:
        nonlocal passed, failed
        if a == b:
            passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            failed += 1
            print(f"  ❌ FAIL: {msg} — expected {b!r}, got {a!r}")

    def assert_in(a: str, b, msg: str = "") -> None:
        nonlocal passed, failed
        if a in b:
            passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            failed += 1
            print(f"  ❌ FAIL: {msg} — '{a}' not found in {b!r}")

    def assert_true(a, msg: str = "") -> None:
        nonlocal passed, failed
        if a:
            passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            failed += 1
            print(f"  ❌ FAIL: {msg}")

    def assert_keys(d: Dict, expected_keys: List[str], msg: str = "") -> None:
        nonlocal passed, failed
        missing = [k for k in expected_keys if k not in d]
        if not missing:
            passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            failed += 1
            print(f"  ❌ FAIL: {msg} — missing keys: {missing}")

    print("Testing Polyglot Compile Cache...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_true(len(config["languages"]) >= 8, f"rotation has {len(config['languages'])} languages (>= 8)")
    assert_in("current_index", config, "current_index field present")

    print("  Testing compile_cache_analysis() output structure...")
    result = compile_cache_analysis()
    expected_keys = [
        "tool", "version", "selected_language", "selected_emoji",
        "compiler_meta", "cross_language_benchmarks", "pipeline_diagram",
        "optimization_recommendations", "rotation", "next_language", "timestamp"
    ]
    assert_keys(result, expected_keys, "All expected keys present")

    print("  Testing compiler_meta structure...")
    meta = result["compiler_meta"]
    assert_keys(meta, [
        "compiler", "version_hint", "pipeline", "incremental",
        "binary_size_kb", "optimization_passes", "type_checker_cost",
        "cold_build_time_s", "incremental_speedup", "memory_usage_mb",
        "lto_overhead_s", "lto_binary_reduction"
    ], "compiler_meta has all required fields")
    assert_true(isinstance(meta["pipeline"], list), "pipeline is a list")
    assert_true(len(meta["pipeline"]) >= 4, "pipeline has at least 4 stages")
    assert_true(meta["cold_build_time_s"] >= 0, "cold_build_time_s is non-negative")
    assert_true(meta["binary_size_kb"] >= 0, "binary_size_kb is non-negative")

    print("  Testing pipeline stages have required fields...")
    for stage in meta["pipeline"]:
        assert_true("name" in stage, "stage has name")
        assert_true("description" in stage, "stage has description")
        assert_true("duration_ms" in stage, "stage has duration_ms")
        assert_true("cacheable" in stage, "stage has cacheable")
        assert_true("parallelizable" in stage, "stage has parallelizable")
        assert_true(stage["duration_ms"] > 0, "duration_ms is positive")

    print("  Testing incremental result fields...")
    inc = meta["incremental"]
    assert_true("full_rebuild_ms" in inc, "incremental has full_rebuild_ms")
    assert_true("after_small_change_ms" in inc, "incremental has after_small_change_ms")
    assert_true("cache_hit_ratio" in inc, "incremental has cache_hit_ratio")
    assert_true(0.0 <= inc["cache_hit_ratio"] <= 1.0, "cache_hit_ratio is between 0 and 1")

    print("  Testing cross_language_benchmarks...")
    benchmarks = result["cross_language_benchmarks"]
    assert_true(len(benchmarks) >= 4, "at least 4 benchmark comparisons")
    for bc in benchmarks:
        assert_true("operation" in bc, "benchmark has operation")
        assert_true("language_scores" in bc, "benchmark has language_scores")
        assert_true("unit" in bc, "benchmark has unit")
        assert_eq(8, len(bc["language_scores"]), f"benchmark '{bc['operation']}' has 8 language scores")
        for lang in ROTATION_LANGUAGES:
            assert_true(lang in bc["language_scores"], f"benchmark has score for {lang}")

    print("  Testing pipeline_diagram contains language name...")
    diag = result["pipeline_diagram"]
    assert_true(result["selected_language"] in diag, "pipeline diagram contains selected language")
    assert_true("ms" in diag, "pipeline diagram shows timing")
    assert_true("│" in diag, "pipeline diagram has visual bars")

    print("  Testing optimization_recommendations not empty...")
    recs = result["optimization_recommendations"]
    assert_true(len(recs) > 0, "has at least one recommendation")

    print("  Testing rotation advances after compile_cache_analysis()...")
    idx_before = load_rotation()["current_index"]
    lang_before = load_rotation()["languages"][idx_before]
    result = compile_cache_analysis()
    idx_after = load_rotation()["current_index"]
    assert_true(idx_after != idx_before, "index changed after analysis")
    assert_eq(lang_before, load_rotation()["last_language"], "last_language recorded correctly")

    print("  Testing all 8 languages have compiler metadata...")
    for lang in ROTATION_LANGUAGES:
        assert_true(lang in COMPILER_META_DB, f"{lang} has compiler metadata")
        m = COMPILER_META_DB[lang]
        assert_true(len(m["pipeline"]) >= 4, f"{lang} pipeline has >= 4 stages")
        assert_true(len(m["optimization_passes"]) > 0, f"{lang} has optimization passes")

    print("  Testing JavaScript has zero build time...")
    js_meta = COMPILER_META_DB["JavaScript"]
    assert_eq(0.0, js_meta["cold_build_time_s"], "JS cold_build_time_s is 0")
    assert_eq(0, js_meta["binary_size_kb"], "JS binary_size_kb is 0")
    assert_eq(0.0, js_meta["incremental"]["full_rebuild_ms"], "JS incremental full_rebuild_ms is 0")

    print("  Testing type_checker_cost values vary across languages...")
    costs = set(COMPILER_META_DB[lang]["type_checker_cost"] for lang in ROTATION_LANGUAGES)
    assert_true(len(costs) > 1, "type_checker_cost varies across languages")

    print("  Testing LTO overhead values...")
    for lang in ROTATION_LANGUAGES:
        m = COMPILER_META_DB[lang]
        assert_true(m["lto_overhead_s"] >= 0, f"{lang} lto_overhead_s >= 0")
        assert_true(0.0 < m["lto_binary_reduction"] <= 1.0, f"{lang} lto_binary_reduction between 0 and 1")

    print("  Testing language emoji mapping...")
    for lang, emoji in LANG_EMOJI.items():
        result = compile_cache_analysis(language=lang)
        assert_eq(emoji, result["selected_emoji"], f"{lang} emoji is {emoji}")

    print("  Testing pipeline_for() helper...")
    diag = pipeline_for("Rust")
    assert_true(diag is not None, "pipeline_for('Rust') returns diagram")
    assert_in("Rust", diag, "diagram contains Rust")
    assert_true(pipeline_for("Python") is None, "pipeline_for('Python') returns None for unknown language")

    print("  Testing tool name and version in response...")
    assert_eq("polyglot-compile-cache", result["tool"], "correct tool name")
    assert_eq("1.0.0", result["version"], "correct tool version")

    print("  Testing next_language is different from selected_language...")
    assert_true(result["next_language"] != result["selected_language"], "next != selected")

    print("  Testing all languages have memory_usage_mb set...")
    for lang in ROTATION_LANGUAGES:
        m = COMPILER_META_DB[lang]
        assert_true("memory_usage_mb" in m, f"{lang} has memory_usage_mb")
        assert_true(m["memory_usage_mb"] >= 0, f"{lang} memory_usage_mb >= 0")

    print("  Testing all languages have incremental_speedup...")
    for lang in ROTATION_LANGUAGES:
        m = COMPILER_META_DB[lang]
        assert_true("incremental_speedup" in m, f"{lang} has incremental_speedup")
        assert_true(m["incremental_speedup"] >= 1.0, f"{lang} incremental_speedup >= 1.0")

    print(f"\n{'=' * 55}")
    print(f"Tests: {passed} passed, {failed} failed")
    if failed == 0:
        print("🎛️ All Compile Cache tests passed!")
    else:
        print(f"💥 {failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--analyze":
        result = compile_cache_analysis()
        print(json.dumps(result, indent=2))
    else:
        print(f"Polyglot Compile Cache v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m compile_cache --test      # Run tests")
        print("  python -m compile_cache --analyze  # Generate analysis")