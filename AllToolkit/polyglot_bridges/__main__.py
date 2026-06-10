#!/usr/bin/env python3
"""Entry point for polyglot_bridges module."""
from . import semantic_bridge, build_bridge, run_tests
import json
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--bridge":
        language = sys.argv[2] if len(sys.argv) > 2 else None
        result = semantic_bridge(language)
        print(json.dumps(result, indent=2))
    else:
        print("Polyglot Semantic Bridges v1.0.0")
        print("Usage:")
        print("  python -m polyglot_bridges --test        # Run tests")
        print("  python -m polyglot_bridges --bridge [lang]  # Build semantic bridge")