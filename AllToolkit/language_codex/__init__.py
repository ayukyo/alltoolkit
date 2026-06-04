#!/usr/bin/env python3
"""
📜 Language Codex v1.0
A creative tool that uncovers the SECRET SYNTAX — hidden idioms, Easter eggs,
and "secret handshakes" that language docs DON'T tell you about.

Creative concept: "Every language has fingerprints. This tool finds them."
Each language reveals:
  - The Weird Compound Assignment nobody teaches
  - The Elvis Operator / Null Shortcut
  - The Underdocumented Operator Nobody Knows
  - The "But Why Does This Work?" corner case
  - The Secret Unicode Weapon
  - The "Wait, That's Legal?!" syntax quirk

Distinct from existing tools:
  - language_compass: learning journey maps (milestones)
  - language_archaeology: historical roots and design philosophy
  - language_ecohub: package ecosystem field guide
  - language_sage: idioms, pro tips, pitfalls
  - language_mastery: XP/level progress tracking

Codex is about HIDDEN DEPTHS — undocumented tricks and syntactic oddities.
"""

import json
import os
import random
from datetime import datetime, timezone, timedelta

TOOL_NAME = "language-codex"
TOOL_VERSION = "1.0.0"
# Resolves to: AllToolkit/AllToolkit/language_codex/__init__.py → AllToolkit/AllToolkit/language_rotation.json
ROTATION_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "language_rotation.json")


def load_rotation():
    with open(ROTATION_FILE, "r") as f:
        return json.load(f)


def save_rotation(data):
    with open(ROTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Secret Syntax / Hidden Depths per language ────────────────────────────────
CODEX_DATA = {
    "Rust": {
        "weird_compound": "x += { let t = 1; t };  // block expressions as assignment values",
        "elvis_null": "let val = value ?? default;  // nil coalescing",
        "underdocumented": "dbg!(&x);  // debug macro that prints location!",
        "but_why": "for i in 0.. { println!(\"{}\", i); }  // infinite range — no Eq bound needed",
        "unicode_weapon": "let 🦀 = \"crab\";  // unicode identifiers fully valid",
        "wait_legal": "let (x,): (i32,) = (5,);  // tuple destructuring with trailing comma",
        "secret_fact": "Rust's turbofish ::<T> solves ambiguous type inference in generics",
        "idiom": "impl AsRef<str> for String { fn as_ref(&self) -> &str { self } }  // identity impl",
    },
    "Go": {
        "weird_compound": "x, _ = fn()  // discards second return with blank identifier",
        "elvis_null": "if v := getVal(); v != nil { return v }  // short-circuit evaluation",
        "underdocumented": "go func() {}()  // immediately-invoked goroutine",
        "but_why": "i := interface{}(&s)  // any type holds any pointer",
        "unicode_weapon": "variable := \"你好世界\"  // UTF-8 source, fully valid identifiers",
        "wait_legal": "const (a, b = iota, iota+1; c = iota)  // iota reuse in same const group",
        "secret_fact": "go run -ldflags '-s -w' strips binary size dramatically",
        "idiom": "for range s { if s[i] == 'x' { break } }  // index capture via range",
    },
    "Swift": {
        "weird_compound": "result = a ?? b ?? c  // chained nil coalescing",
        "elvis_null": "let val = value ?? defaultValue  // nil coalescing operator",
        "underdocumented": "@_transparent @inline(__always)  // internal inlining hints",
        "but_why": "let f: (inout Int) -> Void = { $0 += 1 }  // inout in closure",
        "unicode_weapon": "let 名前 = \"Taro\"; let ✅ = true  // any unicode in identifiers",
        "wait_legal": "enum E { case a, b; static let x = Self.a }  // Self in static",
        "secret_fact": "Swift's #file, #line, #column are compile-time literals",
        "idiom": "guard let x = try? mightThrow() else { return }  // try? + guard",
    },
    "Kotlin": {
        "weird_compound": "x += y;  // also supports x -= y, x *= y for appropriate types",
        "elvis_null": "val safe: String? = nullable ?: \"default\"  // elvis operator",
        "underdocumented": "inline fun <reified T> foo() = T::class.java  // reified generics",
        "but_why": "val items: List<out Any> = listOf<Int>()  // covariance with out",
        "unicode_weapon": "val 이름 = \"Park\"; val 氏名 = \"Tanaka\"  // CJK identifiers",
        "wait_legal": "when (x) { in 1..10 -> print(\"range!\"); !in 11..20 -> print(\"not\") }",
        "secret_fact": "import kotlin.random.*; val x = Random.nextInt() avoids java.util.Random",
        "idiom": "sequence { for (i in 1..) yield(i * i) }.take(5).toList()  // lazy sequences",
    },
    "TypeScript": {
        "weird_compound": "obj?.prop?.nested ?? 'default'  // optional chaining + elvis",
        "elvis_null": "const val = nullable ?? fallback  // nullish coalescing",
        "underdocumented": "declare module '*.txt' { const value: string; export default value; }",
        "but_why": "type X = {} extends { x: any } ? true : false  // empty object extends anything",
        "unicode_weapon": "const 名前 = 'Taro'; type 姓名 = string  // any unicode in types",
        "wait_legal": "[...[1, 2, 3]]  // spread inside array pattern — valid destructuring",
        "secret_fact": "tsc --noEmit --incremental for faster subsequent type checks",
        "idiom": "type Flatten<T> = T extends Array<infer U> ? Flatten<U> : T  // recursive infer",
    },
    "JavaScript": {
        "weird_compound": "a ||= b; a &&= c  // logical assignment operators (ES2021)",
        "elvis_null": "const val = null ?? 'default'  // nullish coalescing (ES2020)",
        "underdocumented": "void 0  // reliable undefined substitute",
        "but_why": "typeof null === 'object'  // historical bug that's now permanent",
        "unicode_weapon": "const 名前 = 'Taro'; const 🎉 = 'party'  // emoji identifiers",
        "wait_legal": "[] == false, [] == 0, ![] == false  // truthy quirks of empty arrays",
        "secret_fact": "Object.is(a, b) differs from === in NaN handling and +/-0",
        "idiom": "for (const [k, v] of Object.entries(obj)) {}  // clean key-value iteration",
    },
    "Java": {
        "weird_compound": "i += j * k  // compound assignment with evaluation order difference",
        "elvis_null": "String safe = Objects.requireNonNullElse(val, \"default\")  // J9+",
        "underdocumented": "varhandle = MethodHandles.lookup().findStatic(...)  // Java 9+",
        "but_why": "Integer cache -128 to 127 means == works unexpectedly on boxed ints",
        "unicode_weapon": "String 名前 = \"Taro\"; String 🎉 = \"party\"  // unicode identifiers",
        "wait_legal": "int[] a = new int[0];  // zero-length arrays are perfectly valid",
        "secret_fact": "jshell --enable-preview for REPL with newest Java features",
        "idiom": "try (var sc = new Scanner(System.in)) {}  // try-with-resources",
    },
    "C/C++": {
        "weird_compound": "x = y = z = 0;  // chained assignment, all get 0",
        "elvis_null": "ptr ? ptr->field : default  // ternary as elvis substitute",
        "underdocumented": "__builtin_expect(cond, 1)  // branch prediction hint",
        "but_why": "int *p = (int *)(void *)ptr;  // void* requires explicit cast",
        "unicode_weapon": "int 名前 = 42;  // C++11 allows u8, u16, u32 prefixed unicode",
        "wait_legal": "int arr[100]; int(*p)[100] = &arr;  // pointer to entire array",
        "secret_fact": "0xCCCCCCCC fill pattern detects use-after-free in debug builds",
        "idiom": "for (int i = 0; i < n; ++i) {}  // ++i preferred over i++ in loops",
    },
}


# ── Codex entry builder ───────────────────────────────────────────────────────
def build_codex_entry(language):
    """Build a complete codex entry for the given language."""
    data = CODEX_DATA.get(language)
    if not data:
        return None

    return {
        "language": language,
        "entries": {
            "weird_compound_assignment": data["weird_compound"],
            "elvis_null_operator": data["elvis_null"],
            "underdocumented_operator": data["underdocumented"],
            "but_why_this_works": data["but_why"],
            "unicode_weapon": data["unicode_weapon"],
            "wait_thats_legal": data["wait_legal"],
            "secret_fact": data["secret_fact"],
            "signature_idiom": data["idiom"],
        },
        "discovered_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


# ── Main entry ────────────────────────────────────────────────────────────────
def reveal(language):
    """
    Main entry: reveal hidden syntax for selected language.
    Reads rotation, selects language, generates codex, advances rotation.
    """
    config = load_rotation()

    if language not in config["languages"]:
        raise ValueError(
            f"Language '{language}' not in rotation. "
            f"Available: {', '.join(config['languages'])}"
        )

    current_idx = config["languages"].index(language)
    next_idx = (current_idx + 1) % len(config["languages"])

    codex = build_codex_entry(language)

    config["current_index"] = next_idx
    config["last_language"] = language
    save_rotation(config)

    return {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "selected_language": language,
        **codex,
        "next_language": config["languages"][next_idx],
        "rotation": config["languages"],
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
    }


# ── Tests ─────────────────────────────────────────────────────────────────────
def run_tests():
    """Run validation tests for the Language Codex module."""
    tests_passed = 0
    tests_failed = 0

    def assert_eq(a, b, msg=""):
        nonlocal tests_passed, tests_failed
        if a == b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — expected {b!r}, got {a!r}")

    def assert_in(a, b, msg=""):
        nonlocal tests_passed, tests_failed
        if a in b:
            tests_passed += 1
            print(f"  ✅ PASS: {msg}")
        else:
            tests_failed += 1
            print(f"  ❌ FAIL: {msg} — '{a}' not found in response")

    print("Testing Language Codex...")

    print("  Loading rotation config...")
    config = load_rotation()
    assert_eq(8, len(config["languages"]), "8 languages in rotation")
    assert_eq(True, 0 <= config["current_index"] < 8, "current_index in valid range")
    assert_eq("Rust", config["languages"][0], "Rust is first language")

    print("  Testing reveal for Rust...")
    result = reveal("Rust")
    assert_eq("Rust", result["selected_language"], "Rust is selected")
    assert_eq("Go", result["next_language"], "Next language is Go")
    assert_in("tool", result.keys(), "tool field present")
    assert_in("version", result.keys(), "version field present")
    assert_in("entries", result.keys(), "entries field present")

    print("  Verifying codex entry structure...")
    entries = result["entries"]
    required_keys = [
        "weird_compound_assignment", "elvis_null_operator",
        "underdocumented_operator", "but_why_this_works",
        "unicode_weapon", "wait_thats_legal",
        "secret_fact", "signature_idiom"
    ]
    for key in required_keys:
        assert_in(key, entries.keys(), f"Entry '{key}' present")
    assert_eq(8, len(entries), "All 8 entry types present")

    print("  Testing reveal for Go...")
    result2 = reveal("Go")
    assert_eq("Go", result2["selected_language"], "Go is selected")
    assert_eq("Swift", result2["next_language"], "Next language is Swift")
    entries2 = result2["entries"]
    assert_eq(True, len(entries2) == 8, "Go codex has 8 entries")

    print("  Testing all 8 languages have codex data...")
    for lang in config["languages"]:
        codex_data = CODEX_DATA.get(lang)
        assert_eq(True, codex_data is not None, f"Codex data exists for {lang}")
        expected_keys = [
            "weird_compound", "elvis_null", "underdocumented",
            "but_why", "unicode_weapon", "wait_legal",
            "secret_fact", "idiom"
        ]
        for key in expected_keys:
            assert_eq(True, key in codex_data, f"{lang} has '{key}' field")

    print("  Testing rotation advancement...")
    config_before = load_rotation()
    idx_before = config_before["current_index"]
    last_before = config_before["last_language"]
    result3 = reveal(config_before["languages"][idx_before])
    config_after = load_rotation()
    assert_eq(idx_before, config_after["current_index"] - 1 if config_after["current_index"] > 0 else 7,
             "current_index advanced by 1 (with wrap)")
    assert_eq(result3["selected_language"], config_after["last_language"],
             "last_language updated to selected language")

    print("  Testing invalid language raises ValueError...")
    try:
        reveal("Python")
        tests_failed += 1
        print("  ❌ FAIL: No error for invalid language")
    except ValueError as e:
        tests_passed += 1
        print(f"  ✅ PASS: ValueError raised for invalid language")
        assert_in("not in rotation", str(e), "Error mentions rotation")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ FAIL: Wrong exception: {e}")

    print("  Testing discovered_at timestamp is ISO format...")
    result4 = reveal("Kotlin")
    assert_in("T", result4["discovered_at"], "ISO timestamp present")

    print("  Testing entry values are non-empty strings...")
    for lang in config["languages"]:
        result5 = reveal(lang)
        for entry_name, entry_value in result5["entries"].items():
            assert_eq(True, isinstance(entry_value, str) and len(entry_value) > 0,
                     f"{lang}: '{entry_name}' is a non-empty string")

    print(f"\n{'='*55}")
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")
    if tests_failed == 0:
        print("📜 All codex tests passed! Hidden syntax revealed.")
    else:
        print(f"💥 {tests_failed} test(s) failed.")
        raise SystemExit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--reveal":
        language = sys.argv[2] if len(sys.argv) > 2 else "Rust"
        result = reveal(language)
        print(json.dumps(result, indent=2))
    else:
        print(f"Language Codex v{TOOL_VERSION}")
        print("Usage:")
        print("  python -m language_codex --test       # Run tests")
        print("  python -m language_codex --reveal [lang]  # Reveal hidden syntax")