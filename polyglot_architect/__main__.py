#!/usr/bin/env python3
"""Entry point for polyglot_architect module."""

import sys
import os

# Ensure parent (AllToolkit/) is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_architect.src import run_tests, architect, generate_architectural_analysis, format_architectural
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        result = architect()
        print(format_architectural(result))
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        result = architect()
        print(json.dumps(result, indent=2))
    else:
        print("🏛️ Polyglot Architect v1.0.0")
        print("  🏛️  ASCII architectural blueprints for how languages 'build' solutions.")
        print("")
        print("Usage:")
        print("  python -m polyglot_architect --test    # Run all tests")
        print("  python -m polyglot_architect --report   # Human-readable report")
        print("  python -m polyglot_architect --json      # JSON output")