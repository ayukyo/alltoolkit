#!/usr/bin/env python3
"""Entry point for language_fugue module."""

import sys
import os

# Ensure AllToolkit/ is on the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from language_fugue import fugue, run_tests
import json


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--fugue":
        result = fugue()
        print(json.dumps(result, indent=2))
    else:
        print(f"Language Fugue v1.0.0")
        print("Usage:")
        print("  python -m language_fugue --test    # Run tests")
        print("  python -m language_fugue --fugue  # Generate code composition")