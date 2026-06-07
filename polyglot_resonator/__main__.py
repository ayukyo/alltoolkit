#!/usr/bin/env python3
"""Entry point for polyglot_resonator module."""

import sys
import os

# Ensure parent (AllToolkit/) is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_resonator import run_tests, resonator
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--resonate":
        result = resonator()
        print(json.dumps(result, indent=2))
    else:
        print("Polyglot Resonator v1.0.0")
        print("Usage:")
        print("  python -m polyglot_resonator --test       # Run tests")
        print("  python -m polyglot_resonator --resonate  # Generate resonance analysis")