#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🪡 Polyglot Loom CLI

Usage:
  python -m polyglot_loom                    # loom report for rotation's current language
  python -m polyglot_loom Java               # loom report for an explicit language
  python -m polyglot_loom --test             # run self-tests
  python -m polyglot_loom --tour             # tour all 8 looms
  python -m polyglot_loom --dye A B          # dye comparison between A and B
  python -m polyglot_loom --current          # show current rotation language (no advance)
  python -m polyglot_loom --snippet "code"   # feed a snippet for weave-pattern detection
"""

import sys
import json

# Ensure parent (AllToolkit/) is on the path so `import polyglot_loom` works
sys.path.insert(0, "/home/admin/.openclaw/workspace/AllToolkit")

from polyglot_loom import (
    loom_report,
    loom_tour,
    dye_comparison,
    get_current_language,
    run_tests,
    TOOL_NAME,
    TOOL_VERSION,
)


def main() -> int:
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(f"{TOOL_NAME} v{TOOL_VERSION}")
        print(
            "  python -m polyglot_loom [LANGUAGE|--test|--tour|--dye|--current]"
            "\n  [--snippet \"code\"]"
        )
        return 0

    if args[0] == "--test":
        failures = run_tests()
        if failures:
            print("FAIL")
            for f in failures:
                print(" -", f)
            return 1
        print("OK — all loom tests passed 🪡")
        return 0

    if args[0] == "--tour":
        print(json.dumps(loom_tour(), indent=2, ensure_ascii=False))
        return 0

    if args[0] == "--dye":
        if len(args) < 3:
            print("Usage: --dye <lang_a> <lang_b>")
            return 1
        print(json.dumps(
            dye_comparison(args[1], args[2]),
            indent=2, ensure_ascii=False,
        ))
        return 0

    if args[0] == "--current":
        print(f"Current rotation language: {get_current_language()}")
        return 0

    # Optional --snippet flag for pattern detection
    snippet = ""
    if "--snippet" in args:
        idx = args.index("--snippet")
        if idx + 1 < len(args):
            snippet = args[idx + 1]
        args = args[:idx] + args[idx + 2:]

    # Default: loom report (either for explicit language or rotation's current)
    if not args:
        report = loom_report(snippet=snippet, advance=True)
    else:
        language = args[0]
        report = loom_report(language=language, snippet=snippet, advance=True)

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())