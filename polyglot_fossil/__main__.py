#!/usr/bin/env python3
"""CLI entry point for polyglot_fossil."""

import sys
import json
from pathlib import Path

TOOL_DIR = Path(__file__).parent
sys.path.insert(0, str(TOOL_DIR))

from polyglot_fossil.src.forge import fossil_dig


def main():
    args = sys.argv[1:]

    if "--test" in args:
        from polyglot_fossil.tests.test_fossil import run_tests
        run_tests()
        return

    if "--help" in args or "-h" in args:
        print("Polyglot Fossil v0.1.0")
        print("Usage:")
        print("  python -m polyglot_fossil [--test]")
        print("  python -m polyglot_fossil [--json]")
        print("  python -m polyglot_fossil [--language LANG]")
        return

    language = None
    if "--language" in args:
        idx = args.index("--language")
        if idx + 1 < len(args):
            language = args[idx + 1]

    as_json = "--json" in args

    result = fossil_dig(language=language)

    if as_json:
        # Exclude report for JSON output
        out = {k: v for k, v in result.items() if k != "report"}
        print(json.dumps(out, indent=2))
    else:
        print(result["report"])


if __name__ == "__main__":
    main()