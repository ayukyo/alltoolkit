#!/usr/bin/env python3
"""Entry point for polyglot_tarot module."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_tarot import (
    tarot,
    format_tarot_reading,
    run_tests,
    READING_ARCHETYPES,
    TOOL_NAME,
    TOOL_VERSION,
)
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        result = tarot()
        print(format_tarot_reading(result))
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        result = tarot()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif len(sys.argv) > 1 and sys.argv[1] == "--archetypes":
        print(f"🔮 {TOOL_NAME} v{TOOL_VERSION} — Available Archetypes\n")
        for arch in READING_ARCHETYPES:
            print(f"  {arch['emoji']} {arch['id']:<20} {arch['name']}")
            print(f"     {arch['question']}")
            print()
    else:
        print(f"🔮 {TOOL_NAME} v{TOOL_VERSION}")
        print("  The Programming Oracle — tarot readings for code concepts.\n")
        print("Usage:")
        print("  python -m polyglot_tarot --test       # Run all tests")
        print("  python -m polyglot_tarot --report     # Human-readable reading")
        print("  python -m polyglot_tarot --json       # JSON output")
        print("  python -m polyglot_tarot --archetypes # List all archetypes")
