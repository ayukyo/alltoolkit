#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⛪ Polyglot Cathedral CLI

Usage:
  python -m polyglot_cathedral                       # cathedral report for rotation's current language
  python -m polyglot_cathedral TypeScript           # cathedral report for an explicit language
  python -m polyglot_cathedral --test                # run self-tests
  python -m polyglot_cathedral --tour                # tour all 8 cathedrals
  python -m polyglot_cathedral --compare Rust Go     # side-by-side comparison of two cathedrals
  python -m polyglot_cathedral --current             # show current rotation language (no advance)
  python -m polyglot_cathedral --snippet "code..."   # feed a snippet for snippet-homing
"""

import sys
import json

# Ensure parent (AllToolkit/) is on the path so `import polyglot_cathedral` works
sys.path.insert(0, "/home/admin/.openclaw/workspace/AllToolkit")

from polyglot_cathedral import (
    cathedral_report,
    cathedral_tour,
    side_by_side_naves,
    get_current_language,
    run_tests,
    TOOL_NAME,
    TOOL_VERSION,
)


def main() -> int:
    args = sys.argv[1:]

    if args and args[0] in ("-h", "--help"):
        print(f"{TOOL_NAME} v{TOOL_VERSION}")
        print(
            "  python -m polyglot_cathedral [LANGUAGE|--test|--tour|--compare|--current]"
            "\n  [--snippet \"code\"]"
        )
        return 0

    # Optional --snippet flag for snippet-homing (valid for any report path)
    snippet = ""
    if "--snippet" in args:
        idx = args.index("--snippet")
        if idx + 1 < len(args):
            snippet = args[idx + 1]
        args = args[:idx] + args[idx + 2:]

    # If no positional args left, default to the rotation's current language
    if not args:
        report = cathedral_report(snippet=snippet, advance=True)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    if args[0] == "--test":
        failures = run_tests()
        if failures:
            print("FAIL")
            for f in failures:
                print(" -", f)
            return 1
        print("OK — all cathedral tests passed ⛪")
        return 0

    if args[0] == "--tour":
        print(json.dumps(cathedral_tour(), indent=2, ensure_ascii=False))
        return 0

    if args[0] == "--compare":
        if len(args) < 3:
            print("Usage: --compare <lang_a> <lang_b>")
            return 1
        print(json.dumps(
            side_by_side_naves(args[1], args[2]),
            indent=2, ensure_ascii=False,
        ))
        return 0

    if args[0] == "--current":
        print(f"Current rotation language: {get_current_language()}")
        return 0

    # Default: cathedral report for an explicit language (and advance rotation)
    language = args[0]
    report = cathedral_report(language=language, snippet=snippet, advance=True)

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())