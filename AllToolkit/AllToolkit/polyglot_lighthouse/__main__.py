#!/usr/bin/env python3
"""Entry point for the polyglot_lighthouse module."""

import sys
import os
import json

# Make sure the parent of this package directory is on sys.path so that
# `import polyglot_lighthouse` works regardless of CWD.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_lighthouse import (
    TOOL_NAME,
    TOOL_VERSION,
    lighthouse_report,
    light_list,
    bearing_between,
    safe_harbor,
    run_tests,
    get_current_language,
)


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        print(json.dumps(lighthouse_report(), indent=2, ensure_ascii=False))
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--lightlist":
        print(json.dumps(light_list(), indent=2, ensure_ascii=False))
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--bearing":
        if len(sys.argv) < 4:
            print("Usage: --bearing <language_a> <language_b>")
            sys.exit(1)
        print(json.dumps(
            bearing_between(sys.argv[2], sys.argv[3]),
            indent=2, ensure_ascii=False,
        ))
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--harbor":
        if len(sys.argv) < 3:
            print("Usage: --harbor <kw1,kw2,...>")
            sys.exit(1)
        keywords = [k.strip() for k in sys.argv[2].split(",") if k.strip()]
        print(json.dumps(safe_harbor(keywords), indent=2, ensure_ascii=False))
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--current":
        print(f"Current language: {get_current_language()}")
        return

    print(f"🗼 Polyglot Lighthouse v{TOOL_VERSION}")
    print("   Maritime navigation for programming languages.")
    print("")
    print("Usage:")
    print("  python -m polyglot_lighthouse --test            # Run all tests")
    print("  python -m polyglot_lighthouse --report          # Generate lighthouse report")
    print("  python -m polyglot_lighthouse --lightlist       # Show the full Light List")
    print("  python -m polyglot_lighthouse --bearing <a> <b>  # Bearing between two lighthouses")
    print("  python -m polyglot_lighthouse --harbor <kw1,kw2> # Find a safe harbor")
    print("  python -m polyglot_lighthouse --current         # Show current rotation language")


if __name__ == "__main__":
    main()