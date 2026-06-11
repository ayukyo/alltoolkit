#!/usr/bin/env python3
"""Entry point for polyglot_constellation module."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_constellation import run_tests, constellation
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--constellation":
        result = constellation()
        print(json.dumps(result, indent=2))
    else:
        print("Polyglot Constellation v1.0.0")
        print("  🌌 Every language is a star in the polyglot sky.")
        print("")
        print("Usage:")
        print("  python -m polyglot_constellation --test            # Run all tests")
        print("  python -m polyglot_constellation --constellation  # Generate constellation map")