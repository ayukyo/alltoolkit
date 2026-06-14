#!/usr/bin/env python3
"""Entry point for polyglot_resonance module."""

import sys
import os

# Ensure parent (AllToolkit/) is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_resonance.src import run_tests, resonance, generate_resonance_analysis, format_resonance
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--report":
        result = resonance()
        print(format_resonance(result))
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        result = resonance()
        print(json.dumps(result, indent=2))
    else:
        print("🎵 Polyglot Resonance v1.0.0")
        print("  🎵 Map how programming concepts vibrate differently across languages.")
        print("")
        print("Usage:")
        print("  python -m polyglot_resonance --test    # Run all tests")
        print("  python -m polyglot_resonance --report # Human-readable report")
        print("  python -m polyglot_resonance --json    # JSON output")
