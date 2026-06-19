#!/usr/bin/env python3
"""Polyglot Gauntlet CLI entry point."""

import sys
from pathlib import Path

# Ensure src is on path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gauntlet import get_gauntlet, format_gauntlet, run_tests

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--gauntlet":
        result = get_gauntlet()
        print(format_gauntlet(result))
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        import json
        result = get_gauntlet()
        print(json.dumps(result, indent=2))
    else:
        print(f"⚔️  Polyglot Gauntlet v1.0.0")
        print("Usage:")
        print("  python -m polyglot_gauntlet --gauntlet   # Issue gauntlet")
        print("  python -m polyglot_gauntlet --test        # Run tests")
        print("  python -m polyglot_gauntlet --json       # JSON output")
