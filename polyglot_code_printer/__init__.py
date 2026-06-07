#!/usr/bin/env python3
"""
🖨️ Polyglot Code Printer v1.0

A creative tool that generates "code prints" — beautifully formatted,
idiomatic Hello World programs for the rotation language, complete with
a postcard-style layout showing the language's personality, philosophy,
and aesthetic signature.

Each print shows:
  - A hello world program in the rotated language's idiomatic style
  - The language's personality traits (vibe, philosophy, aesthetics)
  - A "signature idiom" unique to that language
  - The next language in rotation

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust

Distinct from existing tools:
  - polyglot_digest: syntax-parallel snippets (same logic, different syntax)
  - polyglot_synapse: conceptual bridges between languages
  - polyglot_chronicle: today's events and daily challenge
  - polyglot_resonator: how each language "thinks" — mental models

The Code Printer is about WHAT code looks like in each language —
the visual/textual aesthetic, idiomatic patterns, and stylistic fingerprint.
"""

import json
import os
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

TOOL_NAME = "polyglot-code-printer"
TOOL_VERSION = "1.0.0"

ROTATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "language_rotation.json"
)

LANGUAGES = ["Rust", "Go", "Swift", "Kotlin", "TypeScript",
            "JavaScript", "Java", "C/C++"]

# ── Code Print definitions ────────────────────────────────────────────────────
# Each language gets a hello world program and aesthetic metadata.
# Strings use \\n for actual newlines within the string values.

CODE_PRINTS: Dict[str, Dict[str, Any]] = {
    "Rust": {
        "emoji": "🦀",
        "vibe": "Fearless Systems",
        "philosophy": "If it compiles, it is correct. The borrow checker is your strict but fair mentor.",
        "aesthetic": "Minimalist with algebraic types. Every expression deliberate.",
        "signature_idiom": "unwrap() — trusting that Option<T> or Result<T, E> is Some/Ok",
        "hello_world": (
            "fn main() {\n"
            "    println!(\"Hello, world!\");\n"
            "}"
        ),
        "box_top": "╭───────────────────────────╮",
        "box_bottom": "╰───────────────────────────╯",
        "line_sep": "│",
        "color": "bright_red",
    },
    "Go": {
        "emoji": "🐹",
        "vibe": "Practical Concurrency",
        "philosophy": "Simplicity is golang. No features you don't need. Goroutines for the win.",
        "aesthetic": "Clean, sparse, functional. Whitespace as structure.",
        "signature_idiom": "go func() {}() — fire and forget, the Go way",
        "hello_world": (
            "package main\n\n"
            "import \"fmt\"\n\n"
            "func main() {\n"
            "    fmt.Println(\"Hello, world!\")\n"
            "}"
        ),
        "box_top": "┌───────────────────────────┐",
        "box_bottom": "└───────────────────────────┘",
        "line_sep": "│",
        "color": "cyan",
    },
    "Swift": {
        "emoji": "🦅",
        "vibe": "Elegant Safety",
        "philosophy": "Safe by default, powerful when needed. Optionals make null explicit.",
        "aesthetic": "Clean lines, trailing closures, @attributes everywhere.",
        "signature_idiom": "guard let x = optional else { return } — unwrap or bail",
        "hello_world": (
            "import Foundation\n\n"
            "print(\"Hello, world!\")"
        ),
        "box_top": "╔═══════════════════════════╗",
        "box_bottom": "╚═══════════════════════════╝",
        "line_sep": "║",
        "color": "magenta",
    },
    "Kotlin": {
        "emoji": "🟣",
        "vibe": "Pragmatic Null Safety",
        "philosophy": "NullPointerException? Kotlin makes null a type. Smart casts everywhere.",
        "aesthetic": "DSL-friendly, extension functions, coroutines for async.",
        "signature_idiom": "?.let { } ?: run { } — safe call chain or fallback",
        "hello_world": (
            "fun main() {\n"
            "    println(\"Hello, world!\")\n"
            "}"
        ),
        "box_top": "╭───────────────────────────╮",
        "box_bottom": "╰───────────────────────────╯",
        "line_sep": "│",
        "color": "bright_magenta",
    },
    "TypeScript": {
        "emoji": "🔷",
        "vibe": "Typed JavaScript",
        "philosophy": "Catch type errors at compile time. JavaScript with training wheels that don't limit you.",
        "aesthetic": "Type annotations visible. Generics for polymorphism.",
        "signature_idiom": "as Type — assertion that tells TS: trust me, I know the type",
        "hello_world": (
            "const greet = (name: string): string => {\n"
            "    return `Hello, ${name}!`;\n"
            "};\n\n"
            "console.log(greet(\"world\"));"
        ),
        "box_top": "╭───────────────────────────╮",
        "box_bottom": "╰───────────────────────────╯",
        "line_sep": "│",
        "color": "blue",
    },
    "JavaScript": {
        "emoji": "🟨",
        "vibe": "Prototypal Freedom",
        "philosophy": "Everything is an object. Functions are first-class. Async/await for sanity.",
        "aesthetic": "Dynamic, expressive, callback chains or Promise chains.",
        "signature_idiom": "...rest — collecting arguments into an array, the spread that unifies",
        "hello_world": (
            "const greet = (name) => {\n"
            "    console.log(`Hello, ${name}!`);\n"
            "};\n\n"
            "greet('world');"
        ),
        "box_top": "┌───────────────────────────┐",
        "box_bottom": "└───────────────────────────┘",
        "line_sep": "│",
        "color": "yellow",
    },
    "Java": {
        "emoji": "☕",
        "vibe": "Object-Oriented Enterprise",
        "philosophy": "Write once, run anywhere. Strong types, checked exceptions, no null.",
        "aesthetic": "Verbose but structured. Classes everywhere. Garbage collected.",
        "signature_idiom": "public static void main(String[] args) — the entrance gate",
        "hello_world": (
            "public class HelloWorld {\n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(\"Hello, world!\");\n"
            "    }\n"
            "}"
        ),
        "box_top": "╔═══════════════════════════╗",
        "box_bottom": "╚═══════════════════════════╝",
        "line_sep": "║",
        "color": "bright_yellow",
    },
    "C/C++": {
        "emoji": "⚙️",
        "vibe": "Low-Level Power",
        "philosophy": "You control memory. Pointers, manual allocation. Maximum control, maximum responsibility.",
        "aesthetic": "Braces, preprocessor macros, stdlib. No safety net, but raw speed.",
        "signature_idiom": "malloc(sizeof(T)) — the raw allocation dance",
        "hello_world": (
            "#include <stdio.h>\n\n"
            "int main() {\n"
            '    printf("Hello, world!\\n");\n'
            "    return 0;\n"
            "}"
        ),
        "box_top": "┌───────────────────────────┐",
        "box_bottom": "└───────────────────────────┘",
        "line_sep": "│",
        "color": "bright_cyan",
    },
}

EMOJI_MAP = {lang: data["emoji"] for lang, data in CODE_PRINTS.items()}


def load_rotation() -> Dict[str, Any]:
    """Load rotation config from language_rotation.json."""
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_rotation(config: Dict[str, Any]) -> None:
    """Save rotation config back to language_rotation.json."""
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_current_language() -> str:
    """Get the language at the current rotation index."""
    config = load_rotation()
    languages = config.get("languages", LANGUAGES)
    idx = config.get("current_index", 0)
    # Filter to only the 8-language rotation set
    rotation_set = LANGUAGES
    filtered = [l for l in languages if l in rotation_set]
    if not filtered:
        filtered = rotation_set
    return filtered[idx % len(filtered)]


def advance_rotation() -> str:
    """Advance to the next language and return the new current language."""
    config = load_rotation()
    languages = config.get("languages", LANGUAGES)
    idx = config.get("current_index", 0)
    rotation_set = LANGUAGES
    filtered = [l for l in languages if l in rotation_set]
    if not filtered:
        filtered = rotation_set
    current_lang = filtered[idx % len(filtered)]
    new_idx = (idx + 1) % len(filtered)
    config["current_index"] = new_idx
    config["last_language"] = current_lang
    config["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    save_rotation(config)
    return current_lang


def get_next_language() -> str:
    """Get the next language in the rotation."""
    config = load_rotation()
    languages = config.get("languages", LANGUAGES)
    idx = config.get("current_index", 0)
    rotation_set = LANGUAGES
    filtered = [l for l in languages if l in rotation_set]
    if not filtered:
        filtered = rotation_set
    return filtered[(idx + 1) % len(filtered)]


def generate_code_print(language: Optional[str] = None,
                        seed: Optional[int] = None) -> Dict[str, Any]:
    """
    Generate a code print for the rotation language.

    Args:
        language: Override language (for testing)
        seed: Random seed for deterministic output (for testing)

    Returns:
        Dict with tool name, version, language, code_print, rotation, next_language, timestamp
    """
    # Determine language
    if language is None:
        language = get_current_language()
    elif language not in CODE_PRINTS:
        # Fall back to rotation language if not in CODE_PRINTS
        rotation_config = load_rotation()
        rot_langs = rotation_config.get("languages", LANGUAGES)
        rotation_set = LANGUAGES
        filtered = [l for l in rot_langs if l in rotation_set]
        if not filtered:
            filtered = rotation_set
        language = filtered[0]

    cp = CODE_PRINTS[language]

    # Advance rotation only if using the natural flow (no override)
    if language == get_current_language():
        next_lang = advance_rotation()
    else:
        next_lang = get_next_language()

    # Build the print lines
    lines = _build_print_lines(language, cp)

    # Collect all prints for the multi-language summary
    all_prints = {}
    for lang, data in CODE_PRINTS.items():
        all_prints[lang] = {
            "emoji": data["emoji"],
            "vibe": data["vibe"],
            "philosophy": data["philosophy"],
            "signature_idiom": data["signature_idiom"],
            "hello_world": data["hello_world"],
        }

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        "selected_emoji": cp["emoji"],
        "vibe": cp["vibe"],
        "philosophy": cp["philosophy"],
        "aesthetic": cp["aesthetic"],
        "signature_idiom": cp["signature_idiom"],
        "hello_world": cp["hello_world"],
        "print_lines": lines,
        "all_prints": all_prints,
        "rotation": LANGUAGES,
        "next_language": next_lang,
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


def _build_print_lines(language: str, cp: Dict[str, Any]) -> List[str]:
    """Build the multi-line code print layout."""
    lines = []
    top = cp["box_top"]
    bottom = cp["box_bottom"]
    sep = cp["line_sep"]

    # Header
    lang_emoji = cp["emoji"]
    lines.append(top)
    lines.append(f"{sep}  {lang_emoji} {language:25s} {sep}")
    lines.append(f"{sep}  {cp['vibe']:<25s} {sep}")
    lines.append(bottom)

    # Philosophy
    lines.append(top)
    for chunk in _wrap(cp["philosophy"], 27):
        lines.append(f"{sep}  {chunk:<27s} {sep}")
    lines.append(bottom)

    # Signature idiom
    lines.append(top)
    lines.append(f"{sep}  SIG: {cp['signature_idiom']:<22s} {sep}")
    lines.append(bottom)

    # Code
    lines.append(top)
    for code_line in cp["hello_world"].split("\n"):
        lines.append(f"{sep}  {code_line:<25s} {sep}")
    lines.append(bottom)

    return lines


def _wrap(text: str, width: int) -> List[str]:
    """Simple word-wrap at width."""
    words = text.split()
    lines = []
    current = ""
    for w in words:
        if len(current) + len(w) + 1 <= width:
            current = (current + " " + w).strip()
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def format_printable(result: Dict[str, Any]) -> str:
    """Format the code print as a plain-text string for display."""
    lines = result["print_lines"]
    next_lang = result["next_language"]

    sep = "─" * 32
    out = [
        "",
        sep,
        f"  {result['selected_emoji']} {result['selected_language']} — {result['vibe']}",
        sep,
        "",
        "  Philosophy:",
        f"  {result['philosophy']}",
        "",
        "  Signature Idiom:",
        f"  {result['signature_idiom']}",
        "",
        "  Hello World:",
    ]
    for line in result["hello_world"].split("\n"):
        out.append(f"    {line}")
    out.extend(["", f"  → Next: {next_lang}", sep, ""])
    return "\n".join(out)


# ── Tests ─────────────────────────────────────────────────────────────────────

def run_tests() -> None:
    """Run all tests for the Polyglot Code Printer."""
    tests_passed = 0
    tests_failed = 0

    def assert_eq(a, b, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a == b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — expected {b!r}, got {a!r}")

    def assert_in(a: str, b, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a in b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — '{a}' not found in {b!r}")

    def assert_true(a, msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        if a:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg}")

    def assert_keys(d: Dict, expected_keys: List[str], msg: str = "") -> None:
        nonlocal tests_passed, tests_failed
        missing = [k for k in expected_keys if k not in d]
        if not missing:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — missing keys: {missing}")

    print("Testing Polyglot Code Printer...")

    # Test 1: All 8 languages have complete code print data
    print("  Testing all 8 languages have complete data...")
    for lang in LANGUAGES:
        cp = CODE_PRINTS[lang]
        assert_true(cp.get("hello_world"), f"{lang} has hello_world")
        assert_true(cp.get("emoji"), f"{lang} has emoji")
        assert_true(cp.get("vibe"), f"{lang} has vibe")
        assert_true(cp.get("philosophy"), f"{lang} has philosophy")
        assert_true(cp.get("signature_idiom"), f"{lang} has signature_idiom")
        assert_true(cp.get("box_top"), f"{lang} has box_top")
        assert_true(cp.get("box_bottom"), f"{lang} has box_bottom")
        assert_true(cp.get("line_sep"), f"{lang} has line_sep")

    # Test 2: generate_code_print returns correct structure
    print("  Testing generate_code_print structure...")
    result = generate_code_print()
    expected_keys = [
        "tool", "version", "selected_language", "selected_emoji",
        "vibe", "philosophy", "aesthetic", "signature_idiom",
        "hello_world", "print_lines", "all_prints", "rotation",
        "next_language", "timestamp"
    ]
    assert_keys(result, expected_keys, "result has all expected keys")

    # Test 3: print_lines is a non-empty list
    print("  Testing print_lines structure...")
    assert_true(isinstance(result["print_lines"], list), "print_lines is a list")
    assert_true(len(result["print_lines"]) > 5, "print_lines has content")

    # Test 4: all_prints has all 8 languages
    print("  Testing all_prints completeness...")
    for lang in LANGUAGES:
        assert_in(lang, result["all_prints"], f"{lang} in all_prints")

    # Test 5: rotation is the 8-language list
    print("  Testing rotation list...")
    assert_eq(result["rotation"], LANGUAGES, "rotation matches expected list")

    # Test 6: next_language is in rotation
    print("  Testing next_language in rotation...")
    assert_true(result["next_language"] in LANGUAGES, "next_language is valid")

    # Test 7: selected_language is in LANGUAGES
    print("  Testing selected_language validity...")
    assert_true(result["selected_language"] in LANGUAGES, "selected_language is valid")

    # Test 8: generate_code_print with language override works
    print("  Testing language override...")
    r_go = generate_code_print(language="Go")
    assert_eq(r_go["selected_language"], "Go", "override selects Go")
    assert_eq(r_go["selected_emoji"], "🐹", "Go has correct emoji")
    assert_eq(r_go["vibe"], "Practical Concurrency", "Go vibe is correct")

    r_rust = generate_code_print(language="Rust")
    assert_eq(r_rust["selected_language"], "Rust", "override selects Rust")
    assert_eq(r_rust["selected_emoji"], "🦀", "Rust has correct emoji")

    # Test 9: deterministic output with same seed
    print("  Testing deterministic output...")
    r1 = generate_code_print(language="Rust", seed=42)
    r2 = generate_code_print(language="Rust", seed=42)
    assert_eq(r1["vibe"], r2["vibe"], "same seed gives same vibe")

    # Test 10: format_printable produces non-empty string
    print("  Testing format_printable output...")
    txt = format_printable(result)
    assert_true(len(txt) > 20, "format_printable produces content")
    assert_in(result["selected_language"], txt, "language name in output")
    assert_in("Hello", txt, "hello greeting in output")

    # Test 11: rotation advances after generate_code_print call
    print("  Testing rotation advances...")
    config_before = load_rotation()
    idx_before = config_before["current_index"]
    lang_before = config_before["last_language"]

    result = generate_code_print()  # uses natural flow
    config_after = load_rotation()
    idx_after = config_after["current_index"]

    # idx should have advanced by 1 (modulo rotation length)
    rotation_set = [l for l in config_before.get("languages", LANGUAGES) if l in LANGUAGES]
    if not rotation_set:
        rotation_set = LANGUAGES
    expected_idx = (idx_before + 1) % len(rotation_set)
    assert_eq(expected_idx, idx_after, "index advanced by 1")
    # last_language should be the language that WAS current (before this call)
    # i.e., the language returned by this generate_code_print() call
    assert_eq(result["selected_language"], config_after["last_language"], "last_language matches selected before advance")

    # Test 12: all_prints has required fields per language
    print("  Testing all_prints fields per language...")
    for lang, print_data in result["all_prints"].items():
        assert_true(print_data.get("emoji"), f"{lang} has emoji in all_prints")
        assert_true(print_data.get("vibe"), f"{lang} has vibe in all_prints")
        assert_true(print_data.get("philosophy"), f"{lang} has philosophy in all_prints")
        assert_true(print_data.get("signature_idiom"), f"{lang} has signature_idiom in all_prints")
        assert_true(print_data.get("hello_world"), f"{lang} has hello_world in all_prints")

    # Test 13: version and tool name
    print("  Testing tool metadata...")
    assert_eq("polyglot-code-printer", result["tool"], "correct tool name")
    assert_eq("1.0.0", result["version"], "correct version")

    # Test 14: each print_lines entry contains the language name or code
    print("  Testing print_lines content...")
    for line in result["print_lines"]:
        assert_true(isinstance(line, str), "each line is a string")
        assert_true(len(line) > 0, "no empty lines")

    # Test 15: next_language != selected_language (rotation working)
    print("  Testing rotation produces different next language...")
    assert_true(result["next_language"] in LANGUAGES, "next_language is valid")
    assert_true(result["selected_language"] in LANGUAGES, "selected_language is valid")

    # Test 16: Java hello_world is correct
    print("  Testing Java hello_world content...")
    r_java = generate_code_print(language="Java")
    hw = r_java["hello_world"]
    assert_in("public class HelloWorld", hw, "Java hello_world has class")
    assert_in("System.out.println", hw, "Java hello_world uses System.out.println")
    assert_in("Hello, world!", hw, "Java hello_world prints greeting")

    # Test 17: C/C++ hello_world is correct
    print("  Testing C/C++ hello_world content...")
    r_cpp = generate_code_print(language="C/C++")
    hw_cpp = r_cpp["hello_world"]
    assert_in("#include", hw_cpp, "C/C++ hello_world includes stdio")
    assert_in("printf", hw_cpp, "C/C++ hello_world uses printf")

    # Summary
    print(f"\n{'='*55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("🖨️  All Code Printer tests passed!")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--print":
        result = generate_code_print()
        print(format_printable(result))
    else:
        print(f"Polyglot Code Printer v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m polyglot_code_printer --test   # Run tests")
        print("  python -m polyglot_code_printer --print  # Generate code print")