#!/usr/bin/env python3
"""Entry point for language_archaeology module."""

import sys
from . import run_tests, dig

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--dig":
        import json
        language = sys.argv[2] if len(sys.argv) > 2 else "Rust"
        result = dig(language)
        print(json.dumps(result, indent=2))
    else:
        print("Language Archaeology v1.0.0")
        print("Usage:")
        print("  python -m language_archaeology --test   # Run tests")
        print("  python -m language_archaeology --dig [lang]  # Dig up language history")
