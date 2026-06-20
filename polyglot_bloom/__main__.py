#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 Polyglot Bloom CLI

Usage:
  python -m polyglot_bloom                    # bloom report for rotation's current language
  python -m polyglot_bloom Java               # bloom report for an explicit language
  python -m polyglot_bloom --test             # run self-tests
  python -m polyglot_bloom --tour             # tour all 8 language gardens
  python -m polyglot_bloom --calendar [YEAR]  # year-long bloom calendar
  python -m polyglot_bloom --companion A B    # companion analysis between A and B
  python -m polyglot_bloom --current          # show current rotation language (no advance)
"""

import sys
import json

# Ensure parent (AllToolkit/) is on the path so `import polyglot_bloom` works
sys.path.insert(0, "/home/admin/.openclaw/workspace/AllToolkit")

from polyglot_bloom import (
    bloom_report,
    bloom_calendar,
    companion_analysis,
    garden_tour,
    get_current_language,
    run_tests,
    TOOL_NAME,
    TOOL_VERSION,
)


def main() -> int:
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(f"{TOOL_NAME} v{TOOL_VERSION}")
        print("  python -m polyglot_bloom [LANGUAGE|--test|--tour|--calendar|--companion|--current]")
        return 0

    if args[0] == "--test":
        failures = run_tests()
        if failures:
            print("FAIL")
            for f in failures:
                print(" -", f)
            return 1
        print("OK — all bloom tests passed 🌸")
        return 0

    if args[0] == "--tour":
        print(json.dumps(garden_tour(), indent=2, ensure_ascii=False))
        return 0

    if args[0] == "--calendar":
        year = int(args[1]) if len(args) > 1 else 2026
        print(json.dumps(bloom_calendar(year), indent=2, ensure_ascii=False))
        return 0

    if args[0] == "--companion":
        if len(args) < 3:
            print("Usage: --companion <lang_a> <lang_b>")
            return 1
        print(json.dumps(
            companion_analysis(args[1], args[2]),
            indent=2, ensure_ascii=False,
        ))
        return 0

    if args[0] == "--current":
        print(f"Current rotation language: {get_current_language()}")
        return 0

    # Default: bloom report (either for explicit language or rotation's current)
    language = args[0]
    print(json.dumps(
        bloom_report(language=language, advance=True),
        indent=2, ensure_ascii=False,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())