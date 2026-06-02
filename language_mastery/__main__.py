#!/usr/bin/env python3
"""Entry point for language_mastery module."""
from . import run_tests, forge
import json
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--forge":
        language = sys.argv[2] if len(sys.argv) > 2 else "Rust"
        result = forge(language)
        print(json.dumps(result, indent=2))
    else:
        print("Language Mastery Forge v1.0.0")
        print("Usage: python -m AllToolkit.language_mastery --test")
        print("       python -m AllToolkit.language_mastery --forge [lang]")