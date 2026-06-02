#!/usr/bin/env python3
"""Entry point for language_compass module."""
from . import navigate, run_tests
import json
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--navigate":
        language = sys.argv[2] if len(sys.argv) > 2 else "Rust"
        result = navigate(language)
        print(json.dumps(result, indent=2))
    else:
        print("Language Compass v1.0.0")
        print("Usage:")
        print("  python -m language_compass --test        # Run tests")
        print("  python -m language_compass --navigate [lang]  # Chart a learning journey")