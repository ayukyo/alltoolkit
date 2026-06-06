#!/usr/bin/env python3
"""Entry point for language_ethos module."""

import sys
from . import run_tests, ethos

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--ethos":
        import json
        language = sys.argv[2] if len(sys.argv) > 2 else None
        result = ethos(language)
        print(json.dumps(result, indent=2))
    else:
        print("Language Ethos v1.0.0")
        print("Usage:")
        print("  python -m language_ethos --test        # Run tests")
        print("  python -m language_ethos --ethos [lang]  # Distill language ethos")
