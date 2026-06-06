#!/usr/bin/env python3
"""Entry point for polyglot_digest module."""

import sys
import os

# Ensure parent directory (AllToolkit/) is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polyglot_digest import run_tests, digest
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--digest":
        result = digest()
        print(json.dumps(result, indent=2))
    else:
        print("Polyglot Digest v1.0.0")
        print("Usage:")
        print("  python -m polyglot_digest --test     # Run tests")
        print("  python -m polyglot_digest --digest   # Generate digest")