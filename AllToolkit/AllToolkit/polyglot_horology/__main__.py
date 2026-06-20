#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🕰️ Polyglot Horology CLI

Usage:
  python -m polyglot_horology                    # movement report for rotation's current language
  python -m polyglot_horology Java               # movement report for an explicit language
  python -m polyglot_horology --test             # run self-tests
  python -m polyglot_horology --tour             # tour all 8 movements
  python -m polyglot_horology --compare A B      # chronometer comparison between A and B
  python -m polyglot_horology --current          # show current rotation language (no advance)
  python -m polyglot_horology --snippet "code"   # feed a snippet for crown-signature detection
"""

import sys
import os
import json

# Make sure the parent of this package directory is on sys.path so that
# `import polyglot_horology` works regardless of CWD.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_horology import (
    movement_report,
    movement_tour,
    chronometer_compare,
    get_current_language,
    run_tests,
    TOOL_NAME,
    TOOL_VERSION,
)


def main(argv: list) -> int:
    if argv and argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return 0

    if argv and argv[0] == "--test":
        failures = run_tests()
        return 0 if not failures else 1

    if argv and argv[0] == "--current":
        print(json.dumps({
            "tool": TOOL_NAME,
            "version": TOOL_VERSION,
            "current_language": get_current_language(),
        }, indent=2, ensure_ascii=False))
        return 0

    if argv and argv[0] == "--tour":
        result = movement_tour()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    if argv and argv[0] == "--compare":
        if len(argv) < 3:
            print("Usage: python -m polyglot_horology --compare <language_a> <language_b>")
            return 2
        result = chronometer_compare(argv[1], argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    # Parse optional --snippet flag
    snippet = ""
    args = [a for a in argv if not a.startswith("--snippet")]
    for i, a in enumerate(argv):
        if a == "--snippet" and i + 1 < len(argv):
            snippet = argv[i + 1]
            break

    language = args[0] if args else None
    advance = language is None  # only advance rotation when no explicit language was given

    try:
        result = movement_report(language=language, advance=advance, snippet=snippet)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    # Print a human-readable summary
    m = result["movement"]
    print(f"🕰️ {TOOL_NAME} v{TOOL_VERSION}")
    print(f"  Language: {result['current_language']}  •  Next: {result['next_language']}")
    print(f"  Archetype: {m['archetype']}")
    print(f"  Caliber:   {m['caliber']}  ({m['maker']}, {m['year_introduced']})")
    print(f"  Mainspring: {m['mainspring']}")
    print(f"  Escapement: {m['escapement']}")
    print(f"  Balance:    {m['balance_wheel']}")
    print()
    print(f"  Chronometric Index: {result['chronometric_rate']['chronometric_index']} "
          f"({result['chronometric_rate']['classification']})")
    print(f"  Power Reserve Era:  {result['power_reserve']['era']}")
    print(f"  Complication Rating: {result['complication_dial']['rating']}")
    print(f"  Vitality: {result['vitality']['score']}  ({result['vitality']['classification']})")
    print()
    print(f"  Crown signature: {result['crown_signature']['matched']}")
    print()
    print(f"  Dial face:")
    for line in result["dial_art"].splitlines():
        print(f"    {line}")
    print()
    print("  (full JSON available via import or --tour)")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
