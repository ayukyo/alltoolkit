#!/usr/bin/env python3
"""Entry point for polyglot_dna module."""

import sys
import os

# Ensure parent (AllToolkit/) is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_dna import run_tests, dna
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--dna":
        result = dna()
        print(json.dumps(result, indent=2))
    else:
        print("Polyglot DNA v1.0.0")
        print("  🧬 Every language has a genetic code.")
        print("")
        print("Usage:")
        print("  python -m polyglot_dna --test     # Run all tests")
        print("  python -m polyglot_dna --dna      # Generate DNA for current language")