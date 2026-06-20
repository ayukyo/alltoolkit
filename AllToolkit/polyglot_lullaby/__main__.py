#!/usr/bin/env python3
"""
🍼 Polyglot Lullaby CLI
Usage:
  python -m polyglot_lullaby                 # compose for the rotation's current language
  python -m polyglot_lullaby Rust            # compose for an explicit language
  python -m polyglot_lullaby --test          # run self-tests
  python -m polyglot_lullaby --advance       # rotate the language index and print the new state
"""

import sys
import json
from polyglot_lullaby import (
    compose_lullaby, load_rotation, advance_rotation, pick_language, run_tests, TOOL_NAME, TOOL_VERSION
)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(f"{TOOL_NAME} v{TOOL_VERSION}")
        print("  python -m polyglot_lullaby [LANGUAGE|--test|--advance]")
        return

    if args[0] == "--test":
        failures = run_tests()
        if failures:
            print("FAIL")
            for f in failures:
                print(" -", f)
            sys.exit(1)
        print("OK — self-tests passed")
        return

    if args[0] == "--advance":
        cfg = load_rotation()
        cfg = advance_rotation(cfg)
        print(json.dumps({
            "current_index": cfg["current_index"],
            "current_language": cfg["languages"][cfg["current_index"]],
            "last_language": cfg["last_language"],
            "updated_at": cfg["updated_at"],
        }, indent=2))
        return

    explicit = args[0] if not args[0].startswith("-") else None
    cfg = load_rotation()
    language = pick_language(cfg, explicit=explicit)
    snippet = " ".join(args[1:]) if len(args) > 1 else ""
    print(json.dumps(compose_lullaby(language, snippet), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
