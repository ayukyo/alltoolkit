#!/usr/bin/env python3
"""Entry point for language_paradigm_weaver module."""
from . import paradigm_weaver, build_weave, run_tests
import json
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--weave":
        language = sys.argv[2] if len(sys.argv) > 2 else None
        result = paradigm_weaver(language)
        print(json.dumps(result, indent=2))
    else:
        print("Language Paradigm Weaver v1.0.0")
        print("Usage:")
        print("  python -m language_paradigm_weaver --test     # Run tests")
        print("  python -m language_paradigm_weaver --weave [lang]  # Build paradigm weave")