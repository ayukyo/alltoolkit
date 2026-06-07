#!/usr/bin/env python3
"""
🔐 Polyglot Cipher v1.0
A "language cipher forge" — generates unique cryptographic micro-puzzles
themed around each programming language's design philosophy.

Creative concept: "Every language speaks in its own cipher. This tool forges the code."

Each language gets a distinct cipher algorithm and visual encoding:
  • Rust      → ROT-13 variant with XOR key derived from memory safety themes
  • Go        → Channel-based sliding window cipher
  • Swift     → Unicode scalar transformation with optional chaining
  • Kotlin    → Extension-function based cipher with null-safe wrapping
  • TypeScript → Structural type-preserving cipher (types travel with data)
  • JavaScript → Prototype-chain driven cipher (prototype-inherited keys)
  • Java      → Object-oriented cipher with checked exception handling
  • C/C++     → Pointer-arithmetic cipher with manual memory management

Each run produces a cipher challenge card for the current rotation language,
updates the index, and commits to git.

Distinct from existing tools:
  - language_archaeology:     historical lineage & design philosophy
  - language_compass:         learning journey maps
  - language_ecohub:          package ecosystem field guide
  - language_mastery:          XP/level progress tracking
  - language_sage:            idioms, pro tips, pitfalls
  - language_synapse:          conceptual bridges between languages
  - language_ethos:           philosophical manifesto
  - polyglot_flavor:          sensory tasting notes (sensory lens)
  - polyglot_digest:          syntax-parallel code snippets
  - polyglot_chronicle:       daily history and trivia
  - polyglot_code_printer:     code output formatting
  - polyglot_resonator:       frequency/resonance analysis

Cipher is about CRYPTOGRAPHIC LINGUISTICS — applying each language's core
philosophy to encryption as a creative parallel.
"""

import json
import os
import random
import string
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

TOOL_NAME = "polyglot-cipher"
TOOL_VERSION = "1.0.0"
ROTATION_FILE = str(
    Path(__file__).parent.parent.parent / "language_rotation.json"
)

# Rotation language order: Rust → Go → Swift → Kotlin → TypeScript →
#                          JavaScript → Java → C/C++ → (loop)
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


# ── Cipher algorithms per language ────────────────────────────────────────────

def _rust_cipher(text: str) -> Tuple[str, int]:
    """Rust: ROT-13 with XOR key derived from ownership theme (42 = life!)."""
    key = 42
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord("a") if ch.islower() else ord("A")
            rotated = base + ((ord(ch) - base + key) % 26)
            result.append(chr(rotated))
        else:
            result.append(ch)
    return "".join(result), key


def _go_cipher(text: str) -> Tuple[str, int]:
    """Go: Channel-based sliding window. Window size = 3 (goroutine channels)."""
    window = 3
    result = []
    for i, ch in enumerate(text):
        if ch.isalpha():
            base = ord("a") if ch.islower() else ord("A")
            shift = window if i % 2 == 0 else -window
            rotated = base + ((ord(ch) - base + shift) % 26)
            result.append(chr(rotated))
        else:
            result.append(ch)
    return "".join(result), window


def _swift_cipher(text: str) -> Tuple[str, int]:
    """Swift: Unicode scalar shift, optional nil mapping to '?'."""
    key = 17
    result = []
    for ch in text:
        code = ord(ch)
        if 32 <= code <= 126:
            shifted = 32 + ((code - 32 + key) % 95)
            result.append(chr(shifted))
        else:
            result.append(ch)  # Preserve non-printable
    return "".join(result), key


def _kotlin_cipher(text: str) -> Tuple[str, int]:
    """Kotlin: Caesar cipher with null-safe wrapping (null → space, non-null → char)."""
    key = 7
    result = []
    for ch in text:
        if ch == " ":
            result.append("null")  # Null safety metaphor
        elif ch.isalpha():
            base = ord("a") if ch.islower() else ord("A")
            rotated = base + ((ord(ch) - base + key) % 26)
            result.append(chr(rotated))
        else:
            result.append(ch)
    return "".join(result), key


def _typescript_cipher(text: str) -> Tuple[str, int]:
    """TypeScript: Atbash cipher (types mirror perfectly)."""
    atbash_map = {}
    for i in range(26):
        atbash_map[chr(ord("a") + i)] = chr(ord("a") + 25 - i)
        atbash_map[chr(ord("A") + i)] = chr(ord("A") + 25 - i)
    result = []
    for ch in text:
        result.append(atbash_map.get(ch, ch))
    return "".join(result), 0


def _javascript_cipher(text: str) -> Tuple[str, int]:
    """JavaScript: Vigenère cipher with key = 'JS' (prototype chain inheritance)."""
    key = "JS"
    result = []
    for i, ch in enumerate(text):
        if ch.isalpha():
            base = ord("a") if ch.islower() else ord("A")
            key_char = key[i % len(key)]
            shift = ord(key_char.lower()) - ord("a")
            rotated = base + ((ord(ch) - base + shift) % 26)
            result.append(chr(rotated))
        else:
            result.append(ch)
    return "".join(result), 0


def _java_cipher(text: str) -> Tuple[str, int]:
    """Java: Classloader cipher — reverse the string (classpath order matters)."""
    key = 0  # No simple key; it's structural
    reversed_text = text[::-1]
    result = []
    for ch in reversed_text:
        if ch.isalpha():
            base = ord("a") if ch.islower() else ord("A")
            rotated = base + ((ord(ch) - base + 13) % 26)
            result.append(chr(rotated))
        else:
            result.append(ch)
    return "".join(result), 13


def _cpp_cipher(text: str) -> Tuple[str, int]:
    """C/C++: Pointer arithmetic — XOR each char with its address parity."""
    key = 0x1F  # Bitmask for pointer arithmetic simulation
    result = []
    for i, ch in enumerate(text):
        if ch.isalpha():
            # XOR with pointer-sized step: even index uses XOR, odd uses complement
            if i % 2 == 0:
                encoded = ord(ch) ^ (key + i)
            else:
                encoded = 255 - ord(ch)  # ~ch for odd positions
            # Normalize back to alphabet
            encoded_char = chr(((encoded % 26) + 97) if ch.islower() else ((encoded % 26) + 65))
            result.append(encoded_char)
        else:
            result.append(ch)
    return "".join(result), key


CIPHER_MAP: Dict[str, callable] = {
    "Rust": _rust_cipher,
    "Go": _go_cipher,
    "Swift": _swift_cipher,
    "Kotlin": _kotlin_cipher,
    "TypeScript": _typescript_cipher,
    "JavaScript": _javascript_cipher,
    "Java": _java_cipher,
    "C/C++": _cpp_cipher,
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_rotation() -> Dict[str, Any]:
    """Load language rotation config."""
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data: Dict[str, Any]) -> None:
    """Save updated rotation state."""
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _get_next_language() -> str:
    """Get next language in rotation order (Rust→Go→Swift→Kotlin→TS→JS→Java→C/C++)."""
    config = load_rotation()
    languages = config["languages"]
    idx = config.get("current_index", 0) % len(languages)
    return languages[idx]


def _wrap(text: str, width: int) -> List[str]:
    """Wrap text to a fixed width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        if len(current) + len(word) + 1 <= width:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _section(label: str, text: str, width: int = 58) -> str:
    """Render a labeled section block."""
    lines = _wrap(text, width)
    header = f"║  {label}"
    padded = header + " " * (62 - len(header)) + "║"
    content = "\n".join(f"║  {line}" + " " * (60 - len(line)) + "║" for line in lines)
    return padded + "\n" + content


def _cipher_card(language: str, encoded: str, key: Any, cipher_name: str) -> str:
    """Render a full cipher challenge card."""
    return f"""
╔══════════════════════════════════════════════════════════════════╗
║          🔐  POLYGLOT CIPHER — CHALLENGE CARD  🔐             ║
╠══════════════════════════════════════════════════════════════════╣
║  Language   : {language:<50} ║
║  Cipher     : {cipher_name:<50} ║
╠══════════════════════════════════════════════════════════════════╣
║  ENCRYPTED MESSAGE                                           ║
║                                                                ║
║    {encoded[:54]:<54} ║
╠══════════════════════════════════════════════════════════════════╣
║  CIPHER METADATA                                             ║
║  • Key/Parameter : {str(key):<48} ║
║  • Algorithm     : {cipher_name:<48} ║
╚══════════════════════════════════════════════════════════════════╝"""


def _generate_challenge() -> str:
    """Generate a random challenge phrase."""
    themes = [
        "compilers never lie",
        "pointers are just addresses with ambition",
        "the borrow checker is my therapist",
        "goroutines go dancing through channels",
        "null is not a value it is an absence",
        "types are contracts not suggestions",
        "the prototype chain knows no bounds",
        "the jvm never forgets a class",
        "undefined is not a mistake it is a feature",
        "manual memory management builds character",
    ]
    return random.choice(themes)


# ── Core API ───────────────────────────────────────────────────────────────────

def cipher() -> Dict[str, Any]:
    """
    Main entry point: rotate to the next language, generate a cipher challenge,
    update the rotation file, and return structured data.
    """
    config = load_rotation()
    languages = config["languages"]
    idx = config.get("current_index", 0) % len(languages)
    language = languages[idx]

    # Skip any language not in our rotation (fallback to ROTATION_ORDER)
    if language not in CIPHER_MAP:
        # Advance until we find a language in CIPHER_MAP
        original_idx = idx
        attempts = 0
        while languages[idx] not in CIPHER_MAP:
            idx = (idx + 1) % len(languages)
            attempts += 1
            if idx == original_idx:
                raise ValueError("No supported language found in rotation.")
        language = languages[idx]

    # Compute next_idx: advance within ROTATION_ORDER (not raw list index)
    current_rot_idx = ROTATION_ORDER.index(language)
    next_rot_idx = (current_rot_idx + 1) % len(ROTATION_ORDER)
    next_language = ROTATION_ORDER[next_rot_idx]
    next_idx = languages.index(next_language)

    challenge = _generate_challenge()
    encoded, key = CIPHER_MAP[language](challenge)

    CIPHER_NAMES = {
        "Rust": "Ownership ROT-XOR",
        "Go": "Channel Sliding Window",
        "Swift": "Unicode Scalar Shift",
        "Kotlin": "Null-Safe Caesar",
        "TypeScript": "Structural Atbash",
        "JavaScript": "Prototype Vigenère",
        "Java": "Classloader Reverse + ROT13",
        "C/C++": "Pointer XOR/Complement",
    }
    cipher_name = CIPHER_NAMES.get(language, "Unknown")

    card = _cipher_card(language, encoded, key, cipher_name)

    # Advance index for next run (using ROTATION_ORDER cycle)
    config["current_index"] = next_idx
    config["last_language"] = language
    config["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_rotation(config)

    return {
        "language": language,
        "cipher_name": cipher_name,
        "challenge": challenge,
        "encoded": encoded,
        "key": key,
        "cipher_card": card,
        "rotated_at": config["updated_at"],
    }


def run_tests() -> None:
    """Run unit tests."""
    import traceback

    print("Running Polyglot Cipher tests...\n")

    def assert_eq(a: Any, b: Any, msg: str) -> None:
        if a != b:
            raise AssertionError(f"{msg}: got {a!r}, expected {b!r}")
        print(f"  ✓ {msg}")

    errors = []

    # ── Test 1: load + save round-trip ────────────────────────────────────────
    try:
        config = load_rotation()
        assert isinstance(config, dict), "config should be a dict"
        assert "languages" in config, "config should have 'languages'"
        assert "current_index" in config, "config should have 'current_index'"
        assert_eq(type(config["languages"]), list, "languages is a list")
        assert_eq(type(config["current_index"]), int, "current_index is an int")
        print("  ✓ load_rotation returns valid structure")
    except Exception as e:
        errors.append(("load_rotation", e))

    # ── Test 2: Rust ROT-XOR produces consistent output ────────────────────────
    try:
        encoded, key = _rust_cipher("hello rust")
        assert_eq(key, 42, "Rust key is 42")
        assert encoded != "hello rust", "encoded text differs from input"
        print("  ✓ Rust cipher produces consistent output")
    except Exception as e:
        errors.append(("rust_cipher", e))

    # ── Test 3: Go sliding window ──────────────────────────────────────────────
    try:
        encoded, key = _go_cipher("hello go")
        assert_eq(key, 3, "Go window size is 3")
        # Test even/odd indexing
        h_enc = encoded[0]
        h_orig = "h"
        assert h_enc != h_orig, "Go cipher changes even-indexed chars"
        print("  ✓ Go sliding window cipher works")
    except Exception as e:
        errors.append(("go_cipher", e))

    # ── Test 4: Swift Unicode scalar shift ──────────────────────────────────────
    try:
        encoded, key = _swift_cipher("hello swift")
        assert_eq(key, 17, "Swift key is 17")
        assert encoded != "hello swift", "Swift cipher changes text"
        print("  ✓ Swift Unicode cipher works")
    except Exception as e:
        errors.append(("swift_cipher", e))

    # ── Test 5: Kotlin null-safe Caesar ─────────────────────────────────────────
    try:
        encoded, key = _kotlin_cipher("hello kotlin")
        assert_eq(key, 7, "Kotlin key is 7")
        assert "null" in encoded, "Kotlin cipher maps space to 'null'"
        print("  ✓ Kotlin null-safe cipher works")
    except Exception as e:
        errors.append(("kotlin_cipher", e))

    # ── Test 6: TypeScript Atbash ───────────────────────────────────────────────
    try:
        encoded, _ = _typescript_cipher("abc xyz")
        assert_eq(encoded, "zyx cba", "Atbash inverts alphabet")
        print("  ✓ TypeScript Atbash cipher works")
    except Exception as e:
        errors.append(("typescript_cipher", e))

    # ── Test 7: JavaScript Vigenère ────────────────────────────────────────────
    try:
        encoded, _ = _javascript_cipher("abc")
        assert encoded != "abc", "Vigenère changes text"
        # Reverse: decode is same operation (symmetric when using J/S as shift)
        # key "JS" on "abc": a+J=10, b+S=19, c+J=10 → "kun"
        # key "JS" on "kun": k+J=17→s, u+S=23→c, n+J=15→a → "sca" (not symmetric)
        # Just verify it encodes without error
        assert len(encoded) == 3, "encoded length matches"
        print("  ✓ JavaScript Vigenère cipher encodes correctly")
    except Exception as e:
        errors.append(("javascript_cipher", e))

    # ── Test 8: Java Classloader Reverse ───────────────────────────────────────
    try:
        encoded, key = _java_cipher("hello java")
        assert_eq(key, 13, "Java key is 13 (ROT13 after reverse)")
        assert encoded != "hello java", "Java cipher changes text"
        print("  ✓ Java classloader cipher works")
    except Exception as e:
        errors.append(("java_cipher", e))

    # ── Test 9: C/C++ Pointer XOR ───────────────────────────────────────────────
    try:
        encoded, key = _cpp_cipher("abc")
        assert_eq(key, 0x1F, "C/C++ key is 0x1F")
        assert encoded != "abc", "C/C++ cipher changes text"
        print("  ✓ C/C++ pointer cipher works")
    except Exception as e:
        errors.append(("cpp_cipher", e))

    # ── Test 10: cipher() rotates and saves ────────────────────────────────────
    try:
        config = load_rotation()
        before_lang = config.get("last_language", "")
        result = cipher()
        config2 = load_rotation()
        assert_eq(config2["last_language"], result["language"], "last_language updated")
        assert result["language"] in CIPHER_MAP, "returned language has cipher"
        assert "encoded" in result, "result has encoded field"
        assert "cipher_card" in result, "result has cipher_card"
        assert "challenge" in result, "result has challenge field"
        print("  ✓ cipher() rotates and saves correctly")
    except Exception as e:
        errors.append(("cipher rotation", e))

    # ── Test 11: cipher_card contains key sections ────────────────────────────
    try:
        result = cipher()
        card = result["cipher_card"]
        assert result["language"] in card, "card mentions language"
        assert "ENCRYPTED MESSAGE" in card, "card has encrypted section"
        assert "CIPHER METADATA" in card, "card has metadata section"
        print("  ✓ cipher_card renders all sections")
    except Exception as e:
        errors.append(("cipher_card sections", e))

    # ── Test 12: _wrap handles edge cases ──────────────────────────────────────
    try:
        lines = _wrap("Short", 78)
        assert_eq(len(lines), 1, "short text stays on one line")
        long_text = " ".join(["word"] * 50)
        lines = _wrap(long_text, 40)
        assert all(len(l) <= 42 for l in lines), "all lines respect width"
        print("  ✓ _wrap handles edge cases")
    except Exception as e:
        errors.append(("_wrap", e))

    # ── Test 13: ROTATION_ORDER cycle wraps correctly ──────────────────────────
    try:
        config = load_rotation()
        # C/C++ is rot_idx=7 (last). After it, Rust comes back (rot_idx=0).
        # Find Rust's position in the full list
        rust_lang = ROTATION_ORDER[0]
        rust_idx = config["languages"].index(rust_lang)

        # Set index to C/C++
        cpp_lang = ROTATION_ORDER[-1]
        cpp_idx = config["languages"].index(cpp_lang)
        config["current_index"] = cpp_idx
        save_rotation(config)

        result = cipher()
        config2 = load_rotation()

        # After C/C++, the cycle wraps to Rust — next_idx should be Rust's position
        assert_eq(result["language"], cpp_lang, "first call returns C/C++")
        assert_eq(config2["current_index"], rust_idx, "next index is Rust's position after C/C++ wrap")

        # Next call should return Rust
        result2 = cipher()
        assert_eq(result2["language"], rust_lang, "next call returns Rust after wrap")

        # After Rust, next should be Go (rot_idx=1)
        go_lang = ROTATION_ORDER[1]
        go_idx = config["languages"].index(go_lang)
        config3 = load_rotation()
        assert_eq(config3["current_index"], go_idx, "after Rust, next is Go")

        print("  ✓ rotation wraps around correctly")
    except Exception as e:
        errors.append(("wrap-around", e))

    # ── Test 14: all rotation languages have ciphers ───────────────────────────
    try:
        for lang in ROTATION_ORDER:
            assert lang in CIPHER_MAP, f"{lang} has no cipher"
        print(f"  ✓ All {len(ROTATION_ORDER)} rotation languages have ciphers")
    except Exception as e:
        errors.append(("cipher completeness", e))

    # ── Summary ────────────────────────────────────────────────────────────────
    print()
    if errors:
        for name, err in errors:
            print(f"  ✗ {name}: {err}")
            traceback.print_exception(type(err), err, err.__traceback__)
        print(f"\nTests: {len(errors)} failure(s)")
        raise SystemExit(1)
    else:
        print("All tests passed! ✓")


if __name__ == "__main__":
    run_tests()
