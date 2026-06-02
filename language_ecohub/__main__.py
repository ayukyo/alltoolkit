#!/usr/bin/env python3
"""Entry point for language_ecohub module."""
from . import explore, run_tests
import json
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--explore":
        language = sys.argv[2] if len(sys.argv) > 2 else "Rust"
        result = explore(language)
        print(json.dumps(result, indent=2))
    else:
        print("Language EcoHub v1.0.0")
        print("Usage:")
        print("  python -m language_ecohub --test        # Run tests")
        print("  python -m language_ecohub --explore [lang]  # Explore ecosystem")