#!/usr/bin/env python3
"""Entry point for polyglot_faultline module."""
from . import excavate_faultline, rotate_and_update, run_tests
import json
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1 and sys.argv[1] == "--excavate":
        language = sys.argv[2] if len(sys.argv) > 2 else None
        result = excavate_faultline(language)
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "--rotate":
        result = rotate_and_update()
        print(json.dumps(result, indent=2))
    else:
        print("🌋 Polyglot Faultline v1.0.0")
        print("Usage:")
        print("  python -m polyglot_faultline --test       # Run tests")
        print("  python -m polyglot_faultline --excavate   # Excavate faultline for current language")
        print("  python -m polyglot_faultline --rotate     # Rotate and show next language")